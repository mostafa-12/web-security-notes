# IP vs MAC — Why Two Addresses?

- Small LAN (4 PCs + Switch) works with MAC only
- Problem starts when leaving the room (scale + routing + apps)

---

## MAC — Local Hardware Address

- Burned on NIC from factory, random and flat, example `A4:5E:60:C3:11:9F`
- No geography, no hierarchy, cannot be summarized
- Switch only understands MAC (L2): which Port has this MAC?
- Switch never reads IP, it forwards Frames by MAC table
- Like chassis number of a car — fixed, unique, but says nothing about location

---

## IP — Logical Location Address

- Logical and hierarchical, example `192.168.1.10` = network 1, host 10
- Main street -> side streets -> alleys:

```text
142.0.0.0/8   = city
142.1.0.0/16  = main street
142.1.5.0/24  = alley
142.1.5.32/27 = building
```

- Router only knows prefix direction, not every host (summarization)
- Like home address — changes when device moves, MAC stays same
- Socket = `IP + Port` — apps need IP, MAC has no Ports

---

## Why Separation? (L2 vs L3)

- L2 solves: how to reach a device next to me on same wire?
- L3 solves: how to reach any device in the world on any media?
- Different media (Ethernet / WiFi / Serial) have different L2, IP stays unified above them
- Change NIC -> MAC changes, IP stays logical

---

## ARP — The Bridge

- New device knows IP but not MAC
- ARP asks on local LAN: who has this IP? send me your MAC
- IP = name humans and apps call, ARP = translator to local MAC

```text
Same network -> ARP for dest MAC -> direct via Switch (no router)
Different network -> send to Gateway MAC -> Router handles it
No Gateway + different network = packet dies inside sender
```

- Rule: **IP decision inside sender (L3), Switch executes on MAC (L2)**

---

## DNS Is Different Problem

- DNS solves my problem: remember name instead of number (`google.com` -> `142.250.1.1`)
- Needed with IP or MAC both (humans cannot remember hex)
- DNS says *what is the address*, routing says *from where to reach it*
- DNS does not fix table explosion, summarization does

```text
My PC knows: 142.250.1.1 exact (from DNS)
Mid router knows: 142.250.0.0/16 via this side (65k in one line)
Big router knows: 142.0.0.0/8 via Europe (16M in one line)
```

- Flat random MAC cannot be summarized -> every router must store every host = impossible

---

## Reverse Question — Why IP Cannot Replace MAC?

- New PC has no IP yet — how does it ask for one with IP only? Dead end
- DHCP Discover uses `0.0.0.0 -> 255.255.255.255` but still carried inside Ethernet Frame:
  - Source MAC = my burned MAC (exists before any IP)
  - Dest MAC = `FF:FF:FF:FF:FF:FF` (Broadcast on wire)
- Switch delivers by MAC, server replies to my MAC, then I get IP
- MAC carries me before I have IP

### Day Zero — Network Just Powered On

- No DHCP, no IPs, no config — full chaos on L3
- No chaos on L2: every NIC already has unique factory MAC
- Switch learns `MAC -> Port` from first frames, LAN works with zero config
- L3 (DHCP/IP) is built later on top of working L2

```text
L2 = works immediately with no setup (local plug and play)
L3 = needs planning and assignment, gives the whole world (global routable)
```

- More reasons:
  - Stability: IP changes when device moves (DHCP), MAC stays as hardware identity
  - Media: Ethernet / WiFi / Serial have different L2 needs (access, errors, signals), IP stays unified above them
  - Speed: Switch forwards by small MAC table in hardware, Router does heavier longest-prefix match
- Packet never goes naked on wire — it needs Frame `[src | dst | data | FCS]` so NIC knows if it is mine and Switch knows where to send it
- Broadcast-only without learning = back to Hub/Bus days (collisions, everyone sees everything)

---

## IP Conflict + ARP Spoofing (Security)

- Two devices with same IP: both reply to ARP Request
- Sender ARP cache holds one `IP -> MAC` only, keeps last reply (flapping)
- Traffic goes once to A once to B, both cut intermittently
- Switch is fine: table is `MAC -> Port` (AA->P1, BB->P2), no confusion — confusion is in sender ARP cache (L3), not Switch (L2)
- New device sends Gratuitous ARP first: anyone using this IP? if reply -> `IP conflict` warning
- Attacker abuses same idea: keeps replying I am Gateway (poisoning)
  - One reply is not enough: cache expires + real Gateway also replies and wins back
  - Needs continuous replies (every few seconds) to stay last reply
  - Needs forwarding to real Gateway (MITM relay) or victim notices cut

---

## Switch Aging + MAC Flooding (Security)

- Switch table `MAC -> Port` is not permanent, entry ages out (e.g. 300s) if not heard again
- Unknown dest MAC -> Flood to all ports until owner replies and table learns it (normal, not bug)
- Table has limit (e.g. 8k entries)
- MAC Flooding: attacker sends thousands of fake source MACs -> table full -> Fail-open -> behaves like Hub -> all traffic flooded (Sniffing)
- Defense name only for now: **Port Security** (limit MACs per port)

---

## Quick Summary

```text
Small LAN: MAC is enough
Outside LAN: need hierarchical IP
MAC = who (fixed, flat, local, works before setup)
IP = where (changes, hierarchical, global, needs setup)
MAC carries me before I have IP, IP takes me outside after I have it
ARP connects them locally
DNS helps humans, summarization helps routers
```

---

## Related Notes

- `IPv4.md` — classes + AND + same or different network
- `Basics Knowledge.md` — Network vs Data Link layer, Packet vs Frame
- `Ports.md` — Socket = IP + Port
- `Application Layer-TCP-IP.md` — DNS
