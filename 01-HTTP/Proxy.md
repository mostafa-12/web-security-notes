- **Proxy**: intermediary server between Client and Web Server.
- Browser sends all requests to the Proxy instead of the destination server.
- Proxy forwards the request and returns the response.
- Can provide:
	- Caching
	- Authentication
	- Access Control
	- Filtering / Logging

### HTTP Request through Proxy

```http
GET http://example.com/login HTTP/1.1
```

- With plain HTTP, browser sends the **full URL** because the proxy needs to know the destination host.

Flow:

```
Browser ---> Proxy ---> Web Server
```

---

### HTTPS through Proxy

- Proxy **cannot decrypt HTTPS** by itself.
- Browser sends a **CONNECT** request first.

```http
CONNECT example.com:443 HTTP/1.1
```

- If allowed, proxy creates a **TCP Tunnel** to the destination server.

```
Browser ===== Proxy ===== Web Server
         Encrypted TLS Bytes
```

- Proxy only forwards encrypted bytes.
- TLS Handshake happens directly between Browser and Server.

---

### Burp Proxy (MITM)

Normal HTTPS:

```
Browser <==== TLS ====> Web Server
```

Burp inserts itself in the middle:

```
Browser <== TLS ==> Burp <== TLS ==> Web Server
```

- Two independent TLS connections are created:
	1. Browser ↔ Burp
	2. Burp ↔ Target Server

Burp decrypts, inspects, modifies, then re-encrypts traffic.

---

### Burp Certificate

- Burp generates a fake certificate for every visited domain.
- Example:
	- CN = google.com
	- Issuer = Burp Suite CA

Browser accepts it **only if** Burp CA is installed as a trusted CA.

Without trusting Burp CA:

- Browser shows **Certificate Not Trusted** warning.
- Burp cannot transparently intercept HTTPS.

---

### Why Burp can't use Google's real certificate?

- Private keys never leave the real server.
- Burp doesn't have Google's private key.
- Burp must generate its own certificate and sign it using **Burp CA**.

---

### Certificate Pinning

Some applications don't trust the operating system CA store.

Instead, they verify:

- Expected certificate
- or Expected public key

Even if Burp CA is trusted by the system:

```
Burp CA Installed ✅
Certificate Trusted by OS ✅
Application Still Rejects ❌
```

Because the application performs its own certificate validation.

---

### Summary

HTTP Proxy
→ Reads and forwards normal HTTP requests.

HTTPS Proxy
→ Uses CONNECT to create a TCP tunnel.

Burp Proxy
→ Breaks the tunnel into two TLS connections (MITM).

Certificate Trust
→ Browser trusts Burp only after installing Burp CA.

Certificate Pinning
→ Application ignores system trust and verifies the server certificate itself.



