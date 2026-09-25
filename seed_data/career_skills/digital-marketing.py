"""Seed data for the Digital Marketing & Growth 30-Day Skill Class."""

SKILL = {
    "slug": "digital-marketing",
    "name": "Digital Marketing & Growth",
    "tagline": "Learn to plan, run, and measure real growth campaigns across social, search, email, and paid channels for African markets.",
    "description": "Digital marketing is one of the fastest routes into paid freelance work and full-time roles for Nigerian and African students, since almost every business, from a campus food vendor to a fintech startup, now needs someone who can grow an audience and convert it into customers online. This track builds real, channel-specific skills including SEO, paid ads, email, and content strategy, then ties them together into one complete growth campaign a student can show a client or employer. It matters because digital marketing hiring is driven almost entirely by proof of results, not just certificates.",
    "level": "beginner",
    "estimated_hours": 55,
    "course_title": "30-Day Digital Marketing & Growth Career Track",
    "course_description": "After 30 days, a student can research an audience, choose the right marketing channels, write copy that converts, run basic paid campaigns, read analytics, and assemble a complete, budgeted growth campaign strategy for a real brand.",
    "final_project": {
        "title": "Complete Growth Campaign Strategy",
        "description": "Choose a real or realistic brand or product, such as a campus business, a local service provider, or a startup idea of your own, and build a full growth campaign strategy for it. You must define the target audience and buyer persona, select and justify specific marketing channels, produce a four-week content plan with sample post copy, allocate a realistic budget across paid and organic channels, and set specific, measurable KPI targets with a plan for tracking them. The final deliverable is a professional campaign strategy document you could present to a business owner or hiring manager to prove you can plan and justify a real growth initiative, not just describe marketing theory.",
        "difficulty": "advanced",
        "estimated_hours": 10,
        "skills_demonstrated": ["Audience research", "Channel strategy", "Content planning", "Budget allocation", "KPI setting and measurement", "Campaign presentation"],
        "rubric": [
            {"name": "Audience research and channel strategy justification", "max_points": 25},
            {"name": "Content plan quality and consistency", "max_points": 25},
            {"name": "Budget allocation realism and logic", "max_points": 25},
            {"name": "KPI clarity and measurement plan", "max_points": 25}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Marketing Foundations",
            "title": "How Digital Marketing Actually Drives Business Revenue",
            "learning_objective": "By the end of this class, you will be able to explain how a specific digital marketing activity connects to a measurable business outcome.",
            "duration_minutes": 25,
            "content_html": "<p>Many beginners think digital marketing means posting nice content and hoping people buy something. Businesses that actually pay for marketing think in terms of revenue, cost, and return, and understanding that connection from day one is what separates someone who can be trusted with a real budget from someone who cannot.</p><h2>The Revenue Connection</h2><p>Every marketing activity should be traceable to a business outcome: more awareness leading to more website visits, more visits leading to more leads or sales, and repeat engagement leading to customer retention and referrals. A business owner is not impressed by follower counts alone, they care about cost per customer acquired and whether that customer spends more than it cost to acquire them, a relationship called customer lifetime value versus customer acquisition cost.</p><h2>Worked Example</h2><p>Imagine a Lagos-based skincare brand spends fifty thousand naira on Instagram ads in a month and gains one hundred new customers, each of whom spends an average of eight thousand naira on their first order and is likely to reorder twice more over the following year. The acquisition cost is five hundred naira per customer, while the lifetime value is closer to twenty-four thousand naira per customer, a healthy return that justifies increasing the ad budget. A marketer who can explain this ratio, not just say the ads got a lot of likes, is the one a business owner trusts with a bigger budget next month.</p>",
            "key_concepts": ["Customer acquisition cost", "Customer lifetime value", "Marketing-to-revenue connection", "Vanity metrics vs business metrics", "Return on marketing spend"],
            "practical_exercise": {
                "title": "Calculate a Simple ROI Scenario",
                "instructions": "Write a short fictional scenario for a Nigerian business of your choice: a monthly ad spend, the number of new customers gained, and an estimated average spend per customer. Calculate the customer acquisition cost and briefly explain in two to three sentences whether the campaign appears worth continuing based on the numbers."
            },
            "quiz": [
                {"question": "What is customer acquisition cost?", "options": ["The total revenue a business earns in a month", "The average amount spent on marketing to gain one new customer", "The price of a company's most expensive product", "The number of social media followers a brand has"], "correct_index": 1, "explanation": "Customer acquisition cost measures how much is spent, on average, to acquire a single new paying customer."},
                {"question": "Why are follower counts alone considered a vanity metric rather than a business metric?", "options": ["Followers always convert directly into sales", "Follower counts do not necessarily indicate actual revenue, leads, or business outcomes", "Vanity metrics are the most important numbers to track", "Follower counts cannot be measured accurately"], "correct_index": 1, "explanation": "A large following does not guarantee revenue; business metrics track outcomes tied directly to money and growth."},
                {"question": "In the skincare brand example, why was the campaign considered worth continuing?", "options": ["It had the highest follower growth", "The customer lifetime value was significantly higher than the acquisition cost", "The ads were visually appealing", "The campaign ran for exactly one month"], "correct_index": 1, "explanation": "A lifetime value well above the acquisition cost indicates the marketing spend is generating a strong return."}
            ],
            "resources": [
                {"label": "HubSpot Marketing", "url": "https://www.hubspot.com/marketing"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Marketing Foundations",
            "title": "Understanding Your Target Audience and Building Buyer Personas",
            "learning_objective": "By the end of this class, you will be able to build a one-page buyer persona based on demographic and behavioral characteristics.",
            "duration_minutes": 25,
            "content_html": "<p>Marketing to everyone is the same as marketing to no one. Every strong campaign starts from a clear picture of who the buyer actually is, what they care about, and where they spend their time online, because that single decision shapes every channel and content choice that follows this month.</p><h2>Building a Real Persona</h2><p>A buyer persona should include demographic details like age range, location, and income level, but more importantly it should include behavioral details: what problem they are trying to solve, what platforms they actually use daily, and what objections might stop them from buying. Guessing is common among beginners, but stronger personas are built from real signals: customer conversations, social media comments on competitor pages, and reviews of similar products.</p><h2>Worked Example</h2><p>For a campus food delivery business, a weak persona says students who like food. A strong persona describes a 200-level university student living in a hostel, active mainly on WhatsApp and Instagram, frustrated by long queues at the cafeteria between lectures, price-sensitive but willing to pay a small delivery fee to save thirty minutes during a busy exam week. This level of detail immediately tells you WhatsApp and Instagram should be priority channels, and that your messaging should emphasize speed and convenience during specific busy periods, not generic phrases like delicious food delivered fast.</p>",
            "key_concepts": ["Buyer persona", "Demographic vs behavioral detail", "Audience-driven channel choice", "Customer objections", "Research-based personas"],
            "practical_exercise": {
                "title": "Build a Buyer Persona for Your Capstone Brand",
                "instructions": "Choose the brand or product you will use for your final capstone project. Write a one-page buyer persona including demographic details, their core problem, the platforms they most likely use daily, and one objection that might stop them from buying."
            },
            "quiz": [
                {"question": "Why is a persona like students who like food considered weak?", "options": ["It is too specific", "It lacks behavioral detail such as platforms used, specific problems, and objections", "It includes too much demographic information", "Weak personas are actually preferred in marketing"], "correct_index": 1, "explanation": "A useful persona needs behavioral specifics, not just a broad demographic label, to guide real channel and messaging decisions."},
                {"question": "What kind of information helps build a persona based on real signals rather than guesses?", "options": ["Random assumptions about what people might want", "Customer conversations, competitor page comments, and reviews of similar products", "Only the marketer's personal opinion", "The company's internal org chart"], "correct_index": 1, "explanation": "Real customer signals ground a persona in actual behavior rather than assumption."},
                {"question": "Why does a detailed persona directly influence channel selection?", "options": ["It does not influence channel selection at all", "Knowing which platforms the audience actually uses daily tells you where to focus marketing effort", "Channels are chosen randomly regardless of audience", "Only budget determines channel choice"], "correct_index": 1, "explanation": "Understanding where your specific audience spends their time online is essential for choosing effective channels."}
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Marketing Foundations",
            "title": "The Marketing Funnel — Awareness to Advocacy",
            "learning_objective": "By the end of this class, you will be able to map specific marketing activities onto each stage of the marketing funnel.",
            "duration_minutes": 25,
            "content_html": "<p>A common mistake beginners make is treating every piece of content the same way, using a hard sales pitch even for someone who has never heard of the brand before. The marketing funnel gives you a framework for matching the right message to the right stage of a customer's relationship with your brand.</p><h2>The Funnel Stages</h2><p>Awareness is when a potential customer first encounters your brand, often through social content, ads, or word of mouth, and the goal here is simply to be noticed and remembered, not to sell immediately. Consideration is when they are actively comparing options, where detailed content like reviews, comparisons, or case studies helps. Conversion is the actual purchase decision, where clear calls to action and removing friction matter most. Retention and advocacy come after purchase, focused on keeping customers happy and encouraging them to refer others.</p><h2>Worked Example</h2><p>For a Nigerian online bookstore, an awareness-stage Instagram Reel might simply show an aesthetically pleasing bookshelf with no direct sales pitch, just brand recognition. A consideration-stage blog post might compare the bookstore's delivery speed and pricing against alternatives. A conversion-stage email might offer a limited-time discount code with a clear buy now button. A retention-stage message might simply thank a customer after delivery and ask for a review, or offer a referral discount. Sending a hard buy now pitch at the awareness stage, before anyone knows or trusts the brand, is one of the most common reasons early campaigns underperform.</p>",
            "key_concepts": ["Marketing funnel", "Awareness stage", "Consideration stage", "Conversion stage", "Retention and advocacy"],
            "practical_exercise": {
                "title": "Map Content to Funnel Stages",
                "instructions": "For your capstone brand, write one example piece of content or messaging for each of the four funnel stages (awareness, consideration, conversion, retention), explaining briefly why the tone and goal differ at each stage."
            },
            "quiz": [
                {"question": "What is the main goal of content at the awareness stage of the funnel?", "options": ["Closing the sale immediately", "Being noticed and remembered by a potential customer for the first time", "Offering a discount code", "Asking for a customer review"], "correct_index": 1, "explanation": "Awareness-stage content is about first impressions and recognition, not immediate selling."},
                {"question": "Which funnel stage is most associated with detailed comparisons and case studies?", "options": ["Awareness", "Consideration", "Retention", "Advocacy"], "correct_index": 1, "explanation": "Consideration-stage content helps a potential customer who is actively comparing options make an informed decision."},
                {"question": "Why do early campaigns often underperform when they push a hard sales pitch at the awareness stage?", "options": ["Hard sales pitches always perform best regardless of stage", "The audience does not yet know or trust the brand enough to respond to a direct sales ask", "Awareness-stage content should never mention the product at all", "There is no real difference between funnel stages"], "correct_index": 1, "explanation": "Selling too early, before trust or recognition is built, mismatches the message to where the audience actually is in their journey."}
            ],
            "resources": [
                {"label": "HubSpot Marketing", "url": "https://www.hubspot.com/marketing"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Marketing Foundations",
            "title": "Setting Up Your First Brand's Social Media Presence",
            "learning_objective": "By the end of this class, you will be able to set up and optimize a business social media profile with a clear bio, contact info, and visual consistency.",
            "duration_minutes": 25,
            "content_html": "<p>A poorly set up social media profile actively loses potential customers, even before they see a single post, because an unclear bio, missing contact information, or an unprofessional profile picture immediately signals a brand is not serious or trustworthy.</p><h2>Profile Optimization Basics</h2><p>A strong business profile bio clearly states what the business does and who it serves within the first line, since most viewers decide to follow or leave within seconds. Contact information, whether a WhatsApp link, phone number, or website, should be immediately visible, not buried. Profile and cover images should be consistent with the brand's visual identity and readable even as a small thumbnail. A pinned post or story highlight showcasing best-selling products or key services gives new visitors an instant snapshot of what the business offers.</p><h2>Worked Example</h2><p>A weak Instagram bio for a small skincare brand says just a girl who loves skincare, with no link and no clear offer. A strong bio says Natural skincare for oily and combination skin, made in Lagos, followed by a clickable link to order via WhatsApp, and a highlight labeled Shop showing best-selling products with prices. The strong version answers what, for whom, and how to buy within seconds of a stranger landing on the page, which directly reduces the friction identified in the funnel discussion from Day 3.</p>",
            "key_concepts": ["Profile bio optimization", "Visible contact information", "Visual brand consistency", "Highlight and pinned content strategy", "First-impression friction"],
            "practical_exercise": {
                "title": "Write and Optimize a Bio",
                "instructions": "For your capstone brand, write a complete, optimized social media bio (under 150 characters) that states what the business does, who it serves, and includes a clear next step or contact method. List two additional profile elements (such as a highlight or pinned post) you would add to reduce first-visit friction."
            },
            "quiz": [
                {"question": "Why does an unclear bio hurt a business profile even before a visitor sees any posts?", "options": ["Bios have no real effect on visitor behavior", "Most viewers decide to follow or leave within seconds based on the bio and first impression", "Bios are only seen by existing followers", "Bio length does not matter"], "correct_index": 1, "explanation": "First impressions form quickly, and an unclear bio can cause a potential customer to leave before engaging further."},
                {"question": "What should a strong business bio communicate quickly?", "options": ["A long personal life story", "What the business does, who it serves, and how to take the next step", "Only the founder's name", "Unrelated hobbies and interests"], "correct_index": 1, "explanation": "An effective bio answers what, for whom, and how to act, all within a few seconds of reading."},
                {"question": "Why should contact information be immediately visible on a business profile?", "options": ["It is not important for conversion", "Hiding or burying contact information adds friction that can lose an interested potential customer", "Contact information is only needed for large companies", "Social platforms require it to be hidden"], "correct_index": 1, "explanation": "Easy access to contact information reduces friction for a visitor ready to take action, directly supporting conversion."}
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Marketing Foundations",
            "title": "Content Marketing Fundamentals — What to Post and Why",
            "learning_objective": "By the end of this class, you will be able to categorize content ideas into educational, entertaining, and promotional types and explain the recommended balance.",
            "duration_minutes": 25,
            "content_html": "<p>A page that only ever posts sales pitches tends to lose followers quickly, while a page that provides genuine value earns attention and trust that makes eventual sales messages far more effective. Understanding content types and balance is foundational to every content calendar you will build later this month.</p><h2>Content Categories</h2><p>Educational content teaches the audience something useful related to the brand's space, such as skincare tips from a skincare brand. Entertaining content builds emotional connection and relatability, such as a lighthearted trend or behind-the-scenes moment. Promotional content directly asks for a sale or action, such as a discount announcement. A commonly recommended balance is roughly the majority of content being educational or entertaining, with only a smaller portion being directly promotional, so followers feel the brand adds value rather than only asking for money.</p><h2>Worked Example</h2><p>A campus laundry service posting only discount announcements every day will likely see declining engagement and follower loss. A better content mix includes an educational post about how to remove common stain types, an entertaining post poking fun at the chaos of exam-week laundry piles, and only occasionally a direct promotional post about a discount for bulk orders. This balance keeps the audience engaged between purchases, so when a promotional post does appear, it reaches a warmer, more attentive audience rather than one that has already tuned the brand out.</p>",
            "key_concepts": ["Educational content", "Entertaining content", "Promotional content", "Content balance ratio", "Audience fatigue"],
            "practical_exercise": {
                "title": "Draft Three Content Ideas",
                "instructions": "For your capstone brand, write one specific content idea each for educational, entertaining, and promotional categories, including a short description of what each post would actually show or say. Note the platform you would use for each."
            },
            "quiz": [
                {"question": "What typically happens when a brand's social page posts only promotional, sales-focused content?", "options": ["Engagement usually increases steadily over time", "Followers often lose interest and engagement tends to decline", "This has no effect on audience behavior", "It always leads to higher sales regardless of engagement"], "correct_index": 1, "explanation": "Constant selling without value tends to fatigue an audience, reducing engagement over time."},
                {"question": "What is the general recommended content balance across educational, entertaining, and promotional posts?", "options": ["All content should be promotional", "Mostly educational or entertaining content, with only a smaller share directly promotional", "All content should be educational only", "There is no recommended balance"], "correct_index": 1, "explanation": "A majority-value, minority-promotional mix keeps audiences engaged while still driving sales messaging periodically."},
                {"question": "Why does a promotional post tend to perform better when it follows a period of valuable, non-promotional content?", "options": ["Promotional posts never perform differently based on context", "It reaches a warmer, more engaged audience that already trusts and pays attention to the brand", "Promotional posts should always come first", "Value-based content actively harms promotional performance"], "correct_index": 1, "explanation": "An audience kept engaged through valuable content is more receptive when a promotional message eventually appears."}
            ],
            "resources": [
                {"label": "HubSpot Blog", "url": "https://blog.hubspot.com"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Content, SEO, and Email",
            "title": "Copywriting That Converts — Headlines, CTAs, and Hooks",
            "learning_objective": "By the end of this class, you will be able to write a hook, a benefit-driven body, and a clear call to action for a piece of marketing copy.",
            "duration_minutes": 30,
            "content_html": "<p>The exact same product or offer can perform very differently depending purely on how it is written. Copywriting is a learnable, structured skill, not just natural talent, and small changes in wording routinely produce large differences in real click and conversion rates.</p><h2>Structure of Converting Copy</h2><p>A hook is the first line or headline that stops someone from scrolling past, often built around a specific pain point, a bold claim, or curiosity. The body should focus on benefits, what the customer gains, rather than only features, what the product technically does, since customers buy outcomes, not specifications. A call to action, or CTA, should be specific and create gentle urgency, such as order before Friday to get free delivery, rather than a vague and generic learn more.</p><h2>Worked Example</h2><p>A feature-focused, weak line for a phone accessory brand says our phone case is made of durable polycarbonate material. A benefit-focused, strong version says drop your phone on concrete and walk away without a cracked screen, directly translating the technical feature into an outcome the customer actually cares about. Paired with a hook like tired of replacing your phone screen every few months, and a specific CTA like grab yours before Friday's price goes up, this structure, hook, benefit, CTA, consistently outperforms unstructured, feature-only copy in real campaigns.</p>",
            "key_concepts": ["Hooks", "Benefits vs features", "Call to action", "Urgency and specificity", "Copy structure"],
            "practical_exercise": {
                "title": "Write a Complete Piece of Converting Copy",
                "instructions": "For your capstone brand's core product or service, write one complete piece of copy including a hook, a benefit-focused body of two to three sentences, and a specific call to action. Write a short note explaining which pain point or benefit your hook is built around."
            },
            "quiz": [
                {"question": "What is the main purpose of a hook in marketing copy?", "options": ["To list every technical feature of the product", "To stop someone from scrolling past and draw their attention in", "To close the sale immediately", "To thank existing customers"], "correct_index": 1, "explanation": "A hook's job is purely to capture attention at the very start of a piece of copy."},
                {"question": "Why is benefit-focused copy generally more effective than feature-focused copy?", "options": ["Features are always more persuasive than benefits", "Customers buy outcomes and results, not just technical specifications", "Benefit-focused copy is shorter, which is the only reason it works", "There is no meaningful difference between the two"], "correct_index": 1, "explanation": "Translating features into real outcomes connects more directly with what customers actually care about."},
                {"question": "What makes a call to action like order before Friday to get free delivery stronger than learn more?", "options": ["It is longer", "It is specific and creates a clear, time-bound reason to act now", "Learn more is always the better choice", "Length is the only factor that matters in a CTA"], "correct_index": 1, "explanation": "Specific, urgency-driven CTAs give a clear next step and a reason to act immediately, unlike vague phrasing."}
            ],
            "resources": [
                {"label": "HubSpot Blog", "url": "https://blog.hubspot.com"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Content, SEO, and Email",
            "title": "Search Engine Optimization (SEO) Basics",
            "learning_objective": "By the end of this class, you will be able to identify on-page SEO elements and apply basic optimization to a sample web page or blog post.",
            "duration_minutes": 30,
            "content_html": "<p>Paid ads stop generating traffic the moment you stop paying, but strong SEO can keep bringing free, relevant visitors to a website for months or years after the work is done, making it one of the most valuable long-term marketing skills a business can invest in.</p><h2>On-Page SEO Basics</h2><p>Search engines rank pages partly based on how well the content matches what a searcher is actually looking for, so page titles, headings, and the first paragraph should clearly include the main topic or keyword a customer would realistically search for. Meta descriptions, the short summary shown in search results, should be written to encourage a click, not just stuffed with keywords. Fast page load times and mobile-friendliness, especially important given how many Nigerian users browse on mobile data, also affect ranking.</p><h2>Worked Example</h2><p>A Lagos-based tailoring business writing a blog post to attract search traffic should not title it simply our services, since almost nobody searches that exact phrase. A better title, matching real search behavior, is something like affordable native wear tailors in Lagos, directly matching what a potential customer would type into a search engine. The post's first paragraph, headings, and even image file names should naturally reinforce this same topic, without awkwardly repeating the phrase so many times that it reads unnaturally, since modern search engines penalize obvious keyword stuffing.</p>",
            "key_concepts": ["On-page SEO", "Keyword matching search intent", "Meta descriptions", "Page speed and mobile-friendliness", "Keyword stuffing penalty"],
            "practical_exercise": {
                "title": "Optimize a Sample Page Title and Description",
                "instructions": "For your capstone brand, write a search-optimized page title (under 60 characters) and meta description (under 155 characters) for a page or blog post that a real potential customer might search for. Explain in one sentence what specific search phrase you are targeting and why."
            },
            "quiz": [
                {"question": "Why is SEO considered a valuable long-term marketing investment compared to paid ads?", "options": ["SEO produces results only while actively paying for it, exactly like ads", "SEO can continue generating free traffic long after the initial work is done, unlike ads which stop when spending stops", "SEO has no real difference from paid advertising", "SEO is always faster than paid ads"], "correct_index": 1, "explanation": "Organic SEO rankings can continue attracting traffic without ongoing spend, unlike paid campaigns."},
                {"question": "Why is our services considered a weak page title for SEO purposes?", "options": ["It is too short in character count", "It does not match how real customers actually search for that type of business", "Titles do not affect search rankings at all", "It contains too many keywords"], "correct_index": 1, "explanation": "Effective SEO titles reflect actual search behavior and intent, not generic internal business language."},
                {"question": "What is keyword stuffing, and why is it discouraged?", "options": ["Using a keyword naturally once in a title", "Repeating a keyword excessively and unnaturally, which search engines penalize", "Avoiding keywords entirely in content", "A technique required for good SEO rankings"], "correct_index": 1, "explanation": "Modern search engines penalize unnatural, excessive keyword repetition rather than rewarding it."}
            ],
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Content, SEO, and Email",
            "title": "Keyword Research for Content and Ads",
            "learning_objective": "By the end of this class, you will be able to identify a small set of relevant keywords for a business using free research methods.",
            "duration_minutes": 25,
            "content_html": "<p>Great content or a great ad aimed at the wrong keyword still fails, because it never reaches people actually searching for what the business offers. Keyword research is how you find out, in the audience's own words, what they are actually typing into search engines.</p><h2>Finding Real Keywords</h2><p>A simple starting method is typing a broad term related to the business into a search engine and noting the autocomplete suggestions, which reflect real, common searches. Free tools also show related searches and questions at the bottom of a results page. It is important to distinguish between high-competition broad keywords, which are hard for a small or new business to rank for, and more specific long-tail keywords, which have lower search volume but far higher intent and less competition.</p><h2>Worked Example</h2><p>A new phone repair business in Abuja searching only for the broad keyword phone repair faces enormous competition from large national brands. Researching further, autocomplete and related search suggestions might reveal a more specific, less competitive phrase like cracked screen repair same day Abuja, which has lower search volume overall but is searched by people with much clearer, more urgent buying intent, and is realistically achievable for a small business to rank for or target with a modest ad budget, unlike the broad, expensive keyword.</p>",
            "key_concepts": ["Keyword research", "Autocomplete and related searches", "Broad vs long-tail keywords", "Search intent", "Competition level"],
            "practical_exercise": {
                "title": "Research Five Keywords",
                "instructions": "For your capstone brand, use a search engine's autocomplete and related searches to identify five potential keywords or phrases, including at least two long-tail phrases with clear buying intent. List them and briefly note which one you believe has the strongest, most specific intent."
            },
            "quiz": [
                {"question": "What is a long-tail keyword?", "options": ["A very broad, high-competition search term", "A more specific search phrase with lower volume but often higher buying intent", "A keyword used only in email marketing", "A term that cannot be researched with free tools"], "correct_index": 1, "explanation": "Long-tail keywords are specific phrases that, despite lower search volume, often reflect clearer purchase intent and less competition."},
                {"question": "Why might a small new business struggle to compete for a broad keyword like phone repair?", "options": ["Broad keywords have no competition at all", "Large, established brands typically dominate broad, high-volume keywords, making them hard for small businesses to rank for", "Broad keywords are never searched by real users", "Small businesses are not allowed to target broad keywords"], "correct_index": 1, "explanation": "Broad, high-volume keywords tend to be heavily contested by larger, more established competitors."},
                {"question": "What is one free method for discovering real keyword phrases people search for?", "options": ["Guessing without any research", "Using search engine autocomplete and related search suggestions", "Only asking friends what they think people search for", "Keyword research cannot be done without paid tools"], "correct_index": 1, "explanation": "Autocomplete and related searches reflect actual real-world search behavior and are freely available."}
            ],
            "resources": []
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Content, SEO, and Email",
            "title": "Email Marketing — Building and Nurturing a List",
            "learning_objective": "By the end of this class, you will be able to design a simple lead magnet and write a three-email welcome sequence.",
            "duration_minutes": 30,
            "content_html": "<p>Unlike a social media following, an email list is an asset a business fully owns and controls, not subject to a platform's algorithm changes or account restrictions, which makes it one of the most durable and valuable channels a growing business can build.</p><h2>List Building and Nurturing</h2><p>A lead magnet is something valuable offered for free in exchange for an email address, such as a discount code, a useful guide, or early access to a product. Once someone joins a list, a welcome sequence, a short series of automated emails sent over the following days, builds trust before any hard sales pitch: the first email typically delivers the promised value, the second shares more useful content or a brand story, and the third can introduce a specific offer.</p><h2>Worked Example</h2><p>A Nigerian online fitness coach might offer a free seven-day home workout guide as a lead magnet in exchange for an email address. The welcome sequence's first email delivers the guide immediately as promised. The second email, sent two days later, shares a quick nutrition tip and the coach's own fitness journey to build connection and trust. The third email, sent a few days after that, introduces a paid coaching program with a specific limited-time signup bonus. This gradual sequence, value first, then trust, then offer, converts significantly better than immediately pitching the paid program in the very first email.</p>",
            "key_concepts": ["Lead magnet", "Email list ownership", "Welcome sequence", "Value-trust-offer sequencing", "List-building conversion"],
            "practical_exercise": {
                "title": "Design a Lead Magnet and Welcome Sequence",
                "instructions": "For your capstone brand, describe a specific lead magnet you would offer in exchange for an email signup. Then write one sentence summarizing the content and goal of each of three welcome sequence emails (value delivery, trust building, and offer)."
            },
            "quiz": [
                {"question": "Why is an email list considered a more durable marketing asset than a social media following?", "options": ["Email lists are less valuable than followers", "A business fully owns and controls its email list, unlike a social platform following subject to algorithm changes", "Email cannot be automated", "Social media followers are always more engaged than email subscribers"], "correct_index": 1, "explanation": "Email lists are owned directly by the business, making them independent of platform algorithm or policy changes."},
                {"question": "What is a lead magnet?", "options": ["A paid advertisement", "Something valuable offered for free in exchange for an email address", "A type of email spam filter", "A social media follower count"], "correct_index": 1, "explanation": "A lead magnet is the incentive used to encourage someone to voluntarily join an email list."},
                {"question": "Why does the worked example recommend delaying the paid offer to the third welcome email rather than the first?", "options": ["Delaying offers always reduces sales", "Building value and trust first tends to improve conversion compared to an immediate hard pitch", "The first email should never contain any useful content", "Email sequences must always contain exactly three emails by law"], "correct_index": 1, "explanation": "A gradual sequence that builds trust before pitching tends to outperform an immediate sales pitch."}
            ],
            "resources": [
                {"label": "HubSpot Marketing", "url": "https://www.hubspot.com/marketing"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Content, SEO, and Email",
            "title": "Introduction to Paid Advertising — How Ad Auctions Work",
            "learning_objective": "By the end of this class, you will be able to explain how digital ad auctions determine which ads are shown and at what cost.",
            "duration_minutes": 25,
            "content_html": "<p>Paid advertising can feel like a black box to beginners, but understanding the basic mechanics of how platforms decide which ads to show removes much of the mystery and helps you avoid common early mistakes that waste budget.</p><h2>How the Auction Works</h2><p>Most digital ad platforms use an auction system where advertisers bid to have their ad shown to a specific audience, but the winner is not simply whoever bids the most money. Platforms also weigh ad relevance and expected engagement, since a highly relevant, engaging ad can win a placement over a higher bid with poor relevance, because the platform wants to show ads users actually respond well to. This is why a poorly targeted or poorly written ad often costs more per result than a well-targeted, well-written one, even at the same budget.</p><h2>Worked Example</h2><p>Two Nigerian businesses both bid to advertise to the same audience segment. Business A bids a higher amount but uses generic stock imagery and vague copy, resulting in low engagement. Business B bids slightly less but uses a specific, relevant image and sharp copy tailored to the audience's actual interest, resulting in strong engagement. Because platforms factor in relevance and engagement, not bid amount alone, Business B often ends up paying less per result while reaching more of the right people, which is exactly why the copywriting skills from Day 6 directly affect paid ad performance and cost, not just organic content.</p>",
            "key_concepts": ["Ad auction mechanics", "Bid amount", "Ad relevance and engagement", "Cost efficiency", "Copy quality affecting ad cost"],
            "practical_exercise": {
                "title": "Compare a Weak and Strong Ad",
                "instructions": "Write two versions of a short ad for your capstone brand: one deliberately generic and vague, and one specific and relevant using the copywriting structure from Day 6. Write two to three sentences predicting which would likely perform better in an auction system and why, referencing relevance and engagement."
            },
            "quiz": [
                {"question": "In a digital ad auction, does the highest bidder always win the ad placement?", "options": ["Yes, bid amount is the only factor", "No, platforms also weigh ad relevance and expected engagement alongside bid amount", "Auctions do not exist in digital advertising", "Only the lowest bidder ever wins"], "correct_index": 1, "explanation": "Ad platforms combine bid amount with relevance and engagement predictions to determine ad placement."},
                {"question": "Why might a well-targeted, well-written ad end up costing less per result than a poorly targeted one, even at a similar bid?", "options": ["Cost is unrelated to ad quality or targeting", "Higher relevance and engagement can lower the effective cost within the auction system", "Well-written ads are always more expensive", "Targeting has no effect on ad cost"], "correct_index": 1, "explanation": "Platforms tend to reward relevant, engaging ads with more efficient costs, since users respond to them better."},
                {"question": "Why does the copywriting skill from Day 6 matter directly for paid advertising performance?", "options": ["Copywriting only matters for organic, unpaid content", "Sharper, more relevant copy improves engagement, which can lower cost and improve results in the ad auction", "Ad platforms ignore ad text entirely", "Copy has no measurable effect on ad auctions"], "correct_index": 1, "explanation": "Since relevance and engagement affect auction outcomes, strong copywriting directly impacts paid ad efficiency."}
            ],
            "resources": [
                {"label": "Google Analytics", "url": "https://www.google.com/analytics"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Running Real Campaigns",
            "title": "Running Your First Facebook/Instagram Ad Campaign",
            "learning_objective": "By the end of this class, you will be able to structure a basic Meta ads campaign including objective, audience targeting, and budget.",
            "duration_minutes": 35,
            "content_html": "<p>Meta's advertising platform, covering both Facebook and Instagram, remains one of the most accessible and widely used paid channels for African small businesses because of its detailed targeting options and relatively low minimum spend requirements.</p><h2>Campaign Structure</h2><p>A Meta ads campaign starts with choosing an objective, such as traffic, engagement, or conversions, which tells the platform's algorithm what outcome to optimize delivery for, so choosing the wrong objective can waste budget on the wrong kind of result. Audience targeting lets you narrow reach by location, age, interests, and behaviors, directly informed by the persona work from Day 2. Budget can be set as a daily amount or a total lifetime amount for the campaign's duration, and a realistic starting test budget is usually small, run for several days, before scaling up what works.</p><h2>Worked Example</h2><p>A Nigerian handmade jewelry brand wanting actual sales should choose a conversions or traffic objective pointing to a product page or WhatsApp catalog, not an engagement objective optimized purely for likes and comments, which would technically succeed while generating very few actual purchases. Targeting should reflect the Day 2 persona directly: women aged twenty-two to thirty-five in major Nigerian cities interested in fashion and accessories. Starting with a small daily test budget across a few days lets the business see which specific ad creative and audience combination performs best before committing a larger budget to the winning version.</p>",
            "key_concepts": ["Campaign objective", "Audience targeting", "Daily vs lifetime budget", "Test-then-scale approach", "Objective-outcome mismatch"],
            "practical_exercise": {
                "title": "Structure a Sample Ad Campaign",
                "instructions": "For your capstone brand, define a Meta ads campaign structure: choose an appropriate objective and justify it, describe your audience targeting based on your Day 2 persona, and propose a small test budget and duration before scaling."
            },
            "quiz": [
                {"question": "Why does choosing the correct campaign objective matter?", "options": ["Objectives have no effect on how the algorithm delivers the ad", "The objective tells the platform what outcome to optimize delivery for, so a mismatched objective can waste budget", "All objectives produce identical results", "Objectives only affect the ad's visual design"], "correct_index": 1, "explanation": "The algorithm optimizes delivery toward the chosen objective, so selecting the wrong one can produce results that do not match business goals."},
                {"question": "Why might an engagement objective be a poor choice for a business wanting actual product sales?", "options": ["Engagement objectives always produce the most sales", "It can generate likes and comments without necessarily driving purchases", "Engagement objectives are banned for e-commerce businesses", "There is no difference between engagement and conversion objectives"], "correct_index": 1, "explanation": "An engagement objective optimizes for interactions, not necessarily for the specific action of purchasing."},
                {"question": "Why is starting with a small test budget before scaling recommended?", "options": ["It guarantees the campaign will fail", "It allows testing which creative and audience combination performs best before committing a larger budget", "Test budgets are required by law", "Larger budgets always perform better regardless of testing"], "correct_index": 1, "explanation": "Testing at a small scale reduces risk and identifies what works before larger amounts are committed."}
            ],
            "resources": []
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Running Real Campaigns",
            "title": "Google Ads Fundamentals — Search Campaigns",
            "learning_objective": "By the end of this class, you will be able to structure a basic Google Search ads campaign including keywords, ad copy, and match types.",
            "duration_minutes": 30,
            "content_html": "<p>Unlike social ads that interrupt someone scrolling, Google Search ads reach people at the exact moment they are actively searching for a solution, often producing higher purchase intent, which makes it a powerful complement to the social advertising covered yesterday.</p><h2>Search Campaign Basics</h2><p>A search campaign is built around the specific keywords from Day 8 that you want your ad to appear for, paired with ad copy using the hook, benefit, CTA structure from Day 6. Match types control how closely a search must match your keyword: broad match shows your ad for a wide range of related searches, phrase match requires the core phrase to appear, and exact match only shows for very close variations of the exact keyword, giving increasing control but decreasing reach as you move from broad to exact.</p><h2>Worked Example</h2><p>The phone repair business from Day 8 targeting cracked screen repair same day Abuja might use phrase match to ensure the ad shows for searches containing that core phrase in various orders and with extra words, such as same day cracked screen repair near me in Abuja, while avoiding showing for unrelated broad searches like phone repair jobs Abuja, which would waste budget on job seekers rather than customers. Pairing this tightly matched keyword with ad copy that directly restates the urgency and location increases the likelihood that someone clicking the ad is genuinely ready to buy.</p>",
            "key_concepts": ["Google Search ads", "Keyword-driven campaigns", "Match types", "Search intent alignment", "Budget waste from mismatched keywords"],
            "practical_exercise": {
                "title": "Draft a Search Ad",
                "instructions": "Using one keyword from your Day 8 research, write a Google Search-style ad including a headline, a short description using the hook, benefit, CTA structure, and specify which match type (broad, phrase, or exact) you would use and why."
            },
            "quiz": [
                {"question": "Why do Google Search ads often produce higher purchase intent than social media ads?", "options": ["Search ads are always cheaper", "Search ads reach people at the moment they are actively searching for a solution", "Search ads do not require any budget", "Social ads always outperform search ads"], "correct_index": 1, "explanation": "Search ads target active intent, reaching users already looking for a specific solution, unlike interruptive social feeds."},
                {"question": "What does exact match keyword targeting generally provide compared to broad match?", "options": ["Wider reach but less control", "More control over which searches trigger the ad, but generally narrower reach", "Identical reach and control to broad match", "No effect on which searches trigger the ad"], "correct_index": 1, "explanation": "Exact match narrows the ad's reach to closely related searches, trading some reach for greater relevance control."},
                {"question": "Why might broad match keyword targeting risk wasting budget for a specific local service business?", "options": ["Broad match never wastes budget", "It can show ads for loosely related searches that do not reflect genuine customer intent, such as job searches instead of service searches", "Broad match is not available on Google Ads", "Broad match only works for e-commerce businesses"], "correct_index": 1, "explanation": "Broad match casts a wider net that can include irrelevant searches, potentially wasting spend on non-customer intent."}
            ],
            "resources": [
                {"label": "Google Analytics", "url": "https://www.google.com/analytics"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Running Real Campaigns",
            "title": "Influencer and Affiliate Marketing in the Nigerian Market",
            "learning_objective": "By the end of this class, you will be able to evaluate an influencer partnership using engagement quality rather than follower count alone.",
            "duration_minutes": 25,
            "content_html": "<p>Influencer marketing is enormously popular across Nigerian and African social media, but many businesses waste money partnering with influencers based on follower count alone, missing that engagement quality and audience fit matter far more for actual sales results.</p><h2>Evaluating Influencer Fit</h2><p>Engagement rate, the percentage of followers who actually like, comment, or share a post, is generally a stronger signal of real influence than raw follower count, since an account with fake or inactive followers can have a large count but very low genuine engagement. Audience fit, whether the influencer's actual followers match your target persona, matters more than general fame. Micro-influencers, typically with smaller but highly engaged and niche-specific audiences, often deliver better return on investment for small business budgets than large celebrity influencers.</p><h2>Worked Example</h2><p>A Nigerian skincare brand deciding between a celebrity influencer with two million followers but a low engagement rate around half a percent, and a micro-influencer with twenty thousand highly engaged skincare-focused followers at an engagement rate above six percent, would likely see stronger results from the micro-influencer, both because the audience is more relevant and because the engagement suggests followers actually trust and act on the influencer's recommendations. An affiliate arrangement, paying the micro-influencer a commission per actual sale generated through a unique code, further aligns their incentive directly with real business results rather than just posting content regardless of outcome.</p>",
            "key_concepts": ["Engagement rate", "Audience fit", "Micro-influencers", "Affiliate commission structure", "Follower count vs real influence"],
            "practical_exercise": {
                "title": "Evaluate Two Fictional Influencer Options",
                "instructions": "Create two fictional influencer profiles relevant to your capstone brand, one with a large following and low engagement, one with a smaller but highly engaged, niche-relevant following. Write a short recommendation on which you would partner with and why, referencing engagement rate and audience fit specifically."
            },
            "quiz": [
                {"question": "Why can follower count alone be a misleading measure of an influencer's real value to a brand?", "options": ["Follower count is always accurate and sufficient on its own", "An account can have a large follower count but low genuine engagement, sometimes due to fake or inactive followers", "Engagement rate has no relationship to follower count", "Follower count is the only metric that matters"], "correct_index": 1, "explanation": "Large follower counts do not guarantee real engagement or influence, since some followers may be inactive or fake."},
                {"question": "What often makes micro-influencers a strong choice for small business budgets?", "options": ["They always have millions of followers", "They often have smaller but highly engaged, niche-specific audiences, delivering strong return on investment", "They never charge for partnerships", "They are legally required for small businesses"], "correct_index": 1, "explanation": "Micro-influencers frequently offer better engagement and relevance for a lower cost than large celebrity accounts."},
                {"question": "What does an affiliate commission structure align an influencer's incentive with?", "options": ["The number of followers they gain personally", "Actual sales generated through their unique code or link", "The number of posts they publish regardless of outcome", "Their personal social media growth only"], "correct_index": 1, "explanation": "Commission-based affiliate arrangements tie the influencer's earnings directly to real, measurable business outcomes."}
            ],
            "resources": []
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Running Real Campaigns",
            "title": "Analytics Fundamentals — Reading Google Analytics",
            "learning_objective": "By the end of this class, you will be able to identify and interpret four core Google Analytics metrics for a website's traffic.",
            "duration_minutes": 30,
            "content_html": "<p>Running campaigns without checking analytics is like driving with your eyes closed, you might be moving, but you have no idea whether you are heading in the right direction. Learning to read core analytics metrics is what lets you make informed decisions instead of guessing.</p><h2>Core Metrics to Know</h2><p>Traffic sources show where visitors came from, such as organic search, paid ads, or social media, which tells you which channels are actually driving people to the site. Bounce rate, the percentage of visitors who leave after viewing only one page, can indicate a mismatch between what an ad or search result promised and what the page actually delivers. Conversion rate measures what percentage of visitors complete a desired action, such as a purchase or signup. Average session duration and pages per session hint at how engaging or relevant the content actually is to visitors.</p><h2>Worked Example</h2><p>Reviewing analytics for a campus tutoring service website, a high bounce rate specifically on visitors arriving from a paid ad, but a low bounce rate from organic search visitors, suggests the ad's promise, perhaps a specific discount mentioned in ad copy, is not clearly reflected or honored on the landing page itself, causing disappointed visitors to leave immediately. This single insight, comparing bounce rate by traffic source rather than looking at an overall average, points to a very specific, fixable problem: aligning the ad copy and landing page content, rather than a vague conclusion that the website needs a general redesign.</p>",
            "key_concepts": ["Traffic sources", "Bounce rate", "Conversion rate", "Session duration", "Segmenting metrics by source"],
            "practical_exercise": {
                "title": "Interpret a Sample Analytics Scenario",
                "instructions": "Write a short fictional analytics scenario for your capstone brand's website (traffic source breakdown, bounce rate by source, and conversion rate). Identify one specific insight from your fictional numbers and one concrete action you would take in response."
            },
            "quiz": [
                {"question": "What does bounce rate measure?", "options": ["The total number of website visitors", "The percentage of visitors who leave after viewing only one page", "The amount of money spent on ads", "The number of social media followers"], "correct_index": 1, "explanation": "Bounce rate specifically tracks single-page visits where the user leaves without further interaction."},
                {"question": "Why is it more useful to compare bounce rate by traffic source rather than only looking at an overall average?", "options": ["Segmenting by source has no additional value", "It can reveal specific, fixable problems, such as a mismatch between a particular ad's promise and the landing page", "Overall averages are always more accurate", "Traffic source has no relationship to bounce rate"], "correct_index": 1, "explanation": "Breaking metrics down by source can surface specific issues that an aggregate number would hide."},
                {"question": "What does conversion rate measure?", "options": ["The number of pages on a website", "The percentage of visitors who complete a desired action, such as a purchase or signup", "The total ad spend for a campaign", "The speed at which a website loads"], "correct_index": 1, "explanation": "Conversion rate tracks how effectively traffic is turned into the desired outcome, such as a sale or signup."}
            ],
            "resources": [
                {"label": "Google Analytics", "url": "https://www.google.com/analytics"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Running Real Campaigns",
            "title": "Setting KPIs and Measuring Campaign ROI",
            "learning_objective": "By the end of this class, you will be able to define specific, measurable KPIs for a marketing campaign and calculate its return on investment.",
            "duration_minutes": 30,
            "content_html": "<p>A campaign without clearly defined KPIs, key performance indicators, has no way of being judged a success or failure except by gut feeling, which is exactly the kind of vague reasoning that loses a marketer credibility and future budget with a client or employer.</p><h2>Defining and Measuring KPIs</h2><p>A good KPI is specific and directly tied to the campaign's actual goal, such as generate two hundred qualified leads within thirty days at a cost under one thousand naira per lead, rather than a vague goal like increase brand awareness with no measurable target attached. Return on investment, or ROI, is calculated by comparing the total revenue or value generated against the total cost, expressed as a percentage, giving a clear answer to whether a campaign was worth the spend.</p><h2>Worked Example</h2><p>A campaign for an online course spends two hundred thousand naira in ads and generates fifty course sales at fifteen thousand naira each, a total of seven hundred fifty thousand naira in revenue. The ROI calculation is revenue minus cost, divided by cost, multiplied by one hundred, giving roughly a two hundred seventy-five percent return. Reporting this exact number to a client, rather than saying the campaign went well, immediately establishes you as someone who thinks in the same financial terms the business owner does, tying directly back to the revenue-focused mindset introduced on Day 1.</p>",
            "key_concepts": ["Key performance indicators", "Specific measurable goals", "ROI calculation", "Revenue vs cost comparison", "Client-facing reporting"],
            "practical_exercise": {
                "title": "Define KPIs and Calculate ROI",
                "instructions": "For your capstone brand, write two specific, measurable KPIs for a hypothetical campaign (including a number and timeframe). Then create a simple fictional scenario with an ad spend and resulting revenue, and calculate the ROI using the formula revenue minus cost, divided by cost, multiplied by one hundred."
            },
            "quiz": [
                {"question": "Why is a goal like increase brand awareness considered weak compared to a specific KPI?", "options": ["It is too specific and measurable", "It has no measurable target, making it impossible to judge success or failure objectively", "Brand awareness should never be a marketing goal", "Specific KPIs are less professional than general goals"], "correct_index": 1, "explanation": "Without a measurable target, there is no clear way to determine whether the goal was actually achieved."},
                {"question": "What is the correct formula for calculating ROI as a percentage?", "options": ["Cost divided by revenue", "Revenue minus cost, divided by cost, multiplied by one hundred", "Revenue multiplied by cost", "Cost minus revenue, divided by revenue"], "correct_index": 1, "explanation": "ROI as a percentage is calculated as (revenue minus cost) divided by cost, then multiplied by 100."},
                {"question": "Why does reporting a specific ROI number build more credibility with a client than saying the campaign went well?", "options": ["Clients never care about specific numbers", "It demonstrates the marketer thinks in the same financial terms as the business owner", "Vague statements are always preferred in business", "ROI calculations are not relevant to client relationships"], "correct_index": 1, "explanation": "Concrete financial reporting shows the marketer understands and communicates in terms that matter directly to business decision-makers."}
            ],
            "resources": [
                {"label": "Google Analytics", "url": "https://www.google.com/analytics"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Optimization and Modern Channels",
            "title": "A/B Testing — Improving Campaigns with Data",
            "learning_objective": "By the end of this class, you will be able to design a valid A/B test comparing two versions of a marketing asset.",
            "duration_minutes": 25,
            "content_html": "<p>Guessing which headline, image, or offer will perform better wastes budget when the answer can simply be tested directly with real data. A/B testing removes opinion from the equation and lets actual audience behavior decide what works.</p><h2>Designing a Valid Test</h2><p>An A/B test compares two versions of a single element, such as an ad headline or a landing page button color, while keeping everything else identical, so that any difference in performance can be confidently attributed to that one changed element. Testing too many variables at once, changing the headline, image, and CTA simultaneously, makes it impossible to know which specific change caused a result. Tests also need enough traffic or time to reach a meaningful sample size before drawing conclusions, since a difference based on only a handful of clicks could easily be random chance.</p><h2>Worked Example</h2><p>Testing two versions of a landing page for a food delivery app, version A shows the price prominently at the top, while version B hides the price until further down the page, with every other element, image, headline, and button color, kept identical. After running both versions to a sufficient number of visitors, if version A shows a meaningfully higher conversion rate, the marketer can confidently conclude that showing the price upfront builds trust and reduces friction for this specific audience, a concrete, tested insight that directly improves future campaigns rather than a guess based on personal preference.</p>",
            "key_concepts": ["A/B testing", "Single-variable isolation", "Sample size significance", "Data-driven decisions", "Testing methodology discipline"],
            "practical_exercise": {
                "title": "Design an A/B Test",
                "instructions": "For your capstone brand, design an A/B test comparing two versions of one specific marketing element (such as a headline, image, or CTA button color), keeping all other elements identical. Describe what result would tell you which version to use going forward."
            },
            "quiz": [
                {"question": "Why is it a problem to change the headline, image, and CTA all at once in an A/B test?", "options": ["It is not a problem and is actually recommended", "It becomes impossible to know which specific change caused any difference in results", "Changing multiple elements always improves results", "A/B tests require changing every element simultaneously"], "correct_index": 1, "explanation": "Testing only one variable at a time isolates the cause of any performance difference."},
                {"question": "Why does an A/B test need a sufficient sample size before drawing conclusions?", "options": ["Sample size has no effect on test reliability", "A small number of results could reflect random chance rather than a real, meaningful difference", "Larger sample sizes always cost more money with no benefit", "Sample size is only relevant for paid advertising"], "correct_index": 1, "explanation": "Small samples are more susceptible to random variation, making conclusions unreliable without enough data."},
                {"question": "In the food delivery landing page example, what specific insight did the A/B test provide?", "options": ["That price should always be hidden on every landing page", "That showing the price upfront built trust and reduced friction for this specific audience", "That landing pages do not affect conversion rates", "That image quality was the most important factor"], "correct_index": 1, "explanation": "The test isolated the price placement variable, providing a concrete, tested insight about that specific audience's preference."}
            ],
            "resources": []
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Optimization and Modern Channels",
            "title": "Building a Content Calendar That Ships Consistently",
            "learning_objective": "By the end of this class, you will be able to build a two-week content calendar with a mix of content types across specified platforms.",
            "duration_minutes": 30,
            "content_html": "<p>Inconsistent posting is one of the most common reasons small business social pages fail to grow, not lack of creativity. A content calendar solves this by planning content in advance, so posting becomes a scheduled habit rather than a last-minute scramble that is easy to abandon.</p><h2>Building a Working Calendar</h2><p>A practical content calendar lists the date, platform, content type (educational, entertaining, or promotional, from Day 5), a brief description of the content, and the specific goal or funnel stage it targets. Planning at least one to two weeks ahead, rather than day by day, reduces the daily pressure to think of something and makes it easier to maintain the content balance discussed earlier this month rather than defaulting to promotional posts out of convenience.</p><h2>Worked Example</h2><p>A two-week calendar for a campus laundry service might alternate: Monday an educational post about stain removal on Instagram, Wednesday an entertaining exam-week meme on WhatsApp status, Friday a promotional weekend discount post on Instagram, repeating this pattern with fresh specific content the following week. Having this planned in advance means that even during a busy week, the business owner or marketer already knows exactly what to post and when, rather than skipping days entirely, which is one of the most common and avoidable failures in small business social media management.</p>",
            "key_concepts": ["Content calendar structure", "Advance planning", "Platform-specific scheduling", "Consistency habit", "Avoiding promotional default"],
            "practical_exercise": {
                "title": "Build a Two-Week Content Calendar",
                "instructions": "For your capstone brand, build a two-week content calendar including date, platform, content type, a brief description, and the funnel stage each post targets. Ensure the calendar reflects a healthy mix of educational, entertaining, and promotional content."
            },
            "quiz": [
                {"question": "What is a common reason small business social pages fail to grow, according to this lesson?", "options": ["Lack of creativity is always the main cause", "Inconsistent posting, not lack of creativity, is a frequent underlying cause", "Posting too consistently causes audience fatigue", "Content calendars actively hurt engagement"], "correct_index": 1, "explanation": "Irregular posting undermines audience growth and trust more often than a lack of creative ideas."},
                {"question": "Why is planning content one to two weeks in advance recommended over planning day by day?", "options": ["Advance planning has no real benefit", "It reduces daily pressure and helps maintain a healthy content mix rather than defaulting to convenience", "Day-by-day planning is always more effective", "Advance planning is required by social media platforms"], "correct_index": 1, "explanation": "Planning ahead removes the daily scramble that often leads to skipped posts or an over-reliance on quick promotional content."},
                {"question": "What should each entry in a content calendar ideally specify beyond just the date and platform?", "options": ["Only the exact posting time", "The content type and the funnel stage or goal it targets", "The competitor's posting schedule", "Nothing beyond the date is necessary"], "correct_index": 1, "explanation": "Including content type and funnel stage ensures the calendar maintains strategic balance, not just a random posting schedule."}
            ],
            "resources": []
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Optimization and Modern Channels",
            "title": "Video and Short-Form Content Strategy (TikTok/Reels)",
            "learning_objective": "By the end of this class, you will be able to outline a short-form video concept using a hook, value, and CTA structure.",
            "duration_minutes": 25,
            "content_html": "<p>Short-form video, on platforms like TikTok, Instagram Reels, and YouTube Shorts, currently drives some of the highest organic reach available to small businesses and creators across Africa, often outperforming static image posts by a wide margin without requiring any ad spend.</p><h2>Structuring Short-Form Video</h2><p>The first one to three seconds must hook attention immediately, often through a bold statement, a visual surprise, or a direct question, since viewers decide to keep watching or scroll away almost instantly. The middle of the video should deliver real value quickly and clearly, whether that is entertainment, education, or a relatable moment, avoiding slow, padded introductions. A clear, simple call to action at the end, such as follow for more tips like this or comment your city below, encourages the specific next action that supports your broader funnel goals from Day 3.</p><h2>Worked Example</h2><p>A short-form video for the campus tutoring service might open with the hook this one study method got me from a 45 to a 78 in one semester, immediately followed by a quick, specific explanation of the actual method in the middle, and close with the CTA comment study tips and I will send you my full note-taking template. This structure, hook, value, CTA, applied consistently, tends to significantly outperform a video that opens with a slow, generic introduction like hey guys, welcome back to my channel, which gives viewers an easy reason to scroll away before the actual content even begins.</p>",
            "key_concepts": ["Short-form video hook", "Fast value delivery", "Video CTA", "Organic reach potential", "Avoiding slow introductions"],
            "practical_exercise": {
                "title": "Outline a Short-Form Video Concept",
                "instructions": "For your capstone brand, outline a short-form video concept including the exact opening hook line, a brief description of the value delivered in the middle, and a specific closing call to action. Note which platform you would post it to and why."
            },
            "quiz": [
                {"question": "Why is the first one to three seconds of a short-form video considered so critical?", "options": ["Viewers decide almost instantly whether to keep watching or scroll away", "The opening seconds have no effect on video performance", "Platforms only track engagement after thirty seconds", "The hook is only important for paid video ads"], "correct_index": 1, "explanation": "Viewer attention is decided within the first few seconds, making the hook essential to retaining an audience."},
                {"question": "Why does a slow, generic introduction like hey guys, welcome back to my channel tend to hurt short-form video performance?", "options": ["It has no real effect on viewer behavior", "It delays value delivery and gives viewers an easy reason to scroll away before the content begins", "Generic introductions always improve retention", "Short-form platforms require a standard greeting"], "correct_index": 1, "explanation": "Delayed value in a fast-scrolling environment increases the chance viewers leave before the actual content starts."},
                {"question": "What is the purpose of a clear CTA at the end of a short-form video?", "options": ["To fill remaining time with no real purpose", "To encourage a specific next action that supports the broader marketing funnel goal", "CTAs are not recommended for short-form video", "To repeat the hook from the beginning"], "correct_index": 1, "explanation": "A clear closing CTA directs engaged viewers toward a specific next step aligned with the campaign's goals."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Optimization and Modern Channels",
            "title": "WhatsApp and Community-Led Marketing for African Markets",
            "learning_objective": "By the end of this class, you will be able to design a WhatsApp-based customer engagement or community strategy appropriate for a small business.",
            "duration_minutes": 25,
            "content_html": "<p>WhatsApp is one of the most heavily used communication platforms across Nigeria and much of Africa, and for many small businesses it functions as a primary sales and customer service channel, not just a casual messaging app, making it a marketing channel that cannot be ignored in this market.</p><h2>WhatsApp as a Marketing Channel</h2><p>WhatsApp Business accounts allow a catalog feature to showcase products directly in the app, automated quick replies for common questions, and broadcast lists to share updates with customers who have opted in, without the group-chat clutter of a regular group. Community-led marketing, building an engaged group of customers who feel personally connected to a brand, often through a WhatsApp community or group offering exclusive updates or early access, can drive strong loyalty and word-of-mouth referrals in markets where trust and personal relationships heavily influence buying decisions.</p><h2>Worked Example</h2><p>A small Nigerian fashion brand might set up a WhatsApp Business catalog showing current stock with prices, use quick reply automation to instantly answer common questions like available sizes, and maintain a broadcast list for weekly new-arrival updates sent only to customers who have explicitly opted in, respecting their attention rather than spamming. Additionally, creating an exclusive WhatsApp community for repeat customers, offering early access to new drops before the general public, builds the kind of loyalty and personal connection that is difficult to replicate through impersonal social media ads alone.</p>",
            "key_concepts": ["WhatsApp Business features", "Catalog and quick replies", "Broadcast lists vs groups", "Community-led marketing", "Trust-driven local markets"],
            "practical_exercise": {
                "title": "Design a WhatsApp Marketing Strategy",
                "instructions": "For your capstone brand, describe how you would set up a WhatsApp Business presence, including at least one specific use of the catalog feature, one automated quick reply example, and one idea for an exclusive community or broadcast list offering to build customer loyalty."
            },
            "quiz": [
                {"question": "Why is WhatsApp considered an especially important marketing channel in Nigeria and much of Africa?", "options": ["It is rarely used compared to other platforms", "It functions as a primary sales and customer service channel for many small businesses in this market", "It cannot be used for business purposes", "It has no relevant business features"], "correct_index": 1, "explanation": "WhatsApp's heavy daily use across the region makes it a core, not secondary, business communication and sales channel."},
                {"question": "What is the advantage of a broadcast list over a regular group for sending updates to customers?", "options": ["Broadcast lists have no real advantage", "Broadcast lists avoid group-chat clutter while still reaching opted-in customers with updates", "Groups are always more effective for updates", "Broadcast lists cannot include product information"], "correct_index": 1, "explanation": "Broadcast lists deliver updates directly without the noise and clutter of a shared group conversation."},
                {"question": "Why can community-led marketing be especially effective in markets where trust and personal relationships heavily influence buying decisions?", "options": ["Community-led marketing has no effect on trust", "It builds personal connection and loyalty that is difficult to replicate through impersonal ads alone", "Community-led marketing replaces the need for any product quality", "It only works for large multinational brands"], "correct_index": 1, "explanation": "Personal, community-based engagement builds the kind of trust and loyalty that strongly influences buying behavior in trust-driven markets."}
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Optimization and Modern Channels",
            "title": "Marketing Automation and CRM Basics",
            "learning_objective": "By the end of this class, you will be able to design a simple automated follow-up sequence triggered by a specific customer action.",
            "duration_minutes": 25,
            "content_html": "<p>As a business grows beyond a handful of customers, manually following up with every lead individually becomes impossible. Marketing automation and customer relationship management, or CRM, tools let a small team run consistent, personalized follow-up at scale without hiring a large staff.</p><h2>Automation and CRM Fundamentals</h2><p>A CRM system tracks every customer or lead's information and interaction history in one place, so a business can see exactly where each person is in the buying journey rather than relying on memory or scattered notes. Marketing automation triggers specific actions, such as sending a follow-up email or WhatsApp message, automatically based on a customer's behavior, such as abandoning a cart without completing a purchase, rather than requiring a person to manually notice and respond to every single case.</p><h2>Worked Example</h2><p>An online store using a simple CRM might automatically tag a customer as abandoned cart if they added an item but did not complete checkout within an hour, triggering an automated WhatsApp message an hour later offering help or a small incentive to complete the purchase, without any staff member needing to notice and act manually. This single automation, built once, can recover a meaningful percentage of otherwise lost sales continuously, month after month, a far more scalable approach than a small team trying to manually track and follow up with every visitor who did not complete a purchase.</p>",
            "key_concepts": ["CRM systems", "Marketing automation", "Behavior-triggered messaging", "Abandoned cart recovery", "Scaling personalized follow-up"],
            "practical_exercise": {
                "title": "Design an Automated Follow-Up Sequence",
                "instructions": "For your capstone brand, design one automated follow-up sequence triggered by a specific customer behavior (such as an abandoned cart, an inactive subscriber, or a first-time purchase). Describe the trigger, the timing, and the exact message content."
            },
            "quiz": [
                {"question": "What is the main function of a CRM system?", "options": ["To design social media graphics", "To track customer or lead information and interaction history in one place", "To run paid ad auctions", "To write blog content automatically"], "correct_index": 1, "explanation": "A CRM centralizes customer and lead data so a business can track and manage relationships systematically."},
                {"question": "What triggers a marketing automation sequence, such as an abandoned cart follow-up?", "options": ["A random schedule with no connection to customer behavior", "A specific customer action or behavior, such as not completing checkout", "Manual review by a staff member every single time", "It requires no trigger at all"], "correct_index": 1, "explanation": "Automation is triggered by defined customer behaviors, allowing consistent response without manual monitoring."},
                {"question": "Why is automated follow-up considered more scalable than manual follow-up as a business grows?", "options": ["Automation cannot scale beyond a few customers", "A single automation, once built, can consistently respond to many customers without requiring additional staff time per case", "Manual follow-up is always more effective at any scale", "Scalability has nothing to do with automation"], "correct_index": 1, "explanation": "Automated systems handle growing volume without proportionally increasing staff workload, unlike manual follow-up."}
            ],
            "resources": [
                {"label": "HubSpot Marketing", "url": "https://www.hubspot.com/marketing"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Strategic Campaign Planning",
            "title": "Budget Allocation — Spreading Spend Across Channels",
            "learning_objective": "By the end of this class, you will be able to allocate a fictional marketing budget across multiple channels with clear reasoning for each split.",
            "duration_minutes": 30,
            "content_html": "<p>A common beginner mistake is putting an entire budget into a single channel because it feels trendy, without considering where the specific target audience actually spends time or which channels match the campaign's funnel goals. Thoughtful budget allocation is one of the clearest signals of strategic maturity in a campaign plan.</p><h2>How to Think About Allocation</h2><p>Start by weighing each channel against your persona from Day 2, your funnel goals from Day 3, and past performance data if available, rather than splitting the budget evenly by default, which rarely reflects where the real opportunity lies. It is common and often wise to allocate a larger share to a small number of test channels first, then shift more budget toward whichever channel proves the strongest actual return, rather than spreading a small budget too thinly across many channels where no single effort gets enough spend to produce meaningful results.</p><h2>Worked Example</h2><p>For a monthly budget of one hundred thousand naira for the campus food delivery brand, a reasoned allocation might put fifty percent into Instagram and WhatsApp-focused paid promotion, since that is where the campus persona spends most of their time, thirty percent into a micro-influencer partnership with a relevant campus content creator, and the remaining twenty percent held back as a flexible testing budget to try Google Search ads targeting delivery-related searches. This reasoning, grounded specifically in persona and funnel logic rather than an even split or personal preference, is exactly what a client or employer wants to see justified in a campaign plan.</p>",
            "key_concepts": ["Budget allocation logic", "Persona-driven channel weighting", "Test-and-scale budgeting", "Avoiding thin spread across channels", "Reasoned allocation vs even split"],
            "practical_exercise": {
                "title": "Allocate a Fictional Budget",
                "instructions": "For your capstone brand, allocate a fictional monthly marketing budget of your choosing across at least three channels, specifying the percentage for each. Write one to two sentences of reasoning for each allocation, referencing your persona and funnel goals from earlier in this course."
            },
            "quiz": [
                {"question": "Why is splitting a budget evenly across many channels by default often a weak strategy?", "options": ["Even splitting always produces the best results", "It rarely reflects where the real audience and opportunity actually lies, and can spread spend too thin to be effective anywhere", "Budgets should never be split across more than one channel", "Even splitting is required by most ad platforms"], "correct_index": 1, "explanation": "An even split ignores where the specific audience and opportunity actually exist, often diluting impact across every channel."},
                {"question": "What should guide channel budget allocation according to this lesson?", "options": ["Whichever channel feels trendiest regardless of audience fit", "The target persona, funnel goals, and available performance data", "A completely random distribution", "Only the marketer's personal preference"], "correct_index": 1, "explanation": "Allocation should be grounded in evidence about where the specific target audience is and what the campaign is trying to achieve."},
                {"question": "Why might a marketer hold back a portion of the budget specifically for testing a new channel?", "options": ["Testing budgets are unnecessary and wasteful", "It allows discovering whether an additional channel could be effective before committing a larger amount", "All budget should always go to the largest channel only", "Testing is only relevant for very large companies"], "correct_index": 1, "explanation": "A dedicated testing budget allows evaluating new channels with controlled risk before scaling investment."}
            ],
            "resources": []
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Strategic Campaign Planning",
            "title": "Brand Positioning and Competitive Analysis",
            "learning_objective": "By the end of this class, you will be able to write a one-sentence brand positioning statement based on a competitive analysis.",
            "duration_minutes": 25,
            "content_html": "<p>A brand that tries to appeal to everyone with the same generic message struggles to stand out in a crowded market. Positioning is the deliberate choice of what makes a brand different and specifically why the right customer should choose it over alternatives.</p><h2>Positioning Through Competitive Analysis</h2><p>A competitive analysis looks at what direct competitors are already offering, how they market themselves, and where gaps or weaknesses exist that your brand could occupy instead. A strong positioning statement typically follows a structure like: for target customer who has this specific need, brand name is the option that delivers this specific benefit, unlike competitor approach which falls short in this specific way.</p><h2>Worked Example</h2><p>Reviewing three existing campus food delivery competitors, you might notice they all emphasize speed but none clearly emphasize affordability for budget-conscious students, or none clearly communicate trustworthy, hygienic food handling, both real potential gaps. A resulting positioning statement might say for university students who want affordable meals delivered without breaking their monthly budget, this brand is the delivery service that guarantees a meal under a specific price point every day, unlike competitors who focus only on speed regardless of cost. This clear, specific positioning then directly shapes the messaging in every piece of content and ad copy created for the rest of the campaign.</p>",
            "key_concepts": ["Brand positioning", "Competitive analysis", "Positioning statement structure", "Differentiation gaps", "Positioning-to-messaging consistency"],
            "practical_exercise": {
                "title": "Write a Positioning Statement",
                "instructions": "Identify two to three real or realistic competitors for your capstone brand. Note one strength and one gap or weakness for each. Write a one-sentence positioning statement for your brand using the structure: for target customer with this need, brand is the option that delivers this benefit, unlike competitors who fall short in this way."
            },
            "quiz": [
                {"question": "Why does a brand trying to appeal to everyone with a generic message often struggle to stand out?", "options": ["Generic messaging always performs best in crowded markets", "Without a specific, differentiated position, the brand blends in rather than standing out to a specific audience", "Standing out is not important for a brand's success", "Competitive analysis has no relationship to positioning"], "correct_index": 1, "explanation": "A brand without clear differentiation fails to give a specific reason for a specific customer to choose it over alternatives."},
                {"question": "What is the purpose of a competitive analysis in developing brand positioning?", "options": ["To copy competitors exactly", "To identify gaps or weaknesses in competitor offerings that the brand could occupy instead", "Competitive analysis has no connection to positioning", "To determine the competitor's internal costs"], "correct_index": 1, "explanation": "Analyzing competitors reveals opportunities for differentiation that a brand's positioning can then claim."},
                {"question": "In the worked example, what specific gap did the campus food delivery brand identify among its competitors?", "options": ["Competitors were too affordable already", "Competitors emphasized speed but not affordability or clear hygienic food handling", "There were no gaps to identify", "Competitors did not deliver food at all"], "correct_index": 1, "explanation": "The analysis found that affordability and hygiene were underemphasized by competitors, revealing a specific positioning opportunity."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Strategic Campaign Planning",
            "title": "Crisis Management and Reputation Monitoring",
            "learning_objective": "By the end of this class, you will be able to outline a basic response plan for a negative social media comment or public complaint.",
            "duration_minutes": 25,
            "content_html": "<p>Every brand active online eventually faces a negative comment, complaint, or small controversy, and how it responds publicly often matters more to onlookers than the original complaint itself. A calm, prepared response plan prevents a manageable situation from becoming a much bigger problem.</p><h2>Responding Well Under Pressure</h2><p>The first step is acknowledging the concern publicly and quickly, without being defensive, since silence or a slow response is often read as indifference or guilt, even when neither is true. Serious complaints, especially ones involving specific personal details or strong emotion, should be moved to a private channel such as direct message or email to resolve properly, while still leaving a brief, calm public acknowledgment that the issue is being handled. Monitoring mentions and comments regularly, rather than only reacting when something already escalates, allows a business to catch and address small issues before they grow.</p><h2>Worked Example</h2><p>If a customer publicly comments that their food delivery order arrived cold and unacceptable, a weak brand response ignores the comment or replies defensively saying that never happens. A strong response replies quickly and publicly with something like we are really sorry to hear this, please send us a direct message with your order number so we can make this right immediately, then follows through promptly in private. This public acknowledgment shows every other viewer, not just the complaining customer, that the brand takes problems seriously and responds professionally, which often builds more trust among onlookers than if no complaint had ever appeared at all.</p>",
            "key_concepts": ["Crisis response plan", "Public acknowledgment vs private resolution", "Reputation monitoring", "Avoiding defensiveness", "Trust-building through response quality"],
            "practical_exercise": {
                "title": "Draft a Crisis Response Plan",
                "instructions": "Write a fictional negative public comment your capstone brand might receive. Draft a public response following the acknowledge-and-move-to-private-channel approach, and write two to three sentences describing how you would monitor for and catch such issues early in the future."
            },
            "quiz": [
                {"question": "Why is silence or a slow response to a public complaint often risky for a brand?", "options": ["Silence always shows strength and confidence", "Slow or absent responses are often read as indifference or guilt by onlookers, even if that is not the case", "Silence has no effect on public perception", "Public complaints should always be ignored"], "correct_index": 1, "explanation": "Onlookers often interpret silence negatively, regardless of the brand's actual intentions."},
                {"question": "Why should a serious complaint be moved to a private channel rather than resolved entirely in public comments?", "options": ["Private resolution allows proper, detailed handling while still leaving a brief public acknowledgment", "Complaints should never be acknowledged publicly at all", "Public channels are always the best place to resolve complaints fully", "Moving to private always looks like avoidance"], "correct_index": 0, "explanation": "A brief public acknowledgment shows responsiveness, while detailed resolution is better handled privately for practicality and discretion."},
                {"question": "Why might a well-handled public complaint actually build more trust among onlookers than if no complaint had appeared?", "options": ["Complaints always damage a brand's reputation regardless of response", "A calm, professional response demonstrates the brand takes problems seriously and handles them well", "Onlookers never notice how complaints are handled", "Trust is unrelated to how complaints are managed"], "correct_index": 1, "explanation": "A well-managed response can demonstrate professionalism and care in a way that builds credibility with a wider audience."}
            ],
            "resources": []
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Strategic Campaign Planning",
            "title": "Growth Hacking Tactics for Startups on a Budget",
            "learning_objective": "By the end of this class, you will be able to design a low-cost growth tactic that leverages existing users or partnerships instead of paid ads.",
            "duration_minutes": 25,
            "content_html": "<p>Not every business, especially an early-stage startup or campus venture, has a large ad budget, which is exactly why growth hacking, finding creative, low-cost ways to grow using existing resources and clever mechanics, is such a valuable skill in resource-constrained markets like much of Africa.</p><h2>Low-Cost Growth Levers</h2><p>Referral programs turn existing customers into a growth channel by rewarding them for bringing in new customers, effectively converting satisfied users into an unpaid sales force. Strategic partnerships with complementary, non-competing businesses that share a similar audience can expose a brand to a new pool of potential customers at little or no cost. Product-led mechanics, features built into the product itself that naturally encourage sharing, such as a visible watermark or a shareable result, can drive organic growth simply through normal product use.</p><h2>Worked Example</h2><p>A campus tutoring startup with no ad budget might launch a referral program offering an existing student a free session for every friend they refer who signs up for a paid session, turning happy students into active recruiters at essentially zero marketing cost beyond the discount given. Simultaneously, partnering with a campus stationery shop to offer a joint discount, students who buy from the stationery shop get a coupon for the tutoring service and vice versa, taps into an already-engaged, relevant campus audience without spending on ads at all, exactly the kind of resourceful thinking that impresses early-stage employers and clients working with limited budgets.</p>",
            "key_concepts": ["Growth hacking", "Referral programs", "Strategic partnerships", "Product-led growth mechanics", "Low-budget resourcefulness"],
            "practical_exercise": {
                "title": "Design a Low-Cost Growth Tactic",
                "instructions": "For your capstone brand, design one specific low-cost growth tactic (a referral program, a strategic partnership, or a product-led sharing mechanic). Describe exactly how it would work and why it would appeal to your existing persona from Day 2."
            },
            "quiz": [
                {"question": "What is the core idea behind a referral program as a growth tactic?", "options": ["Paying for expensive traditional advertising", "Rewarding existing customers for bringing in new customers, turning them into an unpaid sales force", "Ignoring existing customers entirely", "Only targeting brand new audiences with paid ads"], "correct_index": 1, "explanation": "Referral programs leverage satisfied existing customers to organically drive new customer acquisition."},
                {"question": "Why might a strategic partnership with a complementary, non-competing business be a valuable low-cost growth tactic?", "options": ["Partnerships always require large budgets to be effective", "It can expose a brand to a new, relevant pool of potential customers at little or no cost", "Partnerships only work for large corporations", "Non-competing businesses never share relevant audiences"], "correct_index": 1, "explanation": "A well-matched partnership can access an already-relevant audience without significant marketing spend."},
                {"question": "Why is growth hacking particularly valuable for early-stage startups in resource-constrained markets?", "options": ["Growth hacking requires large advertising budgets to work", "It focuses on creative, low-cost ways to grow using existing resources rather than expensive paid channels", "It is only relevant for large, well-funded companies", "It has no practical application for startups"], "correct_index": 1, "explanation": "Growth hacking prioritizes resourceful, low-cost tactics, which is especially valuable for budget-constrained early-stage ventures."}
            ],
            "resources": []
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Strategic Campaign Planning",
            "title": "Building a Full Funnel Campaign End to End",
            "learning_objective": "By the end of this class, you will be able to map one complete, connected campaign covering all four funnel stages for a single audience segment.",
            "duration_minutes": 35,
            "content_html": "<p>Individually strong tactics, a good ad here, a good email there, still fail to compound if they are not connected into one deliberate journey. Today you practice tying every skill from this month into a single, coherent full-funnel campaign, exactly the kind of thinking your final capstone project requires.</p><h2>Connecting the Full Journey</h2><p>A full-funnel campaign deliberately designs how a person moves from first hearing about the brand, through consideration and purchase, to becoming a retained, referring customer, ensuring each stage smoothly leads into the next with consistent messaging and appropriate channels for each. This means an awareness-stage social ad should logically lead toward a consideration-stage piece of content or email opt-in, not directly demand an immediate purchase, which mismatches intent as covered back on Day 3.</p><h2>Worked Example</h2><p>For the campus food delivery brand, a full-funnel campaign might start with an awareness-stage Reel showing relatable exam-week chaos, leading interested viewers to follow the account or join a WhatsApp broadcast list for a first-order discount, which serves as the consideration-stage nudge. Those who join the WhatsApp list receive a consideration-stage message with a limited first-order discount code as the conversion-stage push. After their first order, an automated retention message from Day 20 thanks them and offers a referral bonus for inviting a friend, completing the loop back into new awareness through word of mouth. This single connected sequence, not four disconnected tactics, is what a genuinely strategic campaign looks like.</p>",
            "key_concepts": ["Full-funnel campaign design", "Stage-to-stage transition", "Consistent cross-channel messaging", "Connected customer journey", "Strategic integration of tactics"],
            "practical_exercise": {
                "title": "Map a Full-Funnel Campaign",
                "instructions": "For your capstone brand, map one complete full-funnel campaign, describing a specific tactic or piece of content for each of the four funnel stages (awareness, consideration, conversion, retention) and explicitly explaining how each stage leads into the next."
            },
            "quiz": [
                {"question": "Why can individually strong marketing tactics still fail to produce strong overall results?", "options": ["Individual tactics always guarantee overall success regardless of connection", "If they are not connected into one deliberate journey, they do not compound or guide a customer smoothly through the funnel", "Strong tactics never need to be connected to anything else", "Full-funnel thinking has no real advantage over isolated tactics"], "correct_index": 1, "explanation": "Disconnected tactics miss the opportunity to guide a customer smoothly and consistently from first contact to loyal customer."},
                {"question": "Why is it a mismatch for an awareness-stage ad to directly demand an immediate purchase?", "options": ["Awareness-stage viewers already know and trust the brand deeply", "The audience at this stage typically does not yet know or trust the brand enough to respond to a direct purchase ask", "Purchase requests are appropriate at every funnel stage equally", "Awareness ads should never mention the product"], "correct_index": 1, "explanation": "A direct purchase ask mismatches the trust level typical of someone just discovering the brand for the first time."},
                {"question": "What made the campus food delivery example a genuine full-funnel campaign rather than four disconnected tactics?", "options": ["Each stage was designed in isolation with no relationship to the others", "Each stage deliberately led into the next, forming one connected customer journey from awareness to retention and back to referral", "Only the promotional stage was actually planned", "The campaign used only one single channel throughout"], "correct_index": 1, "explanation": "The stages were explicitly linked, forming a deliberate, connected journey rather than isolated efforts."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Digital Marketing Career Paths and What Employers Screen For",
            "learning_objective": "By the end of this class, you will be able to identify at least three digital marketing career paths and the specific skills each one requires.",
            "duration_minutes": 25,
            "content_html": "<p>Digital marketing spans several distinct specializations, and knowing which direction fits your strengths helps you focus your job search and frame your capstone project for the right audience, whether that is a specific employer type or freelance clients.</p><h2>Common Career Paths</h2><p>A social media manager focuses on content strategy, community engagement, and platform-specific execution, closely matching weeks one and four of this course. A performance or paid media marketer focuses on running and optimizing paid campaigns across platforms like Meta and Google, closely matching weeks two and three. A content or SEO marketer focuses on organic content, blogging, and search strategy, matching Days 5 through 8. A growth marketer takes a broader, more analytical view across the full funnel and multiple channels, closely matching the strategic thinking from week five.</p><h2>Worked Example</h2><p>A junior social media manager job posting at a Nigerian consumer brand might emphasize content calendars, community engagement, and platform trends, directly matching your Day 5 and Day 17 work. A junior performance marketing role at a startup might emphasize Meta and Google Ads experience and comfort reading analytics, directly matching Days 11, 12, and 14. Recognizing which of these roles excites you most, based on which weeks of this course you found most engaging, should directly shape how you position your capstone project and CV toward that specific type of role.</p>",
            "key_concepts": ["Social media manager role", "Performance marketer role", "Content and SEO marketer role", "Growth marketer role", "Portfolio-role alignment"],
            "practical_exercise": {
                "title": "Match Your Skills to a Marketing Career Path",
                "instructions": "Find two real entry-level digital marketing job postings, from Nigeria or internationally, for two different roles (for example social media manager and performance marketer). For each posting, list which specific days or exercises from this course directly demonstrate a skill they are asking for."
            },
            "quiz": [
                {"question": "Which career path most closely focuses on running and optimizing paid campaigns across platforms like Meta and Google?", "options": ["Content or SEO marketer", "Performance or paid media marketer", "Community manager only", "Graphic designer"], "correct_index": 1, "explanation": "Performance marketing roles center specifically on paid campaign execution and optimization."},
                {"question": "Which career path most closely aligns with the organic content and search strategy work from Days 5 through 8?", "options": ["Content or SEO marketer", "Performance or paid media marketer only", "Sales representative", "Financial analyst"], "correct_index": 0, "explanation": "Content and SEO marketing roles focus on organic content creation and search visibility, matching those specific days."},
                {"question": "Why is it useful to identify which specific days of this course you found most engaging?", "options": ["It has no bearing on career direction", "It helps identify which marketing career path and role type best matches your interests and strengths", "Engagement with course content is unrelated to real job performance", "Only the final capstone matters for career direction"], "correct_index": 1, "explanation": "Reflecting on which areas were most engaging helps focus career direction and portfolio positioning toward a matching role."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Common Marketing Interview Questions and How to Answer",
            "learning_objective": "By the end of this class, you will be able to confidently answer three common digital marketing interview questions using examples from your own coursework.",
            "duration_minutes": 25,
            "content_html": "<p>Marketing interviews frequently test whether a candidate can reason through real scenarios and back up claims with data or specific examples, not just recite definitions. Preparing structured, evidence-based answers using your own work from this course gives you a real edge over candidates who can only speak in generalities.</p><h2>Sample Question Patterns</h2><p>How would you approach marketing a product with a very limited budget is a resourcefulness question, best answered by referencing your Day 24 growth hacking thinking. Walk me through how you would measure the success of a campaign tests analytical thinking, directly answerable using your Day 15 KPI and ROI framework. Tell me about a time you had to adjust a strategy based on data invites you to describe your Day 16 A/B testing or Day 18 iteration mindset, even if drawn from coursework rather than a paid job.</p><h2>Worked Example</h2><p>A weak answer to how would you measure campaign success says I would look at the numbers and see how it did. A strong answer says I would define specific KPIs before the campaign starts, such as cost per lead and conversion rate, track them using analytics throughout the campaign, and calculate ROI at the end to determine whether the spend was justified, directly referencing your Day 14 and Day 15 work. This structured, specific answer, grounded in a real framework you have actually practiced, is what separates a credible junior candidate from someone speaking only in vague marketing buzzwords.</p>",
            "key_concepts": ["Resourcefulness interview questions", "Analytical measurement questions", "Data-driven adjustment stories", "Structured evidence-based answers", "Coursework as interview evidence"],
            "practical_exercise": {
                "title": "Write Out Three Interview Answers",
                "instructions": "Write full, spoken-style answers to these three questions, each three to five sentences, referencing specific days or exercises from your own work in this course: how would you market a product with a very limited budget, how would you measure the success of a campaign, and tell me about a time you adjusted a strategy based on data."
            },
            "quiz": [
                {"question": "Why is I would look at the numbers and see how it did considered a weak interview answer?", "options": ["It is too specific and detailed", "It lacks a specific framework, such as defined KPIs and an ROI calculation, showing structured thinking", "Vague answers are generally preferred in interviews", "This answer demonstrates strong analytical thinking"], "correct_index": 1, "explanation": "The answer lacks the specificity and structure that demonstrates real analytical capability."},
                {"question": "Which day's framework would be most directly useful for answering how would you measure campaign success?", "options": ["Day 4, profile setup", "Day 15, KPIs and ROI", "Day 19, WhatsApp marketing", "Day 23, crisis management"], "correct_index": 1, "explanation": "The KPI and ROI framework from Day 15 directly addresses how to define and measure campaign success."},
                {"question": "Why is referencing your own coursework valuable in an interview, even without prior paid job experience?", "options": ["Coursework examples are never accepted in interviews", "It provides concrete, structured evidence of applied thinking rather than only vague general claims", "Interviewers only accept examples from paid employment", "Coursework has no relevance to real marketing interviews"], "correct_index": 1, "explanation": "Specific, applied examples from real coursework demonstrate practical thinking even without formal job experience."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Freelance and Agency Marketing — Landing Your First Clients",
            "learning_objective": "By the end of this class, you will be able to draft a specific freelance marketing service offer and identify three channels to find clients.",
            "duration_minutes": 25,
            "content_html": "<p>Freelance digital marketing is a highly accessible entry point for Nigerian students, since small businesses everywhere need marketing help but often cannot afford a full-time hire, creating real, immediate opportunity for someone who can demonstrate results, even at a small scale.</p><h2>Finding and Landing Clients</h2><p>A specific service offer, describing exactly what you deliver, for what type of business, and roughly what result they can expect, converts far better than a vague I do social media and marketing. Practical channels for finding first clients include direct outreach to small businesses with a visibly weak or inconsistent online presence, local business networking groups, and referrals from your own personal or family network, which is often the fastest way to land a genuine first client and build a track record.</p><h2>Worked Example</h2><p>Instead of a vague pitch, a strong freelance offer might say I help small Nigerian businesses build a consistent content calendar and grow their Instagram engagement within thirty days, starting with a free content audit so you can see exactly what I would improve. Offering a free, low-effort content audit as a first step, applying the audit skills practiced across weeks one, two, and four of this course, lowers the barrier for a hesitant small business owner to say yes, and a genuinely useful free audit often converts directly into a paid ongoing engagement once trust is established.</p>",
            "key_concepts": ["Freelance service offer", "Direct outreach to weak online presence", "Referral networks", "Free audit as entry offer", "Trust-to-paid conversion"],
            "practical_exercise": {
                "title": "Draft Your Freelance Marketing Offer",
                "instructions": "Write a specific, one-paragraph freelance marketing service offer describing exactly what you deliver, for what type of client, and the expected timeframe or result. List three real channels (direct outreach targets, networking groups, or referral sources) where you could find your first client."
            },
            "quiz": [
                {"question": "Why does a specific service offer convert better than a vague statement like I do social media and marketing?", "options": ["Specificity has no real effect on client interest", "A specific offer clearly communicates the exact value and outcome a potential client can expect", "Vague offers are always more professional", "Clients prefer offers with no clear details"], "correct_index": 1, "explanation": "Clarity about the exact service and expected outcome helps a potential client immediately see the value."},
                {"question": "Why is a free, low-effort audit often an effective first offer for landing freelance clients?", "options": ["Free offers never lead to paid work", "It lowers the barrier for a hesitant business owner to say yes and can build trust that converts into paid work", "Audits provide no real value to a business", "Clients never trust freelancers regardless of a free audit"], "correct_index": 1, "explanation": "A low-risk free offer reduces hesitation and demonstrates real value, often leading to a paid engagement once trust is built."},
                {"question": "Why are personal or family network referrals often described as the fastest way to land a first client?", "options": ["Referrals never lead to real client relationships", "Existing personal trust and connections lower the barrier to a first opportunity compared to cold outreach", "Referrals are illegal in freelance marketing", "Family networks have no real business value"], "correct_index": 1, "explanation": "Pre-existing trust in personal networks often accelerates the path to a first paying client compared to cold outreach."}
            ],
            "resources": [
                {"label": "LinkedIn for Business", "url": "https://business.linkedin.com"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Marketing Ethics, Data Privacy, and Consumer Trust",
            "learning_objective": "By the end of this class, you will be able to identify ethical concerns in a marketing scenario and propose a more responsible alternative approach.",
            "duration_minutes": 25,
            "content_html": "<p>Marketing skill can be used to genuinely help a business and its customers, or it can be used to manipulate and mislead, and the difference matters both ethically and practically, since misleading tactics tend to damage trust and long-term business results even when they produce short-term gains.</p><h2>Core Ethical Considerations</h2><p>Honest advertising means not exaggerating claims beyond what a product can actually deliver, and not using manipulative urgency, such as a fake countdown timer that resets, to pressure a purchase decision. Data privacy means only collecting customer information you genuinely need, being transparent about how it will be used, and never sharing or selling personal data without clear consent, which is both an ethical obligation and increasingly a legal requirement under data protection laws in Nigeria and other African countries. Respecting an audience's attention, not spamming, and honoring unsubscribe or opt-out requests promptly, builds the kind of long-term trust that repeat business depends on.</p><h2>Worked Example</h2><p>Imagine a weight-loss product ad claims users will lose fifteen kilograms in one week, an exaggerated, almost certainly false claim designed purely to grab attention. An ethical alternative makes an honest, still compelling claim grounded in real, typical results and clearly discloses that individual results vary, avoiding both legal risk and the reputational damage that comes when customers discover the original claim was never realistic. Choosing honesty over exaggeration is not just the right thing to do, it is also the more sustainable long-term business strategy, since a brand's reputation compounds over time in either direction.</p>",
            "key_concepts": ["Honest advertising", "Manipulative urgency tactics", "Data privacy and consent", "Opt-out and unsubscribe respect", "Long-term trust vs short-term gain"],
            "practical_exercise": {
                "title": "Identify and Fix an Ethical Issue",
                "instructions": "Write a short fictional marketing scenario involving an ethical concern (exaggerated claims, manipulative urgency, or misuse of customer data). Identify exactly what makes it unethical, then rewrite the scenario as a more honest, responsible alternative that could still be effective marketing."
            },
            "quiz": [
                {"question": "Why is a fake countdown timer that resets considered a manipulative marketing tactic?", "options": ["It has no real ethical concern attached to it", "It creates false urgency that misleads customers about the actual availability of an offer", "Countdown timers are always ethical regardless of accuracy", "It is a standard, universally accepted practice with no downside"], "correct_index": 1, "explanation": "A fake, resetting countdown misleads customers about real urgency, which is a manipulative and dishonest tactic."},
                {"question": "What does responsible data privacy practice generally require?", "options": ["Collecting as much customer data as possible regardless of need", "Only collecting necessary information, being transparent about its use, and obtaining clear consent before sharing it", "Selling customer data freely without disclosure", "Ignoring customer requests to opt out of communications"], "correct_index": 1, "explanation": "Ethical and often legally required data practice centers on necessity, transparency, and consent."},
                {"question": "Why is choosing honest advertising over exaggerated claims often described as the more sustainable business strategy?", "options": ["Exaggerated claims always produce better long-term results", "A brand's reputation compounds over time, and dishonesty eventually damages trust and future business", "Honesty has no real business impact either way", "Ethical marketing is only relevant for very large companies"], "correct_index": 1, "explanation": "Reputational damage from dishonesty tends to outweigh short-term gains, making honest marketing more sustainable long term."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career Readiness and Capstone",
            "title": "Kickoff: Your Full Growth Campaign Capstone",
            "learning_objective": "By the end of this class, you will be able to assemble a structured outline for your final growth campaign strategy and begin drafting it.",
            "duration_minutes": 30,
            "content_html": "<p>Today you formally begin your final capstone: a complete growth campaign strategy for a real or realistic brand, exactly as described in this course's final project brief. Every skill from research and positioning to channel selection, budgeting, and KPI setting comes together in this single strategic document.</p><h2>Structuring Your Campaign Strategy</h2><p>Start with your target audience and buyer persona from Day 2, refined with any competitive positioning insight from Day 22. Select and justify your specific channels using the persona-driven reasoning from Day 21's budget allocation lesson, rather than defaulting to whatever channel feels trendy. Build a four-week content plan with sample post copy, drawing on your Day 6 copywriting structure and Day 17 content calendar format, ensuring a healthy mix of content types across the funnel stages from Day 25's full-funnel thinking.</p><h2>Finishing the Strategy Document</h2><p>Allocate a realistic budget across your chosen channels with clear reasoning, exactly as practiced on Day 21, and set specific, measurable KPI targets with a plan for how you will track them, using the framework from Day 15. Begin drafting this document today starting with your persona and channel selection, the foundation everything else in your strategy depends on, and continue building out the content plan, budget, and KPIs in the sessions that follow.</p>",
            "key_concepts": ["Capstone campaign structuring", "Persona-to-channel reasoning", "Four-week content planning", "Budget and KPI integration", "Strategic document assembly"],
            "practical_exercise": {
                "title": "Start Your Final Growth Campaign Capstone",
                "instructions": "This IS the start of your final project. Write the persona and channel selection sections of your growth campaign strategy document: restate or refine your buyer persona from Day 2, then list your chosen marketing channels with a clear justification for each, referencing your persona and the budget allocation reasoning from Day 21."
            },
            "quiz": [
                {"question": "What four main components must the final growth campaign strategy include, according to the course's final project brief?", "options": ["Only a list of hashtags", "Channel selection, a content plan, budget allocation, and KPI targets", "A single social media post only", "A list of competitor names with no analysis"], "correct_index": 1, "explanation": "The final project brief specifically requires channel selection, a content plan, budget allocation, and KPI targets."},
                {"question": "Why does the capstone recommend starting with persona and channel selection before the content plan and budget?", "options": ["The order does not matter at all", "Channel and audience decisions form the foundation that the content plan, budget, and KPIs all depend on", "Content should always be planned before knowing the audience", "Budget should always be decided first with no persona"], "correct_index": 1, "explanation": "Persona and channel decisions ground every subsequent strategic choice, making them the logical starting point."},
                {"question": "Which earlier lesson's framework should directly inform the KPI section of the capstone?", "options": ["Day 4, profile setup", "Day 15, setting KPIs and measuring ROI", "Day 19, WhatsApp marketing", "Day 9, email marketing"], "correct_index": 1, "explanation": "Day 15 specifically covers how to define specific, measurable KPIs and calculate ROI, directly applicable to the capstone."}
            ],
            "resources": [
                {"label": "HubSpot Marketing", "url": "https://www.hubspot.com/marketing"},
                {"label": "Google Analytics", "url": "https://www.google.com/analytics"}
            ]
        }
    ]
}
