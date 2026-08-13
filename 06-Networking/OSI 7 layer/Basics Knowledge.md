
# Protocol

It is like our human languages, it's the language of how computers talking together, any services have its protocols like 
- Web has http/https
- Mail has SMTP
- Sharing like FTP
- And more 
And OSI is a group of protocols work together at solid standers were put by IEEE

---

# OSI 7 Layers

![[Pasted image 20260809031058.png]]


Consists of 7 layers every single layer has its protocols and rules 

---
## Actions between layers

Is described into two types 
![[Pasted image 20260809031414.png]]

Between layers in the same device is **Adjacent layer interactions** means that there is a layer take action to the next or previous layer, and also there is **same layer interaction** it's when layer in one device do something and same layer but in opposite device do the opposite thing when it receive data.

---
## Applications layer 7

It's layer where all protocols that server user works 


---

## Presentation Layer 6

- **Compression / Decompression**
    
    - Compresses data to reduce its size before transmission.
        
    - Decompresses it at the receiving side.
        
- **Defines / translates data format**
    
    - Determines how data is represented and interpreted between systems.
        
    - This can include **encoding/decoding** and **serialization/deserialization**.
        
    - Metadata can be part of the data format, e.g. information describing the type, length, or structure of the data.
        
    - The actual representation is ultimately exchanged as **bytes**, regardless of whether the format is text-based or binary.
        
- **Encryption / Decryption**
    
    - Encrypts data before transmission and decrypts it at the receiving side.
        
    - **TLS** provides encryption for protocols such as HTTP, resulting in **HTTPS**.
        
    - Strictly speaking, TLS is usually associated with the **Session/Presentation boundary in the OSI model**, while in the real TCP/IP stack it is commonly treated as operating between the Application and Transport layers.


--- 

## Session Layer 5

- Defines Communication mode (s/h/f Duplex)
	- Single Duplex : like radio u hear the news coming from it but u can't send anything from it
	- Half Duplex : u can receive and also send data in the same media but one of receiving or sending data can work at time in connection media (at same time making collisions and data will be damged)
	- Full Duplex : sending and receiving can occurring at the same time in the same media 
- Manage Logical Sessions (Creates or Terminates)

### Auto-Negotiation & Duplex Mismatch

- **Case 1 — Both Auto**
  - SW1 and SW2 are using `Auto-Negotiation`.
  - They negotiate the best common setting → usually **Full-Duplex (F/D)**.
  - Connection works normally.

- **Case 2 — SW1 forced H/D, SW2 Auto**
  - SW1 is manually configured as **Half-Duplex** and does not negotiate.
  - SW2 cannot negotiate with SW1, so it assumes **Half-Duplex**.
  - → `H/D ↔ H/D` → works normally.

- **Case 3 — SW1 forced F/D, SW2 Auto**
  - SW1 is manually configured as **Full-Duplex** and does not negotiate.
  - SW2 cannot know that SW1 is using Full-Duplex → assumes **Half-Duplex**.
  - → `F/D ↔ H/D` = **Duplex Mismatch**
  - SW2 may experience **collisions** because it is using Half-Duplex, while SW1 can send and receive simultaneously.
  - Result → **Collisions + Errors + Poor Performance**

```text
Case 1:
SW1 Auto  ←→  Auto SW2
              ↓
             F/D

Case 2:
SW1 H/D    ←→  Auto SW2
              ↓
             H/D

Case 3:
SW1 F/D    ←→  Auto SW2
              ↓
             H/D
              ↓
       Duplex Mismatch
              ↓
      Collisions / Errors
      Poor Performance

```


---

## Transport layer 4

Choosing between Two deferent transmitting protocols 

- TCP (transmit control protocol)
	- Data make in chunked here 
	- With every group of chunks the over device send ACK message to make the other device that data received successfully and make him send other groups of chunks 
	
- UDP (user datagram protocol)
	- It sends every data segment without any checking of receiving done or not in the other side 


---


## Network layer 3

The internet layer in other way, it's in where routers work, deals with IP protocol (the internet protocol).

- Logical addressing 
	- Puting with data the source and destination IP address
- Choosing the best path for data (based on speed, length of the path, quality of the path)


--- 

## Data Link Layer 2

- Converting from different formats to binary and opposite 
- Has two sublayers
	- LLC (logical link layer)
		- Talk to the upper layer (network) and asking it some info like what's the protocol of sending request and make sure that the response protocol is the same or it will drop it
	- MAC (Media access control)
		- Where switch work 



---

## Physical Layer 1

- Converting data to a form can be transmitted by the media (like wires or wireless signals)


