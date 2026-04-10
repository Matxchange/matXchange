<div align="center">

# MatXchange ♻️
### The Circular Economy OS for Africa

*Digitizing informal waste collection — paying pickers instantly — anchoring every kilogram to the blockchain*

[![License: MIT](https://img.shields.io/badge/License-MIT-2ECC71.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Frappe-v16-0089FF.svg?style=flat-square)](https://frappeframework.com)
[![Blockchain](https://img.shields.io/badge/Stellar-Testnet-7B68EE.svg?style=flat-square)](https://stellar.org)
[![Payments](https://img.shields.io/badge/M--Pesa-B2C-00A651.svg?style=flat-square)](https://developer.safaricom.co.ke)

</div>

---

## What is MatXchange?

MatXchange is an open-source enterprise platform that digitizes the informal waste sector. It connects waste pickers, collectors, recyclers, and producers on a single verified system — with automatic M-Pesa payments and every transaction permanently recorded on the Stellar blockchain.

---

## The Problem

Kenya's informal waste sector moves millions of kilograms daily but operates without trust or data. Pickers wait days to get paid. Collectors have no audit trail. Producers cannot prove EPR compliance. Regulators are blind.

MatXchange is the solution.

---

## Core Features

- **Instant payments** — M-Pesa B2C fires automatically when waste is submitted
- **Blockchain proof** — every transaction anchored to Stellar, tamper-proof forever
- **EPR compliance** — producers get verifiable on-chain certificates
- **Works on any phone** — USSD `*384*13404#` requires no smartphone or internet
- **Full value chain** — from picker to collector to recycler to marketplace buyer
- **Carbon tracking** — automated impact records with tree-equivalent calculations

---

## Tech Stack

| | Technology |
|---|---|
| Framework | Frappe v16 + ERPNext v16 |
| Database | MariaDB |
| Blockchain | Stellar SDK (Python) |
| Payments | M-Pesa Daraja B2C |
| USSD | Africa's Talking |
| Backend | Python 3.14 |

---

## Installation

```bash
bench init frappe-bench --frappe-branch version-16
cd frappe-bench
bench get-app erpnext --branch version-16
bench get-app https://github.com/samogera/matxchange.git
bench new-site mysite.local --install-app erpnext --install-app matxchange
bench start
```

### Configuration

Add to `sites/your-site/site_config.json`:

```json
{
  "mpesa_consumer_key": "YOUR_KEY",
  "mpesa_consumer_secret": "YOUR_SECRET",
  "mpesa_shortcode": "600998",
  "mpesa_environment": "sandbox",
  "stellar_secret_key": "YOUR_STELLAR_SECRET",
  "stellar_network": "testnet"
}
```

---

## Roadmap

- [x] 35 doctypes — full circular economy data model
- [x] M-Pesa B2C automatic payments
- [x] Stellar blockchain anchoring
- [x] USSD interface for feature phones
- [x] EPR certificate management
- [x] Recycled materials marketplace
- [ ] Role-based dashboards
- [ ] Workflows and approvals
- [ ] Production deployment
- [ ] Airtel Money integration
- [ ] Carbon credit minting on Stellar mainnet

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
Matxchange Ltd 2026
</div>