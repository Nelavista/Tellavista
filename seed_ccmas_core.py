"""One-off seed: populates FUDMA / University of Abuja / University of Ilorin / Kwara State
University (the schools added in seed_academia.py with no course data of their own) using the
National Universities Commission's official Core Curriculum and Minimum Academic Standards
(CCMAS) -- the compulsory national floor every NUC-accredited Nigerian university programme
must teach, published at nuc.edu.ng.

IMPORTANT -- what this data is and isn't:
This is the NATIONAL CORE curriculum per discipline, not each specific university's own
published/registrar-verified course list (unlike Nelavista_Course_Codes.csv, which the user
supplied directly for LASU/UNILAG/UI). A school may use different local course-code numbering
for the same content, or add its own electives on top of this floor. Every Course row created
here is tagged source='nuc_ccmas_core' (see models.py) specifically so this is never confused
with a school's own bespoke catalog -- course_detail.html shows a note when this is the source.

Course code/title/level data below is copied verbatim from the official CCMAS PDFs (downloaded
from nuc.edu.ng in August 2026 and parsed with pdfplumber) -- units, LH/PH, and semester are not
carried over since Course doesn't model them and CCMAS itself doesn't split by semester. Where
a discipline offers multiple specialisation tracks (Science Laboratory Technology: 8 options),
only one representative track (Biology Technology) is used, since Course has no concept of a
sub-specialisation -- this is a simplification, not an omission of real data.

Sources (fetched August 2026):
- Computing:      https://www.nuc.edu.ng/wp-content/uploads/2026/03/Computing-CCMAS-2023-FINAL.pdf
- Sciences:       https://www.nuc.edu.ng/wp-content/uploads/2026/03/Sciences-CCMAS-2023-FINAL.pdf
- Administration: https://www.nuc.edu.ng/wp-content/uploads/2026/03/Administration-and-Management.pdf
- Agriculture:    https://www.nuc.edu.ng/wp-content/uploads/2026/03/Agriculture-2023.pdf

Usage:
    python seed_ccmas_core.py
"""
from app import app, db
from models import University, Faculty, Department, Course
from seed_academia import FACULTY_MAP, GENERAL_STUDIES_FACULTY, GENERAL_STUDIES_DEPT

TARGET_UNIVERSITIES = [
    'Federal University Dutsin-Ma',
    'University of Abuja',
    'University of Ilorin',
    'Kwara State University',
]

# {department_name: {level: [(code, title), ...]}} -- verbatim from the CCMAS PDFs (see module
# docstring for exact source links). GST/ENT "General Studies" courses are repeated inside each
# department's own list (as CCMAS itself repeats them per programme) rather than pulled into a
# separate shared bucket, matching how Nelavista_Course_Codes.csv models departments too.
CCMAS_CORE = {
    'Computer Science': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Practical Physics I'), ('PHY108', 'General Practical Physics II'),
            ('STA111', 'Descriptive Statistics'), ('COS101', 'Introduction to Computing Sciences'),
            ('COS102', 'Problem Solving'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('MTH201', 'Mathematical Methods I'), ('MTH202', 'Elementary Differential Equations'),
            ('COS201', 'Computer Programming I'), ('COS202', 'Computer Programming II'),
            ('CSC203', 'Discrete Structures'), ('CSC299', 'SIWES I'),
            ('IFT211', 'Digital Logic Design'), ('IFT212', 'Computer Architecture and Organisation'),
            ('SEN201', 'Introduction to Software Engineering'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('CSC301', 'Data Structures'), ('CSC308', 'Operating Systems'), ('CSC309', 'Artificial Intelligence'),
            ('CSC322', 'Computer Science Innovation and New Technologies'), ('CSC399', 'SIWES II'),
            ('CYB201', 'Introduction to Cybersecurity and Strategy'), ('DTS304', 'Data Management I'),
            ('ICT305', 'Data Communication System & Network'),
        ],
        '400': [
            ('COS409', 'Research Methodology and Technical Report Writing'),
            ('CSC401', 'Algorithms and Complexity Analysis'),
            ('CSC402', 'Ethics and Legal Issues in Computer Science'),
            ('CSC497', 'Final Year Project I'), ('CSC498', 'Final Year Project II'),
            ('INS401', 'Project Management'),
        ],
    },
    'Information Technology': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Practical Physics I'), ('PHY108', 'General Practical Physics II'),
            ('STA111', 'Descriptive Statistics'), ('COS101', 'Introduction to Computing Sciences'),
            ('COS102', 'Problem Solving'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic, and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('COS201', 'Computer Programming I'), ('COS202', 'Computer Programming II'),
            ('IFT203', 'Introduction to Web Technologies'), ('IFT205', 'Introduction to Information Technology'),
            ('IFT211', 'Digital Logic Design'), ('IFT212', 'Computer Architecture and Organisation'),
            ('IFT299', 'SIWES I'), ('INS202', 'Human-Computer Interface'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('IFT302', 'Web Application Development'),
            ('IFT304', 'Web Development using Content Management Systems'),
            ('IFT308', 'Ethics and Legal Issues in IT'), ('IFT310', 'Mobile Application Development'),
            ('IFT322', 'IT Innovation and Entrepreneurship'), ('IFT342', 'Network Servers and Infrastructures'),
            ('IFT399', 'SIWES II'), ('CSC308', 'Operating Systems'),
            ('ICT305', 'Data Communications Systems and Network'),
        ],
        '400': [
            ('COS409', 'Research Methodology and Technical Report Writing'),
            ('IFT403', 'Mobile and Pervasive Computing'), ('IFT410', 'System Integration and Architecture'),
            ('IFT442', 'Wireless Communications and Networking'),
            ('IFT497', "Final Year Student's Project I"), ('IFT498', "Final Year Student's Project II"),
            ('INS401', 'Project Management'),
        ],
    },
    'Biochemistry': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO101', 'General Biology I'), ('BIO102', 'General Biology II'),
            ('BIO107', 'General Biology Practical I'), ('BIO108', 'General Biology Practical II'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('CHM108', 'General Chemistry Practical II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Physics Practical I'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BCH201', 'General Biochemistry I'), ('BCH202', 'General Biochemistry II'),
            ('BCH203', 'General Biochemistry Practical'),
            ('STA201', 'Statistics for Agriculture & Biological Sciences'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('BCH301', 'Enzymology'), ('BCH302', 'Metabolism of Carbohydrates'),
            ('BCH303', 'Metabolism of Lipids'), ('BCH304', 'Metabolism of Amino Acids & Proteins'),
            ('BCH305', 'Structure and Functions of Nucleic Acids'),
            ('BCH306', 'Analytical Methods in Biochemistry'), ('BCH307', 'Membrane Biochemistry'),
            ('BCH308', 'Bioenergetics'), ('BCH309', 'Inorganic Biochemistry'),
            ('BCH399', 'Industrial Attachment'),
        ],
        '400': [
            ('BCH401', 'Advanced Enzymology'), ('BCH402', 'Molecular Biochemistry'),
            ('BCH403', 'Metabolic Regulations'), ('BCH404', 'Biochemical Reasoning'),
            ('BCH405', 'Plant Biochemistry'), ('BCH406', 'Research Project'),
            ('BCH407', 'Bioinformatics'), ('BCH408', 'Biochemical Entrepreneurship'),
        ],
    },
    'Botany': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO102', 'General Biology II'), ('BIO107', 'General Biology Practical I'),
            ('BIO108', 'General Biology Practical II'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('BOT102', 'Introductory Botany'),
            ('PHY101', 'General Physics I'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BIO201', 'Genetics I'), ('BIO203', 'General Physiology'),
            ('BIO204', 'Biological Techniques'), ('BIO205', 'Introductory Developmental/Cell Biology'),
            ('BOT202', 'Seedless Plants'), ('BOT203', 'Seed Plants'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('BOT301', 'Plant Taxonomy'), ('BOT302', 'Comparative Anatomy of Plant'),
            ('BOT303', 'Plant Physiology'), ('BOT304', 'Plant Ecology'), ('BOT305', 'Mycology'),
            ('BOT311', 'Medicinal Plants'), ('BOT399', 'Industrial Field Attachment'),
        ],
        '400': [
            ('BOT401', 'Seminar'), ('BOT406', 'Plant Pathology'), ('BOT409', 'Plant Virology'),
            ('BOT411', 'Bioinformatics'), ('BOT413', 'Research Project'), ('BOT416', 'Plant Cytogenesis'),
        ],
    },
    'Chemistry': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO101', 'General Biology I'), ('BIO102', 'General Biology II'),
            ('BIO107', 'General Biology Practical I'), ('BIO108', 'General Biology Practical II'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('CHM108', 'General Chemistry Practical II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Physics Practical I'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('CHM210', 'Physical Chemistry I'), ('CHM211', 'Organic Chemistry I'),
            ('CHM212', 'Inorganic Chemistry I'), ('CHM213', 'Analytical Chemistry I'),
            ('CHM214', 'Structure and Bonding'), ('CHM207', 'General Chemistry Practical III'),
            ('CHM208', 'General Chemistry Practical IV'),
            ('STA202', 'Statistics for Physical Sciences & Engineering'),
        ],
        '300': [
            ('ENT312', 'Venture Creation'), ('GST312', 'Peace and Conflict Resolution'),
            ('CHM301', 'Physical Chemistry II'), ('CHM302', 'Inorganic Chemistry II'),
            ('CHM303', 'Organic Chemistry II'), ('CHM304', 'Atomic & Molecular Structure & Symmetry'),
            ('CHM312', 'Analytical Atomic Spectroscopy'), ('CHM314', 'Entrepreneurship Skill in Chemistry'),
            ('CHM316', 'Applied Spectroscopy'), ('CHM319', 'Environmental Chemistry'),
            ('CHM399', 'Industrial Attachment II'),
        ],
        '400': [
            ('CHM400', 'Seminar'), ('CHM401', 'Research Project'), ('CHM406', 'Reaction Kinetics'),
            ('CHM410', 'Analytical Chemistry II'), ('CHM423', 'Organometallic Chemistry'),
            ('CHM424', 'Co-ordination Chemistry'),
        ],
    },
    'Mathematics': {
        '100': [
            ('GST111', 'Communication in English I'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('CSC101', 'Introduction to Computer Sciences'), ('MTH103', 'Elementary Mathematics III'),
            ('STA112', 'Probability I'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('COS201', 'Computer Programming I'), ('MTH201', 'Mathematical Methods I'),
            ('MTH202', 'Elementary Differential Equations'), ('MTH203', 'Sets Logic and Algebra I'),
            ('MTH204', 'Linear Algebra I'), ('MTH205', 'Linear Algebra II'), ('MTH207', 'Real Analysis I'),
            ('MTH209', 'Introduction to Numerical Analysis'), ('MTH210', 'Vector Analysis'),
        ],
        '300': [
            ('GST312', 'Peace and Conflicts Resolutions'), ('ENT311', 'Enterprise Appreciation'),
            ('MTH300', 'Abstract Algebra I'), ('MTH301', 'Metric Space Topology'),
            ('MTH302', 'Ordinary Differential Equations'), ('MTH303', 'Vector and Tensor Analysis'),
            ('MTH304', 'Complex Analysis I'), ('MTH305', 'Complex Analysis II'),
            ('MTH306', 'Abstract Algebra II'), ('MTH307', 'Real Analysis II'),
            ('MTH308', 'Introduction to Mathematical Modelling'), ('MTH310', 'Mathematical Methods II'),
            ('MTH399', 'Industrial Attachment II'),
        ],
        '400': [
            ('MTH401', 'Theory of Ordinary Differential Equations'),
            ('MTH402', 'Theory of Partial Differential Equations'), ('MTH403', 'Functional Analysis'),
            ('MTH404', 'Project'), ('MTH405', 'General Topology'),
            ('MTH406', 'Lebesgue Measure and Integrals'), ('MTH407', 'Mathematical Methods'),
            ('MTH408', 'Entrepreneurship in Mathematics'),
        ],
    },
    'Microbiology': {
        '100': [
            ('GST111', 'Communication In English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO101', 'General Biology I'), ('BIO107', 'General Biology Practical I'),
            ('CHM101', 'General Chemistry I'), ('CHM107', 'General Chemistry Practical I'),
            ('PHY101', 'General Physics I'), ('PHY107', 'General Physics Practical I'),
            ('BIO102', 'General Biology II'), ('BIO108', 'General Biology Practical II'),
            ('CHM102', 'General Chemistry II'), ('CHM108', 'General Chemistry Practical II'),
            ('PHY102', 'General Physics II'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('MCB221', 'General Microbiology'), ('MCB231', 'Basic Techniques in Microbiology'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolutions'), ('ENT312', 'Venture Creation'),
            ('MCB398', 'Entrepreneurship and Microbiology'),
            ('MCB305', 'Fungi of Medical, Food and Industrial Importance'), ('MCB307', 'Immunology'),
            ('MCB399', 'Industrial Attachment II'), ('MCB309', 'Food Microbiology'),
            ('MCB322', 'Bacterial Diversity'), ('MCB324', 'Microbial Ecology'),
        ],
        '400': [
            ('MCB405', 'Principles of Epidemiology and Public Health Management'),
            ('MCB407', 'Pathogenic Microbiology'), ('MCB431', 'Petroleum Microbiology'),
            ('MCB412', 'Microbial Genetics'), ('MCB423', 'Industrial Microbiology'),
            ('MCB424', 'Microbial Physiology & Metabolism'), ('MCB425', 'Environmental Microbiology'),
            ('MCB482', 'Virology & Tissue Culture'), ('MCB491', 'Research Project'),
        ],
    },
    'Physics': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian People and Culture'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY103', 'General Physics III'), ('PHY104', 'General Physics IV'),
            ('PHY107', 'General Practical Physics I'), ('PHY108', 'General Practical Physics II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('PHY201', 'General Physics V (Modern Physics)'),
            ('PHY202', 'Introduction to Electric Circuits & Electronics'),
            ('PHY204', 'General Physics VI (Waves and Optics)'), ('PHY205', 'Thermal Physics'),
            ('PHY206', 'General Physics VII (Energy & Environment)'),
            ('PHY207', 'General Practical Physics III'), ('PHY208', 'General Practical Physics IV'),
            ('PHY211', 'Workshop Practice'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolutions'), ('ENT312', 'Venture Creation'),
            ('PHY301', 'Analytical Mechanics I'), ('PHY303', 'Electromagnetism'),
            ('PHY304', 'Electromagnetic Waves and Optics'), ('PHY305', 'Quantum Physics'),
            ('PHY306', 'Statistical and Thermal Physics'), ('PHY307', 'General Physics Practical V'),
            ('PHY308', 'General Physics Practical VI'), ('PHY318', 'Semiconductor Devices'),
            ('PHY399', 'Industrial Attachment II'),
        ],
        '400': [
            ('PHY401', 'Quantum Mechanics I'), ('PHY402', 'Quantum Physics II'),
            ('PHY403', 'Mathematical Methods in Physics I'), ('PHY404', 'Mathematical Methods in Physics II'),
            ('PHY405', 'Physics Entrepreneurship'), ('PHY455', 'Research Project'),
        ],
    },
    'Zoology': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO101', 'General Biology I'), ('BIO107', 'General Biology Practical I'),
            ('CHM101', 'General Chemistry I'), ('CHM107', 'General Chemistry Practical I'),
            ('PHY101', 'General Physics I'), ('PHY107', 'General Physics Practical I'),
            ('BIO102', 'General Biology II'), ('BIO108', 'General Biology Practical II'),
            ('CHM102', 'General Chemistry II'), ('CHM108', 'General Chemistry Practical II'),
            ('PHY102', 'General Physics II'), ('PHY108', 'General Physics Practical II'),
            ('ZOO101', 'The Mammalian Body'), ('ZOO102', 'Animal Diversity'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BIO201', 'Genetics I'), ('BIO203', 'General Physiology'),
            ('STA201', 'Statistics for Agricultural & Biological Sciences'),
            ('ZOO211', 'Invertebrate Zoology I'), ('ZOO212', 'Invertebrate Zoology II'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('BIO307', 'Field Course I'), ('ZOO301', 'Vertebrate Zoology'),
            ('ZOO311', 'Comparative Animal Physiology'), ('ZOO313', 'Arthropod Diversity'),
            ('ZOO318', 'Principles of Animal Development'), ('ZOO312', 'The Biology of Tropical Parasites'),
            ('ZOO316', 'Histology'), ('ZOO399', 'Industrial Attachment II'),
        ],
        '400': [
            ('BIO407', 'Field Course II'), ('ZOO411', 'Entomology'),
            ('ZOO419', 'Essay Topic in Zoology/Seminar'), ('ZOO499', 'Project'),
            ('ZOO412', 'Parasitology'), ('ZOO422', 'Entrepreneurship and Economic Zoology'),
        ],
    },
    'Biology': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('BIO101', 'General Biology I'), ('BIO102', 'General Biology II'),
            ('BIO107', 'General Biology Practical I'), ('BIO108', 'General Biology Practical II'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BIO201', 'Genetics I'), ('BIO203', 'General Physiology'),
            ('BIO205', 'Introductory Developmental/Cell Biology'), ('BIO202', 'Introductory Ecology'),
            ('BIO204', 'Biological Techniques'), ('BIO206', 'Hydrobiology'), ('BIO208', 'Biostatistics'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('BIO300', 'Industrial Attachment (SIWES)'), ('BIO301', 'Genetics II'),
            ('BIO302', 'Population Biology and Evolution'), ('BIO303', 'Biogeography and Soil Biology'),
            ('BIO304', 'Nigerian Flora and Fauna'), ('BIO306', 'Systematic Biology'),
            ('BIO307', 'Field Course I'),
        ],
        '400': [
            ('BIO400', 'Project'), ('BIO402', 'Principles of Plant and Animal Breeding'),
            ('BIO403', 'Wildlife Conservation and Management'),
            ('BIO404', 'Nigerian Plants and Animals in Prophylactics & Therapeutics'),
            ('BIO406', 'Principles of Pest Management'), ('BIO407', 'Field Course II'),
            ('BIO408', 'Applied Biotechnology'), ('BIO410', 'Bio-Entrepreneurship Options'),
            ('BIO413', 'Bioinformatics'), ('BIO414', 'Molecular Biology'),
        ],
    },
    'Accounting': {
        '100': [
            ('GST111', 'Communication in English Language'), ('GST112', 'Nigerian Peoples and Culture'),
            ('AMS101', 'Principles of Management'), ('AMS102', 'Basic Mathematics'),
            ('AMS103', 'Introduction to Computing'), ('AMS104', 'Principles of Project Management'),
            ('ACC101', 'Introduction to Financial Accounting I'),
            ('ACC102', 'Introduction to Financial Accounting II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic, and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('ACC201', 'Financial Accounting I'), ('ACC202', 'Financial Accounting II'),
            ('ACC203', 'Corporate Governance & Accounting Ethics'), ('ACC204', 'Cost Accounting'),
            ('ACC206', 'Accounting Laboratory'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('ACC301', 'Financial Reporting I'), ('ACC302', 'Financial Reporting II'),
            ('ACC303', 'Management Accounting'), ('ACC305', 'Taxation I'), ('ACC306', 'Taxation II'),
            ('ACC307', 'Auditing and Assurance I'), ('ACC308', 'Public Sector Accounting & Reporting'),
            ('ACC311', 'Entrepreneurship in Accounting'),
        ],
        '400': [
            ('ACC401', 'Advanced Financial Reporting'), ('ACC402', 'Corporate Reporting'),
            ('ACC403', 'Auditing and Assurance II'), ('ACC404', 'Financial Management'),
            ('ACC405', 'Bankruptcy & Liquidation'), ('ACC490', 'Project'),
        ],
    },
    'Business Administration': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('AMS101', 'Principles of Management'), ('AMS102', 'Basic Mathematics'),
            ('AMS103', 'Introduction to Computers'), ('AMS104', 'Principles of Project Management'),
            ('BUA101', 'Introduction to Business I'), ('BUA102', 'Introduction to Business II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic, and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BUA201', 'Principles of Business Administration I'),
            ('BUA202', 'Principles of Business Administration II'), ('BUA203', 'Business Statistics'),
            ('BUA204', 'Quantitative Analysis in Management'), ('BUA205', 'Leadership and Governance'),
            ('BUA216', 'Introduction to Financial Management'), ('BUA218', 'Green Management'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('BUA302', 'Human Behaviour in Organisations'), ('BUA303', 'Management Theory'),
            ('BUA304', 'Human Resource Management'), ('BUA305', 'Financial Management'),
            ('BUA310', 'Production and Operation Management'), ('BUA312', 'Small Business Management'),
            ('BUA313', 'Innovation Management'), ('BUA319', 'E-Commerce'),
            ('BUA321', 'Business Start-up'), ('BUA323', 'Supply Chain Management'),
        ],
        '400': [
            ('BUA401', 'Business Policy and Strategic Management'),
            ('BUA402', 'Strategic Thinking and Problem Solving'),
            ('BUA404', 'Research Project in Business Administration'), ('BUA406', 'International Business'),
            ('BUA409', 'Management Information System'), ('BUA411', 'Analysis for Business Decision'),
            ('BUA420', 'Internship'),
        ],
    },
    'Entrepreneurship': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian People and Culture'),
            ('AMS101', 'Principles of Management'), ('AMS102', 'Basic Mathematics'),
            ('AMS103', 'Introduction to Computers'), ('AMS104', 'Principles of Project Management'),
            ('ECO101', 'Principles of Economics'), ('ENT102', 'Elements of Book Keeping'),
            ('ENT121', 'Introduction to Entrepreneurship & Venture Creation'),
            ('ENT122', 'The Nigerian Entrepreneurial Environment'),
            ('ENT124', 'Basic Financial Literacy'), ('ENT125', 'Business Statistics'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic, and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('ENT223', 'Introduction to Entrepreneurial Financing'),
            ('ENT224', 'Entrepreneurship and Change Management'), ('ENT225', 'Entrepreneurial Marketing'),
            ('ENT227', 'Theories of Entrepreneurship'), ('ENT232', 'Industrial Learning and Tours 1'),
            ('ENT234', 'Biographical Studies of Entrepreneurial Thinkers and Giants'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('ENT315', 'Business Opportunity Scouting and Evaluation'),
            ('ENT323', 'Sociology of Entrepreneurship'), ('ENT325', 'Small Scale Business Management'),
            ('ENT328', 'Family Business and Succession Plan'),
            ('ENT332', 'Feasibilities and Business Planning'), ('ENT334', 'Research Methods'),
            ('ENT336', 'Industrial Learning and Tours 2'),
        ],
        '400': [
            ('ENT416', 'Social Entrepreneurship and Community Development'),
            ('ENT417', 'Technology Entrepreneurship and Intellectual Property Rights'),
            ('ENT424', 'Management of Creativity and Innovation'), ('ENT427', 'E-Business'),
            ('ENT428', 'Entrepreneurship and Gender Issues'),
            ('ENT429', 'Strategic Thinking, Problem Solving and Negotiation Skills'),
            ('ENT432', 'Risk Management and Insurance'), ('ENT442', 'Research for Enterprise'),
        ],
    },
    'Agriculture': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('AGG102', 'Introduction to Agriculture I'), ('AGG112', 'Introduction to Agriculture II'),
            ('BIO101', 'General Biology I'), ('BIO107', 'General Biology Practical I'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('CHM108', 'General Chemistry Practical II'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Physics Practical I'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('AGR201', 'Principles of Agronomy'),
            ('AGR202', 'Introduction to Agricultural Economics, Extension and Rural Sociology'),
            ('AGR203', 'Introduction to Forest Resources and Wildlife Management'),
            ('AGR204', 'Introduction to Animal Production'),
            ('AGR205', 'Introduction to Fisheries and Aquaculture'),
            ('AGR206', 'Principles of Family and Consumer Sciences, Food Science and Technology'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('AGE305', 'Data Science and Statistical Computing'),
            ('AGE306', 'Application of Computer to Agriculture'),
            ('AGE307', 'Introduction to Farm Management and Accounting'),
            ('AGX311', 'Principles of Rural Sociology'),
            ('ANS302', 'Introduction to Animal Breeding and Genetics'),
            ('ANS304', 'Non-Ruminant Animal Production'), ('ANS305', 'Ruminant Animal Production'),
            ('CPS301', 'Arable Crops Production'), ('CPS302', 'Permanent Crops Production'),
            ('CPS304', 'Crop Genetics and Breeding'), ('SOS302', 'Introduction to Agric. Mechanization'),
            ('SOS303', 'Introductory Pedology and Soil Physics'),
        ],
        '400': [
            ('AGE404', 'Farm Records and Accounting'), ('AGX410', 'Community Agricultural Extension'),
            ('ANS404', 'Animal Products, Processing and Marketing'),
            ('ANS405', 'Animal Husbandry Techniques'), ('CPS401', 'Crop Production Techniques I'),
            ('CPS403', 'Crop Protection I'), ('CPS406', 'Farm Mechanization Practices'),
            ('SOS402', 'Soil Survey, Sampling, Classification and Taxonomy'),
            ('AGR499', 'SIWES Report'),
        ],
    },
    'Fisheries': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('AGG102', 'Introduction to Agriculture I'), ('AGG112', 'Introduction to Agriculture II'),
            ('BIO101', 'General Biology I'), ('BIO107', 'General Biology Practical I'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('CHM108', 'General Chemistry Practical II'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Physics Practical I'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('AGR201', 'Principles of Crop Production'),
            ('AGR202', 'Introduction to Agricultural Economics, Extension and Rural Sociology'),
            ('AGR204', 'Introduction to Animal Production, Fisheries and Aquaculture'),
            ('AGR206', 'Principles of Family and Consumer Sciences, Food Science and Technology'),
            ('FAA201', 'Entrepreneurship in Fisheries and Aquaculture'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolution'), ('ENT312', 'Venture Creation'),
            ('FAA301', 'Fisheries Biology'), ('FAA302', 'Fish Nutrition'),
            ('FAA303', 'Ichthyology (Systematics of Fish)'), ('FAA304', 'Fish Gear Design and Production'),
            ('FAA305', 'Limnology'), ('FAA306', 'Fisheries Ecology'), ('FAA307', 'Principles of Aquaculture'),
            ('FAA308', 'Fisheries Stock Assessment'), ('FAA399', 'SIWES'),
        ],
        '400': [
            ('FAA401', 'Fish Processing, Handling, Utilization Technology and Control'),
            ('FAA403', 'Pond Construction and Management; Fish Gear Design, Production, Use and Maintenance'),
            ('FAA404', 'Fish Fry and Fingerlings Production; Hatchery Management; Fish Production and Management and Fish Food Nutrition and Fish Food Technology'),
            ('FAA405', 'Fish Marketing, Marketing Management, Accounting Practices and Fisheries Economics'),
            ('FAA407', 'Aquatic Environment Survey; Climate Change in Fisheries and Aquaculture'),
            ('FAA410', 'Information and Communication Technologies and Value Chain in Fisheries and Aquaculture'),
            ('FAA499', 'Project and Seminar'),
        ],
    },
    # Biology Technology option only (of 8 CCMAS specialisation tracks) -- see module docstring.
    'Science Laboratory Technology': {
        '100': [
            ('GST111', 'Communication in English'), ('GST112', 'Nigerian Peoples and Culture'),
            ('MTH101', 'Elementary Mathematics I'), ('MTH102', 'Elementary Mathematics II'),
            ('COS101', 'Introduction to Computing Sciences'),
            ('GLT101', 'Hazards & Safety in the Laboratory / Laboratory Maintenance & Fittings'),
            ('GLT102', 'Workshop Technology and Practice'), ('GLT104', 'Glass-Blowing Technology'),
            ('BIO101', 'General Biology I'), ('BIO102', 'General Biology II'),
            ('BIO107', 'General Biology Practical I'), ('BIO108', 'General Biology Practical II'),
            ('CHM101', 'General Chemistry I'), ('CHM102', 'General Chemistry II'),
            ('CHM107', 'General Chemistry Practical I'), ('CHM108', 'General Chemistry Practical II'),
            ('PHY101', 'General Physics I'), ('PHY102', 'General Physics II'),
            ('PHY107', 'General Physics Practical I'), ('PHY108', 'General Physics Practical II'),
        ],
        '200': [
            ('GST212', 'Philosophy, Logic and Human Existence'), ('ENT211', 'Entrepreneurship and Innovation'),
            ('BCH201', 'General Biochemistry I'), ('BCH202', 'General Biochemistry II'),
            ('BIO201', 'Genetics I'), ('BIO203', 'General Physiology I'), ('BOT202', 'Seedless Plants'),
            ('CHM211', 'Organic Chemistry I'), ('MCB221', 'General Microbiology I'),
            ('SLT204', 'Biological Laboratory Techniques I'),
        ],
        '300': [
            ('GST312', 'Peace and Conflict Resolutions'), ('ENT312', 'Venture Creation'),
            ('SLT301', 'Entrepreneurship and Management of SLT Business Venture'),
            ('SLT304', 'Biological Laboratory Techniques II'),
            ('SLT331', 'Bioinformatics for SLT Students I'), ('BIO301', 'Genetics II'),
            ('BIO307', 'Industrial Field Course I'),
        ],
        '400': [
            ("SLT402", "Students' Industrial Work Experience"),
            ('SLT431', 'Bioinformatics for SLT Students II'),
            ('BIO404', 'Nigerian Plants and Animals in Prophylactics & Therapeutics'),
            ('BIO414', 'Molecular Biology'), ('MCB412', 'Microbial Genetics'),
        ],
    },
}


def seed_ccmas_core():
    with app.app_context():
        courses_added = skipped = 0
        for uni_name in TARGET_UNIVERSITIES:
            uni = University.query.filter_by(name=uni_name).first()
            if not uni:
                print(f"[WARN] University not found, skipping: {uni_name} -- run seed_academia.py first")
                continue

            for dept_name, levels in CCMAS_CORE.items():
                faculty_name = FACULTY_MAP.get(dept_name)
                if not faculty_name:
                    continue  # shouldn't happen -- CCMAS_CORE keys are drawn from FACULTY_MAP's own set

                fac = Faculty.query.filter_by(university_id=uni.id, name=faculty_name).first()
                if not fac:
                    fac = Faculty(university_id=uni.id, name=faculty_name)
                    db.session.add(fac)
                    db.session.flush()

                dept = Department.query.filter_by(faculty_id=fac.id, name=dept_name).first()
                if not dept:
                    dept = Department(faculty_id=fac.id, name=dept_name)
                    db.session.add(dept)
                    db.session.flush()

                for level, courses in levels.items():
                    for code, title in courses:
                        exists = Course.query.filter_by(department_id=dept.id, level=level, code=code).first()
                        if exists:
                            skipped += 1
                            continue
                        db.session.add(Course(
                            department_id=dept.id, code=code, title=title, level=level,
                            source='nuc_ccmas_core',
                        ))
                        courses_added += 1

                # Commit per department (not once at the very end) -- this script runs against a
                # remote DB over the internet, and a single multi-thousand-row transaction risks
                # the connection being dropped mid-way, rolling back everything. Committing here
                # means a dropped connection only loses the current department's progress, and
                # re-running the script (already idempotent via the .filter_by().first() checks
                # above) picks up exactly where it left off.
                db.session.commit()
                print(f"  {uni_name} / {dept_name}: done (running total -- added: {courses_added}, skipped: {skipped})")

        print(f"Courses added: {courses_added}   Skipped (already exist): {skipped}")


if __name__ == '__main__':
    seed_ccmas_core()
