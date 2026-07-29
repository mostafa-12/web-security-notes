
# Idea 
making URL to sensitive function or page unpredictable like :
```URL
https://insecure-website.com/administrator-panel-yb556
```

it can't be practicable be human and sometimes by brute force, but it can be leaked by many ways like js file

```js
<script>
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```

this code show link to admin-panel by checking if user is admin or not, 
take a look:

- first it's check by **isAdmin** is True or False 
- if True js accesses page document and create a link tage (a tag)
- then it is setting **href attribute with link of admin-panel**  and that what we want 
- then make inner text of tag Admin panel 

# Solution 
- first look at raw scripts was written in page (solution here )
- second request js file and look at it and links in it   
