# Closest Distributors Finder (CRM + Google Maps)

**Developed by Critical Hits LLC**  
**Available via [Vikuno](https://vikuno.com)**

---

## About Vikuno

[Vikuno](https://vikuno.com) is your hub for powerful, production-ready Odoo modules. Built by **Critical Hits LLC**, our solutions help businesses unlock more value from Odoo through automation, smart integrations, and user-friendly design.

---

## Module: Closest Distributors Finder

This module extends the CRM Lead functionality in Odoo to automatically find the **3 closest distributors** based on real-world travel distances. It integrates with the **Google Maps Distance Matrix API**, seamlessly handled via Vikuno’s backend service—**no API setup required**.

### 🔑 Key Features

- 🔍 **Automatic Distance Calculation** using Google Maps
- 📍 **Identifies 3 Closest Distributors** per CRM Lead
- 🔐 **Vikuno-Hosted API Access** — no configuration required
- 🖱️ **One-Click Distributor Search** in CRM Leads
- 🧱 **Clean Error Handling & Logging** for visibility and debugging
- ✅ **Validates Addresses** before making API requests

---

## Installation

1. Install the module via **Apps** in your Odoo instance.
2. Ensure all distributor contacts are tagged with the **"Distributor"** category.
3. Make sure CRM lead partners and distributors have **complete addresses**.

---

## Usage

### 🧭 Finding Closest Distributors

1. Open a **CRM Lead** with a linked partner.
2. Click the **"Find Closest Distributors"** button.
3. The 3 nearest distributors will be automatically filled in based on driving distance.

### 🏷️ Setting Up Distributors

- Go to **Contacts**.
- Edit or create any partner that serves as a distributor.
- Add the **"Distributor"** tag under categories.
- Ensure their **address is complete** (street, city, state, zip, country).

---

## Server Action (Automation)

This module includes a reusable **server action** for workflow automation:

- **Name**: `Find Closest Distributors`
- **Model**: `CRM Lead`
- **Available in**: CRM Lead list and form views

Perfect for integration with scheduled jobs or rule-based automation.

---

## Technical Details

### 📦 Dependencies

- `crm` – CRM lead management
- `contacts` – Partner records
- `base` – Odoo core system

### 🧠 Logic & Models

- `crm.lead`: Extended to store closest distributors
- `res.partner`: Used to identify and filter distributor records
- `google.maps.helper`: Abstracted logic for distance calculation
- `res.config.settings`: Internal use only (no configuration required)

### 🌐 API Integration

- Uses **Google Maps Distance Matrix API** via **Vikuno’s secure proxy**
- Calculates driving distance between the lead’s partner and distributor addresses
- Returns the **top 3 closest** based on travel time
- Graceful handling of edge cases and errors

---

## Troubleshooting

### Common Issues

- ❌ **“No distributors found”**  
  → Ensure the "Distributor" tag is applied and address fields are complete

- ❌ **“Partner has no address”**  
  → Add a full address to the CRM lead’s associated partner

- ⚠️ **API request failed**  
  → Check Odoo logs for address formatting or network issues

### Logging

- Detailed logs are written to standard Odoo logs:
  - API responses
  - Errors and exceptions
  - Address validation checks

---

## Security Notes

- 🔐 No API keys are needed — all external communication is securely proxied via Vikuno
- 🔒 HTTPS used for all outbound requests
- ⏱️ Timeout and error protection is built in to prevent hanging or abuse

---

## Support & Customization

For questions, custom feature requests, or technical help, visit [Vikuno](https://vikuno.com) or contact **Critical Hits LLC**.

---

## Explore More from Vikuno

Looking for more powerful tools to supercharge Odoo?

👉 [Vikuno.com](https://vikuno.com)  
🛠️ Modules for inventory, delivery optimization, CRM, and more  
🚀 Built and supported by Critical Hits LLC

---
