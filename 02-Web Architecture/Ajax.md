## Ajax (Asynchronous JavaScript and XML)

- Ajax is a set of techniques that allows JavaScript to communicate with the server **without reloading the entire page**.
- It sends **background HTTP requests** and updates only the required part of the page using the **DOM**.
- Modern applications usually exchange **JSON** instead of XML.
- The traditional JavaScript API is **XMLHttpRequest (XHR)**, while modern applications often use **Fetch API**.

### Traditional Web App

User Action → HTTP Request → Full Page Reload

### Ajax Web App

User Action → Ajax Request → Server Response → DOM Update (No Page Reload)

### Example

Click **Add to Cart**:

1. JavaScript sends an Ajax request.
2. The server updates the cart.
3. The server returns a small response (e.g., updated cart count).
4. JavaScript updates only the cart icon using the DOM.

### Security Notes

- Ajax increases the application's **Attack Surface** by introducing more endpoints.
- Always inspect Ajax/XHR/Fetch requests in Burp Suite, as they often expose hidden functionality and APIs.


