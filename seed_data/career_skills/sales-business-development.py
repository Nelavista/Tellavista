"""Seed data for the Sales & Business Development 30-Day Skill Class."""

SKILL = {
    "slug": "sales-business-development",
    "name": "Sales & Business Development",
    "tagline": "Learn to prospect, pitch, handle objections, and close real deals for products, services, and businesses across African markets.",
    "description": "Sales is the single most transferable skill a Nigerian or African university student can build, because every business, from a campus reseller to a fast-growing fintech, lives or dies on its ability to bring in revenue. This track takes a student from zero to being able to identify a target market, prospect for real leads, build a pitch, handle tough objections, and walk through a full deal from first contact to signed agreement. It matters for careers because sales and business development roles are widely available, often commission-boosted, and the skills transfer directly into running your own business or freelance practice.",
    "level": "beginner",
    "estimated_hours": 58,
    "course_title": "30-Day Sales & Business Development Career Track",
    "course_description": "After 30 days, a student can define a target market and ideal customer profile, run a structured prospecting campaign, build and deliver a pitch deck, handle common objections with confidence, and document a complete sales and business-development plan for a real or realistic product.",
    "final_project": {
        "title": "Complete Sales & Business Development Plan",
        "description": "Choose a specific product or service and a specific target market, such as a campus laundry app aimed at hostel students or a B2B invoicing tool aimed at small Lagos retailers, and build a full sales and business-development plan around it. You must write a prospecting strategy naming exactly where and how you would find qualified leads, build a short pitch deck that communicates the value proposition clearly, write an objection-handling script covering at least four realistic objections, and produce a mock closed-deal walkthrough that narrates a full sales conversation from first contact to signature. The final deliverable is a portfolio-ready document you could show a hiring manager or use as your own go-to-market plan, proving you can move a stranger from unaware to paying customer, not just describe sales theory.",
        "difficulty": "advanced",
        "estimated_hours": 11,
        "skills_demonstrated": ["Prospecting strategy", "Pitch deck creation", "Objection handling", "Negotiation and closing", "Target market definition", "Sales documentation"],
        "rubric": [
            {"name": "Target market and prospecting strategy quality", "max_points": 25},
            {"name": "Pitch deck clarity and value proposition strength", "max_points": 25},
            {"name": "Objection-handling script realism and coverage", "max_points": 25},
            {"name": "Mock closed-deal walkthrough completeness and realism", "max_points": 25}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Sales Foundations and Mindset",
            "title": "What Sales Actually Is: Solving Problems, Not Pushing Products",
            "learning_objective": "By the end of this class, you will be able to explain the difference between value-based selling and manipulative selling using a real example.",
            "duration_minutes": 25,
            "content_html": "<p>Many students avoid sales because they picture a pushy stranger forcing a product on someone who does not want it. That image is wrong, and it is worth unlearning on day one, because the best salespeople in the world are not the loudest talkers, they are the best listeners who genuinely solve a problem for the person in front of them.</p><h2>Value Exchange, Not Manipulation</h2><p>Selling, at its core, is a value exchange: the buyer gives money because what they receive is worth more to them than the money they are giving up. A salesperson's real job is to understand a buyer's problem well enough to show them, honestly, whether a product solves it. Manipulation tries to create a sale that should not happen, while value-based selling simply removes friction from a sale that already makes sense for both sides.</p><h2>Worked Example</h2><p>Imagine a student selling a printing and binding service to final-year project students in Ibadan. A manipulative approach might exaggerate turnaround time or hide extra costs to force a quick payment. A value-based approach instead asks what deadline the student is working with, explains honestly what is possible, and only proposes the service if it truly fits. The value-based seller closes fewer desperate one-time sales, but earns referrals and repeat business, which is where real income in sales comes from over time.</p>",
            "key_concepts": ["Value-based selling", "Sales as problem-solving", "Manipulation vs persuasion", "Trust and repeat business"],
            "practical_exercise": {
                "title": "Identify a Real Problem You Could Solve",
                "instructions": "Write down one product or service you could realistically sell today, on or around your campus or community. In three to five sentences, describe the specific problem it solves for a specific type of person, and explain why a value-based pitch would work better than a pushy one for this particular buyer."
            },
            "quiz": [
                {"question": "What is the core idea behind value-based selling?", "options": ["A sale happens because the buyer genuinely gets more value than the money spent", "Convincing anyone to buy regardless of fit", "Selling only to people who already trust you", "Hiding costs until after payment"], "correct_index": 0, "explanation": "Value-based selling is built on a genuine, honest exchange where the buyer benefits at least as much as the seller."},
                {"question": "Why does a value-based approach tend to build a stronger long-term income for a salesperson?", "options": ["It closes deals faster than any other method", "It generates referrals and repeat business because buyers trust the seller", "It requires no follow-up after the sale", "It avoids talking to customers directly"], "correct_index": 1, "explanation": "Honest, well-fit sales create trust, which drives referrals and repeat purchases over time."},
                {"question": "In the printing and binding example, what made the value-based approach different from the manipulative one?", "options": ["It offered a lower price automatically", "It skipped a conversation entirely", "It asked about the buyer's actual deadline and only proposed the service if it truly fit", "It used louder marketing language"], "correct_index": 2, "explanation": "The value-based seller diagnosed the real need first, rather than forcing a sale regardless of fit."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Sales Foundations and Mindset",
            "title": "Understanding Your Product's Value Proposition",
            "learning_objective": "By the end of this class, you will be able to write a one-sentence value proposition for a specific product and buyer.",
            "duration_minutes": 25,
            "content_html": "<p>Before you can sell anything well, you need to be able to explain in one clear sentence why a specific buyer should care. Many beginners describe features, like a phone has a bigger battery, instead of value, like you will not have to carry a charger to a full day of lectures, and that gap is often the difference between a confused prospect and an interested one.</p><h2>Features vs Benefits vs Value</h2><p>A feature is a fact about the product. A benefit is what that fact allows the buyer to do. Value is the specific outcome that benefit produces for this particular buyer's life or business. A strong value proposition connects all three in one sentence: this product does X, which means you can Y, so you get Z.</p><h2>Worked Example</h2><p>Consider a mobile point-of-sale app for small shop owners in Kano. Feature: it works offline and syncs later. Benefit: sales are recorded even without internet. Value proposition: unlike paper record books, this app lets a shop owner track every sale even during network outages, so nothing is lost and end-of-day totals are always accurate. Notice the value proposition names a real pain, being unsure of daily totals, and ties it directly to a concrete outcome the shop owner cares about.</p>",
            "key_concepts": ["Feature vs benefit vs value", "Value proposition statement", "Buyer-specific framing", "Outcome-focused selling"],
            "practical_exercise": {
                "title": "Write Your Product's Value Proposition",
                "instructions": "Using the product or service you chose on Day 1, list one feature, its benefit, and the value it creates for your buyer. Then write a single, clear value proposition sentence in the format this product does X, which means you can Y, so you get Z."
            },
            "quiz": [
                {"question": "What is the difference between a feature and a benefit?", "options": ["They mean exactly the same thing", "A feature is a fact about the product, a benefit is what that fact lets the buyer do", "A benefit is always more technical than a feature", "Features only apply to physical products"], "correct_index": 1, "explanation": "A feature describes what the product has or does; a benefit describes what that enables for the buyer."},
                {"question": "Why did the point-of-sale app example emphasize offline syncing specifically?", "options": ["Because it was the cheapest feature to build", "Because all apps must work offline", "Because it directly addressed a real pain point around losing sales records", "Because shop owners never use smartphones"], "correct_index": 2, "explanation": "The value proposition worked because it connected a real feature to a specific, painful problem the buyer already had."},
                {"question": "A strong value proposition should primarily be framed around what?", "options": ["A long list of every feature the product has", "The company's history and founding story", "Generic claims about being the best in the market", "The specific outcome a particular buyer cares about"], "correct_index": 3, "explanation": "Value propositions work best when they are specific to the buyer's real outcome, not generic or feature-heavy."}
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Sales Foundations and Mindset",
            "title": "Defining Your Ideal Customer Profile and Target Market",
            "learning_objective": "By the end of this class, you will be able to build a one-page ideal customer profile describing exactly who you should sell to.",
            "duration_minutes": 25,
            "content_html": "<p>Trying to sell to everyone almost always means selling to no one, because your message, channels, and pitch cannot be sharp if you are not sure who is on the other end. An ideal customer profile, often shortened to ICP, narrows that down to a specific, describable type of buyer most likely to say yes and stay happy.</p><h2>Building an ICP</h2><p>A useful ICP includes who the buyer is, such as their role, age range, or business type, what problem they urgently have, what budget or resources they typically control, and where they can be found, whether online or offline. For business-to-business selling, the ICP might describe a type of company, its size, and the specific job title of the decision maker. For consumer selling, it looks more like a buyer persona built from real behavior, not guesses.</p><h2>Worked Example</h2><p>A student selling a WhatsApp-based tutoring service for WAEC exam preparation should not target all Nigerian students. A sharper ICP is: SS3 students in Lagos or Abuja public and private secondary schools, whose parents are actively worried about exam performance and already pay for extra lessons, reachable through parent WhatsApp groups and school gate flyers. This ICP tells you exactly where to prospect and what pain point to lead with, which is the entire point of building one before you start reaching out to anyone.</p>",
            "key_concepts": ["Ideal customer profile (ICP)", "Target market narrowing", "B2B vs B2C profiling", "Buyer accessibility"],
            "practical_exercise": {
                "title": "Build a One-Page Ideal Customer Profile",
                "instructions": "For your chosen product, write a one-page ideal customer profile covering who the buyer is, what urgent problem they have, what resources or budget they control, and exactly where you could realistically find them. Save this document, since it will anchor your final project's prospecting strategy."
            },
            "quiz": [
                {"question": "Why is trying to sell to everyone usually a weak strategy?", "options": ["It always costs more money than targeted selling", "Everyone always has the same problems", "The message, channels, and pitch cannot be sharp without a specific buyer in mind", "It is illegal in most markets"], "correct_index": 2, "explanation": "A vague audience forces a vague pitch, which rarely persuades anyone specific."},
                {"question": "What should an ideal customer profile include beyond who the buyer is?", "options": ["Only their favorite color", "Nothing beyond their age", "Their political opinions", "Their urgent problem, available budget or resources, and where they can be reached"], "correct_index": 3, "explanation": "A useful ICP is actionable: it tells you what to say and where to find the buyer, not just a demographic label."},
                {"question": "In the WAEC tutoring example, why was targeting parent WhatsApp groups specifically useful?", "options": ["It matched exactly where the identified ICP could realistically be found and reached", "It was the only communication channel that exists", "WhatsApp groups guarantee a sale automatically", "It required no further research"], "correct_index": 0, "explanation": "A sharp ICP names a real, reachable channel, turning the profile into an actionable prospecting plan."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Sales Foundations and Mindset",
            "title": "The Sales Pipeline: Stages From First Contact to Closed Deal",
            "learning_objective": "By the end of this class, you will be able to map a sale onto the correct stage of a standard sales pipeline.",
            "duration_minutes": 25,
            "content_html": "<p>A sale rarely happens in one conversation. Understanding the stages a deal moves through helps a salesperson know exactly what to do next with any given prospect, instead of randomly following up and hoping something sticks.</p><h2>The Standard Pipeline Stages</h2><p>Most sales pipelines follow a similar pattern: prospecting, where you find potential buyers; qualifying, where you confirm they have the problem, budget, and authority to buy; the pitch or demo, where you present the solution; handling objections, where concerns are addressed honestly; and closing, where the deal is agreed and payment or a signed contract follows. After closing, many sales roles also track onboarding and retention, since a happy customer often buys again or refers others.</p><h2>Worked Example</h2><p>A business-development intern at a small logistics startup in Port Harcourt finds a restaurant that might need delivery partnerships through Instagram, that is prospecting. She calls the owner and confirms they currently struggle with late deliveries and have budget allocated for a solution, that is qualifying. She presents the delivery service's tracking dashboard, that is the pitch. The owner worries about delivery fees eating into margins, and she addresses it with real numbers, that is objection handling. The owner signs a three-month trial agreement, that is closing. Knowing exactly which stage a deal is in tells her precisely what action to take next, rather than guessing.</p>",
            "key_concepts": ["Sales pipeline stages", "Prospecting", "Qualifying", "Objection handling", "Closing"],
            "practical_exercise": {
                "title": "Map a Real or Imagined Deal to the Pipeline",
                "instructions": "Write a short five-sentence story of a sale for your chosen product, one sentence per pipeline stage: prospecting, qualifying, pitching, objection handling, and closing. Label each sentence with its stage name."
            },
            "quiz": [
                {"question": "What happens during the qualifying stage of a sales pipeline?", "options": ["The deal is signed and paid for", "The product is delivered to the customer", "The seller finds new potential buyers", "The seller confirms the prospect has the problem, budget, and authority to buy"], "correct_index": 3, "explanation": "Qualifying confirms a prospect is actually a fit before investing more time pitching to them."},
                {"question": "Why is it useful for a salesperson to know exactly which pipeline stage a deal is in?", "options": ["It tells them what action to take next instead of guessing", "It has no practical use", "It is only useful for company reporting", "Pipeline stages are the same as payment methods"], "correct_index": 0, "explanation": "Knowing the stage clarifies the next concrete step needed to move the deal forward."},
                {"question": "In the logistics example, what pipeline stage was the restaurant owner's concern about delivery fees?", "options": ["Prospecting", "Objection handling", "Qualifying", "Closing"], "correct_index": 1, "explanation": "Addressing a specific concern raised by the buyer is the objection-handling stage of the pipeline."}
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Sales Foundations and Mindset",
            "title": "Prospecting Basics: Finding People Worth Talking To",
            "learning_objective": "By the end of this class, you will be able to list three specific, realistic sources of qualified leads for a given product.",
            "duration_minutes": 25,
            "content_html": "<p>Prospecting is the unglamorous work that makes every other sales skill possible, because a brilliant pitch delivered to the wrong person is still a wasted pitch. Good prospecting means finding people who actually match your ideal customer profile, not just anyone who might listen.</p><h2>Common Prospecting Sources</h2><p>Warm sources include existing contacts, past customers, and referrals, and they tend to convert fastest because trust already exists. Online sources include LinkedIn, relevant WhatsApp or Telegram communities, Twitter or X spaces, and Facebook groups where your ICP already gathers. Offline sources include events, campus organizations, markets, and local business associations. The strongest prospecting plans usually combine two or three sources rather than relying on one, since different buyers are reachable in different places.</p><h2>Worked Example</h2><p>A student selling social media management services to small businesses might combine three sources: asking three existing clients for one referral each, joining two local business WhatsApp groups in her city and offering free value before pitching, and commenting genuinely on Instagram posts of small businesses that clearly have inconsistent posting. Each source reaches business owners at a different level of trust and readiness, which increases her total number of realistic conversations per week far more than posting one generic ad and waiting.</p>",
            "key_concepts": ["Prospecting sources", "Warm vs cold leads", "Online and offline channels", "Multi-channel prospecting"],
            "practical_exercise": {
                "title": "List Three Realistic Lead Sources",
                "instructions": "For your chosen product and ideal customer profile, list three specific, realistic sources where you could find qualified leads this week, at least one online and one offline or warm-contact based. For each source, write one sentence on exactly how you would approach people found there."
            },
            "quiz": [
                {"question": "Why do warm sources like referrals tend to convert faster than cold outreach?", "options": ["They always require less effort to close", "Trust already exists between the referred lead and the seller", "Warm sources never involve any conversation", "Referrals are always cheaper than advertising"], "correct_index": 1, "explanation": "Existing trust from a referral shortens the time needed to build credibility with a new lead."},
                {"question": "Why do the strongest prospecting plans usually combine multiple sources?", "options": ["Different buyers are reachable and comfortable in different places", "Because using only one source is against sales best practice rules", "Multiple sources are always free to use", "It reduces the total number of conversations needed"], "correct_index": 0, "explanation": "Combining sources increases the total pool of realistic conversations by reaching buyers where they naturally are."},
                {"question": "In the social media management example, why did the student join local business WhatsApp groups?", "options": ["To avoid ever making a direct pitch", "Because WhatsApp groups guarantee sales automatically", "To replace the need for referrals entirely", "Because her ideal customers, small business owners, were likely already active there"], "correct_index": 3, "explanation": "Prospecting works best when you go to channels where your specific ideal customer profile already spends time."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Outreach, Discovery, and Qualifying",
            "title": "Writing Cold Outreach Messages That Actually Get Replies",
            "learning_objective": "By the end of this class, you will be able to write a personalized cold outreach message following a proven structure.",
            "duration_minutes": 25,
            "content_html": "<p>Most cold messages get ignored because they are generic, too long, or ask for too much too soon. A cold message's only real job is to earn a reply, not to close a deal, and understanding that changes how you write it.</p><h2>A Simple Structure That Works</h2><p>An effective cold message usually has four parts: a specific, personalized opening that proves you did real research, not a copy-paste; a short statement of the relevant problem you believe they have; a one-line hint at how you could help, without a full pitch; and a low-friction ask, such as a quick question or a short call, rather than demanding a meeting immediately. Keeping the whole message under one hundred words respects the reader's time and increases reply rates significantly.</p><h2>Worked Example</h2><p>Generic and weak: Hi, I offer bookkeeping services for businesses, let me know if interested. Strong: Hi Chidinma, I noticed your boutique posted about struggling to track expenses across two branches last week. I help small retail businesses like yours set up a simple weekly bookkeeping system so nothing falls through the cracks at tax time. Would you be open to a fifteen-minute call this week to see if it is a fit? The strong version proves research, names a specific problem, and asks for something small and easy to say yes to.</p>",
            "key_concepts": ["Cold outreach structure", "Personalization", "Low-friction call to action", "Message length and reply rates"],
            "practical_exercise": {
                "title": "Write Three Personalized Cold Messages",
                "instructions": "Using one of the lead sources you identified on Day 5, write three different cold outreach messages to three specific, realistic people or businesses, each under one hundred words, each following the four-part structure covered today. Make each message genuinely different, not a copy-paste template."
            },
            "quiz": [
                {"question": "What is the actual job of a cold outreach message?", "options": ["To earn a reply, not to close the deal", "To close the entire deal immediately", "To list every feature of the product", "To ask for a large amount of the reader's time upfront"], "correct_index": 0, "explanation": "A cold message succeeds if it starts a conversation; closing comes later in the pipeline."},
                {"question": "Why does a low-friction ask, like a fifteen-minute call, work better than demanding an immediate meeting?", "options": ["It guarantees a sale", "Longer requests are always illegal to send", "It is easier for a stranger to say yes to a small, low-risk request", "It removes the need for any further follow-up"], "correct_index": 2, "explanation": "Smaller asks lower the barrier to a first yes, which is the actual goal of a cold message."},
                {"question": "What made the strong bookkeeping example message more effective than the generic one?", "options": ["It was written in bold text", "It referenced a specific, researched detail about the recipient's real problem", "It offered a discount immediately", "It was sent to more people at once"], "correct_index": 1, "explanation": "Specific, researched personalization signals genuine interest and dramatically increases reply rates over generic templates."}
            ],
            "resources": []
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Outreach, Discovery, and Qualifying",
            "title": "Running a Discovery Call: Asking Questions That Matter",
            "learning_objective": "By the end of this class, you will be able to write five discovery-call questions that uncover a prospect's real need.",
            "duration_minutes": 25,
            "content_html": "<p>A discovery call is the first real conversation with a qualified prospect, and its purpose is to listen more than to talk. Beginners often rush into pitching before they truly understand the buyer's situation, which usually produces a pitch that misses what the buyer actually cares about.</p><h2>What Good Discovery Questions Do</h2><p>Strong discovery questions are open-ended, meaning they cannot be answered with a simple yes or no, and they dig into the buyer's current situation, their pain points, what they have already tried, and what a good outcome would look like for them. A useful pattern is to ask about the current process, the cost or frustration of that process, and what changing it successfully would mean for them.</p><h2>Worked Example</h2><p>A student pitching a laundry pickup service to a busy postgraduate researcher should not open with here is our pricing. Better questions include: how are you currently handling laundry with your schedule, what is the most frustrating part of that process, and what would it be worth to you to get that time back each week? The last question often reveals the real value driver, whether it is time, stress, or money, which then shapes exactly how the pitch should be framed later in the call.</p>",
            "key_concepts": ["Discovery call purpose", "Open-ended questions", "Uncovering pain points", "Value driver identification"],
            "practical_exercise": {
                "title": "Write Five Discovery Questions",
                "instructions": "For your chosen product and ideal customer profile, write five open-ended discovery questions you would ask on a first call, covering their current situation, their biggest frustration with it, and what a good outcome would look like to them."
            },
            "quiz": [
                {"question": "What is the main purpose of a discovery call?", "options": ["To immediately close the sale", "To recite every feature of the product", "To ask only yes-or-no questions", "To listen and understand the buyer's real situation and needs"], "correct_index": 3, "explanation": "Discovery calls exist to genuinely understand the buyer before proposing a solution."},
                {"question": "Why are open-ended questions preferred during discovery?", "options": ["They are faster to answer than yes-or-no questions", "They cannot be answered with a simple yes or no, so they reveal more detail", "They are required by law in sales conversations", "They avoid the need for any follow-up questions"], "correct_index": 1, "explanation": "Open-ended questions invite detailed answers that reveal real pain points and priorities."},
                {"question": "In the laundry example, what did the final question about time reveal?", "options": ["The real value driver behind the buyer's decision, such as time or stress", "The exact price the buyer wanted to pay", "That the buyer had no interest in the service", "The buyer's preferred laundry detergent brand"], "correct_index": 0, "explanation": "That question surfaced what the buyer actually valued most, which should shape the eventual pitch."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Outreach, Discovery, and Qualifying",
            "title": "Building Rapport and Trust Quickly With a Stranger",
            "learning_objective": "By the end of this class, you will be able to identify three specific techniques for building trust within the first minutes of a sales conversation.",
            "duration_minutes": 20,
            "content_html": "<p>People buy from people they trust, and trust with a total stranger has to be built quickly, often within the first few minutes of a call or message exchange. Rapport is not about fake flattery, it is about showing genuine interest and consistency.</p><h2>Practical Trust-Building Techniques</h2><p>Active listening, where you reference something the buyer just said rather than moving straight to your next point, signals that you are actually paying attention. Showing relevant credibility, such as a specific past result or a client similar to them, builds confidence without bragging. Being honest about limitations, such as admitting your product is not a perfect fit for every situation, paradoxically increases trust because it proves you are not just trying to close at any cost.</p><h2>Worked Example</h2><p>A freelance graphic designer pitching a small NGO in Abuja could build rapport by referencing a specific detail from the NGO's website, mentioning a similar NGO client whose donor materials she redesigned, and honestly noting that a full rebrand might be more than they need right now, suggesting a smaller starter package instead. That honesty about scope, rather than pushing the most expensive option, is often what convinces a cautious buyer that this designer is trustworthy enough to work with.</p>",
            "key_concepts": ["Rapport building", "Active listening", "Credibility signaling", "Honesty as a trust tool"],
            "practical_exercise": {
                "title": "Script a Rapport-Building Opening",
                "instructions": "Write a short script, four to six sentences, for how you would open a real sales conversation with a specific prospect, showing active listening, one credibility signal, and one honest limitation of your offer. Explain in one sentence why each element builds trust."
            },
            "quiz": [
                {"question": "Why does honestly admitting a limitation of your product often increase buyer trust?", "options": ["Buyers always prefer the cheapest option regardless of fit", "It is legally required in every sales conversation", "It proves the seller is not just trying to close at any cost", "It guarantees the deal will close immediately"], "correct_index": 2, "explanation": "Honesty about fit signals genuine advice rather than pure self-interest, which builds credibility."},
                {"question": "What does active listening in a sales conversation typically look like?", "options": ["Referencing something the buyer just said before continuing", "Interrupting to move to your next pitch point", "Speaking as much as possible without pausing", "Ignoring the buyer's specific comments"], "correct_index": 0, "explanation": "Referencing the buyer's own words shows they were genuinely heard, not just tolerated."},
                {"question": "In the graphic designer example, why did suggesting a smaller starter package help build trust?", "options": ["It guaranteed a larger sale later", "It was the only package she offered", "It avoided discussing pricing entirely", "It showed the designer cared about fit over maximizing the sale size"], "correct_index": 3, "explanation": "Recommending what genuinely fits the buyer's need, rather than the biggest possible sale, builds credibility."}
            ],
            "resources": []
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Outreach, Discovery, and Qualifying",
            "title": "Qualifying a Lead: Budget, Authority, Need, and Timing",
            "learning_objective": "By the end of this class, you will be able to apply the BANT framework to determine whether a lead is worth continued pursuit.",
            "duration_minutes": 25,
            "content_html": "<p>Not every interested person is worth chasing. Chasing an unqualified lead wastes time that could go toward someone actually ready and able to buy, so qualifying is one of the most valuable, if underrated, sales skills.</p><h2>The BANT Framework</h2><p>BANT stands for Budget, whether the prospect has money allocated or accessible for this kind of purchase; Authority, whether the person you are speaking to can actually make or strongly influence the decision; Need, whether they have a real, acknowledged problem your product addresses; and Timing, whether they need a solution now or much later. A lead strong on all four is worth prioritizing, while a lead missing several is either a longer-term nurture or not currently worth heavy effort.</p><h2>Worked Example</h2><p>A sales rep for a school-fee payment platform speaks to a school administrator who loves the product, has real need since manual fee tracking causes errors, but admits the final decision belongs to the proprietor, who is traveling for a month. This lead has strong need but weak authority and timing right now. The right move is not to abandon the lead, but to ask for an introduction to the proprietor and schedule a follow-up for when they return, rather than spending this week's limited selling time here.</p>",
            "key_concepts": ["BANT framework", "Budget qualification", "Decision-maker authority", "Lead prioritization"],
            "practical_exercise": {
                "title": "Qualify Two Sample Leads With BANT",
                "instructions": "Write two short, different lead scenarios for your chosen product, each two to three sentences long. For each, score it informally on Budget, Authority, Need, and Timing, and write one sentence recommending whether to prioritize, nurture, or deprioritize the lead."
            },
            "quiz": [
                {"question": "What does the A in BANT stand for?", "options": ["Authority", "Advertising", "Availability", "Attitude"], "correct_index": 0, "explanation": "Authority refers to whether the person you are speaking with can actually make or strongly influence the buying decision."},
                {"question": "Why is qualifying leads considered a valuable sales skill?", "options": ["It guarantees every lead will eventually buy", "It replaces the need for a pitch entirely", "It is only relevant for very large companies", "It prevents wasting limited time on leads unlikely to convert soon"], "correct_index": 3, "explanation": "Qualifying focuses effort on leads most likely to close, protecting a salesperson's limited time."},
                {"question": "In the school-fee platform example, what was the correct next step given weak authority and timing?", "options": ["Abandon the lead completely", "Immediately ask for full payment", "Ask for an introduction to the actual decision maker and follow up later", "Ignore the administrator entirely going forward"], "correct_index": 2, "explanation": "A lead with real need but weak authority or timing is often worth nurturing rather than dropping or over-investing in immediately."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Outreach, Discovery, and Qualifying",
            "title": "Tracking Every Deal With a Simple Spreadsheet CRM",
            "learning_objective": "By the end of this class, you will be able to set up a basic spreadsheet CRM that tracks leads through every pipeline stage.",
            "duration_minutes": 20,
            "content_html": "<p>Deals fall through the cracks not because sellers are lazy, but because memory is unreliable once you are juggling more than a handful of conversations at once. A simple, consistently updated tracking system, often called a CRM or customer relationship management tool, solves this without needing any paid software.</p><h2>Building a Minimum Viable CRM</h2><p>A basic spreadsheet CRM needs, at minimum, columns for the lead's name and contact information, the source they came from, the current pipeline stage, the date of the last contact, the next planned action and its date, and any notes from the conversation so far. The habit of updating it after every single interaction matters more than the tool itself, since even the best CRM is useless if it is not kept current.</p><h2>Worked Example</h2><p>A student running a phone accessory reselling side hustle keeps a spreadsheet with one row per potential customer: name, where they came from such as Instagram DM or a friend's referral, current stage such as pitched or negotiating, last contact date, and a next-action column that says things like follow up Thursday about the screen protector bundle. Reviewing this sheet for five minutes every morning tells her exactly who to message that day, instead of relying on memory and losing deals to simple forgetfulness.</p>",
            "key_concepts": ["CRM basics", "Pipeline tracking columns", "Next-action discipline", "Deal follow-up consistency"],
            "practical_exercise": {
                "title": "Build Your Own Spreadsheet CRM",
                "instructions": "Create a simple spreadsheet with columns for lead name, source, pipeline stage, last contact date, next action, and notes. Populate it with at least five realistic or real leads for your chosen product, filling in every column for each row."
            },
            "quiz": [
                {"question": "Why do deals commonly fall through the cracks without a tracking system?", "options": ["Sellers are usually careless on purpose", "Memory becomes unreliable once several conversations are happening at once", "CRMs are required by law", "Buyers always forget about the seller first"], "correct_index": 1, "explanation": "As conversation volume grows, relying on memory alone leads to missed follow-ups and lost deals."},
                {"question": "What matters more than which specific tool is used for a CRM?", "options": ["The price of the software", "Having as many columns as possible", "Using the most expensive available option", "Consistently updating it after every interaction"], "correct_index": 3, "explanation": "A CRM is only useful if it is kept current; the habit of updating it matters more than the tool itself."},
                {"question": "What is the purpose of a next-action column in a simple CRM?", "options": ["To clarify exactly what to do next and when, for each lead", "To record the buyer's favorite color", "To replace the need for any notes", "To track only closed deals"], "correct_index": 0, "explanation": "A next-action column turns a passive record into an active daily task list for follow-up."}
            ],
            "resources": []
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Crafting and Delivering the Pitch",
            "title": "Structuring a Pitch Around the Buyer's Real Problem",
            "learning_objective": "By the end of this class, you will be able to structure a spoken pitch using a problem-solution-proof format.",
            "duration_minutes": 25,
            "content_html": "<p>A pitch delivered before discovery is a guess. A pitch delivered after discovery, using what you learned about the buyer's real situation, is a tailored solution, and buyers can tell the difference almost immediately.</p><h2>The Problem-Solution-Proof Structure</h2><p>A strong pitch restates the specific problem the buyer described in discovery, in their own words where possible, so they feel heard. It then presents the solution directly tied to that problem, avoiding a full feature list in favor of the two or three points that matter most to this buyer. Finally, it offers proof, such as a past result, a testimonial, or a simple demonstration, to reduce the buyer's risk of believing a claim that sounds too good.</p><h2>Worked Example</h2><p>After a discovery call revealed a small event-planning business loses bookings because clients cannot pay deposits easily, a pitch for a payment-link tool might sound like: you mentioned losing at least two bookings a month because clients find bank transfers stressful and slow. This tool lets you send a simple payment link that clients can pay by card or transfer in under a minute, and one client of ours, a similar decor business in Enugu, recovered three bookings in their first month using it. That structure ties the pitch directly to the buyer's own stated pain, not a generic sales script.</p>",
            "key_concepts": ["Problem-solution-proof structure", "Tailored pitching", "Reducing perceived risk", "Using the buyer's own words"],
            "practical_exercise": {
                "title": "Write a Problem-Solution-Proof Pitch",
                "instructions": "Using a discovery scenario from your chosen product, write a spoken pitch of four to six sentences following the problem-solution-proof structure. Restate the buyer's problem in their own words, present two key solution points, and include one form of proof, even if it is a realistic hypothetical result."
            },
            "quiz": [
                {"question": "Why is a pitch delivered before any discovery often considered a guess?", "options": ["Because it always uses incorrect pricing", "Because pitches must always come after payment", "Because discovery calls are optional in every sale", "Because it is not grounded in the buyer's actual, confirmed problem"], "correct_index": 3, "explanation": "Without discovery, a pitch is based on assumption rather than the buyer's real, confirmed situation."},
                {"question": "What is the purpose of the proof step in the problem-solution-proof structure?", "options": ["To end the conversation immediately", "To list every feature of the product", "To reduce the buyer's risk in believing a claim by showing real evidence", "To avoid mentioning the price"], "correct_index": 2, "explanation": "Proof, such as a past result or testimonial, makes the pitch's claims more credible and lowers perceived risk."},
                {"question": "In the payment-link example, why did restating the client's own words about lost bookings matter?", "options": ["It showed the buyer their specific problem had genuinely been heard and understood", "It made the pitch longer, which is always better", "It was required by the payment tool's terms of service", "It replaced the need for any solution details"], "correct_index": 0, "explanation": "Reflecting the buyer's own stated problem builds trust that the pitch that follows is genuinely tailored, not generic."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Crafting and Delivering the Pitch",
            "title": "Building Your First Pitch Deck, Slide by Slide",
            "learning_objective": "By the end of this class, you will be able to outline a seven-slide pitch deck for a specific product and buyer.",
            "duration_minutes": 30,
            "content_html": "<p>A pitch deck turns a spoken pitch into something visual a buyer can follow along with or review later, which matters especially when the actual decision maker was not on the call and needs to review the idea afterward.</p><h2>A Simple Seven-Slide Structure</h2><p>A workable pitch deck includes: a title slide naming the product and who it is for; a problem slide stating the pain point clearly, ideally with a number or specific example; a solution slide showing how the product addresses it; a how-it-works slide with three or fewer simple steps; a proof slide with a testimonial, case study, or sample result; a pricing or offer slide that is clear and simple; and a clear next-step slide telling the buyer exactly what to do to move forward. Each slide should hold one main idea, not a paragraph of text.</p><h2>Worked Example</h2><p>For a campus tutoring service pitched to a parent association, the problem slide might state that sixty percent of surveyed SS3 students reported struggling most with mathematics before WAEC. The solution slide shows small-group weekly sessions led by verified university students. The proof slide shows a testimonial from a parent whose child improved from a C to a B in one term. The next-step slide simply says sign up for a free trial session this Saturday, with a phone number. Every slide answers one clear question a busy parent would ask.</p>",
            "key_concepts": ["Pitch deck structure", "One idea per slide", "Problem and solution slides", "Clear next-step slide"],
            "practical_exercise": {
                "title": "Outline Your Seven-Slide Pitch Deck",
                "instructions": "Write a slide-by-slide outline for your chosen product following the seven-slide structure: title, problem, solution, how it works, proof, pricing or offer, and next step. For each slide, write the exact headline and one to two supporting bullet points, not full paragraphs."
            },
            "quiz": [
                {"question": "Why should each slide in a pitch deck hold only one main idea?", "options": ["Slides with more text are harder to print", "Design software only allows one idea per slide", "It keeps the deck easy to follow and prevents overwhelming the buyer", "It reduces the total number of slides required"], "correct_index": 2, "explanation": "Simple, focused slides are easier for a buyer to follow and remember, especially when reviewed without the presenter."},
                {"question": "What is the purpose of the next-step slide at the end of a pitch deck?", "options": ["To repeat the problem slide's content", "To tell the buyer exactly what action to take to move forward", "To list the founder's personal biography", "To remove the need for any pricing information"], "correct_index": 1, "explanation": "A clear next step removes ambiguity about how the buyer should act after seeing the pitch."},
                {"question": "In the tutoring example, why did the problem slide include a specific statistic?", "options": ["Statistics are required by law in every pitch", "It replaced the need for a solution slide", "It was only relevant to parents, not students", "A specific number makes the problem feel real and credible rather than vague"], "correct_index": 3, "explanation": "Concrete evidence, like a specific statistic, makes a stated problem feel real and urgent rather than a vague claim."}
            ],
            "resources": []
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Crafting and Delivering the Pitch",
            "title": "Handling the Most Common Objections With Confidence",
            "learning_objective": "By the end of this class, you will be able to respond to a price objection using the acknowledge-reframe-evidence method.",
            "duration_minutes": 25,
            "content_html": "<p>Objections are not rejection, they are almost always requests for more information or reassurance. Learning to hear an objection without getting defensive is one of the clearest signs of a seller ready for real conversations with real money on the line.</p><h2>Acknowledge, Reframe, Evidence</h2><p>A reliable pattern for handling most objections is: acknowledge the concern genuinely, so the buyer feels heard rather than argued with; reframe the concern by connecting it to the value already established, rather than dismissing it; and provide evidence, such as a comparison, a number, or a guarantee, that directly addresses the specific worry. This avoids the common beginner mistake of either caving immediately on price or arguing that the objection is wrong.</p><h2>Worked Example</h2><p>Buyer: this is too expensive compared to what I currently do manually. Acknowledge: I understand, price is always a fair thing to weigh carefully. Reframe: it is worth comparing this to what the manual process actually costs you in errors and time, which you mentioned earlier averages about four hours a week. Evidence: at your stated hourly value, that is more than this tool's monthly cost in time alone, and you get that time back starting week one. This response takes the objection seriously instead of dismissing it, while still moving the conversation forward with real numbers.</p>",
            "key_concepts": ["Objection handling framework", "Acknowledge-reframe-evidence", "Price objections", "Avoiding defensiveness"],
            "practical_exercise": {
                "title": "Script a Price Objection Response",
                "instructions": "For your chosen product, write a realistic price objection a buyer might raise, then write your full response using the acknowledge-reframe-evidence structure, labeling each of the three parts clearly."
            },
            "quiz": [
                {"question": "What do most objections actually represent, according to today's lesson?", "options": ["A request for more information or reassurance", "A final, unchangeable rejection", "Proof the product has no value", "A sign the buyer is being dishonest"], "correct_index": 0, "explanation": "Most objections are genuine concerns seeking reassurance, not outright rejections of the offer."},
                {"question": "What is the risk of immediately caving on price when an objection is raised?", "options": ["There is no risk at all", "It can undercut the value already established and signal the original price was not justified", "It always increases the buyer's trust", "It guarantees the deal will close faster"], "correct_index": 1, "explanation": "Caving too quickly can suggest the original price was inflated, weakening the buyer's confidence in the value."},
                {"question": "In the price objection example, what role did the mention of four hours a week play?", "options": ["It was irrelevant supporting detail", "It replaced the need to acknowledge the concern", "It served as evidence connecting the cost to a real, buyer-stated time loss", "It was used to avoid answering the objection"], "correct_index": 2, "explanation": "The specific time figure served as concrete evidence tying the price to a cost the buyer had already confirmed."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Crafting and Delivering the Pitch",
            "title": "Negotiation Basics: Anchoring, Trade-offs, and Win-Win Deals",
            "learning_objective": "By the end of this class, you will be able to propose a fair trade-off in a simple negotiation scenario.",
            "duration_minutes": 25,
            "content_html": "<p>Negotiation is not about one side winning and the other losing, it is about finding terms both sides can genuinely accept without resentment, because a resentful customer rarely becomes a repeat one.</p><h2>Anchoring and Trade-offs</h2><p>Anchoring refers to whichever number or term is proposed first, since it shapes the range of the rest of the conversation, which is why sellers should usually propose the first number rather than asking the buyer to name one. When a buyer asks for a lower price or better terms, the strongest response is rarely a flat yes or no, but a trade-off: offering a concession in exchange for something in return, such as a longer commitment, a referral, or upfront payment.</p><h2>Worked Example</h2><p>A freelance web developer quotes one hundred and fifty thousand naira for a small business website. The client asks for one hundred thousand. Instead of simply accepting or refusing, the developer proposes: I can do one hundred and twenty thousand if you pay the full amount upfront instead of in two installments, since that removes my payment-collection risk. This trade-off gives the client a lower number while giving the developer something valuable in return, upfront cash flow, rather than simply losing thirty thousand naira in pure discount for nothing.</p>",
            "key_concepts": ["Anchoring", "Trade-off negotiation", "Win-win outcomes", "Concessions with conditions"],
            "practical_exercise": {
                "title": "Script a Trade-off Negotiation",
                "instructions": "Write a short negotiation scenario for your chosen product where a buyer asks for a lower price or better terms. Script your response as a specific trade-off, naming what you would give and what you would ask for in return, and explain in one sentence why this is fairer than a simple discount."
            },
            "quiz": [
                {"question": "Why do sellers often benefit from proposing the first number in a negotiation?", "options": ["It guarantees the buyer will accept immediately", "The first number anchors and shapes the range of the rest of the conversation", "It is a legal requirement in most sales", "It removes the need for any further discussion"], "correct_index": 1, "explanation": "Anchoring means the first number offered influences how the rest of the negotiation unfolds."},
                {"question": "What is the main idea behind offering a trade-off instead of a flat discount?", "options": ["Trade-offs are always more expensive for the buyer", "Trade-offs remove the need to discuss price at all", "A concession is exchanged for something valuable in return, keeping the deal fair for both sides", "Flat discounts are illegal in most negotiations"], "correct_index": 2, "explanation": "Trade-offs keep negotiations balanced by ensuring both sides give and receive something of value."},
                {"question": "In the web developer example, what did the developer receive in exchange for lowering the price?", "options": ["Nothing, it was a pure discount", "A public testimonial", "A longer project timeline", "Upfront payment instead of installments, reducing payment-collection risk"], "correct_index": 3, "explanation": "The developer traded a lower price for upfront payment, which reduced their financial risk on the project."}
            ],
            "resources": []
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Crafting and Delivering the Pitch",
            "title": "Case Study: A Full B2B Sales Cycle From Lead to Signed Contract",
            "learning_objective": "By the end of this class, you will be able to break down a real business-to-business sales cycle into its individual stages and decisions.",
            "duration_minutes": 30,
            "content_html": "<p>Seeing a complete, realistic sales cycle from start to finish helps connect everything learned so far into one coherent story, since real deals rarely move in a straight, simple line.</p><h2>Case Study: A Cleaning Supplies Distributor</h2><p>A business-development rep for a Lagos cleaning supplies distributor finds a mid-size hotel through a LinkedIn search of hospitality companies in the ICP. She sends a personalized cold message referencing the hotel's recent expansion announcement. The operations manager replies and agrees to a discovery call, where she learns the hotel currently juggles three separate suppliers and often runs out of stock unexpectedly. She proposes a single-supplier contract with guaranteed weekly restocking, presented in a short deck emailed after the call. The manager raises a price objection, comparing it to their cheapest current supplier. The rep acknowledges the concern, reframes around the hidden cost of stockouts and juggling three vendors, and offers a three-month trial period as a trade-off instead of a permanent discount.</p><h2>Why This Matters</h2><p>Every stage covered this week appears here: qualified prospecting, a real discovery call, a tailored pitch, a genuine objection handled without caving, and a trade-off negotiation that protected margin while still moving the deal forward. Notice that the trial period, not a price cut, was what actually unlocked the signed three-month agreement, because it reduced the hotel's perceived risk rather than reducing the distributor's revenue.</p>",
            "key_concepts": ["Full sales cycle", "B2B decision-making", "Risk reduction as a closing tool", "Trial periods as trade-offs"],
            "practical_exercise": {
                "title": "Write Your Own Full Sales Cycle Case Study",
                "instructions": "Using your chosen product, write a six-to-eight sentence case study narrating a full, realistic sales cycle from prospecting through a signed deal, explicitly naming which pipeline stage each sentence represents, similar to the cleaning supplies example."
            },
            "quiz": [
                {"question": "What ultimately unlocked the signed agreement in the cleaning supplies case study?", "options": ["A permanent price cut", "Ignoring the price objection entirely", "A trial period that reduced the hotel's perceived risk", "A much longer discovery call"], "correct_index": 2, "explanation": "The trial period addressed the buyer's risk concern without sacrificing the distributor's regular pricing."},
                {"question": "Why did the rep reframe the price objection around stockouts and multiple vendors?", "options": ["To avoid discussing price at all", "Because the hotel had no other suppliers", "To end the conversation immediately", "To connect the cost to a real, existing pain the hotel already experienced"], "correct_index": 3, "explanation": "Reframing tied the price to a genuine, already-acknowledged cost of the current situation, making the value clearer."},
                {"question": "What made the initial cold message to the hotel effective, based on the case study?", "options": ["It referenced a specific, real detail about the hotel's recent expansion", "It was sent to as many hotels as possible at once", "It immediately included full pricing", "It avoided mentioning the hotel by name"], "correct_index": 0, "explanation": "A specific, researched detail signaled genuine relevance rather than a generic mass message."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Advanced Selling Approaches",
            "title": "Selling to Businesses vs Selling to Individual Consumers",
            "learning_objective": "By the end of this class, you will be able to identify three key differences between B2B and B2C selling approaches.",
            "duration_minutes": 25,
            "content_html": "<p>The same underlying sales skills apply whether you are selling to a business or an individual consumer, but the decision-making process, timeline, and emotional drivers differ enough that treating them identically often backfires.</p><h2>Key Differences</h2><p>Business-to-business, or B2B, sales usually involve longer decision cycles, multiple stakeholders who each care about different things, and a stronger emphasis on return on investment and risk reduction. Business-to-consumer, or B2C, sales are usually faster, involve a single decision maker, and lean more heavily on emotional appeal, convenience, and immediate personal benefit, though price and trust still matter greatly. A pitch built for a company's finance team, focused entirely on ROI spreadsheets, would likely fall flat with an individual consumer simply looking for a quick, trustworthy solution to a personal problem.</p><h2>Worked Example</h2><p>A meal-prep delivery business selling to a single busy young professional in Lagos can pitch convenience and time saved this week, closing potentially within one conversation. The same business pitching a corporate office for staff meal plans instead needs to address a procurement manager's budget approval process, a facilities manager's logistics concerns, and possibly an HR representative's interest in staff wellbeing, often across several meetings before a decision is made. Recognizing which type of sale you are in shapes your entire approach from the first message.</p>",
            "key_concepts": ["B2B vs B2C selling", "Multiple stakeholders", "Decision cycle length", "Emotional vs ROI-driven appeal"],
            "practical_exercise": {
                "title": "Compare a B2B and B2C Pitch for Your Product",
                "instructions": "For your chosen product, write two short pitch openings, one framed for an individual consumer buyer and one framed for a business buyer, and explain in two to three sentences how the framing, tone, and emphasis differ between the two."
            },
            "quiz": [
                {"question": "What typically makes B2B sales cycles longer than B2C ones?", "options": ["B2B products are always more expensive", "B2C buyers never care about price", "B2B sales never involve any discovery call", "Multiple stakeholders are often involved, each caring about different concerns"], "correct_index": 3, "explanation": "Multiple decision-makers with different priorities usually extend the time needed to reach agreement in B2B sales."},
                {"question": "What tends to matter more in most B2C consumer sales compared to B2B?", "options": ["Emotional appeal, convenience, and immediate personal benefit", "Formal procurement approval processes", "Multi-stakeholder budget sign-off", "Quarterly return on investment reports"], "correct_index": 0, "explanation": "Individual consumers usually respond more to convenience and personal benefit than to formal ROI analysis."},
                {"question": "In the meal-prep example, why did the corporate pitch require addressing more people than the individual pitch?", "options": ["Corporate offices have no real decision-making process", "Procurement, facilities, and HR each had distinct, relevant concerns to address", "The individual buyer required more meetings", "Corporate buyers never care about logistics"], "correct_index": 1, "explanation": "Business sales often require satisfying several stakeholders with different priorities before a decision is reached."}
            ],
            "resources": []
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Advanced Selling Approaches",
            "title": "Account-Based Selling: Targeting Specific High-Value Companies",
            "learning_objective": "By the end of this class, you will be able to build a short research profile on one target company for an account-based approach.",
            "duration_minutes": 25,
            "content_html": "<p>Instead of casting a wide net and hoping some leads qualify, account-based selling flips the process by first choosing a small number of high-value target companies, then researching and approaching each one deliberately and thoroughly.</p><h2>How Account-Based Selling Works</h2><p>The process starts with defining what makes a company a great fit beyond just matching the ICP loosely, such as company size, recent growth signals, or a publicly known pain point. Next comes deep research on each target account: who the relevant decision makers are, what challenges the company has publicly discussed, and any warm connections that could provide an introduction. Outreach is then highly tailored to that specific account rather than using a generic template, often across multiple people within the same company at once.</p><h2>Worked Example</h2><p>A business-development rep for a payroll software company selects five fast-growing Nigerian startups that recently announced funding rounds, since new funding often means new hires and payroll complexity. For one target, a fintech that just closed a seed round, she researches the head of operations on LinkedIn, notes the company grew from ten to forty employees in six months according to a press release, and reaches out referencing that specific growth, connecting it directly to payroll complexity they are likely now facing. This deliberate, researched approach on a small number of accounts often outperforms broad, generic outreach to hundreds of unqualified leads.</p>",
            "key_concepts": ["Account-based selling", "High-value target accounts", "Deep account research", "Multi-contact outreach"],
            "practical_exercise": {
                "title": "Research One Target Account",
                "instructions": "Choose one specific, real or realistic company that would be a strong fit for your product. Write a short research profile covering why this company fits your ICP, one recent, specific detail about the company you could reference, and who the likely relevant decision maker would be."
            },
            "quiz": [
                {"question": "What is the core idea behind account-based selling?", "options": ["Contacting as many random companies as possible with the same message", "Choosing a small number of high-value target companies and researching each deeply", "Only selling to companies smaller than ten employees", "Avoiding any research before outreach"], "correct_index": 1, "explanation": "Account-based selling focuses deliberate, deep effort on a small set of carefully chosen target companies."},
                {"question": "Why did the payroll software rep target companies that recently raised funding?", "options": ["New funding often signals rapid hiring and growing payroll complexity", "Funded companies never need payroll software", "It was the only information publicly available", "Funding announcements guarantee an immediate sale"], "correct_index": 0, "explanation": "Recent funding was used as a relevant signal connecting directly to the product's value around growing payroll needs."},
                {"question": "Why does referencing a specific, researched detail about a target company strengthen outreach?", "options": ["It makes the message longer, which always performs better", "It replaces the need to mention the product at all", "It is required for legal compliance", "It shows the outreach is genuinely relevant and not a generic mass message"], "correct_index": 3, "explanation": "Specific, relevant research signals genuine interest and relevance, increasing the odds of a real reply."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Advanced Selling Approaches",
            "title": "Using LinkedIn Effectively for Business Development",
            "learning_objective": "By the end of this class, you will be able to write an optimized LinkedIn profile summary and a first-connection outreach message.",
            "duration_minutes": 25,
            "content_html": "<p>LinkedIn has become one of the most useful free tools available for business development, especially for B2B selling, because decision makers across almost every industry maintain a presence there, searchable by role, company, and industry.</p><h2>Profile and Outreach Basics</h2><p>Before reaching out to anyone, a profile should clearly state who you help and how, not just a job title, since a prospect will likely check your profile before responding. Connection requests perform far better with a short, personalized note referencing something specific about the person or their company than with a blank request. Once connected, the goal of an early message is still a reply and a conversation, not an immediate pitch, following the same low-friction principle covered earlier this month.</p><h2>Worked Example</h2><p>A weak LinkedIn headline reads Business Development at XYZ Company. A stronger one reads I help small Nigerian retailers reduce stock-out losses through better inventory software. A connection note might say: Hi Tunde, I saw your recent post about scaling your electronics store to a second branch, I work with growing retailers on exactly that kind of inventory challenge and would love to connect. This is specific, relevant, and gives Tunde a clear reason to accept beyond simple politeness, unlike a blank connection request with no context at all.</p>",
            "key_concepts": ["LinkedIn profile optimization", "Personalized connection notes", "Low-friction first messages", "Searchable decision makers"],
            "practical_exercise": {
                "title": "Write a LinkedIn Headline and Connection Note",
                "instructions": "Write an optimized LinkedIn-style headline for yourself or your business that clearly states who you help and how. Then write a short, personalized connection request note to a realistic target prospect for your chosen product, referencing a specific, plausible detail about them."
            },
            "quiz": [
                {"question": "Why do personalized connection notes tend to perform better than blank requests?", "options": ["A specific, relevant note gives the recipient a clear reason to accept", "LinkedIn requires a note to send any request", "Blank requests are automatically rejected by LinkedIn", "Personalized notes guarantee an immediate sale"], "correct_index": 0, "explanation": "A relevant, specific note stands out and gives the recipient genuine reason to accept, unlike a generic blank request."},
                {"question": "What should an early LinkedIn message after connecting aim to achieve?", "options": ["An immediate full pitch and price quote", "A request for the person's personal phone number only", "A reply and the start of a conversation", "Nothing, messaging is unnecessary after connecting"], "correct_index": 2, "explanation": "Like cold outreach, an early LinkedIn message should aim for a low-friction reply, not an immediate hard sell."},
                {"question": "Why was the headline I help small Nigerian retailers reduce stock-out losses stronger than Business Development at XYZ Company?", "options": ["It was longer in word count", "It clearly states who is helped and how, rather than just a job title", "It hid the person's actual role", "It included no useful information at all"], "correct_index": 1, "explanation": "A value-focused headline immediately tells a visiting prospect what problem you solve, which a bare job title does not."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Advanced Selling Approaches",
            "title": "Referral and Network-Based Selling",
            "learning_objective": "By the end of this class, you will be able to write a specific, easy-to-act-on referral request for an existing customer or contact.",
            "duration_minutes": 20,
            "content_html": "<p>Referred leads convert at dramatically higher rates than cold leads because trust is transferred instantly from the person making the introduction. Despite this, many sellers rarely ask for referrals directly, often out of a vague fear of seeming pushy.</p><h2>Asking for Referrals the Right Way</h2><p>A weak referral ask is vague, such as let me know if you hear of anyone who needs this. A strong referral ask is specific, naming exactly the kind of person or business you are looking for, which makes it far easier for the other person to actually think of someone. The best timing to ask is right after a customer has expressed genuine satisfaction, such as after a successful delivery, a positive review, or a renewed contract.</p><h2>Worked Example</h2><p>Instead of asking a happy client, a small bakery owner, do you know anyone who needs a website, a stronger ask sounds like: I loved working on your bakery's site, do you know any other small food business owners, maybe from your supplier or vendor network, who are still relying only on Instagram and might want a proper website too? Naming the specific type of business and even a likely network, supplier or vendor contacts, makes it dramatically easier for the bakery owner to think of an actual name rather than drawing a blank.</p>",
            "key_concepts": ["Referral selling", "Specific referral requests", "Optimal referral timing", "Trust transfer"],
            "practical_exercise": {
                "title": "Write a Specific Referral Request",
                "instructions": "Write a specific referral request you could send to a satisfied past or hypothetical customer of your chosen product. Name the exact type of person or business you are asking about and suggest a likely network where that referral might come from."
            },
            "quiz": [
                {"question": "Why do referred leads typically convert at higher rates than cold leads?", "options": ["Referred leads always have larger budgets", "Referrals require no discovery call at all", "Cold leads are always uninterested", "Trust is transferred instantly from the person making the introduction"], "correct_index": 3, "explanation": "A referral carries built-in trust from the referring person, which speeds up the trust-building process significantly."},
                {"question": "Why is a specific referral request more effective than a vague one?", "options": ["Specific requests are always shorter", "It is easier for the person to think of an actual name when given a clear description", "Vague requests are considered rude", "Specificity guarantees a referral will be given"], "correct_index": 1, "explanation": "A specific description narrows the search in the other person's mind, making it easier to recall someone who fits."},
                {"question": "When is generally the best time to ask an existing customer for a referral?", "options": ["Right after they have expressed genuine satisfaction with the result", "Before any work has been delivered", "Only once a year regardless of circumstances", "During a price negotiation"], "correct_index": 0, "explanation": "Satisfaction is highest right after a positive outcome, making it the most natural and effective time to ask."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Advanced Selling Approaches",
            "title": "Case Study: Closing a Deal With an Objection-Heavy Buyer",
            "learning_objective": "By the end of this class, you will be able to sequence a response strategy for a buyer who raises multiple objections in one conversation.",
            "duration_minutes": 30,
            "content_html": "<p>Real buyers rarely raise just one objection. A skeptical buyer often raises several concerns in sequence, and handling them one at a time, calmly, without getting flustered, is a skill worth practicing deliberately before it happens for real money.</p><h2>Case Study: A Skeptical Restaurant Owner</h2><p>A sales rep pitching a digital ordering and delivery system to a restaurant owner in Abuja faces three objections in one meeting. First: I already have a WhatsApp ordering system that works fine. The rep acknowledges this is common and asks how the owner currently tracks which orders are still pending, revealing a gap the owner had not framed as a problem before. Second: this sounds expensive for a small restaurant. The rep reframes around the cost of missed or mixed-up orders during busy periods, which the owner just admitted happens weekly. Third: I do not have time to learn a new system. The rep offers a specific, small commitment, a free quarter setup call, directly addressing the time concern without asking for a big commitment upfront.</p><h2>Why the Sequence Matters</h2><p>Notice the rep did not try to answer all three objections in one long speech, but addressed them one at a time as they came up, using discovery-style questions to reveal the real cost behind each objection before responding. Rushing through multiple objections at once often overwhelms a buyer and reduces the odds of a close, while handling them calmly, one at a time, keeps the buyer engaged and clear-headed.</p>",
            "key_concepts": ["Multiple objection sequencing", "Discovery-style objection handling", "Staying calm under pushback", "Small-commitment offers"],
            "practical_exercise": {
                "title": "Script a Multi-Objection Conversation",
                "instructions": "Write a realistic conversation for your chosen product where a buyer raises three different objections in sequence. Write your response to each objection separately, using a discovery question, a reframe, or a small-commitment offer as appropriate for each one."
            },
            "quiz": [
                {"question": "What mistake does the case study warn against when facing multiple objections at once?", "options": ["Addressing objections one at a time", "Asking discovery-style questions", "Trying to answer all objections in one long speech at once", "Offering a small, specific commitment"], "correct_index": 2, "explanation": "Answering everything at once tends to overwhelm the buyer; addressing objections one at a time keeps them engaged."},
                {"question": "How did the rep respond to the restaurant owner's existing WhatsApp system objection?", "options": ["By asking a discovery question that revealed a gap the owner had not previously named", "By dismissing WhatsApp as an inferior tool immediately", "By offering an immediate discount", "By ending the conversation"], "correct_index": 0, "explanation": "The rep used a question to surface a real, underlying problem rather than directly arguing against the existing system."},
                {"question": "What kind of offer addressed the owner's concern about not having time to learn a new system?", "options": ["A request for a large upfront payment", "A demand to switch systems immediately", "A longer, more detailed product demo", "A small, specific commitment, a free quarter setup call"], "correct_index": 3, "explanation": "A small, low-risk commitment directly addressed the time concern without requiring a big leap from the buyer."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Metrics, Strategy, and Closing Mastery",
            "title": "Sales Metrics That Matter: Conversion Rate, Win Rate, and Velocity",
            "learning_objective": "By the end of this class, you will be able to calculate conversion rate and win rate from a sample set of sales numbers.",
            "duration_minutes": 25,
            "content_html": "<p>Improving as a salesperson requires more than gut feeling about how things are going, it requires tracking a few key numbers that reveal exactly where a pipeline is strong or leaking, so effort can go where it actually helps.</p><h2>Core Metrics to Track</h2><p>Conversion rate measures the percentage of leads that move from one stage to the next, such as from prospected to qualified. Win rate measures the percentage of qualified opportunities that result in a closed deal. Deal velocity measures how long, on average, a deal takes from first contact to close. Tracking these over time reveals patterns, such as a strong prospecting volume but a weak pitch-to-close conversion, which points to the pitch or objection handling needing improvement rather than needing more leads.</p><h2>Worked Example</h2><p>A student running a small graphic design side hustle prospected forty people last month, twelve replied and became qualified conversations, a thirty percent conversion rate, but only three of those twelve became paying clients, a twenty-five percent win rate. Average deal velocity was eleven days from first message to payment. Looking at these numbers, the real bottleneck is not prospecting, which is working reasonably well, but converting qualified conversations into paying clients, meaning her time is better spent this month improving her pitch and objection handling rather than sending more cold messages.</p>",
            "key_concepts": ["Conversion rate", "Win rate", "Deal velocity", "Pipeline bottleneck diagnosis"],
            "practical_exercise": {
                "title": "Calculate Your Own Sample Sales Metrics",
                "instructions": "Using realistic numbers for your chosen product, invent a sample month of activity: leads prospected, leads qualified, and deals closed. Calculate the conversion rate and win rate, and write two to three sentences identifying where the biggest bottleneck likely is based on your numbers."
            },
            "quiz": [
                {"question": "What does win rate measure?", "options": ["The percentage of qualified opportunities that result in a closed deal", "The total number of leads contacted", "The average time a deal takes to close", "The total revenue earned in a month"], "correct_index": 0, "explanation": "Win rate specifically measures how often qualified opportunities actually convert into closed deals."},
                {"question": "Why is tracking these metrics over time useful for a salesperson?", "options": ["It has no practical use beyond reporting", "It replaces the need for any actual selling", "It only matters for large sales teams", "It reveals exactly where the pipeline is strong or leaking so effort can be targeted correctly"], "correct_index": 3, "explanation": "Metrics reveal specific bottlenecks, helping a seller focus improvement efforts where they matter most."},
                {"question": "In the graphic design example, what did the numbers reveal was the real bottleneck?", "options": ["Not enough people were being prospected", "Deal velocity was far too slow to be useful", "Converting qualified conversations into paying clients was the weaker link", "There was no bottleneck at all"], "correct_index": 2, "explanation": "Prospecting and initial replies were reasonably strong, but the drop-off happened at converting conversations into paid clients."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Metrics, Strategy, and Closing Mastery",
            "title": "Building a Complete Prospecting Strategy for a Target Market",
            "learning_objective": "By the end of this class, you will be able to draft a full prospecting strategy naming channels, weekly targets, and outreach cadence.",
            "duration_minutes": 30,
            "content_html": "<p>Individual prospecting techniques matter less without a coherent overall strategy tying them together into a repeatable weekly system, since sporadic, unplanned outreach rarely produces consistent results.</p><h2>Components of a Full Prospecting Strategy</h2><p>A complete prospecting strategy names the specific channels to be used, based on where the ideal customer profile is reachable; sets a realistic weekly target for new leads contacted; defines a follow-up cadence, such as three touches over ten days before considering a lead cold; and includes a simple way to measure results weekly using the metrics covered yesterday. Writing this down, rather than keeping it in your head, makes it far easier to stay consistent, especially during weeks when motivation is lower.</p><h2>Worked Example</h2><p>A freelance social media manager's prospecting strategy might read: primary channel is Instagram DMs to small businesses posting inconsistently, secondary channel is two local business WhatsApp groups; weekly target is fifteen new outreach messages; follow-up cadence is an initial message, a follow-up after three days if no reply, and a final follow-up after seven days before moving on; results are reviewed every Friday using reply rate and number of discovery calls booked. This turns a vague intention to find more clients into a specific, repeatable weekly system she can actually execute and improve over time.</p>",
            "key_concepts": ["Prospecting strategy components", "Weekly outreach targets", "Follow-up cadence", "Repeatable weekly system"],
            "practical_exercise": {
                "title": "Draft Your Full Prospecting Strategy",
                "instructions": "Write a complete prospecting strategy for your chosen product covering primary and secondary channels, a specific weekly outreach target, a defined follow-up cadence with exact timing, and how you will measure results each week. This document should be usable directly in your final project."
            },
            "quiz": [
                {"question": "Why does writing a prospecting strategy down matter more than keeping it in your head?", "options": ["Written strategies are required by law", "It makes it far easier to stay consistent, especially in low-motivation weeks", "Spoken strategies are always inaccurate", "It removes the need to ever prospect again"], "correct_index": 1, "explanation": "A written, specific plan supports consistency and follow-through better than a vague mental intention."},
                {"question": "What does a follow-up cadence define within a prospecting strategy?", "options": ["The total revenue target for the month", "The exact price of the product", "The design of the pitch deck", "The specific timing and number of follow-up touches before considering a lead cold"], "correct_index": 3, "explanation": "A cadence defines exactly when and how many times to follow up before moving on from an unresponsive lead."},
                {"question": "In the social media manager's strategy, how often were results reviewed?", "options": ["Every Friday, using reply rate and discovery calls booked", "Once a year", "Only after closing a deal", "Results were never reviewed"], "correct_index": 0, "explanation": "A weekly review cadence allows the strategy to be adjusted quickly based on real, recent performance data."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Metrics, Strategy, and Closing Mastery",
            "title": "Advanced Objection Handling: Reframing and Social Proof",
            "learning_objective": "By the end of this class, you will be able to combine a reframe with a specific piece of social proof to strengthen an objection response.",
            "duration_minutes": 25,
            "content_html": "<p>Basic objection handling addresses a concern directly, but advanced objection handling strengthens the response further by adding social proof, evidence that other similar people or businesses have faced the same doubt and been satisfied anyway.</p><h2>Combining Reframe and Social Proof</h2><p>Social proof works because buyers trust the experience of people similar to them more than they trust a seller's own claims about their product. Effective social proof is specific rather than vague, naming a similar business, a specific result, or a real number rather than simply saying many clients love this. Pairing a reframe, which reconnects the objection to real value, with a specific proof point makes the response far more persuasive than either alone.</p><h2>Worked Example</h2><p>A buyer objects: I am not sure this training program will actually help my staff perform better. A reframe alone might say the program is specifically designed around practical skills, not just theory. Adding social proof strengthens it further: in fact, a retail chain with a similar staff size in Ibadan saw a measurable drop in customer complaints within six weeks of running this exact program with their front-desk team. The specific business type, similar size, and a measurable result make the claim far more believable than a vague reassurance alone, because the buyer can picture a business much like their own having already faced this same doubt.</p>",
            "key_concepts": ["Social proof", "Specific vs vague evidence", "Combining reframe and proof", "Buyer trust in similar peers"],
            "practical_exercise": {
                "title": "Write a Reframe-Plus-Proof Objection Response",
                "instructions": "For your chosen product, write a realistic objection and a full response combining a reframe with one specific, believable piece of social proof, naming a similar business or buyer type, a specific detail, and a result."
            },
            "quiz": [
                {"question": "Why does social proof tend to persuade buyers effectively?", "options": ["Buyers trust the seller's own claims more than any outside experience", "Social proof replaces the need for a real product", "It is only useful in consumer sales, never in B2B", "Buyers trust the experience of people similar to them more than a seller's own claims"], "correct_index": 3, "explanation": "Seeing that similar buyers had success builds credibility that a seller's own claims alone cannot provide."},
                {"question": "What makes social proof more effective, according to today's lesson?", "options": ["Being as vague and general as possible", "Avoiding any mention of other customers", "Being specific, naming a similar business, a real number, or a measurable result", "Focusing only on the seller's personal opinion"], "correct_index": 2, "explanation": "Specific, concrete proof is more believable and persuasive than vague, general claims."},
                {"question": "In the training program example, why did mentioning a similar retail chain in Ibadan strengthen the response?", "options": ["It let the buyer picture a business like their own having faced and overcome the same doubt", "It was completely unrelated to the buyer's situation", "It replaced the need to describe the program at all", "It avoided answering the original objection"], "correct_index": 0, "explanation": "A relatable, similar example makes it easier for the buyer to trust the claim applies to their own business too."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Metrics, Strategy, and Closing Mastery",
            "title": "Closing Techniques: Reading Buying Signals and Asking for the Sale",
            "learning_objective": "By the end of this class, you will be able to identify three common buying signals and match each to an appropriate closing question.",
            "duration_minutes": 25,
            "content_html": "<p>Many deals are lost not because the buyer said no, but because the seller never actually asked for the sale clearly, hoping the buyer would simply volunteer to commit on their own. Closing is a skill that has to be practiced deliberately, since it feels uncomfortable to many beginners at first.</p><h2>Buying Signals and Closing Questions</h2><p>Common buying signals include asking detailed questions about implementation or delivery timing, asking about payment options, or using language that assumes ownership, such as when we start using this. Once a buying signal appears, a direct but low-pressure closing question moves the conversation forward, such as would you like to go ahead and get started this week, or which of the two payment options works better for you. Avoiding a clear ask at this point often causes a warm, ready buyer to simply drift away without ever formally deciding.</p><h2>Worked Example</h2><p>A prospect who has already asked how soon delivery could start and whether installment payment is available is showing two strong buying signals. Instead of continuing to explain more features, the seller should say something like: it sounds like this could work well for you, would you prefer to pay in full or in two installments to get started this week? This directly acknowledges the signals and moves toward a decision, rather than letting a genuinely interested buyer's momentum quietly fade over days of no clear next step.</p>",
            "key_concepts": ["Buying signals", "Direct closing questions", "Assumptive language", "Avoiding lost momentum"],
            "practical_exercise": {
                "title": "Script Three Closes Matched to Buying Signals",
                "instructions": "Write three different buying signals a prospect might show for your chosen product, and for each one, write a direct, low-pressure closing question that matches and responds to that specific signal."
            },
            "quiz": [
                {"question": "Why are many deals lost even when a buyer is genuinely interested?", "options": ["The buyer always changes their mind eventually", "Buying signals do not actually exist", "The seller never clearly asks for the sale, and the buyer's momentum fades", "Closing questions are considered unprofessional"], "correct_index": 2, "explanation": "Interested buyers can lose momentum and drift away if a seller never directly asks for the commitment."},
                {"question": "Which of the following is an example of a buying signal?", "options": ["A prospect ending the call abruptly with no questions", "A prospect asking about implementation timing or payment options", "A prospect asking to be removed from all future contact", "A prospect never responding to any messages"], "correct_index": 1, "explanation": "Detailed questions about starting or paying signal genuine, active interest in moving forward."},
                {"question": "What should a seller generally do once a clear buying signal appears?", "options": ["Continue listing more product features indefinitely", "End the conversation immediately without a response", "Wait for the buyer to bring up closing on their own", "Ask a direct, low-pressure closing question"], "correct_index": 3, "explanation": "A direct, appropriately timed closing question capitalizes on the buyer's expressed readiness to move forward."}
            ],
            "resources": []
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Metrics, Strategy, and Closing Mastery",
            "title": "Account Management and Upselling After the Deal Closes",
            "learning_objective": "By the end of this class, you will be able to identify a realistic upsell opportunity based on a customer's usage pattern.",
            "duration_minutes": 20,
            "content_html": "<p>Closing a deal is not the finish line, it is the start of a relationship that, managed well, produces far more value than the first sale alone, through renewals, upsells, and referrals covered earlier this month.</p><h2>Managing the Relationship After the Close</h2><p>Good account management means checking in proactively rather than only when there is a problem, tracking how the customer is actually using the product or service, and looking for genuine opportunities where an additional product, upgrade, or service would create more value for them, not just more revenue for the seller. A good upsell is offered because it truly helps the customer, not because it is the next item on a sales quota.</p><h2>Worked Example</h2><p>A small business bookkeeping service notices, three months after onboarding a client, that the client has grown from one shop to two locations and is now manually reconciling both in separate spreadsheets. Reaching out to suggest a multi-location reporting add-on is a natural, relevant upsell tied directly to a real change in the client's situation, not a random additional charge. Framing it around the specific pain, no longer just simple record keeping but reconciling growth across two branches, makes the upsell feel like continued good service rather than a sales push.</p>",
            "key_concepts": ["Account management", "Proactive check-ins", "Usage-based upselling", "Customer-first upsell framing"],
            "practical_exercise": {
                "title": "Identify a Realistic Upsell Scenario",
                "instructions": "For your chosen product, write a short scenario where an existing customer's situation has changed in a way that creates a genuine opportunity for an additional product, upgrade, or service. Write the specific message you would send to propose the upsell, framed around their real, changed need."
            },
            "quiz": [
                {"question": "What defines a good upsell, according to today's lesson?", "options": ["An offer that genuinely helps the customer based on a real change in their needs", "Anything that increases revenue regardless of customer benefit", "Offering the same upsell to every customer automatically", "Avoiding any further contact after the first sale"], "correct_index": 0, "explanation": "A genuine upsell is tied to a real, changed customer need, not simply pushed to increase revenue."},
                {"question": "Why is proactive check-in considered good account management?", "options": ["It guarantees an upsell every time", "It helps identify real changes in the customer's situation before problems arise", "It replaces the need for the original product entirely", "It is only necessary for unhappy customers"], "correct_index": 1, "explanation": "Regular, proactive engagement helps a seller notice real opportunities and issues early, not just when something goes wrong."},
                {"question": "In the bookkeeping example, what specific change justified the upsell offer?", "options": ["The client asked for a discount", "The client stopped using the service entirely", "The client had grown to two locations and was manually reconciling both separately", "There was no real change, it was a random offer"], "correct_index": 2, "explanation": "The upsell was tied directly to a genuine operational change in the client's business, making it relevant and timely."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career Readiness and the Final Project",
            "title": "How Sales Careers Work: Roles, Commission, and Career Paths",
            "learning_objective": "By the end of this class, you will be able to describe the difference between at least three common sales job titles and how compensation typically works for each.",
            "duration_minutes": 25,
            "content_html": "<p>Sales offers one of the widest entry points into paid work for university students and graduates, since many companies hire for potential and coachability over formal experience, but understanding the different roles available helps target the right opportunities.</p><h2>Common Sales Roles</h2><p>A sales development representative, often called an SDR, focuses primarily on prospecting and qualifying leads, then handing them to a closer, and is a common entry-level role. An account executive typically owns the full cycle from qualified lead to closed deal. A business development representative often focuses specifically on outbound outreach and new partnerships. Compensation in sales frequently combines a base salary with commission tied to results, meaning strong performers can often earn significantly above the stated base, which rewards exactly the skills built throughout this course.</p><h2>Worked Example</h2><p>A university student applying to a Nigerian fintech's SDR program would primarily be expected to prospect, qualify using something like BANT, and book discovery calls for a senior account executive, rather than close deals independently on day one. This role is an excellent place to build real pipeline and outreach skills quickly, often with a lower entry bar than an account executive role, and strong SDR performance is one of the most common paths toward being promoted into a full account executive position within a year or two.</p>",
            "key_concepts": ["Sales development representative (SDR)", "Account executive", "Base salary plus commission", "Entry-level sales career paths"],
            "practical_exercise": {
                "title": "Map Your Own Sales Career Entry Point",
                "instructions": "Research or reason through which entry-level sales role, such as SDR or business development representative, would be the most realistic first step for you. Write three to four sentences explaining why, what skills from this course apply directly, and one specific type of company you might target."
            },
            "quiz": [
                {"question": "What does a sales development representative typically focus on?", "options": ["Only closing final contracts", "Prospecting and qualifying leads before handing them to a closer", "Managing company finances", "Designing the product itself"], "correct_index": 1, "explanation": "SDRs generally handle the top of the pipeline, prospecting and qualifying, rather than the full close."},
                {"question": "How does compensation typically work in many sales roles?", "options": ["A fixed salary with no variation regardless of performance", "Payment only after one full year of employment", "A base salary combined with commission tied to results", "No compensation until the entire team hits quota"], "correct_index": 2, "explanation": "Base-plus-commission structures are common in sales, directly rewarding strong individual performance."},
                {"question": "Why is an SDR role often a good entry point for a university student?", "options": ["It requires years of prior closing experience", "It never leads to any career advancement", "It focuses entirely on product design", "It has a lower entry bar and builds core prospecting and qualifying skills quickly"], "correct_index": 3, "explanation": "SDR roles are frequently accessible to newcomers and build foundational skills useful for later advancement."}
            ],
            "resources": [
                {"label": "Indeed Career Advice", "url": "https://www.indeed.com/career-advice"}
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career Readiness and the Final Project",
            "title": "What Hiring Managers Actually Look for in a Sales Candidate",
            "learning_objective": "By the end of this class, you will be able to list four specific qualities hiring managers evaluate in a sales interview beyond raw talkativeness.",
            "duration_minutes": 20,
            "content_html": "<p>A common misconception is that hiring managers want the most talkative, confident-sounding candidate. In reality, most experienced sales hiring managers care far more about coachability, resilience, and evidence of real results or effort than about someone simply sounding smooth.</p><h2>What Actually Gets Evaluated</h2><p>Coachability matters because sales techniques are taught and refined constantly, and a candidate who reacts defensively to feedback is a warning sign. Resilience matters because rejection is frequent in sales, and how someone talks about handling a string of no's often reveals more than a single success story. Curiosity and listening ability matter because the best salespeople ask good questions rather than talk the most, directly connecting back to the discovery skills covered earlier this month. Evidence of initiative, such as a self-driven project, a side hustle, or documented results, stands out far more than a list of soft-skill adjectives on a resume.</p><h2>Worked Example</h2><p>Two candidates apply for the same SDR role. One says I am a natural people person and great communicator with no supporting detail. The other says I ran a small tutoring referral side hustle, tracked a thirty percent reply rate on my outreach messages, and improved it to forty five percent after changing my message structure. The second candidate demonstrates real initiative, measurable results, and a coachable, iterative mindset, all of which are far more convincing to an experienced hiring manager than a confident but unsupported claim.</p>",
            "key_concepts": ["Coachability", "Resilience to rejection", "Curiosity and listening", "Demonstrated initiative over claims"],
            "practical_exercise": {
                "title": "Draft Your Own Evidence-Based Sales Pitch for a Job",
                "instructions": "Write a short, three-to-four sentence answer to the interview prompt tell me about a time you handled rejection or a difficult conversation, using a real or realistic example that demonstrates resilience and a specific, measurable detail, following the style of the second candidate in today's example."
            },
            "quiz": [
                {"question": "According to today's lesson, what do experienced sales hiring managers often value more than raw talkativeness?", "options": ["How loudly a candidate speaks", "The candidate's physical appearance", "Coachability, resilience, and evidence of real initiative or results", "How quickly a candidate can list product features"], "correct_index": 2, "explanation": "Substantive qualities like coachability and demonstrated initiative matter far more than surface-level confidence."},
                {"question": "Why does resilience matter specifically in sales roles?", "options": ["Sales roles never involve any rejection", "Resilience is irrelevant to job performance", "It only matters for senior executive roles", "Rejection is frequent in sales, and how someone handles it reveals a lot about fit"], "correct_index": 3, "explanation": "Frequent rejection is a normal part of sales work, making resilience a genuinely important trait to demonstrate."},
                {"question": "What made the second candidate's answer in the worked example more convincing?", "options": ["It included specific, measurable results and evidence of an iterative, coachable mindset", "It was longer than the first candidate's answer", "It avoided mentioning any real experience", "It focused only on general personality traits"], "correct_index": 0, "explanation": "Specific, measurable evidence of initiative and improvement is far more persuasive than unsupported personality claims."}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career Readiness and the Final Project",
            "title": "Answering Common Sales Interview Questions With Real Structure",
            "learning_objective": "By the end of this class, you will be able to structure an answer to a common sales interview question using the situation-action-result method.",
            "duration_minutes": 25,
            "content_html": "<p>Sales interviews often include behavioral questions that essentially test whether a candidate can sell themselves using the same structured thinking they would apply to a real deal, which makes today's lesson a direct extension of everything practiced this month.</p><h2>The Situation-Action-Result Method</h2><p>A strong behavioral answer briefly sets the situation, so the interviewer understands the context; clearly explains the specific action taken, not a vague generality; and states the measurable or observable result, ideally with a number or concrete outcome. This structure prevents the common mistake of rambling through a story without ever landing on a clear, memorable point.</p><h2>Worked Example</h2><p>Question: tell me about a time you had to convince someone skeptical to try something new. Situation: while running a small campus phone accessory side hustle, a regular customer was skeptical about a new screen protector brand I had started stocking. Action: instead of insisting it was better, I offered to apply it for free on one of his older phones so he could judge the quality himself before paying for anything. Result: he not only bought two, one for himself and one for his sister, but referred three classmates over the following month. This answer is specific, shows initiative, and ties directly back to value-based selling, honesty, and referral generation, themes covered throughout this entire course.</p>",
            "key_concepts": ["Situation-action-result structure", "Behavioral interview questions", "Specific over vague answers", "Connecting stories to real sales skills"],
            "practical_exercise": {
                "title": "Structure Two Interview Answers",
                "instructions": "Choose two common sales interview questions, such as tell me about a time you handled an objection or tell me about a time you missed a target, and write a full situation-action-result answer for each using a real or realistic example from your own experience."
            },
            "quiz": [
                {"question": "What does the situation-action-result method require an answer to clearly include?", "options": ["Only a long, general personal story with no clear structure", "A list of every product feature ever sold", "An apology for past sales mistakes", "Context, a specific action taken, and a measurable or observable result"], "correct_index": 3, "explanation": "The method structures an answer around clear context, a specific action, and a concrete result."},
                {"question": "Why is a vague action, like I tried my best, considered weak in a behavioral interview answer?", "options": ["It does not clearly show what the candidate actually did, unlike a specific described action", "It is too specific for interviewers to follow", "Vague answers are always the correct approach", "Interviewers never ask about actions"], "correct_index": 0, "explanation": "Specific, concrete actions demonstrate real capability far better than vague statements of effort."},
                {"question": "In the screen protector example, what made the result section effective?", "options": ["It included no outcome at all", "It gave a concrete, measurable outcome, including new sales and referrals", "It focused only on the customer's initial skepticism", "It avoided mentioning any specific numbers"], "correct_index": 1, "explanation": "A specific, measurable outcome makes the story memorable and credible to an interviewer."}
            ],
            "resources": [
                {"label": "Indeed Career Advice", "url": "https://www.indeed.com/career-advice"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career Readiness and the Final Project",
            "title": "Building a Sales Portfolio to Prove Results Without a Job Yet",
            "learning_objective": "By the end of this class, you will be able to list three specific artifacts you could include in a sales portfolio to prove capability before formal work experience.",
            "duration_minutes": 20,
            "content_html": "<p>A common frustration for students entering sales is not having formal job experience to point to, but a sales portfolio solves this by proving capability through self-driven work, exactly like the deliverables being built throughout this course.</p><h2>What Belongs in a Sales Portfolio</h2><p>A strong sales portfolio can include a documented prospecting campaign, even a small self-run one, with real numbers such as messages sent and reply rate; a sample pitch deck built for a realistic or real product; a written objection-handling script showing structured thinking; and any real results from freelance, side-hustle, or volunteer selling, even informal ones, described with specific numbers wherever possible. The goal is to show, not just claim, that you understand and can apply the sales process.</p><h2>Worked Example</h2><p>A student with no formal sales job experience builds a simple portfolio page describing a small campus event ticket-selling campaign she ran, including the exact prospecting channels used, a sample message template, the conversion rate from message to sale, and a short reflection on what she would improve next time. This single, well-documented example, with real specific numbers, is often far more convincing to a hiring manager than a resume bullet point simply claiming strong communication skills, because it demonstrates the actual process and thinking, not just the claim.</p>",
            "key_concepts": ["Sales portfolio artifacts", "Self-driven proof of skill", "Documented campaign results", "Showing vs claiming ability"],
            "practical_exercise": {
                "title": "Outline Your Sales Portfolio",
                "instructions": "List three specific artifacts you could include in your own sales portfolio, using work already produced during this course or a real side hustle. For each, write one sentence describing exactly what it proves about your sales ability."
            },
            "quiz": [
                {"question": "What problem does a sales portfolio primarily solve for a student without formal job experience?", "options": ["It replaces the need for any interview", "It proves capability through self-driven, documented work rather than formal job history", "It guarantees a job offer automatically", "It is only useful for experienced sales professionals"], "correct_index": 1, "explanation": "A portfolio demonstrates real, applied skill even without a traditional employment history."},
                {"question": "Why is a documented example with specific numbers more convincing than a resume claim alone?", "options": ["It shows the actual process and thinking, not just an unsupported claim", "Numbers are always exaggerated in portfolios", "Resume claims are always more detailed", "Specific numbers are irrelevant to hiring managers"], "correct_index": 0, "explanation": "Concrete, documented evidence demonstrates real capability far more convincingly than a general claim."},
                {"question": "Which of the following would be a strong addition to a sales portfolio?", "options": ["A vague statement about being a people person", "An unrelated hobby with no connection to sales", "A list of product features memorized from a manual", "A documented prospecting campaign with real reply-rate numbers"], "correct_index": 3, "explanation": "A documented, results-based campaign directly demonstrates applied sales skill, unlike a vague personality claim."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career Readiness and the Final Project",
            "title": "Final Project Kickoff: Building Your Complete Sales & Business Development Plan",
            "learning_objective": "By the end of this class, you will be able to outline all four required sections of your Complete Sales & Business Development Plan and begin drafting the first one.",
            "duration_minutes": 30,
            "content_html": "<p>Today marks the start of the Complete Sales & Business Development Plan, the final project that brings together every skill built over the past twenty-nine days into one portfolio-ready document built around a specific product and a specific target market.</p><h2>What the Final Project Requires</h2><p>The plan requires four connected sections: a prospecting strategy naming exact channels, weekly targets, and follow-up cadence, drawing directly on Day 22's work; a pitch deck communicating a clear value proposition, following the seven-slide structure from Day 12; an objection-handling script covering at least four realistic objections, using the acknowledge-reframe-evidence and social-proof techniques from Days 13 and 23; and a mock closed-deal walkthrough narrating a full, realistic conversation from first contact to signature, similar in style to the case studies on Days 15 and 20.</p><h2>How to Approach Today</h2><p>Rather than trying to write all four sections at once, today's focus is choosing your final product and target market if you have not already settled on one from earlier days, and drafting the prospecting strategy section first, since it anchors who you are writing the rest of the plan for. A plan grounded in a specific, realistic buyer will be dramatically stronger than one written for a vague, generic audience, exactly as emphasized since Day 3.</p>",
            "key_concepts": ["Final project structure", "Prospecting strategy section", "Integrating prior deliverables", "Portfolio-ready documentation"],
            "practical_exercise": {
                "title": "Begin Your Complete Sales & Business Development Plan",
                "instructions": "Start your final project now: confirm the specific product and target market you will use, then write the full prospecting strategy section of your Complete Sales & Business Development Plan, naming your channels, weekly outreach target, and follow-up cadence, building directly on your Day 22 draft."
            },
            "quiz": [
                {"question": "What are the four required sections of the Complete Sales & Business Development Plan?", "options": ["A prospecting strategy, a pitch deck, an objection-handling script, and a mock closed-deal walkthrough", "A resume, a cover letter, a reference list, and a portfolio", "A budget report, a org chart, a marketing plan, and a legal contract", "A product description, a price list, a delivery schedule, and a return policy"], "correct_index": 0, "explanation": "The final project requires these four specific, connected deliverables built around one product and target market."},
                {"question": "Why does today's lesson recommend starting with the prospecting strategy section first?", "options": ["It is the least important section", "The other sections cannot use any earlier course work", "It anchors who the rest of the plan is being written for", "It has no connection to the target market"], "correct_index": 2, "explanation": "Defining the target market and prospecting approach first grounds the pitch, objections, and walkthrough that follow."},
                {"question": "Which earlier day's work does the objection-handling script section build most directly on?", "options": ["Day 1 only", "Days 13 and 23, covering acknowledge-reframe-evidence and social proof", "Day 10's CRM setup", "Day 4's pipeline stages"], "correct_index": 1, "explanation": "The objection-handling techniques taught on Days 13 and 23 are the direct foundation for this section of the final project."}
            ],
            "resources": [
                {"label": "HubSpot Sales", "url": "https://www.hubspot.com/sales"}
            ]
        }
    ]
}
