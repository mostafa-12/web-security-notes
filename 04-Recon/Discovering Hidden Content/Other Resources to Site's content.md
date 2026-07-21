# Using Public Information

## Concept

Hidden content may still be discoverable through public sources, even if it is no longer linked from the target application.

---

## Useful Sources

- Search Engines
- Web Archives (Wayback Machine)
- Public Documentation
- Third-Party References

---

## Why It Works

Search engines and archives may contain:

- Old pages
- Removed content
- Cached resources
- Historical URLs

Third-party websites may reference:

- Internal portals
- Partner functionality
- APIs
- Documentation

---

## Key Idea

Do not rely only on the current application.

Historical and external sources may reveal hidden resources that are no longer visible on the target website.

# Public Information Recon

## Goal

Leverage public sources to discover:

- Old content
- Removed functionality
- Hidden endpoints
- External references

---

## Useful Sources

- Search Engines
- Web Archives
- Public Documentation
- Other organization domains

---

## Search Techniques

Examples:

```text
site:example.com
```

List indexed pages from the target.

```text
site:example.com login
```

Search for specific functionality inside the target.

---

## Why Historical Content Matters

Old pages may reveal:

- Previous URLs
- Hidden features
- Naming conventions
- Internal paths
- API endpoints

Even if removed, they may provide clues about resources that still exist.

---

## Key Idea

Historical information is valuable even when it is no longer accessible.

Old content often reveals patterns that help identify current hidden functionality.




---

# Developer Footprints

## Concept

Developers often publish technical information while asking for help or discussing implementation details.

These public discussions may reveal valuable reconnaissance information.

---

## Possible Information Leaks

- Technologies in use
- Frameworks
- Hidden endpoints
- Application functionality
- Configuration files
- Log files
- Database names
- Stack traces
- Source code snippets
- Known implementation issues

---

## Common Sources

- Technical forums
- Stack Overflow
- GitHub Issues
- Blog posts
- Community discussions

---

## Key Idea

Public discussions made by developers can unintentionally disclose information that helps map and understand the target application.
# People-Based Recon

## Concept

Developers and staff may unintentionally disclose useful technical information in public.

---

## Possible Sources

- Developer names
- Email addresses
- HTML comments
- Contact pages
- About pages
- Public profiles

---

## Public Information

Search for developers' public technical posts to identify:

- Technologies in use
- Frameworks
- Development issues
- Source code snippets
- Configuration details
- Hidden functionality

---

## Key Idea

People can unintentionally reveal information about an application that the application itself does not expose.
# Leveraging the Web Server

## Concept

The web server itself may expose resources that are unrelated to the application's visible functionality.

---

## Possible Targets

- Default server pages
- Sample applications
- Diagnostic scripts
- Third-party components
- Administrative interfaces

---

## Examples

- phpMyAdmin
- phpinfo.php
- Server status pages
- CMS admin panels
- Sample scripts

---

## Discovery Method

Automated tools use databases of:

- Common directories
- Default files
- Third-party software
- Known server components

to probe for publicly accessible resources.

---

## Key Idea

Not every resource belongs to the custom application.

Some resources come from the web server, framework, or installed software and may expose additional attack surfaces.

