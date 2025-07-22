#############################################################################
#
#    Critical Hits LLC
#
#    Copyright (C) 2025-TODAY Critical Hits LLC(<https://www.vikuno.com>)
#    Author: Critical Hits LLC(<https://www.vikuno.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    "name": "Easy Distro - Find the closest warehouse",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Find the closest distributor for any of your contacts.",
    "description": """
        Find the closest Distributor for any of your contacts with the click of a button.
        Requires subscription activation for Google Maps API access.
    """,
    "author": "Critical Hits LLC",
    "company": "Critical Hits LLC",
    "maintainer": "Critical Hits LLC",
    "website": "https://vikuno.com",
    "depends": [
        "base",
        "crm",
        "contacts",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "data": [
        "views/crm_views.xml",
        "views/res_config_settings_views.xml",
        "data/model_load_stub.xml",
    ],
    "price": 70,
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
