# Ports

## What is a Port?

- The **IP address** delivers data to the **device**.
- The **Port** delivers data to the **application** running on that device.

```text
IP    = Home address
Port  = Apartment / door number
```

Port numbers range from **0 to 65535**, divided into 3 ranges:

- **0–1023** → Well-Known (HTTP=80, HTTPS=443, DNS=53, SSH=22, FTP=21)
- **1024–49151** → Registered (MySQL=3306, RDP=3389, 8080 for alternatives)
- **49152–65535** → Dynamic / Ephemeral (used temporarily by clients for new connections)

---

## Sockets

A **Socket** is the endpoint of a connection — it is the combination of an IP and a Port:

```text
Socket = IP + Port
```

### Port vs Socket

| | Port | Socket |
|---|---|---|
| What is it? | A number (a door) | IP + Port (a full endpoint) |
| What does it deliver? | Data to a specific application | Represents an actual connection between two sides |
| By itself? | Just a number | The real working unit |

### How a connection happens

```text
Device A (192.168.1.5) → Device B (192.168.1.9)

B's Socket = 192.168.1.9 : 80       ← receives (server)
A's Socket = 192.168.1.5 : 52345    ← sends from (client ephemeral port)
                ↓
      Connection happens between Socket and Socket
```

- Every connection has **two sockets** — one on each side.
- The Port is just **part** of the Socket.

---

## Ports & Web Security

- Every open port = **attack surface**.
- Recon / port scanning is about finding running services and their versions.
- A **MySQL (3306)** port open on an external server is a red flag — it should be internal only.
- A service moved from a default port (e.g. SSH on 2222 instead of 22) is often just hiding — scanners usually find it anyway.

---

## Related Notes

- `Basics Knowledge.md` — OSI layers
- `07-CheatSheets/Ports-Services.md` — important port numbers & services
