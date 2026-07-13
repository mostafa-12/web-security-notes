## Document Object Model (DOM)

- The DOM is the browser's in-memory representation of an HTML page.
- JavaScript interacts with the DOM, not the raw HTML file.
- It allows JavaScript to:
    - Read or modify HTML elements.
    - Read the current URL.
    - Access cookies (unless HttpOnly).
    - Listen for events (click, submit, keypress, ...).
- Modern web applications use the DOM heavily with Ajax to update parts of the page without reloading.

### Example

```javascript
document.getElementById("title").innerText = "Ahmed";
```

Changes the page content without refreshing it.

***HTML Document***
~~~html
<h1 id="title">Hello</h1>

<input id="name">

<button>Save</button>
~~~

***HTML DOM Tree***
~~~
Document
│
├── html
│   ├── head
│   └── body
│       ├── h1
│       ├── input
│       └── button
~~~

