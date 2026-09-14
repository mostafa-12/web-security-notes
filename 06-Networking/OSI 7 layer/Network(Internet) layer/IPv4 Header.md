# IPv4 Header (20-60 bytes)

- Min 20 bytes, max 60 bytes if Options present
- Row = 32 bits. IHL counts header length in 32-bit words (5 = 20 bytes)

![[Pasted image 20260914004720.png]]

```text
Version | IHL | DSCP | ECN | Total Length
Identification | Flags | Fragment Offset
TTL | Protocol | Header Checksum
Source IP
Destination IP
Options (if IHL > 5)
```

---

## Fields

- Version (4b): always 4
- IHL (4b): header length, min 5
- DSCP+ECN (8b): QoS / priority, not security critical
- Total Length (16b): header + data, max 65535 (abused in Ping of Death)
- Identification (16b): same ID for all fragments of same packet
- Flags (3b): Reserved, DF (Don't Fragment), MF (More Fragments)
- Fragment Offset (13b): position in original packet, value * 8 = byte offset
- TTL (8b): -1 per router, 0 = drop. Prevents loops. Used by traceroute. OS fingerprint (Linux 64, Windows 128)
- Protocol (8b): upper layer (1=ICMP, 6=TCP, 17=UDP). Firewall uses it
- Header Checksum (16b): detects corruption only, not attack. Recalculated each hop (TTL changes)
- Source/Destination IP (32+32b): no authentication -> easy Spoofing (SYN Flood, Smurf)
- Options: rarely used (Record Route, Timestamp), mostly dropped by firewalls

---

## Segmentation (TCP) vs Fragmentation (IP) — Why Both?

- TCP Segmentation: splits stream by MSS (e.g. 1460 for MTU 1500). UDP does not split at all
- IP Fragmentation: forced split if packet > link MTU (Ethernet 1500, PPPoE 1492, VPN ~1400)
- IP cannot trust Transport because it serves TCP/UDP/ICMP all. Must handle any size itself
- IPv4 allows routers to fragment (DF=0). IPv6 removed it
- Modern way: set DF=1 + Path MTU Discovery (router drops + sends ICMP Fragmentation Needed, sender shrinks)

---

## Reassembly — How Order Is Restored

- Each fragment carries: Identification (which packet?), Offset*8 (where?), MF (more coming or last?)
- Receiver buffers per (Src, Dst, Protocol, ID), places each fragment by Offset, ignores arrival order
- Knows it is done when: MF=0 arrives (knows total size) + bytes 0->last fully covered with no gap
- Then strips IP header, passes clean Segment to TCP. TCP never sees fragments, uses its own Seq Numbers
- Reassembly happens only at final destination, routers fragment only, never reassemble
- Timeout (30-60s): if fragment missing, drop all
- Security: overlapping fragments (same Offset, different data) -> Windows takes first, Linux takes last -> IDS evasion

```text
Send: App Data -> TCP Segment [Seq] -> IP Packet [ID] -> Fragments [ID+Offset]
Receive: Fragments -> IP Packet -> TCP Segment -> App Data
```

---

## Related Notes

- `IPv4.md` — classes + Private vs Public + NAT
- `Basics Knowledge.md` — Network layer, Packet
- `Transport Layer-TCP-IP.md` — TCP Segmentation, MSS
