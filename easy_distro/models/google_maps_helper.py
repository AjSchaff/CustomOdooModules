import requests
import logging
from odoo import models, _

_logger = logging.getLogger(__name__)


class GoogleMapsHelper(models.AbstractModel):
    _name = "google.maps.helper"
    _description = "Google Maps Integration Helper"

    # API endpoints (these will be appended to the base URL)
    SUBSCRIPTION_CHECK_ENDPOINT = "/api/check-subscription"
    GOOGLE_DISTANCE_MATRIX_ENDPOINT = "/api/google/distance-matrix"

    def _get_vercel_api_base_url(self):
        """Return the correct Vercel API base URL depending on environment."""
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        if "localhost" in (base_url or ""):
            return "http://localhost:3000"
        return "http://vikuno"

    def _format_address(self, partner):
        """Format partner address for Google Maps API"""
        address_parts = []

        if partner.street:
            address_parts.append(partner.street)
        if partner.street2:
            address_parts.append(partner.street2)
        if partner.city:
            address_parts.append(partner.city)
        if partner.state_id and partner.state_id.name:
            address_parts.append(partner.state_id.name)
        if partner.zip:
            address_parts.append(partner.zip)
        if partner.country_id and partner.country_id.name:
            address_parts.append(partner.country_id.name)

        if not address_parts:
            return None

        return ", ".join(address_parts)

    def get_distance_matrix(self, origin, destinations):
        """Proxy call to Server for Google Maps Distance Matrix."""
        # Check subscription status first
        if not self._check_subscription_active():
            _logger.warning(
                "EasyDistro subscription not active. Please activate your subscription."
            )
            return False

        url = f"{self._get_vercel_api_base_url()}{self.GOOGLE_DISTANCE_MATRIX_ENDPOINT}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Odoo-EasyDistro/1.0",
        }

        # Format addresses
        origin_str = self._format_address(origin)
        if not origin_str:
            _logger.error("Origin partner %s has no valid address", origin.name)
            return False

        # Format destination addresses
        dest_addresses = []
        valid_destinations = []

        for dest in destinations:
            dest_str = self._format_address(dest)
            if dest_str:
                dest_addresses.append(dest_str)
                valid_destinations.append(dest)
            else:
                _logger.warning(
                    "Destination partner %s has no valid address, skipping", dest.name
                )

        if not dest_addresses:
            _logger.error("No valid destination addresses found")
            return False

        data = {"origin": origin_str, "destinations": dest_addresses}

        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            response.raise_for_status()
            result = response.json()
            if result.get("status") == "OK":
                return result
            else:
                _logger.error("Google Maps API error: %s", result.get("status"))
                return False
        except Exception as e:
            _logger.info(
                "Error calling Google Maps API. A Subscription is required. Post install, go to https://vikuno.com/ to subscribe: %s",
                str(e),
            )
            return False

    def _check_subscription_active(self):
        """Check if EasyDistro subscription is active"""
        try:
            easy_distro_subscription_id = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("easy_distro.easy_distro_subscription_id")
            )
            if not easy_distro_subscription_id:
                return False

            # Call Vercel API to check subscription status
            url = f"{self._get_vercel_api_base_url()}{self.SUBSCRIPTION_CHECK_ENDPOINT}"
            data = {
                "subscriptionId": easy_distro_subscription_id,
                "email": self.env.user.email,
                "moduleName": "easy-distro",
            }

            response = requests.post(
                url, json=data, headers={"Content-Type": "application/json"}, timeout=10
            )
            response.raise_for_status()
            result = response.json()

            return result.get("valid", False)
        except Exception as e:
            _logger.error(f"Failed to check EasyDistro subscription status: {str(e)}")
            return False
