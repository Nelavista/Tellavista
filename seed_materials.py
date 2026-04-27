from app import app, db
from models import Material

# ===== EXPANDED COURSE MATERIALS (Based on Your Static PDFs) =====
CORE_MATERIALS = {
    # ========== COMPUTER SCIENCE ==========
    "CSC101": {
        "name": "Introduction to Computer Science",
        "department": "Computer Science",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 101 Past Questions LASU", "url": "static/materials/Computer-Questions-and-Answers-Basic-to-Advanced.pdf", "source": "static"},
            {"title": "CSC 101 Introduction to Computing Lecture 3", "url": "static/materials/CSC-101-Introduction-to-Computing-Lecture-3.pdf", "source": "static"},
        ]
    },
    "CSC111": {
        "name": "Computer Programming I",
        "department": "Computer Science",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 111 Introduction to Computer Science", "url": "static/materials/CSC-111-Introduction-to-Computer-Science.pdf", "source": "static"},
            {"title": "CSC 111 Computer Hardware and Software", "url": "static/materials/CSC-111-Computer-Hardware-and-Software.pdf", "source": "static"},
            {"title": "CSC 111 Past Questions DML", "url": "static/materials/CSC-111-Past-Questions-DML.pdf", "source": "static"},
        ]
    },
    "CSC102": {
        "name": "Introduction to Computing",
        "department": "Computer Science",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "CSC 102 Introduction to Computing Concepts", "url": "static/materials/CSC-102-Introduction-to-Computing-Concepts.pdf", "source": "static"},
        ]
    },
    "CSC201": {
        "name": "Computer Organization",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "DBMS II Transaction Processing", "url": "static/materials/lasu/dbms2/DBMS-II-Unit-6-Transaction-Management.pdf", "source": "static"},
        ]
    },
    "CSC205": {
        "name": "Operating Systems",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "Operating System Note I", "url": "static/materials/1769477900_operating_system_note_i.pdf", "source": "static"},
            {"title": "Operating System", "url": "static/materials/1769477950_operating_system.pdf", "source": "static"},
        ]
    },
    "CSC207": {
        "name": "Programming Languages",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 207 Note 1", "url": "static/materials/1769478505_csc_207_note_1.pdf", "source": "static"},
            {"title": "CSC 207 Test 2", "url": "static/materials/1769478686_csc_207_test_2.pdf", "source": "static"},
        ]
    },
    "CSC213": {
        "name": "Data Structures & Algorithm Analysis",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 213 Note I", "url": "static/materials/1769480768_csc_213_note_i.pdf", "source": "static"},
            {"title": "Complexity Analysis of Algorithms", "url": "static/materials/complexity_analysis_of_algorithm.pdf", "source": "static"},
            {"title": "Algorithm Design Techniques", "url": "static/materials/algorithm_design_techniques_and_analysis.pdf", "source": "static"},
            {"title": "Complexity III", "url": "static/materials/complexity_iii.pdf", "source": "static"},
            {"title": "Complexity IV", "url": "static/materials/complexity_iv.pdf", "source": "static"},
        ]
    },
    "CSC217": {
        "name": "Computer Architecture",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC217 Lecture 1", "url": "static/materials/1769475988_217_lecture_1.pdf", "source": "static"},
            {"title": "CSC217 Lecture 2", "url": "static/materials/1769476027_217_lecture_2.pdf", "source": "static"},
            {"title": "CSC217 Lecture 3", "url": "static/materials/1769476056_217_lecture_3.pdf", "source": "static"},
            {"title": "CSC217 Lecture 4", "url": "static/materials/1769476087_217_lecture_4.pdf", "source": "static"},
            {"title": "CSC217 Key Points & Practice", "url": "static/materials/1769476220_csc217_key_points_practice_questions.pdf", "source": "static"},
        ]
    },
    "CSC221": {
        "name": "Data Structures",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 221 Course Content", "url": "static/materials/1769479515_csc_221_course_content.pdf", "source": "static"},
            {"title": "Data Structure I", "url": "static/materials/1769479567_data_structure_i.pdf", "source": "static"},
            {"title": "Data Structure II", "url": "static/materials/1769479600_data_structure_ii.pdf", "source": "static"},
            {"title": "Hashing", "url": "static/materials/1769479631_hashing.pdf", "source": "static"},
            {"title": "Queues", "url": "static/materials/1769479735_queues.pdf", "source": "static"},
            {"title": "Stacks", "url": "static/materials/1769479771_stacks.pdf", "source": "static"},
            {"title": "Trees I", "url": "static/materials/1769480131_trees_i.pdf", "source": "static"},
            {"title": "Trees II", "url": "static/materials/1769480504_tree_ii.pdf", "source": "static"},
            {"title": "Trees III", "url": "static/materials/1769480347_trees_iii.pdf", "source": "static"},
        ]
    },
    "CSC319": {
        "name": "Compiler Construction",
        "department": "Computer Science",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "Compiler Construction Note II", "url": "static/materials/1769476061_compiler_construction_note_ii.pdf", "source": "static"},
        ]
    },
    
    # ========== MATHEMATICS ==========
    "MAT101": {
        "name": "Elementary Mathematics I",
        "department": "Mathematics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "MAT 101 OER Likely Exam Questions", "url": "static/materials/MAT-101-OER.pdf", "source": "static"},
            {"title": "MAT 101 Questions (DML & Adebanjo)", "url": "static/materials/MAT-101-Questions-DML-and-Adebanjo-2.pdf", "source": "static"},
            {"title": "MAT 101 Lecture 1", "url": "static/materials/lasu/mathematics/1768303502_online_aspect_mat101_lesson_1.pdf", "source": "static"},
            {"title": "MAT 101 Lecture 2: Quadratic Equations", "url": "static/materials/lasu/mathematics/MAT-101-Lecture-2-Theory-of-Quadratic-Equations.pdf", "source": "static"},
            {"title": "MAT 101 Lecture 3: Indices and Logarithms", "url": "static/materials/lasu/mathematics/MAT-101-Lecture-3-Indices-and-Logarithms.pdf", "source": "static"},
            {"title": "Trigonometry", "url": "static/materials/lasu/mathematics/Trigonometry.pdf", "source": "static"},
            {"title": "Indices, Surds and Logarithms", "url": "static/materials/lasu/mathematics/Indices-Surds-and-Logarithms.pdf", "source": "static"},
            {"title": "Inequalities", "url": "static/materials/lasu/mathematics/Inequalities.pdf", "source": "static"},
            {"title": "Theory of Quadratic Equation", "url": "static/materials/lasu/mathematics/Theory-of-Quadratic-Equation.pdf", "source": "static"},
            {"title": "Sequence and Series", "url": "static/materials/lasu/mathematics/Sequence-and-Series.pdf", "source": "static"},
            {"title": "Binomial Expansion", "url": "static/materials/lasu/mathematics/Binomial-Expansion.pdf", "source": "static"},
            {"title": "MAT 101 Practice Questions", "url": "static/materials/MAT-101-Practice-Questions-NoahLyMatics.pdf", "source": "static"},
            {"title": "MAT 101 Questions", "url": "static/materials/MAT-101-Questions.pdf", "source": "static"},
            {"title": "Probability & Statistics for Engineers", "url": "static/materials/Probability-and-Statistics-for-Engineers-and-Scientists-9th-Edition.pdf", "source": "static"},
            {"title": "Introduction to Algebra", "url": "static/materials/Macmillan-Mathematical-Guides-Introduction-to-Algebra.pdf", "source": "static"},
        ]
    },
    "MAT141": {
        "name": "Mathematics for Physical Sciences",
        "department": "Mathematics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "MAT 141 Mathematics", "url": "static/materials/MAT-141.pdf", "source": "static"},
        ]
    },
    "MAT161": {
        "name": "Introductory Statistics",
        "department": "Mathematics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "MAT 161 Descriptive Statistics Lecture 1", "url": "static/materials/lasu/mat161/MAT-161-Descriptive-Statistics-Lecture-1.pdf", "source": "static"},
        ]
    },
    "MAT201": {
        "name": "Mathematical Methods I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "Lecture 1: Real-Valued Functions", "url": "static/materials/LASUmat_201_lesson_1.pdf", "source": "static"},
            {"title": "Lecture 2: Differentiation and Integration", "url": "static/materials/LASUmat_201_lecture_2.pdf", "source": "static"},
            {"title": "Lecture 3: Applications", "url": "static/materials/LASUmat_201_lecture_3.pdf", "source": "static"},
            {"title": "Lecture 4: Mean Value Theorem", "url": "static/materials/LASUmat_201_lecture_4.pdf", "source": "static"},
            {"title": "Lecture 5: Taylor Series", "url": "static/materials/LASU_mat_201_lecture_5.pdf", "source": "static"},
            {"title": "Lecture 7: Partial Derivatives", "url": "static/materials/LASU_mat_201_lecture_7.pdf", "source": "static"},
            {"title": "Lecture 8: Increments and Differentials", "url": "static/materials/LASU_mat_201_lecture_8.pdf", "source": "static"},
            {"title": "Lecture 10: Multiple Integrals", "url": "static/materials/LASU_mat_201_lecture_10.pdf", "source": "static"},
        ]
    },
    
    # ========== BIOCHEMISTRY ==========
    "BCH101": {
        "name": "General Biochemistry I",
        "department": "Biochemistry",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 101 Lipids of Biological Importance", "url": "static/materials/Lipids-of-Biological-Importance.pdf", "source": "static"},
            {"title": "BCH 101 Carbohydrates", "url": "static/materials/BCH-101-Carbohydrate.pdf", "source": "static"},
            {"title": "BCH 101 Amino Acids and Proteins", "url": "static/materials/BCH-101-Amino-Acids-and-Proteins.pdf", "source": "static"},
            {"title": "BCH 101 Macromolecules", "url": "static/materials/BCH-101-Macromolecules.pdf", "source": "static"},
            {"title": "BCH 101 OER Past Questions", "url": "static/materials/BCH-101-OER-Past-Questions.pdf", "source": "static"},
            {"title": "BCH 101 Brief History of Biochemistry", "url": "static/materials/BCH-101-Brief-History-of-Biochemistry.pdf", "source": "static"},
            {"title": "BCH 101 Multiple Choice Questions", "url": "static/materials/BCH-101-Multiple-Choice-Questions.pdf", "source": "static"},
            {"title": "History of Biochemistry", "url": "static/materials/History-of-Biochemistry.pdf", "source": "static"},
        ]
    },
    
    # ========== BIOLOGY ==========
    "BIO101": {
        "name": "General Biology I",
        "department": "Biology",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "BIO 101 Levels of Biological Organization", "url": "static/materials/BIO-101-Levels-of-Biological-Organization-and-Classification.pdf", "source": "static"},
            {"title": "BIO 101 Biomolecules: Carbohydrates and Lipids", "url": "static/materials/BIO-101-Biomolecules-Carbohydrates-and-Lipids.pdf", "source": "static"},
            {"title": "BIO 101 Biomolecules: Proteins and Nucleic Acids", "url": "static/materials/BIO-101-Biomolecules-Proteins-and-Nucleic-Acids.pdf", "source": "static"},
            {"title": "BIO 101 Gametogenesis", "url": "static/materials/BIO-101-Gametogenesis.pdf", "source": "static"},
            {"title": "BIO 101 Microscopy", "url": "static/materials/BIO-101-Microscopy.pdf", "source": "static"},
            {"title": "BIO 101 Cell Structure and Function", "url": "static/materials/BIO-101-Cell-Structure-and-Function-of-Organelles.pdf", "source": "static"},
        ]
    },
    
    # ========== CHEMISTRY ==========
    "CHM101": {
        "name": "General Chemistry I",
        "department": "Chemistry",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 101 Oxidation and Reduction", "url": "static/materials/CHM-101-Oxidation-and-Reduction.pdf", "source": "static"},
            {"title": "CHM 101 Acids and Bases", "url": "static/materials/CHM-101-Acids-and-Bases.pdf", "source": "static"},
            {"title": "CHM 101 Atomic Theory Timeline", "url": "static/materials/CHM-101-Atomic-Theory-Timeline.pdf", "source": "static"},
            {"title": "CHM 101 Redox Reactions", "url": "static/materials/CHM-101-Redox-Reactions-and-Introduction-to-Electrochemistry.pdf", "source": "static"},
            {"title": "CHM 101 Periodicity", "url": "static/materials/CHM-101-Periodicity.pdf", "source": "static"},
            {"title": "CHM 101 Modern Electronic Theory", "url": "static/materials/CHM-101-Modern-Electronic-Theory-of-Atoms.pdf", "source": "static"},
            {"title": "CHM 101 Rates of Reactions", "url": "static/materials/CHM-101-Rates-of-Reactions.pdf", "source": "static"},
            {"title": "CHM 101 Radioactivity", "url": "static/materials/CHM-101-Radioactivity.pdf", "source": "static"},
            {"title": "Sure A in CHM 101 Past Questions", "url": "static/materials/Sure-A-in-CHM-101-Past-Questions-and-Answers.pdf", "source": "static"},
        ]
    },
    "CHM102": {
        "name": "General Chemistry II",
        "department": "Chemistry",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 102 Homework Practice Questions", "url": "static/materials/CHM-102-Homework-Practice-Questions.pdf", "source": "static"},
        ]
    },
    
    # ========== PHYSICS ==========
    "PHY101": {
        "name": "General Physics I",
        "department": "Physics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "PHY 101 OER", "url": "static/materials/PHY-101-OER-Sola-Royal.pdf", "source": "static"},
            {"title": "PHY 101 General Physics I", "url": "static/materials/PHY-101-General-Physics-I-Dr-Adewusi.pdf", "source": "static"},
            {"title": "PHY 101 Circular Motion", "url": "static/materials/PHY-101-Circular-Motion.pdf", "source": "static"},
            {"title": "PHY 101 Mechanics and Properties of Matter", "url": "static/materials/PHY-101-Mechanics-and-Properties-of-Matter.pdf", "source": "static"},
            {"title": "PHY 101 Circular and Oscillatory Motion", "url": "static/materials/PHY-101-Circular-and-Oscillatory-Motion.pdf", "source": "static"},
            {"title": "General Physics Physics and Measurement", "url": "static/materials/General-Physics-Physics-and-Measurement.pdf", "source": "static"},
        ]
    },
    "PHY104": {
        "name": "Electricity and Magnetism",
        "department": "Physics",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "PHY 104 Electricity and Magnetism", "url": "static/materials/PHY-104-Electricity-and-Magnetism.pdf", "source": "static"},
            {"title": "PHY 104 Oscillation", "url": "static/materials/PHY-104-Oscillation.pdf", "source": "static"},
        ]
    },
    
    # ========== ACCOUNTING ==========
    "ACC101": {
        "name": "Introduction to Accounting",
        "department": "Accounting",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Financial Accounting", "url": "static/materials/accounting/Financial-Accounting.pdf", "source": "static"},
            {"title": "Principles of Accounting Vol 1", "url": "static/materials/account/Principles-Of-Accounting-Vol-1.pdf", "source": "static"},
            {"title": "Principles of Financial Accounting", "url": "static/materials/account/Principles-of-Financial-Accounting.pdf", "source": "static"},
        ]
    },
    "ACC102": {
        "name": "Principles of Accounting",
        "department": "Accounting",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "Principles of Accounting Vol 2", "url": "static/materials/account/Principles-Of-Accounting-Vol-2.pdf", "source": "static"},
        ]
    },
    
    # ========== ZOOLOGY ==========
    "ZOO101": {
        "name": "General Zoology",
        "department": "Zoology",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Zoology Test", "url": "static/materials/Zoology-Test.pdf", "source": "static"},
        ]
    },
    "ZOO102": {
        "name": "Animal Diversity",
        "department": "Zoology",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "ZOO 102 Digestive System of Mammals", "url": "static/materials/ZOO-102-Digestive-System-of-Mammals.pdf", "source": "static"},
        ]
    },
    
    # ========== GENERAL COURSES ==========
    "GST101": {
        "name": "Use of English I",
        "department": "General Studies",
        "level": "100",
        "semester": "First Semester",
        "materials": []  # No static materials yet
    },
    "ENT211": {
        "name": "Entrepreneurship",
        "department": "Entrepreneurship",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "ENT 211 Compilation", "url": "static/materials/1769479082_ent_211_compilation.pdf", "source": "static"},
        ]
    },
    
    # ========== INFORMATION TECHNOLOGY ==========
    "IFT219": {
        "name": "Digital Logic Design",
        "department": "Information Technology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "IFT 219 Note I", "url": "static/materials/1769478514_ift_219_note_i.pdf", "source": "static"},
            {"title": "CISC and RISC", "url": "static/materials/IFT219-CISC-and-RISC.pdf", "source": "static"},
        ]
    },
    
    # ========== AGRICULTURE ==========
    "AGR101": {
        "name": "Introduction to Agriculture",
        "department": "Agriculture",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Training Manual for Organic Agriculture", "url": "static/materials/agriculture/Compilation_techniques_organic_agriculture_rev.pdf", "source": "static"},
            {"title": "Genetics, Agriculture, and Biotechnology", "url": "static/materials/agriculture/Genetics-Agriculture-and-Biotechnology-1646343300.pdf", "source": "static"},
            {"title": "Plant Breeding Methods", "url": "static/materials/agriculture/Plant-Breeding-Methods-1724939423.pdf", "source": "static"},
        ]
    },
    
    # ========== BUSINESS ADMINISTRATION ==========
    "BUS101": {
        "name": "Introduction to Business",
        "department": "Business Administration",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Introduction to Business Administration", "url": "static/materials/businessadministation/Introduction-to-Business-Administration-1735836334.pdf", "source": "static"},
            {"title": "Business Fundamentals 1st Edition", "url": "static/materials/businessadministation/Business-Fundamentals-1st-Edition-1760797243.pdf", "source": "static"},
        ]
    },
    
    # ========== SCIENCE LABORATORY TECHNOLOGY ==========
    "GLT201": {
        "name": "Instrument Maintenance",
        "department": "Science Laboratory Technology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "GLT 201 Instrument Maintenance", "url": "static/materials/glt_practice_problems.pdf", "source": "static"},
        ]
    },
}

# ===== SEEDING FUNCTION =====
def seed_materials():
    with app.app_context():
        print("\n🌱 ========================================")
        print("   NELAVISTA MATERIALS SEEDING SYSTEM")
        print("========================================\n")
        
        total_courses = 0
        total_materials = 0
        skipped = 0
        
        for course_code, course_data in CORE_MATERIALS.items():
            # Skip courses with no materials
            if not course_data['materials']:
                continue
                
            print(f"📚 {course_code}: {course_data['name']}")
            print(f"   Department: {course_data['department']} | Level: {course_data['level']}")
            
            for mat in course_data['materials']:
                # Check if material already exists
                exists = Material.query.filter_by(
                    course_code=course_code,
                    title=mat['title']
                ).first()
                
                if exists:
                    skipped += 1
                    continue
                
                # Create new material
                new_material = Material(
                    title=mat['title'],
                    course_code=course_code,
                    department=course_data['department'],
                    level=course_data['level'],
                    semester=course_data['semester'],
                    file_url=mat.get('url'),
                    source='static',
                    is_approved=True,
                    uploaded_by='System Seed',
                    author='System'
                )
                
                db.session.add(new_material)
                total_materials += 1
            
            total_courses += 1
            print(f"   ✅ Added {len(course_data['materials'])} materials\n")
        
        db.session.commit()
        
        print("========================================")
        print("🎉 SEEDING COMPLETE!")
        print("========================================")
        print(f"✅ Courses seeded: {total_courses}")
        print(f"✅ Materials added: {total_materials}")
        print(f"⏭️  Skipped (already exist): {skipped}")
        print(f"🚀 Nelavista is ready to launch!\n")

if __name__ == "__main__":
    seed_materials()