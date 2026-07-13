## HTTP Request

~~~
GET /auth/488/YourDetails.ashx?uid=129 HTTP/1.1
Accept: application/x-ms-application, image/jpeg, application/xaml+xml,
image/gif, image/pjpeg, application/x-ms-xbap, application/x-shockwave-
flash, */*
Referer: https://mdsec.net/auth/488/Home.ashx
Accept-Language: en-GB
User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64;
Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR
3.0.30729; .NET4.0C; InfoPath.3; .NET4.0E; FDM; .NET CLR 1.1.4322)
Accept-Encoding: gzip, deflate
Host: mdsec.net
Connection: Keep-Alive
Cookie: SessionId=5B70C71F3FD4968935CDB6682E545476
### empty line between header and body of request (required to separation)

~~~

1.  First line consists of 
	1. request method
	2. Requested URL (path + optional query string) 
	3. http version (1.1 is default and must required "Host" header)
2. Accept Header -> Accept -> MIME types the client can accept in the response.
3. Referer ->indicate the URL from which the request originated (WebSite u came from sent by browser automatically)
4. User-Agent -> Identify the client (browser, OS, version).
5. Host -> hostname in URL , important when there is more than one website hosted in the same server
6. Cookie -> attach cookies with request (automatically done by browser)

## HTTP Response

~~~
HTTP/1.1 200 OK
Date: Tue, 19 Apr 2011 09:23:32 GMT
Server: Microsoft-IIS/6.0
X-Powered-By: ASP.NET
Set-Cookie: tracking=tI8rk7joMx44S2Uu85nSWc
X-AspNet-Version: 2.0.50727
Cache-Control: no-cache
Pragma: no-cache
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1067

### empty line between header and body of request (required to separation)

<!DOCTYPE html PUBLIC “-//W3C//DTD XHTML 1.0 Transitional//EN” “http://
www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd”><html xmlns=”http://
www.w3.org/1999/xhtml” ><head><title>Your details</title>
...
~~~


1. First line consists of 
	1. HTTP Version 
	2. status code 
	3. explain status code in human language 
2. Server Header :Information about the web server and technologies (may be inaccurate).
3. Set-Cookie : set cookies by server to send it to him again in future requests 
4. Cache-Control / Pragma / Expires: Control browser caching behavior.
5. Response body (optional) contains the returned resource (HTML, JSON, image, etc.).

