![[Pasted image 20260907173717.png]]


![[Pasted image 20260908035928.png]]
![[Pasted image 20260908041134.png]]
# IP Address

- IPv4 = 32 bits divided into 4 octets (0-255 each), example `192.168.1.10`
- **First octet determines the class of IP Address**

---

## Class A

- 1st octet range: (1 => 126)
- Subnet Mask: `255.0.0.0`
- Form: `Network . Host . Host . Host`

```text
Network | Host | Host | Host
  255   |  0   |  0   |  0
```

- NO. of Networks < 255
- Many Hosts

---

## Class B

- 1st octet range: (128 => 191)
- Subnet Mask: `255.255.0.0`
- Form: `Network . Network . Host . Host`

```text
Network | Network | Host | Host
  255   |   255   |  0   |  0
```

---

## Class C

- 1st octet range: (192 => 223)
- Subnet Mask: `255.255.255.0`
- Form: `Network . Network . Network . Host`

```text
Network | Network | Network | Host
  255   |   255   |   255   |  0
```

- Many Networks
- Low No Of Hosts

---

## Class D (Multicast)

- 1st octet range: (224 => 239)
- Note: image says (124 => 239) by mistake, correct is **224**
- Not a device address — it is a **group name**
- Never used as Source, always as **Destination only**
- Sender sends once, only joined devices receive
- Mostly **UDP** (no ACK storm like TCP)
- Example: `224.0.0.5` = all OSPF routers

```text
Going: my real IP (Source) -> group IP (Destination)
Coming: distributed only to joined ports / networks, others get nothing
```

---

## Class E

- 1st octet range: (240 => 255)
- Experimental / Research

---

## Loopback (127.x.x.x)

- Full range `127.0.0.0/8` is reserved, most famous is `127.0.0.1` (localhost)
- Any packet to `127.x.x.x` **never leaves my device**
- Goes down to Network layer then loops back up via `lo` interface
- No Ethernet Frame on wire, no ARP, no Switch/Router sees it

```text
App -> Transport (normal) -> Network (see 127.x -> send to lo)
  -> back up to Transport -> App (same device)
```

- Why full /8 and not one IP? Old Classful reservation + easy check `first_octet == 127`, now waste but hard-coded everywhere (IPv6 fixed it with single `::1`)
- `ping 127.0.0.1` tests my own TCP/IP stack, not cable or router
- Binding on `127.0.0.1` = local only, vs `0.0.0.0` = open to network

---

## Subnet Mask Decides: Same Network or Not?

- Device only knows its network by `IP AND Mask`
- Where mask = 255 keep number, where mask = 0 ignore it
- Example:
  - A = `10.1.1.1`, B = `10.1.2.2`
  - With `/16` (255.255.0.0): A net = `10.1.0.0`, B net = `10.1.0.0` = same network
  - With `/24` (255.255.255.0): A net = `10.1.1.0`, B net = `10.1.2.0` = different networks

### If same network -> talk directly (ARP)

- Sender asks with ARP on local LAN: who has this IP? send me your MAC
- Switch only sees MACs (Broadcast FF:FF:FF:FF:FF:FF then unicast MAC)
- Switch never reads IP, it forwards Frames by MAC table
- No router needed

```text
A decides: B is local -> ARP for B MAC -> Frame to B MAC -> Switch forwards
```

### If different network -> send to Gateway

- Sender says: not my network, I send to Gateway (Router) and it handles it
- Needs Gateway configured + Router connected to both networks + return path works
- Same switch with no router = packet dies inside sender, B never sees anything

```text
A decides: B is remote -> where is Gateway? -> no Gateway = drop (unreachable)
A decides: B is remote -> Gateway MAC -> Router -> B (needs router in middle)
```

- Rule: **IP decision happens inside sender (L3), Switch only executes on MAC (L2)**

---

## Private vs Public IP (RFC 1918 + NAT)

- IPv4 = 32 bits = ~4.3B addresses only (`2^32`), not enough for every device
- Solution: split addresses + reuse private ones behind NAT

### Public IP

- Globally unique, routable on Internet
- Assigned by ISP (ISP gets from RIR like RIPE, ARIN)
- Example: `8.8.8.8`

### Private IP (not routable, reusable in every LAN)

- `10.0.0.0/8` (10.0.0.0 -> 10.255.255.255)
- `172.16.0.0/12` (172.16.0.0 -> 172.31.255.255)
- `192.168.0.0/16` (192.168.0.0 -> 192.168.255.255)

### NAT — How 100 devices share 1 Public IP

- Router replaces Source Private IP with its Public IP + different Source Port (PAT)
- Keeps mapping in NAT Table to return reply to correct device

```text
192.168.1.5:1234 -> Router -> PublicIP:50001 -> Internet
Internet -> PublicIP:50001 -> Router looks up table -> 192.168.1.5:1234
```

- Saved billions of addresses, but broke End-to-End (need Port Forwarding)
- Real fix is IPv6 (`2^128`), NAT was temporary

---

## Quick Summary

```text
A = (N.H.H.H), 1-126
B = (N.N.H.H), 128-191
C = (N.N.N.H), 192-223
D = group not device, 224-239
E = experimental, 240-255
127/8 = me talking to me, stops at L3
```

---

## Related Notes

- `Basics Knowledge.md` — Network layer
- `Transport Layer-TCP-IP.md` — TCP vs UDP
- `Ports.md` — IP delivers to device
