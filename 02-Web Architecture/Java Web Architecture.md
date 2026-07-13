## Java Web Architecture (For Pentesters)

### Java EE (J2EE)

**Not a Framework ❌**
 **It is a Specification (Set of Standards & APIs) ✅**

Defines standards for building **large-scale enterprise applications**.

Goals:
- Multi-tier Architecture
- Load Balancing
- Code Reuse
- Portability between different Application Servers

Examples of implementations:
- Apache Tomcat
- JBoss
- WebLogic

#### Pentesting Note

Knowing the technology stack helps identify:
- Frameworks
- Libraries
- Application Servers

Then search for:
- CVEs
- Known Vulnerabilities
- Misconfigurations

---

### EJB (Enterprise Java Bean)

A **Business Logic Component** managed by the **EJB Container**.

Instead of writing infrastructure yourself, the container automatically provides:

- Transactions
- Security
- Lifecycle Management
- Thread Management
- Resource Management

Example:

```java
TransferEJB.transfer()
```

The container automatically does:

```
Begin Transaction
        ↓
transfer()
        ↓
Commit / Rollback
```

#### Flask Analogy

Instead of writing:

```python
begin_transaction()

try:
    transfer()
    commit()
except:
    rollback()
```

The framework handles everything automatically.

#### Why Heavyweight?

Even if you only need one feature (e.g. Transactions), EJB brings a large infrastructure around your class.

---

### POJO (Plain Old Java Object)

A normal Java Class.

Contains only the Business Logic.

No built-in infrastructure.

If you need extra features, add only what you need (commonly using Spring).

Example:

```java
class TransferService {

    public void transfer() {

    }

}
```

#### Flask Analogy

Similar to writing a normal Python class.

```python
class TransferService:

    def transfer(self):
        ...
```

---

### Servlet

Receives HTTP Requests and returns HTTP Responses.

Acts as the entry point of the application.

Usually it:

- Receives the Request
- Reads Parameters
- Calls Business Logic
- Returns the Response

#### Flask Analogy

```python
@app.route("/login")
def login():
    ...
```

≈

```java
LoginServlet.doPost()
```

Both receive HTTP Requests.

---

### Java Web Container

Runtime Environment that runs Java Web Applications.

Examples:
- Apache Tomcat
- JBoss
- WebLogic

Responsibilities:

- Run the application
- Create Servlets
- Receive HTTP Requests
- Route requests
- Manage Lifecycle
- Return Responses

### Flask Analogy

```
Flask App
      │
Gunicorn / uWSGI
```

↓

```
Servlet
      │
Tomcat
```

Tomcat is similar to Gunicorn (conceptually).

---

### Complete Request Flow

Browser
        │
HTTP Request
        │
Tomcat (Web Container)
        │
Servlet
        │
EJB / POJO
        │
Database
        │
HTTP Response
        │
Browser

---

### Pentesting Notes

Don't memorize technologies.

Instead:

Technology Found
        ↓
Identify its type
        ↓
Framework?
Library?
Application Server?
Web Container?
        ↓
Search for:
- Version
- CVEs
- Public Exploits
- Misconfigurations

Examples:

Headers

```
Server: Apache Tomcat/9
```

↓

Search:

```
Apache Tomcat 9 CVEs
```

Stack Trace

```
org.hibernate...
```

↓

Application uses Hibernate.

Search for known vulnerabilities.

