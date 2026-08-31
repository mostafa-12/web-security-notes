

> **Level: from TCP connection establishment → data transfer → flow control → error detection → connection termination.**

---

# 1. Transport Layer

The **Transport Layer** is responsible for communication between **applications/processes** running on different devices.

The two main protocols are:

```text
TCP
UDP
```

### TCP

TCP is **connection-oriented** and provides reliable data delivery.

It provides:

- Ordered delivery
    
- Acknowledgments (ACK)
    
- Retransmission
    
- Flow control
    
- Error detection
    
- Connection establishment and termination
    

### UDP

UDP is simpler and has lower overhead.

It does **not** provide TCP-style reliability, ordering, or retransmission.

---

# 2. Ports

The IP address identifies the **device**.

The port identifies the **application/service** on that device.

```text
IP Address → Which device?
Port        → Which application/service?
```

Example:

```text
Client                         Server

10.0.0.5:50000  ───────────>  10.0.0.10:443
     ↑                              ↑
 Client application            HTTPS service
```

---

# 3. TCP Segment

TCP carries application data inside a **TCP Segment**:

```text
┌─────────────────────────────┐
│         TCP Header          │
├─────────────────────────────┤
│      Application Data       │
└─────────────────────────────┘
```

Important TCP header fields:

```text
Source Port
Destination Port
Sequence Number
Acknowledgement Number
Flags
Window
Checksum
Options
```

---

# 4. TCP Three-Way Handshake

Before sending normal application data, TCP establishes the connection:

```text
Client                         Server
  │                              │
  │──── SYN ───────────────────>│
  │                              │
  │<─── SYN + ACK ──────────────│
  │                              │
  │──── ACK ───────────────────>│
  │                              │
       Connection Established
```

### SYN

Means:

> "I want to start a TCP connection."

It can carry:

- Initial Sequence Number
    
- MSS
    
- Window information
    
- TCP Options
    

### SYN + ACK

The server says:

> "I received your request, and I accept the connection."

### ACK

The client confirms the server's response.

After that:

```text
ESTABLISHED
```

---

# 5. Sequence Number

TCP works with **bytes**, not simply "Segment 1, Segment 2, Segment 3."

The Sequence Number tells us:

> **Where does the data in this segment start?**

Example:

```text
Sequence Number = 1001
Data Size       = 100 bytes
```

The bytes are:

```text
1001 → 1100
```

So the next expected byte is:

```text
1101
```

---

# 6. Acknowledgement Number

The ACK number means:

> **"This is the next byte I expect."**

Example:

```text
Received:
1001 → 1100

ACK = 1101
```

Meaning:

> "I received everything up to byte 1100, and I am waiting for byte 1101."

Important:

```text
Last Byte = Sequence Number + Data Size - 1

ACK = Sequence Number + Data Size
```

---

# 7. MSS — Maximum Segment Size

MSS is:

> **The maximum amount of application data inside one TCP Segment.**

Example:

```text
MSS = 1460 bytes
```

The sender can send:

```text
[1460] [1460] [1460] [1460] ...
```

The last segment can be smaller.

### MSS is NOT:

```text
❌ File size
❌ Number of segments
❌ Window size
```

---

# 8. MTU and MSS

**MTU (Maximum Transmission Unit)** is the maximum size of the IP packet that can be transmitted on a link.

For a common Ethernet case:

```text
MTU = 1500 bytes
```

With a basic IPv4 + TCP header:

```text
1500
- 20 bytes IP Header
- 20 bytes TCP Header
--------------------
1460 bytes MSS
```

So:

```text
MTU
 ↓
determines the maximum packet size
 ↓
helps determine MSS
```

---

# 9. Buffer

The receiver has a **buffer** in memory where incoming TCP data can be stored before the application reads it.

Example:

```text
Receiver Buffer

┌─────────────────────────────────┐
│ Used Data │      Free Space     │
└─────────────────────────────────┘
```

---

# 10. Receive Window / Window Size

The **Receive Window (`rwnd`)** tells the sender:

> **"I currently have room for X more bytes."**

Example:

```text
Window = 4000 bytes
```

Meaning:

> "You can currently send up to 4000 more bytes, subject to TCP's other limits."

The Window field is inside the TCP Header.

```text
┌──────────────────────────┐
│ Sequence Number          │
│ ACK Number               │
│ Flags                    │
│ Window                   │ ← here
│ Checksum                 │
│ Options                  │
└──────────────────────────┘
```

---

# 11. Buffer ↔ Window

The relationship is:

```text
Buffer
   ↓
Available free space
   ↓
Receive Window
   ↓
Window field advertised to sender
```

Example:

```text
Buffer = 6000 bytes
Used   = 2000 bytes

Free   = 4000 bytes
```

So the receiver can advertise:

```text
Window = 4000
```

As the application consumes data, more buffer space becomes available and the window can increase.

---

# 12. MSS vs Window

These are different things:

```text
MSS
↓
Maximum data in ONE segment

Window
↓
Total number of bytes the receiver currently allows to be in flight
```

Example:

```text
MSS    = 1460
Window = 5840
```

Therefore:

```text
5840 / 1460 = 4
```

So this could represent roughly:

```text
[1460] [1460] [1460] [1460]
```

But the Window itself is measured in **bytes**, not segments.

---

# 13. Sliding Window

The receive window changes as data arrives and buffer space is consumed.

This is the idea behind the **Sliding Window**:

```text
Initial:

[ 1 ][ 2 ][ 3 ][ 4 ]
<------ Window ------>


Later:

        [ 5 ][ 6 ][ 7 ][ 8 ]
        <------ Window ------>
```

The window effectively moves forward through the byte stream.

---

# 14. ACK + Window

A TCP ACK can carry both:

```text
ACK = 1101
Window = 4000
```

Meaning:

```text
ACK = 1101
→ I received up to byte 1100.

Window = 4000
→ I currently have room for 4000 more bytes.
```

So:

```text
ACK
↓
Where did I receive up to?

Window
↓
How much more can I receive?
```

---

# 15. Example: Downloading a 10 MB Image

Suppose:

```text
File   = 10 MB
MSS    = 1460 bytes
Window = 5840 bytes
```

### Step 1 — Establish TCP

```text
Client                         Server

SYN ------------------------->
    <---------------- SYN-ACK
ACK ------------------------->
```

### Step 2 — Application Request

The client sends:

```text
GET /image.jpg
```

### Step 3 — Server Sends the File

The server splits the data according to the MSS:

```text
[1460]
[1460]
[1460]
[1460]
...
```

Each segment has a Sequence Number.

Example:

```text
Segment 1 → Seq = 5001
Segment 2 → Seq = 6461
Segment 3 → Seq = 7921
Segment 4 → Seq = 9381
```

Because:

```text
5001 + 1460 = 6461
6461 + 1460 = 7921
...
```

The client sends ACKs as it receives the data.

---

# 16. What if a Segment Is Lost?

Example:

```text
Segment 1 ✅
Segment 2 ❌
Segment 3 ✅
Segment 4 ✅
```

The Sequence Numbers reveal the gap.

The receiver may continue acknowledging the last contiguous data it has.

For example:

```text
ACK = 2000
```

means:

> "I have everything up to byte 1999, and I still need byte 2000."

TCP has mechanisms to detect the loss and retransmit the missing data.

---

# 17. The Six TCP Flags

The TCP header contains several control **flags**.

At your current level, focus on these six:

```text
URG
ACK
PSH
RST
SYN
FIN
```

## 1. SYN — Synchronize

Used to **start a TCP connection** and synchronize sequence numbers.

```text
Client → SYN → Server
```

Think:

> **"Let's start a connection."**

---

## 2. ACK — Acknowledgment

Used to acknowledge received data or TCP control information.

```text
ACK = 1101
```

Means:

> **"The next byte I expect is 1101."**

Think:

> **"I received it."**

---

## 3. FIN — Finish

Used when a side has finished sending data.

```text
FIN
```

Means:

> **"I am finished sending."**

Used during TCP connection termination.

---

## 4. RST — Reset

Used to **immediately terminate/reset a TCP connection**.

For example, if a connection is not valid or a service refuses the connection:

```text
RST
```

Think:

> **"Stop this connection immediately."**

It is different from `FIN`, which is used for a normal, graceful closing process.

---

## 5. PSH — Push

PSH tells the receiving TCP implementation, roughly:

> **"Pass the available data to the application promptly."**

It is **not**:

```text
❌ End of the window
❌ End of the connection
❌ Missing segment indicator
❌ Segment number
```

Sequence Numbers are what help identify gaps in the byte stream.

Also, **there is no general TCP rule that every 4th segment must have PSH set.**

---

## 6. URG — Urgent

Indicates that urgent data is present, using the **Urgent Pointer**.

At your current level, the important thing is simply:

```text
URG
↓
There is urgent data associated with this segment.
```

You do not need to go deeply into the historical/implementation details yet.

---

# 18. The Flags in the Handshake and Closing

### Opening

```text
SYN
↓
SYN + ACK
↓
ACK
```

### Closing

```text
FIN
↓
ACK
↓
FIN
↓
ACK
```

### Immediate reset

```text
RST
```

---

# 19. Checksum

The TCP/UDP Checksum is used for **Error Detection**.

Simplified idea:

```text
Header + Data
      ↓
Checksum calculation
      ↓
Checksum value
```

The sender places the checksum in the header.

The receiver performs the calculation again.

```text
Match ✅
→ No error detected

Different ❌
→ Data was corrupted
```

### Important

```text
Checksum = Detection
```

It does **not** repair the data.

TCP can use retransmission mechanisms to recover from lost/corrupted data.

UDP does not provide TCP-style retransmission.

---

# 20. TCP vs UDP Checksum

Both have a checksum mechanism:

```text
TCP  → Checksum ✅
UDP  → Checksum ✅
```

But:

```text
TCP
→ Error detection
→ ACK
→ Retransmission
→ Reliability

UDP
→ Error detection
→ No TCP-style reliability/retransmission
```

---

# 21. Four-Way TCP Termination

When both sides are finished:

```text
Client                         Server
  │                              │
  │──── FIN ───────────────────>│
  │<─── ACK ────────────────────│
  │<─── FIN ────────────────────│
  │──── ACK ───────────────────>│
```

Why four messages?

Because each direction can be closed independently.

The client may stop sending while the server still has data to send.

---

# 22. Final Relationship Map

```text
                         TRANSPORT LAYER
                                │
                    ┌───────────┴───────────┐
                    │                       │
                   TCP                     UDP
                    │
            Connection-oriented
                    │
             3-Way Handshake
                    │
          SYN → SYN-ACK → ACK
                    │
               Data Transfer
                    │
       ┌────────────┼─────────────┐
       │            │             │
      MSS         Window       Sequence / ACK
       │            │             │
Size of ONE     Receive         Position of
TCP segment      capacity       bytes in stream
                    │
                  Buffer
                    │
            Available space
                    │
                    ↓
              Sliding Window
                    │
                Checksum
                    │
             Error Detection
                    │
                   FIN
                    │
             4-Way Termination
```

# The Core Things to Remember

```text
SYN
→ Start the connection

ACK
→ Acknowledge / next byte expected

SEQ
→ Where this data starts in the byte stream

MSS
→ Maximum data size of ONE TCP segment

Buffer
→ Memory used to hold received data

Window
→ How many bytes the receiver can currently accept

PSH
→ Push available data to the application promptly

FIN
→ Graceful termination

RST
→ Immediate reset

URG
→ Urgent data indication

Checksum
→ Detect corrupted data
```

### One-line mental model

```text
MSS   = size of one piece
Buffer = storage for received pieces
Window = available receiving space
SEQ   = where this piece belongs
ACK   = what byte comes next
PSH   = deliver data to the application
Checksum = is the data corrupted?
SYN   = start
FIN   = finish
RST   = reset
URG   = urgent
```

![[Screenshot 2026-08-31 010358.png]]