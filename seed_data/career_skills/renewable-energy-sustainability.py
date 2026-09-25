"""Seed data for the Renewable Energy & Sustainability 30-Day Skill Class."""

SKILL = {
    "slug": "renewable-energy-sustainability",
    "name": "Renewable Energy & Sustainability",
    "tagline": "Learn to assess, size, and pitch real solar and sustainability projects for African communities and businesses.",
    "description": "Renewable energy and sustainability is one of the fastest-growing sectors on the continent, driven by an electricity access gap that affects hundreds of millions of people and a rising demand from businesses for measurable environmental responsibility. This track builds the technical vocabulary, assessment methods, and financial reasoning used by real solar mini-grid developers and sustainability consultants, then applies them to a genuine feasibility or impact study. It matters because employers in this field, from development finance institutions to solar EPC companies, hire people who can prove they understand load calculations, cost-benefit analysis, and stakeholder realities, not just climate slogans.",
    "level": "beginner",
    "estimated_hours": 58,
    "course_title": "30-Day Renewable Energy & Sustainability Career Track",
    "course_description": "After 30 days, a student can assess a community's or business's energy and sustainability needs, size and cost a basic renewable energy system, evaluate financial and environmental impact, and produce a professional feasibility or impact report suitable for an employer, investor, or client.",
    "final_project": {
        "title": "Renewable Energy Feasibility or Sustainability Impact Study",
        "description": "Choose one of two real-world capstone paths: a solar mini-grid feasibility study for a specific underserved Nigerian or African community, or a sustainability audit with recommendations for a small business or corporate operation. Your study must include a documented needs assessment, technical system sizing or intervention design, a cost-benefit and financial analysis, identification of key stakeholders and risks, and a set of clear, prioritized recommendations. The final deliverable is a professional written report, similar to what a solar developer, NGO, or sustainability consultancy would present to a funder, client, or hiring manager, proving you can turn raw data into a fundable, actionable plan rather than general commentary about clean energy.",
        "difficulty": "advanced",
        "estimated_hours": 10,
        "skills_demonstrated": [
            "Energy or sustainability needs assessment",
            "Technical system sizing",
            "Cost-benefit and financial analysis",
            "Stakeholder and risk analysis",
            "Professional report writing",
            "Data-driven recommendations"
        ],
        "rubric": [
            {
                "name": "Technical feasibility or intervention analysis depth and accuracy",
                "max_points": 30
            },
            {
                "name": "Cost-benefit and financial analysis quality",
                "max_points": 30
            },
            {
                "name": "Stakeholder, policy, and contextual grounding",
                "max_points": 25
            },
            {
                "name": "Report clarity, structure, and professionalism",
                "max_points": 15
            }
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Energy Access and Renewable Fundamentals",
            "title": "Africa's Electricity Gap and Why Renewable Energy Is a Career Opportunity",
            "learning_objective": "By the end of this class, you will be able to explain why the African electricity access gap has created real, well-paying career paths in renewable energy.",
            "duration_minutes": 25,
            "content_html": "<p>Over half of Sub-Saharan Africa still lacks reliable access to the grid, and even where a grid connection exists, blackouts are common enough that businesses budget separately for diesel generators. This gap is not just a hardship statistic, it is one of the largest active job markets on the continent, spanning solar installers, mini-grid developers, energy auditors, and sustainability consultants who are paid to close that gap one community or company at a time.</p><h2>Why This Sector Is Hiring</h2><p>Governments, development finance institutions, and private investors are pouring money into off-grid and renewable solutions because diesel is expensive and unreliable, while solar costs have fallen dramatically over the past decade. Every solar mini-grid, every rooftop installation, and every corporate sustainability program needs people who can assess a site, run the numbers, and write up a plan a funder will actually approve.</p><h2>Worked Example</h2><p>Consider a rural community in Kaduna State with no grid connection, where households currently spend an average of four thousand naira a month on kerosene and phone charging trips to a nearby town. A mini-grid developer sees this spending as proof of willingness to pay: if that same four thousand naira could instead cover a solar home system subscription, the community gets better light and power, and the developer has a viable customer base. Recognizing that pattern, spending on a poor energy source as evidence of demand for a better one, is the first instinct this track will train in you.</p>",
            "key_concepts": [
                "Electricity access gap",
                "Off-grid energy market",
                "Willingness to pay",
                "Renewable energy career paths",
                "Diesel dependency cost"
            ],
            "practical_exercise": {
                "title": "Document a Local Energy Access Story",
                "instructions": "Write a short profile of one household, business, or community you know personally that deals with unreliable electricity. Describe how they currently cope, such as generators, candles, or phone charging trips, and estimate roughly how much they spend monthly coping with the problem. Submit this as a half-page write-up that you will reuse later in the course."
            },
            "quiz": [
                {
                    "question": "What does the term electricity access gap primarily describe?",
                    "options": [
                        "The portion of the population without reliable access to grid electricity",
                        "The difference between solar and wind energy output",
                        "The cost difference between diesel and petrol generators",
                        "The number of power plants in a country"
                    ],
                    "correct_index": 0,
                    "explanation": "The electricity access gap refers to the share of people lacking reliable grid electricity access."
                },
                {
                    "question": "Why do investors see spending on kerosene or diesel as a useful signal?",
                    "options": [
                        "It proves people dislike renewable energy",
                        "It shows people are already paying for a worse energy option, indicating demand for a better one",
                        "It means the community has no money at all",
                        "It is irrelevant to renewable energy planning"
                    ],
                    "correct_index": 1,
                    "explanation": "Existing spending on poor energy sources demonstrates willingness to pay, which supports the business case for a better alternative."
                },
                {
                    "question": "Which of these is an example of a career created by the energy access gap?",
                    "options": [
                        "Radio broadcaster",
                        "Professional footballer",
                        "Mini-grid developer",
                        "Fashion designer"
                    ],
                    "correct_index": 2,
                    "explanation": "Mini-grid development is a direct career response to closing the electricity access gap."
                }
            ],
            "resources": [
                {
                    "label": "IRENA - International Renewable Energy Agency",
                    "url": "https://www.irena.org"
                }
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Energy Access and Renewable Fundamentals",
            "title": "Energy Basics: Watts, Kilowatt-Hours, and Calculating Daily Load",
            "learning_objective": "By the end of this class, you will be able to calculate the daily energy consumption of a household or business in kilowatt-hours.",
            "duration_minutes": 25,
            "content_html": "<p>Before anyone can size a solar system or write a credible feasibility study, they need to speak the basic language of electricity: watts, kilowatts, and kilowatt-hours. This vocabulary is what separates a professional energy assessment from a guess, and it is used in every job interview and every real report in this field.</p><h2>The Core Units</h2><p>A watt (W) measures how much power a device uses at any instant, and a kilowatt (kW) is simply one thousand watts. A kilowatt-hour (kWh) measures energy used over time, calculated as power multiplied by hours of use. A 100-watt bulb left on for 10 hours consumes 1 kWh (100 watts times 10 hours, divided by 1000 to convert watts to kilowatts). This single formula, power multiplied by time equals energy, is the foundation of every load calculation you will do in this course.</p><h2>Worked Example</h2><p>A small provision shop in Enugu runs a 100W fridge for 24 hours, three 15W LED bulbs for 6 hours, and a 60W fan for 8 hours daily. The fridge uses 2.4 kWh, the bulbs use a combined 0.27 kWh, and the fan uses 0.48 kWh, giving a total daily load of about 3.15 kWh. This number, the shop's daily energy demand, is the very first input any solar installer needs before recommending panel and battery sizes, and getting it wrong means undersizing a system that fails the customer or oversizing one that wastes their money.</p>",
            "key_concepts": [
                "Watt and kilowatt",
                "Kilowatt-hour",
                "Power multiplied by time",
                "Daily load calculation",
                "Appliance energy consumption"
            ],
            "practical_exercise": {
                "title": "Calculate a Daily Energy Load",
                "instructions": "List five appliances used in your own home or a business you know, including each appliance's wattage and average daily hours of use. Calculate the kWh consumed by each appliance and sum them to find the total daily energy load. Present your work as a simple table with appliance, watts, hours, and kWh columns."
            },
            "quiz": [
                {
                    "question": "What does a kilowatt-hour measure?",
                    "options": [
                        "Instantaneous power draw of a device",
                        "The physical size of a solar panel",
                        "The voltage of an electrical system",
                        "Energy consumed over time, calculated as power multiplied by hours"
                    ],
                    "correct_index": 3,
                    "explanation": "A kilowatt-hour is a unit of energy, equal to power in kilowatts multiplied by the number of hours used."
                },
                {
                    "question": "A 100W bulb running for 10 hours consumes how much energy?",
                    "options": [
                        "1 kWh",
                        "100 kWh",
                        "10 kWh",
                        "0.1 kWh"
                    ],
                    "correct_index": 0,
                    "explanation": "100 watts times 10 hours equals 1000 watt-hours, which converts to 1 kWh."
                },
                {
                    "question": "Why is calculating daily load the essential first step before sizing a solar system?",
                    "options": [
                        "It determines what color the panels should be",
                        "It tells the installer how much energy the system must supply, avoiding undersizing or oversizing",
                        "It is only needed for grid-connected systems",
                        "Load calculations are optional in professional practice"
                    ],
                    "correct_index": 1,
                    "explanation": "Accurate daily load figures are the foundation for correctly sizing panels, batteries, and inverters."
                }
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Energy Access and Renewable Fundamentals",
            "title": "How Solar Photovoltaic Panels Convert Sunlight into Electricity",
            "learning_objective": "By the end of this class, you will be able to describe how solar panels generate electricity and what affects their real-world output.",
            "duration_minutes": 25,
            "content_html": "<p>Solar panels look simple from the outside, but understanding what actually happens inside one is what lets you explain performance issues to a client, troubleshoot underperforming systems, and estimate realistic energy output rather than relying on marketing claims from panel sellers.</p><h2>How Photovoltaic Cells Work</h2><p>A solar panel is made of photovoltaic cells, usually silicon, that generate direct current (DC) electricity when sunlight hits them, a process called the photovoltaic effect. Panels are rated by their peak capacity in watts under ideal laboratory conditions, but real-world output is almost always lower because of temperature, dust, cloud cover, and the angle of installation. This is why professionals use a concept called peak sun hours, the equivalent number of hours per day when sunlight intensity is strong enough to produce a panel's rated output, rather than assuming a panel produces its rated wattage for every daylight hour.</p><h2>Worked Example</h2><p>A 300W panel installed in Abuja, which averages around 5.5 peak sun hours daily, produces roughly 1,650 watt-hours (1.65 kWh) per day under good conditions, not 300 watts times 24 hours. Dust accumulation from harmattan season, common across much of Northern Nigeria, can reduce output by 10 to 25 percent if panels are not cleaned regularly. A credible energy assessment always uses local peak sun hour data and realistic derating factors, never the panel's laboratory-rated number, when estimating how much electricity a system will actually generate.</p>",
            "key_concepts": [
                "Photovoltaic effect",
                "Direct current electricity",
                "Peak sun hours",
                "Panel derating factors",
                "Dust and temperature losses"
            ],
            "practical_exercise": {
                "title": "Estimate Realistic Panel Output",
                "instructions": "Using an assumed peak sun hour figure of 5 hours per day for your region, calculate the realistic daily energy output in kWh for a 250W solar panel. Then explain in two to three sentences one local environmental factor, such as dust, rain season, or shading, that could reduce this output further."
            },
            "quiz": [
                {
                    "question": "What is the photovoltaic effect?",
                    "options": [
                        "The process by which batteries store energy",
                        "A method for cleaning solar panels",
                        "The process by which sunlight is converted into direct current electricity in solar cells",
                        "The conversion of wind into electricity"
                    ],
                    "correct_index": 2,
                    "explanation": "The photovoltaic effect describes how sunlight striking a solar cell generates electric current."
                },
                {
                    "question": "Why do professionals use peak sun hours instead of total daylight hours to estimate output?",
                    "options": [
                        "Peak sun hours are always exactly 12",
                        "Peak sun hours only apply to wind turbines",
                        "Daylight hours are impossible to measure",
                        "Sunlight intensity varies throughout the day, so peak sun hours represent equivalent hours of full-intensity output"
                    ],
                    "correct_index": 3,
                    "explanation": "Peak sun hours account for varying sunlight intensity, giving a more realistic output estimate than raw daylight hours."
                },
                {
                    "question": "What is one reason a solar panel's real-world output is usually lower than its rated capacity?",
                    "options": [
                        "Factors like dust, heat, and cloud cover reduce actual output below laboratory conditions",
                        "Panels are rated below their true capability",
                        "Rated capacity already includes all losses",
                        "Real-world output is always higher than rated capacity"
                    ],
                    "correct_index": 0,
                    "explanation": "Environmental factors such as dust, heat, and shading typically reduce a panel's real output below its lab-rated peak."
                }
            ],
            "resources": [
                {
                    "label": "IRENA - Solar Energy",
                    "url": "https://www.irena.org/Energy-Transition/Technology/Solar-energy"
                }
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Energy Access and Renewable Fundamentals",
            "title": "Batteries and Inverters: Storing and Converting Solar Energy for Use",
            "learning_objective": "By the end of this class, you will be able to explain the roles of batteries and inverters in a solar power system and describe key differences between battery types.",
            "duration_minutes": 25,
            "content_html": "<p>Solar panels only produce electricity when the sun is shining, but people need power at night and during cloudy periods, which is why batteries and inverters are just as important to a working system as the panels themselves. Getting these components wrong is one of the most common reasons off-grid systems fail within their first year.</p><h2>Storage and Conversion</h2><p>Batteries store the DC electricity generated during the day so it can be used later, while an inverter converts stored DC electricity into alternating current (AC), the type of power most household appliances and business equipment actually use. Two common battery technologies dominate the African market: lead-acid batteries, which are cheaper upfront but have a shorter lifespan and cannot be drained below about 50 percent without damage, and lithium-ion batteries, which cost more initially but last longer, tolerate deeper discharge, and require less maintenance.</p><h2>Worked Example</h2><p>A small clinic in rural Ogun State needs 5 kWh of backup power to run essential equipment overnight. If the clinic uses lead-acid batteries, it must actually install roughly 10 kWh of battery capacity, since only half can safely be used, while a lithium-ion system might need only about 6 kWh installed to deliver the same usable 5 kWh. This difference directly affects both the upfront cost and the physical space needed for batteries, which is exactly the kind of trade-off a feasibility study must explain clearly to whoever is paying for the system.</p>",
            "key_concepts": [
                "Battery storage",
                "DC to AC inverter conversion",
                "Lead-acid vs lithium-ion batteries",
                "Depth of discharge",
                "Usable vs installed capacity"
            ],
            "practical_exercise": {
                "title": "Compare Battery Options for a Scenario",
                "instructions": "Using the clinic example from today's class, write a short comparison recommending either lead-acid or lithium-ion batteries for a small rural health facility that needs 5 kWh of usable backup power nightly. Justify your recommendation using cost, depth of discharge, and maintenance considerations."
            },
            "quiz": [
                {
                    "question": "What is the main function of an inverter in a solar power system?",
                    "options": [
                        "To generate electricity directly from sunlight",
                        "To convert stored DC electricity into AC electricity for appliance use",
                        "To clean dust off solar panels",
                        "To measure daily peak sun hours"
                    ],
                    "correct_index": 1,
                    "explanation": "An inverter converts the DC electricity stored in batteries into the AC power most appliances require."
                },
                {
                    "question": "Why can lead-acid batteries typically only be used down to about 50 percent capacity?",
                    "options": [
                        "It is a government regulation with no technical basis",
                        "They stop producing power below 50 percent",
                        "Discharging them further damages the battery and shortens its lifespan",
                        "Lead-acid batteries cannot store more than 50 percent to begin with"
                    ],
                    "correct_index": 2,
                    "explanation": "Deep discharge below roughly 50 percent damages lead-acid batteries and reduces their usable lifespan."
                },
                {
                    "question": "Compared to lead-acid, what is a key advantage of lithium-ion batteries?",
                    "options": [
                        "They are always cheaper upfront",
                        "They do not require an inverter",
                        "They cannot be used in off-grid systems",
                        "They tolerate deeper discharge and generally last longer with less maintenance"
                    ],
                    "correct_index": 3,
                    "explanation": "Lithium-ion batteries typically last longer and allow deeper safe discharge than lead-acid batteries, despite higher upfront cost."
                }
            ],
            "resources": []
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Energy Access and Renewable Fundamentals",
            "title": "Comparing Solar, Wind, Hydro, and Biomass for African Contexts",
            "learning_objective": "By the end of this class, you will be able to match a renewable energy source to a specific African geographic and economic context.",
            "duration_minutes": 25,
            "content_html": "<p>Solar dominates renewable energy conversations in Africa, but a credible energy professional knows when solar is not actually the best option, and being able to justify that choice with local context is exactly the kind of judgment that impresses employers and clients.</p><h2>The Main Renewable Sources</h2><p>Solar energy works almost anywhere with reasonable sunlight and needs little site-specific infrastructure, making it the default choice for most small to mid-sized off-grid projects. Wind energy requires consistently strong wind speeds, found in specific corridors like parts of Northern Nigeria and coastal East Africa, and usually needs larger upfront investment. Hydropower, from large dams to small run-of-river systems, works well near flowing water and can provide steady, predictable power but depends heavily on rainfall patterns and environmental approval. Biomass, generated from agricultural or organic waste, suits areas with abundant crop residue or livestock waste and can double as a waste management solution.</p><h2>Worked Example</h2><p>A rice-processing community in Kebbi State generates large volumes of rice husk waste every season. Rather than defaulting to solar, a well-reasoned feasibility study might recommend a small biomass gasification system that both generates power and solves a waste disposal problem, creating value from what would otherwise be burned or dumped. Choosing the right technology for the actual resource available on site, not just the most talked-about option, is a core professional skill this track builds throughout the following weeks.</p>",
            "key_concepts": [
                "Solar suitability",
                "Wind energy requirements",
                "Hydropower and run-of-river systems",
                "Biomass and waste-to-energy",
                "Matching technology to local resources"
            ],
            "practical_exercise": {
                "title": "Justify a Renewable Technology Choice",
                "instructions": "Pick a specific African location you know or can research, such as your home state or town. Based on its geography and economic activities, recommend one renewable energy source (solar, wind, hydro, or biomass) as most appropriate and write a short paragraph justifying your choice using local resource availability."
            },
            "quiz": [
                {
                    "question": "Why might biomass be a strong option for a rice-processing community?",
                    "options": [
                        "It uses abundant rice husk waste as fuel while also solving a waste disposal problem",
                        "Biomass only works in coastal areas",
                        "Biomass is always cheaper than solar everywhere",
                        "Biomass requires no local resources at all"
                    ],
                    "correct_index": 0,
                    "explanation": "Biomass systems can turn locally abundant organic waste, like rice husks, into both power and a waste management solution."
                },
                {
                    "question": "What is a key requirement for wind energy to be viable at a site?",
                    "options": [
                        "Year-round rainfall",
                        "Consistently strong and reliable wind speeds",
                        "Proximity to a river",
                        "Large amounts of agricultural waste"
                    ],
                    "correct_index": 1,
                    "explanation": "Wind power requires locations with consistently strong wind resources to be economically viable."
                },
                {
                    "question": "Why is solar often the default choice for small off-grid projects across Africa?",
                    "options": [
                        "It always produces more energy than any other source",
                        "It requires no maintenance at all",
                        "It works in most locations with reasonable sunlight and needs less site-specific infrastructure",
                        "It is the only renewable source recognized internationally"
                    ],
                    "correct_index": 2,
                    "explanation": "Solar's flexibility and lower site-specific infrastructure needs make it a practical default for many small off-grid projects."
                }
            ],
            "resources": [
                {
                    "label": "IRENA - Technology",
                    "url": "https://www.irena.org/Energy-Transition/Technology"
                }
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Systems, Economics, and Sustainability Concepts",
            "title": "Off-Grid, On-Grid, and Mini-Grid Systems Explained",
            "learning_objective": "By the end of this class, you will be able to distinguish between off-grid, on-grid, and mini-grid systems and identify which suits a given scenario.",
            "duration_minutes": 25,
            "content_html": "<p>Not every renewable energy project looks the same, and one of the most common mistakes beginners make is assuming solar always means a single household with a small panel on the roof. Understanding the three main system architectures is essential for correctly scoping any project you assess in this course.</p><h2>The Three System Types</h2><p>An off-grid (standalone) system serves a single household or business with no connection to any larger network, ideal for isolated locations. An on-grid (grid-tied) system connects directly to the national electricity grid, allowing excess solar generation to be fed back or supplemented by grid power, common in urban areas with unreliable but present grid access. A mini-grid is a localized network that generates and distributes power to multiple households or businesses within a community, operating independently of the national grid, and is one of the fastest-growing solutions for rural electrification across Nigeria and East Africa.</p><h2>Worked Example</h2><p>A cluster of 150 households in a rural community with no existing grid connection is a strong candidate for a mini-grid, since a shared generation and distribution system spreads the cost of panels, batteries, and inverters across many customers, lowering the price per household. A single house in Lagos experiencing frequent blackouts, but still connected to the national grid, is better served by an on-grid hybrid system that reduces generator use and grid dependency without needing a standalone distribution network. Matching the right architecture to the right scenario is a question that shows up constantly in real feasibility work and job interviews alike.</p>",
            "key_concepts": [
                "Off-grid systems",
                "On-grid (grid-tied) systems",
                "Mini-grid architecture",
                "Shared infrastructure cost",
                "Rural electrification"
            ],
            "practical_exercise": {
                "title": "Classify Three Energy Scenarios",
                "instructions": "Write three short scenarios of your own, one that clearly fits an off-grid system, one that fits an on-grid system, and one that fits a mini-grid, using realistic Nigerian or African settings. For each, explain in one sentence why that system type is the correct fit."
            },
            "quiz": [
                {
                    "question": "What defines a mini-grid?",
                    "options": [
                        "A single household system with no distribution network",
                        "A backup generator used during blackouts",
                        "A grid-tied system connected only to one building",
                        "A localized network generating and distributing power to multiple households or businesses, independent of the national grid"
                    ],
                    "correct_index": 3,
                    "explanation": "A mini-grid serves multiple customers within a community through its own local generation and distribution network."
                },
                {
                    "question": "Why is a mini-grid often more cost-effective per household than individual off-grid systems?",
                    "options": [
                        "The generation and distribution costs are shared across many customers",
                        "Mini-grids never require batteries",
                        "Mini-grids are funded entirely by government subsidies",
                        "Each household pays the full system cost individually"
                    ],
                    "correct_index": 0,
                    "explanation": "Spreading shared infrastructure costs across many households lowers the effective cost per customer in a mini-grid."
                },
                {
                    "question": "Which system type is best suited to a single Lagos home with unreliable but present grid access?",
                    "options": [
                        "A rural mini-grid",
                        "An on-grid hybrid system that supplements grid power",
                        "An off-grid standalone system only",
                        "No renewable system is appropriate"
                    ],
                    "correct_index": 1,
                    "explanation": "An on-grid hybrid system can reduce reliance on unreliable grid power and generators without building a separate distribution network."
                }
            ],
            "resources": []
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Systems, Economics, and Sustainability Concepts",
            "title": "The Economics of Renewable Energy: LCOE and Payback Period",
            "learning_objective": "By the end of this class, you will be able to calculate a simple payback period for a renewable energy investment.",
            "duration_minutes": 25,
            "content_html": "<p>A brilliant technical design means nothing to a funder or business owner if the numbers do not make financial sense. Learning to speak in terms of cost per unit of energy and time to recover an investment is what turns a technical idea into something a bank, investor, or client will actually approve.</p><h2>Two Core Financial Concepts</h2><p>The Levelized Cost of Energy (LCOE) represents the average cost per kWh of electricity produced by a system over its entire lifetime, accounting for upfront installation cost, maintenance, and total energy generated. It allows fair comparison between different energy options, such as solar versus diesel, on a like-for-like basis. The payback period is simpler: it is the time it takes for the savings or revenue generated by a system to equal its initial cost, calculated by dividing total system cost by annual savings or income.</p><h2>Worked Example</h2><p>A small business spends 600,000 naira installing a solar system that replaces a diesel generator, saving the business 15,000 naira per month in fuel costs, or 180,000 naira annually. The payback period is 600,000 divided by 180,000, which equals roughly 3.3 years. If the solar system is expected to last 20 years, the business enjoys over 16 years of essentially free energy after payback, a compelling number to put in front of a business owner deciding whether the upfront cost is worth it.</p>",
            "key_concepts": [
                "Levelized Cost of Energy (LCOE)",
                "Payback period",
                "Upfront cost vs long-term savings",
                "Comparing energy options financially",
                "Investment justification"
            ],
            "practical_exercise": {
                "title": "Calculate a Payback Period",
                "instructions": "Using a system cost of 800,000 naira and estimated monthly savings of 20,000 naira from reduced diesel use, calculate the payback period in years. Then write two to three sentences explaining whether you would recommend this investment to a small business owner, and why."
            },
            "quiz": [
                {
                    "question": "What does the payback period measure?",
                    "options": [
                        "The total lifetime energy output of a system",
                        "The number of solar panels needed",
                        "The time required for savings or revenue to equal the system's initial cost",
                        "The percentage of energy lost to inefficiency"
                    ],
                    "correct_index": 2,
                    "explanation": "The payback period tells you how long it takes for accumulated savings to cover the upfront investment cost."
                },
                {
                    "question": "What does LCOE allow you to do?",
                    "options": [
                        "Measure only the upfront cost of a system",
                        "Determine peak sun hours for a region",
                        "Calculate battery depth of discharge",
                        "Fairly compare the average cost per kWh across different energy sources over their lifetime"
                    ],
                    "correct_index": 3,
                    "explanation": "LCOE standardizes cost per unit of energy across different technologies and lifespans, enabling fair comparison."
                },
                {
                    "question": "In the worked example, what was the approximate payback period for the 600,000 naira solar system?",
                    "options": [
                        "About 3.3 years",
                        "10 years",
                        "1 year",
                        "20 years"
                    ],
                    "correct_index": 0,
                    "explanation": "Dividing 600,000 naira by 180,000 naira in annual savings gives a payback period of roughly 3.3 years."
                }
            ],
            "resources": [
                {
                    "label": "Investopedia - Payback Period",
                    "url": "https://www.investopedia.com"
                }
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Systems, Economics, and Sustainability Concepts",
            "title": "Carbon Footprint and Emissions: Measuring Environmental Impact",
            "learning_objective": "By the end of this class, you will be able to explain what a carbon footprint is and estimate emissions avoided by a renewable energy switch.",
            "duration_minutes": 25,
            "content_html": "<p>Sustainability work is not only about installing clean technology, it is about proving, with numbers, the environmental difference that technology makes. Employers and funders increasingly expect reports to quantify environmental impact, not just describe it in general terms.</p><h2>Understanding Carbon Footprint</h2><p>A carbon footprint is the total amount of greenhouse gases, primarily carbon dioxide, produced directly or indirectly by an activity, organization, or individual, usually measured in kilograms or tonnes of CO2 equivalent. Emissions from burning diesel or petrol for backup power are a major contributor for many African households and businesses, since generators are common where grid access is unreliable. When a business or community switches from diesel to solar, the emissions avoided can be estimated using standard fuel-to-CO2 conversion factors.</p><h2>Worked Example</h2><p>A generator burning one liter of diesel produces roughly 2.68 kg of CO2. A small business using 20 liters of diesel weekly for backup power produces about 53.6 kg of CO2 per week, or roughly 2,787 kg (nearly 2.8 tonnes) annually. If that business switches to a solar-battery system covering the same backup load, it avoids close to 2.8 tonnes of CO2 emissions each year, a figure worth including in any sustainability report because it converts an abstract environmental benefit into a concrete, comparable number that funders and corporate sustainability teams can act on.</p>",
            "key_concepts": [
                "Carbon footprint",
                "CO2 equivalent",
                "Emissions from diesel generators",
                "Fuel-to-CO2 conversion factors",
                "Quantifying environmental impact"
            ],
            "practical_exercise": {
                "title": "Estimate Avoided Emissions",
                "instructions": "Using the conversion factor of 2.68 kg of CO2 per liter of diesel, calculate the annual emissions avoided if a household currently using 10 liters of diesel weekly switches entirely to solar power. Show your calculation and express the final answer in kilograms of CO2 avoided per year."
            },
            "quiz": [
                {
                    "question": "What is a carbon footprint?",
                    "options": [
                        "The physical size of a solar panel installation",
                        "The total greenhouse gases produced directly or indirectly by an activity, organization, or individual",
                        "The number of years a battery lasts",
                        "A measure of how much sunlight a region receives"
                    ],
                    "correct_index": 1,
                    "explanation": "A carbon footprint quantifies total greenhouse gas emissions associated with an activity or entity, usually in CO2 equivalent."
                },
                {
                    "question": "Roughly how much CO2 does burning one liter of diesel produce?",
                    "options": [
                        "0.5 kg",
                        "10 kg",
                        "2.68 kg",
                        "100 kg"
                    ],
                    "correct_index": 2,
                    "explanation": "A commonly used conversion factor estimates about 2.68 kg of CO2 emitted per liter of diesel burned."
                },
                {
                    "question": "Why is it valuable to convert avoided emissions into a specific number like tonnes of CO2?",
                    "options": [
                        "It has no practical value in reports",
                        "Numbers are less persuasive than general statements",
                        "It is required only for wind energy projects",
                        "It turns an abstract environmental benefit into a concrete, comparable figure funders and businesses can act on"
                    ],
                    "correct_index": 3,
                    "explanation": "Specific emissions figures make environmental impact measurable and comparable, which strengthens sustainability reports and funding cases."
                }
            ],
            "resources": [
                {
                    "label": "UN Sustainable Development Goals",
                    "url": "https://www.un.org/sustainabledevelopment"
                }
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Systems, Economics, and Sustainability Concepts",
            "title": "The Triple Bottom Line: Balancing People, Planet, and Profit",
            "learning_objective": "By the end of this class, you will be able to evaluate a business decision using the triple bottom line framework of people, planet, and profit.",
            "duration_minutes": 25,
            "content_html": "<p>Sustainability is often mistaken for a purely environmental concern, but the professionals who get hired and promoted in this field understand that a truly sustainable decision must also work socially and financially, not just environmentally. This is the core idea behind one of the most widely used frameworks in the field.</p><h2>People, Planet, Profit</h2><p>The triple bottom line framework evaluates decisions across three dimensions: people (social impact, such as jobs created, health, and community wellbeing), planet (environmental impact, such as emissions, waste, and resource use), and profit (financial viability and economic sustainability). A project that helps the planet but bankrupts the people running it is not sustainable, and neither is a highly profitable project that damages the community or environment it operates in. Real sustainability work means finding decisions that score reasonably well across all three.</p><h2>Worked Example</h2><p>A textile company in Aba considers two options to cut costs: laying off workers to reduce wages, or investing in energy-efficient machinery and solar power to cut electricity bills. The layoff option improves profit but damages the people dimension by harming livelihoods and community trust. The energy-efficiency option requires upfront investment but improves the planet dimension through lower emissions, protects the people dimension by preserving jobs, and still improves profit over time through lower energy costs. A sustainability consultant's job is exactly this kind of comparison, showing decision-makers the option that performs well across all three dimensions rather than sacrificing two for one.</p>",
            "key_concepts": [
                "Triple bottom line",
                "Social impact (people)",
                "Environmental impact (planet)",
                "Financial viability (profit)",
                "Balanced sustainable decision-making"
            ],
            "practical_exercise": {
                "title": "Apply the Triple Bottom Line",
                "instructions": "Think of a business or organization you know. Describe one decision it could make and evaluate it across the three dimensions of people, planet, and profit, noting whether the decision scores positively, negatively, or neutrally on each. Conclude with one sentence on whether you consider it a sustainable decision overall."
            },
            "quiz": [
                {
                    "question": "What are the three dimensions of the triple bottom line?",
                    "options": [
                        "People, planet, and profit",
                        "Cost, quality, and speed",
                        "Marketing, sales, and operations",
                        "Energy, water, and waste"
                    ],
                    "correct_index": 0,
                    "explanation": "The triple bottom line evaluates social impact (people), environmental impact (planet), and financial viability (profit)."
                },
                {
                    "question": "Why is a highly profitable project that damages its community not considered truly sustainable?",
                    "options": [
                        "Profit is the only dimension that matters",
                        "It fails the people dimension of the triple bottom line, even though it succeeds financially",
                        "Community damage always increases profit further",
                        "Sustainability only concerns environmental factors"
                    ],
                    "correct_index": 1,
                    "explanation": "True sustainability requires reasonable performance across people, planet, and profit, not just financial success."
                },
                {
                    "question": "In the Aba textile company example, why was investing in energy efficiency considered the more sustainable choice?",
                    "options": [
                        "It only improved profit and ignored the other dimensions",
                        "It required no upfront investment at all",
                        "It balanced improvements in environmental impact, job preservation, and long-term cost savings",
                        "It had no effect on any of the three dimensions"
                    ],
                    "correct_index": 2,
                    "explanation": "The energy-efficiency option improved or preserved outcomes across people, planet, and profit rather than sacrificing one for another."
                }
            ],
            "resources": []
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Systems, Economics, and Sustainability Concepts",
            "title": "Reading a Household or Business Energy Bill and Spotting Waste",
            "learning_objective": "By the end of this class, you will be able to read a basic electricity bill and identify at least two opportunities to reduce energy waste.",
            "duration_minutes": 25,
            "content_html": "<p>Before recommending solar panels or a sustainability program, a good energy professional first checks whether the customer is simply wasting energy that could be saved for free or at low cost. Energy efficiency is almost always cheaper than adding more generation capacity, and spotting it builds trust with a client before you ever propose a bigger investment.</p><h2>What to Look For</h2><p>A typical Nigerian electricity bill or estimated usage record shows units consumed in kWh, a tariff rate per unit, and sometimes a fixed service charge. Comparing consumption month to month can reveal spikes worth investigating, while a simple walk-through of a home or business often reveals waste: old incandescent bulbs instead of LEDs, appliances left on standby, fridges with worn door seals working harder than necessary, or air conditioning units running with doors and windows open.</p><h2>Worked Example</h2><p>A small salon in Ibadan pays for 400 kWh a month, largely driven by four old incandescent bulbs left on for 10 hours daily and an aging fridge with a poor door seal. Replacing the bulbs with 10W LED equivalents alone could cut roughly 1.6 kWh per day, about 48 kWh monthly, while servicing the fridge seal could meaningfully reduce its compressor runtime. Identifying savings like these before proposing solar means the eventual solar system can be sized smaller and cheaper, since it only needs to cover a genuinely efficient load, not a wasteful one.</p>",
            "key_concepts": [
                "Reading an electricity bill",
                "Energy efficiency audit",
                "Common sources of energy waste",
                "LED versus incandescent lighting",
                "Efficiency before generation"
            ],
            "practical_exercise": {
                "title": "Conduct a Mini Waste Walk-Through",
                "instructions": "Walk through your own home or a business you have access to and list three specific sources of energy waste you observe, such as inefficient bulbs, appliances left running unnecessarily, or poor insulation. For each, suggest one concrete fix and estimate roughly how much energy or cost it might save per month."
            },
            "quiz": [
                {
                    "question": "Why is checking for energy efficiency important before recommending a solar system?",
                    "options": [
                        "Efficiency has no impact on system sizing",
                        "Efficiency checks are only relevant for large industrial facilities",
                        "Solar systems automatically fix all energy waste",
                        "Reducing waste first can allow a smaller, cheaper solar system to meet the same needs"
                    ],
                    "correct_index": 3,
                    "explanation": "Cutting waste lowers the load a solar system must cover, often reducing the size and cost of the recommended system."
                },
                {
                    "question": "Which of these is a common source of energy waste in homes and small businesses?",
                    "options": [
                        "Old incandescent bulbs left on for long hours",
                        "Using LED bulbs",
                        "Turning off unused appliances",
                        "Servicing fridge door seals regularly"
                    ],
                    "correct_index": 0,
                    "explanation": "Incandescent bulbs consume significantly more energy than LEDs and are a frequent, easily fixed source of waste."
                },
                {
                    "question": "In the salon example, what two issues were identified as sources of waste?",
                    "options": [
                        "Solar panel misalignment and battery age",
                        "Old incandescent bulbs and a fridge with a poor door seal",
                        "High tariff rates and inverter inefficiency",
                        "Overuse of air conditioning only"
                    ],
                    "correct_index": 1,
                    "explanation": "The salon example highlighted inefficient lighting and a poorly sealed fridge as key sources of avoidable energy waste."
                }
            ],
            "resources": []
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Assessing Real-World Energy Needs",
            "title": "Conducting a Community Energy Needs Assessment",
            "learning_objective": "By the end of this class, you will be able to design a basic energy needs assessment for a community.",
            "duration_minutes": 30,
            "content_html": "<p>Every credible mini-grid or off-grid project begins with a structured needs assessment, not a guess about what a community wants. Skipping this step is one of the most common reasons rural electrification projects fail to reach their promised impact or financial targets.</p><h2>What a Needs Assessment Covers</h2><p>A community energy needs assessment typically gathers population and household count, current energy sources and monthly spending on them, existing or planned productive uses of electricity such as milling machines, welding, or cold storage, willingness and ability to pay for a new service, and any local infrastructure like schools, clinics, or markets that could anchor early demand. This data comes from household surveys, interviews with local leaders, and site visits, not assumptions made from an office.</p><h2>Worked Example</h2><p>An assessment team visiting a farming community of 300 households in Benue State finds that most households currently spend around 3,500 naira monthly on kerosene and phone charging, a local grinding mill operator wants electricity to replace an expensive diesel engine, and the community clinic needs reliable power for vaccine refrigeration. This information immediately suggests the mini-grid should be sized not just for household lighting, but for the grinding mill's motor load and the clinic's refrigeration needs, both of which represent steady, high-value demand that improves the project's financial viability far beyond household lighting alone.</p>",
            "key_concepts": [
                "Community needs assessment",
                "Household energy survey",
                "Productive use of electricity",
                "Anchor demand",
                "Willingness and ability to pay"
            ],
            "practical_exercise": {
                "title": "Draft a Needs Assessment Survey",
                "instructions": "Write eight to ten survey questions you would ask households and local businesses to assess energy needs in a community, covering current energy spending, appliance ownership, willingness to pay, and any productive uses of electricity. Organize the questions into a clean numbered list."
            },
            "quiz": [
                {
                    "question": "Why is anchor demand, such as a grinding mill or clinic, valuable to identify during a needs assessment?",
                    "options": [
                        "It has no effect on project viability",
                        "Anchor demand only matters for wind projects",
                        "It represents steady, higher-value electricity demand that improves the financial case for a mini-grid",
                        "It is used solely to reduce battery costs"
                    ],
                    "correct_index": 2,
                    "explanation": "Anchor loads like mills or clinics provide consistent, significant demand that strengthens the financial viability of a mini-grid."
                },
                {
                    "question": "What is the main purpose of a community energy needs assessment?",
                    "options": [
                        "To sell solar panels directly to households",
                        "To calculate carbon emissions only",
                        "To install batteries without any prior planning",
                        "To gather real data on current energy use, spending, and demand before designing a project"
                    ],
                    "correct_index": 3,
                    "explanation": "A needs assessment collects real ground-level data that shapes an accurate, appropriate project design."
                },
                {
                    "question": "Which of these is a reliable source of needs assessment data?",
                    "options": [
                        "Household surveys, leader interviews, and site visits",
                        "Assumptions made without visiting the community",
                        "Only national census data from a decade ago",
                        "Guesses based on similar projects elsewhere"
                    ],
                    "correct_index": 0,
                    "explanation": "Direct surveys, interviews, and site visits provide the accurate, current data needed for a credible needs assessment."
                }
            ],
            "resources": []
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Assessing Real-World Energy Needs",
            "title": "Sizing a Solar System: Panels, Batteries, and Inverter Calculations",
            "learning_objective": "By the end of this class, you will be able to calculate the basic panel, battery, and inverter sizing for a given daily energy load.",
            "duration_minutes": 30,
            "content_html": "<p>This is the calculation every solar professional is expected to do confidently: turning a daily energy load into an actual list of equipment. Getting this right on day 12 gives you the technical backbone needed for your capstone feasibility study later in the course.</p><h2>The Sizing Process</h2><p>Start with the daily load in kWh, then divide by local peak sun hours to estimate the required panel capacity in kW, adding a buffer of about 20 to 30 percent for system losses and cloudy days. For battery sizing, decide how many days of autonomy (backup with no sun) are needed, multiply the daily load by that number, then adjust for the battery type's usable depth of discharge. The inverter must be rated to handle the maximum simultaneous power draw of all appliances running at once, not just the average load.</p><h2>Worked Example</h2><p>A household with a 3 kWh daily load, located in a region with 5 peak sun hours, needs roughly 3 divided by 5, or 0.6 kW of panels before buffer, adjusted upward to about 0.75 kW (750W) after adding a 25 percent buffer. For one day of autonomy using lithium batteries with 90 percent usable depth of discharge, battery capacity needed is roughly 3 kWh divided by 0.9, about 3.3 kWh. If the highest simultaneous load, such as a fridge and several lights running together, is 400W, an inverter rated at least 500 to 600W is chosen to safely handle that peak with headroom.</p>",
            "key_concepts": [
                "Panel sizing from daily load",
                "System loss buffer",
                "Days of autonomy",
                "Depth of discharge adjustment",
                "Inverter peak load rating"
            ],
            "practical_exercise": {
                "title": "Size a Complete Solar System",
                "instructions": "Using a daily load of 4 kWh, 5 peak sun hours, one day of battery autonomy, and lithium batteries with 90 percent usable depth of discharge, calculate the required panel capacity in watts, battery capacity in kWh, and a reasonable inverter rating assuming a 500W peak simultaneous load. Show each calculation step."
            },
            "quiz": [
                {
                    "question": "Why is a buffer of 20 to 30 percent typically added when sizing solar panels?",
                    "options": [
                        "To make the system more expensive for no reason",
                        "To account for system losses, cloudy days, and other real-world inefficiencies",
                        "Buffers are not standard practice in solar sizing",
                        "It compensates for battery depth of discharge only"
                    ],
                    "correct_index": 1,
                    "explanation": "The buffer accounts for real-world losses and variable weather conditions that reduce actual system performance below theoretical calculations."
                },
                {
                    "question": "What should determine the inverter's power rating?",
                    "options": [
                        "The average daily load only",
                        "The total number of solar panels installed",
                        "The maximum simultaneous power draw of all appliances running at once",
                        "The battery's depth of discharge percentage"
                    ],
                    "correct_index": 2,
                    "explanation": "An inverter must handle peak simultaneous demand, not just average load, to avoid overload when multiple appliances run together."
                },
                {
                    "question": "What does days of autonomy refer to in battery sizing?",
                    "options": [
                        "The number of days a solar panel lasts before replacement",
                        "The warranty period of an inverter",
                        "The number of days needed to install a system",
                        "The number of days a battery system can supply power with no solar input"
                    ],
                    "correct_index": 3,
                    "explanation": "Days of autonomy is the backup duration a battery bank can provide without any solar charging, used to size battery capacity."
                }
            ],
            "resources": []
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Assessing Real-World Energy Needs",
            "title": "Case Study: How Nigerian Solar Mini-Grids Power Rural Communities",
            "learning_objective": "By the end of this class, you will be able to identify the key success factors behind a real-world mini-grid deployment.",
            "duration_minutes": 25,
            "content_html": "<p>Studying real deployments teaches lessons no textbook formula can, because it shows how technical design, financing, and community dynamics interact in practice. Nigeria has become one of the largest mini-grid markets in Africa, offering many real examples to learn from.</p><h2>What Makes These Projects Work</h2><p>Successful Nigerian mini-grid projects, often supported by programs under the Rural Electrification Agency, typically combine solar generation with battery storage, a smart metering system that lets customers pay as they use power (often via mobile money), and a clear tariff structure that covers operating costs while remaining affordable relative to what households previously spent on kerosene and diesel. Community engagement before construction, explaining costs, benefits, and expected reliability, is consistently cited as a factor separating successful projects from ones that face resistance or non-payment.</p><h2>Worked Example</h2><p>In several documented Nigerian mini-grid deployments, developers found that communities were often already spending more on diesel generator fuel and phone charging trips than the proposed mini-grid tariff would cost, which became the central argument used to win community buy-in and secure initial customer commitments before construction began. Projects that skipped this engagement step and simply built first sometimes faced low uptake, because residents did not trust the pricing or did not understand how the pay-as-you-go metering worked. This case shows that technical design alone does not guarantee success, the business model and community trust matter just as much.</p>",
            "key_concepts": [
                "Rural Electrification Agency",
                "Pay-as-you-go metering",
                "Mobile money payment",
                "Tariff design",
                "Community engagement before construction"
            ],
            "practical_exercise": {
                "title": "Analyze Mini-Grid Success Factors",
                "instructions": "Based on today's case study, list three specific factors that contribute to a successful mini-grid deployment and three risks that could cause one to fail. For each risk, suggest one mitigation strategy a developer could use."
            },
            "quiz": [
                {
                    "question": "What role does pay-as-you-go metering play in many Nigerian mini-grid projects?",
                    "options": [
                        "It allows customers to pay for electricity as they use it, often via mobile money, improving affordability and revenue collection",
                        "It prevents any customer from using electricity on credit",
                        "It eliminates the need for any tariff structure",
                        "It only applies to grid-tied systems, not mini-grids"
                    ],
                    "correct_index": 0,
                    "explanation": "Pay-as-you-go metering makes electricity payments flexible and manageable for customers while helping developers collect revenue reliably."
                },
                {
                    "question": "Why is community engagement before construction considered critical to project success?",
                    "options": [
                        "It has no measurable effect on project outcomes",
                        "It builds trust and understanding around pricing and service, reducing resistance and non-payment later",
                        "Engagement is only required for grid-tied projects",
                        "It replaces the need for a needs assessment"
                    ],
                    "correct_index": 1,
                    "explanation": "Early community engagement builds the trust needed for residents to accept tariffs and adopt the new service, reducing later resistance."
                },
                {
                    "question": "What comparison did successful mini-grid developers use to win community buy-in?",
                    "options": [
                        "Comparing mini-grid tariffs to the cost of solar panels alone",
                        "Comparing mini-grid tariffs to national grid electricity prices only",
                        "Comparing mini-grid tariffs to what households already spent on diesel and phone charging",
                        "Comparing installation time to that of grid extension projects"
                    ],
                    "correct_index": 2,
                    "explanation": "Showing that mini-grid costs were comparable to or lower than existing diesel and charging expenses was a persuasive, concrete argument for adoption."
                }
            ],
            "resources": [
                {
                    "label": "IRENA - Off-grid Renewables",
                    "url": "https://www.irena.org/Energy-Transition/Technology/Off-grid-renewables"
                }
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Assessing Real-World Energy Needs",
            "title": "Financing Renewable Projects: Pay-As-You-Go, Grants, and Microfinance",
            "learning_objective": "By the end of this class, you will be able to compare at least three financing models used for renewable energy projects in Africa.",
            "duration_minutes": 25,
            "content_html": "<p>Even a perfectly designed solar system is worthless if nobody can afford the upfront cost, which is why financing structure is often the deciding factor in whether a renewable energy project actually reaches the people who need it.</p><h2>Common Financing Models</h2><p>Pay-as-you-go (PAYG) financing lets customers pay in small installments, often through mobile money, for a solar home system they use immediately and eventually own outright, spreading a large upfront cost into affordable regular payments. Grant funding, typically from governments, development banks, or NGOs, covers part or all of a project's cost, often used for public infrastructure like clinics and schools where recovering costs from users is impractical. Microfinance loans, provided by community banks or microfinance institutions, let individuals or small businesses borrow specifically for productive energy investments, such as a shop owner financing a solar-powered freezer for cold drinks sales.</p><h2>Worked Example</h2><p>A tailor in Kano wants a solar system to power sewing machines and lighting, costing 250,000 naira upfront, an amount she cannot pay at once. Through a PAYG arrangement, she instead pays 8,000 naira monthly for three years through her mobile phone, a manageable amount compared to what she previously spent on generator fuel and phone charging combined. Meanwhile, a rural primary health center in the same state, which generates no direct revenue from patients, is far better suited to grant funding from a development partner, since it has no realistic way to repay a commercial loan through user fees.</p>",
            "key_concepts": [
                "Pay-as-you-go financing",
                "Grant funding",
                "Microfinance loans",
                "Matching financing to revenue model",
                "Affordability structuring"
            ],
            "practical_exercise": {
                "title": "Match Financing Models to Scenarios",
                "instructions": "Write three short scenarios, one household, one small business, and one public facility like a school or clinic, each needing a solar system. For each, recommend the most appropriate financing model (PAYG, grant, or microfinance) and justify your choice in two to three sentences."
            },
            "quiz": [
                {
                    "question": "Why is grant funding often the best fit for public facilities like rural clinics?",
                    "options": [
                        "Clinics generate high revenue that easily repays commercial loans",
                        "Grants require higher upfront costs than PAYG",
                        "Grants are the only financing option that exists",
                        "Clinics typically cannot recover costs from patients, making loan repayment impractical"
                    ],
                    "correct_index": 3,
                    "explanation": "Since clinics often cannot charge patients enough to repay a loan, grant funding is usually more appropriate than commercial financing."
                },
                {
                    "question": "What is the main advantage of pay-as-you-go financing for a household or small business?",
                    "options": [
                        "It spreads a large upfront cost into smaller, manageable payments, often via mobile money",
                        "It requires the full cost to be paid upfront",
                        "It eliminates the need for any solar equipment",
                        "It is only available to large corporations"
                    ],
                    "correct_index": 0,
                    "explanation": "PAYG makes solar systems accessible by breaking the cost into affordable installments paid over time."
                },
                {
                    "question": "Microfinance loans for renewable energy are typically best suited to which use case?",
                    "options": [
                        "Household lighting with no income generation",
                        "Productive energy investments, such as a shop owner financing income-generating equipment",
                        "Large-scale national grid infrastructure",
                        "Government-funded public schools only"
                    ],
                    "correct_index": 1,
                    "explanation": "Microfinance loans work well when the energy investment directly supports income-generating activity that can repay the loan."
                }
            ],
            "resources": []
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Assessing Real-World Energy Needs",
            "title": "Conducting an Energy Audit for a Small Business or Household",
            "learning_objective": "By the end of this class, you will be able to conduct a structured energy audit and produce a prioritized list of recommendations.",
            "duration_minutes": 30,
            "content_html": "<p>An energy audit is a formal, structured version of the waste walk-through from Day 10, and it is one of the most in-demand entry-level services in the sustainability field because businesses want concrete, prioritized recommendations, not vague advice.</p><h2>Structure of an Energy Audit</h2><p>A basic energy audit involves four steps: gathering utility bills and appliance inventory, measuring or estimating each appliance's energy use, identifying inefficiencies and waste, and producing a prioritized list of recommendations ranked by cost savings versus implementation cost and effort. Recommendations are usually grouped into no-cost or low-cost changes, such as behavior changes and bulb replacements, and higher-cost investments, such as new efficient equipment or solar installation.</p><h2>Worked Example</h2><p>An audit of a small print shop in Port Harcourt finds a large old air conditioner running constantly even when the shop is empty, incandescent bulbs throughout, and a printer left in standby mode overnight. The audit recommends, in priority order: first, install a timer or train staff to turn off the AC and printer when unoccupied (no cost, immediate savings), second, replace bulbs with LEDs (low cost, fast payback), and third, consider a more efficient inverter AC unit at the next equipment replacement cycle (higher cost, longer-term). Presenting recommendations in this prioritized, cost-tiered format is exactly what a client expects from a professional energy auditor and is a format worth mastering for freelance or employed audit work.</p>",
            "key_concepts": [
                "Energy audit process",
                "Appliance inventory",
                "No-cost vs low-cost vs high-cost recommendations",
                "Prioritized recommendation ranking",
                "Client-ready audit format"
            ],
            "practical_exercise": {
                "title": "Produce a Prioritized Energy Audit",
                "instructions": "Using the home or business you audited on Day 10, or a new one, write a short energy audit report with three sections: findings, recommendations grouped by no-cost, low-cost, and high-cost, and a one-paragraph summary of expected impact. Format it as you would present it to a real client."
            },
            "quiz": [
                {
                    "question": "Why are audit recommendations typically grouped into no-cost, low-cost, and high-cost categories?",
                    "options": [
                        "To make the report longer without adding value",
                        "Grouping by cost is not standard practice",
                        "To help the client prioritize actions based on cost and ease of implementation",
                        "Because all recommendations cost the same amount"
                    ],
                    "correct_index": 2,
                    "explanation": "Cost-tiered grouping helps clients act quickly on cheap fixes while planning for larger investments over time."
                },
                {
                    "question": "What is the first step in conducting a basic energy audit?",
                    "options": [
                        "Installing new solar panels immediately",
                        "Contacting a financing institution",
                        "Writing the final report before collecting any data",
                        "Gathering utility bills and an inventory of appliances and their usage"
                    ],
                    "correct_index": 3,
                    "explanation": "An audit begins with data collection, gathering bills and an appliance inventory, before analysis or recommendations can be made."
                },
                {
                    "question": "In the print shop example, which recommendation was ranked as no-cost and immediate?",
                    "options": [
                        "Turning off the AC and printer when the shop is unoccupied",
                        "Replacing the air conditioner with an inverter unit",
                        "Installing a new solar system",
                        "Rewiring the entire shop"
                    ],
                    "correct_index": 0,
                    "explanation": "Simple behavioral or timer-based changes to turn off idle equipment require no cost and deliver immediate savings."
                }
            ],
            "resources": []
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Broader Sustainability Practice",
            "title": "Waste Management and the Circular Economy in African Cities",
            "learning_objective": "By the end of this class, you will be able to explain the circular economy model and identify a circular opportunity in a local waste stream.",
            "duration_minutes": 25,
            "content_html": "<p>Sustainability work extends well beyond energy, and waste management is one of the most visible, fast-growing areas of opportunity in fast-urbanizing African cities, where formal waste collection often struggles to keep up with population growth.</p><h2>Linear vs Circular Systems</h2><p>A traditional linear economy follows a take-make-dispose model: raw materials are extracted, turned into products, used, then thrown away. A circular economy instead designs systems where waste from one process becomes input for another, through reuse, recycling, composting, or repurposing, reducing both raw material extraction and landfill burden. In many African cities, informal waste pickers already practice a rough version of this by collecting and reselling recyclables, though usually without safety protections or fair pricing, an area where formal circular economy businesses are now stepping in.</p><h2>Worked Example</h2><p>A social enterprise in Lagos collects plastic waste from markets and pays informal waste pickers a fair, transparent price per kilogram, then processes the plastic into raw material sold to manufacturers who turn it into new products like plastic lumber or building blocks. This model creates income for waste pickers, reduces plastic pollution in waterways, and generates revenue from material sales, a genuine triple bottom line win. Identifying a similarly overlooked waste stream, whether food waste from markets, sawdust from timber yards, or e-waste from electronics repair shops, is often the starting point for a strong sustainability venture or consulting recommendation.</p>",
            "key_concepts": [
                "Linear economy",
                "Circular economy",
                "Informal waste picking",
                "Waste-to-value business models",
                "Recycling and repurposing"
            ],
            "practical_exercise": {
                "title": "Identify a Circular Economy Opportunity",
                "instructions": "Identify one waste stream you observe locally, such as plastic, food waste, sawdust, or e-waste, and describe a specific circular economy opportunity to turn it into value. Explain who would collect it, how it would be processed or reused, and who the end buyer or beneficiary would be."
            },
            "quiz": [
                {
                    "question": "What best describes a circular economy?",
                    "options": [
                        "A system where materials are extracted, used once, and discarded",
                        "A system designed so waste from one process becomes input for another, reducing extraction and landfill burden",
                        "An economy based only on financial recycling of currency",
                        "A system with no waste collection at all"
                    ],
                    "correct_index": 1,
                    "explanation": "A circular economy keeps materials in use through reuse, recycling, or repurposing rather than following a single-use disposal path."
                },
                {
                    "question": "What role do informal waste pickers often play in African cities?",
                    "options": [
                        "They have no involvement in waste management at all",
                        "They exclusively manage grid electricity distribution",
                        "They collect and resell recyclables, often without formal protections or fair pricing",
                        "They regulate national environmental policy"
                    ],
                    "correct_index": 2,
                    "explanation": "Informal waste pickers frequently perform valuable recycling work in African cities, though often informally and without fair compensation."
                },
                {
                    "question": "In the Lagos plastic waste example, what made the model a triple bottom line success?",
                    "options": [
                        "It only generated profit with no social or environmental benefit",
                        "It required no interaction with local communities",
                        "It eliminated all plastic use in the city",
                        "It created fair income for waste pickers, reduced pollution, and generated revenue from material sales"
                    ],
                    "correct_index": 3,
                    "explanation": "The model delivered social benefit (fair income), environmental benefit (reduced pollution), and financial benefit (revenue) simultaneously."
                }
            ],
            "resources": [
                {
                    "label": "UN Sustainable Development Goals",
                    "url": "https://www.un.org/sustainabledevelopment"
                }
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Broader Sustainability Practice",
            "title": "Water Conservation and Sustainable Agriculture Practices",
            "learning_objective": "By the end of this class, you will be able to identify practical water conservation and sustainable agriculture techniques relevant to African farming contexts.",
            "duration_minutes": 25,
            "content_html": "<p>Water scarcity and unpredictable rainfall directly threaten food security and livelihoods across much of Africa, making water-smart, sustainable agriculture practices a core part of any broader sustainability skill set, especially for anyone advising agribusinesses or rural development projects.</p><h2>Key Techniques</h2><p>Drip irrigation delivers water directly to plant roots through a network of tubes, drastically reducing water waste compared to flood irrigation, and can be powered efficiently by small solar pumps in off-grid farms. Rainwater harvesting captures and stores rain for use during dry periods, reducing dependence on unreliable municipal or borehole water. Crop rotation and intercropping, growing different crops in sequence or together, improve soil health and reduce the need for chemical fertilizers, while reducing pest pressure that would otherwise require costly and environmentally harmful pesticide use.</p><h2>Worked Example</h2><p>A vegetable farm in the outskirts of Kano currently uses flood irrigation and diesel-powered pumps, both water- and fuel-intensive. Switching to a solar-powered drip irrigation system can cut water usage by up to 50 percent while eliminating diesel costs entirely, and adding a simple rainwater harvesting tank captures runoff during the rainy season for use in drier months. Recommending this kind of combined intervention, water efficiency plus renewable energy, is a common and valuable service in agricultural sustainability consulting, since it improves yields, cuts costs, and reduces environmental impact simultaneously.</p>",
            "key_concepts": [
                "Drip irrigation",
                "Rainwater harvesting",
                "Crop rotation and intercropping",
                "Solar-powered water pumping",
                "Water-energy-agriculture linkages"
            ],
            "practical_exercise": {
                "title": "Design a Water-Smart Farm Recommendation",
                "instructions": "Describe a small farm scenario, real or realistic, that currently uses inefficient irrigation. Recommend two specific water conservation or sustainable agriculture practices from today's class that would improve it, and explain the expected benefit of each in one to two sentences."
            },
            "quiz": [
                {
                    "question": "How does drip irrigation reduce water waste compared to flood irrigation?",
                    "options": [
                        "It delivers water directly to plant roots rather than spreading it across the whole field",
                        "It floods the entire field evenly",
                        "It eliminates the need for water entirely",
                        "It only works with diesel-powered pumps"
                    ],
                    "correct_index": 0,
                    "explanation": "Drip irrigation targets water delivery directly to roots, minimizing evaporation and runoff compared to flood irrigation."
                },
                {
                    "question": "What is the primary purpose of rainwater harvesting on a farm?",
                    "options": [
                        "To increase flooding during the rainy season",
                        "To capture and store rain for use during dry periods, reducing dependence on unreliable water sources",
                        "To replace the need for irrigation entirely",
                        "To generate electricity"
                    ],
                    "correct_index": 1,
                    "explanation": "Rainwater harvesting stores water collected during wet periods so it can be used when rainfall or other water sources are scarce."
                },
                {
                    "question": "Why might combining solar-powered drip irrigation with rainwater harvesting be recommended together?",
                    "options": [
                        "They cancel out each other's benefits",
                        "They only work in urban settings",
                        "Together they improve water efficiency, cut fuel costs, and reduce dependence on unreliable water and diesel",
                        "Combining them is more expensive with no added benefit"
                    ],
                    "correct_index": 2,
                    "explanation": "Combining these interventions addresses both water and energy inefficiencies at once, improving yields and cutting costs simultaneously."
                }
            ],
            "resources": []
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Broader Sustainability Practice",
            "title": "Corporate Sustainability Reporting: ESG Basics",
            "learning_objective": "By the end of this class, you will be able to explain the three pillars of ESG reporting and identify sample metrics for each.",
            "duration_minutes": 25,
            "content_html": "<p>As more African businesses seek international investment, partnerships, or export markets, they are increasingly asked to report on ESG performance, creating strong demand for people who understand how to structure and communicate this kind of reporting.</p><h2>The Three ESG Pillars</h2><p>Environmental criteria cover a company's impact on the natural world, including emissions, energy use, waste, and water consumption. Social criteria cover how a company treats people, including employees, suppliers, and communities, covering areas like fair labor practices, workplace safety, and community investment. Governance criteria cover how a company is run, including board structure, transparency, anti-corruption policies, and ethical business practices. Together these three pillars give investors and partners a structured way to evaluate a company beyond pure financial performance.</p><h2>Worked Example</h2><p>A Nigerian agro-processing company seeking a partnership with a European buyer is asked to provide an ESG summary. On the environmental side, it reports its solar-diesel hybrid power system and reduced emissions from switching processing equipment. On the social side, it reports the number of local jobs created and its policy of paying above minimum wage in its host community. On governance, it reports having an independent board member and a documented anti-bribery policy. Presenting exactly this kind of structured, evidence-based ESG summary, not vague claims about being environmentally friendly, is what actually satisfies international partners and unlocks the deal.</p>",
            "key_concepts": [
                "ESG (Environmental, Social, Governance)",
                "Environmental metrics",
                "Social metrics",
                "Governance metrics",
                "Investor and partner reporting expectations"
            ],
            "practical_exercise": {
                "title": "Draft a Mini ESG Summary",
                "instructions": "Choose a real or fictional Nigerian business. Write one specific, evidence-based example for each ESG pillar, environmental, social, and governance, describing something that business does or could do. Avoid vague statements; each example should include a concrete action or metric."
            },
            "quiz": [
                {
                    "question": "What does the Governance pillar of ESG primarily assess?",
                    "options": [
                        "A company's carbon emissions",
                        "Employee salary levels only",
                        "The number of trees a company plants",
                        "How a company is run, including board structure, transparency, and ethical practices"
                    ],
                    "correct_index": 3,
                    "explanation": "Governance covers how a company is managed and overseen, including board structure, transparency, and anti-corruption practices."
                },
                {
                    "question": "Why are more African businesses now engaging with ESG reporting?",
                    "options": [
                        "International investors, partners, and export markets increasingly expect ESG performance data",
                        "ESG reporting is legally required for all businesses worldwide",
                        "ESG reporting has no real business benefit",
                        "It replaces the need for financial reporting entirely"
                    ],
                    "correct_index": 0,
                    "explanation": "Growing demand from international investors and partners for ESG data is driving more African businesses to adopt structured ESG reporting."
                },
                {
                    "question": "In the agro-processing company example, what was reported under the Social pillar?",
                    "options": [
                        "Its solar-diesel hybrid power system",
                        "Local jobs created and above-minimum-wage pay in its host community",
                        "Its independent board member",
                        "Its anti-bribery policy"
                    ],
                    "correct_index": 1,
                    "explanation": "Local job creation and fair wages are social impact metrics, distinct from the environmental and governance examples given."
                }
            ],
            "resources": [
                {
                    "label": "Investopedia - ESG",
                    "url": "https://www.investopedia.com"
                }
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Broader Sustainability Practice",
            "title": "Environmental and Social Impact Assessment Fundamentals",
            "learning_objective": "By the end of this class, you will be able to outline the core components of an environmental and social impact assessment.",
            "duration_minutes": 25,
            "content_html": "<p>Before a mini-grid, factory, or large agricultural project is approved in most African countries, it must go through an environmental and social impact assessment (ESIA), a formal process this course prepares you to understand and contribute to, whether working for a developer, regulator, or consultancy.</p><h2>Core Components</h2><p>An ESIA typically includes a baseline study describing existing environmental and social conditions before the project, an impact identification stage predicting likely effects such as land disturbance, emissions, noise, or displacement of livelihoods, a mitigation plan proposing ways to avoid or reduce negative impacts, and a stakeholder consultation process gathering input from affected communities. Regulatory bodies in Nigeria, such as the Federal Ministry of Environment, require ESIAs for many categories of infrastructure and energy projects above a certain scale.</p><h2>Worked Example</h2><p>A proposed 2 MW solar mini-grid site near a farming community triggers an ESIA that identifies a possible impact: the site overlaps with land currently used for seasonal farming by twelve households. The mitigation plan proposes relocating the panel array to an adjacent, less-farmed plot and offering fair compensation for the temporary disruption of the current season's crops. The consultation process, holding an open meeting with the affected farmers before finalizing the site plan, both fulfills a regulatory requirement and builds the kind of community trust discussed in the mini-grid case study earlier this course.</p>",
            "key_concepts": [
                "Environmental and Social Impact Assessment (ESIA)",
                "Baseline study",
                "Impact identification",
                "Mitigation planning",
                "Stakeholder consultation"
            ],
            "practical_exercise": {
                "title": "Outline a Mini ESIA",
                "instructions": "For a hypothetical renewable energy or infrastructure project of your choice, outline the four core ESIA components: a one-sentence baseline description, one likely negative impact, one mitigation measure, and one stakeholder group you would consult before proceeding."
            },
            "quiz": [
                {
                    "question": "What is the purpose of the baseline study in an ESIA?",
                    "options": [
                        "To predict future profits from the project",
                        "To finalize the project budget",
                        "To describe existing environmental and social conditions before the project begins",
                        "To replace the need for stakeholder consultation"
                    ],
                    "correct_index": 2,
                    "explanation": "The baseline study documents conditions before a project starts, providing a reference point for measuring later impacts."
                },
                {
                    "question": "Why is stakeholder consultation an important part of the ESIA process?",
                    "options": [
                        "It is optional and rarely practiced",
                        "It only applies to projects with no environmental impact",
                        "It replaces the mitigation plan entirely",
                        "It gathers input from affected communities, helping identify concerns and build trust before approval"
                    ],
                    "correct_index": 3,
                    "explanation": "Consultation ensures affected communities have input into the project, surfacing concerns early and building trust."
                },
                {
                    "question": "In the solar mini-grid example, what mitigation measure was proposed for the farmland overlap?",
                    "options": [
                        "Relocating the panel array and offering fair compensation for crop disruption",
                        "Cancelling the project entirely",
                        "Ignoring the affected farmers",
                        "Doubling the mini-grid's size"
                    ],
                    "correct_index": 0,
                    "explanation": "The proposed mitigation relocated the site and compensated affected farmers rather than proceeding without addressing the impact."
                }
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Broader Sustainability Practice",
            "title": "Case Study: Evaluating a Sample Solar Mini-Grid Proposal",
            "learning_objective": "By the end of this class, you will be able to critically evaluate a sample renewable energy proposal for technical, financial, and social soundness.",
            "duration_minutes": 30,
            "content_html": "<p>Today brings together everything covered so far, energy basics, sizing, economics, financing, and impact assessment, into a single skill: critically reading someone else's proposal the way a funder, employer, or reviewer would, before you write your own next week.</p><h2>What Reviewers Check</h2><p>A strong reviewer checks whether the load calculation matches the stated community size and appliances, whether the panel and battery sizing logically follows from that load and the region's peak sun hours, whether the financial model shows a believable payback period and realistic tariff compared to what households can afford, and whether social and environmental risks were genuinely assessed rather than glossed over. Weak proposals often round numbers suspiciously, skip citing peak sun hour data, or promise implausibly fast payback periods without justifying the assumptions behind them.</p><h2>Worked Example</h2><p>A sample proposal claims a mini-grid for 200 households will pay back its full 15 million naira investment in 8 months from tariff revenue alone. A careful reviewer immediately checks the math: 15 million divided by 8 months requires roughly 1.875 million naira in monthly revenue, or about 9,375 naira per household monthly, an amount far higher than what most rural households were shown in earlier case studies to spend on kerosene and charging combined. This kind of red flag, an unrealistic payback claim inconsistent with affordability data, is exactly what you must learn to catch before recommending a project for funding or writing one yourself.</p>",
            "key_concepts": [
                "Proposal review skills",
                "Consistency checking between load, sizing, and finance",
                "Red flags in feasibility claims",
                "Affordability cross-checking",
                "Critical evaluation of assumptions"
            ],
            "practical_exercise": {
                "title": "Review a Sample Proposal Claim",
                "instructions": "Take the sample proposal figures from today's worked example (200 households, 15 million naira investment, 8-month payback claim). Write a short critique identifying why the payback claim is unrealistic, and suggest a more plausible payback period based on a monthly tariff of 3,500 naira per household."
            },
            "quiz": [
                {
                    "question": "What made the sample mini-grid proposal's 8-month payback claim suspicious?",
                    "options": [
                        "The math was mathematically impossible to calculate",
                        "The implied monthly revenue per household was far higher than realistic affordability data suggested",
                        "The proposal did not mention a tariff at all",
                        "8-month payback periods are never used in solar proposals"
                    ],
                    "correct_index": 1,
                    "explanation": "The required monthly revenue per household to hit that payback period was inconsistent with what similar communities could realistically afford."
                },
                {
                    "question": "What should a careful reviewer check regarding panel and battery sizing in a proposal?",
                    "options": [
                        "Whether the proposal is longer than 20 pages",
                        "Only whether the proposal includes colorful diagrams",
                        "Whether the sizing logically follows from the stated load and local peak sun hours",
                        "Whether the developer has a company logo"
                    ],
                    "correct_index": 2,
                    "explanation": "Sizing should be traceable back to the load calculation and local solar resource data, not presented as an unexplained number."
                },
                {
                    "question": "Why is affordability cross-checking an important part of reviewing a mini-grid proposal?",
                    "options": [
                        "Affordability has no bearing on financial viability",
                        "It replaces the need for a needs assessment",
                        "It is only relevant for grid-tied projects",
                        "It verifies that the proposed tariff is realistic given what households can actually pay"
                    ],
                    "correct_index": 3,
                    "explanation": "A tariff that ignores household affordability, even if mathematically balanced, is unlikely to be paid consistently in practice."
                }
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Building a Feasibility Study",
            "title": "Structuring a Professional Feasibility Study Report",
            "learning_objective": "By the end of this class, you will be able to outline the standard sections of a professional renewable energy or sustainability feasibility study.",
            "duration_minutes": 30,
            "content_html": "<p>Everything you have learned so far needs to come together in a document format that funders, employers, and clients actually expect to see. A brilliant analysis buried in a disorganized document often gets rejected simply because the reviewer cannot quickly find what they need.</p><h2>Standard Sections</h2><p>A professional feasibility study typically includes an executive summary (a one-page overview of the project and key findings), background and context, a needs assessment summary, a technical design section (system sizing, technology choice, and justification), a financial analysis (costs, LCOE, payback period, and financing structure), a social and environmental impact section, a risk assessment, and a final recommendations section. The executive summary is written last but placed first, since busy decision-makers often read only that section before deciding whether to read further.</p><h2>Worked Example</h2><p>A feasibility study for a solar mini-grid in a Niger State community would open with a half-page executive summary stating the community size, proposed system capacity, total investment required, expected payback period, and headline social impact, such as the number of households and businesses served. Only after that summary would the document walk through the detailed needs assessment data, technical sizing calculations, and financial model that support those headline numbers. Structuring your capstone project this way, from Day 30 onward, is what will make it read like a real, fundable proposal rather than a school assignment.</p>",
            "key_concepts": [
                "Feasibility study structure",
                "Executive summary",
                "Technical design section",
                "Financial analysis section",
                "Risk assessment section"
            ],
            "practical_exercise": {
                "title": "Draft a Feasibility Study Outline",
                "instructions": "Create a section-by-section outline for a feasibility study on a renewable energy or sustainability topic of your choice, listing each of the eight sections from today's class with one sentence describing what content will go in each section for your chosen project."
            },
            "quiz": [
                {
                    "question": "Why is the executive summary written last but placed first in a feasibility study?",
                    "options": [
                        "Busy decision-makers often read only the summary first, so it must accurately reflect the full completed analysis",
                        "It is the least important section",
                        "It has no connection to the rest of the report",
                        "Order does not matter in professional reports"
                    ],
                    "correct_index": 0,
                    "explanation": "Writing it last ensures accuracy, while placing it first respects how decision-makers actually read reports, summary first."
                },
                {
                    "question": "Which section of a feasibility study covers system sizing and technology justification?",
                    "options": [
                        "Executive summary",
                        "Technical design section",
                        "Risk assessment",
                        "Needs assessment summary"
                    ],
                    "correct_index": 1,
                    "explanation": "The technical design section presents the sizing, technology choice, and justification for the proposed system."
                },
                {
                    "question": "What is the purpose of the risk assessment section in a feasibility study?",
                    "options": [
                        "To list only the positive outcomes of the project",
                        "To replace the financial analysis section",
                        "To identify potential risks and how they might affect the project's success",
                        "To describe the community's history"
                    ],
                    "correct_index": 2,
                    "explanation": "The risk assessment identifies potential threats to the project and prepares stakeholders for how they might be managed."
                }
            ],
            "resources": []
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Building a Feasibility Study",
            "title": "Cost-Benefit Analysis for a Renewable Energy or Sustainability Intervention",
            "learning_objective": "By the end of this class, you will be able to construct a basic cost-benefit analysis comparing costs against quantified benefits.",
            "duration_minutes": 30,
            "content_html": "<p>A cost-benefit analysis is the financial heart of any feasibility study, and constructing one credibly requires pulling together everything from load calculations to LCOE to emissions data into a single, clear comparison that shows whether a project is worth pursuing.</p><h2>Building the Analysis</h2><p>A basic cost-benefit analysis lists all costs, including upfront capital expenditure, ongoing operations and maintenance, and financing costs, against all quantified benefits, including direct financial savings or revenue, avoided costs such as reduced diesel spending, and where relevant, monetized social or environmental value. These are typically compared over the project's expected lifetime, often using a net present value calculation that accounts for money today being worth more than money in the future, though a simpler total-lifetime comparison is acceptable for an entry-level analysis.</p><h2>Worked Example</h2><p>A solar system for a poultry farm in Oyo State costs 1.2 million naira upfront plus 50,000 naira annually in maintenance, totaling roughly 2.2 million naira over a 20-year lifetime. The benefits include eliminating 180,000 naira in annual diesel costs (3.6 million naira over 20 years) and avoiding roughly 2 tonnes of CO2 emissions yearly. Comparing total costs of 2.2 million naira against total financial benefits of 3.6 million naira shows a clear positive case, a net benefit of 1.4 million naira over the system's life, even before counting the environmental benefit, which strengthens the recommendation further in a report aimed at a sustainability-conscious funder.</p>",
            "key_concepts": [
                "Cost-benefit analysis",
                "Capital expenditure vs operating cost",
                "Avoided cost as a benefit",
                "Net present value (introductory)",
                "Monetizing environmental benefit"
            ],
            "practical_exercise": {
                "title": "Build a Simple Cost-Benefit Table",
                "instructions": "For a renewable energy or sustainability intervention of your choice, list all costs (upfront and ongoing) and all benefits (savings, avoided costs, or revenue) over a 10-year period in a simple table. Calculate the net benefit or cost and write one sentence stating whether the project appears financially justified."
            },
            "quiz": [
                {
                    "question": "What is meant by avoided cost as a benefit in a cost-benefit analysis?",
                    "options": [
                        "Money spent on new equipment",
                        "A cost that is postponed rather than eliminated",
                        "The cost of financing a loan",
                        "Savings from no longer having to pay for a previous cost, such as diesel fuel"
                    ],
                    "correct_index": 3,
                    "explanation": "Avoided cost refers to money no longer spent, such as diesel fuel savings, which counts as a financial benefit of the new intervention."
                },
                {
                    "question": "In the poultry farm example, what was the total cost over the system's 20-year lifetime?",
                    "options": [
                        "Roughly 2.2 million naira",
                        "1.2 million naira",
                        "3.6 million naira",
                        "180,000 naira"
                    ],
                    "correct_index": 0,
                    "explanation": "Adding the 1.2 million naira upfront cost to 20 years of 50,000 naira annual maintenance gives roughly 2.2 million naira total."
                },
                {
                    "question": "Why might environmental benefits be included in a cost-benefit analysis even though they are harder to monetize than direct savings?",
                    "options": [
                        "They should never be included in a professional report",
                        "They strengthen the overall case, especially for sustainability-conscious funders",
                        "They always outweigh financial benefits",
                        "They replace the need for financial analysis entirely"
                    ],
                    "correct_index": 1,
                    "explanation": "Including environmental benefits, even alongside strong financial ones, adds persuasive weight for funders focused on sustainability outcomes."
                }
            ],
            "resources": [
                {
                    "label": "Investopedia - Cost-Benefit Analysis",
                    "url": "https://www.investopedia.com"
                }
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Building a Feasibility Study",
            "title": "Stakeholder Engagement and Managing Community Buy-In",
            "learning_objective": "By the end of this class, you will be able to develop a stakeholder engagement plan identifying key groups and engagement methods.",
            "duration_minutes": 25,
            "content_html": "<p>Every project this course has discussed, from mini-grids to sustainability audits, ultimately succeeds or fails based on whether the people affected by it trust and cooperate with it. A stakeholder engagement plan turns that soft skill into a structured, professional deliverable.</p><h2>Identifying and Engaging Stakeholders</h2><p>Stakeholders typically include the direct beneficiaries (households, business owners, or employees), local leadership (traditional rulers, local government officials), regulatory bodies, financiers or investors, and sometimes competing interests such as existing informal energy sellers who might resist a new mini-grid. A good engagement plan matches the method to the stakeholder: community-wide meetings for beneficiaries, formal briefings for regulators and investors, and one-on-one conversations for influential local leaders whose support strongly shapes broader community acceptance.</p><h2>Worked Example</h2><p>A proposed mini-grid in a community currently served informally by a few generator owners who sell power by the hour identifies those generator owners as a stakeholder group likely to resist the project, since it threatens their income. Rather than ignoring them, the engagement plan proposes offering them a role as local mini-grid agents, handling customer sign-ups, and small maintenance tasks, turning a potential source of resistance into a source of support. This kind of proactive stakeholder management, planned before construction, not reactive conflict management after resistance appears, is a mark of a mature, professional project plan.</p>",
            "key_concepts": [
                "Stakeholder identification",
                "Engagement method matching",
                "Competing interests",
                "Turning resistance into support",
                "Proactive vs reactive engagement"
            ],
            "practical_exercise": {
                "title": "Build a Stakeholder Engagement Plan",
                "instructions": "For your capstone project idea, list four stakeholder groups and, for each, identify their likely interest or concern and the engagement method you would use to reach them. Present this as a simple table with columns for stakeholder, interest or concern, and engagement method."
            },
            "quiz": [
                {
                    "question": "Why might existing informal generator owners resist a new mini-grid project?",
                    "options": [
                        "They always support renewable energy projects unconditionally",
                        "They have no connection to the local energy market",
                        "The project could threaten their existing income from selling generator power",
                        "Mini-grids never affect informal energy sellers"
                    ],
                    "correct_index": 2,
                    "explanation": "A new mini-grid can directly compete with informal generator-based power sales, creating a real incentive for resistance."
                },
                {
                    "question": "What is a proactive way to manage stakeholder resistance from informal energy sellers?",
                    "options": [
                        "Ignoring them entirely during planning",
                        "Waiting until after construction to address concerns",
                        "Excluding them from the community entirely",
                        "Offering them a role in the new system, such as local agents, turning resistance into support"
                    ],
                    "correct_index": 3,
                    "explanation": "Involving potential resistors as partners in the new system converts a threat into a source of support before problems arise."
                },
                {
                    "question": "Why should engagement methods differ across stakeholder groups?",
                    "options": [
                        "Different groups, such as regulators versus community members, respond better to different formats like formal briefings versus community meetings",
                        "All stakeholders should always be engaged the same way",
                        "Engagement methods have no effect on stakeholder cooperation",
                        "Only investors need to be engaged at all"
                    ],
                    "correct_index": 0,
                    "explanation": "Matching the engagement method to the stakeholder group, formal for regulators, community-based for residents, improves effectiveness."
                }
            ],
            "resources": []
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Building a Feasibility Study",
            "title": "Navigating Policy, Regulation, and Incentives for Renewables in Nigeria",
            "learning_objective": "By the end of this class, you will be able to identify key regulatory bodies and incentives relevant to a renewable energy project in Nigeria.",
            "duration_minutes": 25,
            "content_html": "<p>A technically sound and financially attractive project can still stall or fail without understanding the regulatory landscape it operates in, which is why every professional feasibility study includes a policy and regulation section.</p><h2>Key Regulatory Bodies and Incentives</h2><p>In Nigeria, the Nigerian Electricity Regulatory Commission (NERC) oversees mini-grid licensing and tariff regulation, while the Rural Electrification Agency (REA) supports and sometimes co-funds off-grid electrification projects. Import duty waivers on solar equipment have periodically been introduced to reduce upfront costs for developers, and some state governments run their own renewable energy incentive programs. Understanding which permits, licenses, and registrations a specific project size and type requires, since mini-grids above certain capacities face different rules than small household systems, prevents costly delays discovered too late in a project timeline.</p><h2>Worked Example</h2><p>A developer planning a mini-grid under 100 kW in Nigeria benefits from a simplified NERC registration process compared to larger systems, which require a more detailed permit application. A feasibility study for such a project would note this threshold explicitly, recommend confirming current REA co-funding opportunities before finalizing the financial model, and flag import duty status on the batteries and panels being sourced, since duty changes can meaningfully shift the total project cost calculated back in the cost-benefit analysis from Day 22.</p>",
            "key_concepts": [
                "Nigerian Electricity Regulatory Commission (NERC)",
                "Rural Electrification Agency (REA)",
                "Import duty incentives",
                "Mini-grid capacity thresholds",
                "Regulatory risk in project planning"
            ],
            "practical_exercise": {
                "title": "Draft a Regulatory Considerations Section",
                "instructions": "Write a short paragraph for your capstone feasibility study identifying which regulatory bodies or licensing requirements would apply to your chosen project, and one incentive (such as an REA program or duty waiver) that could improve its financial case. If you are unsure of exact current rules, state clearly what you would need to confirm and from whom."
            },
            "quiz": [
                {
                    "question": "What is the primary role of the Nigerian Electricity Regulatory Commission (NERC) in mini-grid projects?",
                    "options": [
                        "Providing free equipment to developers",
                        "Overseeing mini-grid licensing and tariff regulation",
                        "Manufacturing solar panels",
                        "Managing community engagement directly"
                    ],
                    "correct_index": 1,
                    "explanation": "NERC regulates licensing and tariffs for mini-grid and broader electricity projects in Nigeria."
                },
                {
                    "question": "Why does mini-grid system capacity matter for regulatory purposes?",
                    "options": [
                        "Capacity has no effect on regulatory requirements",
                        "All mini-grids regardless of size follow identical rules",
                        "Different capacity thresholds can trigger different, more detailed permit and licensing requirements",
                        "Capacity only affects battery choice, not regulation"
                    ],
                    "correct_index": 2,
                    "explanation": "Larger mini-grid systems typically face more detailed regulatory requirements than smaller ones, making capacity a relevant planning factor."
                },
                {
                    "question": "What is a practical reason to research import duty status on solar equipment during feasibility planning?",
                    "options": [
                        "Import duties never affect project costs",
                        "Import duties are fixed and never need verification",
                        "It is only relevant for wind projects",
                        "Duty waivers or changes can meaningfully shift total project cost figures used in the financial analysis"
                    ],
                    "correct_index": 3,
                    "explanation": "Import duty status on equipment can significantly affect total project costs, making it important to confirm during planning."
                }
            ],
            "resources": [
                {
                    "label": "IRENA - Policy",
                    "url": "https://www.irena.org/Energy-Transition/Policy"
                }
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Building a Feasibility Study",
            "title": "Assessing and Documenting Project Risks",
            "learning_objective": "By the end of this class, you will be able to build a risk register identifying likelihood, impact, and mitigation for a renewable energy project.",
            "duration_minutes": 25,
            "content_html": "<p>No feasibility study is complete without an honest accounting of what could go wrong, and being upfront about risk is actually what makes a report more credible to an experienced funder, not less, since it signals the author understands the project deeply.</p><h2>Building a Risk Register</h2><p>A risk register lists specific risks, such as delayed equipment delivery, currency fluctuation affecting imported component costs, lower-than-projected customer uptake, extreme weather damaging infrastructure, or political and community disputes over land, along with an assessment of likelihood (low, medium, high), potential impact, and a mitigation strategy for each. This structured format, rather than a vague paragraph about challenges, allows a reviewer to quickly see which risks are most serious and whether the project team has thought through realistic responses.</p><h2>Worked Example</h2><p>A mini-grid project's risk register lists currency fluctuation as a medium-likelihood, high-impact risk, since panels and batteries are typically imported and priced partly in dollars, and naira depreciation could raise costs mid-project. The mitigation strategy proposes locking in equipment pricing through an early bulk purchase agreement and building a 10 percent cost contingency into the budget. Listing this risk explicitly, rather than hoping currency stays stable, is exactly the kind of realistic, professional risk planning that distinguishes a fundable feasibility study from an overly optimistic one that collapses at the first unexpected cost increase.</p>",
            "key_concepts": [
                "Risk register",
                "Likelihood and impact rating",
                "Currency and supply chain risk",
                "Mitigation strategy",
                "Cost contingency planning"
            ],
            "practical_exercise": {
                "title": "Build a Risk Register",
                "instructions": "For your capstone project, identify four specific risks. For each, rate the likelihood (low, medium, high) and impact (low, medium, high), and write one mitigation strategy. Present this as a table with columns for risk, likelihood, impact, and mitigation."
            },
            "quiz": [
                {
                    "question": "Why does including an honest risk register make a feasibility study more credible, not less?",
                    "options": [
                        "It signals the project team has thought through realistic challenges and planned responses",
                        "Funders prefer reports that hide potential problems",
                        "Risk registers are purely a formality with no real value",
                        "Including risks always guarantees project rejection"
                    ],
                    "correct_index": 0,
                    "explanation": "A thoughtful risk register demonstrates deep understanding of the project and builds funder confidence rather than undermining it."
                },
                {
                    "question": "What two factors are typically rated for each risk in a risk register?",
                    "options": [
                        "Cost and color coding only",
                        "Likelihood and impact",
                        "Location and population size",
                        "Panel wattage and battery type"
                    ],
                    "correct_index": 1,
                    "explanation": "Risk registers typically assess how likely a risk is to occur and how severe its impact would be if it did."
                },
                {
                    "question": "In the worked example, what mitigation strategy was proposed for currency fluctuation risk?",
                    "options": [
                        "Ignoring the risk entirely",
                        "Cancelling the project if currency changes",
                        "Locking in equipment pricing early and building a cost contingency into the budget",
                        "Switching to an entirely different technology"
                    ],
                    "correct_index": 2,
                    "explanation": "The mitigation combined an early bulk purchase agreement with a budget contingency to absorb potential currency-driven cost increases."
                }
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Careers and Capstone Delivery",
            "title": "Renewable Energy and Sustainability Careers: Roles and Employers",
            "learning_objective": "By the end of this class, you will be able to identify at least five distinct job roles and employer types in the renewable energy and sustainability sector.",
            "duration_minutes": 25,
            "content_html": "<p>With the technical and analytical foundation from the past 25 days in place, it is time to map that knowledge onto real jobs, so you know exactly what to search for, apply to, and highlight in interviews once you finish this course.</p><h2>Common Roles and Employers</h2><p>Entry-level roles include energy access field associate, solar installation technician, sustainability analyst, and ESG reporting assistant, while mid-level roles include project developer, energy auditor, and monitoring and evaluation officer. Employers span solar EPC (engineering, procurement, construction) companies, mini-grid developers, development finance institutions and NGOs working on rural electrification, corporate sustainability departments in banks and manufacturing companies, and independent consultancies that produce feasibility studies and ESG reports for clients.</p><h2>Worked Example</h2><p>A student who completes this course could realistically apply for a field associate role at a mini-grid developer, where the job involves conducting exactly the kind of community needs assessments practiced on Day 11, or apply for a junior sustainability analyst role at a bank's ESG department, where the work involves gathering and reporting the kind of metrics discussed on Day 18. Being able to point directly to specific exercises completed in this course, a needs assessment survey, a cost-benefit table, a risk register, gives a concrete answer when an interviewer asks for an example of relevant experience, even without prior formal employment in the sector.</p>",
            "key_concepts": [
                "Entry-level renewable energy roles",
                "Mid-level career paths",
                "Solar EPC companies",
                "Development finance and NGO employers",
                "Corporate sustainability departments"
            ],
            "practical_exercise": {
                "title": "Research a Target Role",
                "instructions": "Search for one real job posting or LinkedIn profile description for an entry-level renewable energy or sustainability role. Write a short summary of the responsibilities listed and identify two specific skills or exercises from this course so far that would directly relate to that role."
            },
            "quiz": [
                {
                    "question": "Which of these is an example of an entry-level role in this sector?",
                    "options": [
                        "Chief executive officer",
                        "Board chairperson",
                        "National energy minister",
                        "Energy access field associate"
                    ],
                    "correct_index": 3,
                    "explanation": "Field associate roles are common entry points, involving hands-on community and site work like needs assessments."
                },
                {
                    "question": "Which type of organization would most likely employ someone in a corporate ESG reporting role?",
                    "options": [
                        "A bank or manufacturing company with a sustainability department",
                        "A solar panel manufacturer only",
                        "Only government regulatory bodies",
                        "Only rural mini-grid developers"
                    ],
                    "correct_index": 0,
                    "explanation": "Banks and manufacturers increasingly maintain sustainability departments that need ESG reporting staff."
                },
                {
                    "question": "Why is it valuable to reference specific course exercises when answering an interview question about experience?",
                    "options": [
                        "Interviewers never ask about relevant experience",
                        "It gives a concrete, specific example of applied skill even without prior formal employment",
                        "Course exercises are irrelevant to real job interviews",
                        "It is better to speak only in general terms"
                    ],
                    "correct_index": 1,
                    "explanation": "Concrete examples from completed exercises demonstrate applied skill more convincingly than general claims of interest or knowledge."
                }
            ],
            "resources": [
                {
                    "label": "LinkedIn Learning",
                    "url": "https://www.linkedin.com/learning"
                }
            ]
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Careers and Capstone Delivery",
            "title": "Common Interview Questions in the Renewable Energy and Sustainability Sector",
            "learning_objective": "By the end of this class, you will be able to confidently answer three common renewable energy and sustainability interview questions using course concepts.",
            "duration_minutes": 25,
            "content_html": "<p>Technical knowledge alone does not get you hired if you cannot communicate it clearly under interview pressure. Today focuses on translating the concepts from this course into confident, structured spoken answers to the questions this sector's interviewers ask most often.</p><h2>Frequent Interview Questions</h2><p>Common questions include: How would you assess whether a community is a good candidate for a mini-grid? What factors would you consider when sizing a solar system? How do you calculate payback period, and why does it matter to a funder? How would you handle resistance from a community stakeholder? Interviewers ask these not to test memorized definitions, but to see whether a candidate can reason through a real scenario using the right framework, which is exactly what this course has trained through worked examples.</p><h2>Worked Example</h2><p>Asked how they would assess mini-grid candidacy, a strong candidate answer references the specific components from Day 11: population and household count, current energy spending as a proxy for willingness to pay, and the presence of anchor loads like a clinic or grinding mill, then gives a concrete hypothetical number, such as noting that households spending over 3,000 naira monthly on kerosene are a positive signal. A weak answer simply says they would check if people need electricity, which shows no structured method. Practicing this kind of specific, framework-based answer out loud, not just reading about it, is what today's exercise is designed to build.</p>",
            "key_concepts": [
                "Structured interview answers",
                "Framework-based reasoning",
                "Community candidacy criteria",
                "Communicating technical reasoning clearly",
                "Specific versus vague answers"
            ],
            "practical_exercise": {
                "title": "Practice Answering Interview Questions Aloud",
                "instructions": "Choose two of the four sample interview questions listed in today's class. Write out a structured answer to each using specific concepts and numbers from earlier days in this course, then practice saying each answer aloud in under 90 seconds without reading directly from your notes."
            },
            "quiz": [
                {
                    "question": "Why do interviewers in this sector typically ask scenario-based questions?",
                    "options": [
                        "To test whether a candidate memorized dictionary definitions",
                        "Scenario questions are rarely used in this sector",
                        "To see whether a candidate can reason through a real scenario using a structured method",
                        "To evaluate a candidate's typing speed"
                    ],
                    "correct_index": 2,
                    "explanation": "Scenario-based questions reveal whether a candidate can apply structured reasoning to realistic problems, not just recall facts."
                },
                {
                    "question": "What made the strong sample answer about mini-grid candidacy effective?",
                    "options": [
                        "It avoided giving any specific details",
                        "It focused only on emotional appeals",
                        "It was the shortest possible answer",
                        "It referenced specific assessment components and included a concrete numerical example"
                    ],
                    "correct_index": 3,
                    "explanation": "Specific, structured answers referencing concrete criteria and numbers demonstrate real understanding more convincingly than vague statements."
                },
                {
                    "question": "What is a key weakness of the sample weak answer, I would check if people need electricity?",
                    "options": [
                        "It shows no structured method or specific criteria for assessment",
                        "It is too detailed and technical",
                        "It correctly follows the needs assessment framework",
                        "It includes too many numbers"
                    ],
                    "correct_index": 0,
                    "explanation": "The weak answer lacks the specific, structured criteria that demonstrate genuine understanding of the assessment process."
                }
            ],
            "resources": [
                {
                    "label": "The Muse - Interview Advice",
                    "url": "https://www.themuse.com/advice"
                }
            ]
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Careers and Capstone Delivery",
            "title": "Writing a Feasibility or Impact Report Employers Will Actually Read",
            "learning_objective": "By the end of this class, you will be able to apply clear, professional writing techniques to a technical feasibility or impact report.",
            "duration_minutes": 25,
            "content_html": "<p>A technically excellent analysis can still fail to persuade if it is buried in dense, jargon-heavy writing. Today focuses specifically on the writing craft that turns your Day 21 outline and all your calculations into a document busy decision-makers will actually finish reading.</p><h2>Writing Techniques That Work</h2><p>Use short paragraphs and clear headings so a reader can scan the document and find what they need quickly. Lead each section with its main finding or conclusion before the supporting detail, a technique often called front-loading, since decision-makers often only read the first sentence of each section closely. Replace vague claims like significant savings with specific numbers like savings of 1.4 million naira over 20 years, and define technical terms briefly the first time they appear, since not every reader will share your technical background.</p><h2>Worked Example</h2><p>A weak sentence reads: The project has various benefits including cost savings and is expected to be quite favorable financially. A strong, front-loaded rewrite reads: The project delivers a net financial benefit of 1.4 million naira over 20 years, with payback achieved in year 6. The second version lets a busy reviewer absorb the key finding in seconds without hunting through vague language, exactly the writing standard your capstone feasibility study needs to meet when you submit it after tomorrow's final planning day.</p>",
            "key_concepts": [
                "Front-loading key findings",
                "Scannable formatting with headings",
                "Replacing vague claims with specific numbers",
                "Defining technical terms for a general reader",
                "Professional report writing craft"
            ],
            "practical_exercise": {
                "title": "Rewrite a Weak Report Sentence",
                "instructions": "Write three weak, vague sentences you might be tempted to use in a feasibility report, such as claims about savings, impact, or performance without specific numbers. Rewrite each one as a strong, front-loaded sentence using specific figures, even if estimated, from your capstone project idea."
            },
            "quiz": [
                {
                    "question": "What does front-loading mean in professional report writing?",
                    "options": [
                        "Writing the conclusion at the very end of the document only",
                        "Leading each section with its main finding before the supporting detail",
                        "Using as much technical jargon as possible",
                        "Writing extremely long paragraphs without headings"
                    ],
                    "correct_index": 1,
                    "explanation": "Front-loading places the key conclusion first in a section, respecting how busy readers actually scan documents."
                },
                {
                    "question": "Why should vague claims like significant savings be replaced with specific numbers?",
                    "options": [
                        "Specific numbers are harder for readers to understand",
                        "Vague language is always preferred in professional reports",
                        "Specific figures are more persuasive and let a reader quickly grasp the actual impact",
                        "Numbers should never appear in a feasibility report"
                    ],
                    "correct_index": 2,
                    "explanation": "Concrete figures communicate impact clearly and credibly, while vague language leaves readers uncertain of actual results."
                },
                {
                    "question": "Why is it important to briefly define technical terms the first time they appear in a report?",
                    "options": [
                        "All readers are assumed to share the author's technical background",
                        "Definitions make a report less credible",
                        "Technical terms should never be used in professional reports",
                        "Not every reader, including some decision-makers, shares the author's technical background"
                    ],
                    "correct_index": 3,
                    "explanation": "Briefly defining terms ensures the report remains accessible to readers who may not share the same technical expertise."
                }
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Careers and Capstone Delivery",
            "title": "Presenting Technical Findings to Non-Technical Stakeholders and Investors",
            "learning_objective": "By the end of this class, you will be able to structure a short verbal presentation of a technical project for a non-technical audience.",
            "duration_minutes": 25,
            "content_html": "<p>Many renewable energy and sustainability roles require presenting findings out loud, to investors, community leaders, or company executives, who often have limited patience for technical detail and want to know quickly whether a project is worth their time and money.</p><h2>Structuring a Strong Presentation</h2><p>A strong short presentation follows a simple structure: state the problem in one sentence, state the proposed solution in one or two sentences, state the headline financial and impact numbers, briefly note the main risk and how it is managed, and close with a specific ask, such as funding approval, a pilot commitment, or a follow-up meeting. Visual aids should show one clear number or comparison per slide or chart, never a dense table of raw data, since audiences remember simple visuals far better than complex ones.</p><h2>Worked Example</h2><p>Presenting the poultry farm solar project from Day 22 to a potential investor, a strong opening says: This farm currently loses 180,000 naira a year to diesel costs; a 1.2 million naira solar investment eliminates that cost entirely and pays for itself in under seven years, while cutting 2 tonnes of CO2 emissions annually. This four-sentence opening, delivered confidently in the first thirty seconds, tells the investor everything they need to decide whether to keep listening, which is exactly the skill this course has been building toward across all 29 days so far.</p>",
            "key_concepts": [
                "Verbal presentation structure",
                "Leading with the problem and solution",
                "Headline numbers over raw data",
                "Visual simplicity",
                "Ending with a clear ask"
            ],
            "practical_exercise": {
                "title": "Script a 60-Second Project Pitch",
                "instructions": "Using your capstone project idea, write a 60-second spoken pitch following today's structure: problem, solution, headline numbers, main risk, and a specific ask. Practice delivering it aloud at least twice, timing yourself to stay close to 60 seconds."
            },
            "quiz": [
                {
                    "question": "Why should a technical presentation to investors lead with the problem and headline numbers rather than detailed methodology?",
                    "options": [
                        "Investors and non-technical audiences often decide quickly whether a project is worth their time based on clear headline information",
                        "Investors prefer long technical explanations first",
                        "Methodology should never be included at all",
                        "Headline numbers are less important than raw data tables"
                    ],
                    "correct_index": 0,
                    "explanation": "Busy, non-technical audiences respond best to a clear, quick summary of the problem and impact before deeper technical detail."
                },
                {
                    "question": "What should a strong presentation close with?",
                    "options": [
                        "A long list of unrelated facts",
                        "A specific ask, such as funding approval or a follow-up meeting",
                        "An apology for taking up the audience's time",
                        "A repeat of the technical methodology"
                    ],
                    "correct_index": 1,
                    "explanation": "Ending with a clear, specific ask tells the audience exactly what action or decision is being requested."
                },
                {
                    "question": "Why are dense tables of raw data discouraged in visual aids for this kind of presentation?",
                    "options": [
                        "Raw data tables are always required by investors",
                        "Visual aids are not allowed in professional presentations",
                        "Audiences remember simple visuals showing one clear number or comparison far better than complex data",
                        "Dense tables are the fastest way to communicate a point"
                    ],
                    "correct_index": 2,
                    "explanation": "Simple, focused visuals communicate key points more effectively than dense data tables, which are harder for an audience to absorb quickly."
                }
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Careers and Capstone Delivery",
            "title": "Launching Your Renewable Energy Feasibility or Sustainability Impact Study",
            "learning_objective": "By the end of this class, you will be able to begin producing your Renewable Energy Feasibility or Sustainability Impact Study capstone project using the full toolkit built over the past 29 days.",
            "duration_minutes": 30,
            "content_html": "<p>Today is the starting point for your final capstone project, the Renewable Energy Feasibility or Sustainability Impact Study, the same deliverable a real solar developer, NGO, or sustainability consultancy would produce for a funder, client, or employer. Everything from load calculations to stakeholder plans to report-writing craft has been building toward this single, portfolio-quality document.</p><h2>Choosing Your Path and Starting Strong</h2><p>First, decide between the two capstone paths: a solar mini-grid feasibility study for a specific underserved community, or a sustainability audit with recommendations for a small business or corporate operation. Choose whichever path connects to a real place, business, or community you have some knowledge of or can realistically research, since specific, grounded detail is what separates a strong capstone from a generic one. Begin by drafting your needs assessment or audit findings section using the methods from Day 11 or Day 15, since every other section, technical design, financial analysis, stakeholder plan, and risk register, depends on this foundation being solid first.</p><h2>How to Approach the Full Study</h2><p>Use the Day 21 outline structure to organize your report, the Day 22 cost-benefit method for your financial analysis, the Day 23 stakeholder framework, and the Day 25 risk register, then apply the Day 28 writing techniques as you draft. Work through it in that order, needs assessment first, then technical design, then financial analysis, then risks and stakeholders, then the executive summary last, exactly as a real feasibility study is professionally assembled.</p>",
            "key_concepts": [
                "Capstone project kickoff",
                "Choosing a feasibility study path",
                "Needs assessment as the foundation",
                "Sequencing a full feasibility report",
                "Applying the full course toolkit"
            ],
            "practical_exercise": {
                "title": "Start Your Capstone: Renewable Energy Feasibility or Sustainability Impact Study",
                "instructions": "This exercise is the official start of your final capstone project. Choose your path (mini-grid feasibility study or business sustainability audit), name the specific community or business you will study, and write your initial needs assessment or audit findings section, at least 300 words, covering current energy or sustainability conditions, key data gathered or estimated, and the core problem your study will address. Submit this as the first working section of your final capstone report."
            },
            "quiz": [
                {
                    "question": "What are the two capstone project paths offered for the final project?",
                    "options": [
                        "A marketing campaign and a business plan",
                        "A research essay and a poetry collection",
                        "A coding project and a design portfolio",
                        "A solar mini-grid feasibility study or a sustainability audit for a business"
                    ],
                    "correct_index": 3,
                    "explanation": "The two capstone options are a mini-grid feasibility study for a community or a sustainability audit for a business."
                },
                {
                    "question": "Why does the capstone project recommend starting with the needs assessment or audit findings section first?",
                    "options": [
                        "Every other section, including technical design and financial analysis, depends on this foundation being solid",
                        "It is the least important section",
                        "The executive summary should always be written first instead",
                        "Needs assessments are optional in a feasibility study"
                    ],
                    "correct_index": 0,
                    "explanation": "The needs assessment or audit findings provide the foundational data that technical, financial, and risk sections all build upon."
                },
                {
                    "question": "In what order does today's class recommend assembling the full feasibility study?",
                    "options": [
                        "Executive summary first, then everything else",
                        "Needs assessment first, then technical design, financial analysis, risks and stakeholders, with the executive summary last",
                        "Risk register first, then needs assessment",
                        "Random order, since sequence does not matter"
                    ],
                    "correct_index": 1,
                    "explanation": "The recommended sequence builds from foundational data through analysis sections, finishing with the executive summary that summarizes it all."
                }
            ],
            "resources": []
        }
    ]
}
