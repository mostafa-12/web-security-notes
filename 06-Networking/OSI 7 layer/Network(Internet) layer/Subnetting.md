# Subnetting & Subnet Mask — Network (Internet) Layer (L3)

> Location: L3 decides same-network vs remote-network. Subnetting lives here.

## 1. Why Subnetting?

One flat large network means:
- Huge broadcast domain, performance drops
- No isolation: HR can see Servers
- IP waste: department needs 10 hosts, you give it 254

Solution: split one large network into smaller subnets, each with:
- Own Network Address
- Own Broadcast Address
- Own policy (Firewall / ACL)
- Connected together via Router

---

## 2. What Subnet Mask Does

It defines which part of the IP is Network and which part is Host.

- `1` = Network (fixed)
- `0` = Host (variable)

Example `/24`:
```
255.255.255.0 = 11111111.11111111.11111111.00000000
```

CIDR = number of `1` bits:
```
/25 = 255.255.255.128
/26 = 255.255.255.192
/27 = 255.255.255.224
/28 = 255.255.255.240
/29 = 255.255.255.248
/30 = 255.255.255.252 -> 2 hosts only, for router-to-router link
```

Fixed rule in any subnet:
- First address = Network ID (reserved, name of network)
- Last address = Broadcast (reserved, talk to all)
- Between them = Usable for devices

So: `Usable = 2^h - 2`

---

## 3. Solving Method (no binary AND)

### a) For a required number of subnets:
```
2^n = number of subnets
```
`n` = borrowed bits from Host part, added to old mask.

Example: need 4 subnets from `/24`:
`2^2 = 4` so `n=2`, new mask `/24+2 = /26`

### b) For hosts per subnet:
```
Total IPs = 2^h
Usable = 2^h - 2
```
`h` = remaining host bits. Subtract 2 for (NID + Broadcast).

### c) Block Size to walk subnets:
```
Block Size = 256 - last octet of mask
```
Walk: `0, Block, Block*2, ...`

Example mask `255.255.255.192`:
Block = `256-192 = 64`, subnets: `0, 64, 128, 192`

---

## 4. Solved Examples

### Ex1: Basics
`192.168.10.45 /24`
- `h=8` so `2^8 - 2 = 254`
- NID: `192.168.10.0`
- Broadcast: `192.168.10.255`
- First usable: `192.168.10.1`
- Last usable: `192.168.10.254`

### Ex2: Block Size
`172.16.5.130 /26`
- Mask: `255.255.255.192`
- `2^2 = 4` subnets
- Block = `256-192 = 64`
- Subnets: `.0 , .64 , .128 , .192`
- Broadcasts: `.63 , .127 , .191 , .255`
- `.130` belongs to:
  - NID: `172.16.5.128`
  - Usable: `.129` to `.190`
  - Broadcast: `172.16.5.191`

### Ex3: Same network or not?
A: `192.168.1.10 /25`
B: `192.168.1.200 /25`

- `/25` Block = `256-128 = 128`
- Two subnets: `0-127` and `128-255`
- A in `192.168.1.0` Broadcast `.127`
- B in `192.168.1.128` Broadcast `.255`
- Result: different networks, need Router.

### Ex4: Fixed Subnetting
`10.0.0.0 /24` need 8 equal subnets:
- `2^n = 8` so `n=3`
- New mask: `/24+3 = /27` = `255.255.255.224`
- Block = `256-224 = 32`
- sub0: NID `.0` - Usable `.1` to `.30` - Broadcast `.31`
- sub1: NID `.32` - Usable `.33` to `.62` - Broadcast `.63`
- Continue `.64 , .96 , .128 , .160 , .192 , .224`

### Ex5: Exam style
`192.168.1.77 /29`
- Mask: `255.255.255.248`
- Block = `256-248 = 8`
- Subnets count: `256/8 = 32`
- Hosts: `2^3 - 2 = 6`
- Walk: `0, 8, 16, ... 64, 72, 80 ...`
- `.77` belongs to:
  - NID: `192.168.1.72` (must be divisible by 8)
  - Usable: `.73` to `.78`
  - Broadcast: `192.168.1.79`
- Note: `.71` is broadcast of previous net (`.64`), not a NID.

---

## 5. VLSM (Variable Length Subnet Mask)

Fixed wastes IPs. VLSM allocates by actual need.

Rule: **Largest first.**

Steps:
1. Sort descending
2. For each, find smallest `h` with `2^h - 2 >= required`
3. Allocate sequentially from first free IP

Quick map:
```
60 host -> h=6 -> /26 -> Block 64
30 host -> h=5 -> /27 -> Block 32
14 host -> h=4 -> /28 -> Block 16
6 host  -> h=3 -> /29 -> Block 8
2 host  -> h=2 -> /30 -> Block 4 (router link)
```

### VLSM Worked Example
`10.0.0.0/24` needs: LAN1=100, LAN2=50, LAN3=20, Link=2

- LAN1 (100): `2^7-2=126` so `h=7` so `/25` Block 128
  - NID `10.0.0.0` - Usable `.1` to `.126` - Broadcast `.127`
- LAN2 (50): `2^6-2=62` so `/26` Block 64, start at `.128`
  - NID `10.0.0.128` - Usable `.129` to `.190` - Broadcast `.191`
- LAN3 (20): `2^5-2=30` so `/27` Block 32, start at `.192`
  - NID `10.0.0.192` - Usable `.193` to `.222` - Broadcast `.223`
- Link (2): `2^2-2=2` so `/30` Block 4, start at `.224`
  - NID `10.0.0.224` - Usable `.225` - `.226` - Broadcast `.227`
  - `.225` for R1 port, `.226` for R2 port

Link = point-to-point wire between two routers, needs exactly 2 IPs, always `/30`.

---

## 6. Real-World Note

No one does binary AND daily:
- Plan once, document, reuse for years
- Memorize: `/25=126 , /26=62 , /27=30 , /28=14 , /30=2`
- Use Subnet Calculator + DHCP + IPAM (NetBox)
- Value of understanding = fast troubleshooting: see IP + Mask, instantly know wrong-network issue.

---

## Related Notes

- `IPv4.md` — classes, NID/Broadcast concept
- `IP vs MAC.md` — L3 vs L2 decision
