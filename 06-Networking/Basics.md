# Network Types 

## Physical types 

- LAN (local area network)
- WAN (wide area network)

---

## Logical types

- Peer to Peer (workgroup)
- Server- based (Domain)

--- 



# Topologies

## Bus

![[Pasted image 20260808182950.png]]

- Devices here are connected together in the same line with T-connector 
- In the end and start of wire there are two terminators To terminate Signal and make it doesn't waver in wire 
- Any Signal is transmitted through the wire to all devices (any one in the wire can see signal)
- If two devices send data at the same time there will be data collisions

---

## Ring 

![[Pasted image 20260808183701.png]]

- Devices connected together in circular form, every device connected to the previous and next device
- Same issue of bus

---


## Full-Mesh 


![[Pasted image 20260808183857.png]]

- Every device connected to all another devices
-  Not good for users devices but useful to connect routers of networks together

---

## Partial-Mesh

![[Pasted image 20260808184138.png]]

- Like full but any unwanted Links or connections between two devices are removed

---

## Star 

![[Pasted image 20260808184335.png]]


- Centralized Device (SW, Router, Modem) work like traffic officer handle how devices talks to each others
- If any devices (not centered Device ) downed network will still work 
- No collisions between devices
- Any to devices can talk together without any data go to others devices


---


# Types of cables

## Copper connectors

### Coaxial Cable
![[Pasted image 20260808185053.png]]

Used with T-Connectors, in bus topology, 

---

### Twisted- pair

Have to Types :
- STP (wire with shield)
- UTP (with no shield)
	- CAT5 (100 mb/s)
	- CAT5e (1 Gb/s)
	- CAT6 (10 Gb/s)

![[Pasted image 20260808185532.png]]
![[Pasted image 20260808185651.png]]

![[Pasted image 20260808185823.png]]

---

## Fiber 
- Fiber optics


# Access Methods 

## CSMA/CD

**CSMA/CD = Carrier Sense Multiple Access with Collision Detection**

A MAC mechanism historically used in **shared, Half-Duplex Ethernet** to handle multiple devices accessing the same medium.

### How It Works

1. **Carrier Sense** → Listen to the medium before transmitting.
    
    - Idle → Transmit.
        
    - Busy → Wait.
        
2. **Multiple Access** → Multiple devices share the same communication medium.
    
3. **Collision Detection** → While transmitting, the device monitors the medium for collisions.
    

### If a Collision Occurs

```text
Detect Collision
      ↓
Stop Transmission
      ↓
Send Jam Signal (waring other devices there is a collision)
      ↓
Random Backoff
      ↓
Retry
```


### Example

```text
PC1 → Listen → Idle → Transmit ──X──
PC2 → Listen → Idle → Transmit ──X──
                         ↓
                     Collision
                         ↓
                  Stop + Backoff
                         ↓
                       Retry with Random time to every device
```

### Important

CSMA/CD is mainly associated with **older/shared Ethernet**.

Modern **Switched Full-Duplex Ethernet** does not normally have collisions, so **CSMA/CD is not needed**.

### Quick Summary

```text
Listen → Transmit → Detect Collision
       → Stop → Backoff → Retry
```

> **CSMA/CD allows Ethernet devices sharing the same medium to detect and recover from collisions.**