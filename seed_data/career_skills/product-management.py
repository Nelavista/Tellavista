"""Seed data for the Product Management 30-Day Skill Class."""

SKILL = {
    "slug": "product-management",
    "name": "Product Management",
    "tagline": "Turn a raw idea into a prioritized roadmap, a real PRD, and a launch plan people can execute.",
    "description": "Product management is the discipline of deciding what a team should build, why, and in what order — sitting between users, engineers, and business goals. Nigerian tech companies and startups increasingly hire junior PMs and associate PMs who can run discovery, write clear requirements, and ship features that solve real problems. This track builds you from zero product experience to a job-ready portfolio piece: a full product plan you could defend in an interview.",
    "level": "beginner",
    "estimated_hours": 60,
    "course_title": "30-Day Product Management Career Track",
    "course_description": "After finishing all 30 days, a student can run lightweight user discovery, define and prioritize a product roadmap, write a clear PRD, and put together a go-to-market and launch plan for a new product or feature.",
    "final_project": {
        "title": "Take a Product Idea From Discovery to Launch Plan",
        "description": "Choose a real problem you or people around you face (a real or realistic product idea — a campus service, a fintech feature, a small business tool) and take it through the full product management pipeline: problem discovery notes and user research, a prioritized roadmap, a complete written PRD for the first release, and a go-to-market/launch plan. The deliverable must show clear reasoning connecting user problems to prioritized features to launch tactics — not just a list of nice ideas. Present it as a document a real founder or hiring manager could read and immediately understand your product thinking.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["user discovery", "prioritization", "PRD writing", "roadmapping", "go-to-market planning", "stakeholder communication", "metrics definition"],
        "rubric": [
            {"name": "Discovery and problem validation quality", "max_points": 20},
            {"name": "Roadmap and prioritization reasoning", "max_points": 25},
            {"name": "PRD clarity and completeness", "max_points": 30},
            {"name": "Go-to-market/launch plan quality", "max_points": 25}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "What Product Managers Actually Do",
            "title": "The PM's Real Job — Deciding What NOT to Build",
            "learning_objective": "By the end of this class, you will be able to explain the core responsibilities of a product manager and distinguish them from engineering and design roles.",
            "duration_minutes": 25,
            "content_html": "<p>Many people think a product manager's job is to have great ideas. In reality, the hardest and most valuable part of the job is saying no — deciding what NOT to build, so the team's limited time goes toward what actually matters. This mental shift is the first thing you need before anything else in this course makes sense.</p><h2>What a PM Actually Owns</h2><p>A PM owns the WHY and the WHAT — why a problem matters and what the team should build to solve it. Engineers own the HOW — the technical implementation. Designers own the user experience and interface. A good PM doesn't write code or design screens, but sits at the intersection, translating business and user needs into a clear plan the team can execute.</p><h2>Worked Example: A Day in a Junior PM's Life</h2><p>A Lagos fintech's junior PM starts the day reviewing user complaints about a confusing transfer flow, then meets with an engineer to scope a fix, then writes a one-page brief justifying why THIS fix matters more than three other requested features this sprint. <strong>The PM doesn't design the new flow or code it — but decides which problem gets the team's attention this week, and defends that decision with evidence.</strong></p><ul><li>The PM's core skill is prioritization and clear reasoning, not raw creativity</li><li>A PM constantly says no to good ideas so the team can focus on the most important ones</li><li>PMs succeed by making engineers and designers more effective, not by doing their jobs for them</li></ul>",
            "key_concepts": ["product manager role", "prioritization", "cross-functional collaboration", "why vs how vs what"],
            "practical_exercise": {
                "title": "Write a Role Comparison",
                "instructions": "Pick any app or product you use regularly. Write three short paragraphs describing what a PM, an engineer, and a designer would each likely be responsible for regarding one specific feature of that app. Submit the three paragraphs, one per role."
            },
            "quiz": [
                {"question": "What is often the hardest and most valuable part of a PM's job?", "options": ["Writing code", "Deciding what NOT to build", "Designing the user interface", "Managing the company's finances"], "correct_index": 1, "explanation": "Saying no to good-but-lower-priority ideas so the team focuses on what matters most is one of the PM's most valuable functions."},
                {"question": "In the why/how/what framework, what does a PM primarily own?", "options": ["The how — technical implementation", "The why and the what — the problem's importance and the plan to solve it", "Only the visual design", "The company's legal contracts"], "correct_index": 1, "explanation": "PMs define why a problem matters and what should be built, while engineers and designers own the how and the interface respectively."},
                {"question": "How do successful PMs typically operate with engineers and designers?", "options": ["By doing engineering and design work themselves", "By making engineers and designers more effective through clear direction", "By avoiding all communication with them", "By making all technical implementation decisions"], "correct_index": 1, "explanation": "Good PMs enable their cross-functional partners by providing clarity and direction, not by taking over their specialized work."}
            ],
            "resources": [{"label": "Mind the Product", "url": "https://www.mindtheproduct.com"}]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "What Product Managers Actually Do",
            "title": "Finding a Real Problem Worth Solving",
            "learning_objective": "By the end of this class, you will be able to write a clear problem statement that specifies who has the problem, what it costs them, and how you know it's real.",
            "duration_minutes": 25,
            "content_html": "<p>Most failed products aren't badly built — they're solutions to problems that didn't really exist, or weren't painful enough for people to change their behavior. Before any roadmap or PRD, a PM must be able to state the problem with precision.</p><h2>Anatomy of a Strong Problem Statement</h2><p>A strong problem statement names: WHO has the problem (a specific user segment, not \"everyone\"), WHAT the problem costs them (time, money, stress, missed opportunity), and EVIDENCE it's real (something you observed or heard, not just assumed).</p><h2>Worked Example</h2><p>Weak: \"Students need a better way to find part-time jobs.\" Strong: <strong>\"Final-year university students in Lagos (WHO) waste an average of 5+ hours a week scrolling unrelated WhatsApp groups looking for part-time gig postings (WHAT it costs them), based on interviews with 8 students who all independently described this exact frustration (EVIDENCE).\"</strong></p><ul><li>A vague \"everyone has this problem\" statement is usually a sign no real research has been done yet</li><li>Quantify the cost of the problem wherever possible — time, money, or a specific frustration</li><li>Evidence doesn't need to be a formal study — even a handful of real conversations counts, and beats pure assumption</li></ul>",
            "key_concepts": ["problem statement", "user segment", "problem evidence", "problem validation"],
            "practical_exercise": {
                "title": "Write a Strong Problem Statement",
                "instructions": "Think of a real frustration you or someone close to you has experienced (an app, a service, a daily task). Write a problem statement following the who/what/evidence structure taught today. If you don't have direct evidence yet, describe exactly what evidence you would go gather. Submit the problem statement."
            },
            "quiz": [
                {"question": "What are the three components of a strong problem statement?", "options": ["Price, feature, timeline", "Who has the problem, what it costs them, and evidence it's real", "Company name, product name, launch date", "Design, engineering, marketing"], "correct_index": 1, "explanation": "A strong problem statement specifies the affected user, the cost of the problem, and evidence proving it's genuinely felt."},
                {"question": "Why is 'everyone has this problem' usually a weak framing?", "options": ["It is always technically accurate", "It signals that no specific research into a real user segment has been done", "Broad problems are always more valuable", "It is the recommended way to start every problem statement"], "correct_index": 1, "explanation": "Vague, universal problem claims usually indicate a lack of focused research into who is actually affected and how."},
                {"question": "What counts as acceptable evidence for a problem statement, according to this lesson?", "options": ["Only formal, large-scale studies", "Even a handful of real conversations with affected users", "Pure personal assumption is sufficient", "Evidence is not necessary at all"], "correct_index": 1, "explanation": "Even informal but real conversations with affected users provide meaningful validation, far better than assumption alone."}
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "What Product Managers Actually Do",
            "title": "Talking to Users — Running a Discovery Interview",
            "learning_objective": "By the end of this class, you will be able to plan and conduct a user discovery interview using open-ended, non-leading questions.",
            "duration_minutes": 30,
            "content_html": "<p>User interviews are the single most direct way to validate whether a problem is real — but done badly, they just confirm what you already wanted to hear. Learning to ask questions that surface honest, unbiased information is a core PM skill used from day one of any product job.</p><h2>Open Questions vs Leading Questions</h2><p>Leading (bad): \"Wouldn't it be great if there was an app that helped you find part-time jobs?\" — this invites a polite \"yes\" that tells you nothing real. Open (good): \"Tell me about the last time you looked for part-time work — what did you actually do?\" — this surfaces real behavior, not a hypothetical opinion.</p><h2>Worked Example: A 5-Question Discovery Script</h2><p>1. \"Walk me through the last time you dealt with [problem area].\" 2. \"What did you try? What worked, what didn't?\" 3. \"How often does this come up?\" 4. \"What's the most frustrating part of that process?\" 5. <strong>\"If you had a magic wand, what would you change?\" — asked LAST, after real behavior has already been surfaced, so it doesn't bias earlier answers.</strong></p><ul><li>Ask about past behavior, not hypothetical future behavior — people are unreliable predictors of their own future actions</li><li>Never pitch your idea during a discovery interview — you're there to learn, not to sell</li><li>Save any solution-focused questions for the very end of the conversation</li></ul>",
            "key_concepts": ["discovery interview", "open-ended questions", "leading questions", "past behavior focus"],
            "practical_exercise": {
                "title": "Write and Conduct a Discovery Interview",
                "instructions": "Write a 5-question discovery interview script about a real problem area (can be related to your final project idea). Conduct the interview with one real person if possible, or simulate realistic likely answers if not. Submit the script plus a summary of what you learned or expect to learn."
            },
            "quiz": [
                {"question": "What is a 'leading question' in a discovery interview?", "options": ["A question that invites unbiased, honest answers", "A question phrased in a way that nudges the person toward a particular answer", "The first question asked in an interview", "A question about the interviewee's job title"], "correct_index": 1, "explanation": "Leading questions are phrased to suggest a desired answer, which biases the response and reduces its research value."},
                {"question": "Why should discovery interviews focus on past behavior rather than hypothetical future behavior?", "options": ["Past behavior is irrelevant to product decisions", "People are unreliable predictors of what they would actually do in the future", "Future behavior questions are always more accurate", "It doesn't matter which is used"], "correct_index": 1, "explanation": "What people say they would do often differs from what they actually do, making real past experiences more reliable evidence."},
                {"question": "Why should you avoid pitching your product idea during a discovery interview?", "options": ["Pitching is always required for good interviews", "The goal is to learn, not to sell, and pitching can bias the person's responses", "It has no effect on the interview's usefulness", "Only experienced PMs are allowed to pitch"], "correct_index": 1, "explanation": "Discovery interviews aim to surface honest, unbiased information; pitching shifts the conversation toward validation rather than learning."}
            ],
            "resources": []
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "What Product Managers Actually Do",
            "title": "Building a Simple User Persona From Real Research",
            "learning_objective": "By the end of this class, you will be able to build a one-page user persona grounded in real research findings rather than assumptions.",
            "duration_minutes": 25,
            "content_html": "<p>A persona is a tool for keeping a team focused on a real, specific user throughout a project — not a marketing exercise. Used well, it prevents a team from building features for an imagined \"average user\" who doesn't actually exist.</p><h2>What Makes a Persona Useful, Not Decorative</h2><p>A useful persona includes: a name and short context (job, life stage), their specific goal related to your product area, their specific pain point (grounded in real research, not guesswork), and their current workaround (what they do today without your product).</p><h2>Worked Example: Persona From Day 3 Interview Insights</h2><p>Name: Chidinma, 23, final-year Economics student. Goal: earn extra income without missing lectures. Pain point: <strong>spends hours scrolling scattered WhatsApp groups and Twitter for gig postings, often missing good opportunities because she saw them too late.</strong> Current workaround: relies on friends forwarding screenshots of job posts, which is slow and unreliable.</p><ul><li>Every detail in a persona should trace back to something you actually heard or observed, not invented</li><li>A persona with a made-up backstory but no real pain point is decorative, not useful</li><li>Keep personas to one page — an overly detailed persona becomes a novel nobody references again</li></ul>",
            "key_concepts": ["user persona", "persona grounding", "current workaround", "research-based design"],
            "practical_exercise": {
                "title": "Build a One-Page Persona",
                "instructions": "Using insights from your Day 3 discovery interview (real or simulated), build a one-page persona including name/context, goal, pain point, and current workaround. Every detail should be traceable to something from your research. Submit the persona."
            },
            "quiz": [
                {"question": "What makes a user persona useful rather than merely decorative?", "options": ["A detailed, creative backstory", "Details grounded in real research findings rather than invented assumptions", "A professional-looking photo", "A long, multi-page document"], "correct_index": 1, "explanation": "A persona is only useful when its details are traceable to real research, not invented for flavor."},
                {"question": "What is a persona's 'current workaround'?", "options": ["The product feature you plan to build", "What the user currently does to address their problem without your product", "The persona's job title", "A summary of your competitor's product"], "correct_index": 1, "explanation": "The current workaround shows how the user copes today, which reveals the real baseline your product needs to improve on."},
                {"question": "Why should a persona be kept to about one page?", "options": ["Longer personas are always better", "An overly detailed persona becomes unwieldy and rarely gets referenced again", "One page is a strict industry regulation", "Length has no effect on usefulness"], "correct_index": 1, "explanation": "A concise, one-page persona stays practical and gets used as a working reference, unlike an overly long document."}
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "What Product Managers Actually Do",
            "title": "Mapping the User Journey to Find the Real Pain Point",
            "learning_objective": "By the end of this class, you will be able to map a user's end-to-end journey through a process and identify the single highest-friction step.",
            "duration_minutes": 25,
            "content_html": "<p>Teams often jump straight to building a solution before understanding the FULL journey a user goes through — missing that the real pain point isn't where they assumed. A journey map forces this discipline before any feature gets prioritized.</p><h2>Building a Simple Journey Map</h2><p>List every step a user takes from starting to solve their problem to finishing (or giving up). For each step, note: what the user does, what they feel (frustration, confusion, confidence), and any friction point. The step with the sharpest negative feeling is usually where the biggest opportunity lies.</p><h2>Worked Example: Journey Map for Finding a Part-Time Job</h2><p>Step 1: Realizes needs extra income (feeling: motivated). Step 2: Asks friends/scrolls social media (feeling: neutral, mildly hopeful). Step 3: <strong>Finds a posting, but it's already 3 days old and the role is filled (feeling: frustrated, wasted effort).</strong> Step 4: Gives up searching actively, waits for friends to forward opportunities (feeling: resigned). The sharpest friction is Step 3 — not the searching itself, but the staleness of information once found.</p><ul><li>Map the FULL journey, including steps before and after your assumed 'core' feature area</li><li>The step with the strongest negative emotion is usually the highest-value place to focus</li><li>Journey maps often reveal the real problem is different from the one you originally assumed</li></ul>",
            "key_concepts": ["journey map", "friction point", "user emotion mapping", "end-to-end process"],
            "practical_exercise": {
                "title": "Map a User Journey",
                "instructions": "Using your Day 4 persona, map their end-to-end journey through the problem area in at least 4 steps. For each step, note what they do, how they feel, and any friction. Identify and label the single highest-friction step. Submit the full journey map."
            },
            "quiz": [
                {"question": "What is the purpose of mapping a user's full journey before building a solution?", "options": ["To make the process take longer for no reason", "To ensure the real pain point is identified, which may differ from initial assumptions", "It is only useful for marketing purposes", "To replace the need for user interviews"], "correct_index": 1, "explanation": "A full journey map often reveals that the actual highest-friction point differs from where the team initially assumed the problem was."},
                {"question": "How do you typically identify the highest-value opportunity within a journey map?", "options": ["The very first step is always the highest priority", "The step with the strongest negative emotion or friction", "The step that takes the least amount of time", "Whichever step the team personally prefers to build"], "correct_index": 1, "explanation": "The step where users feel the most frustration or friction usually represents the biggest opportunity for improvement."},
                {"question": "In the worked example, what was the actual highest-friction step?", "options": ["Realizing the need for income", "Asking friends or scrolling social media", "Finding a posting that was already outdated/filled", "Giving up the search entirely"], "correct_index": 2, "explanation": "The sharpest frustration came from finding stale, already-filled postings — the information's staleness, not just the searching itself."}
            ],
            "resources": []
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "From Problem to Prioritized Plan",
            "title": "Turning Problems Into a Backlog of Potential Features",
            "learning_objective": "By the end of this class, you will be able to translate a validated problem and journey map into a list of at least 8 candidate features.",
            "duration_minutes": 25,
            "content_html": "<p>Once a problem is well understood, the next step is generating a wide range of potential solutions before narrowing down — jumping to just one idea too early often means missing a better option. A backlog starts broad, then gets ruthlessly cut.</p><h2>From Friction Point to Feature Ideas</h2><p>For your identified highest-friction step, brainstorm multiple possible feature solutions — not just the first idea that comes to mind. Include both simple, low-effort ideas and more ambitious ones; you'll evaluate trade-offs later, not now.</p><h2>Worked Example: Feature Backlog for the Stale-Postings Problem</h2><p>1. Real-time job posting feed with timestamps. 2. \"Filled\" status tags updated by posters. 3. Push notifications for new postings matching saved criteria. 4. A \"still available?\" quick-check button for job seekers. 5. Verified-poster badges to filter spam listings. 6. <strong>A weekly digest email summarizing new postings, for users who don't want constant notifications.</strong> 7. In-app chat to ask the poster a quick question. 8. A save-for-later bookmark feature.</p><ul><li>Generate at least 8-10 ideas before evaluating any of them — quantity first, judgment later</li><li>Mix quick, simple ideas with more ambitious ones; don't self-censor at the brainstorm stage</li><li>Every idea should trace back to reducing friction at your identified highest-pain journey step</li></ul>",
            "key_concepts": ["feature backlog", "brainstorming", "solution generation", "idea breadth before judgment"],
            "practical_exercise": {
                "title": "Generate a Feature Backlog",
                "instructions": "Using your Day 5 journey map's highest-friction step, brainstorm a backlog of at least 8 distinct feature ideas that could address it. Don't evaluate or prioritize yet — just generate a wide range. Submit the full list of 8+ feature ideas."
            },
            "quiz": [
                {"question": "Why should a PM generate many feature ideas before narrowing down?", "options": ["It wastes time and should be skipped", "Jumping to the first idea too early risks missing a better solution", "Only one idea should ever be considered", "More ideas always confuses the team"], "correct_index": 1, "explanation": "Broad brainstorming before evaluation increases the chance of finding the best solution rather than settling on the first idea."},
                {"question": "What should every feature idea in the backlog trace back to?", "options": ["The team's personal preferences", "The identified highest-friction point in the user journey", "A competitor's existing feature", "The engineering team's favorite technology"], "correct_index": 1, "explanation": "Feature ideas should directly address the validated pain point, keeping the backlog grounded in real user needs."},
                {"question": "What is the recommended mindset during the initial brainstorming stage?", "options": ["Immediately judge and filter every idea as it's generated", "Generate a wide range of ideas, including both simple and ambitious ones, without self-censoring", "Only generate ideas that are technically easy to build", "Limit the list to exactly 3 ideas"], "correct_index": 1, "explanation": "Quantity and breadth come first in brainstorming; evaluation and prioritization happen in a separate, later step."}
            ],
            "resources": []
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "From Problem to Prioritized Plan",
            "title": "Prioritizing Features With the Impact vs Effort Matrix",
            "learning_objective": "By the end of this class, you will be able to plot a list of features on an impact vs effort matrix and identify the top priorities.",
            "duration_minutes": 25,
            "content_html": "<p>With a backlog of ideas in hand, a PM needs a fast, defensible way to decide what to build first. The impact vs effort matrix is one of the simplest and most widely used prioritization tools in real product teams, precisely because it's quick and easy to explain to stakeholders.</p><h2>The Four Quadrants</h2><p>High impact, low effort: \"quick wins\" — build these first. High impact, high effort: \"big bets\" — worth doing, but plan carefully. Low impact, low effort: \"fill-ins\" — fine to do if there's spare time, not a priority. Low impact, high effort: \"time sinks\" — usually should be cut entirely.</p><h2>Worked Example: Plotting the Job-Posting Backlog</h2><p>\"Filled\" status tags: high impact (directly fixes the staleness pain), low effort (a simple status field) — a quick win. Real-time feed with timestamps: high impact, higher effort (requires more infrastructure) — a big bet. In-app chat: <strong>lower impact for this specific problem, high effort to build safely — a time sink to deprioritize for now.</strong> Bookmark feature: low impact, low effort — a nice-to-have fill-in.</p><ul><li>Always plot impact against the SPECIFIC validated problem, not vague general value</li><li>Quick wins build team and stakeholder confidence early — don't skip them for the flashier big bet</li><li>Time sinks are the easiest priorities to cut, but often the hardest to say no to when a stakeholder is excited about them</li></ul>",
            "key_concepts": ["impact vs effort matrix", "quick wins", "big bets", "time sinks"],
            "practical_exercise": {
                "title": "Plot Your Backlog on the Matrix",
                "instructions": "Using your Day 6 feature backlog, plot each feature into one of the four quadrants (quick win, big bet, fill-in, time sink) with a one-sentence justification for each placement. Identify your top 3 priorities based on the matrix. Submit the full matrix breakdown and your top 3 picks."
            },
            "quiz": [
                {"question": "What type of feature should typically be built first according to the impact vs effort matrix?", "options": ["Low impact, high effort", "High impact, low effort (quick wins)", "Low impact, low effort", "Any feature regardless of quadrant"], "correct_index": 1, "explanation": "Quick wins deliver high value for low investment, making them the natural first priority in most prioritization frameworks."},
                {"question": "What is a 'time sink' in this framework?", "options": ["A high-impact, low-effort feature", "A low-impact, high-effort feature that usually should be cut", "Any feature that takes more than a week to build", "A feature with no clear owner"], "correct_index": 1, "explanation": "Time sinks require significant effort but deliver little value, making them prime candidates for deprioritization or removal."},
                {"question": "Why is it important to plot impact against the specific validated problem, not vague general value?", "options": ["Vague value assessments are just as reliable", "It keeps prioritization grounded in real evidence rather than guesswork", "The specific problem doesn't matter for prioritization", "It only matters for large companies"], "correct_index": 1, "explanation": "Grounding impact assessments in the validated problem prevents prioritization from becoming based on unfounded assumptions."}
            ],
            "resources": [{"label": "Atlassian Agile Resources", "url": "https://www.atlassian.com/agile"}]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "From Problem to Prioritized Plan",
            "title": "Defining an MVP — What's the Smallest Thing Worth Shipping?",
            "learning_objective": "By the end of this class, you will be able to define a minimum viable product scope that tests the core hypothesis with the least possible build effort.",
            "duration_minutes": 25,
            "content_html": "<p>New PMs often confuse \"minimum viable product\" with \"a smaller version of the full vision.\" A true MVP isn't a stripped-down final product — it's the smallest possible thing that tests whether your core assumption is correct at all.</p><h2>MVP as a Test, Not a Mini-Product</h2><p>Before defining an MVP, name the single riskiest assumption behind your idea — the thing that, if false, means the whole idea fails. The MVP should be designed specifically to test THAT assumption, cutting everything else, even if it feels incomplete.</p><h2>Worked Example: MVP for the Job-Posting Idea</h2><p>Riskiest assumption: \"Job posters will actually bother to mark their listing as filled.\" Full-vision feature set: real-time feed, notifications, verified badges, in-app chat, bookmarks. MVP: <strong>a simple WhatsApp-based system where posters reply \"FILLED\" to a bot, updating a lightweight shared spreadsheet-based feed — no app, no notifications, no polish.</strong> This tests the riskiest assumption (will posters actually update status?) with days of work, not months.</p><ul><li>Identify the riskiest assumption FIRST — the MVP exists to test that specific thing</li><li>An MVP can and should feel embarrassingly basic — that's a sign it's minimal enough</li><li>Resist the pressure to add \"just one more feature\" to the MVP; each addition dilutes the test</li></ul>",
            "key_concepts": ["minimum viable product", "riskiest assumption", "MVP scope", "hypothesis testing"],
            "practical_exercise": {
                "title": "Define Your MVP",
                "instructions": "Using your top 3 prioritized features from Day 7, identify the single riskiest assumption behind your product idea. Define an MVP scope that tests specifically that assumption with the least possible build effort. Submit the riskiest assumption and the MVP scope definition."
            },
            "quiz": [
                {"question": "What is a common misconception about MVPs that this lesson corrects?", "options": ["That an MVP should be free to build", "That an MVP is just a smaller version of the full final product, rather than a test of the riskiest assumption", "That MVPs are only for software products", "That MVPs should include every planned feature"], "correct_index": 1, "explanation": "An MVP isn't a stripped-down finished product — it's specifically designed to test whether the core assumption behind the idea holds true."},
                {"question": "What should be identified before defining an MVP's scope?", "options": ["The final marketing budget", "The single riskiest assumption behind the idea", "The company's five-year plan", "The exact final feature list"], "correct_index": 1, "explanation": "Naming the riskiest assumption first ensures the MVP is designed specifically to test the thing that could make or break the idea."},
                {"question": "Why might an MVP feel 'embarrassingly basic'?", "options": ["That means it was built incorrectly", "It's often a sign the MVP is appropriately minimal and focused on testing one core assumption", "MVPs should always look polished and complete", "Basic MVPs always fail"], "correct_index": 1, "explanation": "A truly minimal MVP strips away everything except what's needed to test the core assumption, which can feel very basic by design."}
            ],
            "resources": []
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "From Problem to Prioritized Plan",
            "title": "Setting Metrics That Actually Prove a Feature Worked",
            "learning_objective": "By the end of this class, you will be able to define a specific, measurable success metric for a feature before it's built.",
            "duration_minutes": 25,
            "content_html": "<p>Shipping a feature without deciding in advance how you'll know if it worked is one of the most common product mistakes — teams end up debating success after the fact with no clear answer. Defining the metric BEFORE building forces clearer thinking about what the feature is actually meant to achieve.</p><h2>Choosing a Metric That Matches the Goal</h2><p>A good metric is specific (not \"more engagement\" but a named, countable behavior), has a clear target (a number, not just a direction), and is realistically measurable with tools you actually have access to.</p><h2>Worked Example: Metric for the 'Filled' Status Feature</h2><p>Weak metric: \"Users like the filled status feature.\" Strong metric: <strong>\"At least 60% of job posters mark their listing as filled within 48 hours of it being filled, measured over the first month, up from an estimated 0% today.\"</strong> This metric is specific, has a clear target and timeframe, and directly tests the riskiest assumption from Day 8.</p><ul><li>A metric without a specific number is really just a hope, not a measurable target</li><li>Always define a baseline (what's happening today) alongside the target, so you can measure real change</li><li>Pick metrics you can realistically track with the tools and data access you actually have</li></ul>",
            "key_concepts": ["success metric", "measurable target", "baseline", "metric specificity"],
            "practical_exercise": {
                "title": "Define a Success Metric",
                "instructions": "Using your Day 8 MVP, define one specific, measurable success metric with a clear target number and timeframe. State the current baseline (even if estimated) and explain how you would realistically track this metric. Submit the metric definition."
            },
            "quiz": [
                {"question": "Why is 'users like the feature' considered a weak success metric?", "options": ["It is too specific", "It lacks a specific, measurable target and clear number", "Liking a feature is not a valid consideration", "It is technically impossible to measure"], "correct_index": 1, "explanation": "Without a specific, countable target, a metric like 'users like it' can't be objectively evaluated as success or failure."},
                {"question": "What should accompany a metric's target to measure real change?", "options": ["The company's total revenue", "A baseline showing what's happening today before the feature ships", "The number of team members involved", "A list of competitor features"], "correct_index": 1, "explanation": "A baseline provides the starting point needed to measure whether the feature actually caused meaningful change."},
                {"question": "Why should metrics be defined before a feature is built, not after?", "options": ["It has no real benefit either way", "Defining metrics upfront forces clearer thinking about what the feature should actually achieve", "Metrics can only be calculated before building, never after", "It is only a formality with no practical use"], "correct_index": 1, "explanation": "Pre-defining metrics clarifies the feature's purpose and avoids ambiguous, after-the-fact debates about whether it succeeded."}
            ],
            "resources": []
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "From Problem to Prioritized Plan",
            "title": "Building a Simple Product Roadmap",
            "learning_objective": "By the end of this class, you will be able to build a quarter-based product roadmap organized by theme rather than exact feature dates.",
            "duration_minutes": 30,
            "content_html": "<p>A roadmap is one of the most visible artifacts a PM produces — shared with executives, engineers, and sometimes investors. A common beginner mistake is making it a rigid list of exact dates, which breaks the moment reality shifts (and it always does).</p><h2>Theme-Based, Not Date-Locked Roadmaps</h2><p>Instead of \"Feature X ships March 15,\" organize by theme and rough time horizon: \"Now\" (this quarter, high confidence), \"Next\" (next quarter, directional), \"Later\" (beyond that, more speculative). Group related features under a theme (e.g. \"Trust & Verification\") rather than listing them as disconnected items.</p><h2>Worked Example: A Simple Now/Next/Later Roadmap</h2><p>Now: MVP status-update system (Theme: Reducing stale listings). Next: <strong>Push notifications for saved search criteria, verified-poster badges (Theme: Trust & Discovery).</strong> Later: In-app chat, richer filtering, employer dashboard (Theme: Platform Maturity). This structure communicates direction and priority without over-committing to dates the team can't guarantee.</p><ul><li>Now/Next/Later roadmaps set honest expectations without locking in dates that often slip</li><li>Grouping features into themes tells a clearer story than a flat feature list</li><li>A roadmap should be revisited and updated regularly — it is a living document, not a one-time deliverable</li></ul>",
            "key_concepts": ["product roadmap", "now-next-later", "theme-based planning", "roadmap communication"],
            "practical_exercise": {
                "title": "Build a Now/Next/Later Roadmap",
                "instructions": "Using your Day 6 feature backlog and Day 7 prioritization, organize your features into a Now/Next/Later roadmap, grouping related features under 2-3 named themes. Submit the full roadmap."
            },
            "quiz": [
                {"question": "Why is a rigid, date-locked roadmap considered risky?", "options": ["Dates are always accurate and never change", "It breaks the moment reality shifts, which happens frequently in product work", "Rigid roadmaps are required by most companies", "Date-locked roadmaps have no downsides"], "correct_index": 1, "explanation": "Exact date commitments are fragile because product timelines frequently shift due to new information or unforeseen challenges."},
                {"question": "What do the 'Now/Next/Later' categories represent?", "options": ["Three different product teams", "Rough time horizons with decreasing confidence further out", "Three pricing tiers", "Three types of user personas"], "correct_index": 1, "explanation": "Now/Next/Later communicates direction and relative priority with appropriately decreasing certainty as time horizons extend."},
                {"question": "Why group features under named themes rather than listing them flat?", "options": ["Themes have no communicative value", "Grouped themes tell a clearer strategic story than a disconnected feature list", "Flat lists are always preferred by stakeholders", "Themes are only used in marketing documents"], "correct_index": 1, "explanation": "Thematic grouping helps stakeholders understand the strategic narrative behind the roadmap, not just a list of disconnected items."}
            ],
            "resources": [{"label": "Atlassian Agile Resources", "url": "https://www.atlassian.com/agile"}]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Writing Requirements Real Teams Can Build From",
            "title": "What Goes Into a PRD and Why Engineers Actually Read It",
            "learning_objective": "By the end of this class, you will be able to outline the standard sections of a product requirements document (PRD) and explain the purpose of each.",
            "duration_minutes": 25,
            "content_html": "<p>A PRD (product requirements document) is the bridge between a prioritized idea and an actual engineering build. A poorly written PRD leads to wasted engineering time, scope confusion, and a finished feature that doesn't match what was actually needed.</p><h2>Standard PRD Sections and Their Purpose</h2><p>Problem/context: why this matters (so the team understands intent, not just instructions). Goals and success metrics: what \"done and working\" looks like. User stories/requirements: specific, testable statements of what the product must do. Out of scope: explicitly what is NOT being built this round, preventing scope creep. Open questions: unresolved decisions flagged honestly rather than hidden.</p><h2>Worked Example: Why 'Out of Scope' Matters</h2><p>A PRD for the status-update MVP explicitly states: \"Out of scope for this release: push notifications, verified badges, in-app chat.\" <strong>Without this section, an engineer might reasonably assume notifications are implied and build unplanned work, delaying the actual MVP test.</strong> Explicit scope boundaries protect the team's focus as much as the feature list itself does.</p><ul><li>A PRD's problem/context section prevents the team from building the letter of the request while missing its intent</li><li>Explicit 'out of scope' sections are as important as what IS in scope — ambiguity here causes real delays</li><li>Open questions should be listed honestly, not hidden — a PRD is a living document that gets refined as questions get answered</li></ul>",
            "key_concepts": ["PRD structure", "out of scope", "user stories", "open questions"],
            "practical_exercise": {
                "title": "Outline a PRD Structure",
                "instructions": "Using your Day 8 MVP definition, outline the section headers you would include in a full PRD (problem/context, goals/metrics, requirements, out of scope, open questions) and write 1-2 bullet points under each section header with real content from your project. Submit the outline."
            },
            "quiz": [
                {"question": "What is the purpose of the 'problem/context' section in a PRD?", "options": ["To list the engineering team's salaries", "To help the team understand the intent behind the request, not just literal instructions", "It is optional and rarely useful", "To describe the company's history"], "correct_index": 1, "explanation": "Providing context on why the problem matters helps the team make good judgment calls even when specifics aren't fully covered."},
                {"question": "Why is an 'out of scope' section important in a PRD?", "options": ["It has no real function", "It explicitly prevents scope creep by clarifying what is NOT being built this round", "It should list every possible future feature", "Out of scope sections are only used in large enterprises"], "correct_index": 1, "explanation": "Explicitly stating what is excluded prevents engineers from making unplanned assumptions that expand the project's scope."},
                {"question": "How should open questions be handled in a PRD?", "options": ["They should be hidden to appear more confident", "Listed honestly, since a PRD is a living document refined as answers emerge", "Removed entirely from any PRD", "Only senior PMs are allowed to have open questions"], "correct_index": 1, "explanation": "Honestly flagging unresolved questions keeps the PRD accurate and allows the document to evolve as the team learns more."}
            ],
            "resources": [{"label": "Atlassian Agile Resources", "url": "https://www.atlassian.com/agile"}]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Writing Requirements Real Teams Can Build From",
            "title": "Writing User Stories With Clear Acceptance Criteria",
            "learning_objective": "By the end of this class, you will be able to write a user story with specific, testable acceptance criteria that an engineer can build directly against.",
            "duration_minutes": 25,
            "content_html": "<p>A vague requirement (\"users should be able to update their listing status\") leaves too much open to interpretation, resulting in a build that technically satisfies the request but misses the real need. Acceptance criteria close that gap by defining exactly what \"done\" means.</p><h2>The User Story + Acceptance Criteria Format</h2><p>User story format: \"As a [user type], I want to [action], so that [benefit].\" Acceptance criteria: a bullet list of specific, testable conditions that must be true for the story to be considered complete — written so a tester could check each one with a clear yes/no.</p><h2>Worked Example</h2><p>User story: \"As a job poster, I want to mark my listing as filled, so that seekers don't waste time applying to closed positions.\" Acceptance criteria: <strong>\"Given a poster is viewing their own listing, when they tap 'Mark as Filled', the listing status updates to 'Filled' within 2 seconds, and the listing no longer appears in active search results for new seekers.\"</strong> Each condition here is specific and directly testable — an engineer knows exactly what to build, and a tester knows exactly what to check.</p><ul><li>Acceptance criteria should be specific enough that two different people would agree whether they're met</li><li>The \"Given/When/Then\" format is a common, clear way to structure acceptance criteria</li><li>Vague criteria like \"works well\" or \"is user-friendly\" are not testable and should be rewritten as specific conditions</li></ul>",
            "key_concepts": ["user story format", "acceptance criteria", "given-when-then", "testable requirements"],
            "practical_exercise": {
                "title": "Write Two User Stories With Acceptance Criteria",
                "instructions": "Using your Day 8 MVP, write two user stories in the 'As a... I want... so that...' format. For each, write at least 3 specific, testable acceptance criteria using the Given/When/Then structure. Submit both user stories with their acceptance criteria."
            },
            "quiz": [
                {"question": "What is the standard format for writing a user story?", "options": ["A technical specification document", "'As a [user type], I want to [action], so that [benefit]'", "A list of programming languages", "A budget spreadsheet"], "correct_index": 1, "explanation": "This format captures the user, the desired action, and the underlying benefit, keeping the requirement grounded in real user value."},
                {"question": "What makes acceptance criteria useful to engineers?", "options": ["They are vague enough to allow creative interpretation", "They are specific and testable, so two people would agree on whether they're met", "They only need to be written after the feature ships", "They replace the need for a user story"], "correct_index": 1, "explanation": "Specific, testable criteria eliminate ambiguity, ensuring the built feature matches what was actually intended."},
                {"question": "Why is 'works well' considered a poor acceptance criterion?", "options": ["It is too specific and restrictive", "It is not testable — two people could disagree on whether it's met", "It should always be included in every PRD", "It is the industry-standard phrasing"], "correct_index": 1, "explanation": "Vague phrases without a concrete, checkable condition can't be reliably verified as complete or not."}
            ],
            "resources": []
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Writing Requirements Real Teams Can Build From",
            "title": "Working With Wireframes and Communicating With Designers",
            "learning_objective": "By the end of this class, you will be able to sketch a basic low-fidelity wireframe communicating a feature's core layout and flow.",
            "duration_minutes": 25,
            "content_html": "<p>PMs don't need to be designers, but being able to sketch a rough wireframe helps communicate an idea faster than a paragraph of description, and it gives designers a useful starting point rather than a blank page.</p><h2>Low-Fidelity Wireframing Basics</h2><p>A wireframe is a simple, low-detail sketch showing layout and flow — boxes for content areas, lines for text, simple shapes for buttons. It deliberately avoids colors, fonts, or polish; the goal is communicating structure and flow, not visual design.</p><h2>Worked Example: Wireframing the 'Mark as Filled' Flow</h2><p>Screen 1: a box representing the listing card, with a labeled button \"Mark as Filled\" beneath it. Screen 2 (after tap): <strong>a simple confirmation box with the text \"Are you sure?\" and two buttons, \"Yes\" and \"Cancel\" — showing the flow includes a confirmation step to prevent accidental taps.</strong> Screen 3: the listing card shown again, now with a greyed-out \"Filled\" label replacing the button. This simple three-screen sketch communicates the entire flow clearly, even hand-drawn.</p><ul><li>A wireframe's job is to communicate structure and flow, not to look polished — even hand-drawn sketches work</li><li>Always show the flow across multiple screens/states, not just one static screen</li><li>Bring wireframes to designers as a starting conversation, not a final instruction — invite their expertise, don't just hand over instructions</li></ul>",
            "key_concepts": ["low-fidelity wireframe", "flow sketching", "PM-designer collaboration", "structure over polish"],
            "practical_exercise": {
                "title": "Sketch a Wireframe Flow",
                "instructions": "Using one of your Day 12 user stories, sketch a low-fidelity wireframe showing at least 2-3 screens/states representing the flow (can be hand-drawn and photographed, or made with simple boxes in any tool). Write a one-paragraph description of the flow alongside the sketch. Submit the wireframe and description."
            },
            "quiz": [
                {"question": "What is the main goal of a low-fidelity wireframe?", "options": ["To show final visual polish with exact colors and fonts", "To communicate layout and flow clearly and quickly", "To replace the need for any designer involvement", "To serve as the final production-ready design"], "correct_index": 1, "explanation": "Low-fidelity wireframes intentionally skip visual polish to focus purely on communicating structure and flow."},
                {"question": "Why should a wireframe typically show multiple screens or states?", "options": ["A single screen is always sufficient", "It communicates the full flow a user experiences, not just one moment", "Multiple screens are only needed for complex apps", "It is purely a stylistic preference with no functional purpose"], "correct_index": 1, "explanation": "Showing the flow across states (like before/after an action) communicates the complete user experience, not an isolated snapshot."},
                {"question": "How should a PM present wireframes to a designer?", "options": ["As final instructions with no room for input", "As a starting conversation that invites the designer's expertise", "Wireframes should never be shown to designers", "Only after the feature has already been built"], "correct_index": 1, "explanation": "Wireframes work best as collaborative starting points, giving designers useful context while still inviting their creative expertise."}
            ],
            "resources": []
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Writing Requirements Real Teams Can Build From",
            "title": "Case Study: Diagnosing a Feature That Shipped but Failed",
            "learning_objective": "By the end of this class, you will be able to analyze a shipped feature's failure and trace it back to a specific gap in discovery, prioritization, or requirements.",
            "duration_minutes": 30,
            "content_html": "<p>Studying real product failures — not just successes — builds sharper judgment faster than reading about wins alone. Most feature failures trace back to a specific, identifiable gap earlier in the process, not just \"bad luck.\"</p><h2>A Framework for Diagnosing a Failed Feature</h2><p>Ask: Was the problem actually validated with real user evidence, or assumed? Was the riskiest assumption identified and tested, or skipped? Were requirements specific enough, or left ambiguous? Was a success metric defined before building, or decided after the fact?</p><h2>Worked Example: Diagnosing a Common Failure Pattern</h2><p>Scenario: A team builds an elaborate \"verified poster\" badge system, but usage stays near zero after launch. Diagnosis: <strong>the team skipped user validation, assuming spam/trust was the top concern, when discovery interviews (if done) would have revealed staleness of listings was the actual dominant frustration — verification wasn't the riskiest assumption at all.</strong> The failure traces back to Day 2-5 discovery being skipped, not to the engineering or design execution, which may have been technically excellent.</p><ul><li>Most feature failures trace back to a skipped or rushed discovery step, not poor execution</li><li>Diagnosing failure requires tracing back through the full pipeline: discovery, prioritization, requirements, metrics</li><li>A postmortem's value comes from identifying the SPECIFIC step that broke down, not vague lessons like \"we should communicate better\"</li></ul>",
            "key_concepts": ["feature postmortem", "failure diagnosis", "discovery gap", "root cause tracing"],
            "practical_exercise": {
                "title": "Diagnose a Feature Failure Scenario",
                "instructions": "You are given this scenario: a team built a full in-app messaging feature that engineering delivered on time and bug-free, but fewer than 2% of users ever used it after 3 months. Write a diagnosis tracing this failure back through discovery, prioritization, requirements, and metrics, identifying the most likely specific breakdown point. Submit your written diagnosis."
            },
            "quiz": [
                {"question": "According to this lesson, where do most feature failures typically originate?", "options": ["Always in the engineering execution", "Often in a skipped or rushed discovery step, even when execution is technically excellent", "Only in marketing and launch mistakes", "Failures are always random and untraceable"], "correct_index": 1, "explanation": "Many feature failures trace back to inadequate problem validation earlier in the process, not flaws in the technical build itself."},
                {"question": "What does a useful failure diagnosis require?", "options": ["Vague lessons like 'communicate better'", "Tracing the failure through the full pipeline to identify a specific breakdown point", "Blaming a single team member", "Ignoring the failure and moving to the next project"], "correct_index": 1, "explanation": "Specific, traceable diagnosis (which exact step broke down) produces more actionable lessons than vague generalizations."},
                {"question": "In the worked verified-badge example, what was the actual root cause of the feature's failure?", "options": ["Poor engineering execution", "Skipped user validation that would have revealed a different, more pressing problem", "A lack of marketing budget", "The feature was too simple"], "correct_index": 1, "explanation": "The team assumed trust/verification was the top concern without validating it, missing that staleness was the real dominant issue."}
            ],
            "resources": []
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Writing Requirements Real Teams Can Build From",
            "title": "Running a Sprint Planning Conversation as a PM",
            "learning_objective": "By the end of this class, you will be able to prepare and structure a sprint planning conversation, including a prioritized, right-sized set of stories.",
            "duration_minutes": 25,
            "content_html": "<p>Sprint planning is where the roadmap and PRD meet real execution — a PM who shows up unprepared wastes the whole team's time in the room. Understanding this rhythm, even from a junior seat, is expected knowledge in most tech product roles.</p><h2>Preparing for Sprint Planning</h2><p>Before the meeting: have a prioritized, refined list of user stories ready (not a vague backlog dump), each with clear acceptance criteria (Day 12). Estimate roughly how much fits in the sprint based on team capacity and past velocity, and be ready to explain WHY each story is prioritized where it is.</p><h2>Worked Example: A Prepared Sprint Planning Agenda</h2><p>1. Quick context recap: the sprint's overall goal (e.g. \"ship and start testing the MVP status-update flow\"). 2. Review top 3-5 prioritized stories, one at a time, confirming the team understands acceptance criteria. 3. <strong>Flag any story that seems too large, and offer to help break it into smaller pieces together with the engineer, rather than dictating a solution.</strong> 4. Confirm what's explicitly out of scope for this sprint.</p><ul><li>Arrive with prioritized, well-defined stories — sprint planning is not the time to figure out priorities from scratch</li><li>State the sprint's overall goal upfront so individual stories are understood in context, not in isolation</li><li>Collaborate on breaking down oversized stories rather than dictating technical solutions to engineers</li></ul>",
            "key_concepts": ["sprint planning", "sprint goal", "story sizing", "team capacity"],
            "practical_exercise": {
                "title": "Prepare a Sprint Planning Agenda",
                "instructions": "Using your Day 12 user stories, prepare a sprint planning agenda: state the sprint's overall goal, list your top 3-5 prioritized stories with a one-line justification for their order, and note what's explicitly out of scope for this sprint. Submit the agenda."
            },
            "quiz": [
                {"question": "What should a PM have ready before a sprint planning meeting?", "options": ["A vague, unrefined backlog dump", "A prioritized, refined list of stories with clear acceptance criteria", "Nothing, priorities should be decided live in the meeting", "Only the engineering team's task list"], "correct_index": 1, "explanation": "Coming prepared with prioritized, well-defined stories makes sprint planning efficient and productive for the whole team."},
                {"question": "Why should a PM state the sprint's overall goal at the start of planning?", "options": ["It has no real purpose", "It gives individual stories context so the team understands why they matter together", "Sprint goals are only relevant to executives", "It replaces the need for individual stories"], "correct_index": 1, "explanation": "A clear sprint goal helps the team see how individual stories connect to a shared purpose, not just a disconnected task list."},
                {"question": "How should a PM handle a story that seems too large for the sprint?", "options": ["Dictate exactly how to technically break it down", "Flag it and collaborate with the engineer to break it into smaller pieces", "Remove it from the roadmap entirely without discussion", "Ignore the sizing concern and proceed anyway"], "correct_index": 1, "explanation": "Collaborative breakdown respects engineering expertise while still addressing the sizing concern the PM identified."}
            ],
            "resources": [{"label": "Atlassian Agile Resources", "url": "https://www.atlassian.com/agile"}]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Execution, Data, and Stakeholders",
            "title": "Reading Basic Product Analytics to Understand User Behavior",
            "learning_objective": "By the end of this class, you will be able to interpret basic product usage data (activation, retention, drop-off) to identify a specific area for improvement.",
            "duration_minutes": 30,
            "content_html": "<p>A PM who never looks at usage data is flying blind — guessing about what users do instead of knowing. You don't need to be a data scientist, but understanding a handful of core product metrics is expected baseline knowledge in almost every PM role.</p><h2>Core Metrics Every PM Should Know</h2><p>Activation: did a new user successfully experience the core value (not just sign up)? Retention: do users come back over time? Drop-off/funnel analysis: at which specific step do users abandon a multi-step process?</p><h2>Worked Example: Diagnosing a Funnel</h2><p>Signup funnel data: 100 people start signup, 80 verify their phone number, 45 complete profile setup, 40 post their first listing. Diagnosis: <strong>the sharpest drop-off (80 to 45) happens at profile setup, not signup or phone verification — this is the specific step to investigate and simplify, not the whole onboarding flow.</strong></p><ul><li>Match each metric to a specific stage of the user's experience, not a vague overall 'engagement' number</li><li>Funnel analysis reveals WHERE users are lost, which is more actionable than an aggregate conversion rate alone</li><li>Always investigate the step with the sharpest drop first — it usually offers the highest-leverage fix</li></ul>",
            "key_concepts": ["activation", "retention", "funnel analysis", "drop-off diagnosis"],
            "practical_exercise": {
                "title": "Diagnose a Funnel Scenario",
                "instructions": "You are given this funnel data: 200 users view a landing page, 120 start a signup form, 100 complete the form, 30 use the core feature within their first week. Identify the step with the sharpest drop-off and write a short diagnosis of what might be happening there, plus one specific hypothesis to test. Submit your diagnosis."
            },
            "quiz": [
                {"question": "What does 'activation' measure in product analytics?", "options": ["Total company revenue", "Whether a new user successfully experienced the product's core value", "The number of employees on the product team", "The exact date a feature launched"], "correct_index": 1, "explanation": "Activation specifically tracks whether new users get to experience real value, not just complete signup."},
                {"question": "What does funnel analysis reveal that an aggregate conversion rate alone does not?", "options": ["Nothing additional", "The specific step where users are dropping off", "The total company budget", "The names of individual users"], "correct_index": 1, "explanation": "Funnel analysis breaks a process into steps, showing exactly where users abandon it rather than just an overall conversion number."},
                {"question": "In the worked funnel example, which step had the sharpest drop-off?", "options": ["Signup to phone verification", "Phone verification to profile setup completion", "Profile setup to first listing post", "There was no meaningful drop-off"], "correct_index": 1, "explanation": "The drop from 80 (verified) to 45 (completed profile) was the sharpest, pointing to profile setup as the key friction point."}
            ],
            "resources": []
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Execution, Data, and Stakeholders",
            "title": "Running a Lightweight A/B Test Without a Data Team",
            "learning_objective": "By the end of this class, you will be able to design a simple A/B test with a clear hypothesis, control, and variant for a product change.",
            "duration_minutes": 25,
            "content_html": "<p>Not every product decision needs a full experimentation platform — many early-stage teams and junior PMs run lightweight, manual A/B tests to validate a change before committing fully. Knowing how to design one correctly, even simply, is a valuable and practical skill.</p><h2>Designing a Simple A/B Test</h2><p>Write a clear hypothesis first: \"If we [change], then [metric] will improve, because [reasoning].\" Define your control (the current experience) and variant (the new version) precisely. Decide your success metric and how long you'll run the test before evaluating results.</p><h2>Worked Example: Testing the Profile Setup Drop-Off</h2><p>Hypothesis: \"If we reduce the profile setup form from 8 fields to 3 required fields, then completion rate will improve, because users are likely abandoning due to form length/friction.\" Control: current 8-field form (50% of new users). Variant: <strong>simplified 3-field form, with remaining fields made optional and requestable later (other 50% of new users).</strong> Metric: profile completion rate, measured over 2 weeks.</p><ul><li>A hypothesis should state the change, the expected metric impact, AND the underlying reasoning — not just a guess</li><li>Keep the control and variant identical except for the one variable being tested, just like the copywriting A/B principle</li><li>Decide your test duration and evaluation metric BEFORE launching, to avoid biased after-the-fact interpretation</li></ul>",
            "key_concepts": ["A/B test design", "hypothesis statement", "control and variant", "single-variable testing"],
            "practical_exercise": {
                "title": "Design an A/B Test for Your Funnel Diagnosis",
                "instructions": "Using your Day 16 funnel diagnosis, design a simple A/B test to address the drop-off you identified. Write the hypothesis (if/then/because), define the control and variant precisely, and state your success metric and test duration. Submit the full A/B test design."
            },
            "quiz": [
                {"question": "What three parts should a good A/B test hypothesis include?", "options": ["Budget, timeline, and team size", "The change, the expected metric impact, and the underlying reasoning", "Only a guess with no reasoning", "The names of the test participants"], "correct_index": 1, "explanation": "A complete hypothesis states what will change, what metric should improve, and why that improvement is expected."},
                {"question": "What should differ between the control and variant in a well-designed A/B test?", "options": ["As many variables as possible", "Ideally just the one variable being tested", "Nothing should differ at all", "Only the target audience"], "correct_index": 1, "explanation": "Isolating a single variable ensures any observed difference in results can be confidently attributed to that specific change."},
                {"question": "When should the test duration and evaluation metric be decided?", "options": ["After seeing early results, to adjust as needed", "Before launching the test, to avoid biased after-the-fact interpretation", "Duration and metrics don't need to be decided in advance", "Only after the test has fully concluded"], "correct_index": 1, "explanation": "Pre-committing to duration and metrics prevents cherry-picking results or changing evaluation criteria based on what looks favorable."}
            ],
            "resources": []
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Execution, Data, and Stakeholders",
            "title": "Managing Stakeholders Who Want Everything Built Now",
            "learning_objective": "By the end of this class, you will be able to respond to a stakeholder's urgent, unprioritized feature request with a structured, evidence-based response.",
            "duration_minutes": 25,
            "content_html": "<p>Every PM eventually faces a stakeholder (an executive, a sales lead, a founder) insisting a pet feature must be built immediately, disrupting the roadmap. How a PM handles this moment — without simply saying yes to everything or dismissively saying no — is a defining professional skill.</p><h2>The Structured Response Framework</h2><p>Acknowledge the request and the underlying business reason behind it. Ask what specific problem or evidence is driving the urgency. Show where it would fit relative to current priorities (using your Day 7 matrix or Day 10 roadmap), and what would need to be deprioritized to fit it in NOW versus later.</p><h2>Worked Example: Handling an Urgent Executive Request</h2><p>Executive: \"A big client wants in-app chat, we need it by next week.\" Weak response: either an unquestioning \"okay\" or a dismissive \"that's not on the roadmap.\" Strong response: <strong>\"Got it — can you help me understand what's driving the urgency with this specific client? If we build in-app chat now, it would mean pausing the status-update MVP test that's currently our top priority. Let's look at the trade-off together and decide what makes sense.\"</strong></p><ul><li>Never simply say yes to every urgent request — it erodes the whole team's ability to focus on validated priorities</li><li>Never simply say no either — dismissiveness damages stakeholder trust and misses potentially real signal</li><li>Making trade-offs visible (what gets deprioritized) turns a conflict into a shared, informed decision</li></ul>",
            "key_concepts": ["stakeholder management", "trade-off visibility", "urgent request handling", "prioritization defense"],
            "practical_exercise": {
                "title": "Respond to an Urgent Stakeholder Request",
                "instructions": "You receive this message from a founder: 'I just talked to an investor who thinks we need a referral program immediately, can we add it to this sprint?' Write your full structured response, including a clarifying question and a clear statement of the trade-off involved. Submit your written response."
            },
            "quiz": [
                {"question": "What is the risk of a PM simply saying yes to every urgent stakeholder request?", "options": ["There is no risk at all", "It erodes the team's ability to focus on validated priorities", "Stakeholders always appreciate unconditional agreement", "It has no effect on the roadmap"], "correct_index": 1, "explanation": "Constantly accommodating urgent requests without evaluation undermines focus on the priorities that evidence actually supports."},
                {"question": "What should a PM ask when facing an urgent, unprioritized request?", "options": ["Nothing, just proceed immediately", "What specific problem or evidence is driving the urgency", "Only how much budget is available", "Whether the requester is senior enough to be obeyed"], "correct_index": 1, "explanation": "Understanding the underlying evidence or problem helps evaluate whether the request truly warrants reprioritization."},
                {"question": "Why is making trade-offs visible to a stakeholder an effective technique?", "options": ["It hides the real cost of the request", "It turns a potential conflict into a shared, informed decision", "Trade-offs should never be discussed with stakeholders", "It has no impact on stakeholder trust"], "correct_index": 1, "explanation": "Showing what would need to be deprioritized helps the stakeholder understand the real cost, leading to a more collaborative decision."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Execution, Data, and Stakeholders",
            "title": "Writing a Clear Product Status Update",
            "learning_objective": "By the end of this class, you will be able to write a concise weekly product status update covering progress, risks, and next steps.",
            "duration_minutes": 25,
            "content_html": "<p>Stakeholders and leadership rarely have time to dig into a project's details themselves — a clear, regular status update is how a PM keeps trust and visibility without requiring constant meetings. This is a small habit that has an outsized effect on how a PM is perceived.</p><h2>The Three-Part Status Update</h2><p>Progress: what shipped or moved forward since the last update, in plain language. Risks: anything that could threaten the timeline or goal, stated honestly, not hidden. Next steps: what's happening next and any decisions needed from stakeholders.</p><h2>Worked Example: A Weekly Status Update</h2><p>Progress: \"MVP status-update flow is built and in internal testing; 3 of 5 planned test users have tried it so far.\" Risks: <strong>\"WhatsApp Business API approval is taking longer than expected — this could delay the public test by up to a week. Investigating a backup manual process in the meantime.\"</strong> Next steps: \"Complete testing with remaining 2 users this week; need a decision by Friday on whether to proceed with the backup process if API approval isn't through.\"</p><ul><li>Always report risks honestly and early — surprising stakeholders late with bad news damages trust far more than the risk itself</li><li>Keep updates short and scannable — a busy stakeholder should get the full picture in under a minute of reading</li><li>End with clear next steps and any specific decisions needed, so the update drives action, not just awareness</li></ul>",
            "key_concepts": ["status update", "risk communication", "stakeholder visibility", "next steps"],
            "practical_exercise": {
                "title": "Write a Weekly Status Update",
                "instructions": "Using your final project idea's progress so far, write a realistic weekly status update covering progress, risks, and next steps, following the structure taught today. Keep it concise and scannable. Submit the status update."
            },
            "quiz": [
                {"question": "What are the three core parts of a well-structured status update?", "options": ["Budget, team, and location", "Progress, risks, and next steps", "History, present, and future", "Problem, solution, and marketing"], "correct_index": 1, "explanation": "A clear status update covers what's happened, what could go wrong, and what's coming next, giving stakeholders a full picture quickly."},
                {"question": "Why should risks be reported honestly and early in a status update?", "options": ["Risks should always be hidden to appear more competent", "Surprising stakeholders late with bad news damages trust more than the risk itself", "Risks are irrelevant to stakeholders", "Only positive news should be shared"], "correct_index": 1, "explanation": "Early, honest risk communication maintains stakeholder trust, whereas hidden risks that surface late are far more damaging."},
                {"question": "Why should a status update end with clear next steps and needed decisions?", "options": ["It has no practical benefit", "It drives action rather than just passive awareness", "Next steps should never be included in status updates", "It is only relevant for the PM's personal records"], "correct_index": 1, "explanation": "Ending with specific next steps and decisions turns the update into something stakeholders can act on, not just read."}
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Execution, Data, and Stakeholders",
            "title": "Competitive Analysis Without Copying the Competition",
            "learning_objective": "By the end of this class, you will be able to conduct a competitive analysis that identifies a genuine gap or opportunity, not just a feature checklist.",
            "duration_minutes": 25,
            "content_html": "<p>Beginner competitive analysis often becomes a shallow feature checklist (\"they have X, we should have X too\") that leads to copying rather than genuine strategic thinking. A useful competitive analysis instead reveals where real opportunity exists.</p><h2>Analyzing for Opportunity, Not Just Features</h2><p>For each competitor, note: who they serve best (their strongest user segment), what they do well, and — most importantly — what user complaint or gap shows up repeatedly in their reviews or public feedback. That gap is often your real opportunity.</p><h2>Worked Example: Analyzing an Existing Job-Board Competitor</h2><p>Competitor: an established job-listing app. Serves best: full-time corporate job seekers. Does well: strong employer verification, professional design. Gap found in reviews: <strong>multiple reviews mention the app is \"too formal\" and \"doesn't have quick informal gigs,\" and listings for part-time/informal work are rare and poorly categorized.</strong> This reveals a specific opportunity — informal, part-time gig discovery — rather than just copying their existing verification feature.</p><ul><li>A feature checklist against competitors leads to copying, not strategic differentiation</li><li>Real user complaints in reviews are a goldmine for finding genuine, validated gaps</li><li>The goal of competitive analysis is finding what to do DIFFERENTLY, not matching feature-for-feature</li></ul>",
            "key_concepts": ["competitive analysis", "market gap", "review mining", "differentiation"],
            "practical_exercise": {
                "title": "Conduct a Gap-Focused Competitive Analysis",
                "instructions": "Choose one real competitor relevant to your final project idea. Research (or realistically estimate based on what you know) who they serve best, what they do well, and any recurring complaint or gap you can identify from reviews or public feedback. Write a short analysis identifying the specific opportunity this reveals for your product. Submit the analysis."
            },
            "quiz": [
                {"question": "What is a common weakness of beginner competitive analysis?", "options": ["It is too focused on finding gaps", "It becomes a shallow feature checklist that leads to copying competitors", "It never looks at competitor products at all", "It always identifies genuine strategic opportunities"], "correct_index": 1, "explanation": "Simply listing competitor features and matching them leads to imitation rather than genuine strategic differentiation."},
                {"question": "Where can a PM often find genuine, validated gaps in a competitor's offering?", "options": ["The competitor's marketing materials only", "Recurring complaints in user reviews or public feedback", "The competitor's internal financial reports", "Random guessing"], "correct_index": 1, "explanation": "Real user complaints in reviews reveal actual pain points that competitors haven't addressed, pointing to genuine opportunities."},
                {"question": "What is the real goal of competitive analysis, according to this lesson?", "options": ["Matching every competitor feature exactly", "Finding what to do differently, not just replicating existing features", "Avoiding any research into competitors", "Copying the competitor's pricing exactly"], "correct_index": 1, "explanation": "Effective competitive analysis identifies opportunities for differentiation rather than simply mirroring what already exists."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Go-to-Market and Launch Strategy",
            "title": "Building a Go-to-Market Plan From Scratch",
            "learning_objective": "By the end of this class, you will be able to outline a go-to-market plan covering target audience, positioning, channels, and launch timeline.",
            "duration_minutes": 30,
            "content_html": "<p>Building a great product means little if nobody knows it exists or understands why it matters to them. A go-to-market (GTM) plan is how a PM connects a finished product to real users at launch — and it's expected knowledge even for junior product roles, especially at startups.</p><h2>The Core Components of a GTM Plan</h2><p>Target audience: the specific first segment to focus launch efforts on (not everyone at once). Positioning: one clear sentence on why this product matters to that audience, versus alternatives. Channels: where you'll actually reach that audience (specific communities, platforms, partnerships). Timeline: a rough sequence of pre-launch, launch day, and post-launch activities.</p><h2>Worked Example: GTM for the Job-Posting MVP</h2><p>Target audience: final-year students at 2-3 specific Lagos universities, chosen because that's where initial research happened. Positioning: \"The fastest way to find part-time gigs that are still actually open.\" Channels: <strong>campus WhatsApp groups, partnerships with 2-3 student organization leaders willing to share the tool, and a small number of targeted Instagram posts.</strong> Timeline: 1 week of soft testing with the original interview participants, then a 2-week campus-focused soft launch before considering wider expansion.</p><ul><li>Never launch to \"everyone\" at once — a focused first audience makes early feedback and iteration far more manageable</li><li>Positioning should be a single, clear sentence a stranger could understand in seconds</li><li>Choose channels based on where your SPECIFIC audience actually spends time, not generic 'post on social media'</li></ul>",
            "key_concepts": ["go-to-market plan", "target audience", "positioning statement", "launch channels"],
            "practical_exercise": {
                "title": "Outline Your Go-to-Market Plan",
                "instructions": "Using your final project idea, outline a GTM plan covering: target audience (a specific first segment), a one-sentence positioning statement, 2-3 specific channels you'd use to reach that audience, and a rough pre-launch/launch/post-launch timeline. Submit the full GTM outline."
            },
            "quiz": [
                {"question": "Why should a launch typically target a specific first audience rather than everyone at once?", "options": ["Targeting everyone is always more effective", "A focused audience makes early feedback and iteration more manageable", "Broad launches have no downsides", "It is a legal requirement"], "correct_index": 1, "explanation": "Starting with a focused segment allows the team to gather clearer, more actionable feedback before scaling to a wider audience."},
                {"question": "What should a positioning statement communicate?", "options": ["A list of every technical feature", "One clear sentence on why the product matters to the target audience versus alternatives", "The company's internal org chart", "A detailed pricing breakdown"], "correct_index": 1, "explanation": "A strong positioning statement is a single, clear sentence that quickly communicates the product's value to its intended audience."},
                {"question": "How should launch channels be selected?", "options": ["Randomly, from a general list of all social platforms", "Based on where the specific target audience actually spends time", "Only paid advertising should ever be used", "Channels don't matter for a successful launch"], "correct_index": 1, "explanation": "Effective channel selection is grounded in real knowledge of where the specific target audience can genuinely be reached."}
            ],
            "resources": [{"label": "PMI Resources", "url": "https://www.pmi.org"}]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Go-to-Market and Launch Strategy",
            "title": "Writing Launch Communications for Different Audiences",
            "learning_objective": "By the end of this class, you will be able to write launch messaging tailored to two different audiences — end users and internal stakeholders.",
            "duration_minutes": 25,
            "content_html": "<p>The same launch needs different messages for different audiences — what excites an end user is different from what a stakeholder or investor needs to know. A PM who sends one generic message to everyone usually undersells the launch to at least one group.</p><h2>Tailoring the Message by Audience</h2><p>End users: focus on the benefit to THEM — what changes for their daily experience, in simple, exciting language. Internal stakeholders/leadership: focus on the business rationale — what problem this solves, what metric it's expected to move, and what's next.</p><h2>Worked Example: Two Versions of the Same Launch</h2><p>End-user message: \"No more wasted applications to gigs that are already filled. Now every listing shows real-time status — try it today.\" Internal stakeholder update: <strong>\"We've launched the status-update MVP to our initial 200-user test group, directly testing our riskiest assumption that posters will update listing status. Target: 60% update rate within 48 hours. Results expected by [date], which will inform our next roadmap decision.\"</strong></p><ul><li>End-user messaging should be simple, benefit-focused, and free of internal jargon (MVP, riskiest assumption, etc.)</li><li>Internal messaging should connect the launch back to the original hypothesis and metric, showing strategic reasoning</li><li>Never send internal, jargon-heavy language directly to end users — it confuses rather than excites them</li></ul>",
            "key_concepts": ["launch messaging", "audience-tailored communication", "user-facing copy", "internal stakeholder update"],
            "practical_exercise": {
                "title": "Write Two Launch Messages",
                "instructions": "Using your final project idea, write two versions of a launch announcement: one for end users (simple, benefit-focused) and one for internal stakeholders (strategic, metric-focused). Submit both versions."
            },
            "quiz": [
                {"question": "Why should launch messaging differ between end users and internal stakeholders?", "options": ["It shouldn't differ; one message fits all audiences", "Each audience cares about different things — user benefit versus business rationale", "Internal stakeholders never need launch updates", "End users prefer technical jargon"], "correct_index": 1, "explanation": "End users care about what changes for them personally, while stakeholders care about strategic rationale and metrics — different messages serve each best."},
                {"question": "What should end-user launch messaging generally avoid?", "options": ["Simple, benefit-focused language", "Internal jargon like 'MVP' or 'riskiest assumption'", "Mentioning what changes for the user", "Being exciting or engaging"], "correct_index": 1, "explanation": "Internal terminology confuses end users rather than exciting them about the actual benefit they'll experience."},
                {"question": "What should internal stakeholder launch updates typically connect back to?", "options": ["Nothing in particular", "The original hypothesis and success metric being tested", "Only the visual design of the feature", "A list of every engineer who worked on it"], "correct_index": 1, "explanation": "Connecting the launch to the original hypothesis and metric shows stakeholders the strategic reasoning behind the release."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Go-to-Market and Launch Strategy",
            "title": "Ethical Product Decisions — Dark Patterns and User Trust",
            "learning_objective": "By the end of this class, you will be able to identify manipulative dark patterns in product design and propose an ethical alternative that still meets business goals.",
            "duration_minutes": 25,
            "content_html": "<p>Product decisions have real power over user behavior — and that power can be used to manipulate rather than serve. Business pressure sometimes pushes toward dark patterns; a professional PM understands the line and can defend an ethical alternative that still meets real business goals.</p><h2>Common Product Dark Patterns</h2><p>Confirmshaming: guilt-tripping decline options (\"No, I don't want to save money\"). Forced continuity: making cancellation deliberately difficult after a free trial. Hidden costs: revealing fees only at the final checkout step. Roach motel: easy to sign up, deliberately hard to leave.</p><h2>Worked Example: Redesigning a Cancellation Flow Ethically</h2><p>Dark pattern version: cancellation requires calling a phone line during limited hours, buried three menus deep. Ethical version: <strong>a clear, one-click cancellation option in account settings, paired with a genuine, non-manipulative retention offer shown BEFORE the cancellation completes (e.g. a real discount or a pause option) — giving the business a fair chance to retain the user without trapping them.</strong> The ethical version can still reduce churn, just without deception or friction abuse.</p><ul><li>Making an action hard to complete (like cancellation) is manipulation, not good business design</li><li>A genuine, honest retention offer can coexist with an easy, honest exit path</li><li>PMs should push back professionally when business pressure pushes toward dark patterns, citing long-term trust cost</li></ul>",
            "key_concepts": ["dark patterns", "confirmshaming", "forced continuity", "ethical retention design"],
            "practical_exercise": {
                "title": "Identify and Redesign a Dark Pattern",
                "instructions": "Describe one realistic example of a product dark pattern (confirmshaming, forced continuity, hidden costs, or roach motel) as a bad example. Then describe an ethical redesign that still serves a reasonable business goal. Submit both descriptions with a one-sentence explanation of what made the first one manipulative."
            },
            "quiz": [
                {"question": "What is 'forced continuity' as a dark pattern?", "options": ["Making it easy to cancel a subscription at any time", "Making cancellation deliberately difficult after a free trial", "A feature that improves user retention honestly", "A pricing model with no hidden fees"], "correct_index": 1, "explanation": "Forced continuity deliberately obstructs cancellation, trapping users in a subscription against their genuine preference."},
                {"question": "Can a business ethically try to retain a user who wants to cancel?", "options": ["No, retention offers are always manipulative", "Yes, as long as the exit path remains genuinely easy and the offer is honest", "Only through hidden fees", "Retention should never be attempted"], "correct_index": 1, "explanation": "An honest, non-obstructive retention offer alongside an easy cancellation path is ethical, unlike blocking the exit entirely."},
                {"question": "What should a PM do when business pressure pushes toward a dark pattern?", "options": ["Always comply without question", "Push back professionally, citing the long-term cost to user trust", "Dark patterns are never actually a concern", "Immediately escalate to legal action"], "correct_index": 1, "explanation": "Professional PMs are expected to advocate against manipulative design, weighing long-term trust against short-term gains."}
            ],
            "resources": []
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Go-to-Market and Launch Strategy",
            "title": "Breaking Into Product Management — Landing Your First Role",
            "learning_objective": "By the end of this class, you will be able to identify realistic entry points into product management and build a targeted outreach plan.",
            "duration_minutes": 25,
            "content_html": "<p>Breaking into product management without prior PM experience is a well-known challenge — but there are real, proven entry paths, especially in fast-growing African tech ecosystems where associate and junior PM roles are increasingly common.</p><h2>Realistic Entry Points Into PM</h2><p>Associate/Junior PM roles: some companies hire directly for entry-level PM positions, especially at growing startups. Adjacent role transition: moving into PM from a related role (customer support, business analyst, engineering, design) within the same company, using inside knowledge as an advantage. Founding a small project: building and documenting a real (even tiny) product, exactly like this course's final project, as concrete proof of product thinking.</p><h2>Worked Example: A Targeted Outreach Plan</h2><p>Instead of applying broadly to \"PM jobs,\" identify 10 specific Nigerian or African startups whose product area genuinely interests you. For each, research a specific, small friction point in their existing product. <strong>Reach out with a short message referencing that specific observation, attaching your final project as evidence of real product thinking — not just a generic resume.</strong></p><ul><li>Companies hiring junior PMs value evidence of product thinking over formal titles or years of experience</li><li>An adjacent role inside a company you already work for is a legitimate, common path into PM</li><li>A specific, researched observation about a real company's product beats a generic application every time</li></ul>",
            "key_concepts": ["breaking into PM", "associate PM roles", "adjacent role transition", "targeted outreach"],
            "practical_exercise": {
                "title": "Build a Targeted Outreach Plan",
                "instructions": "Identify 3 real companies (Nigerian or African startups, or any company you're genuinely interested in) where you might target a PM-adjacent opportunity. For each, write one specific, researched observation about a friction point in their existing product, and draft a short outreach message referencing it. Submit the 3 companies, observations, and outreach messages."
            },
            "quiz": [
                {"question": "What do companies hiring junior PMs typically value most?", "options": ["Only a formal PM job title from a previous role", "Evidence of real product thinking, even from adjacent experience or personal projects", "A specific university degree, exclusively", "Years of unrelated work experience"], "correct_index": 1, "explanation": "Demonstrated product thinking — through projects, adjacent roles, or concrete artifacts — often matters more than a formal prior PM title."},
                {"question": "What is a legitimate path into product management mentioned in this lesson?", "options": ["It is impossible to enter PM without prior PM experience", "Transitioning from an adjacent role within the same company", "PM roles are only available to people with computer science degrees", "Only founders can become PMs"], "correct_index": 1, "explanation": "Moving into PM from a related internal role (support, business analysis, engineering) is a well-established entry path."},
                {"question": "What makes a targeted outreach message more effective than a generic application?", "options": ["Sending the same message to as many companies as possible", "Referencing a specific, researched observation about that company's product", "Avoiding any mention of real product knowledge", "Keeping the message as vague as possible"], "correct_index": 1, "explanation": "A specific, researched observation demonstrates genuine interest and real product thinking, standing out from generic applications."}
            ],
            "resources": [{"label": "Mind the Product", "url": "https://www.mindtheproduct.com"}]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Go-to-Market and Launch Strategy",
            "title": "Presenting a Product Plan to Stakeholders Persuasively",
            "learning_objective": "By the end of this class, you will be able to structure a short, persuasive presentation of a product plan that leads with the problem and evidence, not the solution.",
            "duration_minutes": 25,
            "content_html": "<p>A PM's ideas only matter if they can get buy-in — from engineers, from leadership, from investors. Presenting a plan effectively is a distinct skill from having a good plan; many good plans fail to get resourced simply because they were pitched poorly.</p><h2>Structuring a Persuasive Product Pitch</h2><p>Lead with the problem and evidence (not the solution) — this builds shared understanding before asking anyone to agree with your approach. Then present the proposed solution and why it's the right one given the evidence. Close with the ask: what you need (resources, approval, a decision) and by when.</p><h2>Worked Example: A 5-Minute Pitch Structure</h2><p>Minute 1: the problem and evidence (\"8 of 8 interviewed students independently described this frustration...\"). Minute 2: why this matters now (business impact, urgency). Minutes 3-4: the proposed MVP solution and why it's the right first step, referencing the riskiest assumption it tests. <strong>Minute 5: the specific ask — \"I need one engineer for 2 weeks to build and test this MVP, decision needed by Friday.\"</strong></p><ul><li>Leading with solution before problem loses the room — always establish shared understanding of the problem first</li><li>A vague ask (\"what do you all think?\") is weaker than a specific ask (\"I need X by Y date\")</li><li>Practice the pitch out loud and time it — a rambling, unpracticed pitch undermines even a strong plan</li></ul>",
            "key_concepts": ["persuasive presentation", "problem-first pitching", "specific ask", "stakeholder buy-in"],
            "practical_exercise": {
                "title": "Structure Your Product Pitch",
                "instructions": "Using your final project work so far, structure a 5-minute pitch outline following the problem-evidence, solution-reasoning, specific-ask format taught today. Write out the key points for each section. Submit the pitch outline."
            },
            "quiz": [
                {"question": "What should a persuasive product pitch lead with?", "options": ["The proposed solution", "The problem and supporting evidence", "The specific ask", "The team's org chart"], "correct_index": 1, "explanation": "Establishing shared understanding of the problem and its evidence first builds the foundation needed for the audience to accept the proposed solution."},
                {"question": "Why is a specific ask ('I need one engineer for 2 weeks, decision by Friday') stronger than a vague one?", "options": ["Vague asks are always more persuasive", "A specific ask gives the audience a clear, actionable decision to make", "Specific asks are considered rude in business settings", "It has no real difference in effectiveness"], "correct_index": 1, "explanation": "A concrete, specific request makes it easy for stakeholders to say yes or engage meaningfully, unlike an open-ended question."},
                {"question": "Why is practicing a pitch out loud recommended?", "options": ["It is unnecessary for well-written pitches", "A rambling, unpracticed delivery can undermine even a strong underlying plan", "Practicing out loud has no effect on delivery quality", "Only written pitches matter in business settings"], "correct_index": 1, "explanation": "Spoken delivery differs from written text, and practicing aloud helps catch awkward phrasing and improve overall persuasiveness."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "What Hiring Managers Actually Look for in a PM Portfolio",
            "learning_objective": "By the end of this class, you will be able to evaluate a product portfolio piece against the criteria a hiring manager typically uses before submitting it.",
            "duration_minutes": 25,
            "content_html": "<p>Unlike some fields, PM portfolios are less common but increasingly expected, especially for candidates without formal PM experience. Understanding exactly what a hiring manager scans for changes how you present your product thinking work.</p><h2>What Reviewers Actually Scan For</h2><p>1. Is the reasoning visible, not just the final output (why THIS feature, not just what feature)? 2. Is there evidence of real user input, not just personal assumption? 3. Are trade-offs acknowledged (what was deprioritized and why)? 4. Is it concise and scannable — a 20-page document rarely gets fully read.</p><h2>Worked Example: Framing a Portfolio Piece</h2><p>Weak framing: just presenting a finished PRD with no context. Strong framing: <strong>\"This PRD followed 5 user interviews revealing that listing staleness (not verification, my original assumption) was the top frustration — I deprioritized a verification badge feature in favor of a simple status-update MVP as a result.\"</strong> This single framing sentence shows the REASONING behind the work, which is what reviewers actually care about most.</p><ul><li>Always show the reasoning path, not just polished final artifacts — this is what separates a real portfolio from a template exercise</li><li>Explicitly mention when your assumptions changed based on evidence — this signals genuine, evidence-based thinking</li><li>Keep portfolio pieces concise; a reviewer scanning quickly should grasp your reasoning within a minute</li></ul>",
            "key_concepts": ["PM portfolio", "visible reasoning", "trade-off transparency", "reviewer expectations"],
            "practical_exercise": {
                "title": "Write Context Framing for Your Project",
                "instructions": "Using your final project work so far, write a short context framing paragraph (as you would present it in a portfolio) that shows your reasoning path — including any moment where evidence changed your original assumption. Submit the framing paragraph."
            },
            "quiz": [
                {"question": "What do PM portfolio reviewers primarily want to see beyond the finished artifact?", "options": ["Only polished visual design", "The reasoning behind the decisions — why this feature, not just what feature", "The exact number of hours spent", "A list of every tool used"], "correct_index": 1, "explanation": "Reviewers care most about the visible reasoning process, since that reveals genuine product thinking ability."},
                {"question": "Why should a portfolio piece mention when evidence changed an original assumption?", "options": ["It should be hidden to appear more confident", "It signals genuine, evidence-based thinking rather than rigid attachment to initial ideas", "Assumptions should never change", "It has no value to a reviewer"], "correct_index": 1, "explanation": "Showing adaptability based on real evidence demonstrates a mature, evidence-driven approach that hiring managers value."},
                {"question": "Why should portfolio pieces be kept concise and scannable?", "options": ["Long documents are always preferred", "A reviewer scanning quickly should grasp the reasoning within a short time", "Length has no impact on how it's received", "Conciseness is only relevant for engineering portfolios"], "correct_index": 1, "explanation": "Busy reviewers rarely read lengthy documents in full, so concise framing ensures the core reasoning is actually seen."}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Answering the Classic 'Design a Product for X' Interview Question",
            "learning_objective": "By the end of this class, you will be able to structure a clear, complete answer to a product design interview question within a time-boxed format.",
            "duration_minutes": 30,
            "content_html": "<p>\"Design a product for [X]\" is one of the most common PM interview question formats — testing whether a candidate can structure ambiguous problems methodically under time pressure, not whether they land on a 'correct' answer.</p><h2>A Structured Answer Framework</h2><p>1. Clarify the goal and audience first — ask questions rather than assuming (\"Design for who, specifically? What's the business goal here?\"). 2. State a specific user problem and persona. 3. Propose 2-3 solution directions, then pick one with reasoning. 4. Define an MVP and one success metric. 5. Name a risk or trade-off.</p><h2>Worked Example: 'Design a Product for Elderly Nigerians'</h2><p>Clarify: \"Are we thinking about health, social connection, or something else specifically? And is this for a startup or an established company?\" (interviewer clarifies: health reminders). Problem/persona: an elderly person managing multiple medications who forgets doses. Solutions considered: a voice-reminder device, a caregiver-notification app, a simple pill-organizer with alerts — <strong>choosing the caregiver-notification app because it leverages an existing behavior (family members already checking in) rather than requiring the elderly user to adopt new technology alone.</strong> MVP: a simple SMS-based reminder sent to a designated family member. Metric: % of reminders acknowledged within 2 hours. Risk: reliance on a family member being available and responsive.</p><ul><li>Always clarify the ambiguous prompt first — jumping straight to a solution signals poor discovery instincts</li><li>Present multiple solution directions before committing to one, showing breadth of thinking</li><li>Naming a risk or trade-off at the end shows mature, realistic product judgment, not just optimism</li></ul>",
            "key_concepts": ["product design interview", "clarifying questions", "structured problem-solving", "time-boxed answer"],
            "practical_exercise": {
                "title": "Practice a Product Design Interview Answer",
                "instructions": "Answer this prompt using the 5-step framework taught today: 'Design a product to help university students in Nigeria manage their finances.' Write out your clarifying questions, chosen persona/problem, 2-3 solution directions with your final choice and reasoning, MVP and metric, and one named risk. Submit your full structured answer."
            },
            "quiz": [
                {"question": "What is the first step recommended when answering a 'design a product for X' interview question?", "options": ["Immediately propose a detailed solution", "Clarify the ambiguous goal and audience with questions", "Ask for the interview to end", "Describe the company's org chart"], "correct_index": 1, "explanation": "Clarifying the ambiguous prompt first demonstrates good discovery instincts, rather than jumping to assumptions."},
                {"question": "Why should a candidate present multiple solution directions before committing to one?", "options": ["It wastes time and should be avoided", "It shows breadth of thinking before narrowing to a reasoned choice", "Only one solution should ever be considered", "Interviewers prefer candidates who don't explain their reasoning"], "correct_index": 1, "explanation": "Presenting and comparing multiple options before choosing demonstrates thorough, structured product thinking."},
                {"question": "Why should the answer end by naming a risk or trade-off?", "options": ["It makes the answer seem less confident and should be avoided", "It shows mature, realistic product judgment rather than just optimism", "Risks are irrelevant to interview questions", "It should replace the MVP and metric sections"], "correct_index": 1, "explanation": "Acknowledging a real risk or trade-off demonstrates grounded, realistic thinking that interviewers value over blind optimism."}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Answering 'Tell Me About a Time You Prioritized' With a Real Story",
            "learning_objective": "By the end of this class, you will be able to structure a behavioral interview answer about prioritization using the STAR format with a specific, concrete example.",
            "duration_minutes": 25,
            "content_html": "<p>Behavioral interview questions (\"tell me about a time...\") are extremely common in PM interviews, and vague, generic answers are the most common way candidates fail them. Structuring a real, specific story is what separates a strong answer from a forgettable one.</p><h2>The STAR Format</h2><p>Situation: brief context — what was happening. Task: what you specifically needed to decide or accomplish. Action: what you actually did, step by step (this should be the longest part). Result: the specific outcome, ideally with a number or concrete detail.</p><h2>Worked Example: A STAR Answer About Prioritization</h2><p>Situation: \"While working on my course's final project, I had a backlog of 8 feature ideas for a job-posting problem but limited time.\" Task: \"I needed to decide which single feature to build first for the MVP test.\" Action: \"I plotted all 8 ideas on an impact vs effort matrix based on interview evidence, identified the riskiest assumption behind the whole idea, and chose the feature that tested that assumption with the least effort.\" Result: <strong>\"This narrowed 8 ideas down to one clear MVP scope I could realistically build and test within days instead of weeks, directly tied to validated user evidence rather than guesswork.\"</strong></p><ul><li>Use a real example from this course's work if you lack formal job experience — it's genuine, specific, and defensible</li><li>The Action section should be the most detailed part of the answer — this is where your actual thinking process shows</li><li>End with a specific Result — a number, a concrete outcome, or a clear before/after — not a vague \"it went well\"</li></ul>",
            "key_concepts": ["behavioral interview", "STAR format", "prioritization story", "specific outcome"],
            "practical_exercise": {
                "title": "Write a STAR Answer About Prioritization",
                "instructions": "Using your work from this course (Day 6-10 prioritization work, or any other real example), write a full STAR-format answer to 'Tell me about a time you had to prioritize between competing options.' Submit the full STAR answer."
            },
            "quiz": [
                {"question": "What does the STAR format stand for?", "options": ["Story, Task, Action, Review", "Situation, Task, Action, Result", "Strategy, Timeline, Analysis, Reflection", "Setup, Target, Approach, Reasoning"], "correct_index": 1, "explanation": "STAR structures a behavioral answer around the situation, the specific task, the actions taken, and the concrete result."},
                {"question": "Which part of a STAR answer should typically be the most detailed?", "options": ["Situation", "Task", "Action", "Result should always be shortest and vaguest"], "correct_index": 2, "explanation": "The Action section should show the actual thinking and steps taken, making it the most substantive part of the answer."},
                {"question": "Why is a course project considered a legitimate source for a STAR interview answer?", "options": ["Course projects should never be used in interviews", "It provides a genuine, specific, defensible example even without formal job experience", "Only paid work experience counts as valid", "STAR answers cannot use personal projects"], "correct_index": 1, "explanation": "A real, specific project example is more compelling than a vague or fabricated story, even if it comes from coursework rather than a job."}
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Handling Disagreement With Engineering or Design Professionally",
            "learning_objective": "By the end of this class, you will be able to respond to a disagreement with an engineer or designer using a collaborative, evidence-based approach.",
            "duration_minutes": 25,
            "content_html": "<p>Every PM eventually disagrees with an engineer about feasibility or a designer about user experience. How that disagreement is handled — collaboratively or combatively — shapes team trust far more than who turns out to be \"right.\" This is a skill interviewers specifically probe for.</p><h2>The Collaborative Disagreement Approach</h2><p>Step 1: seek to understand their reasoning fully before defending your own position. Step 2: separate the disagreement about the GOAL (usually shared) from disagreement about the APPROACH (where the real debate often is). Step 3: propose testing the disagreement with evidence when possible, rather than debating opinions indefinitely.</p><h2>Worked Example: Disagreeing With an Engineer on Scope</h2><p>Engineer: \"Building real-time status updates will take 3 weeks, not the 3 days you scoped.\" Weak response: insisting on the original timeline. Strong response: <strong>\"Help me understand what's driving the 3-week estimate — is it the real-time infrastructure specifically? If so, could we ship a simpler version first — manual refresh instead of real-time — to test the core assumption faster, and add real-time later if the MVP validates?\"</strong> This response respects the engineer's expertise while still protecting the original goal (fast validation).</p><ul><li>Understanding the reasoning behind a disagreement often reveals it's about approach, not goal — and goals are usually shared</li><li>Proposing a scoped-down alternative can resolve a feasibility disagreement without abandoning the underlying objective</li><li>Never dismiss technical or design expertise — engineers and designers see real constraints a PM often can't</li></ul>",
            "key_concepts": ["cross-functional disagreement", "goal vs approach", "collaborative problem-solving", "scope negotiation"],
            "practical_exercise": {
                "title": "Respond to a Disagreement Scenario",
                "instructions": "You are given this scenario: a designer disagrees with your proposed user flow, saying it adds unnecessary friction. Write your full response using the collaborative approach taught today — seeking to understand their reasoning, separating goal from approach, and proposing a way to resolve the disagreement with evidence. Submit your written response."
            },
            "quiz": [
                {"question": "What is the first step in the collaborative disagreement approach?", "options": ["Insisting on your original position", "Seeking to fully understand the other person's reasoning first", "Escalating immediately to a manager", "Ending the conversation"], "correct_index": 1, "explanation": "Understanding the other person's reasoning first often reveals the disagreement is about approach rather than the shared underlying goal."},
                {"question": "According to this lesson, disagreements between a PM and engineer/designer are often really about what?", "options": ["The overall goal, which is usually shared", "The approach to reaching a shared goal", "Personal dislike between team members", "Company budget allocation"], "correct_index": 1, "explanation": "Teams usually share the same underlying goal; disagreements more often center on the best approach to achieve it."},
                {"question": "Why should a PM avoid dismissing an engineer's technical concerns?", "options": ["Technical concerns are always exaggerated", "Engineers and designers see real constraints a PM often cannot", "PMs always know better than engineers", "It has no effect on team trust"], "correct_index": 1, "explanation": "Respecting technical and design expertise acknowledges real constraints the PM may not fully see, and preserves team trust."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Launching Your Final Project — From Discovery to Launch Plan",
            "learning_objective": "By the end of this class, you will be able to plan and begin execution of your full final project, from problem discovery through the start of your PRD.",
            "duration_minutes": 35,
            "content_html": "<p>Today you begin the final project: taking a product idea from problem discovery through a prioritized roadmap, a written PRD, and a go-to-market/launch plan. This is the single asset that proves everything you've learned over the last 29 days, and the artifact you'll actually show a hiring manager or use to pitch a real idea.</p><h2>How to Approach the Final Project</h2><p>Start by finalizing your problem statement (Day 2) and reviewing or conducting real discovery (Days 3-5) — even a few real conversations strengthen this significantly. Build your feature backlog and prioritize it (Days 6-7), define your MVP and success metric (Days 8-9), and put together your roadmap (Day 10). Then write your full PRD (Days 11-13) and your go-to-market plan (Day 21).</p><h2>A Realistic Execution Plan</h2><p>Session 1: finalize problem statement, persona, and journey map; conduct or review discovery evidence. Session 2: build and prioritize your feature backlog, define MVP and metric, build the roadmap. Session 3: write the full PRD with user stories and acceptance criteria. <strong>Session 4: write your go-to-market plan, then assemble everything into one clear document with a short introductory framing paragraph, exactly as you would present it to a hiring manager or founder.</strong></p><ul><li>Every later section should trace back to your Day 2 problem statement — keep it visible while you write</li><li>Real evidence, even from a handful of conversations, makes this project dramatically stronger than pure assumption</li><li>Treat this exactly like a real product plan you'd defend in an interview — be ready to explain every prioritization decision</li></ul>",
            "key_concepts": ["final project planning", "discovery-to-launch pipeline", "PRD assembly", "product plan presentation"],
            "practical_exercise": {
                "title": "Start Your Final Project",
                "instructions": "This IS the start of your final project. Finalize your problem statement and persona. Conduct or review your discovery evidence. Build and prioritize your feature backlog, and define your MVP and success metric. Submit your problem statement, persona, discovery evidence summary, prioritized backlog, and MVP/metric definition as the beginning of your final project submission."
            },
            "quiz": [
                {"question": "What is the final project for this course?", "options": ["A single feature idea with no supporting analysis", "A full pipeline from problem discovery through a prioritized roadmap, PRD, and go-to-market plan", "Only a resume", "A single user interview transcript"], "correct_index": 1, "explanation": "The final project combines discovery, prioritization, a full PRD, and a go-to-market plan into one complete, defensible product plan."},
                {"question": "Why should every section of the final project trace back to the Day 2 problem statement?", "options": ["The problem statement is not relevant to later sections", "It ensures all prioritization, requirements, and launch decisions stay grounded in the original validated problem", "Problem statements are only used in discovery, not later work", "It has no impact on the final project's quality"], "correct_index": 1, "explanation": "Keeping the problem statement central ensures coherent reasoning throughout the entire product plan, from discovery to launch."},
                {"question": "According to the suggested execution plan, what should happen in the final session of work?", "options": ["Only writing the problem statement", "Writing the go-to-market plan and assembling everything into one clear presentable document", "Only conducting discovery interviews", "Choosing which quiz questions to answer"], "correct_index": 1, "explanation": "The plan reserves the final stage for the go-to-market plan and pulling all prior work into one polished, presentable final document."}
            ],
            "resources": []
        }
    ]
}
