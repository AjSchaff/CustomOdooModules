import requests
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # API endpoints (these will be appended to the base URL)
    SUBSCRIPTION_CHECK_ENDPOINT = "/api/check-subscription"
    GOOGLE_DISTANCE_MATRIX_ENDPOINT = "/api/google/distance-matrix"

    # Subscription fields
    subscription_id = fields.Char(
        string="Subscription ID",
        help="Enter your subscription ID from the purchase confirmation",
        config_parameter="easy_distro.subscription_id",
    )

    # Activation tracking fields
    activated = fields.Boolean(
        string="Activated",
        config_parameter="easy_distro.activated",
        default=False,
        help="Whether this subscription has been activated",
    )

    activated_by = fields.Char(
        string="Activated By",
        config_parameter="easy_distro.activated_by",
        help="Email address of the user who activated this subscription",
    )

    def _get_vercel_api_base_url(self):
        """Return the correct Vercel API base URL depending on environment."""
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        if "localhost" in (base_url or ""):
            return "http://localhost:3000"
        return "http://vikuno"

    def easy_distro_call_vercel_api(self, data, endpoint=None):
        """Make API call to Vercel with proper error handling"""
        if endpoint is None:
            endpoint = self.SUBSCRIPTION_CHECK_ENDPOINT

        url = f"{self._get_vercel_api_base_url()}{endpoint}"

        try:
            response = requests.post(
                url, json=data, headers={"Content-Type": "application/json"}, timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code == 404:
                raise UserError(_("Subscription Code not found."))
            elif status_code == 400:
                raise UserError(_("This subscription is not for this module."))
            else:
                _logger.error(
                    f"HTTP error when calling Vercel API: {url}, Status: HTTP {status_code}"
                )
                raise UserError(_(f"Subscription service error: HTTP {status_code}"))
        except requests.exceptions.RequestException as e:
            _logger.error(
                f"HTTP error when calling Vercel API: {url}, Status: {str(e)}"
            )
            raise UserError(_(f"Subscription service error: {str(e)}"))

    def easy_distro_check_subscription_status(self):
        """Check subscription status using your Vercel API"""
        if not self.subscription_id:
            raise UserError(_("Please enter a subscription ID first."))

        user_email = self.env.user.email
        if not user_email:
            raise UserError(
                _("User email is required. Please set your email in your user profile.")
            )

        try:
            data = {
                "subscriptionId": self.subscription_id,
                "email": user_email,
                "moduleName": "easy-distro",
            }
            response = self.easy_distro_call_vercel_api(data, "/api/check-subscription")
            if response.get("valid"):
                message = response.get("message", "Subscription validated successfully")
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Subscription"),
                        "message": f"✅ {message}",
                        "type": "success",
                        "sticky": False,
                    },
                }
            else:
                error_msg = response.get("message", "Subscription validation failed")
                raise UserError(_(error_msg))
        except Exception as e:
            _logger.error(f"Failed to check subscription via Vercel API: {str(e)}")
            raise UserError(_("Subscription service error: %s") % str(e))

    def easy_distro_get_subscription_status(self):
        # For button in UI
        active = self.easy_distro_check_subscription_status_vercel()
        status = "active" if active else "inactive"
        raise UserError(f"Subscription Status: {status}")

    def easy_distro_check_subscription_status_vercel(self):
        """Check if subscription is active via Vercel API"""
        subscription_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("easy_distro.subscription_id")
        )
        if not subscription_id:
            return False

        try:
            data = {"subscriptionId": subscription_id, "moduleName": "easy-distro"}
            response = self.easy_distro_call_vercel_api(data, "/api/check-subscription")
            return response.get("valid", False)
        except Exception as e:
            _logger.error(f"Failed to check subscription status: {str(e)}")
            return False
