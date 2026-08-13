

# HTTP (hypertext Transfer Protocol)

- Main request for browsing
- Data sent as a clear text (MitM attack Can performed ) 
- Work on Port 80 and port 443 if it's HTTPS secure (data encrypted with SSL/TSL protocol done)
- Work in Request- Response 
- Response type associated with status code to explain response result (`CheatSheets/status-codes`)


# FTP (file transfer protocol)

- Downloading and uploading
- Works in 20/21 port
	- Port 20 to downloading and uploading **data** 
	- Port 21 to **control** choose uploading or downloading data



# SMTP (simple mail transfer protocol)

- Sending mails out of my device to mail server
- Work on **port 25**



# Telnet 

- Work on **port 23**
- Clear text 
	- SSH is better to use because it's **encrypted** 
		- Working in **Port 22**



# RDP (remote Desktop Protocol)

- Work on **port 3389**
- Supported with GUI 
- Developed by Microsoft



# DHCP 

- Assigning IP addresses (also Subnet mask, Gateway, DNS) automatically to devices.
- Work on a Client-Server model.
- Based on **UDP** — Client uses **port 68**, Server uses **port 67**.
- The IP given by DHCP is a **lease** — it is not permanent, the client must renew it after a period.

---

## How a device gets an IP (4 ways)

A device can get an IP address in one of 4 ways:

### 1. Manual (Static)

- You type the IP, Subnet mask, Gateway, and DNS **by hand**.
- **Good for** servers and important network devices (they must not change).
- **Downsides**:
	- Risk of mistakes → IP conflicts.
	- Hard to manage when too many devices.
	- If the network changes (e.g. moved to another WiFi), the old IP will not work.

### 2. DHCP (Automatic)

- The device asks the DHCP server for an IP, the server gives it a lease.
- **Good for** regular users / many devices.
- **Downsides**:
	- Needs a working DHCP server.
	- The IP can change after the lease ends.
		- 50% for renew and 87% for asking other DHCP servers

### 3. Alternate Configuration

- The device **tries DHCP first**.
- If **no DHCP server is found**, it falls back to a **static backup** IP you had configured in the Alternate tab.
- **Why useful?**
	- Laptop at work (DHCP exists) → gets a normal IP.
	- Same laptop at home (no DHCP) → uses the Alternate static IP and keeps working.
- Note: Manual and DHCP can NOT be set at the same time — the Alternate is the backup only when DHCP fails.

### 4. APIPA (Automatic Private IP Addressing)

- When the device finds **no DHCP server AND no Alternate configuration** → it assigns itself an IP from **169.254.x.x**.
- Address range: `169.254.0.0` – `169.254.255.255` (link-local only, can not reach the internet).
- The device keeps looking for a DHCP server in the background — if one appears, it takes the DHCP IP and drops the APIPA one.
- **APIPA means something is wrong** (no DHCP, bad cable, broken server) — it is not a real network config, just a fallback so the device can still talk to link-local neighbors.

---

## DORA (How DHCP works)

The process of getting an IP is called **DORA**:

```text
Client                    Server
  │                            │
  │──── 1. DISCOVER ──────────▶│  Who offers me an IP?  (broadcast)
  │◀──── 2. OFFER ─────────────│  I have an IP for you  (broadcast OR unicast)
  │──── 3. REQUEST ───────────▶│  I choose YOU           (broadcast)
  │◀──── 4. ACK ───────────────│  Done, it is yours      (broadcast OR unicast)
  │                            │
  ▼ The client now uses the IP with a lease timer
```

### Why each step is broadcast or unicast

The client **has no IP yet** and **does not know the server** → it must shout (broadcast).

| Step        | Broadcast?                             | Unicast?              | Why                                                                                                   |
| ----------- | -------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------- |
| 1. DISCOVER | Always broadcast                       | ❌ Impossible          | Client does not know who the server is                                                                |
| 2. OFFER    | ✅ if client set the **broadcast flag** | ✅ if flag not set     | Server has its MAC + the offered IP, so it can send unicast directly                                  |
| 3. REQUEST  | Always broadcast                       | ❌ for the start       | There may be multiple DHCP servers — broadcast tells the others "I rejected your offer, give it back" |
| 4. ACK      | ✅ same logic as OFFER                  | ✅ same logic as OFFER | Follows the client's broadcast flag                                                                   |

### Why REQUEST must be broadcast

If multiple DHCP servers saw the DISCOVER, all of them reserved an IP.
The client sends REQUEST **broadcast** so that:

- The **chosen** server → completes the assignment.
- The **other** servers → know they lost and return the reserved IP to the pool.

> If REQUEST was unicast, the losing servers would keep their IPs reserved and never learn they were rejected → wasted addresses.

### When broadcast is NOT needed

Once the client **already knows the server** and **has an IP**, DORA no longer uses broadcast:

- **Lease renewal (renew)** → unicast straight to the known server.
- **DHCP Relay** (client on a different subnet) → the connection between the server and the relay agent is **unicast**; the relay handles the broadcast part with the client. 



# DNS

