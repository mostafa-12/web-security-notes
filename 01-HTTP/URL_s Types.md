## URL
***A uniform resource locator (URL)***

### consists of 
~~~http

protocol://hostname[:port]/[path/]file[?param=value]
~~~

1. protocol : language of the communication between client and server 
2. hostname : host name of visited website 
3. Port (optional): Uses the protocol's default port unless a custom port is explicitly specified.
4. path : path to the wanted resource 
5. param: optional params to specify some behaviors of site 
### Relative URLs

/auth/488/YourDetails.ashx?uid=129
YourDetails.ashx?uid=129

- Used for navigation within the same website.
- The browser completes the missing parts (protocol, hostname, etc.).

## REST

Representational State Transfer (REST)

- Architectural style for designing web APIs.
- Resources are identified by URLs.
- "REST-style URLs" put parameters in the path instead of the query string.

Examples

```HTTP

/search?make=ford&model=pinto
/search/ford/Pinto
```

