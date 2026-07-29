# Site Map

A Site Map is a page or file that lists the application's pages and helps users (or search engines) navigate the website.

It can be a useful starting point for content discovery and application mapping.

## Types

### HTML Site Map

A human-readable page containing links to important sections of the website.

Example:

```text
/sitemap
/site-map
```

### XML Sitemap

A machine-readable file designed for search engines.

Example:

```text
/sitemap.xml
```

## Note

Do **not** confuse a website's **Site Map** with **Burp Suite's Site Map**.

- **Website Site Map:** Provided by the application to list its content.
- **Burp Site Map:** Generated automatically from the HTTP requests captured during browsing.


# Difference Between robots.txt and sitemap.xml
| **Feature / Aspect** | **robots.txt (Prevention & Control)**                                                    | **sitemap.xml (Invitation & Guidance)**                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Core Function**    | Defines the areas that search engine crawlers are **not allowed** to visit (`Disallow`). | Defines the complete list of pages you **want** to be indexed and appear in search results.              |
| **Direction Method** | **Negative:** Restricts and blocks access.                                               | **Positive:** Facilitates, suggests, and guides access.                                                  |
| **Crawl Priority**   | The very first file the crawler visits upon entering the site to know its boundaries.    | Visited later by the crawler as a reference to quickly find new or updated pages (site's pages history). |
| **Example Content**  | `Disallow: /admin-panel/`                                                                | `<loc>[https://site.com/blog/article1](https://site.com/blog/article1)</loc>`                            |
*Note* : robots.txt located in /
