# 06-Networking

## Purpose

Networking fundamentals for web security — how data moves from browser to server, and where each layer can be abused (spoofing, sniffing, misconfig, fingerprinting).

---

## Contents

| File | Topic |
|------|-------|
| `Basics.md` | Network types (LAN/WAN), topologies, cables, CSMA/CD |
| `Connection Models.md` | Work Group (P2P) local accounts vs Client/Server (Domain/DC) central auth |
| `OSI 7 layer/Basics Knowledge.md` | 7 layers, adjacent vs same-layer interaction, duplex mismatch, CSMA/CD |
| `OSI 7 layer/Ports.md` | Port ranges, Socket = IP + Port, attack surface notes |
| `OSI 7 layer/Transport Layer-TCP-IP.md` | TCP vs UDP, handshake, Seq/ACK, MSS/MTU, rwnd/cwnd, flags, termination |
| `OSI 7 layer/Application Layer-TCP-IP.md` | HTTP/FTP/SMTP/Telnet/SSH/RDP, DHCP (4 ways + DORA), DNS hierarchy |
| `OSI 7 layer/Network(Internet) layer/IPv4.md` | Classes A–E, Loopback, Private vs Public + NAT/PAT, same vs remote network |
| `OSI 7 layer/Network(Internet) layer/IPv4 Header.md` | Header fields, fragmentation/reassembly, IDS evasion |
| `OSI 7 layer/Network(Internet) layer/Subnetting.md` | CIDR, Block Size, VLSM, solved examples |
| `OSI 7 layer/Network(Internet) layer/IP vs MAC.md` | Why two addresses, ARP bridge, IP conflict, ARP spoofing, MAC flooding |

---

## Related Notes

- `07-CheatSheets/Ports-Services.md` — port/service quick reference
- `02-Web Architecture/Anatomy of a Web Request.md` — where networking meets the app stack
- `04-Recon/` — port scanning and service fingerprinting use these fundamentals

---

## Study Order

```
1. Basics.md
2. Connection Models.md
3. OSI 7 layer/Basics Knowledge.md
4. OSI 7 layer/Ports.md
5. OSI 7 layer/Transport Layer-TCP-IP.md
6. OSI 7 layer/Network(Internet) layer/IP vs MAC.md
7. OSI 7 layer/Network(Internet) layer/IPv4.md
8. OSI 7 layer/Network(Internet) layer/IPv4 Header.md
9. OSI 7 layer/Network(Internet) layer/Subnetting.md
10. OSI 7 layer/Application Layer-TCP-IP.md
```
