# Burp Suite CheatSheet

## Table of Contents

- [Overview](#overview)
- [Proxy](#proxy)
- [Target](#target)
- [Repeater](#repeater)
- [Intruder](#intruder)
- [Comparer](#comparer)
- [Decoder](#decoder)
- [Sequencer](#sequencer)
- [Logger](#logger)
- [HTTP History](#http-history)
- [Organizer](#organizer)
- [Professional Workflow](#professional-workflow)
- [Common Shortcuts](#common-shortcuts)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Burp Suite is the industry-standard proxy for web application penetration testing. Intercept, modify, and replay HTTP requests in real time.

---

## Proxy

| Feature | Description |
|---------|-------------|
| **Purpose** | Intercept and modify HTTP/HTTPS traffic between browser and server |
| **When to use** | Every test — this is your primary tool |
| **Intercept** | Pause requests/responses before they reach the server/browser |
| **HTTPS** | Install Burp CA certificate to decrypt TLS traffic |

### Setup

```
1. Configure browser proxy → 127.0.0.1:8080
2. Install Burp CA certificate in browser
3. Enable intercept (or use logging mode)
```

### How Burp MITM Works

```
Browser ←→ Burp ←→ Server
     TLS1    TLS2

Burp generates its own certificate signed by Burp CA.
Browser trusts Burp CA → connection decrypted.
```

---

## Target

| Feature | Description |
|---------|-------------|
| **Purpose** | Map application structure, define scope |
| **When to use** | After initial browsing — review site map |
| **Site Map** | Tree of all discovered content |
| **Scope** | Filter what Burp processes (in-scope vs out-of-scope) |

### Workflow

```
1. Browse the application (proxy traffic flows to Target)
2. Review Site Map — check for unvisited URLs
3. Define Scope — right-click → Add to scope
4. Filter out-of-scope items from view
```

---

## Repeater

| Feature | Description |
|---------|-------------|
| **Purpose** | Manually modify and resend individual requests |
| **When to use** | Testing specific vulnerabilities, verifying findings |
| **Response** | See raw response instantly |

### Workflow

```
1. Send request from Proxy/Target to Repeater (Ctrl+R)
2. Modify request (headers, parameters, body)
3. Click Send
4. Analyze response
5. Iterate until finding is confirmed
```

### Use Cases

- Testing for SQL injection
- Testing access control bypass
- Testing XSS payloads
- Testing file upload restrictions
- Verifying CSRF tokens

---

## Intruder

| Feature | Description |
|---------|-------------|
| **Purpose** | Automated request modification with payloads |
| **When to use** | Brute force, fuzzing, parameter discovery |
| **Positions** | Mark where payloads are inserted |
| **Payloads** | Define payload sets and rules |

### Attack Types

| Type | Description |
|------|-------------|
| Sniper | One payload set, one position at a time |
| Battering Ram | Same payload in all positions |
| Pitchfork | Multiple payload sets, parallel iteration |
| Cluster Bomb | All combinations of multiple payload sets |

### Common Use Cases

- Brute forcing login credentials
- Directory/file brute forcing
- Parameter discovery
- ID enumeration
- Header manipulation

---

## Comparer

| Feature | Description |
|---------|-------------|
| **Purpose** | Compare two pieces of data (byte-by-byte or diff) |
| **When to use** | Comparing responses, finding differences |

### Use Cases

- Comparing responses before/after authorization changes
- Detecting blind SQL injection (response differences)
- Identifying subtle changes in error messages

---

## Decoder

| Feature | Description |
|---------|-------------|
| **Purpose** | Encode/decode data in various formats |
| **Formats** | URL, HTML, Base64, Hex, Gzip, Octal, Binary |

### Quick Use

```
Selected text → Ctrl+U → Send to Decoder
Or: Highlight text in request/response → Send to Decoder
```

---

## Sequencer

| Feature | Description |
|---------|-------------|
| **Purpose** | Analyze randomness of tokens (session IDs, CSRF tokens) |
| **When to use** | Evaluating if tokens are predictable |

### Workflow

```
1. Capture a large sample of tokens
2. Feed them into Sequencer
3. Run analysis (FIPS tests, entropy calculation)
4. Review results
```

---

## Logger

| Feature | Description |
|---------|-------------|
| **Purpose** | Record all HTTP traffic (even non-intercepted) |
| **When to use** | Reviewing background traffic, finding hidden endpoints |

> Unlike Proxy history, Logger captures **all** traffic including from non-browser tools.

---

## HTTP History

| Feature | Description |
|---------|-------------|
| **Purpose** | Browse all requests that passed through the Proxy |
| **When to use** | Reviewing captured traffic, finding endpoints |
| **Filters** | Filter by host, status code, MIME type, etc. |

---

## Organizer

| Feature | Description |
|---------|-------------|
| **Purpose** | Store and organize findings for reports |
| **When to use** | During and after testing — save interesting requests |

---

## Professional Workflow

```
1. Configure scope → Target → Add to scope
2. Browse application → Proxy → HTTP History
3. Review Site Map → Target → Discover hidden content
4. Send interesting requests → Repeater → Manual testing
5. Automate repetitive tests → Intruder
6. Compare responses → Comparer
7. Analyze tokens → Sequencer
8. Save findings → Organizer
9. Generate report → Reporting
```

---

## Common Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Send to Repeater |
| `Ctrl+I` | Send to Intruder |
| `Ctrl+Shift+T` | Switch to Target |
| `Ctrl+Shift+P` | Switch to Proxy |
| `Ctrl+U` | URL-encode selected text |
| `Ctrl+Shift+U` | URL-decode selected text |
| `Ctrl+B` | Base64-encode selected text |
| `Ctrl+Shift+B` | Base64-decode selected text |
| `Ctrl+F` | Find in current tab |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

---

## Bug Bounty Notes

- [ ] Is Burp Proxy intercepting all traffic (including WebSockets)?
- [ ] Are you using the Repeater for manual verification of findings?
- [ ] Did you check HTTP History for hidden endpoints?
- [ ] Are you testing with different Content-Types (JSON, form-data, XML)?
- [ ] Did you test all HTTP methods (GET, POST, PUT, DELETE, PATCH)?
- [ ] Are you using Intruder for brute force and fuzzing?
- [ ] Did you check Logger for background traffic?
- [ ] Are you saving interesting requests to Organizer?
- [ ] Did you configure scope to avoid testing out-of-scope targets?

---

## Checklist

```
□ Burp CA installed and HTTPS decryption working
□ Proxy configured in browser
□ Scope defined for target
□ Initial browsing completed (HTTP History reviewed)
□ Site Map reviewed (Target)
□ Manual testing performed (Repeater)
□ Automated testing performed (Intruder)
□ Token randomness evaluated (Sequencer)
□ Response differences noted (Comparer)
□ Findings saved (Organizer)
```

---

## References

- [PortSwigger Documentation](https://portswigger.net/burp/documentation)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
