"""Seed data for the UI/UX & Product Design 30-Day Skill Class."""

SKILL = {
    "slug": "ui-ux-design",
    "name": "UI/UX & Product Design",
    "tagline": "Go from zero to a polished, research-backed interactive prototype that shows employers and clients you can design real products.",
    "description": "UI/UX design is one of the most in-demand remote-friendly skills for African talent, with Nigerian and other African designers regularly landing global freelance and full-time roles through platforms like Upwork and remote job boards. This track teaches the full product design process, from user research through wireframes to a high-fidelity interactive Figma prototype, so a student finishes with a real, testable product design rather than isolated design exercises. It matters for career growth because most design hiring today is portfolio-driven, not credential-driven.",
    "level": "beginner",
    "estimated_hours": 58,
    "course_title": "30-Day UI/UX & Product Design Career Track",
    "course_description": "After 30 days, a student can research real users, translate findings into personas and wireframes, build a high-fidelity interface in Figma, wire it into an interactive prototype, and run a usability test to validate their design decisions.",
    "final_project": {
        "title": "Complete Digital Product Design Case Study",
        "description": "Design a complete digital product from scratch for a real or realistic brand, app idea, or business problem of your choosing, such as a campus food delivery app or a savings app for informal traders. You must conduct actual or simulated user research and document at least one persona, map the user journey, produce low-fidelity wireframes for the core flow, build a polished high-fidelity UI in Figma, wire it into a clickable interactive prototype covering at least one full user flow, and run a usability test with at least three participants, documenting their feedback and the changes you made in response. This case study becomes the centerpiece of your design portfolio.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["User research", "Persona development", "Wireframing", "High-fidelity UI design", "Interactive prototyping", "Usability testing", "Case study storytelling"],
        "rubric": [
            {"name": "Quality and depth of user research and persona", "max_points": 25},
            {"name": "Wireframe-to-high-fidelity design execution", "max_points": 30},
            {"name": "Prototype interactivity and flow completeness", "max_points": 25},
            {"name": "Usability testing rigor and iteration evidence", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Foundations of Product Design",
            "title": "What UI/UX Designers Actually Do on the Job",
            "learning_objective": "By the end of this class, you will be able to distinguish UX design from UI design and describe the stages of a typical product design process.",
            "duration_minutes": 25,
            "content_html": "<p>Many beginners confuse UI/UX design with just making things look pretty. In real companies and client work, designers are hired to solve problems for users while balancing business goals, and visual polish is only the final layer of that work. Understanding this distinction early will shape how you approach every exercise in this course.</p><h2>UX vs UI</h2><p>UX, user experience, is about how a product works: the structure, flows, and decisions that make something usable and useful. UI, user interface, is about how a product looks and feels: colors, typography, spacing, and the visual details a user directly interacts with. A product can have a gorgeous UI and still fail if the UX is confusing, and a product with excellent UX can still lose users if the UI feels unprofessional or hard to trust.</p><h2>Worked Example</h2><p>Consider a mobile banking app used by a small trader in Lagos. If the UX is poor, the trader might not be able to find how to send money in under three taps, causing frustration even if the app looks modern. If the UI is poor, buttons might be hard to tell apart or text might be too small to read on a low-end Android phone, even if the flow itself is logical. A strong product designer thinks about both layers together, and this course will move you through research and structure first, then visual design, in that order, because that is the order that produces usable products.</p>",
            "key_concepts": ["UX vs UI", "Product design process", "User-centered design", "Usability", "Business and user goals"],
            "practical_exercise": {
                "title": "Audit an App You Use Daily",
                "instructions": "Pick one app you use regularly, such as a banking, food delivery, or social app. Write three sentences describing one thing about its UX (how it works or flows) and three sentences describing one thing about its UI (how it looks). Note one specific improvement you would make to each."
            },
            "quiz": [
                {"question": "What does UX design primarily focus on?", "options": ["Colors and typography", "How a product works and flows for the user", "The company's logo design", "Server infrastructure"], "correct_index": 1, "explanation": "UX is concerned with structure, flow, and usability rather than visual styling alone."},
                {"question": "Can a product have great UI but poor UX?", "options": ["No, they are always the same thing", "Yes, a product can look great but still be confusing or hard to use", "Only mobile apps can have this problem", "This is impossible by definition"], "correct_index": 1, "explanation": "Visual polish does not guarantee usability; a beautiful interface can still have a broken or confusing flow."},
                {"question": "In this course, why does research and structure come before visual design?", "options": ["Visual design is not important", "Because a solid structure and understanding of user needs should guide the visual decisions that follow", "It is simply a random ordering with no reasoning", "Visual design tools are unavailable early in the course"], "correct_index": 1, "explanation": "Designing the interface before understanding the user's needs and flow often leads to rework and products that look good but do not function well."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Foundations of Product Design",
            "title": "Setting Up Figma and Your Design Workflow",
            "learning_objective": "By the end of this class, you will be able to create a Figma file and use its core tools: frames, shapes, text, and basic alignment.",
            "duration_minutes": 30,
            "content_html": "<p>Figma is the industry-standard design tool used by product teams worldwide, including most companies hiring remote African designers, so fluency with it is non-negotiable for this career path. Today is about building comfort with the tool itself so it stops being a barrier for the rest of this course.</p><h2>Core Figma Concepts</h2><p>A frame is Figma's container for a screen or artboard, similar to a canvas with defined dimensions, such as a mobile screen at 375 by 812 pixels. Shapes, text, and images are placed inside frames and can be grouped or organized into layers, visible in the layers panel on the left. Alignment and auto layout tools help you position elements precisely and keep spacing consistent, which matters enormously for a professional-looking result. Components, which you will learn in depth later this month, let you reuse design elements consistently across screens.</p><h2>Worked Example</h2><p>A common first exercise is recreating the login screen of a well-known app purely to practice tool mechanics: create a mobile frame, add a logo placeholder shape at the top, add two rectangle input fields with text labels, add a button shape with centered text, and use Figma's alignment tools to center everything horizontally with even vertical spacing. This is not about original design yet, it is about building raw fluency with frames, shapes, text, and alignment so your hands know the tool before you start solving real design problems.</p>",
            "key_concepts": ["Figma frames", "Layers panel", "Alignment tools", "Auto layout basics", "Design file organization"],
            "practical_exercise": {
                "title": "Recreate a Login Screen",
                "instructions": "Create a new Figma file with a mobile frame sized 375 by 812. Recreate a simple login screen containing a logo placeholder, two labeled input field shapes, and a button, using Figma's alignment tools to center and evenly space the elements. Share a screenshot or the Figma file link."
            },
            "quiz": [
                {"question": "What is a frame in Figma used for?", "options": ["Storing color palettes only", "Acting as a container or artboard representing a screen", "Exporting fonts", "Running code"], "correct_index": 1, "explanation": "Frames define the boundaries of a screen or artboard where design elements are placed."},
                {"question": "Why is Figma considered important for a career in UI/UX design?", "options": ["It is the only tool that can create images", "It is the industry-standard tool used by most product teams hiring designers, including remotely", "It is free with no other reason", "It replaces the need for user research"], "correct_index": 1, "explanation": "Fluency in Figma is a near-universal requirement in current design job postings and client briefs."},
                {"question": "What is the purpose of alignment tools in a design tool like Figma?", "options": ["To add animations", "To position elements precisely and keep spacing consistent for a professional result", "To write code", "To change file formats"], "correct_index": 1, "explanation": "Alignment tools ensure visual consistency and precision, which is core to professional-looking design."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Foundations of Product Design",
            "title": "Understanding Users — Why Research Comes Before Design",
            "learning_objective": "By the end of this class, you will be able to write three strong user research questions for a real or hypothetical product idea.",
            "duration_minutes": 25,
            "content_html": "<p>Designers who skip research often build beautiful solutions to problems users do not actually have. Employers and clients specifically value designers who can show their design decisions are grounded in real user needs, not personal taste, because that grounding is what makes a product succeed commercially.</p><h2>What Research Is Really For</h2><p>User research uncovers what users actually need, how they currently solve their problem, and where their frustrations lie, before you design anything. Common early-stage methods include user interviews, surveys, and reviewing existing app store reviews or complaints about competing products. Good research questions are open-ended and behavior-focused, asking how someone currently does something and what frustrates them, rather than asking would you use a feature like this, which tends to produce unreliable, overly polite answers.</p><h2>Worked Example</h2><p>Imagine you want to design a savings app for informal traders in a Nigerian market. A weak research question is do you want a savings app, which invites a polite yes with no real insight. A strong set of questions includes: walk me through how you currently save money day to day, what has gone wrong with a savings method you have tried before, and what would make you trust a new financial app with your money. These questions surface real behavior and real objections that directly inform your design decisions, rather than flattering assumptions you already had.</p>",
            "key_concepts": ["User research", "Open-ended questions", "Behavior-focused questioning", "Research before design", "Competitor review analysis"],
            "practical_exercise": {
                "title": "Draft Research Questions",
                "instructions": "Choose a product idea for your eventual final project (or a placeholder idea for now). Write five open-ended, behavior-focused user research questions you would ask a potential user, avoiding any yes-or-no or leading questions."
            },
            "quiz": [
                {"question": "Why is asking would you use a feature like this considered a weak research question?", "options": ["It is too long", "It invites polite, non-committal answers rather than revealing real behavior", "It cannot be asked in an interview", "It is only useful for surveys"], "correct_index": 1, "explanation": "Hypothetical, leading questions tend to produce agreeable but unreliable answers rather than genuine insight."},
                {"question": "What is the main purpose of conducting user research before designing?", "options": ["To make the designer feel confident", "To ground design decisions in real user needs and behavior rather than assumptions", "To fill time in the design process", "To avoid using Figma"], "correct_index": 1, "explanation": "Research ensures the eventual design solves a problem users genuinely have, rather than a designer's assumption."},
                {"question": "Which of these is an example of a strong, behavior-focused research question?", "options": ["Do you like this app idea?", "Walk me through how you currently handle this task", "Would you pay for this feature?", "Is this a good idea?"], "correct_index": 1, "explanation": "Asking someone to walk through their current behavior reveals real habits and pain points rather than opinions."}
            ],
            "resources": []
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Foundations of Product Design",
            "title": "Conducting Your First User Interview",
            "learning_objective": "By the end of this class, you will be able to plan and conduct a structured user interview and take usable notes from it.",
            "duration_minutes": 30,
            "content_html": "<p>Reading about research questions is not the same as actually sitting with a real person and listening. Today you conduct an actual interview, because the skill of asking a follow-up question in the moment cannot be learned from a template alone, and interviewing ability is something portfolios and interviews both test directly.</p><h2>Running a Good Interview</h2><p>Start with a short warm, informal opening to build rapport before diving into questions. Ask your prepared open-ended questions, but treat them as a guide rather than a rigid script: when someone says something interesting or surprising, follow up with why or tell me more about that instead of moving straight to your next scripted question. Avoid interrupting, avoid suggesting answers, and resist the urge to defend or explain your product idea during the interview, since your job right now is to listen, not to sell.</p><h2>Worked Example</h2><p>Interviewing a university student about how they manage transport costs, if they mention they usually run out of money mid-week because they underestimate daily transport, a weak interviewer moves on to the next scripted question. A strong interviewer follows up immediately: what do you do when that happens, and have you ever tried anything to prevent it. That single follow-up often produces the most valuable insight of the entire interview, because it digs into the actual pain point rather than staying at the surface level of the original question.</p>",
            "key_concepts": ["Interview rapport", "Follow-up questions", "Active listening", "Avoiding leading behavior", "Note-taking during interviews"],
            "practical_exercise": {
                "title": "Conduct One Real User Interview",
                "instructions": "Using the questions you drafted on Day 3, interview one real person (a classmate, friend, or family member) about the problem your product idea addresses, for at least ten minutes. Take notes during or immediately after, and write a short summary highlighting the two most surprising or useful things you learned."
            },
            "quiz": [
                {"question": "What should an interviewer do when a participant says something unexpected or interesting?", "options": ["Move on immediately to the next scripted question", "Follow up with a question like tell me more about that", "Correct the participant", "End the interview early"], "correct_index": 1, "explanation": "Following up on unexpected statements often surfaces the most valuable insights of the interview."},
                {"question": "Why should an interviewer avoid defending or explaining their product idea during a research interview?", "options": ["It is against Figma's terms of service", "The goal is to listen and understand the user, not to sell or justify the idea", "Explaining ideas is illegal in research", "It takes too much time"], "correct_index": 1, "explanation": "Research interviews are for gathering honest insight, and defending your idea can bias or shut down honest feedback."},
                {"question": "What is the purpose of a warm, informal opening before diving into interview questions?", "options": ["To waste time", "To build rapport so the participant feels comfortable sharing honestly", "It is not actually useful", "To test the participant's patience"], "correct_index": 1, "explanation": "Rapport helps participants relax and share more openly and honestly during the interview."}
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Foundations of Product Design",
            "title": "Turning Research into Personas That Actually Guide Decisions",
            "learning_objective": "By the end of this class, you will be able to build a one-page user persona grounded in real research findings.",
            "duration_minutes": 25,
            "content_html": "<p>A persona is one of the most misunderstood tools in design, often reduced to a decorative fake profile with a stock photo and a made-up name that never actually influences a single design decision. A useful persona is different: it is a working reference that helps you and your team make consistent choices grounded in real research.</p><h2>What Makes a Persona Useful</h2><p>A strong persona includes a name and short background for memorability, but more importantly it includes specific goals the person is trying to achieve, specific frustrations or barriers they currently face, and behavioral details drawn directly from your actual research, not guesses. The test of a good persona is whether you can point to a specific interview quote or observation behind each claim on the page. If you cannot, it is decoration, not a design tool.</p><h2>Worked Example</h2><p>From the transport-cost interview example on Day 4, a resulting persona might be named Blessing, a 200-level student who commutes daily by bus. Her goal is to avoid running out of transport money before the week ends. Her frustration, taken directly from the interview, is that she underestimates daily costs and has no simple way to track spending without opening a full banking app. This persona now directly justifies a design decision: your product should show a simple, glanceable daily transport budget rather than a complex financial dashboard, because that is what Blessing's real behavior calls for.</p>",
            "key_concepts": ["User persona", "Research-grounded design", "Goals and frustrations", "Persona misuse", "Design decision justification"],
            "practical_exercise": {
                "title": "Build Your First Persona",
                "instructions": "Using the notes from your Day 4 interview, build a one-page persona including a name, brief background, two to three specific goals, two to three specific frustrations, and one direct quote or paraphrase from your actual interview supporting each frustration. Submit the persona as a document or Figma page."
            },
            "quiz": [
                {"question": "What makes a persona a decoration rather than a useful design tool?", "options": ["It has a name and photo", "Its claims cannot be traced back to real research findings", "It is created in Figma", "It includes goals and frustrations"], "correct_index": 1, "explanation": "A persona is only useful if its content is grounded in actual research rather than invented assumptions."},
                {"question": "What is the primary purpose of including specific frustrations in a persona?", "options": ["To make the persona look more detailed", "To identify real pain points that should directly inform design decisions", "To fill space on the page", "Frustrations are not necessary in a persona"], "correct_index": 1, "explanation": "Frustrations grounded in research point directly to problems the design should solve."},
                {"question": "How should you test whether a claim on your persona is legitimate?", "options": ["Check if it sounds professional", "Check whether you can point to a specific interview quote or observation behind it", "Check if it matches a template online", "Check if it is visually appealing"], "correct_index": 1, "explanation": "Legitimate persona claims must be traceable to actual research evidence, not assumption or decoration."}
            ],
            "resources": []
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Structure Before Visuals",
            "title": "Mapping the User Journey — Finding Pain Points",
            "learning_objective": "By the end of this class, you will be able to create a user journey map showing stages, actions, emotions, and pain points for a specific task.",
            "duration_minutes": 30,
            "content_html": "<p>Before designing any screens, strong designers map out the entire experience a user goes through to accomplish a goal, not just the part that happens inside the app. This wider view frequently reveals that the biggest pain point is not even inside the product you are about to design, which changes what you should prioritize.</p><h2>Anatomy of a Journey Map</h2><p>A journey map breaks an experience into stages, such as discovering a need, researching options, taking action, and following up afterward. For each stage, you record what the user is doing, what they are thinking or feeling, often rated on a simple emotional scale, and any pain points or drop-off risks at that stage. This format makes it visually obvious where a user's experience dips, which is exactly where design effort should be concentrated.</p><h2>Worked Example</h2><p>Mapping Blessing's journey to track daily transport spending: stage one is realizing she overspent, which happens with frustration when she checks her wallet at day's end. Stage two is trying to remember how much she spent on transport specifically, which is difficult because she paid cash to multiple bus conductors. Stage three is deciding to try a budgeting method, often abandoned quickly because existing apps feel too complex for such a small, specific need. This map reveals the real pain point is not budgeting in general, it is capturing small cash transactions quickly, which should directly shape your core feature, not a generic finance dashboard.</p>",
            "key_concepts": ["User journey map", "Stages of experience", "Emotional mapping", "Pain point identification", "Prioritizing design effort"],
            "practical_exercise": {
                "title": "Build a Journey Map",
                "instructions": "Using your persona from Day 5, map their journey through the core task your product addresses across at least four stages. For each stage, note their action, their emotional state, and any pain point. Present this as a simple table or Figma diagram."
            },
            "quiz": [
                {"question": "What is the main value of mapping a user's full journey rather than only the screens inside your app?", "options": ["It looks more professional in a portfolio", "It can reveal pain points outside the app that are more important than anything inside it", "It replaces the need for a persona", "It is required by Figma"], "correct_index": 1, "explanation": "The biggest pain point in a user's experience is often outside the product itself, and a journey map reveals this."},
                {"question": "What does a journey map typically record for each stage of an experience?", "options": ["Only the final outcome", "The user's actions, emotional state, and pain points at that stage", "Only technical requirements", "The company's revenue at that stage"], "correct_index": 1, "explanation": "A journey map captures actions, feelings, and friction points across each stage of the experience."},
                {"question": "In the worked example, what did the journey map reveal was the real underlying pain point?", "options": ["The user needed a more complex finance dashboard", "The user needed a quick way to capture small cash transactions, not general budgeting", "The user did not want to save money at all", "The user preferred existing budgeting apps"], "correct_index": 1, "explanation": "The map showed the actual friction was capturing quick cash transactions, not general budgeting complexity."}
            ],
            "resources": []
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Structure Before Visuals",
            "title": "Information Architecture — Structuring Content Before Screens",
            "learning_objective": "By the end of this class, you will be able to create a simple sitemap organizing a product's screens and content into a logical hierarchy.",
            "duration_minutes": 25,
            "content_html": "<p>Before drawing a single screen, a designer needs to decide what content and features exist and how they relate to each other. Skipping this step is why some apps feel like a maze, with features buried in illogical places, frustrating users even when individual screens look fine.</p><h2>Building a Sitemap</h2><p>Information architecture is the practice of organizing and structuring content so users can find what they need intuitively. A sitemap is a simple diagram showing every screen or section in a product and how they connect in a hierarchy, similar to an organizational chart. Good information architecture groups related features together and avoids making users guess where something lives, following the principle that a feature should live where a user would naturally expect to look for it, not where it was easiest for the team to build it.</p><h2>Worked Example</h2><p>For Blessing's transport-tracking app, a sitemap might have a home screen at the top level, branching into a quick-add expense screen, a weekly summary screen, and a settings screen. The quick-add screen might further branch into a manual entry option and a save-a-favorite-route option. Sketching this out before touching visual design forces you to decide, for example, whether settings belongs on the home screen directly or one level deeper, a decision that is much cheaper to change on a simple diagram than after building full high-fidelity screens.</p>",
            "key_concepts": ["Information architecture", "Sitemap", "Content hierarchy", "Findability", "Structural planning"],
            "practical_exercise": {
                "title": "Create a Sitemap",
                "instructions": "For your product idea, list every screen or major section you expect it to need. Organize them into a simple hierarchy diagram (a sitemap) showing which screens are top-level and which are nested under others. Use Figma, a diagramming tool, or hand-drawn and photographed if needed."
            },
            "quiz": [
                {"question": "What problem does poor information architecture typically cause for users?", "options": ["Slow internet speeds", "Features feel buried or hard to find, even if individual screens look good", "Higher app store ratings", "Faster loading screens"], "correct_index": 1, "explanation": "Poor structure makes navigation confusing regardless of visual quality."},
                {"question": "What is a sitemap in the context of product design?", "options": ["A visual map of a physical office", "A diagram showing a product's screens or sections and how they connect in a hierarchy", "A list of website URLs only", "A color palette reference"], "correct_index": 1, "explanation": "A sitemap organizes the product's content and screens into a clear hierarchy before visual design begins."},
                {"question": "Why is it cheaper to fix structural decisions at the sitemap stage rather than after building high-fidelity screens?", "options": ["Sitemaps cannot be changed once made", "A simple diagram is much faster to revise than fully designed visual screens", "High-fidelity screens are always structurally perfect", "Structure has no effect on final screens"], "correct_index": 1, "explanation": "Restructuring a simple diagram takes minutes, while reworking fully designed screens takes much longer."}
            ],
            "resources": []
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Structure Before Visuals",
            "title": "Sketching and Low-Fidelity Wireframing",
            "learning_objective": "By the end of this class, you will be able to produce low-fidelity wireframes for a core user flow using boxes, lines, and placeholder text.",
            "duration_minutes": 30,
            "content_html": "<p>Low-fidelity wireframes are intentionally rough because their entire purpose is to test layout and flow decisions quickly and cheaply before investing time in visual polish. Designers who jump straight to high-fidelity screens often waste hours redoing pixel-perfect work every time a structural idea changes.</p><h2>Wireframing Principles</h2><p>A wireframe uses simple boxes, lines, and placeholder text or grayscale blocks to represent content and layout, deliberately avoiding real colors, fonts, or imagery, so that feedback stays focused on structure rather than aesthetics. Every screen should map back to a step in the user journey or sitemap from earlier this week. Keep wireframes fast: hand-drawn sketches or simple Figma shapes are both fine, since speed and iteration matter far more than precision at this stage.</p><h2>Worked Example</h2><p>For the quick-add expense screen in Blessing's app, a low-fidelity wireframe might show a simple box at the top labeled amount, a row of icon placeholders labeled transport, food, and other beneath it, and a large button placeholder labeled save at the bottom. No colors, no real icons, no font choices, just enough structure to ask a real user does this layout make sense to you, and does anything feel missing, which is a much cheaper conversation to have now than after building a polished screen that turns out to need restructuring.</p>",
            "key_concepts": ["Low-fidelity wireframes", "Placeholder content", "Structural feedback", "Rapid iteration", "Flow-to-wireframe mapping"],
            "practical_exercise": {
                "title": "Wireframe Your Core Flow",
                "instructions": "Using your sitemap from Day 7, create low-fidelity wireframes (hand-drawn or simple Figma shapes) for the three to five screens that make up your product's core user flow. Use only boxes, lines, and placeholder text, no colors or real content. Share photos or a Figma link."
            },
            "quiz": [
                {"question": "Why do low-fidelity wireframes deliberately avoid colors and real fonts?", "options": ["Because color tools are hard to use", "So feedback stays focused on structure and layout rather than aesthetics", "Because Figma does not support color at this stage", "Colors are added automatically later"], "correct_index": 1, "explanation": "Removing visual polish keeps early feedback focused on whether the structure and flow make sense."},
                {"question": "What is the main risk of skipping low-fidelity wireframes and jumping straight to high-fidelity design?", "options": ["Nothing, it saves time overall", "Structural changes become expensive because polished visual work has to be redone", "High-fidelity tools cannot represent structure", "Wireframes are legally required"], "correct_index": 1, "explanation": "Structural rework is far more costly once visual polish has already been invested."},
                {"question": "What should every wireframe screen be traceable back to?", "options": ["A random idea with no plan", "A step in the user journey or sitemap", "The designer's personal preference only", "A competitor's app screenshot"], "correct_index": 1, "explanation": "Wireframes should represent planned structure, tracing back to the journey map and sitemap already created."}
            ],
            "resources": []
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Structure Before Visuals",
            "title": "Grids, Layout, and Visual Hierarchy Fundamentals",
            "learning_objective": "By the end of this class, you will be able to apply a grid system and visual hierarchy principles to organize elements on a screen.",
            "duration_minutes": 30,
            "content_html": "<p>Once structure is settled through wireframes, the next layer is layout: how elements are sized, spaced, and arranged so a user's eye naturally moves to the most important thing first. This is where design starts feeling intentional rather than arbitrary.</p><h2>Grids and Hierarchy</h2><p>A grid system divides a screen into consistent columns and margins, commonly a twelve-column grid for larger screens or a simpler four-column grid for mobile, so elements align consistently rather than floating at random positions. Visual hierarchy is the deliberate use of size, weight, color, and spacing to signal importance: a large bold headline draws attention before smaller body text, and a prominent button color draws the eye before a secondary text link.</p><h2>Worked Example</h2><p>On a mobile screen for Blessing's app using a simple grid with consistent side margins, the current weekly total might be shown in large bold text at the top, immediately establishing it as the most important information on the screen. Below it, smaller text shows a supporting detail like remaining budget, and further down a clearly prominent save button uses a strong color and size to stand out from a secondary, smaller cancel link beside it. Every sizing and spacing decision reinforces what the user should notice first, second, and third, rather than presenting everything with equal visual weight.</p>",
            "key_concepts": ["Grid systems", "Visual hierarchy", "Consistent margins", "Size and weight for emphasis", "Primary vs secondary actions"],
            "practical_exercise": {
                "title": "Apply Grid and Hierarchy to One Screen",
                "instructions": "Take one wireframe from Day 8 and rebuild it in Figma using a defined grid (columns and margins). Apply visual hierarchy by varying size and weight so the most important element is obviously dominant, a secondary element is clearly less prominent, and a primary action button stands out from any secondary action."
            },
            "quiz": [
                {"question": "What is the purpose of a grid system in screen layout?", "options": ["To add decoration", "To keep elements aligned consistently across a screen", "To choose brand colors", "To write copy for the app"], "correct_index": 1, "explanation": "Grids provide a consistent structural framework so elements align predictably rather than floating randomly."},
                {"question": "How does visual hierarchy typically signal that one element is more important than another?", "options": ["By making all elements the same size and color", "Through differences in size, weight, color, and spacing", "By hiding less important elements entirely", "Through random placement"], "correct_index": 1, "explanation": "Deliberate variation in size, weight, color, and spacing guides the user's eye to the most important content first."},
                {"question": "In the worked example, why is the save button given a strong color and larger size than the cancel link?", "options": ["It is a random stylistic choice", "To visually establish it as the primary action the designer wants the user to take", "Because cancel buttons are never needed", "To match a competitor's app exactly"], "correct_index": 1, "explanation": "Emphasizing the primary action visually helps guide users toward the intended next step."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Structure Before Visuals",
            "title": "Typography Choices That Make or Break Usability",
            "learning_objective": "By the end of this class, you will be able to select and apply a type scale with appropriate size, weight, and line height for readability.",
            "duration_minutes": 25,
            "content_html": "<p>Typography is often the single largest surface area of any digital product, since most screens are mostly text, yet it is one of the most rushed decisions beginners make. Poor typography choices directly hurt usability, especially for users on lower-end phones or in bright outdoor lighting, both common realities across Nigeria.</p><h2>Type Scale and Readability</h2><p>A type scale is a small, consistent set of font sizes used across a product, such as a set for headlines, subheadings, body text, and captions, rather than picking a new size every time. Line height, the vertical spacing between lines of text, should generally be around 1.4 to 1.6 times the font size for comfortable reading, especially in longer body text. Contrast between text color and background matters enormously for readability in bright sunlight, a real condition for many users checking their phones outdoors in Nigeria.</p><h2>Worked Example</h2><p>For Blessing's app, a practical type scale might use 24px bold for the main balance number, 16px regular for body text and labels, and 13px for small captions like a timestamp, each with consistent line heights applied. Text color would use a dark, high-contrast color against a light background rather than a light gray on white, which looks elegant on a designer's laptop screen indoors but becomes nearly unreadable on a budget phone screen in bright daylight, a usability failure that only becomes obvious if you specifically test for it.</p>",
            "key_concepts": ["Type scale", "Line height", "Font size hierarchy", "Color contrast", "Real-world readability conditions"],
            "practical_exercise": {
                "title": "Define and Apply a Type Scale",
                "instructions": "Define a simple type scale for your product with four levels (for example headline, subheading, body, caption), specifying size and line height for each. Apply this scale to the screen you built on Day 9, replacing any placeholder text sizing with your defined scale."
            },
            "quiz": [
                {"question": "What is a type scale?", "options": ["A tool for measuring screen resolution", "A small, consistent set of font sizes used across a product", "A single font used for everything", "A color palette for buttons"], "correct_index": 1, "explanation": "A type scale limits font sizes to a consistent, deliberate set rather than arbitrary sizing per screen."},
                {"question": "Why does color contrast matter especially for users in Nigeria checking their phones outdoors?", "options": ["Contrast has no effect outdoors", "Bright outdoor lighting makes low-contrast text much harder to read", "Outdoor use requires larger file sizes", "Contrast only matters for print design"], "correct_index": 1, "explanation": "Bright ambient light significantly reduces the readability of low-contrast text on a screen."},
                {"question": "What is a reasonable line height range for comfortable body text readability?", "options": ["0.5 to 0.8 times the font size", "1.4 to 1.6 times the font size", "5 to 10 times the font size", "Line height has no effect on readability"], "correct_index": 1, "explanation": "A line height of roughly 1.4 to 1.6 times the font size is a widely used comfortable reading range."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Visual Design and Systems",
            "title": "Color Theory and Accessible Color Contrast",
            "learning_objective": "By the end of this class, you will be able to build a small, accessible color palette and verify its contrast ratios meet accessibility standards.",
            "duration_minutes": 30,
            "content_html": "<p>Color is one of the fastest ways to make a product feel professional or amateurish, but color choices also have a direct accessibility impact: poor contrast excludes users with low vision or color blindness, and this is increasingly a legal and client requirement, not just a nice-to-have.</p><h2>Building a Working Palette</h2><p>A practical product palette typically includes one primary brand color, one or two secondary or accent colors for highlights, a set of neutral grays for text and backgrounds, and semantic colors for success, warning, and error states. The Web Content Accessibility Guidelines require a contrast ratio of at least 4.5 to 1 for normal body text against its background, which many appealing color combinations fail without adjustment, so checking, not just eyeballing, matters.</p><h2>Worked Example</h2><p>Suppose you choose a soft light green as your primary brand color for Blessing's app. Using it directly as text on a white background might only achieve a contrast ratio around 2 to 1, failing accessibility standards badly. The fix is not abandoning the color entirely, it is using a darker shade of the same green for text and reserving the lighter, softer shade for backgrounds or large decorative elements where contrast requirements are less strict. This is exactly the kind of adjustment a professional designer makes routinely, and being able to explain it shows real accessibility awareness in an interview.</p>",
            "key_concepts": ["Color palette structure", "WCAG contrast ratio", "Semantic colors", "Accessible text color", "Brand vs functional color use"],
            "practical_exercise": {
                "title": "Build and Verify an Accessible Palette",
                "instructions": "Create a color palette for your product with a primary color, one accent color, at least three neutral grays, and success and error colors. Using any free online contrast checker, verify that your primary text color against your main background meets at least a 4.5 to 1 contrast ratio, adjusting shades as needed, and note the ratio you achieved."
            },
            "quiz": [
                {"question": "What minimum contrast ratio does WCAG recommend for normal body text?", "options": ["1.5 to 1", "4.5 to 1", "10 to 1", "There is no recommended ratio"], "correct_index": 1, "explanation": "WCAG guidelines specify a minimum contrast ratio of 4.5 to 1 for normal body text against its background."},
                {"question": "If a brand color fails contrast requirements as text, what is a common professional fix?", "options": ["Abandon the color entirely", "Use a darker shade of the same color for text while keeping the lighter shade for backgrounds or decoration", "Ignore accessibility guidelines", "Only use the color in images"], "correct_index": 1, "explanation": "Adjusting the shade while staying within the same color family preserves brand identity while meeting accessibility needs."},
                {"question": "Why does color accessibility matter beyond aesthetics?", "options": ["It has no real impact on users", "Poor contrast can exclude users with low vision or color blindness from using the product effectively", "It only matters for print design", "It is purely a legal formality with no user impact"], "correct_index": 1, "explanation": "Accessible contrast directly affects whether users with visual impairments can actually use the product."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Visual Design and Systems",
            "title": "Building a Mini Design System — Components and Styles in Figma",
            "learning_objective": "By the end of this class, you will be able to create reusable Figma components and styles for buttons, text, and colors.",
            "duration_minutes": 35,
            "content_html": "<p>Professional design work is rarely a single screen designed in isolation, it is a consistent system reused across dozens of screens. Employers specifically look for designers who understand components and design systems because this is exactly how real product teams work at scale.</p><h2>Components and Styles</h2><p>A Figma component is a reusable design element, such as a button, that you define once and then reuse across your file as instances, so that if you update the original component, every instance updates automatically. Styles let you save color values, text formatting, and effects once and apply them consistently, avoiding subtly inconsistent shades of what was meant to be the same blue across different screens. Building even a small design system, three or four button states, a handful of text styles, and your color palette as saved styles, dramatically speeds up every design decision from this point forward.</p><h2>Worked Example</h2><p>For Blessing's app, you might create one button component with a default state, a pressed state, and a disabled state, using your accessible palette from Day 11. Save your headline, body, and caption typography from Day 10 as text styles. From here on, whenever you need a button anywhere in the file, you drag in the component instance instead of redrawing a rectangle and text every time, and if you later decide to adjust the button's corner radius, updating the master component updates it everywhere instantly.</p>",
            "key_concepts": ["Figma components", "Component instances", "Color and text styles", "Design system consistency", "Scalable design workflow"],
            "practical_exercise": {
                "title": "Build Your Mini Design System",
                "instructions": "In Figma, create a button component with at least two states (default and disabled), save your Day 11 color palette as color styles, and save your Day 10 type scale as text styles. Place all of these on a dedicated design system page in your Figma file."
            },
            "quiz": [
                {"question": "What happens to instances of a Figma component when you update the original component?", "options": ["Nothing changes", "All instances automatically update to reflect the change", "Only the first instance updates", "The component becomes deleted"], "correct_index": 1, "explanation": "Component instances stay linked to the master component, so edits propagate automatically."},
                {"question": "What problem do saved color and text styles solve?", "options": ["They make files load faster only", "They prevent subtly inconsistent colors or text formatting from appearing across different screens", "They are required to export a file", "They replace the need for a grid system"], "correct_index": 1, "explanation": "Styles ensure the same intended color or text formatting is applied consistently everywhere it is used."},
                {"question": "Why do employers value designers who understand components and design systems?", "options": ["Because it looks impressive on a resume with no real use", "Because real product teams build and maintain consistent systems at scale, not isolated screens", "Because components are rarely used in real jobs", "Because it eliminates the need for user research"], "correct_index": 1, "explanation": "Design systems are standard practice in professional product teams, and familiarity signals readiness for real team workflows."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Visual Design and Systems",
            "title": "Designing Your First High-Fidelity Screen",
            "learning_objective": "By the end of this class, you will be able to transform a low-fidelity wireframe into a polished high-fidelity screen using your design system.",
            "duration_minutes": 35,
            "content_html": "<p>This is the moment where weeks one and two come together: your research-informed structure, your grid and hierarchy principles, your accessible colors, your type scale, and your reusable components all combine into an actual polished screen a user could imagine using in a real app.</p><h2>From Wireframe to High-Fidelity</h2><p>Take your low-fidelity wireframe and rebuild it using your defined grid, applying your saved text styles for every piece of text and your saved color styles for every color, and using your button component wherever a button appears rather than drawing a new one. Resist the temptation to introduce new colors, fonts, or spacing values that are not part of your system, since consistency is what separates professional work from a collection of individually pretty but disconnected screens.</p><h2>Worked Example</h2><p>Rebuilding Blessing's quick-add expense wireframe in high fidelity, the amount input becomes a properly styled input field using your neutral color styles for its border, the category icons become actual small icon components in your accent color, and the save button becomes an instance of your button component in its default state, all text uses your saved headline, body, or caption styles exactly as defined. The result should look like it belongs to the same coherent product as every other screen you design this month, because it is built from the exact same reusable system rather than reinvented from scratch.</p>",
            "key_concepts": ["Wireframe to high-fidelity translation", "Design system application", "Visual consistency", "Component reuse", "Polish without new ad hoc styles"],
            "practical_exercise": {
                "title": "Build Your First High-Fidelity Screen",
                "instructions": "Take one wireframe from Day 8 and rebuild it as a complete high-fidelity screen, using only styles and components from your design system (Day 11 and 12). Do not introduce any new colors or font sizes outside your defined system. Share a screenshot or Figma link."
            },
            "quiz": [
                {"question": "Why should new colors or font sizes not be introduced outside your defined design system when building a high-fidelity screen?", "options": ["Figma does not allow new colors", "Consistency across screens is what separates professional work from disconnected, ad hoc design", "New colors are always illegal in design", "It has no real effect on quality"], "correct_index": 1, "explanation": "Sticking to a defined system ensures every screen feels like part of one coherent product."},
                {"question": "What should guide the layout of a high-fidelity screen built from an earlier wireframe?", "options": ["A completely new, unrelated layout", "The structure already validated in the low-fidelity wireframe, refined with the design system", "Random placement of elements", "Copying a competitor's screen exactly"], "correct_index": 1, "explanation": "High-fidelity design should build on the already-validated structural decisions from the wireframing stage."},
                {"question": "What combines in this stage of the course to produce the final high-fidelity screen?", "options": ["Only visual taste with no prior planning", "Research-informed structure, grid and hierarchy, accessible colors, type scale, and reusable components", "Only the button component", "A random selection of fonts"], "correct_index": 1, "explanation": "High-fidelity design is the culmination of all the structural and systemic decisions made in the preceding days."}
            ],
            "resources": []
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Visual Design and Systems",
            "title": "Mobile-First Design Principles and Responsive Layouts",
            "learning_objective": "By the end of this class, you will be able to design a mobile-first layout and explain how it would adapt to a larger tablet or desktop screen.",
            "duration_minutes": 30,
            "content_html": "<p>Across Africa, the overwhelming majority of internet and app usage happens on mobile phones, often mid-range or budget Android devices, not desktop computers. Designing mobile-first, rather than shrinking a desktop design down, is both a technical best practice and a direct reflection of how your real users will actually experience your product.</p><h2>What Mobile-First Really Means</h2><p>Mobile-first design means starting your design process on the smallest, most constrained screen size first, forcing you to prioritize only the most essential content and actions, then expanding thoughtfully for larger screens rather than cramming a desktop layout down into a small one. Touch targets, the tappable area of a button or icon, need to be large enough for a finger, generally at least 44 by 44 pixels, which is a very different constraint than a precise mouse cursor on desktop.</p><h2>Worked Example</h2><p>Designing Blessing's home screen mobile-first, you might show only the current weekly total and a single prominent add-expense button on the small screen, deliberately leaving out a detailed chart that would feel cramped. Explaining how this adapts to a tablet, you might introduce a second column showing a simple spending chart alongside the total, since the extra width comfortably accommodates it without cramming. This is different from designing a busy desktop dashboard first and then trying to figure out what to delete for mobile, which usually produces a worse mobile experience because deletion decisions are harder than addition decisions.</p>",
            "key_concepts": ["Mobile-first design", "Touch target sizing", "Responsive adaptation", "Content prioritization", "Progressive enhancement for larger screens"],
            "practical_exercise": {
                "title": "Design Mobile-First and Explain Tablet Adaptation",
                "instructions": "Take your high-fidelity screen from Day 13 (or design a new home screen) and ensure all buttons meet a minimum 44 by 44 pixel touch target. Then write a short paragraph explaining exactly how the layout would expand for a tablet-sized screen, specifying what new content or columns would be added, not just stretched."
            },
            "quiz": [
                {"question": "What does mobile-first design mean?", "options": ["Designing for desktop first, then adapting down", "Starting the design process on the smallest screen size and expanding thoughtfully for larger screens", "Only designing for mobile and ignoring other devices entirely", "Using mobile phones to sketch designs"], "correct_index": 1, "explanation": "Mobile-first means designing for the most constrained screen first, then thoughtfully expanding for larger screens."},
                {"question": "What is a recommended minimum touch target size for buttons on mobile?", "options": ["10 by 10 pixels", "44 by 44 pixels", "200 by 200 pixels", "There is no recommended minimum"], "correct_index": 1, "explanation": "A minimum of roughly 44 by 44 pixels ensures buttons are comfortably tappable with a finger."},
                {"question": "Why is mobile-first design particularly relevant for products aimed at African users?", "options": ["African users primarily use desktop computers", "The majority of internet and app usage in Africa happens on mobile devices", "Mobile-first design is required by African law", "It has no particular relevance"], "correct_index": 1, "explanation": "Given how dominant mobile usage is across African markets, designing mobile-first reflects real user context."}
            ],
            "resources": []
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Visual Design and Systems",
            "title": "Micro-interactions and Motion Basics",
            "learning_objective": "By the end of this class, you will be able to design a simple micro-interaction using Figma's smart animate feature between two states.",
            "duration_minutes": 30,
            "content_html": "<p>Small moments of feedback, a button that visibly responds to a tap, a checkbox that animates when checked, make a product feel alive and trustworthy rather than static and unresponsive. These micro-interactions are subtle but noticeably absent in amateur work, and skilled use of them is a clear signal of design maturity.</p><h2>Designing Purposeful Motion</h2><p>A micro-interaction typically has a trigger, such as a tap, a rule for what happens, and feedback showing the result, ideally completing quickly, generally under half a second, so it feels responsive rather than sluggish. Figma's smart animate feature lets you create two frames representing before and after states of an element, and Figma automatically interpolates the transition when you connect them in prototype mode, which you will use fully in the next module.</p><h2>Worked Example</h2><p>For Blessing's save button, a simple micro-interaction shows the button slightly shrinking and changing to a confirmed state with a small checkmark icon the instant it is tapped, giving immediate visual confirmation the action registered, which matters enormously on a slower mobile connection where the actual save might take a moment longer. Creating this in Figma means designing a default-state frame and a confirmed-state frame with the checkmark, then using smart animate between them, a small detail that meaningfully increases a user's trust that their tap actually worked.</p>",
            "key_concepts": ["Micro-interactions", "Trigger, rule, feedback", "Smart animate", "Perceived responsiveness", "Motion duration"],
            "practical_exercise": {
                "title": "Design a Smart Animate Micro-interaction",
                "instructions": "In Figma, create two frames representing the before and after states of one interactive element in your product, such as a button changing to a confirmed state. Connect them using smart animate in prototype mode and test the transition. Note the trigger, rule, and feedback for your micro-interaction in one sentence each."
            },
            "quiz": [
                {"question": "What are the three parts of a well-designed micro-interaction?", "options": ["Color, font, and spacing", "Trigger, rule, and feedback", "Wireframe, prototype, and handoff", "Persona, journey, and sitemap"], "correct_index": 1, "explanation": "A micro-interaction is structured around a trigger, the rule governing what happens, and feedback shown to the user."},
                {"question": "What does Figma's smart animate feature do?", "options": ["It writes code automatically", "It automatically interpolates a transition between two connected frames representing different states", "It generates color palettes", "It creates user personas"], "correct_index": 1, "explanation": "Smart animate creates a smooth transition between two frames based on matching layer properties."},
                {"question": "Why does immediate visual feedback on a tap matter, especially on slower mobile connections?", "options": ["It has no real benefit", "It reassures the user their action registered even if the actual server response takes longer", "It slows down the app intentionally", "It replaces the need for the action to actually work"], "correct_index": 1, "explanation": "Immediate feedback builds user trust that the interface is responsive, even while a slower backend process completes."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Prototyping and Testing",
            "title": "Building Interactive Prototypes in Figma",
            "learning_objective": "By the end of this class, you will be able to connect multiple screens into a clickable Figma prototype covering a full user flow.",
            "duration_minutes": 35,
            "content_html": "<p>A set of disconnected static screens cannot be tested with real users or convincingly demonstrated to a client or employer. An interactive prototype, where a user can actually tap through a realistic flow, is what turns your design work into something that feels like a real product, and it is required for your final capstone.</p><h2>Wiring Up a Prototype</h2><p>In Figma's prototype mode, you connect elements on one frame to another frame using an interaction, typically on tap, navigate to, choosing a transition style such as instant or a simple animation. A complete prototype should cover an entire meaningful flow start to finish, such as opening the app, adding an expense, and seeing the updated total, not just one isolated screen, since a partial flow cannot be properly usability tested.</p><h2>Worked Example</h2><p>For Blessing's app, wiring the full add-expense flow means connecting the home screen's add button to the quick-add screen, connecting the quick-add screen's save button through your Day 15 micro-interaction to a brief confirmation state, and then automatically navigating back to an updated home screen showing the new total reflected. Testing this yourself by clicking through it exactly as a real user would, on both desktop preview and Figma's mobile app if possible, often reveals missing connections or confusing dead ends you did not notice while designing individual screens in isolation.</p>",
            "key_concepts": ["Figma prototype mode", "Interaction connections", "Complete flow coverage", "Transition styles", "Self-testing a prototype"],
            "practical_exercise": {
                "title": "Wire a Complete Prototype Flow",
                "instructions": "Using all the high-fidelity screens you have built this month, connect them in Figma's prototype mode into one complete, clickable flow from start to finish (for example: home screen, add action, confirmation, updated home screen). Test the full flow yourself by clicking through it and fix any broken or missing connections."
            },
            "quiz": [
                {"question": "Why is a complete end-to-end flow important in a prototype rather than a single isolated screen?", "options": ["Isolated screens are always sufficient for testing", "A partial flow cannot be properly usability tested since users need a realistic beginning-to-end experience", "Figma cannot connect more than one screen", "Complete flows take less time to build"], "correct_index": 1, "explanation": "Meaningful usability testing requires users to move through a full, realistic task, not an isolated screen."},
                {"question": "What does an on tap, navigate to interaction do in Figma's prototype mode?", "options": ["It deletes the connected frame", "It defines what happens (moving to another frame) when a user taps a specific element", "It exports the file as a PDF", "It changes the file's color palette"], "correct_index": 1, "explanation": "This interaction type connects a trigger, tapping an element, to a resulting action, navigating to another frame."},
                {"question": "Why is it useful to click through your own prototype before sharing it for testing?", "options": ["It is not useful and wastes time", "It often reveals missing connections or confusing dead ends not obvious while designing screens in isolation", "Figma requires this step to save the file", "It automatically fixes accessibility issues"], "correct_index": 1, "explanation": "Self-testing surfaces structural gaps that are easy to miss when screens are designed and viewed individually."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Prototyping and Testing",
            "title": "Usability Testing — Planning and Running a Session",
            "learning_objective": "By the end of this class, you will be able to write a usability test script with realistic tasks and run a session with a real participant.",
            "duration_minutes": 35,
            "content_html": "<p>Designers regularly fall in love with their own solutions, which is exactly why usability testing with real people, not just self-review, is considered essential professional practice, not an optional extra step. A design that seems obvious to its creator is often confusing to someone seeing it for the first time.</p><h2>Planning a Usability Test</h2><p>A usability test script includes a brief, neutral introduction explaining you are testing the design, not the participant, followed by realistic task-based instructions such as add an expense for lunch today rather than leading instructions like tap the plus button. While observing, note where the participant hesitates, clicks the wrong element, or expresses confusion out loud, and resist the urge to help them immediately, since their struggle is exactly the data you need.</p><h2>Worked Example</h2><p>Testing Blessing's prototype, a good task instruction is imagine you just spent five hundred naira on transport, please add this expense using the app, rather than please tap the add button, which would give away the answer instead of testing whether they can find it themselves. If the participant hesitates at the home screen, unsure where to tap, that hesitation itself is valuable data revealing your add button may not be visually prominent enough, exactly the kind of finding that leads to a meaningful design iteration in tomorrow's class.</p>",
            "key_concepts": ["Usability test script", "Task-based instructions", "Observing without helping", "Think-aloud method", "Recognizing hesitation as data"],
            "practical_exercise": {
                "title": "Run Your First Usability Test",
                "instructions": "Write a usability test script with a neutral introduction and three realistic, task-based instructions for your prototype. Run the test with one real participant, observing without helping. Take detailed notes on where they hesitated, clicked incorrectly, or expressed confusion, and submit your script plus your observation notes."
            },
            "quiz": [
                {"question": "Why should usability test instructions be task-based rather than directive, like tap the plus button?", "options": ["Task-based instructions are shorter to write", "Directive instructions give away the answer instead of testing whether the participant can find it themselves", "Directive instructions are illegal in usability testing", "There is no meaningful difference"], "correct_index": 1, "explanation": "Task-based instructions test whether the design itself guides the user, rather than testing their ability to follow direct commands."},
                {"question": "What should a usability test facilitator do when a participant hesitates or struggles?", "options": ["Immediately help them complete the task", "Observe and note the hesitation without helping, since it is valuable data", "End the test immediately", "Tell them the correct answer right away"], "correct_index": 1, "explanation": "Struggle and hesitation are exactly the signals a usability test is meant to surface, so intervening too early loses that data."},
                {"question": "Why is usability testing considered essential rather than optional in professional design work?", "options": ["It has no real value beyond looking thorough", "Designers can become too close to their own work to notice confusing elements a fresh user would catch", "It replaces the need for wireframing entirely", "It is only useful for very large companies"], "correct_index": 1, "explanation": "Real user feedback catches usability issues that a designer, deeply familiar with their own work, is likely to overlook."}
            ],
            "resources": []
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Prototyping and Testing",
            "title": "Analyzing Usability Test Results and Iterating",
            "learning_objective": "By the end of this class, you will be able to synthesize usability test findings into prioritized design changes and apply at least one to your prototype.",
            "duration_minutes": 30,
            "content_html": "<p>Collecting usability feedback is only half the job; a designer who cannot translate observations into concrete changes has not actually closed the loop. Employers specifically value seeing iteration in a portfolio, because it proves you can respond to evidence rather than defend your first idea indefinitely.</p><h2>From Observation to Action</h2><p>Start by listing every observation from your test notes, then group similar issues together, since three participants struggling with the same button is a stronger signal than one participant's one-off confusion. Prioritize issues by how many participants hit them and how severely they blocked the task, fixing high-frequency, high-severity issues first. For each prioritized issue, write a specific proposed design change, not just this is confusing, but here is exactly what will change and why it should help.</p><h2>Worked Example</h2><p>If your Day 17 test showed the participant hesitating at the home screen before finding the add button, and this is your only test, treat it as a hypothesis worth addressing rather than definitive proof, but still act on it: the specific fix might be increasing the button's size, adding a bolder color from your accessible palette, and adding a short text label alongside the icon rather than relying on an icon alone. Apply this change directly to your Figma prototype and note in your documentation exactly what changed and which test observation motivated it, which is exactly the story a hiring manager wants to see in a portfolio case study.</p>",
            "key_concepts": ["Findings synthesis", "Prioritizing by frequency and severity", "Specific design changes", "Iteration documentation", "Portfolio storytelling of iteration"],
            "practical_exercise": {
                "title": "Iterate Based on Test Findings",
                "instructions": "Review your Day 17 usability test notes and list at least two specific issues observed. For each, write a specific proposed design change and apply at least one of them directly to your Figma prototype. Write a short before-and-after note explaining what changed and why, referencing the specific test observation that motivated it."
            },
            "quiz": [
                {"question": "Why should a designer prioritize issues that multiple participants struggled with over a single one-off comment?", "options": ["Single comments should always be ignored completely", "A pattern across multiple participants is a stronger, more reliable signal than an isolated observation", "Single comments are always more important", "Frequency has no bearing on prioritization"], "correct_index": 1, "explanation": "Repeated observations across participants provide stronger evidence of a genuine, widespread usability issue."},
                {"question": "What makes a proposed design change specific rather than vague?", "options": ["Saying this is confusing with no further detail", "Describing exactly what will change, such as size, color, or label, and why it should help", "Avoiding any explanation at all", "Only referencing competitor apps"], "correct_index": 1, "explanation": "A specific, actionable change describes precisely what will be modified and the reasoning behind it."},
                {"question": "Why do employers value seeing iteration documented in a design portfolio?", "options": ["It makes the portfolio longer", "It proves the designer can respond to real evidence rather than only defending their first idea", "Iteration is required by Figma", "It has no real professional value"], "correct_index": 1, "explanation": "Demonstrated iteration shows a designer's process is grounded in evidence and responsive to real user feedback."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Prototyping and Testing",
            "title": "Designing Forms and Reducing User Friction",
            "learning_objective": "By the end of this class, you will be able to redesign a form to reduce the number of fields and cognitive effort required from the user.",
            "duration_minutes": 25,
            "content_html": "<p>Forms are where many products lose users, since every additional field or unclear label adds friction that can cause someone to abandon a task entirely, especially on mobile where typing is slower and more error-prone than on desktop.</p><h2>Reducing Form Friction</h2><p>Only ask for information that is genuinely necessary right now, deferring optional details to later or removing them entirely. Use the most appropriate input type for each field, such as a numeric keypad for a phone number field rather than a full keyboard, and provide smart defaults where possible, such as pre-selecting today's date. Group related fields visually and show clear, specific error messages exactly where the problem is, rather than a generic something went wrong message at the top of the form.</p><h2>Worked Example</h2><p>A signup form asking for full name, email, phone number, date of birth, and a security question before letting someone even try the app creates significant friction and likely drop-off. A friction-reduced version might ask only for a phone number and a password to get started, since that is the minimum needed to create an account, and defer optional profile details like full name to a later point after the user has already experienced value from the app. This ordering, minimum viable information first, is a pattern seen across most successful African fintech and consumer apps for exactly this reason.</p>",
            "key_concepts": ["Form friction", "Minimum necessary fields", "Appropriate input types", "Smart defaults", "Specific error messaging"],
            "practical_exercise": {
                "title": "Redesign a High-Friction Form",
                "instructions": "Find a signup or data-entry form from a real app you have used that felt long or annoying. List every field it asked for, then redesign it in Figma, removing or deferring any field that is not strictly necessary to get started, and note which input type you would use for each remaining field."
            },
            "quiz": [
                {"question": "Why should optional information be deferred rather than requested upfront in a signup form?", "options": ["Deferred information is never actually needed", "Reducing upfront friction lowers the chance a user abandons the task before experiencing value", "Forms with more fields always convert better", "It is a legal requirement"], "correct_index": 1, "explanation": "Minimizing upfront requirements reduces drop-off, letting users reach value faster before being asked for more."},
                {"question": "Why is using a numeric keypad input type important for a phone number field on mobile?", "options": ["It has no real effect on usability", "It reduces typing effort and errors compared to a full keyboard", "It is required by every operating system", "It changes the color of the field"], "correct_index": 1, "explanation": "Matching the input type to the expected data reduces friction and typing errors, especially on mobile."},
                {"question": "What is a better practice for form error messages than a generic something went wrong message?", "options": ["No error messages at all", "Clear, specific messages shown exactly where the problem occurred", "Only showing errors after the entire form is submitted with no detail", "Redirecting the user to a different page"], "correct_index": 1, "explanation": "Specific, well-placed error messages help users understand and fix the exact problem quickly."}
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Prototyping and Testing",
            "title": "Designing for Accessibility (WCAG Basics)",
            "learning_objective": "By the end of this class, you will be able to audit a screen against basic WCAG accessibility criteria and propose specific fixes.",
            "duration_minutes": 30,
            "content_html": "<p>Accessible design is not a niche specialty, it is baseline professional practice, and clients and employers increasingly require it explicitly, both for ethical reasons and because it often overlaps with legal compliance requirements in many markets.</p><h2>Core Accessibility Checks</h2><p>Beyond the color contrast covered on Day 11, key checks include ensuring interactive elements are large enough and clearly distinguishable, that the design does not rely on color alone to convey meaning, such as showing an error only in red with no icon or text label for users who cannot perceive that color difference, and that a logical reading and navigation order exists for anyone using a screen reader. Text should also be resizable without breaking the layout, since some users increase device font sizes significantly.</p><h2>Worked Example</h2><p>Auditing Blessing's budget screen, if a warning that spending is near the limit is shown only as a red progress bar with no text, a colorblind user or someone with low vision may miss the warning entirely. The fix is adding a text label like eighty percent of weekly budget used alongside the color, and optionally a warning icon, so the meaning does not rely on color perception alone. This single fix, redundant coding of meaning through color plus text or icon, is one of the most common and impactful accessibility improvements across real products.</p>",
            "key_concepts": ["WCAG basics", "Color-independent meaning", "Screen reader navigation order", "Resizable text", "Redundant coding of information"],
            "practical_exercise": {
                "title": "Audit One Screen for Accessibility",
                "instructions": "Choose one high-fidelity screen from your project. Check whether any information is conveyed using color alone, whether touch targets meet minimum size, and whether text hierarchy would make sense to someone using a screen reader. Write down at least two specific accessibility issues found and your proposed fix for each."
            },
            "quiz": [
                {"question": "Why is it a problem to convey an error or warning using color alone, such as a red progress bar with no text?", "options": ["Color is always the clearest way to convey meaning", "Users with color blindness or low vision may not perceive the meaning without a text or icon backup", "Red is not a valid color for warnings", "It has no real accessibility impact"], "correct_index": 1, "explanation": "Relying solely on color excludes users who cannot distinguish that color difference, so meaning should be reinforced with text or icons."},
                {"question": "What does redundant coding of information mean in accessible design?", "options": ["Repeating the exact same visual element twice", "Conveying meaning through more than one channel, such as color plus text or an icon", "Writing duplicate code in development", "Using the same color for every element"], "correct_index": 1, "explanation": "Redundant coding ensures meaning is accessible even if one channel, like color, cannot be perceived by a given user."},
                {"question": "Why should text remain resizable without breaking a screen's layout?", "options": ["Resizable text has no accessibility benefit", "Some users increase device font sizes significantly and still need the design to remain usable", "It is only relevant for print design", "Layouts never need to accommodate different text sizes"], "correct_index": 1, "explanation": "Users who rely on larger text sizes for readability still need the interface to remain functional and legible."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Collaboration and Professional Practice",
            "title": "Handoff — Preparing Designs for Developers",
            "learning_objective": "By the end of this class, you will be able to prepare a Figma file with proper naming, spacing annotations, and specs ready for developer handoff.",
            "duration_minutes": 30,
            "content_html": "<p>A design that looks perfect in Figma but cannot be accurately built by a developer has not actually finished its job. Handoff, the process of preparing your files for engineering, is a frequently underestimated skill that directly affects how smoothly a real product actually ships.</p><h2>What Developers Need</h2><p>Layers and frames should be named clearly and logically, such as button-primary rather than Rectangle 47, since developers navigate your file structure directly. Figma's inspect panel automatically shows spacing, sizing, and color values to anyone with view access, but organizing your file with clear sections and consistent naming makes that information far easier to find. Flag any states that are not obvious from the static screens, such as an empty state, a loading state, or an error state, since developers need to know these exist even if you have not designed every single one.</p><h2>Worked Example</h2><p>Handing off Blessing's app, a developer opening your Figma file should immediately see clearly labeled frames like home-screen, add-expense-form, and confirmation-state, with your button and input components clearly named to match. If the home screen shows a populated list of expenses, but you have not designed what it looks like on day one before any expenses exist, you should explicitly flag this empty state as a gap in a note, rather than leaving the developer to guess or invent a solution that may not match your design intent.</p>",
            "key_concepts": ["Developer handoff", "Layer naming conventions", "Figma inspect panel", "Edge case states", "File organization for engineering"],
            "practical_exercise": {
                "title": "Prepare a File for Handoff",
                "instructions": "Take your final prototype file and rename all major frames and components with clear, descriptive names. Identify at least two edge-case states (such as empty, loading, or error) that you have not yet designed, and write a short note flagging each one for a developer, describing what should happen in that state even without a full visual design."
            },
            "quiz": [
                {"question": "Why does clear layer and frame naming matter for developer handoff?", "options": ["It has no real impact on development", "Developers navigate the file structure directly, so unclear names like Rectangle 47 slow them down and cause confusion", "Figma requires specific names to function", "Naming only affects the designer's own workflow"], "correct_index": 1, "explanation": "Developers rely on clear naming to understand and correctly implement the design structure."},
                {"question": "What should a designer do about states like empty, loading, or error that have not been fully designed?", "options": ["Ignore them and let the developer guess", "Explicitly flag them as gaps with a note describing the intended behavior", "Delete the entire prototype", "Assume they are unnecessary"], "correct_index": 1, "explanation": "Flagging undesigned states prevents developers from having to invent behavior that may not match the designer's intent."},
                {"question": "What does Figma's inspect panel automatically provide to someone with view access?", "options": ["Nothing useful for development", "Spacing, sizing, and color values for selected elements", "A full working code export with no adjustments needed", "User research data"], "correct_index": 1, "explanation": "The inspect panel surfaces measurement and style details directly from the design file, aiding accurate implementation."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Collaboration and Professional Practice",
            "title": "Design Critique — Giving and Receiving Feedback Like a Pro",
            "learning_objective": "By the end of this class, you will be able to give structured, specific design feedback and respond professionally to critique of your own work.",
            "duration_minutes": 25,
            "content_html": "<p>Design is a collaborative craft, and the ability to give and receive critique well is something teams and clients notice immediately, often more than raw visual talent. Poor critique habits, either vague praise or harsh unstructured criticism, waste everyone's time and damage working relationships.</p><h2>Structured Critique</h2><p>Good feedback is specific and tied to a goal, such as the button placement here makes it easy to miss on a small screen, rather than a vague I do not like this. A useful structure is to state what you observe, why it matters for the user or business goal, and, if you have one, a possible direction, without dictating the exact solution, since the designer receiving feedback should retain ownership of the final decision. When receiving critique yourself, resist the instinct to immediately defend your choice, and instead ask clarifying questions to fully understand the concern before responding.</p><h2>Worked Example</h2><p>A weak critique of Blessing's home screen says the colors feel off. A strong critique says the accent color used for the add button is very close in shade to the background, which could make it hard to notice quickly, especially given our earlier finding that users need to add expenses fast. This version identifies the specific element, explains the user impact, and connects back to actual research, making it immediately actionable rather than a matter of personal taste.</p>",
            "key_concepts": ["Structured critique", "Observation-impact-direction format", "Specific vs vague feedback", "Receiving feedback professionally", "Design ownership"],
            "practical_exercise": {
                "title": "Practice Structured Critique",
                "instructions": "Find one screen from a classmate, an online design community, or a real app. Write a structured critique using the observation, impact, and possible direction format for two separate elements on that screen. Then write two sentences reflecting on how you would respond if someone gave similarly specific feedback on your own work."
            },
            "quiz": [
                {"question": "What makes feedback like the colors feel off weak compared to more structured critique?", "options": ["It is too long", "It lacks specificity, does not identify what exactly is wrong, and gives no actionable direction", "It is technically incorrect", "Vague feedback is actually preferred by most designers"], "correct_index": 1, "explanation": "Vague feedback fails to identify a specific problem or its impact, making it hard to act on."},
                {"question": "What three elements does the observation, impact, direction critique structure include?", "options": ["Color, font, and spacing", "What is observed, why it matters for the user or goal, and a possible direction", "Budget, timeline, and scope", "Persona, journey, and wireframe"], "correct_index": 1, "explanation": "This structure moves feedback from vague opinion to specific, actionable, and reasoned critique."},
                {"question": "What should a designer do when receiving critique rather than immediately defending their choice?", "options": ["Ignore the feedback entirely", "Ask clarifying questions to fully understand the concern before responding", "Argue immediately to protect the original decision", "Change everything without evaluating the feedback"], "correct_index": 1, "explanation": "Understanding the concern fully before responding leads to more productive, professional collaboration."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Collaboration and Professional Practice",
            "title": "Case Study Storytelling — Presenting Your Design Process",
            "learning_objective": "By the end of this class, you will be able to structure a case study narrative that walks a reader through your design process and decisions.",
            "duration_minutes": 30,
            "content_html": "<p>A portfolio full of pretty final screens with no explanation tells an employer nothing about how you think, and hiring managers explicitly say they care more about process than final polish, because process is what predicts how you will perform on their actual team.</p><h2>Case Study Structure</h2><p>A strong case study typically follows a clear arc: the problem and context, your research and key insight, the design decisions that followed from that insight, the outcome or what you learned from testing, and honest reflection on what you would do differently with more time. Each section should connect logically to the next, so a reader can see your reasoning, not just admire a screenshot, and specific evidence, like an actual research quote or a specific usability test finding, is far more convincing than general claims.</p><h2>Worked Example</h2><p>A weak case study section says I designed a clean, modern interface for the app. A strong version says research revealed users struggled to log small cash transactions quickly, so I prioritized a one-tap quick-add flow over a full transaction form, and usability testing confirmed this reduced task completion time and hesitation compared to my first version, directly referencing your Day 4 interview finding and your Day 18 iteration. This version proves your design decisions were reasoned, not just aesthetic preferences, which is exactly what a hiring manager is trying to evaluate.</p>",
            "key_concepts": ["Case study structure", "Problem-to-outcome narrative", "Evidence-based storytelling", "Honest reflection", "Process over polish"],
            "practical_exercise": {
                "title": "Outline Your Case Study",
                "instructions": "Write a case study outline for your final project using the five-part structure: problem and context, research and key insight, design decisions, outcome or testing results, and reflection. Write two to three sentences for each section, referencing specific work you have produced this month."
            },
            "quiz": [
                {"question": "Why do hiring managers often say they care more about a designer's process than their final polished screens?", "options": ["Polish is never actually evaluated", "Process reveals how a candidate thinks and reasons, which predicts how they will perform on a real team", "Process is easier to fake than polish", "Final screens are irrelevant to hiring decisions"], "correct_index": 1, "explanation": "Understanding a candidate's reasoning process helps predict how they will approach real design problems on the job."},
                {"question": "What makes a case study section like I designed a clean, modern interface weak?", "options": ["It is too specific", "It lacks connection to research, reasoning, or evidence behind the decision", "It is factually incorrect", "It uses too much technical language"], "correct_index": 1, "explanation": "Without grounding in research or reasoning, such statements read as unsupported opinion rather than justified design thinking."},
                {"question": "What should the final section of a strong case study typically include?", "options": ["A list of tools used with no other content", "Honest reflection on what you would do differently with more time", "Only a screenshot of the final screen", "A generic thank you message"], "correct_index": 1, "explanation": "Honest reflection demonstrates self-awareness and growth mindset, both valued in hiring evaluations."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Collaboration and Professional Practice",
            "title": "Design Systems at Scale — Tokens, Libraries, and Consistency",
            "learning_objective": "By the end of this class, you will be able to explain how design tokens and shared libraries scale consistency across large products and teams.",
            "duration_minutes": 25,
            "content_html": "<p>Your mini design system from Day 12 works well for a single project, but real companies operate at a much larger scale, often across dozens of products and multiple design and engineering teams, requiring more formal systems. Understanding this next level, even conceptually, shows an employer you can grow into a larger organization.</p><h2>Tokens and Shared Libraries</h2><p>A design token is a named, centrally managed value, such as color-primary or spacing-medium, used instead of a hardcoded value directly in a design or code, so that a single update to the token propagates everywhere it is referenced, across both design files and the actual codebase. A shared component library, published from a central Figma file, lets multiple designers across different product teams pull from the exact same button, input, and card components rather than each recreating their own slightly different version.</p><h2>Worked Example</h2><p>At a larger company than a solo project, if the brand team decides to update the primary blue slightly, updating the color-primary token once in the shared library automatically updates every product across the entire company that references that token, in both design files and the live product code, rather than requiring dozens of designers and engineers to manually hunt down and update every individual usage. This is the same principle as your Day 12 component instances, applied at the scale of an entire organization instead of a single file.</p>",
            "key_concepts": ["Design tokens", "Shared component libraries", "Cross-team consistency", "Design-to-code token mapping", "Scaling design systems"],
            "practical_exercise": {
                "title": "Convert Your Palette to Tokens",
                "instructions": "Take your color palette and type scale from Days 10 and 11 and rewrite them as a token list using clear naming conventions, such as color-primary, color-error, spacing-small, spacing-medium, text-body, text-headline. Write two sentences explaining how this token list could be shared with a developer to keep design and code in sync."
            },
            "quiz": [
                {"question": "What is a design token?", "options": ["A physical object used in workshops", "A named, centrally managed value like a color or spacing measurement used instead of a hardcoded value", "A type of Figma plugin only", "A payment method for design software"], "correct_index": 1, "explanation": "Tokens are named values that centralize and propagate design decisions across files and code."},
                {"question": "What is the benefit of using tokens instead of hardcoded color or spacing values?", "options": ["Tokens make files load slower", "A single update to a token propagates the change everywhere it is referenced, across design and code", "Tokens have no practical benefit", "Tokens replace the need for a color palette entirely"], "correct_index": 1, "explanation": "Centralized tokens mean one change updates every instance, saving significant manual rework at scale."},
                {"question": "How do shared component libraries help larger organizations?", "options": ["They prevent any customization at all", "They let multiple teams pull from the same consistent components instead of each recreating their own versions", "They are only useful for a single designer working alone", "They replace the need for user research"], "correct_index": 1, "explanation": "Shared libraries maintain consistency across many products and teams by centralizing reusable components."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Collaboration and Professional Practice",
            "title": "Cross-Functional Collaboration with PMs and Engineers",
            "learning_objective": "By the end of this class, you will be able to describe how a designer collaborates with product managers and engineers across a typical feature's lifecycle.",
            "duration_minutes": 25,
            "content_html": "<p>Designers rarely work in isolation on a real team; most of the job involves collaborating with product managers who define priorities and business goals, and engineers who build what gets designed. Understanding these relationships helps you work effectively from your very first job, rather than learning it the hard way on the job.</p><h2>How the Roles Work Together</h2><p>A product manager typically defines the problem, the target user, and success metrics before design work starts in depth, and a designer should push back with research-informed questions if a requested feature does not seem to actually solve the user's real problem, using exactly the research and journey mapping skills from earlier this month. During implementation, engineers frequently surface technical constraints the designer did not anticipate, such as a third-party payment provider not supporting a specific input flow, requiring the designer to adapt the solution collaboratively rather than treating the original design as untouchable.</p><h2>Worked Example</h2><p>Imagine a product manager asks for a rewards points feature to increase engagement in Blessing's app. A collaborative designer asks what specific user problem this solves and how success will be measured, rather than immediately jumping to screens, potentially revealing through further research that the real driver of engagement is something else entirely. Later, if an engineer explains that showing real-time point balances requires an expensive backend change not currently planned, a good designer proposes an alternative, such as an end-of-week summary instead of real-time updates, that respects the constraint while still serving the underlying user need.</p>",
            "key_concepts": ["Cross-functional collaboration", "Product manager relationship", "Engineering constraints", "Pushing back with research", "Adaptive problem-solving"],
            "practical_exercise": {
                "title": "Practice a Collaboration Scenario",
                "instructions": "Write a short fictional scenario where a product manager requests a feature for your project that you suspect does not fully address the real user problem, based on your own research. Write the clarifying questions you would ask, and then write how you would adapt your design if an engineer told you a key part of your solution was technically difficult to build in the current timeline."
            },
            "quiz": [
                {"question": "What should a designer do if a product manager requests a feature that does not seem to solve the user's actual problem?", "options": ["Build exactly what was requested with no questions", "Push back with research-informed clarifying questions before starting design work", "Refuse to work on the project entirely", "Ignore the product manager's input completely"], "correct_index": 1, "explanation": "Using research to ask informed questions helps ensure the team is solving the right problem before investing design effort."},
                {"question": "How should a designer typically respond when an engineer surfaces a technical constraint mid-project?", "options": ["Insist the original design must be built exactly as specified regardless of constraints", "Collaborate to adapt the solution in a way that respects the constraint while still serving the user need", "Abandon the feature entirely", "Ignore the engineer's feedback"], "correct_index": 1, "explanation": "Adapting collaboratively to real constraints while preserving the underlying user goal is core to effective cross-functional work."},
                {"question": "What does a product manager typically define before design work begins in depth?", "options": ["The exact pixel values for every screen", "The problem, target user, and success metrics for a feature", "The engineering codebase structure", "The company's entire marketing strategy"], "correct_index": 1, "explanation": "Product managers typically frame the problem and goals that design and engineering then work to solve and build."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "UI/UX Career Paths and What a Design Portfolio Must Show",
            "learning_objective": "By the end of this class, you will be able to identify at least two UI/UX career paths and list the specific evidence a portfolio needs for each.",
            "duration_minutes": 25,
            "content_html": "<p>UI/UX design covers several distinct roles, and knowing which direction interests you helps you tailor your portfolio and job search, especially since Nigerian and African designers increasingly compete for remote roles at companies worldwide, not just locally.</p><h2>Common Design Career Paths</h2><p>A product designer works across the full process you practiced this month, research through prototyping, often at a startup or tech company. A UI or visual designer focuses more narrowly on high-fidelity interface and system work, valuable for agencies or brands needing strong visual craft. A UX researcher specializes in the research methods from week one, often at larger companies with dedicated research teams. Freelance and contract product design, common on platforms serving African talent, typically requires strong end-to-end case studies since clients cannot verify your process any other way except through your portfolio.</p><h2>Worked Example</h2><p>A product designer portfolio needs full case studies like your capstone project, showing research through testing. A UI-focused portfolio can lean more heavily on strong final visuals and a demonstrated design system, closer to your Day 12 and Day 24 work. A researcher-focused portfolio should emphasize interview methodology and synthesis, closer to your Days 3, 4, and 18 work. Recognizing which of these best matches your own strengths and interests, based on which weeks of this course you enjoyed most, should directly shape how you frame your capstone case study for job applications.</p>",
            "key_concepts": ["Product designer role", "UI or visual designer role", "UX researcher role", "Freelance product design", "Portfolio-role alignment"],
            "practical_exercise": {
                "title": "Choose Your Path and Align Your Portfolio",
                "instructions": "Reflect on which weeks of this course you enjoyed and performed best in (research, structure, visual design, or prototyping and testing). Choose the career path that best matches, and write three sentences on how you will emphasize that strength when presenting your final capstone case study to potential employers or clients."
            },
            "quiz": [
                {"question": "Which career path typically emphasizes strong final visuals and a demonstrated design system most heavily?", "options": ["UX researcher", "UI or visual designer", "Backend engineer", "Product manager"], "correct_index": 1, "explanation": "UI or visual designer roles focus most closely on interface craft and systematic visual consistency."},
                {"question": "What does a UX researcher role typically specialize in?", "options": ["Writing backend code", "Research methods such as interviews and synthesis of user insights", "Only visual polish of screens", "Marketing budget allocation"], "correct_index": 1, "explanation": "UX researchers focus on gathering and synthesizing user insight rather than the full design and prototyping process."},
                {"question": "Why do freelance and contract product designers particularly need strong end-to-end case studies?", "options": ["Case studies are not important for freelancers", "Clients cannot verify a freelancer's process any other way except through the portfolio itself", "Freelancers do not need portfolios", "Case studies are only required for full-time roles"], "correct_index": 1, "explanation": "Without an internal team to vouch for their work, freelancers rely heavily on portfolio case studies to prove their process and skill."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Common UX Interview Questions and Portfolio Walkthroughs",
            "learning_objective": "By the end of this class, you will be able to confidently deliver a five-minute portfolio walkthrough answering common UX interview questions.",
            "duration_minutes": 30,
            "content_html": "<p>Most design interviews include a portfolio walkthrough where you present your own work and answer questions about your decisions in real time, and being unprepared for this specific format, even with strong work, can cost you the role. Practicing this today directly prepares you for real interviews.</p><h2>What Interviewers Actually Ask</h2><p>Common questions include walk me through your process on this project, which should follow your Day 23 case study structure, what was the biggest challenge and how did you handle it, best answered with a specific, honest example rather than a vague generality, and why did you make this particular design decision, which should reference research or testing evidence whenever possible rather than personal taste. Interviewers are also listening for how you talk about feedback and iteration, since design maturity shows up more in how you discuss change than in a single polished screenshot.</p><h2>Worked Example</h2><p>A weak answer to why did you make the button this color says I just liked how it looked. A strong answer says the button color needed to pass accessibility contrast requirements while still standing out as the primary action, referencing your Day 11 and Day 9 work directly, and connects back to a specific testing observation if you have one. Practicing this kind of specific, evidence-based answer out loud, not just having it in your head, is what makes the difference in a real, sometimes nerve-wracking interview setting.</p>",
            "key_concepts": ["Portfolio walkthrough format", "Process and challenge questions", "Evidence-based decision explanations", "Discussing feedback and iteration", "Interview preparation practice"],
            "practical_exercise": {
                "title": "Practice Your Portfolio Walkthrough",
                "instructions": "Using your capstone project so far, prepare and practice out loud, timing yourself, a five-minute portfolio walkthrough covering your process, one specific challenge you faced, and one design decision you can justify with research or testing evidence. Write a short outline of what you said in each section."
            },
            "quiz": [
                {"question": "Why is being unprepared for a portfolio walkthrough risky even if your actual design work is strong?", "options": ["Portfolio walkthroughs are never actually part of design interviews", "The format itself is a skill that must be practiced separately from the quality of the work shown", "Interviewers never ask about process", "Strong work always speaks for itself with no explanation needed"], "correct_index": 1, "explanation": "Presenting and articulating your process clearly is a distinct skill from producing the work itself, and it needs separate practice."},
                {"question": "What makes an answer to why did you make this design decision strong rather than weak?", "options": ["Saying I just liked how it looked", "Referencing research or testing evidence behind the decision", "Avoiding the question entirely", "Talking only about color trends in general"], "correct_index": 1, "explanation": "Evidence-based reasoning demonstrates that decisions were grounded in user needs, not just personal preference."},
                {"question": "What are interviewers often specifically listening for beyond the final visual result?", "options": ["Only the exact hex codes used", "How the candidate discusses feedback, challenges, and iteration", "The number of tools used", "The length of the presentation only"], "correct_index": 1, "explanation": "How a candidate talks about handling feedback and iterating reveals design maturity and process quality."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Freelancing as a Designer — Finding Clients in Nigeria and Beyond",
            "learning_objective": "By the end of this class, you will be able to identify three concrete channels for finding freelance design clients and draft a client-facing service offer.",
            "duration_minutes": 25,
            "content_html": "<p>Freelancing is a realistic and common path for Nigerian designers, offering income and portfolio-building opportunities even before landing a full-time role, but succeeding at it requires treating it as a small business, not just waiting for work to appear.</p><h2>Finding Real Clients</h2><p>Common channels include global freelance platforms, local business networks such as WhatsApp groups and LinkedIn connections within Nigeria's growing startup and small business community, and direct outreach to small businesses that clearly need design help, such as a local business with an outdated or confusing website. A clear service offer, describing exactly what you deliver, for whom, and roughly what it costs, converts interested contacts into paying clients far better than a vague I do UI/UX design.</p><h2>Worked Example</h2><p>Instead of a vague offer, a strong freelance pitch to a small Nigerian business might say I design mobile-friendly websites for local businesses that currently do not work well on phones, delivering a clickable prototype within one week for a fixed price, directly addressing a specific, visible pain point, mobile usability, that you learned to identify and fix in weeks two and three of this course. Reaching out to five real small businesses with this specific offer, rather than posting a generic message hoping for replies, is a far more effective way to land your first paid client.</p>",
            "key_concepts": ["Freelance client channels", "Local business networks", "Specific service offers", "Direct outreach", "Treating freelancing as a business"],
            "practical_exercise": {
                "title": "Draft Your Freelance Service Offer",
                "instructions": "Write a specific, one-paragraph freelance service offer describing exactly what you deliver, for what type of client, and in what rough timeframe, addressing a specific pain point you are equipped to solve. List three real channels (platforms, groups, or direct outreach targets) where you could share this offer."
            },
            "quiz": [
                {"question": "Why does a specific service offer convert better than a vague statement like I do UI/UX design?", "options": ["Specificity has no real effect on client interest", "A specific offer clearly addresses a pain point a potential client can immediately recognize in their own business", "Vague offers are always more professional", "Clients prefer not knowing what they are paying for"], "correct_index": 1, "explanation": "Specific offers help potential clients immediately see the relevance and value to their own situation."},
                {"question": "What is one concrete channel mentioned for finding freelance design clients in Nigeria?", "options": ["Only cold-calling random phone numbers", "Local business networks such as WhatsApp groups and LinkedIn connections", "Waiting passively for clients to appear", "Only applying to full-time jobs"], "correct_index": 1, "explanation": "Local networks and direct outreach are practical, accessible channels for finding early freelance clients."},
                {"question": "Why is direct outreach to specific small businesses often more effective than a generic public post?", "options": ["Direct outreach is never effective", "It targets a real, identified need rather than hoping the right person happens to see a generic message", "Public posts always outperform direct outreach", "Small businesses never need design help"], "correct_index": 1, "explanation": "Targeted outreach addressing a specific, visible problem is more likely to convert into an actual paying client."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Ethical Design — Avoiding Dark Patterns",
            "learning_objective": "By the end of this class, you will be able to identify common dark patterns and redesign an example to be ethical and transparent.",
            "duration_minutes": 25,
            "content_html": "<p>As designers gain skill in persuasion, layout, and hierarchy, that same skill can be misused to manipulate users against their own interests. Understanding dark patterns is both an ethical responsibility and a practical career skill, since regulators worldwide are increasingly scrutinizing manipulative design practices.</p><h2>Common Dark Patterns</h2><p>Confirmshaming uses guilt-inducing language on a decline option, such as no, I do not want to save money, to pressure users into a choice. A roach motel makes it easy to sign up but deliberately difficult to cancel or unsubscribe. Hidden costs reveal extra fees only at the final step of checkout after a user has already invested time in the process. Forced continuity silently charges a user after a free trial ends without a clear, easy-to-find reminder or simple cancellation path.</p><h2>Worked Example</h2><p>Imagine a subscription app for Blessing's budgeting tool uses a dark pattern where canceling requires navigating through five confusing screens and a customer service chat, while signing up takes one tap, a classic roach motel pattern. An ethical redesign makes cancellation just as easy to find and complete as signup, perhaps a single clear button in account settings, even though this may reduce short-term revenue from users who forget to cancel. This is exactly the kind of design decision an employer wants to know you would push back on, since ethical design builds long-term trust and increasingly avoids real regulatory and reputational risk.</p>",
            "key_concepts": ["Dark patterns", "Confirmshaming", "Roach motel pattern", "Hidden costs", "Ethical design tradeoffs"],
            "practical_exercise": {
                "title": "Identify and Redesign a Dark Pattern",
                "instructions": "Find one real example of a dark pattern you have encountered in an app or website (or research one online). Describe exactly what makes it manipulative, then sketch or describe an ethical redesign of that same flow that respects the user's autonomy and transparency."
            },
            "quiz": [
                {"question": "What is a roach motel dark pattern?", "options": ["A pattern that makes signup difficult but cancellation easy", "A pattern that makes signup easy but cancellation deliberately difficult", "A pattern related only to physical retail stores", "A pattern used exclusively in gaming apps"], "correct_index": 1, "explanation": "The roach motel pattern deliberately makes entering a service easy while making leaving it hard."},
                {"question": "What is confirmshaming?", "options": ["Praising a user for making a purchase", "Using guilt-inducing language on a decline option to pressure a user's choice", "A method for testing color contrast", "A type of accessibility audit"], "correct_index": 1, "explanation": "Confirmshaming manipulates users through guilt-laden wording rather than a neutral, respectful choice."},
                {"question": "Why might an employer want a designer who would push back against dark patterns, even if they could increase short-term revenue?", "options": ["Ethical concerns are never relevant to business decisions", "Dark patterns carry long-term reputational and increasing regulatory risk that outweighs short-term gains", "Dark patterns always increase long-term revenue with no downside", "Employers never consider ethics in hiring"], "correct_index": 1, "explanation": "Manipulative design increasingly carries real regulatory and trust risks that can outweigh short-term gains."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Kickoff: Your Full Product Design Capstone",
            "learning_objective": "By the end of this class, you will be able to assemble a scope and work plan for your final product design case study and begin executing it.",
            "duration_minutes": 30,
            "content_html": "<p>Today you formally begin your final capstone: a complete digital product case study covering research, personas, wireframes, a high-fidelity interactive prototype, and usability testing, exactly as described in this course's final project brief. This is where every skill from the past 29 days comes together into one cohesive, portfolio-ready deliverable.</p><h2>Planning Your Capstone</h2><p>Start by confirming your product idea and target user, ideally building on work you have already started this month rather than beginning from nothing. Write a short scope statement listing exactly what your case study will include: at least one persona grounded in real or realistic research from Days 3 through 5, a journey map and sitemap from Days 6 and 7, low-fidelity wireframes for your core flow from Day 8, a high-fidelity design using your design system from Days 9 through 15, a fully connected interactive prototype from Day 16, and a usability test with at least three participants with documented iteration from Days 17 and 18.</p><h2>Getting Started Today</h2><p>Begin actual execution now: if you have not already conducted real user interviews, schedule and conduct at least one today, or review and formalize the research you have already gathered this month into a clear persona and journey map, since this research foundation is what every later design decision in your case study will need to reference and justify.</p>",
            "key_concepts": ["Capstone scoping", "Full case study assembly", "Research-to-prototype pipeline", "Multi-participant usability testing", "Portfolio-ready deliverable"],
            "practical_exercise": {
                "title": "Start Your Final Product Design Capstone",
                "instructions": "This IS the start of your final project. Write a one-page scope statement for your capstone case study listing your product idea, target user, and the specific deliverables you will produce (persona, journey map, wireframes, high-fidelity prototype, usability test). Then take the first concrete step: either conduct one real user interview today or formalize your existing research notes into a documented persona."
            },
            "quiz": [
                {"question": "How many usability test participants does the final capstone project require at minimum?", "options": ["None", "At least three", "Fifty", "Exactly one"], "correct_index": 1, "explanation": "The final project brief specifies usability testing with at least three participants, with documented feedback and iteration."},
                {"question": "What should the capstone scope statement written today reference?", "options": ["A completely new topic unrelated to the rest of the course", "The specific deliverables and skills practiced across the previous 29 days", "Only the final high-fidelity screens with no earlier work", "A different student's project"], "correct_index": 1, "explanation": "The capstone is designed to integrate and demonstrate the full skill set built throughout the course, not a disconnected new topic."},
                {"question": "What is suggested as the very first concrete action to take today toward the capstone?", "options": ["Skip straight to high-fidelity visual design", "Conduct a real user interview or formalize existing research into a persona", "Write the final case study conclusion first", "Design the prototype's micro-interactions first"], "correct_index": 1, "explanation": "Since every later decision depends on it, starting with solid research grounding is the recommended first concrete step."}
            ],
            "resources": [
                {"label": "Figma Resources", "url": "https://www.figma.com/resources/"}
            ]
        }
    ]
}
