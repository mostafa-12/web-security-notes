## HTTP Methods 

- GET:
	- Retrieve data from the server.
	- Parameters are usually sent in the URL query string.
	- Safe to bookmark and share.
	- Never send sensitive data in the URL.
- POST : 
	- Creates New resource in server
	- Perform an action on the server.
	- Data is sent in the request body (can also use query parameters).
	- Used for actions like login, registration, updating data.
	- Browser warns before resending a POST request (to avoid repeating actions).
- HEAD : same as GET but without body content only headers
- TRACE : same request's body is same response's body (to check there is no Data-Manipulation)
	- زي صدي الصوت في ال tcp channel 
- OPTION : show allowed HTTP Methods can be performed 
- PUT:
	- Upload or replace a resource.
	- If enabled, it may allow arbitrary file upload (security risk).
- PATCH : Partially replaces an existing resource

***Note : query params can be booked marked  with URL***
