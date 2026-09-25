"""Seed data for the Cybersecurity 30-Day Skill Class."""

SKILL = {
    "slug": "cybersecurity",
    "name": "Cybersecurity",
    "tagline": "Learn to think like an attacker, defend like a professional, and prove it with a real vulnerability assessment report.",
    "description": "Cybersecurity is one of the fastest-growing tech fields in Africa, with banks, fintechs, telcos, and government agencies all short on qualified defenders. This track takes you from zero technical background to running a legal penetration test on a practice target and writing the kind of report a client or employer actually pays for. You will learn networking, Linux, common attack techniques, and how to communicate findings the way a junior security analyst is expected to.",
    "level": "beginner",
    "estimated_hours": 65,
    "course_title": "30-Day Cybersecurity Career Track",
    "course_description": "After 30 days, a student can set up a legal home lab, use industry-standard tools to find common vulnerabilities in a practice environment, and produce a professional security assessment report with severity ratings and remediation advice.",
    "final_project": {
        "title": "Vulnerability Assessment and Security Report",
        "description": "Using a legal, deliberately-vulnerable practice environment such as a TryHackMe or Hack The Box room, or a local vulnerable VM like Metasploitable or OWASP Juice Shop, perform a structured vulnerability assessment. You must enumerate the target, identify at least five real vulnerabilities across different categories, confirm each finding with evidence such as screenshots or command output, and rate each one using CVSS-style severity. Then write a professional security report aimed at a non-technical business stakeholder and a technical remediation appendix aimed at the engineering team. The report is the deliverable that goes in your portfolio and gets shown to employers or clients.",
        "difficulty": "advanced",
        "estimated_hours": 10,
        "skills_demonstrated": ["Vulnerability assessment", "Nmap and enumeration", "Risk rating with CVSS", "Technical report writing", "Remediation planning", "Ethical hacking methodology"],
        "rubric": [
            {"name": "Depth and accuracy of technical findings", "max_points": 30},
            {"name": "Correct use of tools and methodology", "max_points": 30},
            {"name": "Quality and clarity of the written report", "max_points": 25},
            {"name": "Practicality of remediation recommendations", "max_points": 15}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Security Foundations and Your Lab",
            "title": "How Attackers Actually Get In — the CIA Triad in Practice",
            "learning_objective": "By the end of this class, you will be able to explain the CIA triad and use it to classify real-world security incidents by which property was broken.",
            "duration_minutes": 25,
            "content_html": "<p>Every security job, from bank SOC analyst to freelance penetration tester, comes back to one question: what is actually at risk when a system is attacked? Employers do not hire people who can only recite tool names. They hire people who can look at an incident and say exactly what broke and why it matters to the business.</p><h2>The CIA Triad</h2><p>Confidentiality means only authorized people can read data. Integrity means data cannot be changed without detection. Availability means systems stay up when legitimate users need them. Nearly every attack you will study this month breaks one or more of these three properties. A data breach at a Nigerian fintech breaks confidentiality when customer BVNs leak. A website defacement breaks integrity when an attacker changes the homepage content. A distributed denial-of-service attack against a bank's online banking portal breaks availability when real customers cannot log in.</p><h2>Worked Example</h2><p>In 2023, several African banks reported SIM-swap fraud where attackers convinced telecom staff to reassign a victim's phone number, then used SMS one-time passwords to drain accounts. Confidentiality broke first, when the attacker obtained enough personal data to impersonate the victim. Then integrity broke, when unauthorized transactions altered account balances. As a security professional, your job is to identify which control could have stopped each stage, not just describe the attack.</p><p>Today, install nothing yet. Instead, practice thinking in these three categories, because you will use them every day for the rest of this course.</p>",
            "key_concepts": ["Confidentiality", "Integrity", "Availability", "CIA triad", "Security incident classification"],
            "practical_exercise": {
                "title": "Classify Three Real Incidents",
                "instructions": "Find three real cybersecurity incident reports from the last two years (news articles about breaches at African or global companies are fine). For each one, write two to three sentences identifying which part of the CIA triad was broken and why. Submit your three write-ups as a single document."
            },
            "quiz": [
                {"question": "Which part of the CIA triad is broken when a website is taken offline by a flood of fake traffic?", "options": ["Confidentiality", "Integrity", "Availability", "Authentication"], "correct_index": 2, "explanation": "A denial-of-service attack prevents legitimate access, which is an availability failure."},
                {"question": "A hacker changes the price listed for products on an e-commerce site without permission. Which property is violated?", "options": ["Integrity", "Confidentiality", "Availability", "Non-repudiation"], "correct_index": 0, "explanation": "Unauthorized modification of data is an integrity violation, even if no data was stolen."},
                {"question": "Why do employers care about the CIA triad instead of just tool names?", "options": ["It is required by law in every country", "It helps communicate business impact and prioritize fixes", "It is the only framework tested in interviews", "It replaces the need for technical skills"], "correct_index": 1, "explanation": "Framing findings in terms of business impact is what separates a junior analyst from someone who cannot explain why a vulnerability matters."}
            ],
            "resources": [
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Security Foundations and Your Lab",
            "title": "Building Your Legal Home Lab with VirtualBox and Kali Linux",
            "learning_objective": "By the end of this class, you will be able to install a virtual machine running Kali Linux inside an isolated lab network on your own computer.",
            "duration_minutes": 35,
            "content_html": "<p>Nobody gets hired in security without hands-on evidence, and you cannot practice attack techniques on real websites without breaking the law. The solution every professional uses is a home lab: virtual machines that only exist on your own laptop, isolated from the internet, where you can legally attack practice targets you control.</p><h2>Why Kali Linux and VirtualBox</h2><p>VirtualBox is free software that lets you run an entire operating system inside a window on your existing computer. Kali Linux is a Linux distribution built specifically for security testing, preloaded with tools like Nmap, Burp Suite, and Metasploit that you will use throughout this course. Running Kali inside VirtualBox means you can experiment freely, break things, and reset to a clean snapshot in minutes, all without touching your main operating system.</p><h2>Worked Example</h2><p>A typical beginner lab setup looks like this: your host laptop runs Windows or macOS as normal. Inside VirtualBox, you create one virtual machine for Kali Linux, the attacker machine, and later a second virtual machine for a deliberately vulnerable target like Metasploitable. Both virtual machines are set to a Host-Only or Internal network adapter, meaning they can talk to each other but cannot reach the public internet or your home network. This isolation is what makes practicing attacks legal and safe.</p><p>Take your time on this step. A broken lab environment is the single biggest reason beginners give up in week one.</p>",
            "key_concepts": ["Virtual machine", "VirtualBox", "Kali Linux", "Isolated lab network", "Host-only networking"],
            "practical_exercise": {
                "title": "Set Up Your Lab",
                "instructions": "Download and install VirtualBox, then download the official Kali Linux virtual machine image and import it. Configure its network adapter to Host-Only mode. Take a screenshot showing Kali Linux booted and logged in, and write two sentences describing what Host-Only networking does and why you configured it that way."
            },
            "quiz": [
                {"question": "What is the main reason security learners use virtual machines instead of testing on real websites?", "options": ["Virtual machines run faster", "It is illegal to test systems you do not own or have permission to test", "Real websites do not have vulnerabilities", "Virtual machines are required by ISPs"], "correct_index": 1, "explanation": "Unauthorized testing against systems you do not own or lack written permission for is illegal in most countries, so a private lab is the safe and legal way to practice."},
                {"question": "What does setting a virtual machine's network adapter to Host-Only accomplish?", "options": ["It gives the VM a public IP address", "It isolates the VM so it can only talk to other VMs on the same host, not the internet", "It increases the VM's processing speed", "It automatically encrypts all VM traffic"], "correct_index": 1, "explanation": "Host-Only networking keeps lab traffic contained to your own machine, which is essential for safe, legal practice."},
                {"question": "Why is Kali Linux commonly used for security work?", "options": ["It is the only operating system that can run a web browser", "It comes preloaded with security testing tools like Nmap and Burp Suite", "It is required by all employers", "It cannot be run inside a virtual machine"], "correct_index": 1, "explanation": "Kali Linux bundles the standard toolset security professionals use, saving setup time."}
            ],
            "resources": [
                {"label": "Kali Linux", "url": "https://www.kali.org"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Security Foundations and Your Lab",
            "title": "Networking Fundamentals Every Security Analyst Needs",
            "learning_objective": "By the end of this class, you will be able to explain IP addresses, ports, and common protocols well enough to read a network scan result.",
            "duration_minutes": 30,
            "content_html": "<p>You cannot attack or defend what you do not understand, and almost every security tool you will use this month reports its findings in terms of IP addresses, ports, and protocols. Skipping networking basics is the number one reason beginners get lost during their first scan.</p><h2>The Building Blocks</h2><p>An IP address identifies a device on a network, similar to a street address. A port is a numbered doorway on that device, with specific services listening on specific ports, such as web servers on port 80 or 443, and SSH remote login on port 22. A protocol is the agreed-upon language used over a connection, such as HTTP for web traffic or DNS for translating domain names into IP addresses. When a security tool reports that port 3306 is open, it usually means a MySQL database is reachable, which is immediately interesting to an attacker or auditor.</p><h2>Worked Example</h2><p>Imagine a scan of a small company server returns three open ports: 22, 80, and 3389. Port 22 suggests SSH remote administration is exposed. Port 80 suggests an unencrypted web server. Port 3389 suggests Windows Remote Desktop is reachable. A junior analyst who understands these numbers immediately knows to check whether SSH allows weak passwords, whether the web server should be forced to HTTPS, and whether Remote Desktop should even be exposed at all. That is the value networking knowledge adds to a scan result.</p>",
            "key_concepts": ["IP address", "Port", "Protocol", "TCP and UDP", "Common service ports"],
            "practical_exercise": {
                "title": "Map Ten Common Ports",
                "instructions": "Create a table listing ten common port numbers (for example 21, 22, 25, 53, 80, 110, 143, 443, 3306, 3389) with the service name that typically runs on each and one sentence on why that service being open might matter for security. Submit the table."
            },
            "quiz": [
                {"question": "What does an open port typically indicate on a scanned device?", "options": ["The device is turned off", "A service is actively listening for connections on that port", "The device has no operating system", "The port is permanently closed"], "correct_index": 1, "explanation": "An open port means something on the device is actively accepting connections, which is why scanners report it."},
                {"question": "Which port is most commonly associated with SSH remote administration?", "options": ["port 80", "port 443", "port 22", "port 25"], "correct_index": 2, "explanation": "Port 22 is the standard port for SSH."},
                {"question": "Why does a security analyst need to understand common ports and protocols?", "options": ["To design company logos", "To correctly interpret what a scan result actually exposes", "Because it is required for internet access", "To write marketing copy"], "correct_index": 1, "explanation": "Reading a scan meaningfully requires knowing what services typically run where."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Security Foundations and Your Lab",
            "title": "The Linux Command Line for Security Work",
            "learning_objective": "By the end of this class, you will be able to navigate the file system and run basic commands in the Kali Linux terminal.",
            "duration_minutes": 30,
            "content_html": "<p>Nearly every security tool you will touch this month, from Nmap to Metasploit to Hashcat, runs from a terminal, and most professional environments you will assess run Linux servers. Comfort with the command line is not optional for this career.</p><h2>Core Commands</h2><p>Start with navigation: pwd shows your current directory, ls lists files, and cd changes directory. Use cat to read a file's contents and man to read the manual for any command you do not understand. File permissions matter enormously in security, so learn chmod for changing permissions and sudo for running a command with administrator rights. Piping output from one command into another with the vertical bar symbol, and redirecting output to a file with the greater-than symbol, are patterns you will use constantly when saving scan results.</p><h2>Worked Example</h2><p>A common early workflow looks like this: you run an Nmap scan and save the output to a file with a redirect, then use cat to review it, then use grep to search that file for the word open so you only see the ports that matter. Each of these is a small command, but chained together they form the exact workflow a working analyst uses dozens of times a day. Muscle memory here will save you hours later in this course.</p>",
            "key_concepts": ["Terminal navigation", "File permissions", "chmod and sudo", "Piping and redirection", "grep filtering"],
            "practical_exercise": {
                "title": "Terminal Workflow Practice",
                "instructions": "In your Kali Linux terminal, create a folder called lab-notes, create a text file inside it listing five Linux commands and what each does, then use cat to print the file to the screen and grep to search it for one specific word. Paste the full terminal session, including the commands you typed, into your submission."
            },
            "quiz": [
                {"question": "Which command lists the files in the current directory in Linux?", "options": ["cd", "ls", "pwd", "rm"], "correct_index": 1, "explanation": "ls lists directory contents."},
                {"question": "What does the pipe symbol do when placed between two commands?", "options": ["It deletes the first command's output", "It sends the output of the first command as input to the second", "It runs both commands at the same time on separate cores", "It cancels the first command"], "correct_index": 1, "explanation": "Piping chains commands together so output flows from one into the next."},
                {"question": "Why is command-line comfort important for a security analyst specifically?", "options": ["Most professional security tools and target servers are operated through the terminal", "Graphical interfaces are banned in security work", "The terminal is only used for writing reports", "It has no practical importance"], "correct_index": 0, "explanation": "Security tooling and the servers being assessed are overwhelmingly terminal-driven, especially on Linux."}
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Security Foundations and Your Lab",
            "title": "Understanding the Cyber Kill Chain and MITRE ATT&CK",
            "learning_objective": "By the end of this class, you will be able to map a described attack scenario onto the stages of the Cyber Kill Chain.",
            "duration_minutes": 25,
            "content_html": "<p>When an employer asks you to describe how you would approach an assessment, they are testing whether you have a structured methodology or are just randomly poking at a target. The Cyber Kill Chain and the MITRE ATT&CK framework are the two most referenced structures in the industry, and interviewers expect you to know at least one well.</p><h2>The Kill Chain Stages</h2><p>The Cyber Kill Chain breaks an attack into stages: reconnaissance, weaponization, delivery, exploitation, installation, command and control, and actions on objectives. Reconnaissance is gathering information about a target. Delivery is getting a malicious payload to the target, for example through a phishing email. Exploitation is triggering a vulnerability. Installation is establishing persistence. Command and control is the attacker's remote channel back into the compromised system. Actions on objectives is the attacker actually achieving their goal, such as stealing data.</p><h2>Worked Example</h2><p>Consider a phishing attack against a university staff member. Reconnaissance is the attacker finding staff emails on the university website. Delivery is sending a fake IT-support email. Exploitation happens when the staff member clicks a malicious link and enters credentials. Installation might be a malicious browser extension. Command and control is the attacker's server receiving stolen session cookies. Actions on objectives is the attacker logging into the university's student records system. Breaking any single link in this chain, such as staff phishing awareness, stops the entire attack.</p>",
            "key_concepts": ["Cyber Kill Chain", "MITRE ATT&CK", "Reconnaissance", "Exploitation", "Command and control"],
            "practical_exercise": {
                "title": "Map an Attack to the Kill Chain",
                "instructions": "Write a short fictional but realistic scenario of an attack against a Nigerian business (bank, e-commerce store, or university). Then break your scenario into the seven Cyber Kill Chain stages, one to two sentences per stage, showing exactly what the attacker does at each point."
            },
            "quiz": [
                {"question": "In the Cyber Kill Chain, what happens during the reconnaissance stage?", "options": ["The attacker steals the final data", "The attacker gathers information about the target before attacking", "The attacker installs malware", "The attacker patches the vulnerability"], "correct_index": 1, "explanation": "Reconnaissance is the information-gathering stage that precedes any actual attack action."},
                {"question": "Which stage of the Kill Chain involves the attacker maintaining a remote connection to the compromised system?", "options": ["Delivery", "Weaponization", "Command and control", "Reconnaissance"], "correct_index": 2, "explanation": "Command and control is the channel an attacker uses to remotely control a compromised machine."},
                {"question": "Why do employers value candidates who know a structured attack framework?", "options": ["It proves they memorized a textbook", "It shows they can approach assessments methodically instead of randomly", "It is only relevant to malware authors", "Frameworks are not actually used in real jobs"], "correct_index": 1, "explanation": "Structured methodology is what makes an assessment repeatable, defensible, and complete."}
            ],
            "resources": [
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Reconnaissance and Scanning",
            "title": "Passwords, Hashes, and Why Encryption Is the Wrong Word",
            "learning_objective": "By the end of this class, you will be able to explain the difference between encryption and hashing and why passwords should always be hashed, not encrypted.",
            "duration_minutes": 25,
            "content_html": "<p>One of the most common mistakes junior developers and even some companies make is saying passwords are encrypted when they should be hashed. Getting this distinction right is a quick way to sound credible in an interview or a client report.</p><h2>Hashing vs Encryption</h2><p>Encryption is reversible: data is scrambled with a key, and the same or a related key can unscramble it back to the original. Hashing is one-way: a hash function takes input of any size and produces a fixed-size output that cannot be reversed back into the original input. A properly designed system never needs to see your original password again, it only needs to check that a new hash matches the stored hash, so passwords should always be hashed with a slow, salted algorithm such as bcrypt or Argon2, never encrypted and never hashed with a fast general-purpose function like plain MD5.</p><h2>Worked Example</h2><p>Suppose a database breach exposes a table of user passwords. If the system used strong salted bcrypt hashing, an attacker with the leaked hashes still has to guess each password individually and slowly, which can take an impractical amount of time for strong passwords. If the system instead stored passwords in plain text or with reversible encryption, every single account is immediately compromised the moment the database leaks. This single design decision is often the difference between a contained incident and a catastrophic breach.</p>",
            "key_concepts": ["Hashing", "Encryption", "Salting", "bcrypt and Argon2", "Password storage"],
            "practical_exercise": {
                "title": "Explain It to a Non-Technical Founder",
                "instructions": "Write a short explanation, no more than 200 words, that you could send to a non-technical startup founder explaining why their app should hash passwords with bcrypt instead of encrypting them, using a plain-language analogy rather than jargon."
            },
            "quiz": [
                {"question": "What is the key difference between hashing and encryption?", "options": ["Hashing is reversible, encryption is not", "Encryption is reversible with a key, hashing is designed to be one-way", "They are the same thing with different names", "Hashing only works on numbers"], "correct_index": 1, "explanation": "Encryption can be reversed with the correct key, while a good hash function cannot be reversed back to the original input."},
                {"question": "Why should passwords be hashed rather than encrypted?", "options": ["Hashing is faster to compute for attackers", "The system never needs to recover the original password, only verify it, so a one-way function is safer", "Encryption is illegal in most countries", "Hashing makes passwords visible to administrators"], "correct_index": 1, "explanation": "Since verification only requires comparing hashes, there is no legitimate need to ever reverse the stored value, making hashing the safer choice."},
                {"question": "What does salting a password hash protect against?", "options": ["Network outages", "Precomputed hash lookup attacks like rainbow tables", "Slow server response times", "SQL syntax errors"], "correct_index": 1, "explanation": "A unique salt per password defeats precomputed hash tables, forcing attackers to crack each password individually."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Reconnaissance and Scanning",
            "title": "Reconnaissance — Gathering Intel Without Touching the Target",
            "learning_objective": "By the end of this class, you will be able to perform passive reconnaissance on a target domain using only publicly available information.",
            "duration_minutes": 30,
            "content_html": "<p>Before any professional penetration test touches a target system, it starts with reconnaissance: gathering as much public information as possible without sending a single suspicious packet. This is also usually the very first phase listed in any signed scope of work, so understanding it is essential before you touch real tools.</p><h2>Passive vs Active Recon</h2><p>Passive reconnaissance never directly interacts with the target, it only uses information already public, such as WHOIS domain registration records, DNS records, job postings that reveal technology stacks, employee social media profiles, and search engine results. Active reconnaissance, which you will learn later, involves directly probing the target, such as scanning its ports. Skilled analysts always start passive because it carries zero risk of detection or accidental disruption.</p><h2>Worked Example</h2><p>Imagine you are assessing a fictional Nigerian e-commerce company with permission. Passive recon might reveal, through WHOIS, when the domain was registered and which registrar is used. DNS records might reveal a subdomain like mail.example.com or staging.example.com, hinting at a possibly less-secured test environment. A job posting for a PHP developer with WordPress experience tells you the likely technology stack before you have run a single scan. All of this is gathered without ever sending a packet directly at the company's live infrastructure.</p>",
            "key_concepts": ["Passive reconnaissance", "Active reconnaissance", "WHOIS", "DNS enumeration", "OSINT"],
            "practical_exercise": {
                "title": "Passive Recon on a Public Domain",
                "instructions": "Pick a well-known public company website you do not need explicit permission to look up information about (their WHOIS and public DNS records only, no scanning). Record what you can learn from WHOIS, public DNS records, and job postings. Write a short summary of what an attacker could infer about the company's technology from this alone, without touching the live systems."
            },
            "quiz": [
                {"question": "What distinguishes passive reconnaissance from active reconnaissance?", "options": ["Passive recon is illegal, active recon is legal", "Passive recon never directly interacts with the target, active recon does", "Passive recon requires expensive tools", "There is no meaningful difference"], "correct_index": 1, "explanation": "Passive recon relies entirely on already-public information, avoiding any direct contact with the target's systems."},
                {"question": "Which of these is an example of passive reconnaissance?", "options": ["Running a port scan against the target server", "Reading a company's public job postings for technology hints", "Sending exploit payloads to a web form", "Brute-forcing a login page"], "correct_index": 1, "explanation": "Reading public job postings gathers information without touching the target's systems."},
                {"question": "Why do professional penetration testers typically start with passive reconnaissance?", "options": ["It is required by antivirus software", "It carries no risk of detection or disruption to the target", "It is the fastest way to gain access", "It replaces the need for a signed scope of work"], "correct_index": 1, "explanation": "Passive recon is safe and low-risk, which is why it always comes before any direct interaction with the target."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Reconnaissance and Scanning",
            "title": "Scanning Networks with Nmap",
            "learning_objective": "By the end of this class, you will be able to run an Nmap scan against a lab target and interpret which ports and services are exposed.",
            "duration_minutes": 35,
            "content_html": "<p>Nmap is the single most widely used network scanning tool in the industry, and knowing it well is close to a baseline requirement for any junior security role. Today you move from passive recon into active scanning, but only against machines in your own isolated lab.</p><h2>Reading an Nmap Scan</h2><p>A basic scan such as nmap with a target IP checks the most common one thousand ports and reports each as open, closed, or filtered. Adding the -sV flag attempts to identify the exact software and version running on each open port, which is critical because specific versions have specific known vulnerabilities. Adding -A enables more aggressive detection including operating system fingerprinting. Every open port is a potential entry point, so a scan result is really a map of a target's attack surface.</p><h2>Worked Example</h2><p>Scanning a Metasploitable virtual machine, a deliberately vulnerable practice target, typically reveals dozens of open ports including old FTP, Telnet, and Samba services running outdated, known-vulnerable versions. A version scan might reveal vsftpd 2.3.4, which has a well-documented backdoor vulnerability. Simply reading the Nmap output and cross-referencing the version number against known vulnerability databases is often enough to identify a critical finding before you have even attempted exploitation.</p>",
            "key_concepts": ["Nmap", "Port scanning", "Service version detection", "Attack surface", "Scan flags"],
            "practical_exercise": {
                "title": "Scan Your Lab Target",
                "instructions": "In your isolated lab, run an Nmap scan with version detection against your Metasploitable or similar practice target's IP address. Save the full output to a text file. Write a short summary listing the open ports found, the service and version on each, and which one finding looks most interesting to investigate further."
            },
            "quiz": [
                {"question": "What does the -sV flag do in an Nmap scan?", "options": ["It scans all 65535 ports instead of the default set", "It attempts to detect the specific software and version running on open ports", "It disables logging", "It encrypts scan traffic"], "correct_index": 1, "explanation": "Version detection reveals exactly what software is listening, which is essential for identifying known vulnerabilities."},
                {"question": "Why is it important to only run Nmap scans against systems you own or have explicit permission to test?", "options": ["Nmap only works on your own network", "Unauthorized scanning can be illegal and is considered hostile activity", "Nmap cannot scan remote systems", "It has no legal implications"], "correct_index": 1, "explanation": "Scanning systems without authorization can violate computer misuse laws even if no damage is done."},
                {"question": "What does an open port on a scanned target generally represent from a security perspective?", "options": ["A guaranteed vulnerability", "A potential entry point that should be investigated", "A sign the machine is offline", "An error in the scan"], "correct_index": 1, "explanation": "An open port is not automatically a vulnerability, but it is a point of exposure worth investigating."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Reconnaissance and Scanning",
            "title": "Reading and Understanding Vulnerability Scan Reports",
            "learning_objective": "By the end of this class, you will be able to run an automated vulnerability scanner and interpret its severity ratings and findings.",
            "duration_minutes": 30,
            "content_html": "<p>Manually finding every vulnerability by hand does not scale, which is why professional assessments always pair manual testing with automated vulnerability scanners. Learning to read these reports critically, instead of blindly trusting them, is a core skill that separates a useful analyst from someone who just forwards a tool's raw output.</p><h2>How Scanners Rate Severity</h2><p>Tools like OpenVAS or Nessus compare a target's exposed services and versions against a database of known vulnerabilities, then assign a severity based on the Common Vulnerability Scoring System, or CVSS, typically ranging from low to critical. A critical finding usually means remote code execution is possible with little effort. A low finding might be an outdated software banner with no known exploit. Crucially, automated scanners produce false positives, findings that look real but are not actually exploitable in context, so every finding needs a human to verify it before it goes in a client report.</p><h2>Worked Example</h2><p>An automated scan against a lab web server might report a critical finding for an outdated version of a content management system with a known remote code execution vulnerability, alongside a low finding for a server banner revealing its software name. The critical finding deserves immediate manual verification and probably an actual proof-of-concept exploit attempt in your report. The low finding might simply go in an appendix as a minor hardening recommendation. Treating every finding as equally urgent wastes a client's time and damages your credibility.</p>",
            "key_concepts": ["Automated vulnerability scanning", "CVSS severity", "False positives", "Manual verification", "Vulnerability databases"],
            "practical_exercise": {
                "title": "Run and Triage a Vulnerability Scan",
                "instructions": "Run an automated vulnerability scan such as OpenVAS or Nikto against your isolated lab target. From the results, pick the three highest-severity findings and write one paragraph each explaining what the vulnerability is, why the severity rating makes sense, and what you would check manually to confirm it is real before including it in a report."
            },
            "quiz": [
                {"question": "What is a false positive in the context of a vulnerability scan?", "options": ["A finding that is confirmed and exploitable", "A finding the scanner reports that turns out not to be a real, exploitable issue", "A scan that fails to run", "A critical severity rating"], "correct_index": 1, "explanation": "False positives are inaccurate findings that require manual verification to rule out."},
                {"question": "What scoring system do most vulnerability scanners use to rate severity?", "options": ["CVSS", "HTTP status codes", "IP addressing scheme", "OSI model layers"], "correct_index": 0, "explanation": "The Common Vulnerability Scoring System, CVSS, is the industry standard for rating vulnerability severity."},
                {"question": "Why should a security analyst manually verify automated scan findings before reporting them?", "options": ["Manual verification is legally required in every country", "Automated scanners can produce false positives that would mislead the client", "Automated scanners are always wrong", "Reports are not allowed to reference tool output"], "correct_index": 1, "explanation": "Because scanners can misfire, human verification protects the credibility and accuracy of the final report."}
            ],
            "resources": []
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Reconnaissance and Scanning",
            "title": "Social Engineering and the Human Attack Surface",
            "learning_objective": "By the end of this class, you will be able to identify common social engineering techniques and design one defensive awareness recommendation against each.",
            "duration_minutes": 25,
            "content_html": "<p>Technical controls can be close to perfect and an organization can still be breached because a single employee was tricked. Social engineering exploits human psychology rather than software flaws, and it remains one of the most common ways real attackers gain initial access, which is why every professional assessment considers the human attack surface, not just servers and code.</p><h2>Common Techniques</h2><p>Phishing uses fraudulent emails to trick someone into clicking a malicious link or entering credentials on a fake page. Vishing does the same over a phone call, often impersonating IT support or a bank. Pretexting involves inventing a believable false scenario, such as posing as a new employee who forgot their badge, to gain physical or informational access. Baiting leaves an infected USB drive somewhere an employee is likely to find and plug it in out of curiosity.</p><h2>Worked Example</h2><p>A common Nigerian scenario involves an attacker calling a company's junior finance staff pretending to be the CEO traveling abroad, urgently requesting a wire transfer, often called CEO fraud or business email compromise when done by email. The pretext exploits urgency and hierarchy so the employee feels unable to say no or verify through normal channels. The correct defensive control is not a technical firewall rule, it is a documented policy requiring out-of-band verification, such as a phone call to a known number, before any financial transfer above a threshold, regardless of who is asking.</p>",
            "key_concepts": ["Social engineering", "Phishing", "Vishing", "Pretexting", "Business email compromise"],
            "practical_exercise": {
                "title": "Design an Awareness Recommendation",
                "instructions": "Choose two social engineering techniques covered today. For each, write a realistic short scenario targeting a Nigerian small business, then write one specific, actionable staff training or policy recommendation that would have prevented it. Submit both scenarios and recommendations."
            },
            "quiz": [
                {"question": "What is the defining feature of social engineering attacks?", "options": ["They exploit software bugs directly", "They exploit human psychology rather than technical vulnerabilities", "They only happen over email", "They require advanced coding skills"], "correct_index": 1, "explanation": "Social engineering targets people, using trust, urgency, or authority rather than a technical flaw."},
                {"question": "What is pretexting?", "options": ["Sending mass unsolicited emails", "Inventing a believable false scenario to manipulate a target into giving access or information", "Scanning a network for open ports", "Encrypting a victim's files for ransom"], "correct_index": 1, "explanation": "Pretexting relies on a fabricated but believable story to manipulate the target."},
                {"question": "Why is out-of-band verification an effective defense against CEO fraud scams?", "options": ["It slows down legitimate business so much that fraud becomes pointless", "It confirms a request through a separate trusted channel, defeating impersonation over a single compromised channel", "It requires no employee training", "It eliminates the need for any financial controls"], "correct_index": 1, "explanation": "Verifying urgent requests through a second, trusted channel breaks the impersonation even if the original email or call was convincing."}
            ],
            "resources": []
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Exploitation Fundamentals",
            "title": "Exploiting Your First Vulnerable Machine on TryHackMe",
            "learning_objective": "By the end of this class, you will be able to fully compromise a beginner-level vulnerable machine on a legal practice platform, from scan to root access.",
            "duration_minutes": 40,
            "content_html": "<p>Today you put together everything from weeks one and two: reconnaissance, scanning, and vulnerability research, into a full end-to-end compromise on a legal practice platform. This is the single most important skill milestone so far, because it is exactly the workflow you will repeat in your final capstone project.</p><h2>The Standard Workflow</h2><p>Start with an Nmap version scan to see what is exposed. Research each service version against a public vulnerability database to find a known exploit. Use a tool like Metasploit, or a manually downloaded exploit script, to attempt the exploit against your target. If successful, you gain a shell, a remote command-line session on the target machine. From there, explore the file system to find flag files, which practice platforms use to prove you actually achieved access, similar to how a real report needs evidence.</p><h2>Worked Example</h2><p>A classic beginner room might expose an outdated FTP server with anonymous login enabled. Logging in with the username anonymous and a blank password gives you access to files on the server, one of which might contain SSH credentials. Using those credentials to SSH into the machine gives you a full shell as a low-privilege user. This chain, misconfigured FTP leading to leaked credentials leading to SSH access, is a realistic pattern seen in real assessments, not just artificial practice scenarios.</p>",
            "key_concepts": ["End-to-end exploitation", "Shell access", "Anonymous FTP misconfiguration", "Credential chaining", "Practice platforms"],
            "practical_exercise": {
                "title": "Complete a Beginner Room",
                "instructions": "On TryHackMe or a similar legal practice platform, complete one beginner-rated room end to end. Document every step you took: the scan command and result, the vulnerability you identified, the exploit method used, and the final flag or evidence of access. Submit this as a mini walkthrough with screenshots or terminal output."
            },
            "quiz": [
                {"question": "What is a shell in the context of exploiting a machine?", "options": ["A graphical desktop environment", "A remote command-line session that lets you run commands on the target", "A type of firewall", "A password manager"], "correct_index": 1, "explanation": "A shell gives the attacker or tester a command-line interface to interact directly with the compromised machine."},
                {"question": "Why do practice platforms like TryHackMe use flag files?", "options": ["To slow down attackers", "To provide concrete proof that a specific level of access was actually achieved", "They are required by law", "To encrypt the target machine"], "correct_index": 1, "explanation": "Flags are unique strings that prove you genuinely reached a certain stage of compromise, similar to evidence in a real report."},
                {"question": "What made the anonymous FTP example in today's lesson exploitable?", "options": ["The FTP server was using strong encryption", "Anonymous login was enabled, allowing access without valid credentials", "The FTP server was completely offline", "The attacker used a zero-day exploit"], "correct_index": 1, "explanation": "Anonymous FTP access is a misconfiguration that allows anyone to log in without credentials, often exposing sensitive files."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Exploitation Fundamentals",
            "title": "Web App Basics — How HTTP Requests Become Attack Surface",
            "learning_objective": "By the end of this class, you will be able to inspect and modify a raw HTTP request to understand how web applications can be manipulated.",
            "duration_minutes": 30,
            "content_html": "<p>The majority of paid penetration testing and bug bounty work today targets web applications, not raw network services, because that is where most businesses now expose functionality. Understanding HTTP at a low level is the foundation for every web attack you will learn this week.</p><h2>Anatomy of an HTTP Request</h2><p>Every browser action generates an HTTP request containing a method such as GET or POST, a URL path, headers carrying metadata like cookies and content type, and sometimes a body carrying submitted form data. A web application decides what to do based entirely on this request. If that application trusts data in the request without properly validating it, an attacker who edits the raw request before it is sent can manipulate the application's behavior in ways the developers never intended.</p><h2>Worked Example</h2><p>Consider a simple request to view an invoice, such as a GET request to a path like /invoice?id=1042. If the server does not check that the logged-in user actually owns invoice 1042, an attacker can simply change the number in the URL to view other customers' invoices, a vulnerability called insecure direct object reference. This is not a complex exploit, it requires no special tool beyond a browser address bar, yet it is one of the most commonly found real-world vulnerabilities in production web applications.</p>",
            "key_concepts": ["HTTP request", "GET and POST methods", "Headers and cookies", "Insecure direct object reference", "Client-server trust"],
            "practical_exercise": {
                "title": "Inspect Requests with Browser DevTools",
                "instructions": "Open your browser's developer tools Network tab, visit a website you use regularly, and perform an action like logging in or searching. Find the actual HTTP request generated, and write down its method, URL, and at least two headers you observe. Explain in two to three sentences what would happen if an attacker could freely edit that request before it reached the server."
            },
            "quiz": [
                {"question": "What does an insecure direct object reference vulnerability typically allow an attacker to do?", "options": ["Crash the server permanently", "Access data belonging to other users by changing an identifier in the request", "Bypass network firewalls entirely", "Install malware on the client browser automatically"], "correct_index": 1, "explanation": "IDOR happens when an application fails to check ownership before returning data referenced by a user-controlled identifier."},
                {"question": "Which part of an HTTP request commonly carries session information like cookies?", "options": ["The URL path", "The headers", "The HTTP method", "The status code"], "correct_index": 1, "explanation": "Cookies and other metadata are carried in HTTP headers."},
                {"question": "Why is it dangerous for a server to trust client-submitted data without validation?", "options": ["Client-submitted data is always encrypted", "An attacker fully controls what the client sends and can submit unexpected or malicious values", "Servers cannot process client data at all", "Validation is only relevant for mobile apps"], "correct_index": 1, "explanation": "Since the client is outside the server's control, any request data must be validated server-side, not trusted blindly."}
            ],
            "resources": [
                {"label": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Exploitation Fundamentals",
            "title": "SQL Injection — Finding and Exploiting It Safely",
            "learning_objective": "By the end of this class, you will be able to identify a SQL injection vulnerability in a lab application and use it to extract data.",
            "duration_minutes": 35,
            "content_html": "<p>SQL injection has been on the OWASP Top Ten list for over a decade and remains one of the most damaging vulnerabilities found in real assessments, because a single successful injection can expose an entire database. It is also one of the most frequently tested topics in cybersecurity job interviews.</p><h2>How It Works</h2><p>SQL injection happens when user input is inserted directly into a database query without proper handling, allowing an attacker to change the query's logic. A classic example is a login form where the backend builds a query by directly concatenating the username field into a SQL string. If an attacker enters a username designed to always evaluate true in the underlying SQL logic, the query can return a result and log the attacker in without knowing any valid password.</p><h2>Worked Example</h2><p>On a deliberately vulnerable practice application like DVWA or OWASP Juice Shop, a search field might be vulnerable to injection. Entering a crafted value that closes the intended query and appends a UNION SELECT statement can trick the database into returning data from a completely different table, such as a table of usernames and password hashes, directly in the search results. The fix, which you should always mention in a report, is using parameterized queries or prepared statements so user input is always treated as data, never as executable query logic.</p>",
            "key_concepts": ["SQL injection", "Query concatenation", "UNION-based injection", "Parameterized queries", "OWASP Top Ten"],
            "practical_exercise": {
                "title": "Exploit SQL Injection in a Lab App",
                "instructions": "Using a legal vulnerable practice application such as DVWA, OWASP Juice Shop, or a TryHackMe SQL injection room, identify and exploit a SQL injection vulnerability to extract data you should not normally see. Document the exact input you used, the response you received, and one sentence explaining the correct developer fix."
            },
            "quiz": [
                {"question": "What fundamentally causes a SQL injection vulnerability?", "options": ["Using HTTPS instead of HTTP", "User input being inserted into a database query without proper handling", "The database server being physically unsecured", "Using a slow internet connection"], "correct_index": 1, "explanation": "SQL injection arises when untrusted input is allowed to alter the structure or logic of a SQL query."},
                {"question": "What is the standard developer fix for SQL injection vulnerabilities?", "options": ["Hiding the login page URL", "Using parameterized queries or prepared statements", "Disabling the database entirely", "Increasing server RAM"], "correct_index": 1, "explanation": "Parameterized queries ensure user input is always treated strictly as data, never as executable SQL logic."},
                {"question": "Why has SQL injection remained a persistent issue for so many years despite being well known?", "options": ["It cannot be fixed with current technology", "Developers sometimes still build queries by concatenating raw user input instead of using safe query methods", "Databases no longer support parameterized queries", "It only affects operating systems, not applications"], "correct_index": 1, "explanation": "The vulnerability persists mainly due to insecure coding practices, not a lack of available fixes."}
            ],
            "resources": [
                {"label": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"},
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Exploitation Fundamentals",
            "title": "Cross-Site Scripting (XSS) in Practice",
            "learning_objective": "By the end of this class, you will be able to identify and demonstrate a cross-site scripting vulnerability in a lab web application.",
            "duration_minutes": 30,
            "content_html": "<p>Cross-site scripting, or XSS, is another OWASP Top Ten mainstay and one of the most commonly reported bug bounty findings worldwide, because it is easy to introduce and often overlooked by developers focused on backend logic.</p><h2>Reflected, Stored, and DOM-Based XSS</h2><p>XSS happens when an application includes untrusted input in a page without properly encoding it, allowing an attacker to inject their own JavaScript that runs in another user's browser. Reflected XSS happens when malicious input is immediately echoed back in the response, often via a URL parameter, requiring the victim to click a crafted link. Stored XSS is more dangerous: the malicious input is saved on the server, for example in a comment or profile field, and executes automatically for every user who later views that page. DOM-based XSS happens entirely on the client side through unsafe JavaScript handling of user-controlled data.</p><h2>Worked Example</h2><p>Imagine a comment section on a practice blog application that does not sanitize input. An attacker posts a comment containing a script tag that steals the session cookie of anyone who views the page and sends it to a server the attacker controls. Every subsequent visitor, including an administrator, silently executes that script, potentially handing over their session and allowing full account takeover. This is why stored XSS is typically rated more severely than reflected XSS in a professional report.</p>",
            "key_concepts": ["Cross-site scripting", "Reflected XSS", "Stored XSS", "DOM-based XSS", "Output encoding"],
            "practical_exercise": {
                "title": "Demonstrate XSS in a Lab App",
                "instructions": "Using a legal practice application such as DVWA, OWASP Juice Shop, or a TryHackMe XSS room, find and trigger a reflected or stored XSS vulnerability with a harmless proof-of-concept payload such as an alert popup. Document the exact input, where it was injected, and whether it was reflected or stored, and explain why stored XSS is generally rated more severe."
            },
            "quiz": [
                {"question": "What is the key difference between reflected and stored XSS?", "options": ["Reflected XSS is saved on the server and runs for every visitor, stored XSS requires a crafted link each time", "Stored XSS is saved on the server and runs automatically for visitors, reflected XSS requires the victim to trigger it via a crafted request", "There is no meaningful difference", "Reflected XSS only affects mobile browsers"], "correct_index": 1, "explanation": "Stored XSS persists on the server and affects any viewer automatically, which is generally more dangerous than reflected XSS."},
                {"question": "What is the primary developer defense against XSS?", "options": ["Disabling JavaScript entirely on the server", "Properly encoding or sanitizing user-supplied output before rendering it in a page", "Using a faster web server", "Blocking all cookies"], "correct_index": 1, "explanation": "Correct output encoding prevents injected input from being interpreted as executable script by the browser."},
                {"question": "Why is stored XSS typically rated with higher severity than reflected XSS in a report?", "options": ["It requires more technical skill to discover", "It can automatically execute against every visitor without requiring a crafted link to be clicked", "It only works on outdated browsers", "It cannot be fixed by developers"], "correct_index": 1, "explanation": "Because stored XSS persists and triggers automatically for any viewer, its potential blast radius is much larger."}
            ],
            "resources": [
                {"label": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Exploitation Fundamentals",
            "title": "Using Burp Suite to Intercept and Modify Traffic",
            "learning_objective": "By the end of this class, you will be able to configure Burp Suite as a proxy and intercept and modify a live web request.",
            "duration_minutes": 35,
            "content_html": "<p>Burp Suite is the industry-standard tool for web application testing, used in nearly every professional penetration test and bug bounty workflow. Today you set it up properly and use it to do what a browser address bar alone cannot: intercept and edit requests before they leave your machine.</p><h2>How a Proxy Tool Works</h2><p>Burp Suite sits between your browser and the target website as a proxy, meaning all traffic passes through it first. With interception turned on, Burp pauses each outgoing request, letting you view and edit every field, header, and parameter before choosing to forward it. This lets you test things a normal browser interaction cannot, such as submitting a negative number in a quantity field, or removing a security header entirely, to see how the server reacts.</p><h2>Worked Example</h2><p>Testing a lab e-commerce checkout flow, you intercept the request that submits your cart total and discover the total price is sent from the browser, not recalculated server-side. Editing that field in Burp Suite to a much lower price before forwarding the request, and watching the server accept it, demonstrates a serious business logic flaw: never trust a price the client sends. This exact class of bug, trusting client-supplied pricing or quantity data, is regularly found in real e-commerce assessments.</p>",
            "key_concepts": ["Burp Suite", "Proxy interception", "Request tampering", "Business logic flaws", "Client-side trust issues"],
            "practical_exercise": {
                "title": "Intercept and Modify a Request",
                "instructions": "Configure Burp Suite Community Edition as your browser proxy against a legal lab target such as OWASP Juice Shop. Intercept one request, modify at least one parameter value, and forward it. Document the original and modified request, the server's response, and one sentence on what the finding would mean in a real assessment."
            },
            "quiz": [
                {"question": "What role does Burp Suite play when configured as a proxy?", "options": ["It replaces the target web server", "It sits between the browser and the target, letting you view and edit traffic before it is sent", "It only scans for open ports", "It automatically fixes vulnerabilities it finds"], "correct_index": 1, "explanation": "As a proxy, Burp Suite intercepts traffic in transit, giving the tester full control to inspect and modify requests."},
                {"question": "Why is it a serious vulnerability if an e-commerce checkout trusts a price submitted from the client?", "options": ["It has no real security impact", "An attacker can modify the price in transit before the server processes payment", "Client-submitted prices are always more accurate", "It only affects the visual display, not the actual charge"], "correct_index": 1, "explanation": "If the server does not recalculate the price itself, an attacker can pay far less than the real amount by editing the request."},
                {"question": "What is the correct server-side fix for the pricing flaw described in the lesson?", "options": ["Hide the price field from the browser entirely", "Always recalculate the price server-side from trusted product data rather than trusting client input", "Encrypt the price field only", "Remove the shopping cart feature"], "correct_index": 1, "explanation": "Sensitive values like price must be authoritative on the server, never trusted from client-supplied data."}
            ],
            "resources": [
                {"label": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Advanced Exploitation Techniques",
            "title": "Privilege Escalation on Linux Targets",
            "learning_objective": "By the end of this class, you will be able to enumerate a compromised Linux machine for common privilege escalation paths and gain root access.",
            "duration_minutes": 35,
            "content_html": "<p>Gaining initial access to a machine is rarely the end goal in a real assessment. Most valuable data and system control require higher privileges, so privilege escalation, going from a low-privileged foothold to full administrative control, is a core stage of nearly every professional engagement.</p><h2>Common Linux Escalation Paths</h2><p>Once you have a low-privilege shell, enumeration is the first step: checking sudo permissions with sudo -l, looking for misconfigured file permissions on sensitive files, searching for cron jobs running as root that a low-privilege user can modify, and checking for outdated kernel versions with known exploits. A very common real-world finding is a sudo rule that allows a low-privilege user to run a specific program as root without a password, where that program can be abused to spawn a root shell.</p><h2>Worked Example</h2><p>On a practice machine, running sudo -l might show that your low-privilege user is allowed to run a text editor as root without a password. Many common command-line editors have a built-in way to spawn a shell from within the program, and since the editor itself was launched as root, the shell it spawns is also root. This single misconfiguration, an overly permissive sudo rule, is one of the most frequently seen privilege escalation findings in both practice labs and real internal penetration tests.</p>",
            "key_concepts": ["Privilege escalation", "sudo misconfiguration", "Cron job abuse", "Kernel exploits", "Linux enumeration"],
            "practical_exercise": {
                "title": "Escalate Privileges in Your Lab",
                "instructions": "On a legal practice machine such as a TryHackMe privilege escalation room, gain a low-privilege shell and enumerate for escalation paths using sudo -l and a check of cron jobs and file permissions. Document the exact misconfiguration you found and the commands you used to escalate to root, including the final proof of root access."
            },
            "quiz": [
                {"question": "What does privilege escalation refer to in a security assessment?", "options": ["Increasing a server's network bandwidth", "Moving from a low-privilege foothold to higher, often administrative, access on a system", "Encrypting data at rest", "Changing a user's display name"], "correct_index": 1, "explanation": "Privilege escalation means gaining more access rights than the account initially had."},
                {"question": "What command is commonly used to check what a Linux user is permitted to run as root?", "options": ["ls -la", "sudo -l", "chmod 777", "ping"], "correct_index": 1, "explanation": "sudo -l lists the commands the current user is permitted to run with elevated privileges."},
                {"question": "Why is an overly permissive sudo rule for a text editor considered a serious finding?", "options": ["It has no real impact because editors cannot run other commands", "Many command-line editors can spawn a shell, which inherits root privileges if the editor was run as root", "It only affects graphical applications", "It requires physical access to exploit"], "correct_index": 1, "explanation": "If a program with shell-spawning capability is run as root via sudo, the spawned shell also runs as root, granting full escalation."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Advanced Exploitation Techniques",
            "title": "Privilege Escalation on Windows Targets",
            "learning_objective": "By the end of this class, you will be able to enumerate a compromised Windows machine for common misconfigurations that allow privilege escalation.",
            "duration_minutes": 35,
            "content_html": "<p>Windows dominates corporate desktop and server environments, so Windows privilege escalation skills are essential for anyone doing internal network assessments, which make up a large share of paid penetration testing work.</p><h2>Common Windows Escalation Paths</h2><p>After gaining a foothold, useful enumeration steps include checking installed services for weak file or folder permissions that allow replacing a service executable, checking for stored credentials in configuration files or scheduled tasks, and checking for missing security patches that correspond to known local privilege escalation exploits. A service running as the highly privileged SYSTEM account, but with a program file that a low-privilege user can overwrite, is a classic and still common finding.</p><h2>Worked Example</h2><p>On a practice Windows machine, enumeration might reveal a custom application service configured to run as SYSTEM, but the folder holding its executable is writable by any authenticated user. Replacing that executable with a malicious one, then restarting or waiting for the service to run, executes the attacker's code with SYSTEM privileges, the highest level on Windows. This exact pattern, a privileged service pointing at a file or folder with weak permissions, appears repeatedly across real internal assessments of poorly configured Windows environments.</p>",
            "key_concepts": ["Windows privilege escalation", "Service misconfiguration", "SYSTEM privileges", "Weak file permissions", "Unpatched local exploits"],
            "practical_exercise": {
                "title": "Enumerate a Windows Practice Target",
                "instructions": "On a legal practice platform, work through a beginner Windows privilege escalation room. Document the enumeration commands or tools you used, the specific misconfiguration you identified (service permission, stored credential, or missing patch), and the steps you took to escalate privileges, with evidence of the final access level achieved."
            },
            "quiz": [
                {"question": "What makes a Windows service a privilege escalation risk if its executable folder has weak permissions?", "options": ["Services cannot be restarted by users", "A low-privilege user can replace the executable, which then runs with the service's often higher privilege level", "Weak folder permissions only affect file storage, not execution", "SYSTEM services cannot be exploited"], "correct_index": 1, "explanation": "If the service runs as SYSTEM but its files are writable by a low-privilege user, replacing the executable lets an attacker execute code at SYSTEM level."},
                {"question": "What is the SYSTEM account on Windows roughly equivalent to?", "options": ["A guest account with no permissions", "The highest-privileged built-in account, similar to root on Linux", "A network printer account", "A temporary session account"], "correct_index": 1, "explanation": "SYSTEM is the most privileged account on a Windows machine, comparable to root on Linux."},
                {"question": "Why do internal Windows environments frequently show privilege escalation findings in real assessments?", "options": ["Windows cannot run any security software", "Legacy configurations, weak permissions, and missed patches accumulate over time in real environments", "Windows machines are never patched by vendors", "Privilege escalation is impossible to prevent"], "correct_index": 1, "explanation": "Real-world environments accumulate configuration drift and missed patches over years, creating exploitable gaps."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Advanced Exploitation Techniques",
            "title": "Password Cracking with Hashcat and Wordlists",
            "learning_objective": "By the end of this class, you will be able to crack a captured password hash using Hashcat and an appropriate wordlist.",
            "duration_minutes": 30,
            "content_html": "<p>After gaining access to a system, you often find password hashes rather than plaintext passwords, whether in a database dump, a Windows SAM file, or a Linux shadow file. Turning those hashes back into usable passwords is a practical skill directly tested in many junior security roles.</p><h2>Cracking Approaches</h2><p>A dictionary attack tries every word in a wordlist, such as the well-known rockyou.txt list of leaked real-world passwords, against a hash. A brute-force attack tries every possible character combination, which is thorough but extremely slow for anything beyond short passwords. Hashcat is the standard tool for this work, and it needs to know the hash type, since MD5, SHA-256, and bcrypt hashes all require different cracking modes.</p><h2>Worked Example</h2><p>Suppose you extract an MD5 password hash from a lab database. Running Hashcat with the correct hash mode for MD5 and the rockyou.txt wordlist against that single hash can crack a weak, common password like a name plus a birth year in seconds. If the same password had instead been hashed with bcrypt, even a strong wordlist attack would take dramatically longer because bcrypt is intentionally slow, which is exactly why bcrypt is the recommended algorithm from Day 6 and why this lesson reinforces why hashing algorithm choice matters so much.</p>",
            "key_concepts": ["Password cracking", "Dictionary attack", "Brute-force attack", "Hashcat", "Hash identification"],
            "practical_exercise": {
                "title": "Crack a Practice Hash",
                "instructions": "Using Hashcat and a common wordlist such as rockyou.txt, crack at least one deliberately weak password hash from a legal practice source such as a TryHackMe room or a hash you generate yourself in your lab for practice. Document the hash type, the command used, the cracked password, and one paragraph explaining why weak passwords remain crackable even with modern hashing."
            },
            "quiz": [
                {"question": "What is a dictionary attack in password cracking?", "options": ["Trying every possible character combination", "Trying every word in a precompiled wordlist of likely passwords against a hash", "Guessing passwords by asking the user directly", "Disabling the login page entirely"], "correct_index": 1, "explanation": "A dictionary attack tests known or likely passwords from a wordlist rather than every possible combination."},
                {"question": "Why does Hashcat need to know the specific hash type before attempting to crack it?", "options": ["Different hash algorithms produce output that must be processed with the matching cracking mode", "Hashcat only works on one hash type total", "Hash type has no effect on cracking", "It is only needed for encryption, not hashing"], "correct_index": 0, "explanation": "Each hash algorithm has a distinct structure, so Hashcat must be told which algorithm to target."},
                {"question": "Why does a bcrypt-hashed password resist cracking better than an MD5-hashed one, even with the same wordlist?", "options": ["bcrypt hides the password from the wordlist entirely", "bcrypt is intentionally slow to compute, making large-scale guessing far more time-consuming", "MD5 cannot be cracked at all", "bcrypt does not produce a hash"], "correct_index": 1, "explanation": "bcrypt's deliberate computational cost dramatically slows down attackers attempting large-scale guessing, unlike fast algorithms like MD5."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Advanced Exploitation Techniques",
            "title": "Wireless Network Security Testing Basics",
            "learning_objective": "By the end of this class, you will be able to explain common WiFi security weaknesses and how a wireless assessment on an authorized network is conducted.",
            "duration_minutes": 25,
            "content_html": "<p>Wireless networks extend an organization's attack surface beyond its walls, and many small businesses in Nigeria and across Africa still run WiFi with outdated security or weak passwords, making wireless assessment a valuable and marketable skill even for smaller clients who cannot afford a full penetration test.</p><h2>Wireless Weaknesses</h2><p>WEP encryption is badly broken and crackable in minutes, and should never be used today. WPA2 is far stronger but still vulnerable to offline password cracking if the network uses a weak pre-shared key, since an attacker can capture the handshake exchanged when a device connects and crack it offline without needing to be near the network anymore. WPA3 fixes many of these weaknesses but is not yet universal. Rogue access points, unauthorized WiFi networks set up to mimic a legitimate one, are another common attack used to intercept traffic from unsuspecting users.</p><h2>Worked Example</h2><p>On an authorized wireless assessment of a small business network you have explicit permission to test, capturing the WPA2 four-way handshake during a legitimate device connection and running it through a cracking tool against a wordlist can reveal a weak pre-shared key like a phone number or business name plus year, a very common finding in African small business networks. The remediation recommendation is straightforward and cheap: a long, random passphrase and moving toward WPA3 where supported.</p>",
            "key_concepts": ["WEP and WPA2 weaknesses", "WPA handshake capture", "Rogue access points", "Pre-shared key strength", "Wireless assessment scope"],
            "practical_exercise": {
                "title": "Audit Your Own Home WiFi Configuration",
                "instructions": "On your own home or personal WiFi router, which you are authorized to review, check and document the encryption type in use (WEP, WPA2, or WPA3), the general strength of the current passphrase without writing the actual password down, and two specific improvements you would recommend. Never test a network you do not own or have written authorization to test."
            },
            "quiz": [
                {"question": "Why is WEP encryption considered unsafe for any network today?", "options": ["It is too slow to be practical", "It has well-known cryptographic weaknesses that allow it to be cracked in minutes", "It is more expensive than WPA2", "It only works with old routers"], "correct_index": 1, "explanation": "WEP has fundamental cryptographic flaws that make it trivially crackable with widely available tools."},
                {"question": "What does capturing a WPA2 handshake allow an attacker to do?", "options": ["Immediately connect to the network with no further effort", "Attempt an offline password cracking attack against the captured handshake", "Permanently disable the network", "Bypass the need for any password entirely"], "correct_index": 1, "explanation": "The captured handshake can be cracked offline against a wordlist to attempt to recover the pre-shared key."},
                {"question": "What is a rogue access point?", "options": ["A legitimate network extender installed by IT", "An unauthorized WiFi network set up to mimic a legitimate one and intercept user traffic", "A type of firewall rule", "A wired network switch"], "correct_index": 1, "explanation": "Rogue access points impersonate trusted networks to trick users into connecting and exposing their traffic."}
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Advanced Exploitation Techniques",
            "title": "Capturing and Analyzing Traffic with Wireshark",
            "learning_objective": "By the end of this class, you will be able to capture network traffic with Wireshark and identify sensitive data sent in the clear.",
            "duration_minutes": 30,
            "content_html": "<p>Wireshark is the standard tool for packet-level network analysis, used by both attackers looking for exposed data and defenders investigating incidents. Reading raw traffic is a skill that shows up constantly, from confirming a vulnerability during a test to investigating a suspected breach.</p><h2>Reading a Packet Capture</h2><p>Wireshark captures every packet crossing a network interface and lets you filter and inspect them individually. Filters like http or tcp.port equals 80 narrow a capture down to relevant traffic. A key finding to look for is any application sending sensitive data, such as login credentials, over unencrypted HTTP instead of HTTPS, since anyone with access to the same network segment, such as public WiFi, can potentially see that data with a tool like Wireshark.</p><h2>Worked Example</h2><p>In your isolated lab, capturing traffic while logging into a deliberately insecure practice web application that uses plain HTTP will let you filter by the http protocol and find the exact POST request containing the username and password fields in readable plaintext. This is a powerful, visual way to demonstrate to a non-technical stakeholder in a report why forcing HTTPS everywhere matters, because you can literally show them the captured plaintext password as evidence.</p>",
            "key_concepts": ["Packet capture", "Wireshark filters", "Cleartext credential exposure", "HTTP vs HTTPS", "Network traffic analysis"],
            "practical_exercise": {
                "title": "Capture and Analyze Cleartext Traffic",
                "instructions": "In your isolated lab, use Wireshark to capture traffic while logging into a deliberately vulnerable practice application over plain HTTP. Filter the capture to isolate the login request, and take a screenshot showing the credentials visible in plaintext. Write two to three sentences explaining this finding as you would in a client report."
            },
            "quiz": [
                {"question": "What is the main risk of an application sending login credentials over plain HTTP?", "options": ["The login will always fail", "Anyone with access to the network path can potentially intercept and read the credentials", "HTTP is faster than HTTPS so this is only a performance issue", "There is no security risk if the password is short"], "correct_index": 1, "explanation": "Unencrypted HTTP traffic can be read by anyone positioned to observe the network path, exposing sensitive data like credentials."},
                {"question": "What does a Wireshark filter like http do?", "options": ["It blocks all HTTP traffic from being captured", "It narrows the displayed packets down to only HTTP traffic", "It encrypts the captured traffic", "It deletes non-HTTP packets from the network"], "correct_index": 1, "explanation": "Filters in Wireshark control what captured traffic is displayed, without affecting the underlying capture."},
                {"question": "Why is a Wireshark capture of plaintext credentials a persuasive piece of evidence in a security report?", "options": ["It proves the finding with concrete, visual evidence a non-technical reader can understand", "It is the only acceptable form of evidence in any report", "It automatically fixes the vulnerability", "It replaces the need for a severity rating"], "correct_index": 0, "explanation": "Visual, concrete evidence like a captured plaintext password makes the business risk immediately clear to any reader."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Professional Practice and Reporting",
            "title": "Planning a Professional Penetration Test — Scope and Rules of Engagement",
            "learning_objective": "By the end of this class, you will be able to draft a basic scope of work and rules of engagement document for a penetration test.",
            "duration_minutes": 30,
            "content_html": "<p>No legal, professional penetration test begins without a signed agreement defining exactly what can be tested, when, and how. Skipping this step is the difference between a paid professional engagement and a computer crime, and clients specifically look for testers who understand this process.</p><h2>Key Elements of Scope</h2><p>A scope of work defines exactly which systems, IP ranges, or applications are in scope and, just as importantly, what is explicitly out of scope. Rules of engagement define allowed testing windows, whether denial-of-service style testing is permitted, an emergency contact if something breaks, and how findings will be reported and to whom. Written authorization, sometimes called a get-out-of-jail-free letter, is what legally protects the tester if their activity is ever questioned by law enforcement or a third party.</p><h2>Worked Example</h2><p>A small Nigerian retail company hiring you to test their new e-commerce checkout flow would sign a scope of work that names the exact domain and IP range in scope, explicitly excludes their production payment gateway if it is run by a third party, sets an approved testing window outside peak sales hours, and includes emergency contact details for both sides. Testing anything outside that written scope, even accidentally, such as a linked third-party service, is a serious professional and legal problem, regardless of good intentions.</p>",
            "key_concepts": ["Scope of work", "Rules of engagement", "Written authorization", "Testing windows", "Out-of-scope systems"],
            "practical_exercise": {
                "title": "Draft a Scope of Work",
                "instructions": "Write a one-page scope of work and rules of engagement document for a fictional penetration test of a small business web application. Include in-scope systems, explicitly out-of-scope systems, allowed testing hours, an emergency contact process, and a statement of written authorization."
            },
            "quiz": [
                {"question": "Why is written authorization essential before starting a penetration test?", "options": ["It speeds up the testing process technically", "It legally protects the tester and confirms exactly what the client has permitted", "It is only a formality with no real consequence", "It is required only for government clients"], "correct_index": 1, "explanation": "Written authorization is the legal basis that separates authorized testing from a criminal offense."},
                {"question": "What does defining out-of-scope systems in an agreement protect against?", "options": ["Slower report delivery", "Accidentally testing systems the client did not authorize, which could cause legal or business harm", "Higher project costs", "Weaker vulnerability findings"], "correct_index": 1, "explanation": "Explicitly excluding systems prevents accidental testing of infrastructure the client does not control or has not approved."},
                {"question": "What is commonly included in rules of engagement beyond the technical scope?", "options": ["The tester's personal banking details", "Testing windows, escalation contacts, and reporting expectations", "The client's marketing budget", "Unrelated staff performance reviews"], "correct_index": 1, "explanation": "Rules of engagement cover operational details like timing, emergency contacts, and how results will be communicated."}
            ],
            "resources": [
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Professional Practice and Reporting",
            "title": "OWASP Top 10 Deep Dive — Prioritizing What Matters",
            "learning_objective": "By the end of this class, you will be able to explain all ten OWASP Top 10 categories and map lab findings from this course onto them.",
            "duration_minutes": 30,
            "content_html": "<p>The OWASP Top 10 is the most referenced web security standard in the industry, cited in job descriptions, compliance requirements, and client conversations. Being able to fluently discuss it signals baseline professional competence to any employer or client.</p><h2>The Categories</h2><p>The current OWASP Top 10 covers broken access control, cryptographic failures, injection (including SQL injection from Day 13), insecure design, security misconfiguration, vulnerable and outdated components, identification and authentication failures, software and data integrity failures, security logging and monitoring failures, and server-side request forgery. Notice that several categories, like broken access control and insecure design, are about how a system was architected, not just a single coding bug, which is why fixing them often requires more than a one-line patch.</p><h2>Worked Example</h2><p>Reviewing your work from this course so far: the insecure direct object reference from Day 12 falls under broken access control. The SQL injection from Day 13 falls under injection. The outdated vsftpd version from Day 8 falls under vulnerable and outdated components. The plaintext credentials captured in Wireshark on Day 20 relate to cryptographic failures. Mapping your own lab findings onto this list is exactly the exercise a hiring manager might ask you to walk through in an interview, so treat today as rehearsal.</p>",
            "key_concepts": ["OWASP Top 10", "Broken access control", "Security misconfiguration", "Vulnerable components", "Vulnerability categorization"],
            "practical_exercise": {
                "title": "Map Your Findings to OWASP",
                "instructions": "Go back through your notes from Days 8, 12, 13, 14, and 20. For each finding, identify which OWASP Top 10 category it belongs to and write one sentence justifying the mapping. Submit this as a short reference table you can reuse in your final capstone report."
            },
            "quiz": [
                {"question": "Which OWASP Top 10 category does an insecure direct object reference vulnerability typically fall under?", "options": ["Broken access control", "Security logging and monitoring failures", "Server-side request forgery", "Software and data integrity failures"], "correct_index": 0, "explanation": "IDOR is a failure to properly enforce access control on individual objects or records."},
                {"question": "Why are OWASP categories like insecure design considered architectural rather than simple coding bugs?", "options": ["They only apply to mobile apps", "They stem from how a system was planned and structured, not just a single line of faulty code", "They are automatically fixed by updating software versions", "They cannot be found during testing"], "correct_index": 1, "explanation": "Insecure design issues arise from flawed planning or architecture, requiring broader changes than a simple patch."},
                {"question": "Why is fluency with the OWASP Top 10 valuable in a job interview?", "options": ["It is the only topic ever discussed in security interviews", "It demonstrates shared professional vocabulary and baseline competence that hiring managers expect", "It guarantees a job offer regardless of other skills", "It is unrelated to real assessment work"], "correct_index": 1, "explanation": "The OWASP Top 10 is a common reference point, and fluency with it signals you can communicate findings in industry-standard terms."}
            ],
            "resources": [
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Professional Practice and Reporting",
            "title": "Writing Findings That Get Fixed — Severity Ratings with CVSS",
            "learning_objective": "By the end of this class, you will be able to write a well-structured vulnerability finding with an appropriate CVSS-based severity rating.",
            "duration_minutes": 30,
            "content_html": "<p>A brilliant technical finding that is poorly written and vaguely rated often gets ignored or deprioritized by a busy engineering team. Writing findings clearly enough that they actually get fixed is arguably as valuable a skill as finding the vulnerability in the first place.</p><h2>Structure of a Good Finding</h2><p>A strong finding includes a clear title, a severity rating, a description of the vulnerability in plain language, the exact steps to reproduce it, evidence such as a screenshot or request and response pair, the business impact in terms a non-technical reader understands, and a specific remediation recommendation, not just fix this. CVSS severity considers factors like how easily the vulnerability can be exploited, whether it requires authentication, and what impact it has on confidentiality, integrity, and availability, tying directly back to Day 1's framework.</p><h2>Worked Example</h2><p>Compare two ways of writing the same finding. A weak version says the login is vulnerable to SQL injection, please fix. A strong version says the login form at slash login is vulnerable to SQL injection in the username field, rated critical because it allows complete authentication bypass and full database extraction without credentials, includes the exact payload used and a screenshot of extracted data, explains that this could expose all customer records including payment information, and recommends switching to parameterized queries with a specific code-level example. The second version gets prioritized and fixed far faster.</p>",
            "key_concepts": ["Finding structure", "CVSS severity", "Steps to reproduce", "Business impact statement", "Remediation recommendation"],
            "practical_exercise": {
                "title": "Rewrite a Weak Finding",
                "instructions": "Take the SQL injection finding you documented on Day 13. Rewrite it as a complete, professional finding including a title, severity rating with justification, description, steps to reproduce, evidence reference, business impact statement, and specific remediation recommendation."
            },
            "quiz": [
                {"question": "What is missing from a finding that simply says the login is vulnerable to SQL injection, please fix?", "options": ["Nothing, this is a complete finding", "Reproduction steps, evidence, business impact, and a specific remediation recommendation", "The name of the tester", "The date the test was performed"], "correct_index": 1, "explanation": "A usable finding needs enough detail that an engineer can reproduce, understand the impact, and know exactly how to fix it."},
                {"question": "What does CVSS severity scoring take into account?", "options": ["Only how many lines of code are affected", "Factors such as exploitability, authentication requirements, and impact on confidentiality, integrity, and availability", "The tester's years of experience", "The client's marketing budget"], "correct_index": 1, "explanation": "CVSS scores combine exploitability and impact factors, tying back to the CIA triad from Day 1."},
                {"question": "Why should a finding include a business impact statement rather than only technical detail?", "options": ["Business impact statements are legally required in every report", "It helps non-technical stakeholders understand why the fix should be prioritized", "Technical detail is never needed in professional reports", "It replaces the need for evidence"], "correct_index": 1, "explanation": "Decision-makers who approve fixes are often non-technical, so translating risk into business terms drives prioritization."}
            ],
            "resources": []
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Professional Practice and Reporting",
            "title": "Defensive Security — Blue Team Basics and Detection",
            "learning_objective": "By the end of this class, you will be able to describe how common attacks from this course could be detected by a defensive security team.",
            "duration_minutes": 25,
            "content_html": "<p>Understanding offense makes you a better defender, and understanding defense makes you a far more credible offensive tester, since you can advise clients not just on the vulnerability but on how to detect similar attacks in the future. Many job postings in Africa are for blue team or SOC analyst roles, so this perspective broadens your career options significantly.</p><h2>Detection Fundamentals</h2><p>A Security Operations Center, or SOC, monitors logs and alerts from firewalls, servers, and applications looking for suspicious patterns. Common detection signals include repeated failed login attempts suggesting a brute-force attack, unusual outbound traffic suggesting data exfiltration or command and control activity, and web server logs showing SQL injection style payloads in request parameters. A Security Information and Event Management system, or SIEM, aggregates logs from many sources so an analyst can correlate events that would look harmless in isolation.</p><h2>Worked Example</h2><p>Recall the SQL injection attack from Day 13. From a defender's perspective, the web application firewall or SIEM could be configured to alert whenever request parameters contain suspicious SQL keywords like UNION SELECT combined with unusual characters. The privilege escalation from Day 16, using sudo to spawn a root shell from a text editor, would show up in system logs as an unusual sudo execution pattern for that user account, something a trained SOC analyst reviewing daily logs should flag for investigation.</p>",
            "key_concepts": ["Security Operations Center", "SIEM", "Log correlation", "Detection signatures", "Blue team perspective"],
            "practical_exercise": {
                "title": "Write Detection Recommendations",
                "instructions": "Choose two attacks you performed earlier in this course, such as the SQL injection from Day 13 or the privilege escalation from Day 16. For each, write a short detection recommendation explaining what log entries or alerts a defensive team could use to catch that specific attack in progress."
            },
            "quiz": [
                {"question": "What is the main function of a SIEM system?", "options": ["It automatically fixes vulnerabilities", "It aggregates and correlates logs from multiple sources to help detect suspicious activity", "It replaces the need for firewalls", "It encrypts all network traffic"], "correct_index": 1, "explanation": "A SIEM centralizes and correlates log data, making it easier to spot patterns that indicate an attack."},
                {"question": "What log pattern would most likely indicate a brute-force login attack?", "options": ["A single successful login", "Repeated failed login attempts against the same account in a short time", "A server restart", "Normal daytime traffic volume"], "correct_index": 1, "explanation": "Multiple rapid failed login attempts are a classic signature of a brute-force or credential-stuffing attack."},
                {"question": "Why is understanding defensive detection valuable for someone pursuing offensive security roles?", "options": ["It has no relevance to offensive testing work", "It allows a tester to advise clients on detection gaps, not just the vulnerabilities themselves", "It replaces the need to understand exploitation", "It is only relevant to network engineers"], "correct_index": 1, "explanation": "Understanding both sides makes an offensive tester more valuable, since they can identify not just the vulnerability but also detection blind spots."}
            ],
            "resources": []
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Professional Practice and Reporting",
            "title": "Incident Response Fundamentals",
            "learning_objective": "By the end of this class, you will be able to outline the six standard incident response phases and apply them to a sample breach scenario.",
            "duration_minutes": 25,
            "content_html": "<p>Even organizations with strong preventive controls eventually experience a security incident, and how they respond in the first hours determines whether it becomes a minor event or a business-ending crisis. Incident response knowledge is frequently tested in interviews and is a distinct career path in itself.</p><h2>The Six Phases</h2><p>Preparation involves having tools, playbooks, and trained staff ready before anything happens. Identification is detecting and confirming that an incident actually occurred. Containment stops the incident from spreading further, often by isolating affected systems. Eradication removes the root cause, such as malware or a compromised account. Recovery restores systems to normal operation safely. Lessons learned captures what happened and what should change to prevent a repeat, closing the loop back to preparation.</p><h2>Worked Example</h2><p>Imagine a Nigerian company discovers ransomware has encrypted several file servers. Preparation would have included offline backups and a response playbook. Identification is the IT team noticing files are inaccessible and ransom notes appearing. Containment means immediately disconnecting affected machines from the network to stop the spread. Eradication means removing the malware and any attacker persistence mechanisms. Recovery means restoring data from clean backups, not paying the ransom, and verifying systems are clean before reconnecting. Lessons learned means investigating how the ransomware got in, likely a phishing email from Day 10, and updating staff training and email filtering accordingly.</p>",
            "key_concepts": ["Incident response lifecycle", "Containment", "Eradication", "Recovery", "Lessons learned"],
            "practical_exercise": {
                "title": "Apply the Incident Response Lifecycle",
                "instructions": "Write a short fictional incident scenario, such as a phishing-driven account compromise at a Nigerian business. Walk through all six incident response phases, one paragraph each, describing exactly what actions the response team should take at each phase for your specific scenario."
            },
            "quiz": [
                {"question": "Which incident response phase focuses on stopping an ongoing incident from spreading further?", "options": ["Preparation", "Containment", "Lessons learned", "Identification"], "correct_index": 1, "explanation": "Containment is specifically about limiting the incident's spread and impact once it has been identified."},
                {"question": "What is the purpose of the lessons learned phase?", "options": ["To assign blame to individual employees", "To review what happened and improve future preparation and defenses", "To restore backups", "To notify customers of a breach"], "correct_index": 1, "explanation": "Lessons learned closes the loop by using the incident to strengthen future preparation and prevention."},
                {"question": "In a ransomware scenario, why is restoring from clean offline backups preferred over paying the ransom?", "options": ["Paying the ransom is always faster and guaranteed to work", "Backups avoid funding criminal activity and there is no guarantee attackers will provide a working decryption key after payment", "Backups are illegal to use", "Ransomware cannot be removed any other way"], "correct_index": 1, "explanation": "Paying attackers offers no guarantee of recovery and encourages further attacks, making clean backups the safer recovery path."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Cybersecurity Career Paths and What Employers Actually Screen For",
            "learning_objective": "By the end of this class, you will be able to identify at least three distinct cybersecurity career paths and the entry-level skills each one screens for.",
            "duration_minutes": 25,
            "content_html": "<p>Cybersecurity is not one job, it is a family of specializations, and knowing which path fits your strengths helps you focus your job search and your final capstone presentation instead of applying broadly and vaguely.</p><h2>Common Entry Points</h2><p>A SOC analyst monitors alerts and logs, a strong fit if you enjoyed Day 24's detection work. A penetration tester or offensive security consultant does authorized attacks like most of this course, a strong fit if you enjoyed the exploitation weeks. A GRC analyst, standing for governance, risk, and compliance, focuses on policies, audits, and regulatory frameworks rather than hands-on hacking. An application security engineer works closely with developers to fix vulnerabilities like those from week three at the code level. Entry-level employers in Nigeria and internationally typically screen for demonstrable hands-on skill, evidence of continuous learning through certifications or practice platforms, and clear written communication.</p><h2>Worked Example</h2><p>A junior SOC analyst job posting at a Nigerian bank might list requirements like familiarity with SIEM tools, understanding of common attack patterns, and strong written communication for incident reports, directly matching Days 24 and 25. A junior penetration tester posting at a security consultancy might list Nmap, Burp Suite, and OWASP Top 10 familiarity, directly matching Days 8, 15, and 22. Recognizing this overlap between what you have practiced and what job postings ask for is exactly how you should frame your CV.</p>",
            "key_concepts": ["SOC analyst", "Penetration tester", "GRC analyst", "Application security engineer", "Entry-level hiring signals"],
            "practical_exercise": {
                "title": "Match Your Skills to a Career Path",
                "instructions": "Find two real entry-level cybersecurity job postings, from Nigeria or internationally, for two different roles (for example SOC analyst and penetration tester). For each posting, list which specific days or exercises from this course directly demonstrate a skill they are asking for."
            },
            "quiz": [
                {"question": "Which cybersecurity role primarily focuses on monitoring alerts and logs for suspicious activity?", "options": ["Penetration tester", "SOC analyst", "GRC analyst", "Graphic designer"], "correct_index": 1, "explanation": "SOC analysts are responsible for real-time monitoring and detection of security events."},
                {"question": "What does a GRC analyst primarily focus on?", "options": ["Writing exploit code", "Governance, risk, and compliance, including policies and audits", "Cracking passwords", "Designing user interfaces"], "correct_index": 1, "explanation": "GRC roles center on policy, regulatory compliance, and organizational risk management rather than hands-on offensive testing."},
                {"question": "What do entry-level cybersecurity employers commonly screen for beyond raw technical knowledge?", "options": ["Only university GPA", "Demonstrable hands-on skill and clear written communication", "Only prior job titles", "Physical strength"], "correct_index": 1, "explanation": "Because security work involves both technical execution and reporting to others, communication skill is highly valued alongside technical ability."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Common Interview Questions and How to Answer Them Technically",
            "learning_objective": "By the end of this class, you will be able to confidently answer three common technical cybersecurity interview questions using examples from your own lab work.",
            "duration_minutes": 25,
            "content_html": "<p>Technical interviews in cybersecurity often test whether you can explain concepts clearly and back them up with real examples, not just recite definitions. Today you prepare answers using the actual hands-on work you have already done this month, which is far more convincing than generic textbook answers.</p><h2>Sample Question Patterns</h2><p>Walk me through how you would approach testing a web application is a methodology question, best answered by describing the flow from recon through scanning, manual testing, and reporting that you practiced across weeks two and three. What is the difference between a vulnerability and an exploit tests conceptual understanding, a vulnerability is a weakness, an exploit is the method used to take advantage of it. Tell me about a time you found something interesting invites you to describe a specific lab finding, such as your Day 13 SQL injection or Day 16 privilege escalation, in a structured way.</p><h2>Worked Example</h2><p>A weak answer to walk me through your approach is I would run some scans and look for vulnerabilities. A strong answer says I would start with passive reconnaissance to understand the target without touching it directly, then move to active scanning with a tool like Nmap to map the attack surface, then manually test the highest-value findings such as web application inputs, and finally document everything with severity ratings and remediation advice, referencing your own Day 7 through Day 23 workflow. Specificity, backed by real lab evidence, is what separates a hire from a pass.</p>",
            "key_concepts": ["Interview methodology questions", "Vulnerability vs exploit", "STAR-style answers", "Referencing real lab work", "Technical communication"],
            "practical_exercise": {
                "title": "Write Out Three Interview Answers",
                "instructions": "Write full, spoken-style answers to these three questions, each three to five sentences, referencing specific days or findings from your own work in this course: walk me through how you would approach testing a web application, explain the difference between a vulnerability and an exploit, and tell me about an interesting finding from your practice work."
            },
            "quiz": [
                {"question": "What is the key difference between a vulnerability and an exploit?", "options": ["They are the same thing", "A vulnerability is a weakness, an exploit is the method used to take advantage of that weakness", "A vulnerability only exists in hardware, an exploit only in software", "An exploit is always illegal, a vulnerability never is"], "correct_index": 1, "explanation": "A vulnerability is the underlying flaw, while an exploit is the specific technique or code that leverages it."},
                {"question": "Why do specific, evidence-backed answers perform better in technical interviews than generic ones?", "options": ["Interviewers only care about answer length", "They demonstrate real hands-on experience and understanding rather than memorized theory", "Generic answers are always factually incorrect", "Specific answers are required by law"], "correct_index": 1, "explanation": "Concrete examples prove you can actually apply your knowledge, which is more convincing than reciting definitions."},
                {"question": "What is a strong way to answer a methodology question like walk me through your testing approach?", "options": ["List every tool you have ever heard of", "Describe a structured flow from reconnaissance through scanning, manual testing, and reporting", "Say it depends and give no further detail", "Refuse to answer without a written contract"], "correct_index": 1, "explanation": "A structured, methodical answer shows you understand the full assessment process, not just isolated techniques."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Building a Portfolio That Proves You Can Do the Job",
            "learning_objective": "By the end of this class, you will be able to structure a public portfolio that showcases your lab work to employers and clients.",
            "duration_minutes": 25,
            "content_html": "<p>In cybersecurity, a portfolio of demonstrated, legal hands-on work often matters more to hiring managers than a certificate alone, because it proves you can actually apply skills, not just pass a multiple-choice exam. Today you organize a month of scattered lab notes into something a stranger can evaluate in five minutes.</p><h2>What Belongs in a Security Portfolio</h2><p>A strong portfolio includes a short professional summary, write-ups of completed practice rooms or labs with the methodology and findings clearly explained, any relevant certifications or completed courses, and, critically, evidence you handled everything legally and ethically, since employers are wary of anyone who cannot demonstrate they understand authorization boundaries. Platforms like GitHub for written walkthroughs, or a simple personal website, are common and free ways to host this.</p><h2>Worked Example</h2><p>A useful portfolio entry for your Day 11 TryHackMe room might include a short paragraph on the target and objective, a screenshot of your Nmap scan, a description of the vulnerability found and how you exploited it, and a short reflection on what you learned. Avoid including actual exploit code for real, non-practice systems, or anything that resembles boasting about unauthorized access. A well-organized portfolio with five solid write-ups beats a disorganized one with twenty.</p>",
            "key_concepts": ["Security portfolio structure", "Lab write-ups", "Ethical framing", "GitHub for security work", "Professional summary"],
            "practical_exercise": {
                "title": "Draft Your Portfolio Homepage",
                "instructions": "Write the homepage content for your cybersecurity portfolio: a three to four sentence professional summary about yourself, a list of at least three completed labs or exercises from this course you would feature, and one sentence explaining how you approach ethical and legal boundaries in your work."
            },
            "quiz": [
                {"question": "Why do hiring managers in cybersecurity often value a portfolio of hands-on work highly?", "options": ["Portfolios are required by law", "It demonstrates practical, applied skill rather than only theoretical knowledge", "Portfolios replace the need for an interview entirely", "Certificates are never checked"], "correct_index": 1, "explanation": "A portfolio shows you can actually perform the work, which theory-only credentials cannot prove on their own."},
                {"question": "What should a security portfolio avoid including?", "options": ["Screenshots of practice lab findings", "Evidence or boasting about unauthorized access to real, non-practice systems", "A professional summary", "A list of completed practice rooms"], "correct_index": 1, "explanation": "Any suggestion of unauthorized access is a serious red flag to employers and can carry legal risk."},
                {"question": "What makes a lab write-up genuinely useful in a portfolio rather than just a screenshot dump?", "options": ["Including no explanation at all", "Explaining the objective, methodology, findings, and a reflection in clear written form", "Only listing tool names used", "Making it as long as possible regardless of clarity"], "correct_index": 1, "explanation": "A clear narrative of objective, method, and findings shows both technical skill and communication ability."}
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Responsible Disclosure and the Legal Side of Security Work",
            "learning_objective": "By the end of this class, you will be able to explain the responsible disclosure process and describe the legal boundaries of security testing.",
            "duration_minutes": 25,
            "content_html": "<p>Every skill you have learned this month can be used legally to build a career or illegally to commit a crime, and the difference is entirely about authorization and process. Understanding this clearly is not just an ethical requirement, it is something employers explicitly probe for before trusting you with client access.</p><h2>Responsible Disclosure</h2><p>If you ever discover a real vulnerability in a system you were not explicitly authorized to test, for example by stumbling onto it accidentally, the responsible path is not to exploit it further, but to report it through the organization's official channel, often a security.txt file or a bug bounty program, describe the issue clearly without demonstrating destructive impact, and give the organization reasonable time to fix it before any public discussion. Laws in Nigeria, including the Cybercrimes Act, and equivalent laws in most countries, criminalize unauthorized access to computer systems regardless of intent, even well-meaning intent.</p><h2>Worked Example</h2><p>Imagine you notice a small local business website has an obvious SQL injection flaw while simply browsing normally, without deliberately probing for it. The responsible action is to stop, find a contact email or a formal disclosure channel, and report the issue factually, without extracting real customer data as proof, and follow up respectfully. Extracting real data to prove the point, even if your intentions are good, crosses into unauthorized access and could expose you to prosecution, no matter how helpful you meant to be.</p>",
            "key_concepts": ["Responsible disclosure", "Bug bounty programs", "Cybercrimes Act", "Authorization boundaries", "Legal risk of good intentions"],
            "practical_exercise": {
                "title": "Draft a Responsible Disclosure Report",
                "instructions": "Write a short, professional responsible disclosure email as if you had accidentally discovered a vulnerability on a real website while browsing normally. The email should describe the issue factually without demonstrating destructive proof, explain your intent is to help, and request a secure channel to share further technical detail."
            },
            "quiz": [
                {"question": "What should you do if you accidentally discover a real vulnerability on a system you are not authorized to test?", "options": ["Exploit it fully to prove the issue is real", "Report it responsibly through an official channel without further exploitation", "Post about it publicly on social media immediately", "Ignore it completely and never mention it"], "correct_index": 1, "explanation": "Responsible disclosure means reporting through proper channels without causing further, unauthorized impact."},
                {"question": "Why do laws like Nigeria's Cybercrimes Act matter even for well-intentioned security researchers?", "options": ["They only apply to malicious hackers, not researchers", "They criminalize unauthorized access to computer systems regardless of intent", "They only apply to government systems", "They have no real enforcement"], "correct_index": 1, "explanation": "Most cybercrime laws focus on authorization, not intent, meaning even good-faith actions without permission can be illegal."},
                {"question": "In responsible disclosure, why should you avoid extracting real customer data as proof of a vulnerability?", "options": ["Data extraction is technically impossible", "It escalates unauthorized access and creates real legal and privacy risk, even as proof", "Customer data is never sensitive", "It is required by every disclosure program"], "correct_index": 1, "explanation": "Extracting real data goes beyond identifying the flaw and creates genuine harm and legal exposure, undermining the good intent."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Kickoff: Your Full Vulnerability Assessment Capstone",
            "learning_objective": "By the end of this class, you will be able to select a legal practice target, define your assessment scope, and begin executing your final vulnerability assessment project.",
            "duration_minutes": 30,
            "content_html": "<p>Today you begin your final capstone project: a complete vulnerability assessment and professional security report on a legal, deliberately-vulnerable practice environment, exactly as described in this course's final project brief. Everything from the past 29 days, recon, scanning, exploitation, and reporting, comes together in this single deliverable.</p><h2>Approaching the Capstone</h2><p>Start by selecting your target: a TryHackMe or Hack The Box room, or a local vulnerable VM such as Metasploitable or OWASP Juice Shop, matching the final project brief. Define your scope in writing, even for a solo practice project, listing exactly what you plan to test, mirroring Day 21's professional habits. Then work through your standard methodology: passive and active reconnaissance from Days 7 and 8, vulnerability identification using the categories from Day 22, manual exploitation and verification as practiced across weeks three and four, and severity rating using the CVSS approach from Day 23.</p><h2>What Your Final Report Needs</h2><p>You need at least five confirmed vulnerabilities across different categories, each with evidence such as screenshots or command output, a CVSS-style severity rating, and a specific remediation recommendation, all structured using the finding format from Day 23. Write two versions of your summary: a short, plain-language section for a non-technical business stakeholder describing overall risk, and a detailed technical appendix for engineers, exactly as a real client deliverable would require.</p>",
            "key_concepts": ["Capstone scoping", "End-to-end methodology", "Multi-vulnerability reporting", "Stakeholder-specific writing", "Portfolio-quality deliverable"],
            "practical_exercise": {
                "title": "Start Your Final Vulnerability Assessment Capstone",
                "instructions": "This IS the start of your final project. Choose your legal practice target (a TryHackMe or Hack The Box room, or a local vulnerable VM such as Metasploitable or OWASP Juice Shop), write a one-paragraph scope statement describing exactly what you will test, and complete your initial passive and active reconnaissance against it, saving your Nmap output and any early observations as the first section of your final report."
            },
            "quiz": [
                {"question": "What is the minimum number of confirmed vulnerabilities required for the final capstone report?", "options": ["One", "Five, across different categories", "Fifty", "There is no minimum"], "correct_index": 1, "explanation": "The final project brief requires at least five confirmed vulnerabilities across different categories, with evidence for each."},
                {"question": "Why does the capstone report need both a non-technical summary and a technical appendix?", "options": ["It is a formatting requirement with no real purpose", "Different stakeholders, business decision-makers and engineers, need the information presented differently to act on it", "Technical appendices are optional and rarely read", "Non-technical summaries are only for marketing purposes"], "correct_index": 1, "explanation": "Business stakeholders and engineers need risk and technical detail framed differently to make decisions and implement fixes."},
                {"question": "What should the very first step of the capstone project be, according to today's lesson?", "options": ["Immediately attempting exploitation with no planning", "Selecting a legal practice target and defining a written scope", "Writing the final report before any testing", "Skipping reconnaissance entirely"], "correct_index": 1, "explanation": "Just like a real professional engagement, the capstone should start with target selection and a clear written scope before any testing begins."}
            ],
            "resources": [
                {"label": "TryHackMe", "url": "https://tryhackme.com"},
                {"label": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        }
    ]
}
