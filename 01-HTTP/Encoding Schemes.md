## Common Encoding Schemes

### URL Encoding
- Encodes special URL characters using `%XX`.
- Example:
  - Space → `%20`
  - `&` → `%26`
  - `=` → `%3D`
- Used to safely send special characters in URLs and request parameters.

### Unicode Encoding
- Represents characters using Unicode values.
- May be used to bypass weak input validation.

### HTML Encoding
- Escapes HTML metacharacters.
- Examples:
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `&` → `&amp;`
- Mainly important when testing for XSS.

### Base64
- Encodes binary/text data using printable ASCII.
- Common in:
  - Cookies
  - Tokens
  - Basic Authentication
- **Base64 is encoding, NOT encryption. Always try decoding it.**

### Hex Encoding
- Represents each byte as hexadecimal.
- Example:
  - `daf` → `646166`

### Pentesting Notes
- Identify the encoding.
- Decode it.
- Analyze the original data.
- Modify it if needed.
- Re-encode before sending the request.