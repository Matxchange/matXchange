<div align="center">

# MatXchange ♻️
### The Circular Economy OS for Africa

*Digitizing informal waste collection — paying pickers instantly — anchoring every kilogram to the blockchain*


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

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
Matxchange Ltd 2026
</div>