# Connection Models

Two ways to design how devices share resources in a network.

---

# Work Group (P2P)

- All devices are **equal** — there is no central server managing accounts or permissions.
- Every device manages its **own local user accounts** and permissions.
- A user account created on one PC exists **only on that PC** — it does NOT propagate to other devices.
- Even if two devices have an account with the same name (e.g. "Sara"), they are **two different accounts** with separate permission databases.
- To give the same user access on multiple PCs, you must create the account and set permissions on **each PC separately**.

## How to share a folder with a specific user

The permission is granted to a **user account** that must exist on the sharing machine:

1. Create the account on your PC (`Computer Management` or `Settings → Accounts`).
2. Grant share permission to that account: Right-click folder → `Properties → Sharing → Share` → add the account.
3. When that user connects from their PC (`\\YourPC\SharedFolder`), they type their username + password and get only their own permissions.

> You do NOT need to log out of your account and log in as the other user to grant the permission. You can create the account and set permissions while logged in.


# Client/Server

- One central machine — the **Domain Controller (DC)** — manages all accounts and permissions in one place (Active Directory).
- Users log in with a **single domain account** that works on **any PC in the domain**.
- Permission is granted **once** from the DC and applies everywhere.

## How the DC works

- The DC stores all accounts and permissions centrally.
- When a user logs in, the PC asks the DC: "Who is this user? What permissions do they have?"
- Group Policy (GPO) enforces unified policies (e.g. password strength, blocking USB) across all PCs at once.

## Advantages

- Easier management — add a user once, they appear on every device.
- Central security — permissions controlled from one place.
- The DC is a high-value target for attackers, which is why it is heavily hardened.

---

# Comparison

| | Work Group (P2P) | Client/Server (Domain) |
|---|---|---|
| Control | Distributed (each PC manages itself) | Centralized (DC) |
| Where accounts live | Locally on each PC | Centrally in the DC |
| Account on one PC seen on others? | No | Yes |
| Same username on another PC | Different account | Same account |
| Grant a permission | On each PC separately | Once, from the DC |
| Single point of failure | No | Yes (the DC) |
| Security | Harder to enforce | Easier / centralized |
| Scalability | Limited | High |
| Example | Workgroup sharing, torrent | Company networks, Windows Domain |

---

# Quick Summary

> **P2P = each device manages its own local accounts, so permissions are local.**
> **Client/Server = accounts are centralized in the DC, so permissions follow you everywhere.**

---

## Related Notes

- `Basics Knowledge.md` — OSI layers
- `Basics.md` — network types & topologies
