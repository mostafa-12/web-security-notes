# Hidden Content

Hidden content refers to resources that exist on the server but are not reachable through normal navigation.

## Common Examples

- Backup files (`.bak`, `.old`, `.save`, `~`)
- Backup archives (`.zip`, `.tar.gz`, `.rar`)
- Unlinked test or beta functionality
- Default application pages
- Old application versions
- Configuration files (`.env`, `config.*`)
- Source code files
- HTML / JavaScript comments
- Log files

## Why Spidering Is Not Enough

A web spider discovers resources by following links.

If a resource has no incoming links, it will not be discovered through normal spidering.

## Key Takeaway

Discovering hidden content requires multiple techniques, including:

- Manual analysis
- Spidering
- Directory/File enumeration
- JavaScript analysis
- Source code review
- Reviewing `robots.txt`
- Guessing common filenames and directories

> Effective hidden content discovery is a combination of automation, manual analysis, and sometimes luck.