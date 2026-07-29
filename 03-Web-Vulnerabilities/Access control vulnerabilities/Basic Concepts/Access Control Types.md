
# Vertical access control
## +Privileges 

means that every level or role has it's privileges 

### example 

- Guest
  → Read posts

↑

- Authenticated User
  → Guest's privileges
  + Create/Delete own posts

↑

- Admin
  → Authenticated User's privileges
  + Add/Delete users

↑

- Owner
  → Admin's privileges
  + Add/Delete admins

---

### Defect

any user in lower level do function only allowed to users from upper level

Example:

Guest
→ + Add/Delete users ❌

or

Authenticated User
→ + Manage admins ❌

= Vertical Privilege Escalation

# Horizontal access controls

different users have access to a subset of resources of the same type.
Mostafa → Mostafa's resources ✅
Ahmed → Ahmed's resources ✅
Mostafa → Ahmed's resources ❌


# Context-Dependent Access Control

Access depends on the **state** of the application or the **user's interaction**.

### Purpose
- Prevent actions in the wrong order.

### Example

**Right** ✅

```
Add to Cart
    ↓
Checkout
    ↓
Payment
    ↓
Order Confirmed
```

---
**Wrong** ❌

```
Add to Cart
    ↓
Checkout
    ↓
Payment
    ↓
Add to Cart
    ↓
Order Confirmed
```

❌ After payment → Modify shopping cart

### Defect
- Bypass the required workflow.
- Perform restricted actions out of sequence.