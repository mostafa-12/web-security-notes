
# Transport Layer — TCP & UDP

> **Level: from TCP connection establishment → data transfer → flow control → congestion control → error detection → connection termination.**

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
    
- Congestion control
    
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

# 10. Receive Window — `rwnd`

The **Receive Window (`rwnd`)** tells the sender:

> **"I currently have room for X more bytes."**

Example:

```text
Window = 4000 bytes
```

Meaning:

> "I currently have room for about 4000 more bytes."

The Window field is inside the TCP Header:

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

# 11. Buffer ↔ `rwnd`

The relationship is:

```text
Buffer
   ↓
Available free space
   ↓
Receive Window (rwnd)
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
rwnd = 4000
```

As the application consumes data, more buffer space becomes available and `rwnd` can increase.

---

# 12. `rwnd` vs `cwnd`

TCP has **two different limits** that affect how much data can be sent at the same time.

```text
rwnd = Receive Window
cwnd = Congestion Window
```

They work **together**, but they solve different problems.

---

## `rwnd` — Receiver Capacity

`rwnd` answers:

> **"How much can the receiver currently accept?"**

It is related to the receiver's buffer.

```text
Buffer
   ↓
Available Space
   ↓
rwnd
```

Example:

```text
rwnd = 5000 bytes
```

The receiver is currently able to accept about 5000 more bytes.

---

## `cwnd` — Network Capacity

`cwnd` answers roughly:

> **"How much data can I currently put into the network without causing excessive congestion?"**

It is controlled by the sender's **Congestion Control** algorithm.

Initially, TCP starts cautiously and then increases `cwnd` as transmission succeeds.

Simplified:

```text
Small amount
     ↓ ACK ✅
More
     ↓ ACK ✅
More
     ↓ ACK ✅
...
```

This is associated with **Slow Start** and later **Congestion Avoidance**.

If TCP detects congestion, such as packet loss, it reduces its sending rate/window according to the congestion-control algorithm.

---

# 13. How `rwnd` and `cwnd` Work Together

The sender must respect **both** limits.

Simplified:

```text
Effective Send Window ≈ min(rwnd, cwnd)
```

Example:

```text
MSS  = 1000 bytes
rwnd = 5000 bytes
cwnd = 3000 bytes
```

Therefore:

```text
min(5000, 3000) = 3000 bytes
```

So roughly:

```text
[1000] [1000] [1000]
```

can be in flight.

---

### Another Example

```text
MSS  = 1000 bytes
rwnd = 2000 bytes
cwnd = 5000 bytes
```

The network can handle 5000 bytes, but the receiver only has room for 2000.

Therefore:

```text
min(2000, 5000) = 2000 bytes
```

So roughly:

```text
[1000] [1000]
```

can be sent.

---

# 14. MSS vs `rwnd` vs `cwnd`

These three are different:

```text
MSS
↓
Maximum data size of ONE segment

rwnd
↓
How much the receiver can currently accept

cwnd
↓
How much data the sender currently allows into the network
```

So:

```text
MSS
   ↓
Size of each piece

rwnd + cwnd
   ↓
How many bytes can currently be in flight
```

The sender also has to obey the MSS when constructing each segment.

---

# 15. Sliding Window

The **Sliding Window** is the idea that the range of data allowed to be sent/received moves forward as ACKs arrive and buffer space becomes available.

Simplified:

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

# 16. ACK + Window

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

# 17. Example: Downloading a 10 MB Image

Suppose:

```text
File   = 10 MB
MSS    = 1460 bytes
rwnd   = 5840 bytes
```

### Step 1 — Establish TCP

```text
Client                         Server

SYN ------------------------->
    <---------------- SYN-ACK
ACK ------------------------->
```

### Step 2 — Application Request

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

The number increases because each previous segment carried 1460 bytes.

---

# 18. What If a Segment Is Lost?

Example:

```text
Segment 1 ✅
Segment 2 ❌
Segment 3 ✅
Segment 4 ✅
```

The Sequence Numbers reveal the gap.

For example:

```text
ACK = 2000
```

means:

> "I have everything up to byte 1999, and I still need byte 2000."

TCP has mechanisms to detect the loss and retransmit the missing data.

---

# 19. The Six TCP Flags

The six commonly discussed TCP flags are:

```text
URG
ACK
PSH
RST
SYN
FIN
```

## SYN — Synchronize

Used to start a TCP connection.

```text
Client → SYN → Server
```

> **"Let's start a connection."**

---

## ACK — Acknowledgment

Used to acknowledge received data or TCP control information.

```text
ACK = 1101
```

> **"The next byte I expect is 1101."**

---

## FIN — Finish

Used when a side has finished sending data.

```text
FIN
```

> **"I am finished sending."**

Used during normal TCP termination.

---

## RST — Reset

Used to immediately reset/terminate a TCP connection.

```text
RST
```

> **"Stop/reset this connection immediately."**

Unlike `FIN`, it is not a graceful close.

---

## PSH — Push

Roughly means:

> **"Pass the available data to the application promptly."**

It does **not** mean:

```text
❌ End of the window
❌ End of the connection
❌ Missing segment
❌ Segment number
```

Sequence Numbers are used to determine where data belongs and reveal gaps.

There is also **no general TCP rule that every 4th segment must have PSH set**.

---

## URG — Urgent

Indicates that urgent data is associated with the segment.

```text
URG
↓
Urgent data indication
```

At this level, knowing the purpose is enough.

---

# 20. Flags During Opening and Closing

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

### Immediate Reset

```text
RST
```

---

# 21. Checksum

The TCP/UDP Checksum is used for **Error Detection**.

Simplified idea:

```text
Header + Data
      ↓
Checksum Calculation
      ↓
Checksum Value
```

The sender places the checksum in the header.

The receiver calculates it again.

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

# 22. TCP vs UDP Checksum

Both have a checksum mechanism:

```text
TCP → Checksum ✅
UDP → Checksum ✅
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

# 23. Four-Way TCP Termination

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

# 24. Final Relationship Map

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
       ┌────────────┼────────────────────┐
       │            │                    │
      MSS          rwnd                 cwnd
       │            │                    │
Size of ONE    Receiver capacity    Network congestion
TCP segment          │                    │
                     │                    │
                  Buffer             Congestion Control
                                          │
                               Slow Start / Congestion
                                    Avoidance
                     │                    │
                     └─────────┬──────────┘
                               ↓
                         min(rwnd, cwnd)
                               ↓
                      Amount in flight
                               │
                         Sequence / ACK
                               │
                         Data ordering
                               │
                          Checksum
                               │
                       Error Detection
                               │
                              FIN
                               │
                       4-Way Termination
```

# Core Things to Remember

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

rwnd
→ How much the receiver can currently accept

cwnd
→ How much data TCP currently allows into the network

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
MSS    = size of one piece
Buffer = storage for received data
rwnd   = receiver's available capacity
cwnd   = network's current sending limit
SEQ    = where this piece belongs
ACK    = what byte comes next
PSH    = deliver data to the application
Checksum = detect corruption
SYN    = start
FIN    = finish
RST    = reset
URG    = urgent
```

**The most important relationship:**

```text
MSS → size of ONE segment

rwnd → receiver limit

cwnd → network limit

Actual sending
≈ min(rwnd, cwnd)
```