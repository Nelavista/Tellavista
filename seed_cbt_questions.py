"""One-off seed: copies the hand-authored, honest practice-question bank embedded in
templates/CBT.html's generateFullQuestionBank() (cbtTemplates / writtenTemplates,
subject-code-prefix keyed) verbatim into the CBTQuestion table, so it becomes a real,
admin-manageable question bank (see models.py's "CBT PERSISTENCE" section) instead of
living only in client-side JS. No new question content is written here -- every
question/option/answer/explanation below is copied unchanged from CBT.html.

Usage:
    python seed_cbt_questions.py
"""
from app import app, db
from models import CBTQuestion

# ---- MCQ bank, copied verbatim from CBT.html's cbtTemplates ----------------------
CBT_TEMPLATES = {
    'MTH': [
        {"q": "Solve: 2x + 5 = 13", "o": ["3", "4", "5", "6"], "a": 1, "e": "2x = 8 => x = 4."},
        {"q": "What is log₂(8)?", "o": ["2", "3", "4", "8"], "a": 1, "e": "log₂(2³) = 3."},
        {"q": "Derivative of x³?", "o": ["x²", "2x²", "3x²", "3x³"], "a": 2, "e": "d/dx(xⁿ)=nxⁿ⁻¹ => 3x²."},
        {"q": "∫2x dx = ?", "o": ["x", "x²+C", "2x²", "2+C"], "a": 1, "e": "∫2x dx = x² + C."},
        {"q": "5! = ?", "o": ["25", "60", "120", "720"], "a": 2, "e": "5×4×3×2×1 = 120."},
        {"q": "What is the value of sin(90°)?", "o": ["0", "0.5", "1", "undefined"], "a": 2, "e": "sin(90°) = 1."},
        {"q": "Solve for x: x² - 9 = 0", "o": ["x = 3 only", "x = -3 only", "x = ±3", "x = 9"], "a": 2, "e": "x² = 9 => x = 3 or x = -3."},
        {"q": "Sum of interior angles of a triangle?", "o": ["90°", "180°", "270°", "360°"], "a": 1, "e": "Triangle interior angles always sum to 180°."},
        {"q": "What is the gradient (slope) of the line y = 3x + 2?", "o": ["2", "3", "5", "1/3"], "a": 1, "e": "In y=mx+c, m is the gradient; here m=3."},
        {"q": "What is 3⁴?", "o": ["12", "64", "81", "243"], "a": 2, "e": "3×3×3×3 = 81."},
    ],
    'BCH': [
        {"q": "What is the monomer of proteins?", "o": ["Nucleotides", "Amino acids", "Monosaccharides", "Fatty acids"], "a": 1, "e": "Amino acids link via peptide bonds to form proteins."},
        {"q": "Which enzyme breaks down starch?", "o": ["Pepsin", "Amylase", "Lipase", "Trypsin"], "a": 1, "e": "Amylase hydrolyzes starch into simpler sugars."},
        {"q": "Where does glycolysis occur in the cell?", "o": ["Mitochondria", "Nucleus", "Cytoplasm", "Ribosome"], "a": 2, "e": "Glycolysis takes place in the cytoplasm."},
        {"q": "Which vitamin is essential for blood clotting?", "o": ["Vitamin A", "Vitamin C", "Vitamin K", "Vitamin D"], "a": 2, "e": "Vitamin K activates clotting factors."},
        {"q": "DNA's sugar component is:", "o": ["Ribose", "Deoxyribose", "Glucose", "Fructose"], "a": 1, "e": "DNA contains deoxyribose; RNA contains ribose."},
        {"q": "The pH of a neutral solution is:", "o": ["0", "7", "14", "1"], "a": 1, "e": "Pure water/neutral solutions have pH 7."},
        {"q": "Lipids are primarily used in the body for:", "o": ["Energy storage and membranes", "Genetic information", "Oxygen transport only", "Muscle contraction only"], "a": 0, "e": "Lipids store energy and form cell membranes."},
        {"q": "Which bond links amino acids together?", "o": ["Glycosidic bond", "Peptide bond", "Ester bond", "Hydrogen bond"], "a": 1, "e": "Peptide bonds form between the carboxyl and amino groups of amino acids."},
    ],
    'CSC': [
        {"q": "CPU stands for?", "o": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Process Unit"], "a": 0, "e": "CPU = Central Processing Unit."},
        {"q": "Binary equivalent of decimal 10?", "o": ["1001", "1010", "1100", "1110"], "a": 1, "e": "8+2 = 1010 in binary."},
        {"q": "RAM stands for?", "o": ["Read Access Memory", "Random Access Memory", "Read And Modify", "Rapid Access Module"], "a": 1, "e": "RAM = Random Access Memory."},
        {"q": "Which is a high-level programming language?", "o": ["Machine code", "Assembly", "Python", "Binary"], "a": 2, "e": "Python is a high-level language; machine code/binary/assembly are low-level."},
        {"q": "HTML stands for:", "o": ["Hyper Text Markup Language", "High Text Manual Language", "Hyperlink Text Markup Language", "Home Tool Markup Language"], "a": 0, "e": "HTML = Hyper Text Markup Language."},
        {"q": "What does OS stand for in computing?", "o": ["Operating System", "Output Signal", "Online Storage", "Optical Sensor"], "a": 0, "e": "OS = Operating System."},
        {"q": "Which data structure uses LIFO (Last In, First Out)?", "o": ["Queue", "Stack", "Array", "Linked list"], "a": 1, "e": "A stack pops the most recently pushed item first (LIFO)."},
        {"q": "1 byte equals how many bits?", "o": ["4", "8", "16", "32"], "a": 1, "e": "1 byte = 8 bits."},
    ],
    'PHY': [
        {"q": "Newton's 2nd Law of Motion states:", "o": ["F=ma", "F=mv", "F=½mv²", "F=mg"], "a": 0, "e": "Force = mass × acceleration."},
        {"q": "Speed of light in a vacuum is approximately:", "o": ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "300 km/s"], "a": 0, "e": "c ≈ 3×10⁸ m/s."},
        {"q": "The SI unit of force is:", "o": ["Joule", "Newton", "Watt", "Pascal"], "a": 1, "e": "Force is measured in Newtons (N)."},
        {"q": "Ohm's Law is expressed as:", "o": ["V = IR", "V = I/R", "V = I+R", "V = I-R"], "a": 0, "e": "Voltage = Current × Resistance."},
        {"q": "The SI unit of electric current is:", "o": ["Volt", "Ampere", "Ohm", "Watt"], "a": 1, "e": "Current is measured in Amperes (A)."},
        {"q": "Which quantity is measured in Joules?", "o": ["Force", "Energy/Work", "Power", "Current"], "a": 1, "e": "Energy and work are measured in Joules."},
        {"q": "The acceleration due to gravity on Earth is approximately:", "o": ["9.8 m/s²", "6.4 m/s²", "3.2 m/s²", "12.0 m/s²"], "a": 0, "e": "g ≈ 9.8 m/s² near Earth's surface."},
    ],
    'CHM': [
        {"q": "Atomic number of Carbon?", "o": ["4", "6", "8", "12"], "a": 1, "e": "Carbon has 6 protons, so atomic number 6."},
        {"q": "What type of bond forms in NaCl?", "o": ["Covalent", "Ionic", "Metallic", "Hydrogen"], "a": 1, "e": "Na donates an electron to Cl, forming an ionic bond."},
        {"q": "The pH scale ranges from:", "o": ["0–7", "0–14", "1–10", "0–100"], "a": 1, "e": "The standard pH scale runs from 0 to 14."},
        {"q": "Which of these is a noble gas?", "o": ["Oxygen", "Nitrogen", "Argon", "Hydrogen"], "a": 2, "e": "Argon is a noble gas (Group 18)."},
        {"q": "Avogadro's number is approximately:", "o": ["6.022×10²³", "3.14×10⁸", "9.8×10²", "1.6×10⁻¹⁹"], "a": 0, "e": "Avogadro's number ≈ 6.022×10²³ per mole."},
        {"q": "The chemical formula for water is:", "o": ["H₂O", "HO₂", "H₃O", "H₂O₂"], "a": 0, "e": "Water is H₂O — two hydrogen atoms bonded to one oxygen."},
        {"q": "Which particle has a negative charge?", "o": ["Proton", "Neutron", "Electron", "Nucleus"], "a": 2, "e": "Electrons carry a negative charge."},
    ],
    'MCB': [
        {"q": "Which of these is a prokaryote?", "o": ["Yeast", "Bacteria", "Algae", "Protozoa"], "a": 1, "e": "Bacteria lack a membrane-bound nucleus (prokaryotic)."},
        {"q": "Gram staining differentiates bacteria based on:", "o": ["Cell wall composition/thickness", "DNA content", "Flagella number", "Spore presence"], "a": 0, "e": "Gram-positive bacteria have a thick peptidoglycan layer that retains crystal violet stain."},
        {"q": "Viruses are best described as:", "o": ["Free-living cells", "Obligate intracellular parasites", "A type of bacteria", "A type of fungus"], "a": 1, "e": "Viruses can only replicate inside a host cell."},
        {"q": "Which equipment sterilizes lab materials using pressurized steam?", "o": ["Autoclave", "Refrigerator", "Centrifuge", "Microscope"], "a": 0, "e": "An autoclave uses high-pressure steam to sterilize equipment."},
        {"q": "Antibiotics are generally effective against:", "o": ["Viruses", "Bacteria", "Prions", "All pathogens equally"], "a": 1, "e": "Antibiotics target bacterial cell processes, not viruses."},
        {"q": "Which of these is a fungus?", "o": ["E. coli", "Saccharomyces (yeast)", "Influenza virus", "Plasmodium"], "a": 1, "e": "Yeast (Saccharomyces) is a unicellular fungus."},
    ],
    'GST': [
        {"q": "Which sentence has correct subject-verb agreement?", "o": ["The list of items are on the table", "The list of items is on the table", "The lists of item is on the table", "The list of item are on the table"], "a": 1, "e": "'List' is singular, so it takes the singular verb 'is'."},
        {"q": "Which word is a synonym for 'ubiquitous'?", "o": ["Rare", "Widespread", "Hidden", "Temporary"], "a": 1, "e": "'Ubiquitous' means present/found everywhere — 'widespread'."},
        {"q": "Which sentence is correctly punctuated?", "o": ["Its a beautiful day", "It's a beautiful day", "Its' a beautiful day", "It is' a beautiful day"], "a": 1, "e": "'It's' is the correct contraction of 'it is'."},
        {"q": "A figure of speech that compares two unlike things using 'like' or 'as' is called a:", "o": ["Metaphor", "Simile", "Hyperbole", "Personification"], "a": 1, "e": "A simile explicitly uses 'like' or 'as' to compare."},
        {"q": "Nigeria gained independence from Britain in:", "o": ["1957", "1960", "1963", "1966"], "a": 1, "e": "Nigeria became independent on 1 October 1960."},
        {"q": "Nigeria became a republic in:", "o": ["1960", "1963", "1970", "1979"], "a": 1, "e": "Nigeria became a republic on 1 October 1963."},
        {"q": "'Ad hominem' is an example of a:", "o": ["Fallacy that attacks the person, not the argument", "Valid logical proof", "Mathematical theorem", "Grammar rule"], "a": 0, "e": "Ad hominem attacks the arguer rather than addressing the argument."},
        {"q": "Citizenship primarily refers to:", "o": ["Membership of a political community with rights and duties", "Ownership of property", "Membership of a religious group", "Employment status"], "a": 0, "e": "Citizenship is legal membership of a state, carrying rights and responsibilities."},
        {"q": "Which approach best describes peaceful conflict resolution?", "o": ["Negotiation and dialogue", "Use of force", "Ignoring the conflict", "Litigation only"], "a": 0, "e": "Negotiation/dialogue resolves disputes without violence."},
        {"q": "Which word is opposite in meaning to 'candid'?", "o": ["Honest", "Deceptive", "Blunt", "Direct"], "a": 1, "e": "'Candid' means honest/open; its opposite is 'deceptive'."},
    ],
    'BOT': [
        {"q": "The basic unit of classification in the plant kingdom is:", "o": ["Genus", "Species", "Family", "Order"], "a": 1, "e": "Species is the fundamental taxonomic unit."},
        {"q": "Photosynthesis primarily occurs in which organelle?", "o": ["Mitochondria", "Chloroplast", "Nucleus", "Ribosome"], "a": 1, "e": "Chloroplasts contain chlorophyll and carry out photosynthesis."},
        {"q": "Which pigment is primarily responsible for photosynthesis?", "o": ["Carotenoid", "Chlorophyll", "Anthocyanin", "Xanthophyll"], "a": 1, "e": "Chlorophyll absorbs light energy for photosynthesis."},
        {"q": "The vascular tissue that transports water in plants is:", "o": ["Phloem", "Xylem", "Cambium", "Cortex"], "a": 1, "e": "Xylem conducts water and minerals from roots upward."},
        {"q": "Which of these is a non-vascular plant group?", "o": ["Angiosperms", "Gymnosperms", "Bryophytes", "Pteridophytes"], "a": 2, "e": "Bryophytes (mosses) lack true vascular tissue."},
        {"q": "The loss of water vapor through leaves is called:", "o": ["Respiration", "Transpiration", "Translocation", "Photosynthesis"], "a": 1, "e": "Transpiration is water loss via stomata on leaves."},
        {"q": "Which flower part produces pollen?", "o": ["Stigma", "Anther", "Ovary", "Sepal"], "a": 1, "e": "The anther, part of the stamen, produces pollen."},
        {"q": "Angiosperms are characterized by having:", "o": ["Naked seeds", "Covered/enclosed seeds", "No seeds", "Spores only"], "a": 1, "e": "Angiosperm seeds are enclosed within a fruit/ovary."},
        {"q": "The study of fungi is called:", "o": ["Mycology", "Bacteriology", "Virology", "Phycology"], "a": 0, "e": "Mycology is the scientific study of fungi."},
        {"q": "Which gas do plants absorb during photosynthesis?", "o": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "a": 1, "e": "Plants absorb CO₂ and release O₂ during photosynthesis."},
    ],
    'BIO': [
        {"q": "The basic unit of life is the:", "o": ["Tissue", "Cell", "Organ", "Organism"], "a": 1, "e": "The cell is the smallest structural/functional unit of life."},
        {"q": "Which organelle is known as the 'powerhouse of the cell'?", "o": ["Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"], "a": 1, "e": "Mitochondria generate ATP through respiration."},
        {"q": "DNA stands for:", "o": ["Deoxyribonucleic acid", "Dinitrogen acid", "Deoxyribose nuclear acid", "Diribonucleic acid"], "a": 0, "e": "DNA = Deoxyribonucleic acid."},
        {"q": "Which of these is NOT one of Mendel's laws of inheritance?", "o": ["Law of segregation", "Law of independent assortment", "Law of dominance", "Law of natural selection"], "a": 3, "e": "Natural selection is Darwin's theory, not one of Mendel's inheritance laws."},
        {"q": "The type of cell division that produces gametes is:", "o": ["Mitosis", "Meiosis", "Binary fission", "Budding"], "a": 1, "e": "Meiosis produces haploid gametes for sexual reproduction."},
        {"q": "Which blood cells primarily fight infection?", "o": ["Red blood cells", "White blood cells", "Platelets", "Plasma"], "a": 1, "e": "White blood cells (leukocytes) are part of the immune response."},
        {"q": "Which is an example of asexual reproduction?", "o": ["Budding in yeast", "Fertilization in humans", "Cross-pollination", "Meiosis"], "a": 0, "e": "Budding produces offspring from a single parent without gametes."},
        {"q": "The theory of evolution by natural selection was proposed by:", "o": ["Gregor Mendel", "Charles Darwin", "Louis Pasteur", "Robert Hooke"], "a": 1, "e": "Charles Darwin proposed natural selection in 'On the Origin of Species'."},
        {"q": "Enzymes are primarily made of:", "o": ["Carbohydrates", "Lipids", "Proteins", "Nucleic acids"], "a": 2, "e": "Enzymes are biological catalysts made of protein."},
        {"q": "Homeostasis refers to:", "o": ["Cell division", "Maintenance of stable internal conditions", "Growth of an organism", "Reproduction"], "a": 1, "e": "Homeostasis keeps internal conditions (temperature, pH, etc.) stable."},
    ],
    'FIS': [
        {"q": "The scientific study of fish is called:", "o": ["Ichthyology", "Ornithology", "Herpetology", "Entomology"], "a": 0, "e": "Ichthyology is the branch of zoology studying fish."},
        {"q": "Fish primarily respire using:", "o": ["Lungs", "Gills", "Skin only", "Trachea"], "a": 1, "e": "Gills extract dissolved oxygen from water."},
        {"q": "Bony fish (Osteichthyes) are characterized by:", "o": ["Cartilaginous skeleton", "Bony skeleton", "No skeleton", "Exoskeleton"], "a": 1, "e": "Osteichthyes have a skeleton made of bone."},
        {"q": "Aquaculture refers to:", "o": ["Farming of aquatic organisms under controlled conditions", "Wild capture fishing only", "Fish processing", "Deep sea diving"], "a": 0, "e": "Aquaculture is the controlled cultivation of aquatic organisms."},
        {"q": "Which organ helps bony fish maintain buoyancy?", "o": ["Liver", "Swim bladder", "Gills", "Heart"], "a": 1, "e": "The swim bladder adjusts gas volume to control buoyancy."},
        {"q": "Cartilaginous fish (Chondrichthyes) include:", "o": ["Tilapia and Catfish", "Sharks and Rays", "Salmon and Tuna", "Eels and Cod"], "a": 1, "e": "Sharks and rays have cartilage, not bone, skeletons."},
        {"q": "The lateral line system in fish is used for:", "o": ["Digestion", "Detecting water movement/vibration", "Reproduction", "Respiration"], "a": 1, "e": "The lateral line senses pressure changes and vibrations in water."},
        {"q": "Tilapia, commonly farmed in Nigeria, belongs to the family:", "o": ["Cichlidae", "Salmonidae", "Gadidae", "Anguillidae"], "a": 0, "e": "Tilapia species belong to family Cichlidae."},
    ],
    'ENT': [
        {"q": "An entrepreneur is best defined as someone who:", "o": ["Works for a fixed salary", "Identifies opportunities and takes risks to start a business", "Only invests in stocks", "Manages government agencies"], "a": 1, "e": "Entrepreneurship centers on opportunity identification and risk-taking to build a venture."},
        {"q": "Which is a key characteristic of a successful entrepreneur?", "o": ["Risk aversion", "Innovation", "Avoiding change", "Working in isolation always"], "a": 1, "e": "Innovation drives new products/processes that create value."},
        {"q": "A business plan primarily helps to:", "o": ["Guarantee profit", "Outline goals, strategy and financial projections", "Avoid taxes", "Replace marketing"], "a": 1, "e": "A business plan documents strategy, goals and finances for the venture."},
        {"q": "SWOT stands for:", "o": ["Strengths, Weaknesses, Opportunities, Threats", "Sales, Work, Output, Tax", "Strategy, Wealth, Operations, Trade", "Skills, Wages, Opportunities, Trends"], "a": 0, "e": "SWOT = Strengths, Weaknesses, Opportunities, Threats."},
        {"q": "A sole proprietorship is a business owned by:", "o": ["Two or more partners", "One person", "The government", "Shareholders only"], "a": 1, "e": "A sole proprietorship has a single owner who bears full responsibility."},
        {"q": "Venture capital refers to:", "o": ["A government loan", "Funding provided to startups with high growth potential", "Personal savings only", "A bank overdraft"], "a": 1, "e": "Venture capital is investment funding for high-growth-potential startups."},
        {"q": "Market segmentation refers to:", "o": ["Dividing a market into distinct groups of buyers", "Setting a single price for all", "Selling only online", "Reducing production costs"], "a": 0, "e": "Segmentation groups customers by shared characteristics to target them effectively."},
    ],
    'SLT': [
        {"q": "Which equipment measures precise volumes of liquid?", "o": ["Beaker", "Pipette", "Test tube", "Funnel"], "a": 1, "e": "A pipette delivers accurately measured liquid volumes."},
        {"q": "The primary purpose of a Bunsen burner in the lab is to:", "o": ["Cool samples", "Provide a heat source", "Measure pH", "Filter solutions"], "a": 1, "e": "A Bunsen burner provides a controllable open flame for heating."},
        {"q": "Which safety equipment protects the eyes during lab work?", "o": ["Lab coat", "Safety goggles", "Gloves", "Apron"], "a": 1, "e": "Safety goggles shield eyes from splashes and fumes."},
        {"q": "A centrifuge is used to:", "o": ["Separate substances of different densities by spinning", "Heat samples", "Measure mass", "Filter gases"], "a": 0, "e": "Centrifugation separates components by density under centrifugal force."},
        {"q": "The correct first step when there is a chemical spill is to:", "o": ["Ignore it", "Alert others and follow safety protocol", "Clean with bare hands", "Leave without reporting"], "a": 1, "e": "Spills should be reported immediately and handled per safety protocol."},
        {"q": "A pH meter is used to measure:", "o": ["Temperature", "Acidity or alkalinity of a solution", "Volume", "Mass"], "a": 1, "e": "A pH meter measures how acidic or alkaline a solution is."},
        {"q": "Which glassware is calibrated for accurate volume measurement?", "o": ["Beaker", "Volumetric flask", "Test tube", "Petri dish"], "a": 1, "e": "Volumetric flasks are calibrated to hold a precise volume."},
    ],
    'ACC': [
        {"q": "The accounting equation is:", "o": ["Assets = Liabilities + Owner's Equity", "Assets = Liabilities − Equity", "Assets + Liabilities = Equity", "Revenue = Expenses"], "a": 0, "e": "The fundamental accounting equation balances assets against liabilities plus equity."},
        {"q": "Which financial statement shows profit or loss over a period?", "o": ["Balance sheet", "Income statement", "Cash flow statement", "Trial balance"], "a": 1, "e": "The income statement reports revenues, expenses and resulting profit/loss."},
        {"q": "Double-entry bookkeeping means every transaction affects:", "o": ["One account only", "At least two accounts", "Only cash accounts", "Only revenue accounts"], "a": 1, "e": "Every transaction has a debit and a corresponding credit entry."},
        {"q": "A debit entry typically increases:", "o": ["Liabilities and equity", "Assets and expenses", "Revenue only", "Nothing"], "a": 1, "e": "Debits increase asset and expense accounts."},
        {"q": "Depreciation is best described as:", "o": ["Increase in asset value", "Allocation of an asset's cost over its useful life", "A type of revenue", "A liability"], "a": 1, "e": "Depreciation spreads an asset's cost across the periods it is used."},
        {"q": "The trial balance is used to:", "o": ["Check arithmetic accuracy of ledger accounts", "Calculate tax", "Record cash sales", "File annual returns"], "a": 0, "e": "A trial balance verifies that total debits equal total credits."},
        {"q": "Which of these is a current asset?", "o": ["Building", "Cash", "Long-term investment", "Goodwill"], "a": 1, "e": "Cash is a current asset — readily available/liquid."},
        {"q": "Accrual accounting recognizes revenue when it is:", "o": ["Cash is received", "Earned, regardless of cash receipt", "The year ends", "Invoices are printed"], "a": 1, "e": "Accrual accounting records revenue when earned, not necessarily when cash changes hands."},
    ],
    'BUS': [
        {"q": "Management is best defined as:", "o": ["Owning a business", "The process of planning, organizing, leading and controlling resources", "Selling products only", "Hiring employees only"], "a": 1, "e": "Management covers planning, organizing, leading and controlling organizational resources."},
        {"q": "Which is NOT one of the four core management functions (POLC)?", "o": ["Planning", "Organizing", "Leading", "Advertising"], "a": 3, "e": "POLC = Planning, Organizing, Leading, Controlling — advertising is a marketing function."},
        {"q": "A SWOT analysis examines:", "o": ["Strengths, Weaknesses, Opportunities, Threats", "Sales figures only", "Staff performance only", "Competitors only"], "a": 0, "e": "SWOT evaluates internal strengths/weaknesses and external opportunities/threats."},
        {"q": "Which organizational structure has a clear single chain of command?", "o": ["Matrix structure", "Line/hierarchical structure", "Flat structure", "Network structure"], "a": 1, "e": "A line structure has authority flowing directly top to bottom."},
        {"q": "The marketing mix (4Ps) consists of:", "o": ["Product, Price, Place, Promotion", "Profit, People, Process, Physical evidence", "Plan, Policy, Process, Product", "Profit, Price, Plan, People"], "a": 0, "e": "The classic 4Ps: Product, Price, Place, Promotion."},
        {"q": "A leadership style where the leader decides with little input from subordinates is:", "o": ["Democratic", "Autocratic", "Laissez-faire", "Transformational"], "a": 1, "e": "Autocratic leaders make decisions unilaterally."},
        {"q": "Human Resource Management primarily deals with:", "o": ["Managing an organization's workforce", "Managing finances only", "Managing production only", "Managing IT systems only"], "a": 0, "e": "HRM covers recruitment, training, performance and welfare of employees."},
    ],
    'AGR': [
        {"q": "Agronomy is the branch of agriculture concerned with:", "o": ["Animal breeding", "Crop production and soil management", "Fish farming", "Forestry only"], "a": 1, "e": "Agronomy focuses on crop science and soil management."},
        {"q": "Which of these is a leguminous crop?", "o": ["Maize", "Cowpea", "Rice", "Sorghum"], "a": 1, "e": "Cowpea is a legume that fixes atmospheric nitrogen via root nodules."},
        {"q": "The three primary macronutrients for plants (NPK) are:", "o": ["Nitrogen, Phosphorus, Potassium", "Calcium, Iron, Zinc", "Carbon, Hydrogen, Oxygen", "Sulfur, Boron, Copper"], "a": 0, "e": "NPK = Nitrogen, Phosphorus, Potassium, the main plant macronutrients."},
        {"q": "Crop rotation is practiced primarily to:", "o": ["Increase soil fertility and reduce pest buildup", "Reduce rainfall", "Increase land size", "Reduce labor only"], "a": 0, "e": "Rotating crops restores soil nutrients and interrupts pest/disease cycles."},
        {"q": "Growing different crops together on the same land is called:", "o": ["Monocropping", "Mixed/intercropping", "Fallowing", "Shifting cultivation"], "a": 1, "e": "Intercropping grows multiple crops together to maximize land use."},
        {"q": "Adding organic matter to improve soil fertility is called:", "o": ["Irrigation", "Composting/manuring", "Pesticide application", "Harvesting"], "a": 1, "e": "Composting/manuring enriches soil with organic nutrients."},
        {"q": "Livestock husbandry refers to:", "o": ["Growing crops", "Breeding and raising farm animals", "Fishing", "Forestry management"], "a": 1, "e": "Husbandry involves the breeding, feeding and care of farm animals."},
    ],
    'STA': [
        {"q": "The measure of central tendency representing the middle value in ordered data is:", "o": ["Mean", "Median", "Mode", "Range"], "a": 1, "e": "The median is the middle value when data is arranged in order."},
        {"q": "The mode of a dataset is:", "o": ["The average", "The middle value", "The most frequently occurring value", "The difference between max and min"], "a": 2, "e": "Mode = the value that appears most often."},
        {"q": "Standard deviation measures:", "o": ["Central tendency", "Dispersion/spread of data", "Probability", "Correlation"], "a": 1, "e": "Standard deviation quantifies how spread out data values are."},
        {"q": "A probability value must always lie between:", "o": ["-1 and 1", "0 and 1", "0 and 100", "1 and 10"], "a": 1, "e": "Probabilities range from 0 (impossible) to 1 (certain)."},
        {"q": "Which graph best shows the frequency distribution of continuous data?", "o": ["Pie chart", "Histogram", "Line graph only", "Scatter plot only"], "a": 1, "e": "A histogram displays frequency distribution of continuous, grouped data."},
        {"q": "The range of a dataset is calculated as:", "o": ["Sum of all values", "Maximum minus minimum value", "Mean divided by count", "The middle value"], "a": 1, "e": "Range = highest value − lowest value."},
        {"q": "In a perfectly normal distribution, the mean, median and mode are:", "o": ["Always different", "Equal", "Unrelated", "Always zero"], "a": 1, "e": "A normal distribution is symmetric, so mean = median = mode."},
    ],
    'ZOO': [
        {"q": "The classification unit directly below Kingdom is:", "o": ["Species", "Phylum", "Genus", "Family"], "a": 1, "e": "Taxonomic order: Kingdom > Phylum > Class > Order > Family > Genus > Species."},
        {"q": "Which is a characteristic of all mammals?", "o": ["Cold-blooded", "Presence of mammary glands", "Laying eggs only", "Gills for respiration"], "a": 1, "e": "Mammary glands (milk production) define the mammal class."},
        {"q": "Animals without a backbone are called:", "o": ["Vertebrates", "Invertebrates", "Mammals", "Chordates"], "a": 1, "e": "Invertebrates lack a vertebral column (e.g. insects, worms)."},
        {"q": "Insects belong to which phylum?", "o": ["Mollusca", "Arthropoda", "Annelida", "Chordata"], "a": 1, "e": "Insects are arthropods, characterized by jointed legs and an exoskeleton."},
        {"q": "Amphibians are characterized by:", "o": ["Living exclusively in water", "Dual life stages (aquatic larva, terrestrial adult)", "Having feathers", "Being warm-blooded"], "a": 1, "e": "Amphibians typically develop as aquatic larvae before becoming terrestrial adults."},
        {"q": "Maintaining a stable internal body temperature is called:", "o": ["Osmoregulation", "Thermoregulation", "Digestion", "Excretion"], "a": 1, "e": "Thermoregulation keeps body temperature within a stable range."},
        {"q": "Which of these is a cold-blooded (ectothermic) animal?", "o": ["Human", "Dog", "Lizard", "Bird"], "a": 2, "e": "Reptiles like lizards are ectothermic — their body temperature depends on the environment."},
    ],
    'ECO': [
        {"q": "The basic economic problem arises from:", "o": ["Too much government", "Scarcity of resources relative to unlimited wants", "Overproduction", "Excess supply"], "a": 1, "e": "Economics studies how scarce resources are allocated against unlimited wants."},
        {"q": "Demand refers to:", "o": ["The quantity producers wish to sell", "The quantity consumers are willing and able to buy at a price", "Total goods in the market", "Government spending"], "a": 1, "e": "Demand is willingness and ability to purchase at a given price."},
        {"q": "According to the law of demand, as price rises, quantity demanded:", "o": ["Increases", "Decreases", "Remains constant", "Doubles"], "a": 1, "e": "Price and quantity demanded are inversely related, ceteris paribus."},
        {"q": "Opportunity cost refers to:", "o": ["The monetary cost only", "The value of the next best alternative forgone", "Total cost of production", "Government tax"], "a": 1, "e": "Opportunity cost is what you give up by choosing one option over the next best one."},
        {"q": "GDP stands for:", "o": ["Gross Domestic Product", "General Domestic Profit", "Gross Development Plan", "Government Data Point"], "a": 0, "e": "GDP = Gross Domestic Product, the total value of goods/services produced in a country."},
        {"q": "Inflation refers to:", "o": ["A general and sustained rise in price levels", "A fall in prices", "An increase in wages only", "A decrease in money supply"], "a": 0, "e": "Inflation is a sustained increase in the general price level over time."},
        {"q": "A market structure with only one seller is called:", "o": ["Perfect competition", "Monopoly", "Oligopoly", "Monopsony"], "a": 1, "e": "A monopoly exists when a single firm supplies the entire market."},
    ],
}
# Aliases: the same subject is taught under a different course-code prefix at some
# schools/levels (e.g. LASU uses both MTH and MAT for Mathematics, and both GST and
# GES for General Studies) -- copied from CBT.html's own aliasing.
CBT_TEMPLATES['MAT'] = CBT_TEMPLATES['MTH']
CBT_TEMPLATES['GES'] = CBT_TEMPLATES['GST']

# ---- Written/essay bank, copied verbatim from CBT.html's writtenTemplates --------
WRITTEN_TEMPLATES = {
    'MTH': [
        {"q": "Prove that the sum of the first n natural numbers is n(n+1)/2, using mathematical induction.", "ms": "Base case n=1: 1 = 1(2)/2 = 1 ✓. Inductive step: assume true for n=k, i.e. sum = k(k+1)/2. For n=k+1: sum = k(k+1)/2 + (k+1) = (k+1)(k+2)/2, matching the formula. Hence true for all n by induction."},
        {"q": "Solve the quadratic equation x² − 5x + 6 = 0 and show your working.", "ms": "Factorize: x² − 5x + 6 = (x−2)(x−3) = 0. So x = 2 or x = 3. Verify: 2²−5(2)+6=0 ✓, 3²−5(3)+6=0 ✓."},
    ],
    'BCH': [
        {"q": "Describe the fluid mosaic model of cell membrane structure.", "ms": "The membrane is a phospholipid bilayer with embedded/peripheral proteins. Hydrophobic fatty-acid tails face inward, hydrophilic phosphate heads face outward toward the aqueous environment. The bilayer's fluidity allows lateral movement of lipids and proteins, enabling functions like transport, signaling and cell recognition."},
        {"q": "Outline the main stages of cellular respiration and where each occurs.", "ms": "Glycolysis (cytoplasm): glucose → 2 pyruvate, net 2 ATP. Krebs cycle (mitochondrial matrix): pyruvate fully oxidized, produces NADH/FADH2 and CO2. Electron transport chain (inner mitochondrial membrane): NADH/FADH2 drive ATP synthesis via oxidative phosphorylation, producing the bulk of ATP."},
    ],
    'CSC': [
        {"q": "Describe the Von Neumann computer architecture.", "ms": "Consists of CPU (Arithmetic Logic Unit + Control Unit), Memory (stores both data and instructions in the same address space), and Input/Output devices, connected by a system bus. Operates on the fetch-decode-execute cycle: instructions are fetched from memory, decoded by the control unit, and executed by the ALU."},
        {"q": "Explain the difference between compiled and interpreted programming languages, with examples.", "ms": "Compiled languages (e.g. C, C++) are translated entirely into machine code by a compiler before execution, producing a standalone executable — generally faster but needs recompilation after changes. Interpreted languages (e.g. Python, JavaScript) are executed line-by-line by an interpreter at runtime — generally slower but more flexible for quick testing/changes."},
    ],
    'PHY': [
        {"q": "State Newton's three laws of motion, with a real-world example of each.", "ms": "1st Law (Inertia): an object stays at rest or in uniform motion unless acted on by a net force — e.g. passengers lurch forward when a car brakes suddenly. 2nd Law: F = ma — e.g. pushing a loaded cart requires more force than pushing an empty one for the same acceleration. 3rd Law: every action has an equal and opposite reaction — e.g. a rocket expels gas downward and is propelled upward."},
        {"q": "Explain the difference between speed and velocity.", "ms": "Speed is a scalar quantity — distance traveled per unit time, with magnitude only. Velocity is a vector quantity — displacement per unit time, having both magnitude and direction. Two objects can have the same speed but different velocities if moving in different directions."},
    ],
    'CHM': [
        {"q": "Describe the structure of an atom, including its subatomic particles.", "ms": "An atom has a central nucleus containing protons (charge +1, mass ≈1 amu) and neutrons (charge 0, mass ≈1 amu), surrounded by electrons (charge -1, negligible mass) occupying shells/orbitals around the nucleus. The number of protons (atomic number) defines the element."},
        {"q": "Explain the difference between ionic and covalent bonding, with an example of each.", "ms": "Ionic bonding: transfer of electrons between atoms, forming oppositely charged ions held by electrostatic attraction — e.g. NaCl (Na loses an electron to Cl). Covalent bonding: atoms share electron pairs to achieve stability — e.g. H2O, where oxygen shares electrons with two hydrogen atoms."},
    ],
    'MCB': [
        {"q": "Explain the Gram staining procedure and its significance in microbiology.", "ms": "Steps: apply crystal violet (primary stain) → apply iodine (mordant, fixes the dye) → decolorize with alcohol/acetone → counterstain with safranin. Gram-positive bacteria retain crystal violet (thick peptidoglycan wall) and appear purple; Gram-negative bacteria lose crystal violet during decolorization and take up safranin, appearing pink/red. This distinction guides antibiotic choice and bacterial identification."},
        {"q": "Describe the general structure of a bacterial cell.", "ms": "Prokaryotic cell lacking a membrane-bound nucleus; genetic material (a single circular chromosome) is in the nucleoid region. Surrounded by a cell membrane and a cell wall (peptidoglycan). May have a capsule, flagella (movement), pili (attachment/conjugation), and ribosomes for protein synthesis, but no membrane-bound organelles."},
    ],
    'GST': [
        {"q": "Discuss the importance of effective communication skills for a university student.", "ms": "Supports academic success (clear essays, presentations, comprehension of lectures), professional readiness (job interviews, workplace reports), stronger interpersonal relationships, sharper critical thinking, and meaningful civic/community participation."},
        {"q": "Explain the concept of citizenship and its responsibilities in a democratic society.", "ms": "Citizenship is legal membership of a state carrying both rights (voting, protection under the law, freedom of expression) and duties (obeying laws, paying taxes, jury/civic service where applicable). It also involves active political participation and a sense of national identity and social responsibility."},
    ],
    'BOT': [
        {"q": "Describe the process of photosynthesis, including the raw materials and products involved.", "ms": "Photosynthesis has light-dependent reactions (thylakoid membrane) and light-independent reactions/Calvin cycle (stroma), occurring in chloroplasts. Raw materials: carbon dioxide (via stomata), water (from roots), and light energy. Products: glucose (C6H12O6) and oxygen. Overall equation: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2."},
        {"q": "Classify the plant kingdom into its major divisions, with an example of each.", "ms": "Thallophyta (algae, e.g. Spirogyra) — non-vascular, undifferentiated body. Bryophyta (mosses, e.g. Funaria) — non-vascular, simple tissue differentiation. Pteridophyta (ferns, e.g. Nephrolepis) — vascular, spore-producing. Spermatophyta (seed plants) — split into Gymnospermae (naked seeds, e.g. Pinus) and Angiospermae (covered seeds, e.g. most flowering plants)."},
    ],
    'BIO': [
        {"q": "Explain the structure and function of the cell membrane.", "ms": "A phospholipid bilayer with embedded and peripheral proteins (the fluid mosaic model). Functions include selective permeability (controlling what enters/exits the cell), physical protection, cell signaling via receptor proteins, and cell recognition via surface glycoproteins."},
        {"q": "Differentiate between mitosis and meiosis.", "ms": "Mitosis: a single division producing two genetically identical diploid daughter cells, used for growth and tissue repair. Meiosis: two successive divisions producing four genetically varied haploid daughter cells (gametes), involving crossing-over, used for sexual reproduction."},
    ],
    'FIS': [
        {"q": "Discuss the importance of fisheries and aquaculture to the Nigerian economy.", "ms": "Provides a major source of animal protein and food security; generates employment in fishing/farming communities; contributes income and export earnings; supplies raw materials to related industries (e.g. fishmeal for animal feed); sustains livelihoods in coastal and riverine communities."},
        {"q": "Describe the external morphology of a typical bony fish.", "ms": "Streamlined body divided into head, trunk and tail. Fins — dorsal, pectoral, pelvic, anal and caudal — aid movement and balance. Body covered by protective scales. The lateral line senses water vibration/pressure. The operculum (gill cover) protects the gills used for respiration."},
    ],
    'ENT': [
        {"q": "Discuss the key elements that should be included in a business plan.", "ms": "Executive summary, business description, market/competitor analysis, organizational structure, product/service description, marketing and sales strategy, operations plan, financial projections, and funding requirements."},
        {"q": "Explain the difference between an entrepreneur and a manager.", "ms": "An entrepreneur initiates and owns a business venture, bears financial risk, and drives innovation. A manager is typically employed to run day-to-day operations, implements existing strategy within an established structure, and does not necessarily bear the venture's financial risk."},
    ],
    'SLT': [
        {"q": "Discuss the general safety precautions to observe in a science laboratory.", "ms": "Wear appropriate PPE (lab coat, safety goggles, gloves); no eating or drinking in the lab; know the location of safety equipment (fire extinguisher, eyewash station, first aid kit); handle chemicals with care and read labels; never pipette by mouth; dispose of waste according to protocol; report accidents/spills immediately."},
        {"q": "Explain the procedure for calibrating a laboratory weighing balance.", "ms": "Place the balance on a stable, level, vibration-free surface. Clean the weighing pan. Zero/tare the balance before use. Use certified reference/calibration weights to check accuracy across the working range. Record any deviation and adjust or service the balance; recalibrate periodically as part of routine quality control."},
    ],
    'ACC': [
        {"q": "Explain the accounting equation and illustrate it with an example.", "ms": "Assets = Liabilities + Owner's Equity. Example: a business buys equipment worth ₦500,000, financed by ₦200,000 cash from the owner and a ₦300,000 bank loan. Assets (equipment, ₦500,000) = Liabilities (loan, ₦300,000) + Equity (owner's contribution, ₦200,000)."},
        {"q": "Discuss the importance of the double-entry bookkeeping system.", "ms": "Ensures accuracy since every transaction has an equal debit and credit; enables the trial balance to check that the books balance; provides a complete, traceable record of every transaction; supports preparation of financial statements; and helps detect errors or fraud."},
    ],
    'BUS': [
        {"q": "Discuss the four functions of management, with examples.", "ms": "Planning: setting goals and strategy (e.g. drafting an annual budget). Organizing: arranging resources and structure (e.g. creating departments and reporting lines). Leading: motivating and directing staff toward objectives. Controlling: monitoring performance against goals and correcting deviations (e.g. performance reviews)."},
        {"q": "Explain the concept of the marketing mix (4Ps).", "ms": "Product: what is offered to meet customer needs. Price: the amount charged, reflecting value and positioning. Place: the channels through which the product reaches customers. Promotion: the communication/advertising used to inform and persuade customers. Together they form a coordinated marketing strategy."},
    ],
    'AGR': [
        {"q": "Discuss the importance of agriculture to the Nigerian economy.", "ms": "Ensures food security; is the largest employer of labor in Nigeria; supplies raw materials to agro-based industries; generates foreign exchange through export crops (e.g. cocoa, cashew); and drives rural development and household income generation."},
        {"q": "Explain the concept of crop rotation and its benefits.", "ms": "Crop rotation is the practice of growing different types of crops in sequence on the same land across seasons. Benefits: replenishes soil nutrients (e.g. legumes fix atmospheric nitrogen), breaks pest and disease life cycles, improves soil structure, and reduces weed pressure and reliance on chemical inputs."},
    ],
    'STA': [
        {"q": "Differentiate between mean, median and mode as measures of central tendency.", "ms": "Mean: the sum of all values divided by the count — sensitive to extreme values/outliers. Median: the middle value when data is arranged in order — more robust to outliers. Mode: the most frequently occurring value — most useful for categorical/discrete data."},
        {"q": "Explain the difference between descriptive and inferential statistics.", "ms": "Descriptive statistics summarize and describe the features of a dataset (e.g. mean, charts, tables). Inferential statistics use sample data to draw conclusions or make predictions about a larger population, using tools like hypothesis testing and confidence intervals."},
    ],
    'ZOO': [
        {"q": "Discuss the general characteristics of the phylum Chordata.", "ms": "Chordates share: a notochord (flexible rod providing support), a dorsal hollow nerve cord, pharyngeal slits (present at some life stage), and a post-anal tail. The phylum includes fish, amphibians, reptiles, birds and mammals."},
        {"q": "Compare and contrast vertebrates and invertebrates.", "ms": "Vertebrates possess a vertebral column/backbone and an internal skeleton, and include fish, amphibians, reptiles, birds and mammals. Invertebrates lack a backbone, may have an exoskeleton (e.g. insects) or no rigid skeleton, and make up roughly 95% of known animal species (e.g. insects, mollusks, worms)."},
    ],
    'ECO': [
        {"q": "Explain the law of demand and the factors that can cause the demand curve to shift.", "ms": "The law of demand states there is an inverse relationship between price and quantity demanded, all else equal (ceteris paribus). Shift factors (which move the whole curve, unlike a price change which moves along it): changes in consumer income, tastes/preferences, prices of substitute/complementary goods, population size, and consumer expectations."},
        {"q": "Discuss the causes and effects of inflation on an economy.", "ms": "Causes: demand-pull (aggregate demand exceeds supply), cost-push (rising input/production costs), and monetary factors (excessive growth in money supply). Effects: reduced purchasing power, planning uncertainty for businesses/households, redistribution of income (often hurting fixed-income earners), and potential benefit to debtors as real debt value falls."},
    ],
}
WRITTEN_TEMPLATES['MAT'] = WRITTEN_TEMPLATES['MTH']
WRITTEN_TEMPLATES['GES'] = WRITTEN_TEMPLATES['GST']


def seed_cbt_questions():
    with app.app_context():
        added = skipped = 0
        for subject, items in CBT_TEMPLATES.items():
            for item in items:
                exists = CBTQuestion.query.filter_by(
                    subject_code=subject, question_type='cbt', question_text=item['q']
                ).first()
                if exists:
                    skipped += 1
                    continue
                q = CBTQuestion(
                    subject_code=subject, question_type='cbt', question_text=item['q'],
                    correct_index=item['a'], explanation=item.get('e'),
                )
                q.options = item['o']
                db.session.add(q)
                added += 1

        for subject, items in WRITTEN_TEMPLATES.items():
            for item in items:
                exists = CBTQuestion.query.filter_by(
                    subject_code=subject, question_type='written', question_text=item['q']
                ).first()
                if exists:
                    skipped += 1
                    continue
                db.session.add(CBTQuestion(
                    subject_code=subject, question_type='written',
                    question_text=item['q'], mark_scheme=item.get('ms'),
                ))
                added += 1

        db.session.commit()
        print(f"CBTQuestions added: {added}   Skipped (already exist): {skipped}")


if __name__ == '__main__':
    seed_cbt_questions()
