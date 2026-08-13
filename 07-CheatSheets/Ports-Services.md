# Ports & Services CheatSheet

## Table of Contents

- [Overview](#overview)
- [Well-Known Ports](#well-known-ports)
- [Web Ports](#web-ports)
- [Database Ports](#database-ports)
- [Remote Access Ports](#remote-access-ports)
- [Mail Ports](#mail-ports)
- [File Sharing / Other Ports](#file-sharing--other-ports)
- [Port Ranges](#port-ranges)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> A port delivers data to a specific application. Knowing which service runs on which port lets you map the attack surface during recon and pick the right exploitation path.

---

## Well-Known Ports

| Port        | Protocol | Service                    |
| ----------- | -------- | -------------------------- |
| 20 / 21     | TCP      | FTP (data / control)       |
| 22          | TCP      | SSH                        |
| 23          | TCP      | Telnet                     |
| 25          | TCP      | SMTP                       |
| 53          | TCP/UDP  | DNS                        |
| 67 / 68     | UDP      | DHCP (server / client)     |
| 69          | UDP      | TFTP                       |
| 80          | TCP      | HTTP                       |
| 110         | TCP      | POP3                       |
| 123         | UDP      | NTP                        |
| 135         | TCP      | RPC / MSRPC                |
| 137–139     | TCP/UDP  | NetBIOS                    |
| 143         | TCP      | IMAP                       |
| 161 / 162   | UDP      | SNMP (agent / trap)        |
| 389         | TCP      | LDAP                       |
| 443         | TCP      | HTTPS                      |
| 445         | TCP      | SMB (Windows file sharing) |
| 465 / 587   | TCP      | SMTP (SSL / submission)    |
| 636         | TCP      | LDAPS                      |
| 993 / 995   | TCP      | IMAPS / POP3S              |
| 1433        | TCP      | MSSQL                      |
| 1521        | TCP      | Oracle DB                  |
| 2049        | TCP      | NFS                        |
| 2375 / 2376 | TCP      | Docker (unencrypted / TLS) |
| 3306        | TCP      | MySQL / MariaDB            |
| 3389        | TCP      | RDP                        |
| 5432        | TCP      | PostgreSQL                 |
| 5900        | TCP      | VNC                        |
| 6379        | TCP      | Redis                      |
| 8080        | TCP      | HTTP alternative / proxies |
| 8443        | TCP      | HTTPS alternative          |
| 9200        | TCP      | Elasticsearch              |
| 11211       | TCP/UDP  | Memcached                  |
| 27017       | TCP      | MongoDB                    |

---

## Web Ports

| Port        | Service   | Notes                                               |
| ----------- | --------- | --------------------------------------------------- |
| 80          | HTTP      | Default for web                                     |
| 443         | HTTPS     | Default for secure web                              |
| 8080        | HTTP-alt  | Common for proxies, dev servers, Tomcat             |
| 8443        | HTTPS-alt | Common alternative to 443                           |
| 8000 / 8888 | HTTP-dev  | Common dev servers                                  |
| 8009        | AJP       | Apache JServ protocol (may reveal Tomcat internals) |

> **Security Note:** Custom ports (e.g. web on 8443 or 1337) are not hiding — scanners and Shodan still find them.

---

## Database Ports

| Port | Service | Security Note |
|------|---------|---------------|
| 1433 | MSSQL | xp_cmdshell abuse potential |
| 1521 | Oracle | TNS listener attacks |
| 3306 | MySQL | Should be internal-only |
| 5432 | PostgreSQL | Often exposed by misconfig |
| 6379 | Redis | Unauthenticated RCE if open |
| 9200 | Elasticsearch | Unauthenticated data leak |
| 11211 | Memcached | UDP amplification / data leak |
| 27017 | MongoDB | Open = full database exposure |

> Databases exposed on the internet are a high-value finding — never dismiss an open DB port.

---

## Remote Access Ports

| Port | Service | Security Note |
|------|---------|---------------|
| 22 | SSH | Brute-force target; check key auth |
| 23 | Telnet | Unencrypted — credentials leak |
| 3389 | RDP | Brute-force / NLA check |
| 5900 | VNC | Often no/lazy auth |

---

## Mail Ports

| Port | Service | Notes |
|------|---------|-------|
| 25 | SMTP | Email sending; open relay check |
| 110 | POP3 | Unencrypted |
| 143 | IMAP | Unencrypted |
| 465 | SMTPS | SSL |
| 587 | SMTP-submission | Client submission |
| 993 | IMAPS | SSL |
| 995 | POP3S | SSL |

---

## File Sharing / Other Ports

| Port | Service | Notes |
|------|---------|-------|
| 21 | FTP | Check anonymous login |
| 69 | TFTP | Often no auth |
| 445 | SMB | EternalBlue history, SMBv1 check |
| 137–139 | NetBIOS | Legacy, info disclosure |
| 2049 | NFS | Check exported shares |
| 389 / 636 | LDAP / LDAPS | Anonymous bind check |

---

## Port Ranges

| Range | Name | Purpose |
|-------|------|---------|
| 0 – 1023 | Well-Known | Core system services |
| 1024 – 49151 | Registered | Application services |
| 49152 – 65535 | Dynamic / Ephemeral | Temporary client connections |

---

## Bug Bounty Notes

- [ ] Does an uncommon port (8080, 8443, 8000) host a different app than the main one?
- [ ] Is any database port (3306, 5432, 6379, 9200) reachable from the internet?
- [ ] Is SSH on a non-default port (hiding attempt)?
- [ ] Does FTP allow anonymous login?
- [ ] Is SNMP (161) exposing community strings / system info?
- [ ] Are backup/legacy services (Telnet, NetBIOS, SMBv1) still running?
- [ ] Does the service version match known vulnerabilities (searchsploit / NVD)?
- [ ] Is Docker (2375) exposed without TLS?

---

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| Only scanning well-known ports | Real targets often run on registered/custom ports |
| Ignoring UDP ports | SNMP, DNS, NTP, TFTP live on UDP |
| Assuming a changed port hides a service | Scanners + Shodan still see it |
| Not fingerprinting versions | Version = the actual exploit path |
| Dismissing "boring" DB ports | Open DB = massive data exposure |

---

## Checklist

```
□ Full TCP scan (1-65535) performed
□ Top UDP ports scanned (53, 69, 123, 161, 500, 4500)
□ Service versions fingerprinted (nmap -sV)
□ Database ports checked for internet exposure
□ Anonymous FTP / SNMP / NFS checked
□ Legacy services (Telnet, NetBIOS, SMBv1) checked
□ Web app on every discovered port reviewed
□ Version CVE lookup done
```

---

## References

- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- [Nmap Ports Database](https://nmap.org/book/ports.html)
