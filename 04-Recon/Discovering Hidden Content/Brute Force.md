# Brute-Force Content Discovery

## Concept

If hidden resources cannot be discovered through spidering, they may be found by guessing common names.

---

## Example

Discovered:

```text
/auth/
/images/
/include/
/home/
```

Possible guesses:

```text
/admin/
/api/
/uploads/
/backup/
/test/
/dashboard/
```

---

## Method

1. Generate requests using common directory/file names.
2. Send requests automatically.
3. Analyze server responses.
4. Identify existing resources.

---

## Goal

Discover hidden content that has no incoming links.

---

## Key Idea

Brute-force discovery is **not random guessing**.

It is guided by:

- Existing application structure
- Common naming conventions
- Wordlists
- Previous reconnaissance findings


## Note : 
***after realizing appliction and knowing it shown dirs we can generate word list by AI depends on results we get by manual or automating spidering *** 


# Inference from Published Content

## Concept

Applications usually follow consistent naming conventions.

Previously discovered resources can be used to predict additional hidden content.

---

## Naming Conventions

Example:

```text
/auth/Login
/auth/Register
/auth/ForgotPassword
```

Possible related resources:

```text
/auth/ResetPassword
/auth/UpdatePassword
/auth/RetrievePassword
```

Instead of random guessing, generate requests that follow the application's naming style.

---

## Numeric Patterns

Example:

```text
/pub/media/100
/pub/media/117
/pub/user/11
```

Likely candidates:

```text
/pub/media/101
/pub/media/102
/pub/media/103

/pub/user/10
/pub/user/12
```

Sequential or predictable identifiers often reveal additional resources.

---

## Key Idea

Use the application's existing structure as a guide.

The goal is to perform **context-aware enumeration**, not random brute force.

Every discovered resource provides clues about:

- Naming conventions
- URL structure
- Identifier patterns
- Possible hidden functionality