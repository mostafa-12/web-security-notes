# OWASP-Juice-Shop

## Purpose

Hands-on practice for the theory in this repo — solving OWASP Juice Shop challenges and mapping each one back to the vulnerability notes and testing methodology.

> Each file is a raw working note (payloads, requests, JWT dumps). Promote stable solutions into stage-by-stage write-ups as they mature.

---

## Contents

| File | Challenge / Topic |
|------|-------------------|
| `00-View Basket.md` | View another user's basket — `GET /rest/basket/{id}` IDOR (swap ID / Intruder 0→N) |
| `01-Access Admin Section.md` | Admin-section access — session/JWT capture (`role`, `deluxeToken`, `bid`) |
| `03-BAC-Roadmap.md` | BAC-only track roadmap (easiest → hardest): View Basket → Admin Section → Five-Star → Web3 Sandbox → Forged Feedback/Review → Manipulate Basket → Product Tampering → CSRF → Easter Egg |

---

## Related Notes

- `03-Web-Vulnerabilities/Access control vulnerabilities/` — access control types + testing methodology
- `03-Web-Vulnerabilities/Multi-Step Processes.md` — multi-request workflow testing
- `09-Writeups & Reports/` — real-world case studies using the same techniques
- `07-CheatSheets/Access-Control.md` — quick reference during labs

---

## Study Order

```
1. 00-View Basket.md
2. 01-Access Admin Section.md
3. 03-BAC-Roadmap.md (solving order for the rest of the BAC track)
```
