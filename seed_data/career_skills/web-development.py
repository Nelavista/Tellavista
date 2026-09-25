"""Seed data for the Web Development 30-Day Skill Class."""

SKILL = {
    "slug": "web-development",
    "name": "Web Development",
    "tagline": "Learn to build and ship real websites and web apps that live on the internet, not just your laptop.",
    "description": "Web development is the skill of building the websites and web applications that businesses, schools, and startups run on every day. It is one of the most in-demand and accessible tech skills for a Nigerian student because the tools are free, remote freelance work is abundant, and a working portfolio site is proof enough to get hired without a formal degree in the field. This track takes you from understanding how a browser loads a page to building and deploying a full-stack, multi-page web application with a live public URL.",
    "level": "beginner",
    "estimated_hours": 64,
    "course_title": "30-Day Web Development Career Track",
    "course_description": "After 30 days you will be able to build responsive, multi-page websites with HTML, CSS, and JavaScript, build interactive frontends with React, connect them to a real backend API, and deploy a full-stack application live on the internet.",
    "final_project": {
        "title": "Build and Deploy a Production-Style Web Application",
        "description": "Design, build, and deploy a multi-page web application with a live public URL, such as a student marketplace, a local business directory, an event booking tool, or a personal finance tracker. The app must include at least three distinct pages or views, a working backend API with a real database, at least one form that creates or updates data, and basic error and loading state handling. It must be deployed to a live host like Vercel, Netlify, or Render so anyone with the link can use it, and include a README documenting the architecture and setup. This is the exact kind of live, working project that convinces a client or hiring manager you can ship real software, not just write code.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["HTML/CSS", "JavaScript", "React", "REST API design", "database integration", "deployment", "responsive design"],
        "rubric": [
            {"name": "Functionality and multi-page navigation", "max_points": 30},
            {"name": "Backend API and data persistence", "max_points": 25},
            {"name": "Frontend code quality and responsiveness", "max_points": 25},
            {"name": "Successful live deployment and documentation", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "How the Web Actually Works",
            "title": "What Happens When a Browser Loads Your Website",
            "learning_objective": "By the end of this class, you will be able to explain the request-response cycle that happens when a browser loads a webpage.",
            "duration_minutes": 20,
            "content_html": """<p>Every time someone types a website address or taps a link, a whole sequence of events happens in under a second to put a page on their screen. Understanding this sequence is the foundation everything else in web development builds on, and it is a question that comes up constantly in junior developer interviews.</p><h2>The Request-Response Cycle</h2><p>The browser sends an HTTP request to a server asking for a page. The server processes that request and sends back an HTTP response, usually containing HTML, CSS, and JavaScript files. The browser then reads the HTML to build the page structure, applies the CSS for styling, and runs the JavaScript for interactivity.</p><pre><code>Browser  --- GET request --->  Server
Browser  <--- HTML/CSS/JS ---  Server</code></pre><h2>Frontend vs Backend</h2><p>Everything the browser builds and displays is called the <strong>frontend</strong>. The server-side code that processes requests, talks to databases, and sends back responses is the <strong>backend</strong>. Web developers often specialize in one side or work across both (called full-stack), and this track will teach you enough of both to build a complete application by day 30. Nigerian tech job listings for "frontend developer," "backend developer," and "full-stack developer" all build on this same core mental model.</p>""",
            "key_concepts": ["HTTP request-response cycle", "frontend vs backend", "client-server model", "browser rendering"],
            "practical_exercise": {
                "title": "Trace a Real Page Load",
                "instructions": "Open your browser's developer tools (right-click, Inspect, then the Network tab), visit any website, and reload the page. Find the first HTML request in the list, note its status code, and identify at least three other file types (CSS, JS, images) that were also requested. Submit a screenshot of the Network tab with these items labeled."
            },
            "quiz": [
                {"question": "What does the browser send to a server to request a webpage?", "options": ["An HTML file", "An HTTP request", "A CSS stylesheet", "A JavaScript function"], "correct_index": 1, "explanation": "The browser sends an HTTP request to the server, which then responds with the requested resources."},
                {"question": "Which part of a website is called the 'backend'?", "options": ["The visible layout and styling", "The server-side code that processes requests and talks to databases", "The browser's address bar", "The website's logo"], "correct_index": 1, "explanation": "The backend refers to server-side logic, including request processing and database interactions, which the user never sees directly."},
                {"question": "What three things does the browser use to build and display a page after receiving a response?", "options": ["Only HTML", "HTML, CSS, and JavaScript", "Only images", "Only a database connection"], "correct_index": 1, "explanation": "The browser combines HTML for structure, CSS for styling, and JavaScript for interactivity to render a complete page."}
            ],
            "resources": [
                {"label": "MDN: How the Web Works", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "How the Web Actually Works",
            "title": "Setting Up Your Web Development Toolkit: VS Code, Git, and GitHub",
            "learning_objective": "By the end of this class, you will be able to set up a local development environment with a code editor, Git, and a GitHub repository.",
            "duration_minutes": 25,
            "content_html": """<p>Professional web developers do not write code in random text editors and email files to each other. They use a standard toolkit: a code editor built for programming, Git for tracking changes, and GitHub for hosting code and collaborating. Setting this up correctly today saves you from painful workarounds for the rest of this track.</p><h2>Installing Your Tools</h2><p>Install VS Code as your code editor, and Git for version control. VS Code has extensions like Live Server that let you preview HTML changes instantly in the browser as you save.</p><pre><code>git init
git add .
git commit -m "Initial commit"</code></pre><h2>Connecting to GitHub</h2><p>Create a free GitHub account, create a new repository, and push your local project to it. This gives you a backup of your code, a portfolio employers can browse, and practice with the exact workflow used on real engineering teams.</p><pre><code>git remote add origin https://github.com/yourname/project.git
git push -u origin main</code></pre><p>Every project you build for the rest of this track should live in its own GitHub repository — by day 30 your GitHub profile itself becomes part of your job application.</p>""",
            "key_concepts": ["VS Code", "Git version control", "GitHub repositories", "git init/add/commit/push"],
            "practical_exercise": {
                "title": "Set Up and Push Your First Repository",
                "instructions": "Install VS Code and Git, create a folder called my-first-site with a single index.html file containing basic text, initialize a Git repository, commit it, create a GitHub repository, and push your code to it. Submit the link to your GitHub repository."
            },
            "quiz": [
                {"question": "What is the purpose of Git in a developer's workflow?", "options": ["To design page layouts", "To track changes to code over time and enable collaboration", "To host images", "To write CSS"], "correct_index": 1, "explanation": "Git is a version control system that tracks code changes, letting developers collaborate and undo mistakes safely."},
                {"question": "What command uploads your local commits to GitHub?", "options": ["git commit", "git push", "git pull", "git init"], "correct_index": 1, "explanation": "git push uploads local commits to a remote repository like GitHub."},
                {"question": "Why does a GitHub profile matter for a web developer job search?", "options": ["It has no real impact on hiring", "It serves as a visible portfolio employers can browse to see real code and projects", "It replaces the need for a resume entirely", "GitHub is only used for private projects"], "correct_index": 1, "explanation": "A GitHub profile showcasing real projects gives employers direct evidence of a candidate's skills and work habits."}
            ],
            "resources": [
                {"label": "GitHub", "url": "https://github.com/"},
                {"label": "Git Documentation", "url": "https://git-scm.com/doc"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "How the Web Actually Works",
            "title": "Structuring a Webpage with Semantic HTML",
            "learning_objective": "By the end of this class, you will be able to build a well-structured webpage using semantic HTML elements.",
            "duration_minutes": 25,
            "content_html": """<p>HTML is the skeleton of every webpage. Before any styling or interactivity is added, HTML defines what content exists and how it is organized, which matters not just for humans but for search engines and screen readers used by visually impaired users.</p><h2>Semantic vs Generic Elements</h2><p><strong>Semantic HTML</strong> means using tags that describe their content's purpose, like header, nav, main, article, and footer, instead of generic div tags everywhere. This makes your page more accessible and better ranked by search engines, both of which matter to real employers and clients.</p><pre><code>&lt;header&gt;
  &lt;h1&gt;Campus Marketplace&lt;/h1&gt;
  &lt;nav&gt;&lt;a href="#listings"&gt;Listings&lt;/a&gt;&lt;/nav&gt;
&lt;/header&gt;
&lt;main&gt;
  &lt;article&gt;
    &lt;h2&gt;Textbook for Sale&lt;/h2&gt;
    &lt;p&gt;Used Calculus textbook, N3000.&lt;/p&gt;
  &lt;/article&gt;
&lt;/main&gt;
&lt;footer&gt;&lt;p&gt;Contact us&lt;/p&gt;&lt;/footer&gt;</code></pre><h2>Why This Matters for Your Career</h2><p>Recruiters and senior developers reviewing your code notice whether you use semantic HTML, because it signals you learned web development properly rather than copying random templates. Screen readers rely on these tags to describe pages to blind users, so semantic HTML is also a basic accessibility requirement in most professional projects and job postings.</p>""",
            "key_concepts": ["semantic HTML", "header/nav/main/footer", "accessibility", "SEO basics", "document structure"],
            "practical_exercise": {
                "title": "Build a Semantic HTML Page",
                "instructions": "Build a single HTML page for a fictional personal portfolio using semantic tags: header with a nav, a main section with at least two article elements, and a footer. Do not use any div tags for this exercise. Submit your HTML file."
            },
            "quiz": [
                {"question": "What does 'semantic HTML' mean?", "options": ["HTML written in a foreign language", "Using tags that describe the purpose of their content, like nav or article", "HTML that only works on mobile", "HTML with no styling at all"], "correct_index": 1, "explanation": "Semantic HTML uses meaningful tags (header, nav, main, article) that describe the role of the content they contain."},
                {"question": "Why is semantic HTML important for accessibility?", "options": ["It makes pages load faster only", "Screen readers rely on semantic tags to describe page structure to visually impaired users", "It has no accessibility benefit", "It only matters for print layouts"], "correct_index": 1, "explanation": "Screen readers use semantic elements to help users navigate and understand a page's structure, which generic divs do not provide."},
                {"question": "Which of these is a semantic HTML element?", "options": ["<div>", "<span>", "<article>", "<b>"], "correct_index": 2, "explanation": "<article> is a semantic element describing a self-contained piece of content, unlike generic elements like div or span."}
            ],
            "resources": [
                {"label": "MDN: HTML Elements Reference", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML"},
                {"label": "W3Schools HTML Tutorial", "url": "https://www.w3schools.com/html/"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "How the Web Actually Works",
            "title": "Styling Pages with CSS: Selectors, the Box Model, and Layout Basics",
            "learning_objective": "By the end of this class, you will be able to style an HTML page using CSS selectors and correctly reason about the box model.",
            "duration_minutes": 30,
            "content_html": """<p>CSS controls everything about how a page looks: colors, spacing, fonts, and positioning. Nearly every visual bug a beginner hits — elements overlapping, spacing that will not behave, layouts breaking on resize — traces back to a misunderstanding of the box model, so getting this right early saves enormous frustration later.</p><h2>Selectors</h2><p>CSS selectors target which elements a style applies to, using tag names, classes, or ids.</p><pre><code>p { color: #333; }
.card { border: 1px solid #ddd; padding: 16px; }
#main-title { font-size: 32px; }</code></pre><h2>The Box Model</h2><p>Every HTML element is a box made of four layers, from inside out: content, padding, border, and margin. Padding adds space inside the border, margin adds space outside it, and misunderstanding this is the single most common source of layout confusion for beginners.</p><pre><code>.card {
  width: 300px;
  padding: 16px;
  border: 2px solid #333;
  margin: 20px;
  box-sizing: border-box;
}</code></pre><p>Setting box-sizing: border-box, as shown above, makes width include padding and border rather than adding to it, which is what most developers use by default because it makes sizing far more predictable.</p>""",
            "key_concepts": ["CSS selectors", "box model", "padding, border, margin", "box-sizing"],
            "practical_exercise": {
                "title": "Style Your Semantic HTML Page",
                "instructions": "Take the portfolio page you built on Day 3 and style it with CSS: set a font and color scheme, style your article elements as cards with padding, border, and margin, and set box-sizing: border-box globally. Submit your updated HTML and CSS files."
            },
            "quiz": [
                {"question": "In the CSS box model, what does padding control?", "options": ["Space outside the element's border", "Space inside the element, between its content and its border", "The element's text color", "The element's font size"], "correct_index": 1, "explanation": "Padding is the space between an element's content and its border, inside the box."},
                {"question": "What does setting box-sizing: border-box do?", "options": ["It removes all borders from an element", "It makes an element's declared width include its padding and border", "It hides the element", "It centers the element automatically"], "correct_index": 1, "explanation": "border-box makes the specified width/height include padding and border, making sizing more predictable."},
                {"question": "Which CSS selector targets an element by its class?", "options": ["#main-title", "p", ".card", "*"], "correct_index": 2, "explanation": "A period before a name (.card) selects elements with that class attribute."}
            ],
            "resources": [
                {"label": "MDN: CSS Box Model", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model"},
                {"label": "W3Schools CSS Tutorial", "url": "https://www.w3schools.com/css/"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "How the Web Actually Works",
            "title": "Making Layouts Responsive with Flexbox and Grid",
            "learning_objective": "By the end of this class, you will be able to build a layout that adapts correctly to different screen sizes using Flexbox and Grid.",
            "duration_minutes": 30,
            "content_html": """<p>Most web traffic today, especially in Nigeria, comes from mobile phones, so a site that only looks good on a laptop screen is a broken site in practice. Responsive design means building layouts that adapt gracefully across screen sizes, and Flexbox and Grid are the two modern CSS tools that make this achievable without hacks.</p><h2>Flexbox for One-Dimensional Layouts</h2><p>Flexbox arranges items in a single row or column and is ideal for navigation bars, card rows, and centering content.</p><pre><code>.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}</code></pre><h2>Grid for Two-Dimensional Layouts</h2><p>CSS Grid handles rows and columns together, making it the right tool for full page layouts or card galleries.</p><pre><code>.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}</code></pre><h2>Media Queries for Breakpoints</h2><p>Media queries apply different CSS rules depending on screen width, which is how you adjust a layout for phones versus desktops.</p><pre><code>@media (max-width: 600px) {
  .nav { flex-direction: column; }
}</code></pre><p>Testing your layout by resizing the browser window, or using your browser's device toolbar, should become an automatic habit every time you style a new page.</p>""",
            "key_concepts": ["Flexbox", "CSS Grid", "responsive design", "media queries", "mobile-first layout"],
            "practical_exercise": {
                "title": "Build a Responsive Card Gallery",
                "instructions": "Build a page with a Flexbox navigation bar and a Grid-based gallery of at least six cards. Add a media query so the navigation stacks vertically and the gallery becomes a single column on screens under 600px wide. Test it by resizing your browser and submit your HTML/CSS along with a screenshot at both desktop and mobile widths."
            },
            "quiz": [
                {"question": "Which CSS layout tool is best suited for a full two-dimensional page layout with rows and columns?", "options": ["Flexbox", "CSS Grid", "The box model alone", "Semantic HTML"], "correct_index": 1, "explanation": "CSS Grid is designed for two-dimensional layouts involving both rows and columns simultaneously."},
                {"question": "What does a CSS media query allow you to do?", "options": ["Add images to a page", "Apply different CSS rules based on conditions like screen width", "Connect to a database", "Write JavaScript inside CSS"], "correct_index": 1, "explanation": "Media queries let you apply CSS rules conditionally, commonly based on the viewport width, enabling responsive design."},
                {"question": "Why is responsive design especially important for a Nigerian audience?", "options": ["Nigerian users only use desktop computers", "A large share of web traffic comes from mobile phones, so non-responsive sites break for many users", "Responsive design is only a legal requirement in some countries", "It has no particular relevance to any specific audience"], "correct_index": 1, "explanation": "With mobile phones being the primary internet access point for many Nigerian users, non-responsive layouts fail a large share of the actual audience."}
            ],
            "resources": [
                {"label": "MDN: CSS Flexbox", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout"},
                {"label": "MDN: CSS Grid", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Bringing Pages to Life with JavaScript",
            "title": "Adding Interactivity with JavaScript: Variables, Functions, and Events",
            "learning_objective": "By the end of this class, you will be able to write JavaScript that responds to user actions like clicks using variables, functions, and event listeners.",
            "duration_minutes": 30,
            "content_html": """<p>HTML and CSS give a page structure and style, but they cannot make anything actually happen when a user clicks a button. JavaScript is the language that runs inside the browser and makes pages interactive, and it is a required skill for essentially every web developer job posting that exists.</p><h2>Variables and Functions</h2><p>Variables store values, and functions bundle reusable logic together.</p><pre><code>let cartTotal = 0;

function addToCart(price) {
  cartTotal += price;
  console.log("Cart total is now:", cartTotal);
}</code></pre><h2>Responding to Events</h2><p>An event listener runs a function whenever a specific action happens, like a button being clicked.</p><pre><code>const button = document.querySelector("#add-btn");
button.addEventListener("click", function () {
  addToCart(1500);
});</code></pre><p>This click-to-function pattern is the backbone of almost every interactive feature on the web: form submissions, dropdown menus, image sliders, and shopping carts all boil down to "when this event happens, run this function." Getting comfortable reading and writing this pattern today makes every later class in this track click faster.</p>""",
            "key_concepts": ["JavaScript variables", "functions", "event listeners", "DOM selection basics"],
            "practical_exercise": {
                "title": "Build a Click Counter",
                "instructions": "Build an HTML page with a button and a number displayed as text starting at 0. Write JavaScript so that each click increases the displayed number by 1, using a variable to track the count and an event listener on the button. Submit your HTML and JavaScript files."
            },
            "quiz": [
                {"question": "What does an event listener do?", "options": ["Styles an HTML element", "Runs a specified function when a particular event, like a click, occurs", "Connects to a database", "Deletes an HTML element permanently"], "correct_index": 1, "explanation": "An event listener waits for a specific event (like a click) and runs the given function when it happens."},
                {"question": "Which method is commonly used to select an HTML element in JavaScript by its id?", "options": ["document.querySelector('#id')", "document.createElement()", "document.write()", "document.styleSheet()"], "correct_index": 0, "explanation": "document.querySelector('#id') selects the first element matching the given CSS-style selector, including id selectors."},
                {"question": "What is the role of a function in JavaScript?", "options": ["To store a single value permanently", "To bundle reusable logic that can be called whenever needed", "To style HTML elements", "To define the page's structure"], "correct_index": 1, "explanation": "Functions group logic into a reusable, callable block, avoiding repeated code."}
            ],
            "resources": [
                {"label": "MDN: JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
                {"label": "freeCodeCamp", "url": "https://www.freecodecamp.org/"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Bringing Pages to Life with JavaScript",
            "title": "Manipulating the DOM to Build Dynamic Pages",
            "learning_objective": "By the end of this class, you will be able to create, modify, and remove HTML elements dynamically using JavaScript DOM methods.",
            "duration_minutes": 30,
            "content_html": """<p>The DOM (Document Object Model) is the browser's live, in-memory representation of your HTML page, and JavaScript's real power comes from being able to read and change it after the page has already loaded. This is how a to-do list adds new items, how a like button updates a count, and how a page updates without a full reload.</p><h2>Creating and Adding Elements</h2><p>You can build new elements entirely in JavaScript and insert them into the page.</p><pre><code>const list = document.querySelector("#todo-list");
const item = document.createElement("li");
item.textContent = "Buy groceries";
list.appendChild(item);</code></pre><h2>Updating and Removing Elements</h2><p>Existing elements can be changed or removed the same way.</p><pre><code>item.textContent = "Buy groceries - done";
item.classList.add("completed");
item.remove();</code></pre><p>Every dynamic feature you have ever used on a website — adding items to a cart without reloading, marking a task complete, showing a live comment count — is built from exactly these three operations: create, update, and remove. Mastering this pattern today is the direct foundation for how frameworks like React work under the hood, which you will start learning next week.</p>""",
            "key_concepts": ["DOM", "createElement", "appendChild", "classList", "dynamic content"],
            "practical_exercise": {
                "title": "Build a Working To-Do List",
                "instructions": "Build a page with a text input and an 'Add' button. When clicked, add the input's text as a new list item to a visible list on the page, and clear the input. Add a 'Delete' button next to each item that removes it from the list when clicked. Submit your HTML, CSS, and JavaScript files."
            },
            "quiz": [
                {"question": "What does the DOM represent?", "options": ["The website's source code file only", "The browser's live, in-memory representation of the HTML page", "A type of CSS selector", "A database table"], "correct_index": 1, "explanation": "The DOM is the browser's dynamic, in-memory tree structure of the page that JavaScript can read and modify."},
                {"question": "Which JavaScript method creates a brand new HTML element?", "options": ["document.remove()", "document.createElement()", "document.querySelector()", "document.write()"], "correct_index": 1, "explanation": "document.createElement() creates a new, detached HTML element that can then be added to the page."},
                {"question": "What does the .remove() method do when called on a DOM element?", "options": ["It hides the element temporarily", "It permanently removes the element from the page", "It changes the element's color", "It duplicates the element"], "correct_index": 1, "explanation": ".remove() deletes the element from the DOM entirely, removing it from the visible page."}
            ],
            "resources": [
                {"label": "MDN: Document Object Model", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Bringing Pages to Life with JavaScript",
            "title": "Working with Forms and Validating User Input",
            "learning_objective": "By the end of this class, you will be able to capture form input, prevent default form submission, and validate user input with JavaScript.",
            "duration_minutes": 25,
            "content_html": """<p>Forms are how users give information to a website: signing up, logging in, posting a listing, submitting an order. A form that lets bad data through, or crashes on unexpected input, is a common and embarrassing bug that scares off real users, so validating input properly is a core, expected skill.</p><h2>Capturing Form Data</h2><p>The submit event fires when a user submits a form, and preventDefault stops the page from doing a full reload, which is the standard browser behavior otherwise.</p><pre><code>const form = document.querySelector("#signup-form");
form.addEventListener("submit", function (event) {
  event.preventDefault();
  const email = document.querySelector("#email").value;
  console.log("Submitted email:", email);
});</code></pre><h2>Validating Input</h2><p>Basic validation checks that required fields are filled and formatted correctly before the data is used or sent anywhere.</p><pre><code>if (!email.includes("@")) {
  alert("Please enter a valid email address.");
  return;
}
if (password.length < 8) {
  alert("Password must be at least 8 characters.");
  return;
}</code></pre><p>HTML also offers built-in validation attributes like required and type="email", which are worth combining with JavaScript checks, since relying on JavaScript alone can be bypassed and relying on HTML alone gives poor error messages.</p>""",
            "key_concepts": ["form submit event", "preventDefault", "input validation", "HTML validation attributes"],
            "practical_exercise": {
                "title": "Build a Validated Signup Form",
                "instructions": "Build a signup form with name, email, and password fields. Prevent the default submission, and validate that name is not empty, email contains an @ symbol, and password is at least 8 characters, showing a clear error message for each failed check. On successful validation, display a success message on the page. Submit your HTML and JavaScript."
            },
            "quiz": [
                {"question": "What does event.preventDefault() do when called inside a form's submit handler?", "options": ["It deletes the form", "It stops the browser's default full-page reload on submission", "It validates the form automatically", "It submits the form to a server immediately"], "correct_index": 1, "explanation": "preventDefault() stops the browser's default behavior, which for forms is a full page reload/navigation on submit."},
                {"question": "Why is it risky to rely only on JavaScript for form validation?", "options": ["JavaScript cannot validate forms at all", "JavaScript validation can be bypassed, so server-side and HTML validation are also needed", "JavaScript validation is always slower than HTML", "Forms do not need validation"], "correct_index": 1, "explanation": "Client-side JavaScript can be disabled or bypassed, so it should be combined with HTML validation attributes and, ultimately, server-side checks."},
                {"question": "Which HTML attribute makes a form field mandatory using built-in browser validation?", "options": ["mandatory", "required", "validate", "must-fill"], "correct_index": 1, "explanation": "The required attribute triggers the browser's built-in validation, preventing submission if the field is empty."}
            ],
            "resources": [
                {"label": "MDN: Client-side Form Validation", "url": "https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Bringing Pages to Life with JavaScript",
            "title": "Fetching Data from APIs with JavaScript's Fetch",
            "learning_objective": "By the end of this class, you will be able to fetch data from a public API and display it dynamically on a webpage.",
            "duration_minutes": 30,
            "content_html": """<p>Most real websites do not hardcode their content; they fetch live data from an API and render it dynamically. A weather site pulls current conditions, an e-commerce site pulls product listings, a news site pulls the latest articles — all using the same fetch pattern you will practice today.</p><h2>Making a Fetch Request</h2><p>The fetch function returns a Promise, and using async/await makes the code easy to read top to bottom.</p><pre><code>async function loadCountries() {
  const response = await fetch("https://restcountries.com/v3.1/region/africa");
  const data = await response.json();
  console.log(data);
}
loadCountries();</code></pre><h2>Rendering Fetched Data</h2><p>Once you have the data, you combine it with the DOM skills from Day 7 to display it on the page.</p><pre><code>const list = document.querySelector("#country-list");
data.forEach(country => {
  const item = document.createElement("li");
  item.textContent = country.name.common;
  list.appendChild(item);
});</code></pre><h2>Handling Errors</h2><p>Networks fail and APIs go down, so wrapping fetch calls in try/catch and showing the user a clear error message instead of a blank or broken page is expected in any real project.</p><pre><code>try {
  const response = await fetch(url);
  if (!response.ok) throw new Error("Request failed");
} catch (error) {
  console.error(error);
}</code></pre>""",
            "key_concepts": ["fetch API", "async/await", "Promises", "rendering API data", "error handling"],
            "practical_exercise": {
                "title": "Build a Live Data Display Page",
                "instructions": "Choose a free public API (a country info API, a currency exchange API, or similar). Build a page that fetches data from it on load, displays it as a dynamically generated list on the page, and shows a clear error message if the fetch fails. Submit your HTML, CSS, and JavaScript files."
            },
            "quiz": [
                {"question": "What does JavaScript's fetch function return?", "options": ["A plain string", "A Promise that resolves to the response", "An HTML element", "A CSS stylesheet"], "correct_index": 1, "explanation": "fetch() returns a Promise, which resolves with the Response object once the request completes."},
                {"question": "Why should fetch calls be wrapped in try/catch?", "options": ["It is required by JavaScript syntax", "To handle network failures or API errors gracefully instead of breaking the page", "It makes fetch requests faster", "try/catch is only for form validation"], "correct_index": 1, "explanation": "try/catch lets you catch and handle errors like network failures, showing the user a clear message instead of a broken experience."},
                {"question": "What does the await keyword do inside an async function?", "options": ["It stops the function from running", "It pauses execution until the Promise resolves, then continues with the result", "It deletes the fetched data", "It converts JSON to HTML automatically"], "correct_index": 1, "explanation": "await pauses an async function until the awaited Promise resolves, making asynchronous code read like synchronous code."}
            ],
            "resources": [
                {"label": "MDN: Using Fetch", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Bringing Pages to Life with JavaScript",
            "title": "Building a Multi-Page Static Website and Publishing It Online",
            "learning_objective": "By the end of this class, you will be able to build a linked multi-page website and publish it live using a free static hosting service.",
            "duration_minutes": 35,
            "content_html": """<p>Today you combine everything from the first two weeks into one real, complete, publicly accessible website. Going from "code on my laptop" to "a live link I can send anyone" is a genuinely motivating milestone, and it is the same publishing workflow you will reuse for every project for the rest of this track.</p><h2>Linking Multiple Pages</h2><p>A multi-page site is just several HTML files linked together with anchor tags pointing to each other's filenames.</p><pre><code>&lt;nav&gt;
  &lt;a href="index.html"&gt;Home&lt;/a&gt;
  &lt;a href="about.html"&gt;About&lt;/a&gt;
  &lt;a href="contact.html"&gt;Contact&lt;/a&gt;
&lt;/nav&gt;</code></pre><h2>Publishing with Netlify or Vercel</h2><p>Free static hosting services let you deploy a site in minutes by connecting your GitHub repository, and every future push to that repository automatically updates the live site.</p><pre><code># After connecting your GitHub repo on Netlify or Vercel,
# every "git push" automatically triggers a new live deployment.</code></pre><p>Once deployed, your site gets a real public URL you can put on your resume, LinkedIn, or CV. This single deployment skill — connect repo, push, get a live link — is exactly what you will repeat for the full-stack final project at the end of this track.</p>""",
            "key_concepts": ["multi-page navigation", "relative links", "static site hosting", "Netlify/Vercel deployment", "continuous deployment"],
            "practical_exercise": {
                "title": "Build and Deploy a Three-Page Website",
                "instructions": "Build a three-page personal or portfolio site (Home, About, Contact) with a shared navigation bar linking all pages, styled consistently with CSS. Push it to GitHub, deploy it live using Netlify or Vercel's free tier, and confirm all navigation links work on the live site. Submit the live URL and your GitHub repository link."
            },
            "quiz": [
                {"question": "What is required to link two HTML pages together in the same site?", "options": ["A database connection", "An anchor tag with an href pointing to the other page's filename", "A JavaScript fetch call", "A CSS media query"], "correct_index": 1, "explanation": "An <a href=\"page.html\"> tag creates a clickable link to another page in the same site."},
                {"question": "What happens when you push new code to a GitHub repository connected to Netlify or Vercel?", "options": ["Nothing happens automatically", "It automatically triggers a new deployment, updating the live site", "The old live site is deleted permanently", "It requires manual re-upload every time"], "correct_index": 1, "explanation": "Connected hosting services automatically redeploy the live site whenever new commits are pushed to the linked repository."},
                {"question": "Why is having a live public URL valuable for a portfolio project?", "options": ["It has no real value over local code", "It lets employers or clients actually see and use the working project, not just read code", "Live URLs are required by GitHub", "It makes the code run faster"], "correct_index": 1, "explanation": "A live URL lets anyone experience the actual working project directly, which is far more convincing than a static code listing."}
            ],
            "resources": [
                {"label": "Netlify", "url": "https://www.netlify.com/"},
                {"label": "Vercel", "url": "https://vercel.com/"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Modern Frontend with React",
            "title": "Introduction to Modern JavaScript: ES6+ Features You'll Use Every Day",
            "learning_objective": "By the end of this class, you will be able to use modern JavaScript features including arrow functions, destructuring, template literals, and array methods.",
            "duration_minutes": 25,
            "content_html": """<p>Modern JavaScript code, including virtually every React codebase you will ever encounter on a job, looks quite different from the JavaScript you may have learned in older tutorials. Learning these modern features (often called ES6+) now means React's syntax next class will feel familiar rather than confusing.</p><h2>Arrow Functions and Template Literals</h2><pre><code>const greet = (name) => `Hello, ${name}!`;
console.log(greet("Amaka"));</code></pre><h2>Destructuring</h2><p>Destructuring pulls values out of objects or arrays into named variables in one line, which shows up constantly in React component code.</p><pre><code>const student = { name: "Chidi", age: 21 };
const { name, age } = student;

const [first, second] = ["a", "b"];</code></pre><h2>Array Methods: map, filter, and find</h2><p>These three methods replace most manual for-loops when working with arrays of data, and you will use them constantly for rendering lists in React.</p><pre><code>const prices = [500, 1200, 300];
const withTax = prices.map(p => p * 1.075);
const expensive = prices.filter(p => p > 1000);</code></pre><p>Spend real time getting comfortable with map specifically — it is the exact method React uses to turn an array of data into a list of visual components.</p>""",
            "key_concepts": ["arrow functions", "template literals", "destructuring", "map/filter/find"],
            "practical_exercise": {
                "title": "Practice Modern JavaScript Syntax",
                "instructions": "Given an array of at least five student objects (each with name and score properties), write code using destructuring to extract fields, template literals to build a message per student, .filter() to find students who scored above 70, and .map() to create an array of formatted result strings. Submit your script and its console output."
            },
            "quiz": [
                {"question": "What does the .map() array method return?", "options": ["A single number", "A new array with the results of calling a function on every element", "The original array unchanged", "A boolean value"], "correct_index": 1, "explanation": ".map() creates and returns a new array by applying a given function to each element of the original array."},
                {"question": "What is destructuring used for?", "options": ["Deleting properties from an object", "Extracting values from objects or arrays into named variables in one line", "Converting a string to a number", "Making an array shorter"], "correct_index": 1, "explanation": "Destructuring provides a concise way to unpack values from objects or arrays directly into variables."},
                {"question": "Which syntax below is a template literal?", "options": ["'Hello ' + name", "`Hello ${name}`", "\"Hello\" .concat(name)", "String(name)"], "correct_index": 1, "explanation": "Template literals use backticks and ${} to embed expressions directly inside a string."}
            ],
            "resources": [
                {"label": "MDN: JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Modern Frontend with React",
            "title": "Getting Started with React: Components and JSX",
            "learning_objective": "By the end of this class, you will be able to create a React project and build simple components using JSX.",
            "duration_minutes": 30,
            "content_html": """<p>React is the most widely used JavaScript framework in the industry, and it changes how you think about building pages: instead of manually creating and updating DOM elements like Day 7, you describe what the UI should look like for a given set of data, and React handles updating the actual page for you.</p><h2>Creating a React Project</h2><pre><code>npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev</code></pre><h2>Components and JSX</h2><p>A React app is built from <strong>components</strong> — reusable, self-contained pieces of UI written in <strong>JSX</strong>, a syntax that lets you write HTML-like markup directly inside JavaScript.</p><pre><code>function ProfileCard() {
  return (
    &lt;div className="card"&gt;
      &lt;h2&gt;Amaka Johnson&lt;/h2&gt;
      &lt;p&gt;Computer Science, Year 3&lt;/p&gt;
    &lt;/div&gt;
  );
}

export default ProfileCard;</code></pre><p>Notice className instead of class — JSX is JavaScript under the hood, and class is a reserved word in JavaScript, so React uses className instead. Components can be nested inside each other just like HTML tags, which is how entire React applications are built up from small, reusable pieces.</p>""",
            "key_concepts": ["React components", "JSX syntax", "Vite project setup", "className"],
            "practical_exercise": {
                "title": "Build Your First React Components",
                "instructions": "Create a new React project with Vite. Build three separate components: a Header, a ProfileCard showing a name and bio, and a Footer, each in its own file. Import and render all three inside your main App component. Submit your project's src folder files."
            },
            "quiz": [
                {"question": "What is JSX?", "options": ["A separate programming language from JavaScript", "A syntax extension that lets you write HTML-like markup inside JavaScript", "A CSS framework", "A database query language"], "correct_index": 1, "explanation": "JSX lets developers write HTML-like syntax directly within JavaScript code, which React then converts into actual DOM elements."},
                {"question": "Why does React use className instead of class in JSX?", "options": ["className loads faster", "class is a reserved word in JavaScript, so className is used instead", "React does not support styling", "className is required by CSS"], "correct_index": 1, "explanation": "Since JSX compiles to JavaScript and class is a reserved keyword there, React uses className for the HTML class attribute."},
                {"question": "What is a React component?", "options": ["A CSS file", "A reusable, self-contained piece of UI, often written as a function returning JSX", "A type of database table", "An HTML attribute"], "correct_index": 1, "explanation": "Components are the building blocks of a React app — reusable functions (or classes) that return UI described in JSX."}
            ],
            "resources": [
                {"label": "React Documentation", "url": "https://react.dev/"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Modern Frontend with React",
            "title": "Managing State and Props in React Applications",
            "learning_objective": "By the end of this class, you will be able to use React state to make components interactive and pass data between components using props.",
            "duration_minutes": 30,
            "content_html": """<p>Static components that never change are only half of React's power. Real applications need to respond to user actions — a counter increasing, a like button toggling, a cart updating — and this is exactly what React's state system is built for.</p><h2>useState for Interactive Components</h2><p>The useState hook gives a component its own piece of memory that, when updated, automatically triggers React to re-render the component with the new value.</p><pre><code>import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return (
    &lt;button onClick={() =&gt; setCount(count + 1)}&gt;
      Clicked {count} times
    &lt;/button&gt;
  );
}</code></pre><h2>Passing Data with Props</h2><p>Props let a parent component pass data down into a child component, similar to function arguments.</p><pre><code>function ProfileCard({ name, bio }) {
  return (
    &lt;div&gt;
      &lt;h2&gt;{name}&lt;/h2&gt;
      &lt;p&gt;{bio}&lt;/p&gt;
    &lt;/div&gt;
  );
}

&lt;ProfileCard name="Amaka" bio="Loves React" /&gt;</code></pre><p>The core rule to internalize: state belongs to the component that owns it and can change over time, while props flow one-way from parent to child and cannot be changed by the child itself.</p>""",
            "key_concepts": ["useState hook", "props", "component re-rendering", "one-way data flow"],
            "practical_exercise": {
                "title": "Build a Like Button Component",
                "instructions": "Build a LikeButton component using useState that tracks a like count starting at 0, incrementing by 1 on each click. Then build a parent component that renders three LikeButton instances, each receiving a different starting label via props (e.g. 'Post 1', 'Post 2', 'Post 3'). Submit your component files."
            },
            "quiz": [
                {"question": "What does the useState hook provide to a React component?", "options": ["A way to connect to a database", "A piece of state and a function to update it, triggering a re-render on change", "A way to style the component", "A method to delete the component"], "correct_index": 1, "explanation": "useState returns a state value and a setter function; calling the setter updates the state and triggers React to re-render."},
                {"question": "How does data typically flow between a parent and child component in React?", "options": ["Only from child to parent", "From parent to child via props, in one direction", "Data cannot be shared between components", "Only through a global database"], "correct_index": 1, "explanation": "Props flow one-way from parent components down to child components; children cannot directly modify their parent's data."},
                {"question": "What triggers a React component to re-render?", "options": ["Refreshing the browser only", "A change in its state or the props it receives", "Writing new CSS", "Restarting the development server"], "correct_index": 1, "explanation": "React automatically re-renders a component whenever its internal state changes or it receives new props."}
            ],
            "resources": [
                {"label": "React Documentation: State", "url": "https://react.dev/learn/state-a-components-memory"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Modern Frontend with React",
            "title": "Handling Forms, Events, and Lists in React",
            "learning_objective": "By the end of this class, you will be able to build a controlled form and render dynamic lists of data in React.",
            "duration_minutes": 30,
            "content_html": """<p>Nearly every real application needs to take input from a user and display a list of items — a search bar, a comment form, a product listing. React has specific patterns for both that differ from the plain JavaScript approach you used in week two, and getting comfortable with them is essential before building anything real.</p><h2>Controlled Form Inputs</h2><p>In React, an input's value is tied directly to state, making the component the "single source of truth" for what the input contains.</p><pre><code>function SearchBox() {
  const [query, setQuery] = useState("");
  return (
    &lt;input
      value={query}
      onChange={(e) =&gt; setQuery(e.target.value)}
      placeholder="Search..."
    /&gt;
  );
}</code></pre><h2>Rendering Lists with map and key</h2><p>Just like Day 11's array methods, .map() is how you turn an array of data into a list of JSX elements — but React additionally requires a unique key prop on each item.</p><pre><code>const students = ["Amaka", "Chidi", "Fatima"];

&lt;ul&gt;
  {students.map((name, index) =&gt; (
    &lt;li key={index}&gt;{name}&lt;/li&gt;
  ))}
&lt;/ul&gt;</code></pre><p>The key prop helps React efficiently track which list items changed, were added, or were removed — skipping it causes subtle bugs that are easy to miss until a list starts behaving strangely.</p>""",
            "key_concepts": ["controlled inputs", "onChange handler", "rendering lists", "key prop"],
            "practical_exercise": {
                "title": "Build a Filterable Student List",
                "instructions": "Build a React component with a controlled search input and a hardcoded array of at least eight student names. As the user types in the search box, filter and display only the names that match what has been typed so far, using .filter() and .map() with proper key props. Submit your component file."
            },
            "quiz": [
                {"question": "In a React controlled input, what determines the input's displayed value?", "options": ["The browser's default behavior", "A state variable that the component controls directly", "A CSS rule", "It cannot be controlled by React"], "correct_index": 1, "explanation": "A controlled input's value is tied to a state variable, making React the single source of truth for what is displayed."},
                {"question": "Why does React require a unique key prop when rendering a list with .map()?", "options": ["It is only for styling purposes", "It helps React efficiently track which items changed, were added, or were removed", "Keys are required by JavaScript syntax generally", "It prevents the list from being empty"], "correct_index": 1, "explanation": "The key prop gives React a stable identity for each list item, allowing efficient updates and preventing rendering bugs."},
                {"question": "What event handler is typically used to update state as a user types into an input?", "options": ["onClick", "onChange", "onSubmit", "onLoad"], "correct_index": 1, "explanation": "onChange fires whenever an input's value changes, making it the standard way to keep state in sync with user typing."}
            ],
            "resources": [
                {"label": "React Documentation: Lists and Keys", "url": "https://react.dev/learn/rendering-lists"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Modern Frontend with React",
            "title": "Routing Between Pages in a React App",
            "learning_objective": "By the end of this class, you will be able to set up multi-page navigation in a React application using React Router.",
            "duration_minutes": 25,
            "content_html": """<p>A React app is technically a single HTML page, so it needs a special tool to simulate the multi-page navigation you built with plain links back on Day 10. React Router is the standard library for this, and virtually every real-world React application uses it or something like it.</p><h2>Setting Up Routes</h2><pre><code>npm install react-router-dom</code></pre><pre><code>import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    &lt;BrowserRouter&gt;
      &lt;Routes&gt;
        &lt;Route path="/" element={&lt;Home /&gt;} /&gt;
        &lt;Route path="/about" element={&lt;About /&gt;} /&gt;
        &lt;Route path="/contact" element={&lt;Contact /&gt;} /&gt;
      &lt;/Routes&gt;
    &lt;/BrowserRouter&gt;
  );
}</code></pre><h2>Navigating Without a Full Reload</h2><p>Instead of regular anchor tags, React Router provides a Link component that changes the page shown without a full browser reload, keeping the app fast and preserving any global state.</p><pre><code>import { Link } from "react-router-dom";

&lt;nav&gt;
  &lt;Link to="/"&gt;Home&lt;/Link&gt;
  &lt;Link to="/about"&gt;About&lt;/Link&gt;
&lt;/nav&gt;</code></pre><p>This routing pattern is exactly what you will use to build the multiple pages or views required in your final project at the end of this track.</p>""",
            "key_concepts": ["React Router", "BrowserRouter", "Routes and Route", "Link component"],
            "practical_exercise": {
                "title": "Build a Multi-Page React App with Routing",
                "instructions": "Install react-router-dom and build a React app with three routed pages (Home, About, Projects), each as its own component, connected by a shared navigation bar using Link components. Confirm navigation works without a full page reload. Submit your project files."
            },
            "quiz": [
                {"question": "Why does a React app need React Router instead of using regular multi-page HTML links?", "options": ["React apps cannot have more than one page", "A React app is technically one HTML page, so a library is needed to simulate multi-page navigation", "React Router is required by JavaScript syntax", "Regular links work fine in React and Router is optional decoration"], "correct_index": 1, "explanation": "Since a React app runs as a single-page application, React Router provides the mechanism to show different views for different URLs without full reloads."},
                {"question": "What does the React Router Link component do differently from a regular HTML anchor tag?", "options": ["It cannot navigate to other pages at all", "It changes the displayed route without triggering a full browser page reload", "It only works with external websites", "It requires a database connection"], "correct_index": 1, "explanation": "Link updates the URL and displayed component without a full page reload, keeping the single-page app fast and preserving state."},
                {"question": "Which component wraps a React app to enable routing?", "options": ["<Routes>", "<BrowserRouter>", "<Link>", "<Route>"], "correct_index": 1, "explanation": "<BrowserRouter> is the top-level component that enables routing functionality throughout the app."}
            ],
            "resources": [
                {"label": "React Router Documentation", "url": "https://reactrouter.com/"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Full-Stack Development",
            "title": "Connecting a React Frontend to a Real API",
            "learning_objective": "By the end of this class, you will be able to fetch and display data from an external API inside a React component using useEffect.",
            "duration_minutes": 30,
            "content_html": """<p>Day 9 taught you to fetch data with plain JavaScript. In React, fetching data correctly requires one more concept: the useEffect hook, which controls when side effects like network requests happen relative to a component rendering. Getting this pattern right is one of the most common sources of bugs for React beginners.</p><h2>Fetching Data with useEffect</h2><pre><code>import { useState, useEffect } from "react";

function CountryList() {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://restcountries.com/v3.1/region/africa")
      .then(res => res.json())
      .then(data => {
        setCountries(data);
        setLoading(false);
      });
  }, []);

  if (loading) return &lt;p&gt;Loading...&lt;/p&gt;;

  return (
    &lt;ul&gt;
      {countries.map(c =&gt; &lt;li key={c.cca3}&gt;{c.name.common}&lt;/li&gt;)}
    &lt;/ul&gt;
  );
}</code></pre><h2>Why the Empty Dependency Array Matters</h2><p>The empty array [] as the second argument to useEffect tells React to run this effect only once, when the component first mounts, rather than on every re-render — forgetting it is one of the most common causes of infinite fetch loops beginners run into.</p>""",
            "key_concepts": ["useEffect hook", "dependency array", "loading state", "fetching in React"],
            "practical_exercise": {
                "title": "Build a React Component That Fetches Real Data",
                "instructions": "Build a React component that fetches data from any public API on mount using useEffect, shows a loading message while the request is in progress, and renders the results as a list once loaded. Submit your component file."
            },
            "quiz": [
                {"question": "What is the purpose of the useEffect hook in React?", "options": ["To style components", "To run side effects, like data fetching, in response to rendering or state changes", "To create new components", "To delete state variables"], "correct_index": 1, "explanation": "useEffect handles side effects such as API calls, subscriptions, or manual DOM changes, tied to a component's lifecycle."},
                {"question": "What does passing an empty array [] as useEffect's second argument do?", "options": ["It runs the effect on every render", "It runs the effect only once, when the component first mounts", "It disables the effect entirely", "It causes an error"], "correct_index": 1, "explanation": "An empty dependency array tells React to run the effect only once after the initial render, not on subsequent re-renders."},
                {"question": "Why is showing a loading state important when fetching data in a component?", "options": ["It is purely decorative and has no functional purpose", "Data fetching is asynchronous, so the UI needs to show something meaningful while waiting for the response", "Loading states are required by JavaScript syntax", "It prevents the fetch from happening"], "correct_index": 1, "explanation": "Since network requests take time, a loading state gives users clear feedback instead of a blank or broken-looking screen while data is being fetched."}
            ],
            "resources": [
                {"label": "React Documentation: useEffect", "url": "https://react.dev/reference/react/useEffect"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Full-Stack Development",
            "title": "Styling React Apps with Component Libraries and CSS Frameworks",
            "learning_objective": "By the end of this class, you will be able to style a React application efficiently using a utility-first CSS framework.",
            "duration_minutes": 25,
            "content_html": """<p>Writing custom CSS for every single component works fine for small pages, but it becomes slow and inconsistent as an application grows. Utility-first CSS frameworks like Tailwind CSS solve this by providing small, reusable classes that handle spacing, color, and layout directly in your JSX, which is why Tailwind has become extremely common in modern React job listings.</p><h2>Utility-First Styling with Tailwind</h2><pre><code>&lt;div className="flex items-center justify-between p-4 bg-white shadow rounded-lg"&gt;
  &lt;h2 className="text-xl font-bold text-gray-800"&gt;Amaka Johnson&lt;/h2&gt;
  &lt;button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"&gt;
    Follow
  &lt;/button&gt;
&lt;/div&gt;</code></pre><h2>Why Teams Choose This Approach</h2><p>Instead of switching between a JSX file and a separate CSS file, styling happens right where the markup is, which speeds up development and keeps styles from drifting out of sync with the components that use them. Component libraries like Material UI or Chakra UI take this further by providing entire pre-built, styled components (buttons, modals, forms) so you do not have to build every UI piece from scratch, which is especially useful for building functional prototypes quickly.</p>""",
            "key_concepts": ["Tailwind CSS", "utility-first CSS", "component libraries", "rapid UI development"],
            "practical_exercise": {
                "title": "Restyle a Component with Tailwind CSS",
                "instructions": "Install Tailwind CSS in your React project (or use the Tailwind CDN play script for quick practice), and restyle one of your earlier components (ProfileCard or LikeButton) using only Tailwind utility classes instead of a separate CSS file. Submit your restyled component and a screenshot of the result."
            },
            "quiz": [
                {"question": "What is the core idea behind a utility-first CSS framework like Tailwind?", "options": ["Writing one giant CSS file for the whole site", "Using small, reusable classes applied directly in markup to handle styling", "Avoiding CSS entirely", "Only styling with inline JavaScript"], "correct_index": 1, "explanation": "Utility-first frameworks provide small, single-purpose classes (like p-4 or text-xl) applied directly to elements instead of writing custom CSS rules."},
                {"question": "What is a benefit of styling directly in JSX with utility classes?", "options": ["It removes the need for HTML entirely", "Styles stay closely tied to the markup, reducing drift between JSX and separate CSS files", "It automatically creates a database", "It disables responsive design"], "correct_index": 1, "explanation": "Keeping styles inline with markup avoids the common problem of CSS files becoming out of sync with the components they style."},
                {"question": "What do component libraries like Material UI or Chakra UI provide?", "options": ["Only color palettes with no components", "Pre-built, already-styled UI components like buttons and modals", "A replacement for JavaScript", "Database connection tools"], "correct_index": 1, "explanation": "Component libraries offer ready-made, styled UI building blocks, speeding up development compared to building every element from scratch."}
            ],
            "resources": [
                {"label": "Tailwind CSS Documentation", "url": "https://tailwindcss.com/docs"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Full-Stack Development",
            "title": "Introduction to Backend Development with Node.js and Express",
            "learning_objective": "By the end of this class, you will be able to build and run a simple backend server using Node.js and Express.",
            "duration_minutes": 30,
            "content_html": """<p>Everything you have built so far runs entirely in the browser. But real applications need a backend: server-side code that can securely store data, enforce business rules, and serve information to many different users. Node.js lets you write that backend in JavaScript, the same language you already know from the frontend, and Express is the standard framework for building it.</p><h2>Setting Up a Basic Server</h2><pre><code>npm init -y
npm install express</code></pre><pre><code>const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Welcome to my API");
});

app.get("/api/students", (req, res) => {
  res.json([{ name: "Amaka" }, { name: "Chidi" }]);
});

app.listen(3000, () => console.log("Server running on port 3000"));</code></pre><h2>Understanding Routes</h2><p>Each app.get() defines a <strong>route</strong>: a specific URL path plus a function that runs when a request hits it. This is the exact same request-response cycle from Day 1, except now you are the one writing the server side of it, which is a genuine milestone in becoming a full-stack developer.</p>""",
            "key_concepts": ["Node.js", "Express framework", "routes", "request/response objects"],
            "practical_exercise": {
                "title": "Build Your First Express API",
                "instructions": "Set up a new Node.js project, install Express, and build a server with at least three GET routes: one returning a welcome message, and two returning JSON data of your choice (a list of students, products, or similar). Run the server locally and test each route in your browser. Submit your server.js file and screenshots of each route's response."
            },
            "quiz": [
                {"question": "What does Node.js allow you to do?", "options": ["Run JavaScript in the browser only", "Run JavaScript outside the browser, on a server", "Replace HTML entirely", "Write only CSS code"], "correct_index": 1, "explanation": "Node.js is a JavaScript runtime that lets you execute JavaScript code on a server, outside of a browser environment."},
                {"question": "In Express, what does app.get('/api/students', callback) define?", "options": ["A CSS style rule", "A route that responds to GET requests at the /api/students path", "A database table", "A React component"], "correct_index": 1, "explanation": "app.get() defines a route: a URL path paired with a function that handles GET requests to that path."},
                {"question": "What does res.json() do in an Express route handler?", "options": ["Deletes the response", "Sends a JSON-formatted response back to the client", "Converts JSON into HTML", "Starts the server"], "correct_index": 1, "explanation": "res.json() sends data back to the client formatted as JSON, which is the standard format for API responses."}
            ],
            "resources": [
                {"label": "Express Documentation", "url": "https://expressjs.com/"},
                {"label": "Node.js Documentation", "url": "https://nodejs.org/en/docs"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Full-Stack Development",
            "title": "Building a REST API with Express and a Database",
            "learning_objective": "By the end of this class, you will be able to build a REST API with Express that reads and writes data to a real database.",
            "duration_minutes": 35,
            "content_html": """<p>Yesterday's API returned hardcoded data. A real backend stores and retrieves data from a database, so it persists between requests and server restarts. Today you connect Express to a real database and build the four operations every data-driven application needs: create, read, update, and delete, known together as CRUD.</p><h2>Connecting to a Database</h2><p>MongoDB (with Mongoose) and PostgreSQL are both extremely common choices. Here is a simple example with MongoDB.</p><pre><code>const mongoose = require("mongoose");
mongoose.connect("mongodb://localhost:27017/mydb");

const Student = mongoose.model("Student", {
  name: String,
  score: Number
});</code></pre><h2>Building CRUD Routes</h2><pre><code>app.get("/api/students", async (req, res) => {
  const students = await Student.find();
  res.json(students);
});

app.post("/api/students", async (req, res) => {
  const student = new Student(req.body);
  await student.save();
  res.status(201).json(student);
});</code></pre><h2>Reading the Request Body</h2><p>Notice req.body in the POST route — this requires app.use(express.json()) middleware so Express can parse incoming JSON data sent by the client. Every REST API you build from here forward follows this same pattern: GET to read, POST to create, PUT/PATCH to update, DELETE to remove.</p>""",
            "key_concepts": ["REST API", "CRUD operations", "database connection", "req.body", "Express middleware"],
            "practical_exercise": {
                "title": "Build a Full CRUD API",
                "instructions": "Using Express and a database of your choice (MongoDB, PostgreSQL, or even a simple JSON file for practice), build a REST API for a 'tasks' resource with GET (list all), POST (create), PUT (update), and DELETE routes. Test each route with a tool like Postman or curl. Submit your server code and screenshots of each route working."
            },
            "quiz": [
                {"question": "What does CRUD stand for?", "options": ["Create, Read, Update, Delete", "Connect, Render, Upload, Deploy", "Code, Run, Undo, Debug", "Copy, Replace, Use, Discard"], "correct_index": 0, "explanation": "CRUD stands for Create, Read, Update, Delete — the four basic operations any data-driven application performs on stored data."},
                {"question": "Why is app.use(express.json()) needed for a POST route that uses req.body?", "options": ["It is not actually needed", "It allows Express to parse incoming JSON data sent in the request body", "It connects to the database", "It handles routing"], "correct_index": 1, "explanation": "This middleware parses incoming JSON payloads so that req.body contains the parsed data, rather than being undefined."},
                {"question": "Which HTTP method is conventionally used to create a new resource in a REST API?", "options": ["GET", "POST", "DELETE", "OPTIONS"], "correct_index": 1, "explanation": "POST is the standard HTTP method used to create a new resource on the server."}
            ],
            "resources": [
                {"label": "Express Documentation", "url": "https://expressjs.com/"},
                {"label": "MongoDB Documentation", "url": "https://www.mongodb.com/docs/"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Full-Stack Development",
            "title": "Connecting Your React Frontend to Your Own Backend API",
            "learning_objective": "By the end of this class, you will be able to connect a React frontend to your own Express backend to create a working full-stack feature.",
            "duration_minutes": 35,
            "content_html": """<p>This is the moment the frontend and backend halves of this track finally meet. Instead of fetching from a public API like Day 16, today your React app talks to the Express server you built on Days 18 and 19 — the same pattern powering every real full-stack product you have ever used.</p><h2>Fetching from Your Own API</h2><pre><code>useEffect(() => {
  fetch("http://localhost:3000/api/tasks")
    .then(res => res.json())
    .then(data => setTasks(data));
}, []);</code></pre><h2>Sending Data to Your API</h2><pre><code>async function addTask(title) {
  const response = await fetch("http://localhost:3000/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });
  const newTask = await response.json();
  setTasks([...tasks, newTask]);
}</code></pre><h2>Dealing with CORS</h2><p>Running your frontend and backend on different ports during development often triggers a CORS (Cross-Origin Resource Sharing) error, which the browser throws as a security measure. Installing and enabling the cors package on your Express server (app.use(cors())) fixes this, and it is one of the most common early full-stack bugs you will encounter and now know how to solve.</p>""",
            "key_concepts": ["full-stack integration", "fetch to local API", "CORS", "frontend-backend communication"],
            "practical_exercise": {
                "title": "Connect Your React App to Your Express API",
                "instructions": "Run your Day 19 Express API and your React app at the same time. Update your React app to fetch the list of tasks from your own API on load, and add a form that POSTs a new task to your API and updates the displayed list. Fix any CORS errors you encounter. Submit both codebases and a screenshot of the working connected app."
            },
            "quiz": [
                {"question": "What is a CORS error typically caused by?", "options": ["A missing database connection", "The browser blocking requests between different origins (like different ports) as a security measure", "A syntax error in JSX", "A missing CSS file"], "correct_index": 1, "explanation": "CORS errors occur when the browser blocks a request between different origins (protocol, domain, or port) unless the server explicitly allows it."},
                {"question": "How is a CORS issue typically fixed on an Express server?", "options": ["By deleting the frontend code", "By installing and enabling the cors middleware package", "By disabling JavaScript in the browser", "CORS cannot be fixed"], "correct_index": 1, "explanation": "Adding the cors middleware to an Express server allows it to explicitly permit cross-origin requests from the frontend."},
                {"question": "What HTTP header must be set when sending JSON data in a POST request body?", "options": ["Accept-Language", "Content-Type: application/json", "User-Agent", "Cache-Control"], "correct_index": 1, "explanation": "Setting Content-Type: application/json tells the server the request body is JSON so it can be parsed correctly."}
            ],
            "resources": [
                {"label": "MDN: CORS", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "User Authentication: Sessions, Tokens, and Password Security",
            "learning_objective": "By the end of this class, you will be able to explain how password hashing and JWT authentication work and implement a basic login flow.",
            "duration_minutes": 30,
            "content_html": """<p>Almost every real application needs to know who is using it, whether to show personalized content, protect private data, or restrict certain actions. Authentication is also a security-sensitive area where mistakes are common and costly, so understanding the fundamentals properly matters far more than memorizing one library's syntax.</p><h2>Never Store Plain Text Passwords</h2><p>Passwords must always be hashed before storage, using a library like bcrypt, so that even if a database is breached, the actual passwords are not exposed.</p><pre><code>const bcrypt = require("bcrypt");
const hashed = await bcrypt.hash(password, 10);
const isValid = await bcrypt.compare(enteredPassword, hashed);</code></pre><h2>Tokens with JWT</h2><p>After a successful login, the server issues a JSON Web Token (JWT) that the client stores and sends with future requests to prove who they are, avoiding the need to log in again on every request.</p><pre><code>const jwt = require("jsonwebtoken");
const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: "1h" });</code></pre><p>On protected routes, the server verifies this token before allowing access. This pattern — hash on signup, verify on login, token on every subsequent request — is the standard authentication flow you will see in almost every professional web application.</p>""",
            "key_concepts": ["password hashing", "bcrypt", "JWT authentication", "protected routes"],
            "practical_exercise": {
                "title": "Build a Basic Signup and Login Flow",
                "instructions": "Add signup and login routes to your Express API. On signup, hash the password with bcrypt before saving the user. On login, compare the entered password against the stored hash, and if valid, issue a JWT. Build one protected route that only responds successfully if a valid token is provided. Submit your authentication code."
            },
            "quiz": [
                {"question": "Why should passwords never be stored as plain text in a database?", "options": ["Plain text passwords take up too much storage space", "If the database is breached, plain text passwords expose users' actual passwords directly", "Databases cannot store text", "It is only a stylistic preference"], "correct_index": 1, "explanation": "Storing plain text passwords means a database breach immediately exposes every user's real password, which hashing prevents."},
                {"question": "What is the purpose of a JWT (JSON Web Token) after a user logs in?", "options": ["To store the user's password permanently", "To let the client prove their identity on future requests without logging in again each time", "To hash passwords", "To style the login page"], "correct_index": 1, "explanation": "A JWT is issued after login and sent with future requests, allowing the server to verify identity without requiring repeated logins."},
                {"question": "What does bcrypt.compare() do during login?", "options": ["It hashes a new password for storage", "It checks whether the entered password matches the stored hash", "It deletes the user's account", "It generates a JWT"], "correct_index": 1, "explanation": "bcrypt.compare() verifies an entered password against a stored hash without ever needing to store or reveal the original password."}
            ],
            "resources": [
                {"label": "MDN: Web Security", "url": "https://developer.mozilla.org/en-US/docs/Web/Security"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Handling Errors, Loading States, and Edge Cases Like a Professional",
            "learning_objective": "By the end of this class, you will be able to build a React application that handles loading, error, and empty states gracefully.",
            "duration_minutes": 25,
            "content_html": """<p>A weekend project stops working the moment something unexpected happens: a slow network, a failed request, an empty list. A professional application anticipates these situations and handles them gracefully, which is one of the clearest signals separating beginner code from job-ready code.</p><h2>The Three States Every Data-Driven Component Needs</h2><p>Loading, error, and empty are the three states any component that fetches data should explicitly handle, alongside the normal "data loaded successfully" state.</p><pre><code>function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/tasks")
      .then(res => {
        if (!res.ok) throw new Error("Failed to load tasks");
        return res.json();
      })
      .then(data => setTasks(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return &lt;p&gt;Loading tasks...&lt;/p&gt;;
  if (error) return &lt;p&gt;Error: {error}&lt;/p&gt;;
  if (tasks.length === 0) return &lt;p&gt;No tasks yet. Add one!&lt;/p&gt;;

  return &lt;ul&gt;{tasks.map(t =&gt; &lt;li key={t.id}&gt;{t.title}&lt;/li&gt;)}&lt;/ul&gt;;
}</code></pre><p>Skipping the empty state is a subtle but very common mistake — a blank white space with no explanation leaves users confused about whether something is broken.</p>""",
            "key_concepts": ["loading state", "error state", "empty state", "graceful UX handling"],
            "practical_exercise": {
                "title": "Add Full State Handling to Your Task List",
                "instructions": "Take a component from earlier in this track that fetches data and add explicit handling for all four states: loading, error, empty (no results), and success. Test the error state by temporarily pointing the fetch to an invalid URL, and test the empty state with no data. Submit your updated component and screenshots of all four states."
            },
            "quiz": [
                {"question": "Besides the successful 'data loaded' state, what three other states should a data-fetching component handle?", "options": ["Loading, error, and empty", "Bold, italic, and underline", "Login, signup, and logout", "Create, read, and update"], "correct_index": 0, "explanation": "Loading, error, and empty states, alongside the success state, cover the realistic range of outcomes a data-fetching component can encounter."},
                {"question": "Why is handling the empty state important, even when there is no error?", "options": ["It is not actually important", "Without it, users see a blank space with no explanation of whether something is broken", "Empty states are only relevant for mobile apps", "It replaces the need for error handling"], "correct_index": 1, "explanation": "An unexplained blank UI leaves users uncertain about whether the app is broken, which a clear empty-state message prevents."},
                {"question": "What does the .finally() method do in a Promise chain?", "options": ["It only runs if the promise succeeds", "It runs regardless of whether the promise resolved or rejected", "It cancels the promise", "It only runs if the promise fails"], "correct_index": 1, "explanation": ".finally() runs after a Promise settles, whether it resolved successfully or was rejected, making it ideal for stopping a loading state either way."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Testing Your Web App: Unit and Integration Testing Basics",
            "learning_objective": "By the end of this class, you will be able to write basic unit and component tests for a web application using Jest and React Testing Library.",
            "duration_minutes": 30,
            "content_html": """<p>Manually clicking through your app to check if it still works after every change does not scale, and it is easy to miss a broken feature this way. Automated tests catch regressions instantly, and increasingly, employers expect at least basic testing knowledge even from junior developers.</p><h2>Unit Testing Plain Functions</h2><pre><code>// utils.js
function calculateTotal(prices) {
  return prices.reduce((sum, p) => sum + p, 0);
}

// utils.test.js
test("calculates total correctly", () => {
  expect(calculateTotal([100, 200, 300])).toBe(600);
});</code></pre><h2>Testing React Components</h2><p>React Testing Library lets you test components the way a real user would interact with them, by rendering, finding elements, and simulating clicks.</p><pre><code>import { render, screen, fireEvent } from "@testing-library/react";
import Counter from "./Counter";

test("increments count on button click", () => {
  render(&lt;Counter /&gt;);
  const button = screen.getByRole("button");
  fireEvent.click(button);
  expect(screen.getByText(/Clicked 1 times/)).toBeInTheDocument();
});</code></pre><p>You do not need 100% test coverage for a portfolio project, but having a handful of meaningful tests around your core logic shows real engineering discipline to anyone reviewing your code.</p>""",
            "key_concepts": ["Jest", "React Testing Library", "unit tests", "component testing"],
            "practical_exercise": {
                "title": "Write Tests for Your Components and Functions",
                "instructions": "Write at least two unit tests for a plain utility function and two component tests using React Testing Library for a component with interactive behavior (like your Counter or LikeButton). Run the tests and confirm they pass. Submit your test files and a screenshot of the passing test run."
            },
            "quiz": [
                {"question": "What is a key advantage of automated tests over manually clicking through an app?", "options": ["Manual testing is always more thorough", "Automated tests run quickly and consistently, catching regressions that manual testing might miss", "Automated tests replace the need for writing any code", "There is no real advantage"], "correct_index": 1, "explanation": "Automated tests can be run instantly and repeatedly, reliably catching breakages that manual clicking might miss or take too long to check."},
                {"question": "What does React Testing Library's fireEvent.click() simulate?", "options": ["A server request", "A user clicking on an element in the rendered component", "A CSS style change", "A database write"], "correct_index": 1, "explanation": "fireEvent.click() simulates a real user click event on a rendered component during a test."},
                {"question": "Is 100% test coverage required for a strong portfolio project?", "options": ["Yes, it is strictly required", "No, a handful of meaningful tests around core logic is enough to show engineering discipline", "Tests are irrelevant to portfolio projects", "Only backend code needs tests"], "correct_index": 1, "explanation": "A reasonable set of meaningful tests demonstrates testing discipline without requiring exhaustive, time-consuming full coverage."}
            ],
            "resources": [
                {"label": "React Testing Library Documentation", "url": "https://testing-library.com/docs/react-testing-library/intro/"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Optimizing Web Performance: Load Times, Images, and Bundling",
            "learning_objective": "By the end of this class, you will be able to identify and fix common web performance issues including image size and unnecessary re-renders.",
            "duration_minutes": 25,
            "content_html": """<p>A slow website loses users, especially on the slower or more expensive mobile data connections common across Nigeria. Performance is not just a technical nicety; it directly affects whether people actually use what you build, and it is a real topic employers evaluate in code reviews.</p><h2>Optimizing Images</h2><p>Unoptimized images are one of the single biggest causes of slow page loads. Compressing images, using modern formats like WebP, and specifying width/height to avoid layout shift all make a measurable difference.</p><pre><code>&lt;img src="profile.webp" width="200" height="200" loading="lazy" alt="Profile photo" /&gt;</code></pre><h2>Avoiding Unnecessary Re-renders in React</h2><p>React re-rendering more than necessary can make an app feel sluggish. Using React DevTools' profiler helps spot this, and tools like React.memo prevent a component from re-rendering when its props have not actually changed.</p><pre><code>const ProfileCard = React.memo(function ProfileCard({ name, bio }) {
  return &lt;div&gt;&lt;h2&gt;{name}&lt;/h2&gt;&lt;p&gt;{bio}&lt;/p&gt;&lt;/div&gt;;
});</code></pre><h2>Checking Your Work</h2><p>Chrome DevTools' Lighthouse tab gives a free, immediate performance score and specific, actionable suggestions for any page, and running it on your own projects is a habit worth building now.</p>""",
            "key_concepts": ["image optimization", "lazy loading", "React.memo", "Lighthouse audits"],
            "practical_exercise": {
                "title": "Run and Fix a Lighthouse Performance Audit",
                "instructions": "Run a Lighthouse audit (in Chrome DevTools) on one of your deployed projects from this track, note your performance score and the top three suggestions given. Fix at least two of them (such as compressing an image or adding lazy loading), redeploy, and re-run the audit. Submit both before-and-after Lighthouse scores."
            },
            "quiz": [
                {"question": "Why are unoptimized images a common cause of slow page loads?", "options": ["Images never affect load time", "Large, uncompressed image files take longer to download over the network", "Images are always cached instantly", "Browsers ignore image size"], "correct_index": 1, "explanation": "Large image files take longer to transfer over the network, making them one of the most common causes of slow page loads."},
                {"question": "What does React.memo help prevent?", "options": ["A component from rendering at all", "A component from re-rendering when its props have not actually changed", "API requests from failing", "CSS from loading"], "correct_index": 1, "explanation": "React.memo skips re-rendering a component if its props are unchanged, avoiding unnecessary rendering work."},
                {"question": "What tool in Chrome DevTools gives a free performance score and improvement suggestions for a webpage?", "options": ["The Elements panel", "Lighthouse", "The Console tab alone", "The Sources tab"], "correct_index": 1, "explanation": "Lighthouse audits a page and provides a performance score along with specific, actionable recommendations."}
            ],
            "resources": [
                {"label": "web.dev Performance", "url": "https://web.dev/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Production-Ready Practices",
            "title": "Deploying a Full-Stack Web App to Production (Vercel, Netlify, Render)",
            "learning_objective": "By the end of this class, you will be able to deploy both the frontend and backend of a full-stack application to live, publicly accessible hosts.",
            "duration_minutes": 35,
            "content_html": """<p>Day 10 deployed a static site. A full-stack app has two separate pieces to deploy: the React frontend and the Express backend, and they typically live on different hosting services optimized for each job. This is the exact deployment shape you will use for your final project.</p><h2>Deploying the Frontend</h2><p>Vercel and Netlify are both excellent for React frontends built with Vite, connecting directly to your GitHub repository for automatic deployments.</p><pre><code>npm run build
# Push to GitHub, then connect the repo on Vercel or Netlify</code></pre><h2>Deploying the Backend</h2><p>Render is a popular free option for hosting an Express server, since it supports long-running Node processes, unlike some purely static hosts.</p><pre><code># On Render: create a new Web Service, connect your GitHub repo,
# set the start command to "node server.js", and set your environment
# variables (database URL, JWT secret) in the dashboard.</code></pre><h2>Connecting Them Together</h2><p>Once both are live, update your frontend's fetch calls to point to your backend's live Render URL instead of localhost, and set environment variables rather than hardcoding secrets like database URLs and JWT secrets directly in your code. Testing the full flow on the live URLs, not just locally, is the final step before calling a project done.</p>""",
            "key_concepts": ["frontend deployment", "backend deployment", "Render", "environment variables in production"],
            "practical_exercise": {
                "title": "Deploy Your Full-Stack App Live",
                "instructions": "Deploy your Express backend from Days 18-21 to Render (or a similar host), and deploy your React frontend to Vercel or Netlify, updating your frontend's API calls to use the live backend URL. Set any secrets as environment variables in each platform's dashboard rather than hardcoding them. Submit both live URLs."
            },
            "quiz": [
                {"question": "Why might a full-stack app's frontend and backend be deployed to different hosting services?", "options": ["It is a strict requirement of React", "Frontend hosts like Vercel/Netlify are optimized for static sites, while backend hosts like Render support long-running server processes", "It is impossible to deploy both to the same place", "Backend code cannot be deployed at all"], "correct_index": 1, "explanation": "Static hosts are optimized for serving frontend build files, while services like Render are built to run persistent backend server processes."},
                {"question": "What should you update in your frontend code after deploying your backend to a live URL?", "options": ["Nothing needs to change", "The fetch calls that previously pointed to localhost, to now point to the live backend URL", "The React component names", "The CSS framework"], "correct_index": 1, "explanation": "Frontend fetch calls must be updated to target the live backend URL instead of a local development address for the deployed app to work."},
                {"question": "Where should sensitive values like a JWT secret or database URL be stored in production?", "options": ["Hardcoded directly in the source code", "As environment variables set in the hosting platform's dashboard", "In the page's HTML", "In a public GitHub README"], "correct_index": 1, "explanation": "Environment variables set through the hosting platform keep secrets out of the source code and version control history."}
            ],
            "resources": [
                {"label": "Render", "url": "https://render.com/"},
                {"label": "Vercel", "url": "https://vercel.com/"}
            ]
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Job-Ready Web Development",
            "title": "What Web Developer Interviews Actually Test (Coding Challenges and System Design)",
            "learning_objective": "By the end of this class, you will be able to describe the common stages of a web developer interview and practice a live coding style challenge.",
            "duration_minutes": 25,
            "content_html": """<p>Web developer interviews, whether for a Nigerian startup or a remote international role, generally follow a recognizable pattern: a coding challenge testing core JavaScript and problem-solving, a practical round building or debugging a small feature, and sometimes a system design or architecture discussion for more senior roles.</p><h2>The Coding Challenge Round</h2><p>Expect array and string manipulation problems, and increasingly, small React component challenges like "build a component that filters a list as the user types" — exactly what you practiced on Day 14.</p><pre><code>function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return [...duplicates];
}</code></pre><h2>The Practical / Take-Home Round</h2><p>Many companies now give a small take-home project instead of (or in addition to) a whiteboard challenge, asking you to build a small feature with a live API, which is exactly the kind of task this entire track has been preparing you for. Explaining your reasoning out loud as you code, not just producing a correct answer silently, is often what interviewers are actually evaluating.</p>""",
            "key_concepts": ["technical interview stages", "coding challenges", "take-home projects", "explaining reasoning aloud"],
            "practical_exercise": {
                "title": "Complete a Timed Coding Challenge",
                "instructions": "Set a 20-minute timer. Write a function that takes an array of product objects (each with name and price) and returns only the products under a given price, sorted from cheapest to most expensive, without using any external libraries. Write a short paragraph explaining your approach as if speaking to an interviewer. Submit your code and explanation."
            },
            "quiz": [
                {"question": "What is a common format companies use instead of or alongside a whiteboard coding challenge?", "options": ["A handwriting test", "A small take-home project involving a real feature or API", "An unrelated personality quiz", "A typing speed test"], "correct_index": 1, "explanation": "Take-home projects, asking candidates to build a small real feature, have become a common and practical alternative to pure whiteboard challenges."},
                {"question": "Why is explaining your reasoning out loud important during a coding interview?", "options": ["It is not actually important", "Interviewers often care as much about your problem-solving process as the final correct answer", "It replaces the need to write working code", "It is only relevant for senior roles"], "correct_index": 1, "explanation": "Interviewers frequently assess how a candidate thinks through a problem, which explaining aloud makes visible, not just whether the final answer is correct."},
                {"question": "What kind of coding challenge has become increasingly common for frontend roles specifically?", "options": ["Only pure algorithm problems with no UI", "Small React component challenges, like building a filterable list", "Database schema design only", "Networking protocol questions"], "correct_index": 1, "explanation": "Frontend-focused interviews increasingly include small practical component-building challenges relevant to the actual job, like filtering or rendering lists."}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Job-Ready Web Development",
            "title": "Web Accessibility and SEO Fundamentals Employers Expect You to Know",
            "learning_objective": "By the end of this class, you will be able to audit and improve a webpage's accessibility and basic SEO.",
            "duration_minutes": 25,
            "content_html": """<p>Accessibility (making a site usable by people with disabilities) and SEO (making a site discoverable by search engines) are often treated as afterthoughts by beginners, but experienced developers and hiring managers view both as basic professional competence, not extra features.</p><h2>Basic Accessibility Practices</h2><p>Every image needs meaningful alt text, every form input needs an associated label, and interactive elements should be reachable and operable using only a keyboard.</p><pre><code>&lt;img src="chart.png" alt="Bar chart showing sales growth from January to June" /&gt;
&lt;label for="email"&gt;Email&lt;/label&gt;
&lt;input id="email" type="email" /&gt;</code></pre><h2>Basic SEO Practices</h2><p>Search engines rely on meta tags, a single clear h1 per page, and semantic structure (from Day 3) to understand and rank a page's content.</p><pre><code>&lt;head&gt;
  &lt;title&gt;Campus Marketplace - Buy and Sell With Fellow Students&lt;/title&gt;
  &lt;meta name="description" content="Buy and sell textbooks, gadgets, and more with students on your campus." /&gt;
&lt;/head&gt;</code></pre><p>Chrome's Lighthouse tab, used already for performance, also scores accessibility and SEO with specific fixes listed — running it on your final project before submission is a quick, high-value habit.</p>""",
            "key_concepts": ["web accessibility", "alt text", "form labels", "SEO meta tags", "Lighthouse audits"],
            "practical_exercise": {
                "title": "Audit and Fix Accessibility and SEO Issues",
                "instructions": "Run a Lighthouse accessibility and SEO audit on one of your deployed projects. List the top three issues found in each category, fix at least two accessibility issues (missing alt text, missing labels) and two SEO issues (missing title, missing meta description), and re-run the audit. Submit before-and-after scores."
            },
            "quiz": [
                {"question": "Why does an image need meaningful alt text?", "options": ["It is purely decorative and optional", "Screen readers use alt text to describe images to visually impaired users, and it also helps SEO", "Alt text makes images load faster", "It is only needed for logos"], "correct_index": 1, "explanation": "Alt text allows screen readers to describe an image's content to users who cannot see it, and search engines also use it to understand image content."},
                {"question": "What is the purpose of a meta description tag?", "options": ["It styles the page", "It provides a summary of the page's content that search engines often display in search results", "It runs JavaScript", "It defines the page's color scheme"], "correct_index": 1, "explanation": "The meta description gives search engines (and often users in search results) a concise summary of what the page is about."},
                {"question": "Which tool used earlier in this track also scores accessibility and SEO, not just performance?", "options": ["React DevTools", "Lighthouse", "npm", "Git"], "correct_index": 1, "explanation": "Chrome's Lighthouse tool audits performance, accessibility, SEO, and best practices together, providing actionable suggestions for each."}
            ],
            "resources": [
                {"label": "MDN: Accessibility", "url": "https://developer.mozilla.org/en-US/docs/Web/Accessibility"},
                {"label": "Google Search Central SEO Docs", "url": "https://developers.google.com/search/docs"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Job-Ready Web Development",
            "title": "Version Control Workflows: Branches, Pull Requests, and Code Review",
            "learning_objective": "By the end of this class, you will be able to use Git branches and open a pull request to simulate a real team collaboration workflow.",
            "duration_minutes": 25,
            "content_html": """<p>Day 2 covered basic Git commands, but real teams rarely commit directly to their main branch. They use branches and pull requests so changes can be reviewed before merging, catching bugs and sharing knowledge across the team before code reaches production.</p><h2>Working with Branches</h2><pre><code>git checkout -b feature/add-search-bar
# make your changes
git add .
git commit -m "Add search bar to homepage"
git push -u origin feature/add-search-bar</code></pre><h2>Opening a Pull Request</h2><p>On GitHub, a pull request (PR) proposes merging your branch into main, showing exactly what changed line by line, and lets teammates leave comments before it is approved and merged.</p><pre><code># On GitHub: click "Compare & pull request" after pushing your branch,
# write a clear description of what changed and why, then request review.</code></pre><h2>Why This Workflow Matters</h2><p>Even working solo, practicing this branch-then-PR habit on your own projects prepares you for how virtually every professional engineering team actually operates, and shows up as a positive signal in your GitHub history when employers review it.</p>""",
            "key_concepts": ["Git branches", "pull requests", "code review", "collaborative workflow"],
            "practical_exercise": {
                "title": "Practice a Branch-and-Pull-Request Workflow",
                "instructions": "On one of your existing GitHub repositories, create a new branch, make a small meaningful change (a new feature or a bug fix), push the branch, and open a pull request on GitHub with a clear title and description of the change. Merge it once opened. Submit the link to your pull request."
            },
            "quiz": [
                {"question": "Why do real engineering teams typically avoid committing directly to the main branch?", "options": ["It is technically impossible to do so", "Branches and pull requests allow changes to be reviewed before merging, catching bugs early", "Main branches do not accept any commits ever", "It has no real benefit"], "correct_index": 1, "explanation": "Using branches and pull requests enables review before code reaches the main branch, catching issues and sharing knowledge across the team."},
                {"question": "What does a pull request (PR) show reviewers?", "options": ["Only the final merged code with no history", "Exactly what changed, line by line, compared to the target branch", "The developer's personal information", "Nothing useful for review"], "correct_index": 1, "explanation": "A pull request displays a clear diff of the proposed changes, letting reviewers see exactly what was added, removed, or modified."},
                {"question": "What command creates and switches to a new Git branch in one step?", "options": ["git branch new-branch", "git checkout -b new-branch", "git merge new-branch", "git push new-branch"], "correct_index": 1, "explanation": "git checkout -b new-branch creates a new branch and switches to it immediately in a single command."}
            ],
            "resources": [
                {"label": "GitHub Docs: About Pull Requests", "url": "https://github.com/"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Job-Ready Web Development",
            "title": "Building a Web Developer Portfolio That Gets You Interviews",
            "learning_objective": "By the end of this class, you will be able to build a personal portfolio site and write project descriptions that highlight real technical decisions.",
            "duration_minutes": 25,
            "content_html": """<p>Your portfolio site is often the very first thing a recruiter or client looks at, and it is itself a demonstration of your skills — a portfolio with bad layout or broken links undermines your credibility before anyone even reads your project descriptions.</p><h2>What a Strong Portfolio Includes</h2><p>At minimum: a short, specific bio (not "aspiring developer" but what you actually build and care about), 3-4 real projects with live links and GitHub links, and a way to contact you.</p><h2>Writing Project Descriptions That Matter</h2><p>Avoid vague descriptions like "a website using React." Instead, name the problem solved, the specific technical decisions made, and a challenge overcome, mirroring the framing from Day 27 of the Data Engineering track's portfolio lesson but for web projects specifically. For example: "Built a campus marketplace app with React and Express where students list and search items; implemented debounced search to avoid firing an API call on every keystroke, cutting unnecessary requests by roughly 80%."</p><p>Deploy your portfolio itself using the same skills from Day 10 and Day 25 — a portfolio that is not live online defeats its own purpose.</p>""",
            "key_concepts": ["portfolio site structure", "project storytelling", "technical decision framing", "live portfolio deployment"],
            "practical_exercise": {
                "title": "Build and Deploy Your Portfolio Site",
                "instructions": "Build a personal portfolio site (using plain HTML/CSS or React) with a specific bio, at least three of your projects from this track with live and GitHub links, and a contact method. For each project, write a 2-3 sentence description naming the specific problem solved and one technical decision you made. Deploy it live and submit the URL."
            },
            "quiz": [
                {"question": "What makes a project description on a portfolio stand out to a hiring manager?", "options": ["Listing only the programming languages used", "Naming the specific problem solved and a real technical decision or challenge overcome", "Using as many buzzwords as possible", "Keeping descriptions as short as one word"], "correct_index": 1, "explanation": "Specific, concrete descriptions of problems solved and decisions made demonstrate real engineering judgment far more than vague or generic phrasing."},
                {"question": "Why is it important for a developer's portfolio site itself to be well-built?", "options": ["It has no bearing on how the developer is perceived", "The portfolio itself is a demonstration of the developer's skills, and a poor one undermines credibility", "Portfolios are never actually viewed by employers", "Only the projects listed matter, not the portfolio site itself"], "correct_index": 1, "explanation": "A portfolio site is itself a piece of the developer's work; a poorly built one contradicts any claims of web development skill."},
                {"question": "What should a portfolio bio focus on instead of a generic phrase like 'aspiring developer'?", "options": ["A list of unrelated hobbies only", "What the person actually builds and cares about, made specific and concrete", "The exact number of hours studied", "Nothing, bios are unnecessary"], "correct_index": 1, "explanation": "A specific bio describing real interests and work is far more memorable and credible than a generic, interchangeable phrase."}
            ],
            "resources": [
                {"label": "GitHub Pages", "url": "https://pages.github.com/"}
            ]
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Job-Ready Web Development",
            "title": "Final Project Day: Building and Deploying Your Multi-Page Web App",
            "learning_objective": "By the end of this class, you will be able to plan and begin building your complete multi-page, full-stack web application final project.",
            "duration_minutes": 35,
            "content_html": """<p>Today you start the capstone: a production-style, multi-page web application with a live public URL, built with a real backend API, a database, at least one form that creates or updates data, and proper loading and error handling, exactly as covered across this track's final weeks.</p><h2>How to Approach It</h2><p>Pick an idea you actually care about, since motivation matters over the coming days: a student marketplace, an event booking tool, a local business directory. Sketch your pages and routes first, like Day 15's routing practice, then design your database schema for the data each page needs. Build the backend CRUD routes from Days 18-19 before touching the frontend, so you have real data to work with from the start.</p><h2>What "Done" Looks Like</h2><p>A finished submission has at least three distinct pages connected by React Router, a working form that creates or updates real data through your API, proper loading/error/empty states from Day 22, and a live deployment on Vercel/Netlify plus Render following Day 25's process, with a README explaining your architecture. Today's goal is not a finished app — it is a clear plan, your database schema, and your backend's core routes built and tested, since the remaining classes' practice time will go into frontend, polish, and deployment.</p>""",
            "key_concepts": ["capstone planning", "full-stack execution", "project scoping", "final project kickoff"],
            "practical_exercise": {
                "title": "Start Your Final Project: Build the Full-Stack App",
                "instructions": "This is the literal start of your final project. Choose your app idea, sketch your pages/routes and database schema, set up your Express backend and database, and build and test your core CRUD routes with Postman or curl before writing any frontend code. Submit your architecture sketch, database schema, and working backend routes as the first deliverable toward your final web application project."
            },
            "quiz": [
                {"question": "What should be built first when starting the final project, according to the recommended approach?", "options": ["The React frontend styling", "The backend CRUD routes and database schema, so there is real data to work with", "The portfolio site", "The Lighthouse performance audit"], "correct_index": 1, "explanation": "Building and testing the backend and its data routes first ensures there is real, working data available before frontend development begins."},
                {"question": "What is the minimum number of distinct pages the final project requires?", "options": ["One", "At least three, connected by React Router", "Ten", "There is no page requirement"], "correct_index": 1, "explanation": "The final project brief requires at least three distinct pages or views connected through routing, forming a genuine multi-page application."},
                {"question": "What should today's work realistically focus on completing?", "options": ["The entire finished and deployed application", "A clear plan, database schema, and working backend routes", "Only the portfolio site from Day 29", "Writing unit tests exclusively"], "correct_index": 1, "explanation": "Day 30 is the project kickoff — the realistic goal is a solid plan and a working backend foundation, with frontend and deployment to follow in continued practice."}
            ],
            "resources": []
        }
    ]
}
