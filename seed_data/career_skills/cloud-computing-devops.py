"""Seed data for the Cloud Computing & DevOps 30-Day Skill Class."""

SKILL = {
    "slug": "cloud-computing-devops",
    "name": "Cloud Computing & DevOps",
    "tagline": "Deploy, automate, and monitor real applications on cloud infrastructure the way production teams do.",
    "description": "Cloud computing and DevOps are the skills behind how modern software actually runs in the real world: servers in data centers, automated deployment pipelines, and systems that alert engineers before users notice a problem. This is one of the fastest-growing and highest-paying tech skill areas for a Nigerian graduate, because every serious tech company, bank, and startup now runs on AWS, GCP, or Azure and needs people who can deploy and operate their systems reliably. This track takes you from understanding what a server actually is to deploying a real application on cloud infrastructure with a working CI/CD pipeline and basic monitoring, exactly the kind of hands-on experience DevOps and cloud job postings ask for.",
    "level": "beginner",
    "estimated_hours": 64,
    "course_title": "30-Day Cloud Computing & DevOps Career Track",
    "course_description": "After 30 days you will be able to provision cloud infrastructure, containerize applications with Docker, build automated CI/CD pipelines, and deploy and monitor a live application running in the cloud.",
    "final_project": {
        "title": "Deploy and Operate a Production-Style Cloud Application",
        "description": "Deploy a real application, such as a simple API, a blog platform, or a small web app, onto real cloud infrastructure with a complete, automated operational setup. The project must include a Dockerized application deployed to a cloud provider (AWS, GCP, or Azure) or a platform like Render, a CI/CD pipeline using GitHub Actions that automatically tests and deploys on every push to main, basic monitoring or health-check alerting so you would know if the app went down, and a documented architecture diagram explaining how the pieces fit together. This is the kind of live, operated system that proves to a hiring manager or client you can not just write code, but actually run it reliably in production.",
        "difficulty": "advanced",
        "estimated_hours": 13,
        "skills_demonstrated": ["Docker", "CI/CD pipelines", "cloud deployment", "infrastructure basics", "monitoring and alerting", "Linux/command line", "architecture documentation"],
        "rubric": [
            {"name": "Successful cloud deployment and containerization", "max_points": 30},
            {"name": "Working CI/CD pipeline", "max_points": 25},
            {"name": "Monitoring, health checks, and reliability", "max_points": 25},
            {"name": "Architecture documentation and clarity", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "How Servers and the Cloud Actually Work",
            "title": "What a Server Actually Is and Why the Cloud Replaced Physical Servers",
            "learning_objective": "By the end of this class, you will be able to explain what a server is and why companies moved from owning physical servers to renting cloud infrastructure.",
            "duration_minutes": 20,
            "content_html": """<p>Every app, website, and API you have ever used runs on a server somewhere, a computer that stays on and responds to requests instead of being used directly by one person. Understanding this is the starting point for everything in cloud computing and DevOps, and it is a concept that comes up in nearly every entry-level interview in this field.</p><h2>From Physical Servers to the Cloud</h2><p>Before cloud computing, a company that needed a server had to buy a physical machine, install it in a data center, and maintain it themselves, a slow and expensive process. Cloud providers like AWS, Google Cloud, and Microsoft Azure changed this by letting you rent computing power by the hour or minute, provisioned in minutes instead of weeks.</p><pre><code>Old way:  Buy server -> Ship to data center -> Install -> Configure -> Wait weeks
Cloud way: Click "Launch Instance" -> Server ready in under 5 minutes</code></pre><h2>Why This Matters for Your Career</h2><p>Nigerian fintechs, logistics startups, and banks all run on cloud infrastructure today because it is cheaper to start with and scales instantly when traffic grows. A "Cloud Engineer," "DevOps Engineer," or "Site Reliability Engineer" job is fundamentally about managing this exact shift: provisioning, securing, and operating servers that live in someone else's data center but that your code runs on.</p>""",
            "key_concepts": ["servers", "data centers", "cloud computing", "AWS/GCP/Azure", "infrastructure provisioning"],
            "practical_exercise": {
                "title": "Compare Three Cloud Providers",
                "instructions": "Research AWS, Google Cloud, and Microsoft Azure's free tier offerings, and write a short comparison covering what each gives you for free, any time limits, and which one you plan to use for this track and why. Submit your written comparison, at least 150 words."
            },
            "quiz": [
                {"question": "What is a server, in simple terms?", "options": ["A type of laptop", "A computer that stays on and responds to requests instead of being used directly by one person", "A programming language", "A type of internet cable"], "correct_index": 1, "explanation": "A server is a computer designed to run continuously and respond to requests from other computers, rather than being used interactively like a personal laptop."},
                {"question": "What was a major drawback of owning physical servers before cloud computing?", "options": ["Provisioning a physical server was slow and expensive, often taking weeks", "Physical servers were faster than cloud servers", "Physical servers could not run any software", "There was no drawback at all"], "correct_index": 0, "explanation": "Physical servers required buying hardware, shipping it to a data center, and manual setup, a process that took weeks compared to minutes in the cloud."},
                {"question": "Which of these is a major cloud provider?", "options": ["React Native", "Figma", "Amazon Web Services (AWS)", "MySQL Workbench"], "correct_index": 2, "explanation": "AWS, along with Google Cloud (GCP) and Microsoft Azure, is one of the three dominant cloud infrastructure providers."}
            ],
            "resources": [
                {"label": "AWS Getting Started", "url": "https://aws.amazon.com/getting-started/"},
                {"label": "Google Cloud Documentation", "url": "https://cloud.google.com/docs"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "How Servers and the Cloud Actually Work",
            "title": "Navigating the Linux Command Line You Will Use Every Day",
            "learning_objective": "By the end of this class, you will be able to navigate a Linux filesystem and manage files using core terminal commands.",
            "duration_minutes": 30,
            "content_html": """<p>Almost every cloud server you will ever touch runs Linux, not Windows or macOS, so comfort with the Linux command line is non-negotiable for any cloud or DevOps role. This is not optional knowledge, it is the daily interface for the entire rest of this track.</p><h2>Core Navigation Commands</h2><p>These five commands cover the vast majority of what you will do when first exploring a server.</p><pre><code>pwd                  # print current directory
ls -la               # list all files, including hidden ones, with details
cd /var/www          # change directory
mkdir project        # create a new directory
touch app.py         # create a new empty file</code></pre><h2>Viewing and Editing Files</h2><p>You will frequently need to inspect a file's contents or edit configuration directly on a server.</p><pre><code>cat config.yml        # print a file's contents
nano config.yml       # edit a file in a simple terminal editor
grep "ERROR" app.log  # search a file for a specific string</code></pre><p>Every day for the rest of this track, and every real DevOps job afterward, will involve typing commands like these into a terminal connected to a remote server, so practicing them until they feel automatic now will save you real time later.</p>""",
            "key_concepts": ["Linux filesystem", "terminal navigation", "pwd/ls/cd/mkdir", "cat/nano/grep"],
            "practical_exercise": {
                "title": "Complete a Terminal Navigation Challenge",
                "instructions": "Using your terminal (or a free online Linux sandbox if you do not have Linux locally), create a folder structure with three nested directories, create a text file inside the deepest one containing your name, then use cat to print its contents and grep to search for your name within it. Submit a screenshot of your terminal session showing all commands and their output."
            },
            "quiz": [
                {"question": "What operating system do most cloud servers run?", "options": ["Linux", "Windows", "macOS", "ChromeOS"], "correct_index": 0, "explanation": "The vast majority of cloud servers run Linux due to its stability, security, and low resource overhead."},
                {"question": "Which command lists all files in a directory, including hidden ones, with detailed information?", "options": ["cd", "ls -la", "mkdir", "pwd"], "correct_index": 1, "explanation": "ls -la lists all files (including hidden ones starting with a dot) along with permissions, size, and modification details."},
                {"question": "What does the grep command do?", "options": ["Deletes a file permanently", "Creates a new directory", "Displays the current directory path", "Searches file contents for a specific pattern or string"], "correct_index": 3, "explanation": "grep searches through file contents for lines matching a given pattern, commonly used to find errors in log files."}
            ],
            "resources": [
                {"label": "MDN: Command Line Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "How Servers and the Cloud Actually Work",
            "title": "Understanding IP Addresses, DNS, and How Traffic Reaches a Server",
            "learning_objective": "By the end of this class, you will be able to explain how a domain name resolves to a server's IP address and reaches an application.",
            "duration_minutes": 25,
            "content_html": """<p>When you type a website address into a browser, several invisible steps happen before your request even reaches a server. Understanding this chain, domain name to IP address to server to application, is essential for debugging deployment issues, which you will hit constantly in this field.</p><h2>DNS: Translating Names to Addresses</h2><p>Computers communicate using IP addresses (like 192.0.2.10), not names. DNS (Domain Name System) is the internet's phonebook, translating a human-readable domain like example.com into the actual IP address of the server hosting it.</p><pre><code>You type: example.com
DNS lookup: example.com -> 192.0.2.10
Browser connects to: 192.0.2.10</code></pre><h2>Ports: Reaching the Right Application</h2><p>A single server can run multiple applications, each listening on a different <strong>port</strong>. Port 80 is the default for HTTP, 443 for HTTPS, and custom applications often use ports like 3000, 5000, or 8080 during development.</p><pre><code>example.com:443  -> reaches the HTTPS web server on that machine
example.com:5000 -> reaches a different app running on port 5000</code></pre><p>When you deploy your first app later this week and it does not load, the very first things to check are exactly these: is the DNS pointing to the right server, and is the app actually listening on the expected port.</p>""",
            "key_concepts": ["DNS resolution", "IP addresses", "ports", "HTTP/HTTPS default ports"],
            "practical_exercise": {
                "title": "Trace a Real Domain's DNS Resolution",
                "instructions": "Use an online DNS lookup tool or the terminal command 'nslookup' (or 'dig') to look up the IP address behind three real websites of your choice. Record each domain and the IP address(es) it resolved to, and write one sentence explaining what would happen if that DNS record pointed to the wrong server. Submit your findings."
            },
            "quiz": [
                {"question": "What does DNS do?", "options": ["Encrypts website traffic", "Translates human-readable domain names into IP addresses", "Stores website files", "Speeds up your internet connection"], "correct_index": 1, "explanation": "DNS acts as the internet's phonebook, resolving domain names like example.com into the numeric IP address of the server hosting them."},
                {"question": "What is the default port for HTTPS traffic?", "options": ["21", "80", "443", "8080"], "correct_index": 2, "explanation": "Port 443 is the standard port for HTTPS (secure HTTP) traffic, while port 80 is the standard for unencrypted HTTP."},
                {"question": "Why can a single server run multiple applications at once without conflict?", "options": ["Each application can listen on a different port", "It cannot, only one app can run per server", "All applications automatically share the same port", "Servers are only capable of running one process ever"], "correct_index": 0, "explanation": "Ports let a single server route different types of traffic to different applications, each listening on its own designated port number."}
            ],
            "resources": [
                {"label": "MDN: How DNS Works", "url": "https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "How Servers and the Cloud Actually Work",
            "title": "Launching and Connecting to Your First Cloud Virtual Machine",
            "learning_objective": "By the end of this class, you will be able to launch a cloud virtual machine and connect to it over SSH.",
            "duration_minutes": 35,
            "content_html": """<p>Today you provision your first real cloud server, a milestone moment in this track. A virtual machine (VM) is a slice of a physical server in a data center rented out as if it were your own dedicated computer, and it is the most fundamental building block of cloud infrastructure.</p><h2>Launching a VM</h2><p>Most cloud providers offer a free-tier VM (AWS calls this EC2, GCP calls it Compute Engine). You choose an operating system image (usually a Linux distribution like Ubuntu), a machine size, and launch it, receiving a public IP address in return.</p><pre><code># Example: AWS EC2 free-tier instance type
Instance type: t2.micro (free tier eligible)
OS image: Ubuntu 22.04 LTS
Result: A public IP address, e.g. 3.90.12.45</code></pre><h2>Connecting with SSH</h2><p>SSH (Secure Shell) lets you securely log into your VM's command line from your own laptop, using a key pair instead of a password for security.</p><pre><code>ssh -i my-key.pem ubuntu@3.90.12.45</code></pre><p>Once connected, you are inside a real, running Linux server, the exact environment every command from Day 2 works in. Everything you build for the rest of this track will eventually run on infrastructure just like this.</p>""",
            "key_concepts": ["virtual machines (VMs)", "cloud instance provisioning", "SSH", "key pairs", "public IP addresses"],
            "practical_exercise": {
                "title": "Launch and SSH Into a Free-Tier VM",
                "instructions": "Create a free-tier account with AWS, GCP, or Azure, launch a small free-tier Linux virtual machine, and connect to it using SSH with a generated key pair. Once connected, run 'whoami' and 'uname -a' to confirm you are inside the remote server. Submit a screenshot of your terminal showing the successful SSH connection and command output."
            },
            "quiz": [
                {"question": "What is a virtual machine (VM) in cloud computing?", "options": ["A slice of a physical server rented out as if it were your own dedicated computer", "A physical computer you must buy", "A type of mobile app", "A programming language"], "correct_index": 0, "explanation": "A VM is virtualized computing capacity rented from a cloud provider, behaving like a dedicated server even though it shares underlying physical hardware."},
                {"question": "What protocol is used to securely log into a remote server's command line?", "options": ["FTP", "HTTP", "DNS", "SSH"], "correct_index": 3, "explanation": "SSH (Secure Shell) provides an encrypted connection for remotely accessing and controlling a server's command line."},
                {"question": "What is typically used instead of a password to authenticate an SSH connection to a cloud VM?", "options": ["A CAPTCHA", "A key pair (public/private key)", "A phone number", "A QR code"], "correct_index": 1, "explanation": "Cloud VMs commonly use SSH key pairs for authentication, which are more secure than passwords and standard practice in cloud environments."}
            ],
            "resources": [
                {"label": "AWS EC2 Getting Started", "url": "https://aws.amazon.com/ec2/getting-started/"},
                {"label": "Google Cloud Compute Engine", "url": "https://cloud.google.com/compute/docs"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "How Servers and the Cloud Actually Work",
            "title": "Running Your First Web Server on a Cloud VM",
            "learning_objective": "By the end of this class, you will be able to install and run a simple web server on your cloud VM and access it from your browser.",
            "duration_minutes": 30,
            "content_html": """<p>An empty VM is not useful on its own; it becomes useful once it runs software that other people can access. Today you install and run a real web server on the VM you launched yesterday, and reach it from your own browser, closing the loop from "rented computer" to "live website."</p><h2>Installing and Starting a Web Server</h2><p>Nginx is one of the most widely used web servers in production, lightweight and simple to configure for serving a basic page.</p><pre><code>sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl status nginx</code></pre><h2>Opening the Firewall Port</h2><p>By default, cloud providers block incoming traffic except what you explicitly allow, through a setting usually called a security group (AWS) or firewall rule (GCP). You must open port 80 for HTTP traffic to actually reach Nginx.</p><pre><code># In your cloud provider's security group / firewall settings:
Allow inbound TCP traffic on port 80 from 0.0.0.0/0 (anywhere)</code></pre><p>Once the port is open, visiting <code>http://your-vm-ip-address</code> in a browser should show the default Nginx welcome page, live evidence that your server is reachable from the public internet.</p>""",
            "key_concepts": ["Nginx", "systemctl", "security groups/firewall rules", "opening ports", "public web access"],
            "practical_exercise": {
                "title": "Serve a Custom Page from Your VM",
                "instructions": "Install Nginx on your VM, open port 80 in your cloud provider's firewall/security group settings, then replace the default index.html with a custom page containing your name and today's date. Visit your VM's public IP in a browser to confirm it loads. Submit a screenshot of the custom page loading in your browser via the public IP."
            },
            "quiz": [
                {"question": "What is Nginx?", "options": ["A programming language", "A cloud provider", "A widely used web server for serving web content", "A version control system"], "correct_index": 2, "explanation": "Nginx is a popular, lightweight web server used widely in production to serve web content and handle traffic."},
                {"question": "Why is it necessary to open port 80 in a cloud VM's firewall settings before a website is publicly reachable?", "options": ["Cloud providers block incoming traffic by default until explicitly allowed", "It is not necessary, all ports are open by default", "Port 80 is only used for email", "Opening ports is only required for HTTPS, never HTTP"], "correct_index": 0, "explanation": "Cloud VMs typically block all inbound traffic by default; a security group or firewall rule must explicitly allow the port before external requests can reach the server."},
                {"question": "What command starts the Nginx service on a Linux server using systemctl?", "options": ["sudo apt remove nginx", "sudo systemctl start nginx", "cd nginx", "ls nginx"], "correct_index": 1, "explanation": "sudo systemctl start nginx starts the Nginx service so it begins listening for incoming web requests."}
            ],
            "resources": [
                {"label": "Nginx Documentation", "url": "https://nginx.org/en/docs/"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Containers: Packaging Applications the Modern Way",
            "title": "Why Docker Exists: Solving 'It Works on My Machine'",
            "learning_objective": "By the end of this class, you will be able to explain what a container is and why Docker solves environment-consistency problems.",
            "duration_minutes": 25,
            "content_html": """<p>Every developer has experienced this: code that works perfectly on their own laptop breaks the moment it runs somewhere else, because of a different operating system version, a missing dependency, or a different configuration. Docker exists specifically to solve this problem, and it is now a baseline expectation on almost every DevOps and backend job posting.</p><h2>What a Container Actually Is</h2><p>A <strong>container</strong> packages an application together with everything it needs to run, code, runtime, system libraries, and configuration, into one portable unit. Unlike a full virtual machine, a container shares the host machine's operating system kernel, making it much lighter and faster to start.</p><pre><code>Without Docker: "It works on my machine" (but not the server)
With Docker:    The exact same container runs identically everywhere</code></pre><h2>Containers vs Virtual Machines</h2><p>A VM virtualizes an entire computer, including its own OS, and can take minutes to boot. A container virtualizes only the application layer, typically starting in under a second, which is why modern cloud deployments are built around containers rather than full VMs for individual applications.</p><p>By the end of this week, you will have taken a real application, packaged it into a Docker container, and run that exact same container both on your laptop and on a cloud server.</p>""",
            "key_concepts": ["containers", "Docker", "environment consistency", "containers vs virtual machines"],
            "practical_exercise": {
                "title": "Document a Real 'Works on My Machine' Scenario",
                "instructions": "Interview a developer you know, or research a real forum post/blog post describing a case where code broke when moved between environments due to missing dependencies or version mismatches. Write three to four sentences summarizing the specific problem and explaining how packaging the app in a Docker container would have prevented it. Submit your write-up."
            },
            "quiz": [
                {"question": "What core problem does Docker solve?", "options": ["Slow internet connections", "Inconsistent behavior of an application across different environments", "Writing code faster", "Designing user interfaces"], "correct_index": 1, "explanation": "Docker packages an application with everything it needs to run consistently, solving the classic 'it works on my machine' problem."},
                {"question": "What is the key architectural difference between a container and a virtual machine?", "options": ["Containers require their own full operating system, VMs do not", "There is no real difference", "Containers cannot run on cloud servers", "A container shares the host machine's OS kernel, while a VM virtualizes an entire separate OS"], "correct_index": 3, "explanation": "Containers share the host OS kernel and are lightweight, while VMs virtualize an entire separate operating system, making them heavier and slower to start."},
                {"question": "Roughly how quickly does a container typically start compared to a virtual machine?", "options": ["It takes several minutes, similar to a VM", "Containers never fully start", "In under a second, much faster than a typical VM boot", "Exactly the same speed as a VM"], "correct_index": 2, "explanation": "Because containers do not boot a full separate operating system, they typically start in under a second, far faster than a VM."}
            ],
            "resources": [
                {"label": "Docker: Get Started", "url": "https://www.docker.com/get-started/"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Containers: Packaging Applications the Modern Way",
            "title": "Writing Your First Dockerfile to Containerize an App",
            "learning_objective": "By the end of this class, you will be able to write a Dockerfile that builds a working container image for a simple application.",
            "duration_minutes": 30,
            "content_html": """<p>A Dockerfile is a plain text recipe describing exactly how to build a container image: what base environment to start from, what to install, what code to copy in, and how to start the application. Writing your first one today turns the concept from yesterday into something real and runnable.</p><h2>Anatomy of a Dockerfile</h2><pre><code>FROM node:20-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3000
CMD ["node", "server.js"]</code></pre><h2>What Each Instruction Does</h2><p><code>FROM</code> sets the base image to build on top of. <code>WORKDIR</code> sets the working directory inside the container. <code>COPY</code> brings files from your project into the image. <code>RUN</code> executes a command during the build (like installing dependencies). <code>EXPOSE</code> documents which port the app listens on. <code>CMD</code> defines the command that runs when a container starts from this image.</p><h2>Building and Running the Image</h2><pre><code>docker build -t my-first-app .
docker run -p 3000:3000 my-first-app</code></pre><p>The <code>-p 3000:3000</code> flag maps port 3000 on your machine to port 3000 inside the container, letting you visit <code>localhost:3000</code> and see your containerized app running.</p>""",
            "key_concepts": ["Dockerfile", "FROM/WORKDIR/COPY/RUN/CMD", "docker build", "docker run", "port mapping"],
            "practical_exercise": {
                "title": "Containerize a Simple App",
                "instructions": "Write a Dockerfile for a small application of your choice (a simple Node.js, Python Flask, or static HTML app works fine), build the image with docker build, and run it with docker run, mapping a port so you can view it in your browser. Submit your Dockerfile and a screenshot of the running app in your browser via the container."
            },
            "quiz": [
                {"question": "What does the FROM instruction in a Dockerfile specify?", "options": ["The base image the new image is built on top of", "The port the app listens on", "The command to run when the container starts", "The container's name"], "correct_index": 0, "explanation": "FROM sets the starting base image (such as an OS or language runtime) that the rest of the Dockerfile builds upon."},
                {"question": "What does the CMD instruction define?", "options": ["The base image", "Which files to copy into the image", "The command that runs when a container is started from the built image", "The image's file size"], "correct_index": 2, "explanation": "CMD specifies the default command executed when a container is launched from the image."},
                {"question": "What does the flag -p 3000:3000 do in a 'docker run' command?", "options": ["It sets the container's memory limit", "It deletes port 3000", "It has no effect on networking", "It maps port 3000 on the host machine to port 3000 inside the container"], "correct_index": 3, "explanation": "The -p flag maps a host machine port to a container port, allowing external access to the application running inside the container."}
            ],
            "resources": [
                {"label": "Docker: Dockerfile Reference", "url": "https://docs.docker.com/reference/dockerfile/"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Containers: Packaging Applications the Modern Way",
            "title": "Managing Multi-Container Apps with Docker Compose",
            "learning_objective": "By the end of this class, you will be able to run a multi-container application, such as an app plus a database, using Docker Compose.",
            "duration_minutes": 30,
            "content_html": """<p>Real applications rarely run as a single container; a typical app needs a database, and maybe a cache, running alongside it. Manually starting multiple containers and connecting them with individual docker run commands gets unmanageable fast, which is exactly the problem Docker Compose solves.</p><h2>Defining Multiple Services in One File</h2><p>A docker-compose.yml file describes all the containers your application needs and how they connect, in one declarative configuration.</p><pre><code>version: "3.8"
services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: examplepassword
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:</code></pre><h2>Starting Everything with One Command</h2><pre><code>docker compose up --build</code></pre><p>This single command builds your app's image, pulls the Postgres image, starts both containers, and connects them on a shared network where the <code>web</code> service can reach the database simply by using <code>db</code> as the hostname. The <code>depends_on</code> field ensures the database starts before the app. This exact pattern, app plus database in Compose, is how most real projects are developed locally before deployment.</p>""",
            "key_concepts": ["Docker Compose", "docker-compose.yml", "multi-container apps", "service networking", "volumes"],
            "practical_exercise": {
                "title": "Run an App with a Database Using Docker Compose",
                "instructions": "Write a docker-compose.yml that runs your Dockerized app from Day 7 alongside a Postgres or MySQL database container, using depends_on and a named volume for data persistence. Start everything with 'docker compose up' and confirm both containers are running with 'docker ps'. Submit your docker-compose.yml and a screenshot of docker ps showing both containers."
            },
            "quiz": [
                {"question": "What problem does Docker Compose solve?", "options": ["It replaces the need for Dockerfiles entirely", "It only works with a single container at a time", "It is used exclusively for writing application code", "It manages running and connecting multiple containers together using one configuration file"], "correct_index": 3, "explanation": "Docker Compose lets you define and run multi-container applications (like an app plus a database) together with one declarative file and one command."},
                {"question": "In a docker-compose.yml, what does the depends_on field control?", "options": ["Which port the app uses", "The startup order of services, such as ensuring a database starts before the app", "The container's CPU limit", "The image's file size"], "correct_index": 1, "explanation": "depends_on tells Docker Compose to start one service before another, commonly used to start a database before the application that needs it."},
                {"question": "What command starts all services defined in a docker-compose.yml file?", "options": ["docker compose up", "docker build .", "docker run -p 3000:3000", "docker ps"], "correct_index": 0, "explanation": "docker compose up reads the docker-compose.yml file and starts all defined services together."}
            ],
            "resources": [
                {"label": "Docker Compose Documentation", "url": "https://docs.docker.com/compose/"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Containers: Packaging Applications the Modern Way",
            "title": "Storing and Sharing Images with Docker Hub",
            "learning_objective": "By the end of this class, you will be able to push a Docker image to a container registry and pull it down on another machine.",
            "duration_minutes": 25,
            "content_html": """<p>A container image built only on your laptop is not useful for deployment; a cloud server needs a way to get that exact same image. Container registries, like Docker Hub, solve this by acting as a storage and distribution point for images, similar to how GitHub hosts code.</p><h2>Tagging and Pushing an Image</h2><p>Images are tagged with your registry username and a name, then pushed to make them available for download anywhere.</p><pre><code>docker login
docker build -t yourusername/my-first-app:v1 .
docker push yourusername/my-first-app:v1</code></pre><h2>Pulling the Image on Any Machine</h2><p>Once pushed, that exact image, byte for byte identical, can be pulled and run on a cloud server, a teammate's laptop, or anywhere Docker is installed.</p><pre><code>docker pull yourusername/my-first-app:v1
docker run -p 3000:3000 yourusername/my-first-app:v1</code></pre><h2>Why This Matters for Deployment</h2><p>This exact push/pull workflow is how most modern deployments actually work: your CI/CD pipeline (which you will build in week three) builds an image, pushes it to a registry, and your cloud server pulls and runs it. Understanding this flow now makes the automation you build later far less mysterious.</p>""",
            "key_concepts": ["Docker Hub", "container registries", "image tagging", "docker push/pull"],
            "practical_exercise": {
                "title": "Push and Pull Your Own Docker Image",
                "instructions": "Create a free Docker Hub account, tag your app image from Day 7 with your username, push it to Docker Hub, then delete the local image and pull it back down to confirm it downloads and runs identically. Submit your Docker Hub repository link and a screenshot showing the successful pull and run."
            },
            "quiz": [
                {"question": "What is Docker Hub used for?", "options": ["Writing application code", "Hosting live websites directly", "Storing and distributing container images so they can be pulled and run anywhere", "Managing DNS records"], "correct_index": 2, "explanation": "Docker Hub is a container registry that stores images so they can be pulled and run consistently on any machine with Docker installed."},
                {"question": "What command uploads a locally built image to a registry?", "options": ["docker pull", "docker push", "docker build", "docker run"], "correct_index": 1, "explanation": "docker push uploads a tagged local image to the configured registry, such as Docker Hub."},
                {"question": "Why does the registry-based push/pull workflow matter for deployment pipelines?", "options": ["It has no relevance to deployment", "Registries are only used for personal projects, never in production", "Deployment never involves container registries", "CI/CD pipelines typically build an image, push it to a registry, and the server pulls and runs it from there"], "correct_index": 3, "explanation": "This push/pull pattern is the standard mechanism automated deployment pipelines use to get a built image from CI onto a running server."}
            ],
            "resources": [
                {"label": "Docker Hub", "url": "https://hub.docker.com/"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Containers: Packaging Applications the Modern Way",
            "title": "Deploying Your First Dockerized App to a Live Cloud Server",
            "learning_objective": "By the end of this class, you will be able to deploy a Docker container to a cloud VM so it is reachable on the public internet.",
            "duration_minutes": 35,
            "content_html": """<p>This class connects everything from the last two weeks: a real cloud VM, Docker, and a container image, into one working live deployment. This is the first genuinely production-shaped milestone in this track.</p><h2>Installing Docker on Your Cloud VM</h2><pre><code>ssh -i my-key.pem ubuntu@your-vm-ip
sudo apt update
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER</code></pre><h2>Pulling and Running Your Image on the Server</h2><pre><code>docker pull yourusername/my-first-app:v1
docker run -d -p 80:3000 --restart unless-stopped yourusername/my-first-app:v1</code></pre><p>The <code>-d</code> flag runs the container in the background (detached), <code>-p 80:3000</code> maps the server's public port 80 to your app's internal port 3000, and <code>--restart unless-stopped</code> makes the container automatically restart if it crashes or the server reboots, a small but important reliability detail production teams always set.</p><h2>Confirming It Is Live</h2><p>Open your VM's public IP address in a browser. If port 80 is open in your security group from Day 5, your Dockerized app should now be live on the actual internet, the same app you built and tested only on your laptop days ago.</p>""",
            "key_concepts": ["installing Docker on a server", "docker run -d", "restart policies", "live public deployment"],
            "practical_exercise": {
                "title": "Deploy Your App Live to Your Cloud VM",
                "instructions": "Install Docker on your cloud VM from Day 4, pull your image from Docker Hub, and run it with the -d flag, correct port mapping, and a restart policy of unless-stopped. Confirm the app is publicly reachable by visiting your VM's IP address in a browser from a different network (like your phone's mobile data). Submit a screenshot of the app loading via the public IP, plus the exact docker run command you used."
            },
            "quiz": [
                {"question": "What does the -d flag do in 'docker run -d'?", "options": ["Deletes the container immediately", "Runs the container in the background (detached mode)", "Downloads the image again", "Disables networking for the container"], "correct_index": 1, "explanation": "The -d flag runs a container detached, in the background, so the terminal is freed up rather than staying attached to the container's output."},
                {"question": "Why is a restart policy like --restart unless-stopped important for a production deployment?", "options": ["It makes the container automatically restart if it crashes or the server reboots, improving reliability", "It has no practical effect", "It prevents the container from ever stopping, even intentionally", "It is only relevant during local development"], "correct_index": 0, "explanation": "A restart policy ensures the application keeps running through crashes or server reboots without requiring manual intervention, a basic reliability practice."},
                {"question": "What is a good way to confirm a deployed app is genuinely publicly reachable?", "options": ["Only test it from the same machine that deployed it", "Assume it works if the docker run command did not print an error", "Public reachability cannot be verified", "Visit the server's public IP address from a completely different network, such as mobile data"], "correct_index": 3, "explanation": "Testing from a different network confirms the app is reachable over the public internet, not just accessible locally on the same machine or network."}
            ],
            "resources": [
                {"label": "Docker Engine Installation", "url": "https://docs.docker.com/engine/install/"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Automating Deployment with CI/CD",
            "title": "What CI/CD Actually Means and Why Every Team Uses It",
            "learning_objective": "By the end of this class, you will be able to explain the difference between continuous integration and continuous deployment.",
            "duration_minutes": 20,
            "content_html": """<p>Manually SSHing into a server and running deployment commands by hand, like you did on Day 10, does not scale and is error-prone. CI/CD is the practice of automating this, and it is one of the most consistently listed requirements in DevOps and backend job postings.</p><h2>Continuous Integration (CI)</h2><p><strong>Continuous Integration</strong> means automatically running tests (and often linting or builds) every time code is pushed, catching bugs before they reach production. If a teammate's change breaks something, CI catches it within minutes, not after it has already broken the live app.</p><h2>Continuous Deployment (CD)</h2><p><strong>Continuous Deployment</strong> (or Continuous Delivery) means automatically deploying code to a server once it passes CI, removing manual deployment steps entirely.</p><pre><code>Developer pushes code
   -> CI runs tests automatically
   -> If tests pass, CD deploys automatically
   -> App is live within minutes, with no manual SSH steps</code></pre><h2>Why This Matters for Your Career</h2><p>Companies rely on CI/CD because it makes deployment fast, repeatable, and far less risky than manual steps a tired engineer might get wrong at 11pm. You will build a real, working GitHub Actions CI/CD pipeline over the next several days, ending in the exact automated pipeline your final project requires.</p>""",
            "key_concepts": ["continuous integration", "continuous deployment", "automated testing", "deployment pipelines"],
            "practical_exercise": {
                "title": "Diagram a CI/CD Pipeline",
                "instructions": "Draw or describe step by step what should happen, from a developer pushing code to that code being live on a server, in a CI/CD pipeline for a simple web app. Include at minimum: trigger, test step, build step, and deploy step. Submit your diagram or written step-by-step flow."
            },
            "quiz": [
                {"question": "What does Continuous Integration (CI) primarily automate?", "options": ["Writing the application code itself", "Designing the app's user interface", "Buying cloud server capacity", "Running tests (and often builds/linting) automatically whenever code is pushed"], "correct_index": 3, "explanation": "CI automatically runs tests and checks on every code push, catching problems early rather than after manual review."},
                {"question": "What does Continuous Deployment (CD) automate?", "options": ["Automatically deploying code to a server once it passes CI checks", "Writing test cases", "Designing database schemas", "Creating cloud accounts"], "correct_index": 0, "explanation": "CD automates the deployment step itself, pushing passing code live without requiring a person to manually SSH in and deploy."},
                {"question": "Why do companies prefer CI/CD over manual deployment steps?", "options": ["Manual deployment is always safer", "CI/CD removes the need for testing entirely", "Automated pipelines are faster, more repeatable, and reduce the risk of human error during deployment", "It has no real advantage over manual steps"], "correct_index": 2, "explanation": "Automating deployment reduces the chance of mistakes that can happen with manual, repetitive processes, especially under time pressure."}
            ],
            "resources": [
                {"label": "GitHub Actions", "url": "https://github.com/features/actions"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Automating Deployment with CI/CD",
            "title": "Writing Your First GitHub Actions Workflow to Run Tests",
            "learning_objective": "By the end of this class, you will be able to write a GitHub Actions workflow that automatically runs tests on every push.",
            "duration_minutes": 30,
            "content_html": """<p>GitHub Actions is GitHub's built-in CI/CD tool, meaning you do not need to set up any separate infrastructure to start automating tests and deployments. Today you write your first real workflow, the CI half of CI/CD.</p><h2>Anatomy of a Workflow File</h2><p>Workflows live in a specific folder in your repository and are written in YAML, triggered automatically by events like a push.</p><pre><code># .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm install
      - run: npm test</code></pre><h2>What Happens on Every Push</h2><p>Once this file is committed, GitHub automatically spins up a fresh Ubuntu virtual machine, checks out your code, installs dependencies, and runs your test suite, every single time anyone pushes to main or opens a pull request. You can watch this run live in your repository's "Actions" tab, and a red X versus a green check tells the whole team instantly whether a change is safe.</p>""",
            "key_concepts": ["GitHub Actions", "workflow YAML files", "on: push triggers", "jobs and steps", "actions/checkout"],
            "practical_exercise": {
                "title": "Add an Automated Test Workflow to a Real Repository",
                "instructions": "Take a project with at least one automated test (or add a trivial test if needed), create a .github/workflows/test.yml file that installs dependencies and runs the test suite on every push to main, then push a commit and confirm the workflow runs successfully in the Actions tab. Submit a link to your repository's Actions tab showing a passing run, plus your workflow YAML file."
            },
            "quiz": [
                {"question": "What format are GitHub Actions workflow files written in?", "options": ["YAML", "JSON", "XML", "Plain text with no structure"], "correct_index": 0, "explanation": "GitHub Actions workflows are defined in YAML files, typically located in the .github/workflows directory of a repository."},
                {"question": "What triggers the workflow shown to run automatically?", "options": ["Manually clicking a button every time, with no automatic trigger", "A push to the main branch or a pull request targeting main", "Only when a new repository is created", "It runs on a fixed schedule regardless of code changes"], "correct_index": 1, "explanation": "The 'on: push' and 'on: pull_request' triggers cause the workflow to run automatically whenever those events occur on the specified branches."},
                {"question": "Where can you view the live results of a GitHub Actions workflow run?", "options": ["Only in the terminal on your own laptop", "It cannot be viewed anywhere", "In the repository's Actions tab on GitHub", "Only in an email notification with no web view"], "correct_index": 2, "explanation": "GitHub provides an Actions tab within each repository showing the status and logs of every workflow run."}
            ],
            "resources": [
                {"label": "GitHub Actions Documentation", "url": "https://docs.github.com/en/actions"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Automating Deployment with CI/CD",
            "title": "Extending Your Pipeline to Build and Push a Docker Image",
            "learning_objective": "By the end of this class, you will be able to extend a GitHub Actions workflow to automatically build and push a Docker image.",
            "duration_minutes": 30,
            "content_html": """<p>Now you connect two things you have already built separately: your Dockerfile from week two and your GitHub Actions workflow from yesterday. Automating the image build step is the bridge between CI and CD, the "build" stage that produces the artifact your deployment step will use.</p><h2>Storing Secrets Safely</h2><p>Your Docker Hub username and password must never be hardcoded in a workflow file. GitHub Actions provides encrypted repository secrets for exactly this.</p><pre><code># In your GitHub repo: Settings -> Secrets and variables -> Actions
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN</code></pre><h2>Adding a Build-and-Push Job</h2><pre><code>  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: yourusername/my-first-app:latest</code></pre><p>The <code>needs: test</code> line ensures this job only runs after the test job passes, so a broken build never gets pushed to your registry. Every push to main now automatically tests your code, builds a fresh image, and pushes it, with zero manual docker commands.</p>""",
            "key_concepts": ["GitHub Actions secrets", "docker/build-push-action", "job dependencies (needs)", "automated image builds"],
            "practical_exercise": {
                "title": "Automate Your Docker Image Build",
                "instructions": "Add your Docker Hub credentials as repository secrets, then extend your workflow with a build-and-push job that depends on your test job passing and pushes a freshly built image to Docker Hub on every push to main. Push a small code change and confirm a new image appears in your Docker Hub repository automatically. Submit your updated workflow YAML and a screenshot of the new image on Docker Hub with its build timestamp."
            },
            "quiz": [
                {"question": "Why should Docker Hub credentials never be hardcoded directly into a workflow YAML file?", "options": ["YAML files cannot contain text values", "Hardcoded credentials would be publicly visible in the repository, a serious security risk", "It would make the build faster", "There is no risk either way"], "correct_index": 1, "explanation": "Credentials in a workflow file would be exposed to anyone who can view the repository; encrypted secrets keep them hidden while still usable by the workflow."},
                {"question": "What does 'needs: test' do in a GitHub Actions job definition?", "options": ["It makes this job wait and only run if the referenced test job succeeds first", "It deletes the test job", "It has no functional effect", "It runs the job before the test job"], "correct_index": 0, "explanation": "The needs field creates a dependency, ensuring a job only runs after the specified job(s) complete successfully."},
                {"question": "What is the practical benefit of automatically building and pushing a Docker image on every push to main?", "options": ["It removes the need for a Dockerfile", "It has no benefit over manual builds", "It ensures a fresh, tested image is always available without manual docker build/push commands", "It automatically deploys the app with no further steps needed"], "correct_index": 2, "explanation": "Automating the build-and-push step removes manual, error-prone steps and guarantees the pushed image corresponds to tested, current code."}
            ],
            "resources": [
                {"label": "GitHub Actions: Encrypted Secrets", "url": "https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Automating Deployment with CI/CD",
            "title": "Completing the Pipeline: Automatic Deployment to Your Server",
            "learning_objective": "By the end of this class, you will be able to add an automated deployment step so a pushed image is deployed to a live server without manual intervention.",
            "duration_minutes": 30,
            "content_html": """<p>Today you complete the full CI/CD loop: your pipeline now tests, builds, pushes, and deploys, all triggered by a single git push. This is the exact automated pipeline your final project's rubric requires, and it is worth building carefully.</p><h2>Deploying Over SSH from GitHub Actions</h2><p>A common pattern uses an SSH action to connect to your cloud VM and run deployment commands remotely, using a private key stored as a secret.</p><pre><code>  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ubuntu
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            docker pull yourusername/my-first-app:latest
            docker stop my-app || true
            docker rm my-app || true
            docker run -d --name my-app -p 80:3000 --restart unless-stopped yourusername/my-first-app:latest</code></pre><h2>Why Each Piece Matters</h2><p>The script stops and removes any existing container before starting the new one, so you do not end up with a stale version still running and blocking the port. The <code>|| true</code> prevents the workflow from failing if there was no existing container to stop, which is the case on the very first deployment.</p><p>Push a change to main and watch it: within a few minutes, without touching SSH yourself, your live app updates automatically.</p>""",
            "key_concepts": ["automated SSH deployment", "appleboy/ssh-action", "zero-manual-step deployment", "graceful container replacement"],
            "practical_exercise": {
                "title": "Complete Your Automated Deployment Pipeline",
                "instructions": "Add your server's IP and an SSH private key as repository secrets, then add a deploy job that connects over SSH, pulls the latest image, and replaces the running container. Make a small visible change to your app, push it to main, and confirm it appears live on your server within a few minutes with no manual steps. Submit your complete workflow YAML and a screenshot showing the change live on your server plus the successful GitHub Actions run."
            },
            "quiz": [
                {"question": "What is the purpose of stopping and removing the existing container before starting the new one in the deploy script?", "options": ["To avoid a stale old version staying alive and blocking the port from the new container", "It is unnecessary and can be skipped safely", "It deletes the Docker image from the registry", "It disables the server's firewall"], "correct_index": 0, "explanation": "Removing the old container first prevents port conflicts and ensures the new container's traffic replaces the old version cleanly."},
                {"question": "Why is '|| true' added after the stop and remove commands in the deploy script?", "options": ["It has no purpose and could be removed", "It prevents the workflow from failing if there was no existing container to stop, such as on the first deployment", "It forces the deployment to always fail", "It skips the docker pull step"], "correct_index": 1, "explanation": "Without || true, the script would error out on the first deployment (when no container exists yet to stop), halting the workflow unnecessarily."},
                {"question": "What triggers the full test-build-push-deploy pipeline once it is fully set up?", "options": ["Manually running each step by hand every time", "Restarting the cloud server", "Editing the Dockerfile only", "A single git push to the main branch"], "correct_index": 3, "explanation": "Once configured, the entire pipeline runs automatically from a single push to main, requiring no manual intervention."}
            ],
            "resources": [
                {"label": "GitHub Actions Documentation", "url": "https://docs.github.com/en/actions"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Automating Deployment with CI/CD",
            "title": "Case Study: Debugging a Broken CI/CD Pipeline",
            "learning_objective": "By the end of this class, you will be able to systematically diagnose and fix a failing GitHub Actions workflow using its logs.",
            "duration_minutes": 25,
            "content_html": """<p>Pipelines break. A dependency version changes, a secret gets misspelled, a script has a typo, and suddenly your automated deployment is red instead of green. Debugging CI/CD failures methodically, rather than randomly changing things, is a skill real DevOps engineers rely on daily.</p><h2>Reading Workflow Logs</h2><p>Every step in a GitHub Actions run has its own expandable log. The failing step is marked with a red X, and the log usually shows the exact error, a missing environment variable, a failed command, or a timeout.</p><pre><code>Run docker pull yourusername/my-first-app:latest
Error response from daemon: pull access denied, repository does not exist
or may require authorization</code></pre><h2>Common CI/CD Failure Causes</h2><ul><li>A secret name typo (referencing <code>secrets.DOCKER_TOKEN</code> when the actual secret is named <code>DOCKERHUB_TOKEN</code>)</li><li>Forgetting to update the image tag after renaming a repository</li><li>A test that passes locally but fails in CI due to a missing environment variable</li><li>An SSH key with incorrect permissions or a mismatched public/private key pair</li></ul><h2>A Repeatable Debugging Process</h2><p>1) Find the exact failing step. 2) Read its full log output, not just the summary. 3) Reproduce the failing command locally if possible. 4) Fix the smallest possible cause. 5) Push again and confirm green. This mirrors the debugging process from earlier tracks, applied to infrastructure instead of application code.</p>""",
            "key_concepts": ["reading GitHub Actions logs", "common pipeline failure causes", "secret misconfiguration", "systematic pipeline debugging"],
            "practical_exercise": {
                "title": "Break and Fix Your Own Pipeline",
                "instructions": "Intentionally break your pipeline from earlier this week (misspell a secret name, or introduce a failing test), push the change, and watch it fail in the Actions tab. Read the log carefully, diagnose the exact cause, fix it, and confirm the pipeline turns green again. Submit screenshots of both the failing run's log and the fixed, passing run."
            },
            "quiz": [
                {"question": "Where should you look first when a GitHub Actions workflow fails?", "options": ["Delete the repository and start over", "The specific failing step's expanded log output in the Actions tab", "Randomly change unrelated files until it passes", "Ignore it, failures do not need to be investigated"], "correct_index": 1, "explanation": "The failing step's log usually contains the exact error message needed to diagnose the problem, making it the correct starting point."},
                {"question": "What is a common cause of CI/CD pipeline failures related to secrets?", "options": ["Secrets never cause failures", "Secrets automatically fix themselves over time", "A typo in a secret's name, referencing a name that does not match what was actually configured", "Using too many secrets always breaks pipelines"], "correct_index": 2, "explanation": "A mismatched secret name (referencing secrets.X when the configured secret is actually named Y) is a very common and easy-to-make pipeline failure."},
                {"question": "What is the recommended first debugging step after identifying the failing log message?", "options": ["Try to reproduce the failing command locally, if possible, before making changes", "Immediately rewrite the entire pipeline from scratch", "Disable the whole pipeline permanently", "Contact GitHub support before trying anything else"], "correct_index": 0, "explanation": "Reproducing the failure locally, when possible, helps confirm the actual cause before making changes, avoiding blind trial and error."}
            ],
            "resources": [
                {"label": "GitHub Actions: Monitoring Workflows", "url": "https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Monitoring, Reliability, and Container Orchestration",
            "title": "Knowing When Your App Is Down: Health Checks and Basic Monitoring",
            "learning_objective": "By the end of this class, you will be able to add a health check endpoint and use it to monitor whether an app is running correctly.",
            "duration_minutes": 25,
            "content_html": """<p>An app that crashes with nobody noticing for six hours is a far worse outcome than an app that crashes but alerts someone within a minute. Monitoring is not optional polish, it is a core responsibility of running real software, and "basic monitoring" is explicitly part of your final project's requirements.</p><h2>Adding a Health Check Endpoint</h2><p>A health check is a simple endpoint that returns a success response if the app (and often its database connection) is working correctly.</p><pre><code># Simple Express.js health check example
app.get("/health", (req, res) =&gt; {
  res.status(200).json({ status: "ok", timestamp: new Date().toISOString() });
});</code></pre><h2>Checking It Automatically</h2><p>A free uptime monitoring service can ping this endpoint every few minutes and alert you (by email or SMS) if it stops responding correctly.</p><pre><code>Monitor: GET https://your-app.com/health every 5 minutes
Alert condition: non-200 response, or no response within 10 seconds</code></pre><h2>Why This Is a Real Job Skill</h2><p>"How would you know if this app went down at 3am?" is a genuine interview question for cloud and DevOps roles. The honest answer, after today, is: a health check endpoint plus an uptime monitor that alerts you, exactly the setup you are building right now.</p>""",
            "key_concepts": ["health check endpoints", "uptime monitoring", "alerting", "reliability basics"],
            "practical_exercise": {
                "title": "Add a Health Check and Set Up Monitoring",
                "instructions": "Add a /health endpoint to your deployed app that returns a 200 status with a JSON status message, redeploy it through your CI/CD pipeline, then set up a free uptime monitoring service to check that endpoint every few minutes with email alerting on failure. Submit a screenshot of your health endpoint responding and a screenshot of your monitoring service configuration."
            },
            "quiz": [
                {"question": "What is the purpose of a health check endpoint?", "options": ["To provide a simple, reliable way to confirm the app is running correctly", "To display the app's homepage", "To handle user login", "To store application data"], "correct_index": 0, "explanation": "A health check endpoint gives monitoring tools a lightweight, consistent way to confirm the application is up and functioning."},
                {"question": "What should an uptime monitor typically do if a health check stops responding correctly?", "options": ["Do nothing and wait indefinitely", "Automatically delete the application", "Restart the entire cloud provider account", "Alert the responsible person, such as by email or SMS"], "correct_index": 3, "explanation": "The core value of uptime monitoring is timely alerting so a human can respond quickly when something breaks."},
                {"question": "Why is monitoring considered a core responsibility rather than optional polish?", "options": ["It is purely cosmetic and rarely checked by employers", "Without it, an outage could go unnoticed for hours, directly harming real users", "Monitoring only matters for very large companies", "Health checks are only used during development, never in production"], "correct_index": 1, "explanation": "Without monitoring, a crashed or degraded application can remain broken for a long time before anyone notices, directly affecting users."}
            ],
            "resources": [
                {"label": "AWS: Monitoring Overview", "url": "https://aws.amazon.com/what-is/application-monitoring/"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Monitoring, Reliability, and Container Orchestration",
            "title": "Reading Logs to Diagnose Problems in a Running App",
            "learning_objective": "By the end of this class, you will be able to view and search a running container's logs to diagnose an issue.",
            "duration_minutes": 25,
            "content_html": """<p>When your health check fails or a user reports a bug, logs are usually the first and best source of truth about what actually happened. Knowing how to quickly pull and search logs from a live container is a skill you will use in nearly every real incident.</p><h2>Viewing Container Logs</h2><pre><code>docker logs my-app                # print all logs
docker logs -f my-app             # follow logs live, like tail -f
docker logs --tail 100 my-app     # show only the last 100 lines
docker logs --since 30m my-app    # show logs from the last 30 minutes</code></pre><h2>Searching Logs for Errors</h2><p>Combining docker logs with grep, which you learned back on Day 2, lets you quickly filter noisy logs down to just what matters.</p><pre><code>docker logs my-app 2&gt;&amp;1 | grep -i "error"</code></pre><h2>Good Logging Habits in Your Own Code</h2><p>Logs are only useful if the application actually writes meaningful ones. A good log line includes a timestamp, a severity level, and enough context to understand what happened without guessing.</p><pre><code>console.log(`[${new Date().toISOString()}] ERROR: Failed to connect to database - ${err.message}`);</code></pre><p>This habit, writing clear logs as you build, pays off enormously the first time something breaks in production at an inconvenient hour.</p>""",
            "key_concepts": ["docker logs", "log filtering with grep", "log levels", "structured log messages"],
            "practical_exercise": {
                "title": "Diagnose a Simulated Failure Using Logs",
                "instructions": "In your deployed app, add a log statement that fires with an ERROR level message when a specific route is hit (simulate a failure condition), trigger it, then use docker logs combined with grep to find that specific error message among the container's output. Submit the exact commands you used and a screenshot of the filtered log output."
            },
            "quiz": [
                {"question": "What does 'docker logs -f my-app' do?", "options": ["Deletes the container's logs", "Force-stops the container", "Follows the container's logs live, showing new output as it happens", "Filters logs by error level automatically"], "correct_index": 2, "explanation": "The -f flag follows log output in real time, similar to the Unix tail -f command, useful for watching what happens as it occurs."},
                {"question": "Why is combining docker logs with grep useful?", "options": ["It lets you quickly filter large amounts of log output down to only relevant lines, like errors", "It has no practical use", "grep only works on application code, not logs", "It permanently deletes matching log lines"], "correct_index": 0, "explanation": "Piping logs through grep filters noisy output down to lines matching a specific pattern, such as the word 'error', making problems easier to spot."},
                {"question": "What makes a log message genuinely useful for diagnosing a problem later?", "options": ["Logging as little information as possible", "Including a timestamp, severity level, and enough context to understand what happened", "Avoiding any mention of error details", "Logs do not need to be readable by humans"], "correct_index": 1, "explanation": "Clear, contextual log messages with timestamps and severity levels make it far easier to reconstruct what happened during an incident."}
            ],
            "resources": [
                {"label": "Docker: docker logs Reference", "url": "https://docs.docker.com/reference/cli/docker/container/logs/"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Monitoring, Reliability, and Container Orchestration",
            "title": "Understanding Kubernetes and Why Companies Use It at Scale",
            "learning_objective": "By the end of this class, you will be able to explain what Kubernetes does and why it is used to run containers at scale.",
            "duration_minutes": 25,
            "content_html": """<p>Running one container on one server, as you have done so far, works fine for a small project. But what happens when a company needs to run hundreds of containers across many servers, automatically restart failed ones, and scale up during high traffic? That is the exact problem Kubernetes solves, and its name appears in an enormous share of cloud and DevOps job postings.</p><h2>What Kubernetes Actually Does</h2><p>Kubernetes (often called K8s) is a container orchestration system: it decides which server runs which container, restarts containers that crash, scales the number of running containers up or down based on load, and routes traffic to healthy containers only.</p><pre><code>You declare:  "I want 3 copies of my-app running, always"
Kubernetes:   Continuously ensures exactly 3 healthy copies exist,
              replacing any that crash automatically</code></pre><h2>Core Kubernetes Concepts</h2><p>A <strong>Pod</strong> is the smallest deployable unit, usually wrapping one container. A <strong>Deployment</strong> describes how many replicas of a Pod should run. A <strong>Service</strong> gives a stable network address to a set of Pods, even as individual Pods are replaced.</p><p>You will not run a full production Kubernetes cluster in this beginner track, but understanding these core concepts, and being able to explain them, is exactly what a cloud/DevOps interview at this level tests for.</p>""",
            "key_concepts": ["Kubernetes (K8s)", "container orchestration", "Pods", "Deployments", "Services"],
            "practical_exercise": {
                "title": "Map Docker Compose Concepts to Kubernetes",
                "instructions": "Take your docker-compose.yml from Day 8 and write a short explanation mapping each concept to its Kubernetes equivalent: which parts would become a Deployment, which would become a Service, and what would need to change to run multiple replicas of your app. Submit your written mapping, at least 150 words."
            },
            "quiz": [
                {"question": "What problem does Kubernetes primarily solve?", "options": ["Writing application code faster", "Automatically managing, scaling, and restarting containers across many servers", "Designing user interfaces", "Replacing the need for Docker entirely"], "correct_index": 1, "explanation": "Kubernetes orchestrates containers at scale, handling scheduling, restarts, and scaling automatically across a cluster of servers."},
                {"question": "What is a Kubernetes Pod?", "options": ["An entire physical server", "A type of database", "A monitoring dashboard", "The smallest deployable unit in Kubernetes, usually wrapping one container"], "correct_index": 3, "explanation": "A Pod is the basic building block in Kubernetes, typically wrapping a single container (or tightly coupled containers) as the smallest deployable unit."},
                {"question": "What does a Kubernetes Deployment describe?", "options": ["The visual design of an app", "The DNS records for a domain", "How many replicas of a Pod should run and how to update them", "The billing plan for a cloud account"], "correct_index": 2, "explanation": "A Deployment defines the desired state for a set of Pods, including how many replicas should be running at all times."}
            ],
            "resources": [
                {"label": "Kubernetes Documentation", "url": "https://kubernetes.io/docs/home/"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Monitoring, Reliability, and Container Orchestration",
            "title": "Managing Application Secrets and Environment Variables Safely",
            "learning_objective": "By the end of this class, you will be able to correctly manage environment variables and secrets across local, CI, and production environments.",
            "duration_minutes": 25,
            "content_html": """<p>Database passwords, API keys, and other sensitive values should never be hardcoded into your application code or committed to Git, yet this remains one of the most common security mistakes made by beginners and even experienced developers under deadline pressure.</p><h2>Using .env Files Locally</h2><p>Locally, secrets are typically stored in a .env file, which must be excluded from version control using .gitignore.</p><pre><code># .env
DATABASE_URL=postgres://user:pass@localhost:5432/mydb
API_KEY=sk_test_abc123

# .gitignore
.env</code></pre><h2>Environment Variables in Docker and CI/CD</h2><p>In Docker, secrets are passed at runtime rather than baked into the image. In GitHub Actions, they come from encrypted repository secrets, as you used on Day 13.</p><pre><code>docker run -e DATABASE_URL=$DATABASE_URL -p 3000:3000 my-app</code></pre><h2>Why This Discipline Matters</h2><p>A secret committed to a public GitHub repository, even briefly, can be scraped by automated bots within minutes and used maliciously. Treating .env files, Docker environment variables, and CI secrets as three separate, correctly scoped layers, never mixing them or hardcoding values, is a non-negotiable professional habit in cloud and DevOps work.</p>""",
            "key_concepts": [".env files", ".gitignore", "environment variables in Docker", "CI/CD secrets", "secret hygiene"],
            "practical_exercise": {
                "title": "Audit and Fix Secret Handling in a Project",
                "instructions": "Review one of your projects from this track for any hardcoded secrets or credentials in the code, move any you find into a .env file, add .env to .gitignore if it is not already there, and confirm the app still works by reading values from environment variables instead. Submit a before/after comparison showing what was hardcoded and how you fixed it."
            },
            "quiz": [
                {"question": "Why should secrets like database passwords never be hardcoded directly into application code?", "options": ["If committed to a public repository, they can be discovered and exploited by automated bots within minutes", "Hardcoding secrets has no downside", "Hardcoded values run slower than environment variables", "It is only a concern for very large companies"], "correct_index": 0, "explanation": "Publicly exposed secrets, even briefly, are routinely scraped by automated bots scanning GitHub, creating a real and immediate security risk."},
                {"question": "What file should a .env file be listed in to prevent it from being committed to Git?", "options": ["package.json", "Dockerfile", ".gitignore", "README.md"], "correct_index": 2, "explanation": ".gitignore tells Git which files to exclude from version control, and .env should always be listed there to avoid committing secrets."},
                {"question": "Where do secrets typically come from when running inside a GitHub Actions workflow?", "options": ["A local .env file on the runner's disk", "They are typed in manually every run", "GitHub Actions cannot use secrets at all", "Encrypted repository secrets configured in GitHub settings"], "correct_index": 3, "explanation": "GitHub Actions workflows access sensitive values through encrypted repository secrets rather than local files or hardcoded values."}
            ],
            "resources": [
                {"label": "GitHub Actions: Using Secrets", "url": "https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Monitoring, Reliability, and Container Orchestration",
            "title": "Case Study: Diagnosing and Fixing a Production Outage",
            "learning_objective": "By the end of this class, you will be able to work through a simulated production outage using logs, monitoring, and a structured incident process.",
            "duration_minutes": 30,
            "content_html": """<p>This class simulates the exact scenario you were building toward all week: your monitoring alerts fire, and now what? Real DevOps and cloud engineers are judged heavily on how calmly and systematically they respond to exactly this moment.</p><h2>A Realistic Incident Scenario</h2><p>Imagine your health check monitor just alerted you: your app is returning errors. A structured response looks like this: 1) Confirm the outage is real by checking the endpoint yourself. 2) Check container logs for the error. 3) Check recent deployments, did something just get pushed? 4) Check resource usage, is the server out of memory or disk space?</p><pre><code>docker ps                     # is the container even running?
docker logs --tail 100 my-app # what does the app say went wrong?
df -h                         # is the disk full?
free -h                       # is the server out of memory?</code></pre><h2>Rolling Back Safely</h2><p>If a recent deployment caused the issue, the fastest fix is often not debugging forward but rolling back to the last known-good image.</p><pre><code>docker pull yourusername/my-first-app:previous-tag
docker stop my-app &amp;&amp; docker rm my-app
docker run -d --name my-app -p 80:3000 yourusername/my-first-app:previous-tag</code></pre><p>Writing a short incident summary afterward, what broke, why, and how it was fixed, is standard practice at real companies and is exactly the kind of story you can tell in an interview.</p>""",
            "key_concepts": ["incident response process", "rollback strategy", "resource diagnostics", "post-incident summary"],
            "practical_exercise": {
                "title": "Simulate and Resolve an Outage",
                "instructions": "Intentionally deploy a broken version of your app (introduce a code bug that causes it to crash or error), confirm the outage using your health check, diagnose the cause using docker logs, then roll back or fix and redeploy through your pipeline. Write a short incident summary: what broke, how you found it, and how you fixed it. Submit your incident summary and screenshots showing the broken state and the resolved state."
            },
            "quiz": [
                {"question": "What is the recommended first step after receiving an alert that an app may be down?", "options": ["Immediately delete the server", "Wait 24 hours to see if it resolves on its own", "Roll back before investigating anything", "Confirm the outage is real by checking the endpoint yourself"], "correct_index": 3, "explanation": "Confirming the alert reflects a real problem (rather than a false alarm) is the correct first step before taking any corrective action."},
                {"question": "What is often the fastest fix when a recent deployment caused an outage?", "options": ["Rewriting the entire application from scratch", "Rolling back to the last known-good image", "Deleting the monitoring system", "Ignoring the issue until the next scheduled deployment"], "correct_index": 1, "explanation": "Rolling back to a previously working image is typically faster and safer than debugging forward under pressure during an active outage."},
                {"question": "Why is writing a short incident summary after resolving an outage considered good practice?", "options": ["It documents what broke, why, and how it was fixed, which helps prevent recurrence and is useful to discuss in interviews", "It has no value once the issue is fixed", "Incident summaries are only required by law in some countries", "It replaces the need for monitoring going forward"], "correct_index": 0, "explanation": "A clear incident summary captures lessons learned, helps prevent similar issues, and is a strong, concrete example to reference in job interviews."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Cloud Provider Deep Dive",
            "title": "Understanding IAM: Who Can Do What in Your Cloud Account",
            "learning_objective": "By the end of this class, you will be able to explain IAM and apply the principle of least privilege to a cloud account.",
            "duration_minutes": 25,
            "content_html": """<p>Every major security breach involving cloud infrastructure that makes the news usually traces back to overly broad permissions: a leaked key that had far more access than it needed. Identity and Access Management (IAM) is how cloud providers control exactly who, and what, can do exactly what.</p><h2>Users, Roles, and Policies</h2><p>An IAM <strong>user</strong> represents a person or service. A <strong>policy</strong> is a set of permissions, like "can read from this storage bucket" or "can start and stop virtual machines." A <strong>role</strong> is a set of permissions that can be assumed temporarily, often by an application rather than a person.</p><pre><code>{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::my-app-bucket/*"
}</code></pre><h2>The Principle of Least Privilege</h2><p>This IAM policy example allows reading files from one specific storage bucket, and nothing else, not deleting files, not accessing other buckets, not launching servers. This is the <strong>principle of least privilege</strong>: every user or service should have exactly the permissions it needs to do its job, and no more.</p><h2>Why This Matters</h2><p>Using your cloud account's root/admin credentials for everyday work, instead of creating scoped-down IAM users, is one of the most common beginner mistakes, and one that real hiring managers specifically ask about to gauge security awareness.</p>""",
            "key_concepts": ["IAM", "users, roles, policies", "principle of least privilege", "cloud account security"],
            "practical_exercise": {
                "title": "Create a Least-Privilege IAM User",
                "instructions": "In your cloud provider's console, create a new IAM user (separate from your root account) with a custom policy that grants only the specific permissions needed for one task, such as reading from a single storage bucket, rather than full admin access. Submit a screenshot of the IAM user and its attached policy, along with two sentences explaining what it can and cannot do."
            },
            "quiz": [
                {"question": "What does an IAM policy define?", "options": ["The visual theme of a cloud dashboard", "The billing amount for a cloud account", "A specific set of permissions, defining what actions are allowed on which resources", "The physical location of a data center"], "correct_index": 2, "explanation": "An IAM policy is a document specifying exactly which actions are allowed (or denied) on which resources."},
                {"question": "What does the principle of least privilege mean?", "options": ["Giving every user full administrator access for convenience", "Giving a user or service exactly the permissions needed for its job, and no more", "Removing all permissions from every account", "Only applying to root account users"], "correct_index": 1, "explanation": "Least privilege means scoping permissions as narrowly as possible to what is actually required, reducing the impact if credentials are ever compromised."},
                {"question": "Why is using root/admin credentials for everyday cloud work considered a bad practice?", "options": ["It is actually the recommended best practice", "Root credentials cannot be used for regular tasks at all", "There is no meaningful security difference", "It gives far more access than needed for routine tasks, increasing risk if credentials are exposed"], "correct_index": 3, "explanation": "Root/admin credentials have unrestricted access; using them for routine work unnecessarily increases the damage possible if those credentials leak."}
            ],
            "resources": [
                {"label": "AWS IAM Documentation", "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Cloud Provider Deep Dive",
            "title": "Using Managed Databases Instead of Self-Hosting One",
            "learning_objective": "By the end of this class, you will be able to explain the tradeoffs of a managed database service and connect an app to one.",
            "duration_minutes": 25,
            "content_html": """<p>Running your own database inside a container, as you did on Day 8, works for development, but production teams almost always use a managed database service instead, where the cloud provider handles backups, patching, and failover for you.</p><h2>Self-Hosted vs Managed Databases</h2><p>A self-hosted database (like the Postgres container from week two) requires you to handle backups, security patches, and scaling manually. A managed service, like Amazon RDS, Google Cloud SQL, or a service like Supabase or Neon, handles these operational burdens automatically, for a cost.</p><pre><code>Self-hosted:  You manage backups, updates, scaling, and failover
Managed:      Provider handles backups, updates, scaling; you manage data/schema</code></pre><h2>Connecting an App to a Managed Database</h2><p>From your application's perspective, very little changes, you still connect using a connection string, just pointing at the managed service's endpoint instead of localhost or a container name.</p><pre><code>DATABASE_URL=postgresql://user:password@mydb.abc123.us-east-1.rds.amazonaws.com:5432/myapp</code></pre><h2>Why This Matters for Real Projects</h2><p>For a real production app, especially one holding real user data, a managed database is almost always the right default choice, trading a modest cost for dramatically reduced operational risk, which is exactly the reasoning a hiring manager wants to hear you articulate.</p>""",
            "key_concepts": ["managed database services", "RDS/Cloud SQL", "connection strings", "operational tradeoffs"],
            "practical_exercise": {
                "title": "Provision a Free-Tier Managed Database",
                "instructions": "Create a free-tier managed database instance (using AWS RDS free tier, or a free service like Supabase or Neon), retrieve its connection string, and connect to it from your local machine using a database client or command-line tool to confirm it works. Submit a screenshot of the successful connection and the (credentials redacted) connection details."
            },
            "quiz": [
                {"question": "What is a key advantage of a managed database service over self-hosting one?", "options": ["Managed databases are always free", "The provider handles operational tasks like backups, patching, and failover automatically", "Managed databases require no connection string", "There is no real difference"], "correct_index": 1, "explanation": "Managed database services take on operational burdens like backups and patching, reducing the operational risk and effort for the application team."},
                {"question": "From an application's perspective, what typically changes when switching from a self-hosted to a managed database?", "options": ["Mainly just the connection string, pointing to the managed service's endpoint instead", "The entire application must be rewritten", "Nothing changes, managed databases cannot be connected to externally", "The application must stop using SQL"], "correct_index": 0, "explanation": "Applications generally connect the same way (via a connection string); the main change is pointing at the managed service's endpoint instead of a local or containerized database."},
                {"question": "Why would a production team holding real user data typically prefer a managed database?", "options": ["It has no meaningful benefit over self-hosting", "Managed databases cannot store real user data", "It is required by law in every case", "It trades a modest cost for significantly reduced operational risk around backups and failover"], "correct_index": 3, "explanation": "For real production data, the reduced risk of data loss or downtime from a managed provider's backup and failover handling is usually worth the added cost."}
            ],
            "resources": [
                {"label": "AWS RDS Documentation", "url": "https://docs.aws.amazon.com/rds/"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Cloud Provider Deep Dive",
            "title": "Understanding Cloud Costs and Avoiding Surprise Bills",
            "learning_objective": "By the end of this class, you will be able to explain how cloud billing works and set up alerts to avoid unexpected charges.",
            "duration_minutes": 25,
            "content_html": """<p>A surprise cloud bill is one of the most common bad experiences for beginners, sometimes running into hundreds of dollars from a forgotten running resource. Understanding how billing actually works, and protecting yourself with budget alerts, is essential before you start experimenting more freely.</p><h2>How Cloud Billing Actually Works</h2><p>Most cloud resources are billed by the hour or by usage, not a flat monthly fee, meaning a VM left running, even if idle and unused, keeps accumulating cost until you explicitly stop or terminate it.</p><pre><code>t2.micro instance: $0.0116/hour if outside free tier
Left running for 30 days: 720 hours x $0.0116 = ~$8.35
Multiple forgotten instances: costs compound quickly</code></pre><h2>Setting Up Budget Alerts</h2><p>Every major cloud provider lets you set a budget with email alerts at specific thresholds, a five-minute setup that has saved countless beginners from a nasty surprise.</p><pre><code># AWS Billing -> Budgets -> Create budget
Budget amount: $5.00
Alert at: 50%, 80%, 100% of budget</code></pre><h2>A Habit That Saves Money</h2><p>Always stop or terminate cloud VMs and delete unused resources (like unattached storage volumes or old snapshots) when you are done with a session. Making this a closing habit, the way you would close a tab you are not using, prevents almost all beginner billing surprises.</p>""",
            "key_concepts": ["hourly cloud billing", "free tier limits", "budget alerts", "resource cleanup habits"],
            "practical_exercise": {
                "title": "Set Up a Budget Alert on Your Cloud Account",
                "instructions": "In your cloud provider's billing console, create a budget of a small amount (such as $5) with email alerts at 50%, 80%, and 100% thresholds. Then review your account for any running resources you no longer need and stop or terminate them. Submit a screenshot of your configured budget alert and a note on any resources you cleaned up."
            },
            "quiz": [
                {"question": "How are most cloud resources like virtual machines typically billed?", "options": ["A single flat annual fee regardless of usage", "Cloud resources are always free", "A one-time payment when the resource is created", "By the hour or by usage, accumulating cost as long as the resource is running"], "correct_index": 3, "explanation": "Most cloud resources are billed based on time running or actual usage, meaning idle but running resources still accumulate charges."},
                {"question": "What is the purpose of setting up a budget alert?", "options": ["To receive a notification (like email) when spending approaches or exceeds a set threshold", "To automatically delete your cloud account", "Budget alerts prevent all cloud services from working", "To increase your monthly bill automatically"], "correct_index": 0, "explanation": "Budget alerts notify you as spending approaches configured thresholds, helping catch runaway costs before they become a large surprise bill."},
                {"question": "What habit helps prevent unexpected cloud bills from forgotten resources?", "options": ["Never checking your cloud account after setup", "Always leaving every resource running indefinitely", "Stopping or terminating unused VMs and deleting unused resources when a session is done", "Disabling billing alerts to avoid notifications"], "correct_index": 2, "explanation": "Regularly cleaning up unused running resources is the single most effective habit for avoiding unexpected charges from forgotten infrastructure."}
            ],
            "resources": [
                {"label": "AWS Billing and Cost Management", "url": "https://aws.amazon.com/aws-cost-management/"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Cloud Provider Deep Dive",
            "title": "Introduction to Infrastructure as Code with Terraform",
            "learning_objective": "By the end of this class, you will be able to explain what Infrastructure as Code is and write a simple Terraform configuration.",
            "duration_minutes": 30,
            "content_html": """<p>So far, you have created cloud resources by clicking through a web console. This does not scale for real teams and leaves no record of exactly how infrastructure was configured. Infrastructure as Code (IaC) solves this by defining infrastructure in version-controlled configuration files, and Terraform is the most widely used tool for it.</p><h2>Defining Infrastructure in Code</h2><pre><code># main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c101f26f147fa7fd"
  instance_type = "t2.micro"

  tags = {
    Name = "my-first-app-server"
  }
}</code></pre><h2>The Core Terraform Workflow</h2><pre><code>terraform init     # download required provider plugins
terraform plan      # preview exactly what will change
terraform apply     # create/update the actual infrastructure</code></pre><p>The <code>terraform plan</code> step is what makes this powerful: before anything is actually created, Terraform shows you exactly what it will add, change, or destroy, preventing the accidental clicks that cause real incidents in cloud consoles.</p><h2>Why This Matters for Your Career</h2><p>IaC skills, especially Terraform, are frequently listed in mid-level and senior DevOps job postings because it makes infrastructure reviewable, repeatable, and version-controlled just like application code, rather than living only in one person's memory of console clicks.</p>""",
            "key_concepts": ["Infrastructure as Code (IaC)", "Terraform", "terraform init/plan/apply", "declarative infrastructure"],
            "practical_exercise": {
                "title": "Write a Terraform Configuration for a VM",
                "instructions": "Install Terraform locally, write a main.tf file that defines a free-tier virtual machine on your chosen cloud provider, and run terraform init and terraform plan to preview the resource it would create (you do not need to actually apply it if you want to avoid extra cost, but you may if comfortable). Submit your main.tf file and a screenshot of the terraform plan output."
            },
            "quiz": [
                {"question": "What is Infrastructure as Code (IaC)?", "options": ["Defining and managing infrastructure using version-controlled configuration files instead of manual console clicks", "Writing application business logic", "A type of database", "A cloud provider's name"], "correct_index": 0, "explanation": "IaC means describing infrastructure (servers, networks, etc) in code, making it reviewable, repeatable, and version-controlled like application code."},
                {"question": "What does 'terraform plan' do?", "options": ["It immediately creates the infrastructure with no preview", "It previews exactly what changes Terraform would make, without applying them", "It deletes all existing infrastructure", "It only works after infrastructure is already created"], "correct_index": 1, "explanation": "terraform plan shows a preview of additions, changes, and deletions before anything is actually applied, letting you review changes safely."},
                {"question": "Why do DevOps job postings often value Terraform or similar IaC tools?", "options": ["They have no real workplace relevance", "Terraform replaces the need for cloud providers entirely", "IaC makes infrastructure changes reviewable, repeatable, and documented in code rather than relying on manual console actions", "IaC tools are only used for hobby projects"], "correct_index": 2, "explanation": "IaC tools bring the same review, versioning, and repeatability benefits to infrastructure that version control brings to application code, which real teams rely on."}
            ],
            "resources": [
                {"label": "Terraform Documentation", "url": "https://developer.hashicorp.com/terraform/docs"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Cloud Provider Deep Dive",
            "title": "What Cloud and DevOps Job Postings and Interviews Actually Look For",
            "learning_objective": "By the end of this class, you will be able to identify the core skills cloud/DevOps job postings ask for and prepare interview talking points.",
            "duration_minutes": 25,
            "content_html": """<p>You now have real, hands-on experience with nearly every core building block of a cloud/DevOps role. Today is about translating that experience into language that matches what employers actually screen for, since technical skill alone does not guarantee it gets recognized in a resume or interview.</p><h2>What Junior Cloud/DevOps Postings Commonly Require</h2><p>Real Nigerian and remote job postings for junior cloud or DevOps roles typically list: Linux fundamentals, Docker/containerization, at least one cloud provider (AWS is most common), CI/CD experience (often specifically GitHub Actions or Jenkins), and basic scripting. Notice you have hands-on experience with every one of these from this track alone.</p><h2>A Common Interview Question</h2><p><strong>"Walk me through what happens from the moment a developer pushes code to it being live in production."</strong> A strong answer references exactly what you built in weeks two and three: push triggers CI (tests run), then a build step (Docker image built and pushed to a registry), then a deploy step (image pulled and run on the server), with monitoring confirming it is healthy afterward.</p><h2>Preparing Your Talking Points</h2><p>For your work this month, be ready to explain in two sentences: what your CI/CD pipeline automates, and one specific incident or bug you diagnosed and fixed (referencing Day 15 or Day 20). Concrete stories like this are what separate a candidate who "knows the theory" from one who has actually done the work.</p>""",
            "key_concepts": ["junior cloud/DevOps job requirements", "explaining a deployment pipeline end to end", "common interview questions", "concrete incident stories"],
            "practical_exercise": {
                "title": "Find and Analyze a Real Job Posting",
                "instructions": "Search for one real junior or entry-level cloud engineer or DevOps engineer job posting (Nigerian or remote), and list every technical requirement it mentions. For each requirement, note which specific day or project from this track already demonstrates it. Submit the job posting link/text and your requirement-by-requirement mapping."
            },
            "quiz": [
                {"question": "Which cloud provider is most commonly referenced in junior cloud/DevOps job postings?", "options": ["There is no common provider mentioned", "AWS", "A provider not covered in this track", "Only private, on-premises servers"], "correct_index": 1, "explanation": "AWS is the most widely referenced cloud provider in junior-level cloud and DevOps job postings, though GCP and Azure are also common."},
                {"question": "In the sample interview question about code going from push to production, what is the correct high-level order of steps?", "options": ["Push triggers CI (tests), then build (image built and pushed), then deploy (image pulled and run), then monitoring confirms health", "Deploy, then test, then build", "Monitoring first, then push, then nothing else happens", "There is no meaningful order, all steps happen simultaneously with no dependency"], "correct_index": 0, "explanation": "The standard CI/CD flow is: push triggers tests, then a build step produces and stores an artifact, then a deploy step runs it, followed by monitoring to confirm health."},
                {"question": "What kind of story is most convincing evidence of real hands-on skill in an interview?", "options": ["Reciting a dictionary definition of DevOps", "Listing tool names with no further explanation", "A specific incident or bug you personally diagnosed and fixed, with concrete details", "Avoiding any mention of past mistakes or bugs"], "correct_index": 2, "explanation": "Concrete, specific stories about real problems solved demonstrate hands-on experience far more convincingly than reciting definitions or tool names alone."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Planning Your Final Project: Application, Architecture, and Scope",
            "learning_objective": "By the end of this class, you will be able to write a scoped project plan defining your final application, its architecture, and its deployment pipeline.",
            "duration_minutes": 30,
            "content_html": """<p>Just like scope kills mobile or web projects, it kills cloud projects too, except here the risk is compounded by cloud costs and infrastructure complexity. Today is entirely about planning your final project properly, before touching any infrastructure for the capstone itself.</p><h2>Choosing and Scoping Your Application</h2><p>Pick a simple real application to deploy, a small API, a basic blog platform, or a small web app you have already built in an earlier track. It does not need new features; the point of this project is demonstrating operational skill, not building complex new functionality.</p><pre><code>App: Simple Notes API
Purpose: A small REST API for creating and retrieving text notes
Deployment target: A cloud VM (or Render/Railway if avoiding raw VM costs)
Pipeline: GitHub Actions -> test -> build Docker image -> deploy
Monitoring: /health endpoint + free uptime monitor with email alerts</code></pre><h2>Sketching Your Architecture</h2><p>Before building, sketch (even as a simple text diagram) how the pieces connect: user, load balancer or direct connection, application container, database, and monitoring service. This becomes the basis of the architecture documentation your final project rubric requires.</p><pre><code>User -&gt; DNS -&gt; Cloud VM (Docker container: app)
                    |
                    v
              Managed Database
                    ^
                    |
         Uptime Monitor (checks /health)</code></pre><p>This plan is your real spec for Day 30's execution, so treat it as a genuine document, not a rough note.</p>""",
            "key_concepts": ["project scoping", "architecture diagramming", "pipeline planning", "monitoring planning"],
            "practical_exercise": {
                "title": "Write Your Final Project Spec",
                "instructions": "Write a one-page spec for your final project including: the application you will deploy and its purpose, your deployment target, your planned CI/CD pipeline steps, your monitoring approach, and a simple text or drawn architecture diagram showing how the pieces connect. Submit this spec as your plan for the final project."
            },
            "quiz": [
                {"question": "Why does this lesson recommend deploying an application you have already built, rather than building something new?", "options": ["The final project is meant to demonstrate operational skill (deployment, CI/CD, monitoring), not new application development", "Building something new is always required", "Reusing an old project is against the rules", "It has no bearing on scope or risk"], "correct_index": 0, "explanation": "Since the capstone tests deployment and operations skills, reusing an already-built application reduces unnecessary risk and keeps focus on the actual grading criteria."},
                {"question": "What should a final project architecture sketch typically include?", "options": ["Only the application's color scheme", "How key pieces connect: user traffic, the application, the database, and monitoring", "A list of every commit made during the course", "The developer's personal daily schedule"], "correct_index": 1, "explanation": "An architecture diagram should show the real components and how they connect, forming the basis of the documentation the final project rubric requires."},
                {"question": "Why is planning the deployment pipeline steps in advance important for a cloud/DevOps capstone?", "options": ["It is not important and can be skipped", "Pipelines cannot be planned in advance", "Planning only matters for the application code, not infrastructure", "It ensures Day 30 begins with execution against a clear plan rather than open-ended research under time pressure"], "correct_index": 3, "explanation": "A clear pipeline and monitoring plan means the final build day can focus on executing a known plan rather than researching decisions from scratch."}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Provisioning and Securing Your Final Project's Infrastructure",
            "learning_objective": "By the end of this class, you will be able to provision and correctly secure the cloud infrastructure your final project will run on.",
            "duration_minutes": 30,
            "content_html": """<p>Before building your final project's pipeline, the underlying infrastructure needs to actually exist and be secured correctly. Getting this right today prevents scrambling to fix security group misconfigurations or missing databases while also trying to build a pipeline on Day 30.</p><h2>Provisioning Your Target Infrastructure</h2><p>Based on your Day 26 plan, provision what you actually need: a cloud VM (as in week one) if deploying via Docker directly, or an account with a platform like Render or Railway if you are avoiding raw VM management, plus a managed database if your app needs one (Day 22).</p><pre><code># Checklist before moving on:
[ ] VM launched (or platform account created) and reachable via SSH/dashboard
[ ] Docker installed on the VM (if using a raw VM)
[ ] Security group / firewall allows only necessary ports (80/443, and SSH from your IP only)
[ ] Managed database provisioned, if needed, with connection string saved securely</code></pre><h2>Locking Down Access</h2><p>Restrict SSH access in your security group to only your own IP address rather than 0.0.0.0/0 (anywhere), a simple change that meaningfully reduces your attack surface, and exactly the kind of default-secure configuration real teams require.</p><pre><code># Instead of allowing SSH from anywhere:
Allow inbound TCP 22 from 0.0.0.0/0     # risky

# Restrict it to your own IP:
Allow inbound TCP 22 from 105.112.xx.xx/32   # your IP only</code></pre>""",
            "key_concepts": ["infrastructure provisioning checklist", "SSH access restriction", "security group hardening", "pre-deployment readiness"],
            "practical_exercise": {
                "title": "Provision and Secure Your Final Project Infrastructure",
                "instructions": "Provision the cloud infrastructure your Day 26 plan requires (VM or platform account, plus a database if needed), and restrict SSH access in your security group/firewall to only your own current IP address instead of leaving it open to everyone. Submit a screenshot of your provisioned infrastructure and your security group/firewall rules showing the restricted SSH access."
            },
            "quiz": [
                {"question": "Why should infrastructure be provisioned and checked before starting to build the deployment pipeline?", "options": ["It does not matter what order things happen in", "To avoid scrambling to fix missing infrastructure or misconfigurations while also trying to build the pipeline under time pressure", "Pipelines can be built without any infrastructure existing", "Infrastructure never needs to exist before a pipeline runs"], "correct_index": 1, "explanation": "Having infrastructure ready and verified in advance avoids compounding problems (missing resources plus pipeline bugs) during the final, time-limited build."},
                {"question": "Why is restricting SSH access to your own IP address instead of 0.0.0.0/0 recommended?", "options": ["It has no security benefit", "0.0.0.0/0 is required for SSH to function at all", "It meaningfully reduces the attack surface by preventing SSH connection attempts from anywhere on the internet", "Restricting SSH access always breaks the connection entirely"], "correct_index": 2, "explanation": "Allowing SSH from anywhere (0.0.0.0/0) exposes the server to constant automated attack attempts; restricting it to your own IP significantly reduces this risk."},
                {"question": "What should be included in a pre-deployment infrastructure checklist according to this lesson?", "options": ["Confirming the VM/platform is reachable, Docker is installed if needed, ports are correctly restricted, and any database is provisioned", "Only the application's UI colors", "A list of unrelated personal tasks", "Nothing, checklists are unnecessary for this kind of project"], "correct_index": 0, "explanation": "A proper checklist confirms the actual infrastructure pieces (compute, Docker, network rules, database) are ready before pipeline work begins."}
            ],
            "resources": [
                {"label": "AWS Security Groups", "url": "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Documenting Architecture and Writing an Operations README",
            "learning_objective": "By the end of this class, you will be able to write clear architecture documentation and an operations README for a deployed system.",
            "duration_minutes": 25,
            "content_html": """<p>A working system nobody else can understand or operate is a liability, not an asset, to a real team, and it is one of the four explicit grading criteria for your final project. Documentation is part of the deliverable, not an afterthought squeezed in at the end.</p><h2>What Architecture Documentation Should Cover</h2><pre><code># Architecture

## Overview
A REST API for managing notes, deployed as a Docker container on
an AWS EC2 instance, backed by a managed Postgres database.

## Diagram
User -&gt; HTTPS -&gt; EC2 (Docker: notes-api) -&gt; RDS Postgres

## Components
- notes-api: Node.js/Express app, containerized with Docker
- Database: AWS RDS Postgres (managed, automated backups)
- CI/CD: GitHub Actions (test -&gt; build -&gt; push -&gt; deploy on push to main)
- Monitoring: /health endpoint checked every 5 min by UptimeRobot</code></pre><h2>What an Operations README Should Cover</h2><p>Beyond architecture, document how to actually operate the system: how to deploy a change, how to check logs, how to roll back, and how monitoring alerts work. This is written for "future you," or a teammate, at 2am during an incident, not for someone reading casually.</p><pre><code>## Deploying a Change
Push to main; GitHub Actions handles test, build, and deploy automatically.

## Checking Logs
ssh -i key.pem ubuntu@&lt;ip&gt; && docker logs --tail 100 notes-api

## Rolling Back
docker pull yourusername/notes-api:&lt;previous-tag&gt; && ...</code></pre>""",
            "key_concepts": ["architecture documentation", "operations README", "documenting deploy/rollback steps", "writing for incident response"],
            "practical_exercise": {
                "title": "Write Architecture and Operations Documentation",
                "instructions": "Write an ARCHITECTURE.md covering your system's components, a simple diagram, and how they connect, plus an operations section (or separate file) covering exactly how to deploy a change, check logs, and roll back. Base it on your actual final project plan from Day 26-27. Submit both documents."
            },
            "quiz": [
                {"question": "Why is documentation considered part of the final project deliverable rather than an afterthought?", "options": ["It is one of the explicit grading criteria, and a working system nobody can understand is a liability to a real team", "Documentation is optional and does not affect grading", "Documentation replaces the need for the app to actually work", "Only large companies require documentation"], "correct_index": 0, "explanation": "Architecture and operational documentation is explicitly part of the final project rubric and reflects a real professional expectation, not an optional extra."},
                {"question": "Who is operations documentation like a deploy/rollback guide primarily written for?", "options": ["No one, it is never actually read", "Only the original author, and only immediately after writing it", "Search engines, for SEO purposes", "Future you or a teammate who needs to operate or fix the system quickly, possibly during an incident"], "correct_index": 3, "explanation": "Operations documentation should be written clearly enough for someone (including your future self) to follow quickly under pressure, such as during an outage."},
                {"question": "What should be included in a system's architecture documentation?", "options": ["Only the programming language used", "The system's components, how they connect, and a simple diagram", "A list of unrelated personal notes", "The developer's resume"], "correct_index": 1, "explanation": "Architecture documentation should clearly describe the system's components and their relationships, typically supported by a simple diagram."}
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Final Infrastructure and Pipeline Review Before You Ship",
            "learning_objective": "By the end of this class, you will be able to review a deployment pipeline and infrastructure setup for security, reliability, and cleanliness before final submission.",
            "duration_minutes": 25,
            "content_html": """<p>The day before you execute your final build is the right time to review your habits against a real checklist, applying everything from this track, security, monitoring, and clean pipeline practices, one more time before it matters most.</p><h2>A Practical Pre-Ship Checklist</h2><ul><li>No secrets hardcoded anywhere in code or committed to Git (Day 19)</li><li>SSH restricted to your own IP, not open to everyone (Day 27)</li><li>Container has a restart policy set (Day 10)</li><li>CI/CD pipeline's test step actually fails on broken code, not just always passing (Day 12-13)</li><li>Health check endpoint returns correctly, and monitoring alerts are actually configured and tested (Day 16)</li><li>Budget alert is set on your cloud account (Day 23)</li></ul><h2>Testing Your Pipeline End to End One More Time</h2><p>Push a trivial, harmless change through your full pipeline right now and confirm every stage, test, build, push, deploy, still works cleanly, before you are relying on it for your actual final project tomorrow.</p><pre><code># A safe trivial test: update a comment or a version string
git commit -am "chore: verify pipeline before final project"
git push origin main
# Watch the Actions tab: test -&gt; build -&gt; push -&gt; deploy, all green</code></pre><h2>Why This Habit Matters</h2><p>Reviewing your own infrastructure and pipeline against a checklist, rather than assuming it is fine, is exactly the discipline that separates reliable operators from those who get paged at 3am for a preventable mistake.</p>""",
            "key_concepts": ["pre-ship security checklist", "pipeline dry-run", "reliability review", "operational discipline"],
            "practical_exercise": {
                "title": "Run a Full Pipeline and Infrastructure Review",
                "instructions": "Go through the full pre-ship checklist against your provisioned infrastructure and pipeline, fixing anything that fails, then push one trivial change through the entire pipeline to confirm every stage still works end to end. Submit a before/after list of every specific issue you found and fixed, plus a screenshot of the fully green pipeline run."
            },
            "quiz": [
                {"question": "Why should you push a trivial change through the full pipeline the day before final project execution?", "options": ["It serves no real purpose", "Trivial changes are not allowed in CI/CD pipelines", "To confirm every stage of the pipeline still works cleanly before relying on it for the actual final project", "It permanently disables the pipeline"], "correct_index": 2, "explanation": "A low-risk dry run confirms the pipeline is genuinely working end to end before depending on it under the time pressure of the final build day."},
                {"question": "According to the pre-ship checklist, what should be true about a CI/CD pipeline's test step?", "options": ["It should actually fail when the code is genuinely broken, not just always report success", "It should always pass regardless of code changes", "Test steps are optional and can be skipped for the final project", "It should only run once, ever"], "correct_index": 0, "explanation": "A test step that always passes regardless of actual code correctness provides false confidence; it must genuinely catch broken code to be useful."},
                {"question": "What does reviewing infrastructure and pipelines against a checklist before shipping help prevent?", "options": ["It has no effect on reliability", "Preventable mistakes, like open SSH access or missing restart policies, that could otherwise cause real incidents", "It only helps with visual design issues", "It replaces the need for monitoring entirely"], "correct_index": 1, "explanation": "A structured review catches known, preventable issues (like overly open access or missing safeguards) before they can cause a real incident."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Capstone Preparation and Delivery",
            "title": "Deploying and Operating Your Production-Style Cloud Application",
            "learning_objective": "By the end of this class, you will be able to execute your planned final project into a live, monitored, CI/CD-deployed cloud application.",
            "duration_minutes": 40,
            "content_html": """<p>Today you execute the plan you built over the last several days into your final project: <strong>Deploy and Operate a Production-Style Cloud Application</strong>. This is the single deliverable that proves everything you learned across this track, and it should look and operate like a real, professionally run system.</p><h2>Executing Against Your Spec</h2><p>Return to your Day 26 spec, Day 27 provisioned infrastructure, and Day 28 documentation draft, and now build the real thing: containerize your app with Docker (week two), wire up a full GitHub Actions pipeline that tests, builds, pushes, and deploys on every push to main (week three), add your health check endpoint and connect uptime monitoring with alerting (Day 16), and finalize your ARCHITECTURE.md and operations README with the real, final details.</p><pre><code>Deploy checklist for today:
[ ] App containerized and running via CI/CD-deployed image
[ ] Full pipeline: test -&gt; build -&gt; push -&gt; deploy, triggered by git push
[ ] /health endpoint live, uptime monitor configured and alerting
[ ] ARCHITECTURE.md finalized with real diagram and component list
[ ] Operations README finalized with real deploy/logs/rollback commands</code></pre><h2>Proving It Actually Works</h2><p>Before considering this done, prove each piece genuinely functions: push a real change and watch it deploy automatically, temporarily break the health check to confirm your monitor actually alerts you, and read through your own documentation as if you were a stranger seeing this system for the first time.</p><p>By the end of today, you should have a live application running on real cloud infrastructure, a working CI/CD pipeline, active monitoring, and documentation, a complete, demoable capstone ready for your portfolio.</p>""",
            "key_concepts": ["final project execution", "applying the full pipeline learned", "verifying monitoring works", "portfolio-ready delivery"],
            "practical_exercise": {
                "title": "Start and Build Your Final Project: Deploy and Operate a Production-Style Cloud Application",
                "instructions": "This IS the start of your final project. Using your Day 26 spec, Day 27 infrastructure, and Day 28 documentation draft, begin building your final project now: containerize your app, wire up the full test-build-push-deploy GitHub Actions pipeline, connect health-check monitoring with real alerting, and finalize your architecture and operations documentation. Submit your in-progress or completed project repository link, a screenshot of a successful full pipeline run, a screenshot proving your monitoring alert actually fired during a test, and your finalized documentation files."
            },
            "quiz": [
                {"question": "What four elements does the final project require according to its description?", "options": ["Only a working application with no other requirements", "A Dockerized app deployed to the cloud, a CI/CD pipeline, monitoring/health checks, and documented architecture", "Only a CI/CD pipeline with no deployment", "A mobile app instead of a cloud deployment"], "correct_index": 1, "explanation": "The final project explicitly requires cloud deployment with containerization, an automated CI/CD pipeline, monitoring/alerting, and documented architecture."},
                {"question": "Why should you temporarily break the health check during final testing rather than just trusting it is configured correctly?", "options": ["It is unnecessary since configuration is always correct", "Breaking the health check is required by the cloud provider", "This step has no relationship to monitoring", "To prove the monitoring alert actually fires in practice, not just that it is theoretically configured"], "correct_index": 3, "explanation": "Actually triggering a failure and confirming the alert fires proves the monitoring setup genuinely works, rather than assuming it does based on configuration alone."},
                {"question": "What should trigger the full deployment pipeline for the final project once it is complete?", "options": ["A manual SSH session run by hand every time", "Restarting the cloud provider's dashboard", "A git push to the main branch", "Editing the ARCHITECTURE.md file only"], "correct_index": 2, "explanation": "The whole point of the CI/CD pipeline built across this track is that a single git push to main triggers the entire test-build-push-deploy sequence automatically."}
            ],
            "resources": [
                {"label": "GitHub Actions", "url": "https://github.com/features/actions"},
                {"label": "Docker Documentation", "url": "https://docs.docker.com/get-started/"}
            ]
        }
    ]
}
