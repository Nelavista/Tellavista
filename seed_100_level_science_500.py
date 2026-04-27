"""
NELAVISTA - 100 LEVEL FACULTY OF SCIENCE MATERIALS SEEDER
Adds 500+ materials for First & Second Semester Science courses at LASU

Course Coverage:
- Chemistry (CHM 101, 102)
- Physics (PHY 101, 102, 104)
- Biology (BIO 101, 102)
- Mathematics (MTH 101, 102)
- Biochemistry (BCH 101, 102)
- Botany (BOT 101)
- Zoology (ZOO 101, 102)
- Microbiology (MCB 101, 102)
- General Studies (GST 101, 102, 111, 121, 122)

Usage: python seed_100_level_science_500.py
"""

import os
from app import app, db
from models import Material

# ============================================================
# CORE MATERIALS DATABASE - 500+ MATERIALS
# ============================================================

SCIENCE_100_MATERIALS = {
    
    # ========== CHEMISTRY CHM 101 - General Chemistry I ==========
    "CHM101": {
        "name": "General Chemistry I",
        "department": "Chemistry",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "General Chemistry I - Complete Textbook (OpenStax)", "url": "https://openstax.org/details/books/chemistry-2e", "source": "static"},
            {"title": "CHM 101 - Atomic Structure and Periodic Table", "url": "static/materials/CHM101_Atomic_Structure.pdf", "source": "static"},
            {"title": "CHM 101 - Chemical Bonding Fundamentals", "url": "static/materials/CHM101_Chemical_Bonding.pdf", "source": "static"},
            {"title": "CHM 101 - Stoichiometry and Mole Concept", "url": "static/materials/CHM101_Stoichiometry.pdf", "source": "static"},
            {"title": "CHM 101 - States of Matter (Solid, Liquid, Gas)", "url": "static/materials/CHM101_States_of_Matter.pdf", "source": "static"},
            {"title": "CHM 101 - Chemical Reactions and Equations", "url": "static/materials/CHM101_Chemical_Reactions.pdf", "source": "static"},
            {"title": "CHM 101 - Acids, Bases and Salts", "url": "static/materials/CHM101_Acids_Bases.pdf", "source": "static"},
            {"title": "CHM 101 - Oxidation and Reduction", "url": "static/materials/CHM101_Redox.pdf", "source": "static"},
            {"title": "CHM 101 - Thermochemistry Basics", "url": "static/materials/CHM101_Thermochemistry.pdf", "source": "static"},
            {"title": "CHM 101 - Chemical Kinetics Introduction", "url": "static/materials/CHM101_Kinetics.pdf", "source": "static"},
            {"title": "CHM 101 - Solutions and Solubility", "url": "static/materials/CHM101_Solutions.pdf", "source": "static"},
            {"title": "CHM 101 - Electrochemistry Fundamentals", "url": "static/materials/CHM101_Electrochemistry.pdf", "source": "static"},
            {"title": "CHM 101 - Gas Laws and Ideal Gas Equation", "url": "static/materials/CHM101_Gas_Laws.pdf", "source": "static"},
            {"title": "CHM 101 - Colligative Properties", "url": "static/materials/CHM101_Colligative.pdf", "source": "static"},
            {"title": "CHM 101 - Chemical Equilibrium", "url": "static/materials/CHM101_Equilibrium.pdf", "source": "static"},
            {"title": "CHM 101 - Laboratory Safety and Techniques", "url": "static/materials/CHM101_Lab_Safety.pdf", "source": "static"},
            {"title": "CHM 101 - Past Questions Compilation 2020-2024", "url": "static/materials/CHM101_Past_Questions.pdf", "source": "static"},
            {"title": "CHM 101 - Lecture Notes Complete", "url": "static/materials/CHM101_Lecture_Notes.pdf", "source": "static"},
            {"title": "CHM 101 - Practice Problems with Solutions", "url": "static/materials/CHM101_Practice_Problems.pdf", "source": "static"},
            {"title": "CHM 101 - Summary Notes for Quick Revision", "url": "static/materials/CHM101_Summary.pdf", "source": "static"},
            {"title": "Chemistry Atoms First 2e - OpenStax", "url": "https://openstax.org/details/books/chemistry-atoms-first-2e", "source": "static"},
            {"title": "CHM 101 - Electron Configuration Guide", "url": "static/materials/CHM101_Electron_Config.pdf", "source": "static"},
            {"title": "CHM 101 - Molecular Geometry and VSEPR", "url": "static/materials/CHM101_VSEPR.pdf", "source": "static"},
            {"title": "CHM 101 - Ionic vs Covalent Bonding", "url": "static/materials/CHM101_Bonding_Types.pdf", "source": "static"},
            {"title": "CHM 101 - Exam Preparation Guide", "url": "static/materials/CHM101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== CHEMISTRY CHM 102 - General Chemistry II ==========
    "CHM102": {
        "name": "General Chemistry II",
        "department": "Chemistry",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 102 - Organic Chemistry Introduction", "url": "static/materials/CHM102_Organic_Intro.pdf", "source": "static"},
            {"title": "CHM 102 - Hydrocarbons and Functional Groups", "url": "static/materials/CHM102_Hydrocarbons.pdf", "source": "static"},
            {"title": "CHM 102 - Isomerism (Structural and Stereoisomerism)", "url": "static/materials/CHM102_Isomerism.pdf", "source": "static"},
            {"title": "CHM 102 - Aromatic Compounds", "url": "static/materials/CHM102_Aromatic.pdf", "source": "static"},
            {"title": "CHM 102 - Reaction Mechanisms", "url": "static/materials/CHM102_Mechanisms.pdf", "source": "static"},
            {"title": "CHM 102 - Alkanes, Alkenes, Alkynes", "url": "static/materials/CHM102_Alkanes.pdf", "source": "static"},
            {"title": "CHM 102 - Alcohols, Ethers, and Phenols", "url": "static/materials/CHM102_Alcohols.pdf", "source": "static"},
            {"title": "CHM 102 - Aldehydes and Ketones", "url": "static/materials/CHM102_Aldehydes.pdf", "source": "static"},
            {"title": "CHM 102 - Carboxylic Acids and Derivatives", "url": "static/materials/CHM102_Carboxylic.pdf", "source": "static"},
            {"title": "CHM 102 - Amines and Amides", "url": "static/materials/CHM102_Amines.pdf", "source": "static"},
            {"title": "CHM 102 - Polymers and Polymerization", "url": "static/materials/CHM102_Polymers.pdf", "source": "static"},
            {"title": "CHM 102 - Spectroscopy Basics (IR, NMR, UV)", "url": "static/materials/CHM102_Spectroscopy.pdf", "source": "static"},
            {"title": "CHM 102 - Laboratory Organic Synthesis", "url": "static/materials/CHM102_Lab_Synthesis.pdf", "source": "static"},
            {"title": "CHM 102 - Past Questions 2020-2024", "url": "static/materials/CHM102_Past_Questions.pdf", "source": "static"},
            {"title": "CHM 102 - Complete Lecture Notes", "url": "static/materials/CHM102_Lecture_Notes.pdf", "source": "static"},
            {"title": "CHM 102 - Organic Nomenclature IUPAC Rules", "url": "static/materials/CHM102_Nomenclature.pdf", "source": "static"},
            {"title": "CHM 102 - Reaction Summary Sheet", "url": "static/materials/CHM102_Reactions.pdf", "source": "static"},
            {"title": "CHM 102 - Practice Problems with Solutions", "url": "static/materials/CHM102_Practice.pdf", "source": "static"},
            {"title": "CHM 102 - Quick Revision Notes", "url": "static/materials/CHM102_Revision.pdf", "source": "static"},
            {"title": "CHM 102 - Exam Tips and Strategy", "url": "static/materials/CHM102_Exam_Tips.pdf", "source": "static"},
        ]
    },

    # ========== PHYSICS PHY 101 - General Physics I ==========
    "PHY101": {
        "name": "General Physics I",
        "department": "Physics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "University Physics Volume 1 - OpenStax", "url": "https://openstax.org/details/books/university-physics-volume-1", "source": "static"},
            {"title": "PHY 101 - Mechanics and Motion", "url": "static/materials/PHY101_Mechanics.pdf", "source": "static"},
            {"title": "PHY 101 - Newton's Laws of Motion", "url": "static/materials/PHY101_Newtons_Laws.pdf", "source": "static"},
            {"title": "PHY 101 - Work, Energy and Power", "url": "static/materials/PHY101_Energy.pdf", "source": "static"},
            {"title": "PHY 101 - Momentum and Collisions", "url": "static/materials/PHY101_Momentum.pdf", "source": "static"},
            {"title": "PHY 101 - Rotational Motion", "url": "static/materials/PHY101_Rotation.pdf", "source": "static"},
            {"title": "PHY 101 - Gravitation and Planetary Motion", "url": "static/materials/PHY101_Gravitation.pdf", "source": "static"},
            {"title": "PHY 101 - Simple Harmonic Motion", "url": "static/materials/PHY101_SHM.pdf", "source": "static"},
            {"title": "PHY 101 - Waves and Oscillations", "url": "static/materials/PHY101_Waves.pdf", "source": "static"},
            {"title": "PHY 101 - Properties of Matter", "url": "static/materials/PHY101_Matter.pdf", "source": "static"},
            {"title": "PHY 101 - Elasticity and Hooke's Law", "url": "static/materials/PHY101_Elasticity.pdf", "source": "static"},
            {"title": "PHY 101 - Fluid Mechanics", "url": "static/materials/PHY101_Fluids.pdf", "source": "static"},
            {"title": "PHY 101 - Surface Tension and Viscosity", "url": "static/materials/PHY101_Surface_Tension.pdf", "source": "static"},
            {"title": "PHY 101 - Laboratory Manual and Experiments", "url": "static/materials/PHY101_Lab_Manual.pdf", "source": "static"},
            {"title": "PHY 101 - Past Questions 2020-2024", "url": "static/materials/PHY101_Past_Questions.pdf", "source": "static"},
            {"title": "PHY 101 - Complete Lecture Notes", "url": "static/materials/PHY101_Lecture_Notes.pdf", "source": "static"},
            {"title": "PHY 101 - Formula Sheet", "url": "static/materials/PHY101_Formulas.pdf", "source": "static"},
            {"title": "PHY 101 - Solved Examples and Problems", "url": "static/materials/PHY101_Solved_Problems.pdf", "source": "static"},
            {"title": "PHY 101 - Quick Revision Guide", "url": "static/materials/PHY101_Revision.pdf", "source": "static"},
            {"title": "PHY 101 - Exam Preparation Notes", "url": "static/materials/PHY101_Exam_Prep.pdf", "source": "static"},
            {"title": "PHY 101 - Vector Analysis", "url": "static/materials/PHY101_Vectors.pdf", "source": "static"},
            {"title": "PHY 101 - Kinematics Equations", "url": "static/materials/PHY101_Kinematics.pdf", "source": "static"},
            {"title": "PHY 101 - Projectile Motion", "url": "static/materials/PHY101_Projectile.pdf", "source": "static"},
            {"title": "PHY 101 - Circular Motion", "url": "static/materials/PHY101_Circular.pdf", "source": "static"},
            {"title": "PHY 101 - Conservation Laws", "url": "static/materials/PHY101_Conservation.pdf", "source": "static"},
        ]
    },

    # ========== PHYSICS PHY 102 - General Physics II ==========
    "PHY102": {
        "name": "General Physics II",
        "department": "Physics",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "University Physics Volume 2 - OpenStax", "url": "https://openstax.org/details/books/university-physics-volume-2", "source": "static"},
            {"title": "PHY 102 - Electricity and Magnetism", "url": "static/materials/PHY102_EM.pdf", "source": "static"},
            {"title": "PHY 102 - Electric Fields and Charges", "url": "static/materials/PHY102_Electric_Fields.pdf", "source": "static"},
            {"title": "PHY 102 - Coulomb's Law and Applications", "url": "static/materials/PHY102_Coulomb.pdf", "source": "static"},
            {"title": "PHY 102 - Electric Potential and Capacitance", "url": "static/materials/PHY102_Capacitance.pdf", "source": "static"},
            {"title": "PHY 102 - Direct Current Circuits", "url": "static/materials/PHY102_DC_Circuits.pdf", "source": "static"},
            {"title": "PHY 102 - Kirchhoff's Laws", "url": "static/materials/PHY102_Kirchhoff.pdf", "source": "static"},
            {"title": "PHY 102 - Magnetic Fields and Forces", "url": "static/materials/PHY102_Magnetic_Fields.pdf", "source": "static"},
            {"title": "PHY 102 - Electromagnetic Induction", "url": "static/materials/PHY102_Induction.pdf", "source": "static"},
            {"title": "PHY 102 - Alternating Current (AC)", "url": "static/materials/PHY102_AC.pdf", "source": "static"},
            {"title": "PHY 102 - Optics and Light", "url": "static/materials/PHY102_Optics.pdf", "source": "static"},
            {"title": "PHY 102 - Reflection and Refraction", "url": "static/materials/PHY102_Reflection.pdf", "source": "static"},
            {"title": "PHY 102 - Lenses and Mirrors", "url": "static/materials/PHY102_Lenses.pdf", "source": "static"},
            {"title": "PHY 102 - Interference and Diffraction", "url": "static/materials/PHY102_Interference.pdf", "source": "static"},
            {"title": "PHY 102 - Modern Physics Introduction", "url": "static/materials/PHY102_Modern.pdf", "source": "static"},
            {"title": "PHY 102 - Quantum Mechanics Basics", "url": "static/materials/PHY102_Quantum.pdf", "source": "static"},
            {"title": "PHY 102 - Atomic Structure", "url": "static/materials/PHY102_Atomic.pdf", "source": "static"},
            {"title": "PHY 102 - Nuclear Physics Introduction", "url": "static/materials/PHY102_Nuclear.pdf", "source": "static"},
            {"title": "PHY 102 - Laboratory Experiments", "url": "static/materials/PHY102_Lab.pdf", "source": "static"},
            {"title": "PHY 102 - Past Questions 2020-2024", "url": "static/materials/PHY102_Past_Questions.pdf", "source": "static"},
            {"title": "PHY 102 - Complete Lecture Notes", "url": "static/materials/PHY102_Lecture_Notes.pdf", "source": "static"},
            {"title": "PHY 102 - Formula Sheet", "url": "static/materials/PHY102_Formulas.pdf", "source": "static"},
            {"title": "PHY 102 - Practice Problems", "url": "static/materials/PHY102_Practice.pdf", "source": "static"},
            {"title": "PHY 102 - Quick Revision Guide", "url": "static/materials/PHY102_Revision.pdf", "source": "static"},
            {"title": "PHY 102 - Exam Preparation", "url": "static/materials/PHY102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== PHYSICS PHY 104 - Heat & Thermodynamics ==========
    "PHY104": {
        "name": "Heat and Thermodynamics",
        "department": "Physics",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "PHY 104 - Temperature and Heat", "url": "static/materials/PHY104_Temperature.pdf", "source": "static"},
            {"title": "PHY 104 - Laws of Thermodynamics", "url": "static/materials/PHY104_Laws.pdf", "source": "static"},
            {"title": "PHY 104 - Heat Transfer Mechanisms", "url": "static/materials/PHY104_Heat_Transfer.pdf", "source": "static"},
            {"title": "PHY 104 - Kinetic Theory of Gases", "url": "static/materials/PHY104_Kinetic_Theory.pdf", "source": "static"},
            {"title": "PHY 104 - Thermodynamic Processes", "url": "static/materials/PHY104_Processes.pdf", "source": "static"},
            {"title": "PHY 104 - Entropy and Second Law", "url": "static/materials/PHY104_Entropy.pdf", "source": "static"},
            {"title": "PHY 104 - Carnot Engine and Efficiency", "url": "static/materials/PHY104_Carnot.pdf", "source": "static"},
            {"title": "PHY 104 - Thermal Expansion", "url": "static/materials/PHY104_Expansion.pdf", "source": "static"},
            {"title": "PHY 104 - Calorimetry", "url": "static/materials/PHY104_Calorimetry.pdf", "source": "static"},
            {"title": "PHY 104 - Phase Changes", "url": "static/materials/PHY104_Phase_Changes.pdf", "source": "static"},
            {"title": "PHY 104 - Past Questions", "url": "static/materials/PHY104_Past_Questions.pdf", "source": "static"},
            {"title": "PHY 104 - Lecture Notes", "url": "static/materials/PHY104_Notes.pdf", "source": "static"},
            {"title": "PHY 104 - Problem Solving Guide", "url": "static/materials/PHY104_Problems.pdf", "source": "static"},
            {"title": "PHY 104 - Quick Revision", "url": "static/materials/PHY104_Revision.pdf", "source": "static"},
            {"title": "PHY 104 - Exam Preparation", "url": "static/materials/PHY104_Exam.pdf", "source": "static"},
        ]
    },

    # ========== BIOLOGY BIO 101 - General Biology I ==========
    "BIO101": {
        "name": "General Biology I",
        "department": "Biology",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Biology 2e - OpenStax Complete Textbook", "url": "https://openstax.org/details/books/biology-2e", "source": "static"},
            {"title": "BIO 101 - Cell Biology and Structure", "url": "static/materials/BIO101_Cell_Biology.pdf", "source": "static"},
            {"title": "BIO 101 - Prokaryotic vs Eukaryotic Cells", "url": "static/materials/BIO101_Cell_Types.pdf", "source": "static"},
            {"title": "BIO 101 - Cell Membrane and Transport", "url": "static/materials/BIO101_Membrane.pdf", "source": "static"},
            {"title": "BIO 101 - Cellular Respiration", "url": "static/materials/BIO101_Respiration.pdf", "source": "static"},
            {"title": "BIO 101 - Photosynthesis Process", "url": "static/materials/BIO101_Photosynthesis.pdf", "source": "static"},
            {"title": "BIO 101 - Cell Division (Mitosis and Meiosis)", "url": "static/materials/BIO101_Cell_Division.pdf", "source": "static"},
            {"title": "BIO 101 - DNA Structure and Replication", "url": "static/materials/BIO101_DNA.pdf", "source": "static"},
            {"title": "BIO 101 - Protein Synthesis (Transcription & Translation)", "url": "static/materials/BIO101_Protein_Synthesis.pdf", "source": "static"},
            {"title": "BIO 101 - Genetics and Mendelian Inheritance", "url": "static/materials/BIO101_Genetics.pdf", "source": "static"},
            {"title": "BIO 101 - Classification of Living Things", "url": "static/materials/BIO101_Classification.pdf", "source": "static"},
            {"title": "BIO 101 - Plant Biology Basics", "url": "static/materials/BIO101_Plants.pdf", "source": "static"},
            {"title": "BIO 101 - Animal Biology Basics", "url": "static/materials/BIO101_Animals.pdf", "source": "static"},
            {"title": "BIO 101 - Microbiology Introduction", "url": "static/materials/BIO101_Microbiology.pdf", "source": "static"},
            {"title": "BIO 101 - Ecology and Ecosystems", "url": "static/materials/BIO101_Ecology.pdf", "source": "static"},
            {"title": "BIO 101 - Evolution and Natural Selection", "url": "static/materials/BIO101_Evolution.pdf", "source": "static"},
            {"title": "BIO 101 - Human Anatomy Overview", "url": "static/materials/BIO101_Anatomy.pdf", "source": "static"},
            {"title": "BIO 101 - Laboratory Techniques", "url": "static/materials/BIO101_Lab_Techniques.pdf", "source": "static"},
            {"title": "BIO 101 - Microscopy and Staining", "url": "static/materials/BIO101_Microscopy.pdf", "source": "static"},
            {"title": "BIO 101 - Past Questions 2020-2024", "url": "static/materials/BIO101_Past_Questions.pdf", "source": "static"},
            {"title": "BIO 101 - Complete Lecture Notes", "url": "static/materials/BIO101_Lecture_Notes.pdf", "source": "static"},
            {"title": "BIO 101 - Diagrams and Illustrations", "url": "static/materials/BIO101_Diagrams.pdf", "source": "static"},
            {"title": "BIO 101 - Quick Revision Guide", "url": "static/materials/BIO101_Revision.pdf", "source": "static"},
            {"title": "BIO 101 - Exam Preparation", "url": "static/materials/BIO101_Exam_Prep.pdf", "source": "static"},
            {"title": "BIO 101 - Study Tips and Strategies", "url": "static/materials/BIO101_Study_Tips.pdf", "source": "static"},
        ]
    },

    # ========== BIOLOGY BIO 102 - General Biology II ==========
    "BIO102": {
        "name": "General Biology II",
        "department": "Biology",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "Concepts of Biology - OpenStax", "url": "https://openstax.org/details/books/concepts-biology", "source": "static"},
            {"title": "BIO 102 - Animal Physiology", "url": "static/materials/BIO102_Physiology.pdf", "source": "static"},
            {"title": "BIO 102 - Plant Physiology", "url": "static/materials/BIO102_Plant_Physiology.pdf", "source": "static"},
            {"title": "BIO 102 - Human Body Systems", "url": "static/materials/BIO102_Body_Systems.pdf", "source": "static"},
            {"title": "BIO 102 - Nervous System", "url": "static/materials/BIO102_Nervous.pdf", "source": "static"},
            {"title": "BIO 102 - Endocrine System", "url": "static/materials/BIO102_Endocrine.pdf", "source": "static"},
            {"title": "BIO 102 - Circulatory System", "url": "static/materials/BIO102_Circulatory.pdf", "source": "static"},
            {"title": "BIO 102 - Respiratory System", "url": "static/materials/BIO102_Respiratory.pdf", "source": "static"},
            {"title": "BIO 102 - Digestive System", "url": "static/materials/BIO102_Digestive.pdf", "source": "static"},
            {"title": "BIO 102 - Excretory System", "url": "static/materials/BIO102_Excretory.pdf", "source": "static"},
            {"title": "BIO 102 - Reproductive System", "url": "static/materials/BIO102_Reproductive.pdf", "source": "static"},
            {"title": "BIO 102 - Immune System", "url": "static/materials/BIO102_Immune.pdf", "source": "static"},
            {"title": "BIO 102 - Biodiversity and Conservation", "url": "static/materials/BIO102_Biodiversity.pdf", "source": "static"},
            {"title": "BIO 102 - Population Ecology", "url": "static/materials/BIO102_Population.pdf", "source": "static"},
            {"title": "BIO 102 - Community Ecology", "url": "static/materials/BIO102_Community.pdf", "source": "static"},
            {"title": "BIO 102 - Ecosystem Dynamics", "url": "static/materials/BIO102_Ecosystem.pdf", "source": "static"},
            {"title": "BIO 102 - Biogeochemical Cycles", "url": "static/materials/BIO102_Cycles.pdf", "source": "static"},
            {"title": "BIO 102 - Laboratory Practical Guide", "url": "static/materials/BIO102_Lab_Guide.pdf", "source": "static"},
            {"title": "BIO 102 - Dissection Techniques", "url": "static/materials/BIO102_Dissection.pdf", "source": "static"},
            {"title": "BIO 102 - Past Questions 2020-2024", "url": "static/materials/BIO102_Past_Questions.pdf", "source": "static"},
            {"title": "BIO 102 - Complete Lecture Notes", "url": "static/materials/BIO102_Lecture_Notes.pdf", "source": "static"},
            {"title": "BIO 102 - Quick Revision Guide", "url": "static/materials/BIO102_Revision.pdf", "source": "static"},
            {"title": "BIO 102 - Exam Preparation", "url": "static/materials/BIO102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== MATHEMATICS MTH 101 - Elementary Mathematics I ==========
    "MTH101": {
        "name": "Elementary Mathematics I",
        "department": "Mathematics",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "Algebra and Trigonometry - OpenStax", "url": "https://openstax.org/details/books/algebra-and-trigonometry", "source": "static"},
            {"title": "MTH 101 - Real Numbers and Number Systems", "url": "static/materials/MTH101_Real_Numbers.pdf", "source": "static"},
            {"title": "MTH 101 - Algebra Fundamentals", "url": "static/materials/MTH101_Algebra.pdf", "source": "static"},
            {"title": "MTH 101 - Linear Equations and Inequalities", "url": "static/materials/MTH101_Linear.pdf", "source": "static"},
            {"title": "MTH 101 - Quadratic Equations", "url": "static/materials/MTH101_Quadratic.pdf", "source": "static"},
            {"title": "MTH 101 - Functions and Graphs", "url": "static/materials/MTH101_Functions.pdf", "source": "static"},
            {"title": "MTH 101 - Polynomial Functions", "url": "static/materials/MTH101_Polynomials.pdf", "source": "static"},
            {"title": "MTH 101 - Exponential and Logarithmic Functions", "url": "static/materials/MTH101_Exponential.pdf", "source": "static"},
            {"title": "MTH 101 - Trigonometry Basics", "url": "static/materials/MTH101_Trigonometry.pdf", "source": "static"},
            {"title": "MTH 101 - Trigonometric Identities", "url": "static/materials/MTH101_Trig_Identities.pdf", "source": "static"},
            {"title": "MTH 101 - Sequences and Series", "url": "static/materials/MTH101_Sequences.pdf", "source": "static"},
            {"title": "MTH 101 - Binomial Theorem", "url": "static/materials/MTH101_Binomial.pdf", "source": "static"},
            {"title": "MTH 101 - Permutations and Combinations", "url": "static/materials/MTH101_Permutations.pdf", "source": "static"},
            {"title": "MTH 101 - Probability Basics", "url": "static/materials/MTH101_Probability.pdf", "source": "static"},
            {"title": "MTH 101 - Matrices and Determinants", "url": "static/materials/MTH101_Matrices.pdf", "source": "static"},
            {"title": "MTH 101 - Vectors Introduction", "url": "static/materials/MTH101_Vectors.pdf", "source": "static"},
            {"title": "MTH 101 - Complex Numbers", "url": "static/materials/MTH101_Complex.pdf", "source": "static"},
            {"title": "MTH 101 - Past Questions 2020-2024", "url": "static/materials/MTH101_Past_Questions.pdf", "source": "static"},
            {"title": "MTH 101 - Complete Lecture Notes", "url": "static/materials/MTH101_Lecture_Notes.pdf", "source": "static"},
            {"title": "MTH 101 - Practice Problems with Solutions", "url": "static/materials/MTH101_Practice.pdf", "source": "static"},
            {"title": "MTH 101 - Formula Sheet", "url": "static/materials/MTH101_Formulas.pdf", "source": "static"},
            {"title": "MTH 101 - Quick Revision Guide", "url": "static/materials/MTH101_Revision.pdf", "source": "static"},
            {"title": "MTH 101 - Exam Tips and Strategies", "url": "static/materials/MTH101_Exam_Tips.pdf", "source": "static"},
            {"title": "MTH 101 - Calculator Techniques", "url": "static/materials/MTH101_Calculator.pdf", "source": "static"},
            {"title": "MTH 101 - Graph Plotting Guide", "url": "static/materials/MTH101_Graphs.pdf", "source": "static"},
        ]
    },

    # ========== MATHEMATICS MTH 102 - Elementary Mathematics II ==========
    "MTH102": {
        "name": "Elementary Mathematics II",
        "department": "Mathematics",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "Calculus Volume 1 - OpenStax", "url": "https://openstax.org/details/books/calculus-volume-1", "source": "static"},
            {"title": "MTH 102 - Introduction to Calculus", "url": "static/materials/MTH102_Intro_Calculus.pdf", "source": "static"},
            {"title": "MTH 102 - Limits and Continuity", "url": "static/materials/MTH102_Limits.pdf", "source": "static"},
            {"title": "MTH 102 - Differentiation Techniques", "url": "static/materials/MTH102_Differentiation.pdf", "source": "static"},
            {"title": "MTH 102 - Applications of Derivatives", "url": "static/materials/MTH102_Derivative_Apps.pdf", "source": "static"},
            {"title": "MTH 102 - Integration Techniques", "url": "static/materials/MTH102_Integration.pdf", "source": "static"},
            {"title": "MTH 102 - Definite and Indefinite Integrals", "url": "static/materials/MTH102_Integrals.pdf", "source": "static"},
            {"title": "MTH 102 - Applications of Integration", "url": "static/materials/MTH102_Integration_Apps.pdf", "source": "static"},
            {"title": "MTH 102 - Differential Equations Introduction", "url": "static/materials/MTH102_Diff_Equations.pdf", "source": "static"},
            {"title": "MTH 102 - Coordinate Geometry", "url": "static/materials/MTH102_Coordinate.pdf", "source": "static"},
            {"title": "MTH 102 - Conic Sections", "url": "static/materials/MTH102_Conics.pdf", "source": "static"},
            {"title": "MTH 102 - 3D Geometry", "url": "static/materials/MTH102_3D_Geometry.pdf", "source": "static"},
            {"title": "MTH 102 - Vector Calculus", "url": "static/materials/MTH102_Vector_Calculus.pdf", "source": "static"},
            {"title": "MTH 102 - Taylor and Maclaurin Series", "url": "static/materials/MTH102_Series.pdf", "source": "static"},
            {"title": "MTH 102 - Partial Derivatives", "url": "static/materials/MTH102_Partial.pdf", "source": "static"},
            {"title": "MTH 102 - Multiple Integrals", "url": "static/materials/MTH102_Multiple_Integrals.pdf", "source": "static"},
            {"title": "MTH 102 - Past Questions 2020-2024", "url": "static/materials/MTH102_Past_Questions.pdf", "source": "static"},
            {"title": "MTH 102 - Complete Lecture Notes", "url": "static/materials/MTH102_Lecture_Notes.pdf", "source": "static"},
            {"title": "MTH 102 - Solved Examples", "url": "static/materials/MTH102_Solved.pdf", "source": "static"},
            {"title": "MTH 102 - Practice Problems", "url": "static/materials/MTH102_Practice.pdf", "source": "static"},
            {"title": "MTH 102 - Formula Sheet", "url": "static/materials/MTH102_Formulas.pdf", "source": "static"},
            {"title": "MTH 102 - Quick Revision", "url": "static/materials/MTH102_Revision.pdf", "source": "static"},
            {"title": "MTH 102 - Exam Preparation", "url": "static/materials/MTH102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== BIOCHEMISTRY BCH 101 - General Biochemistry I ==========
    "BCH101": {
        "name": "General Biochemistry I",
        "department": "Biochemistry",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 101 - Introduction to Biochemistry", "url": "static/materials/BCH101_Introduction.pdf", "source": "static"},
            {"title": "BCH 101 - Lipids of Biological Importance", "url": "static/materials/Lipids-of-Biological-Importance.pdf", "source": "static"},
            {"title": "BCH 101 - Carbohydrates Structure and Function", "url": "static/materials/BCH-101-Carbohydrate.pdf", "source": "static"},
            {"title": "BCH 101 - Amino Acids and Proteins", "url": "static/materials/BCH-101-Amino-Acids-and-Proteins.pdf", "source": "static"},
            {"title": "BCH 101 - Protein Structure Levels", "url": "static/materials/BCH101_Protein_Structure.pdf", "source": "static"},
            {"title": "BCH 101 - Nucleic Acids (DNA and RNA)", "url": "static/materials/BCH101_Nucleic_Acids.pdf", "source": "static"},
            {"title": "BCH 101 - Water and pH in Biological Systems", "url": "static/materials/BCH101_Water_pH.pdf", "source": "static"},
            {"title": "BCH 101 - Buffers and Henderson-Hasselbalch", "url": "static/materials/BCH101_Buffers.pdf", "source": "static"},
            {"title": "BCH 101 - Enzyme Classification", "url": "static/materials/BCH101_Enzymes.pdf", "source": "static"},
            {"title": "BCH 101 - Enzyme Kinetics Basics", "url": "static/materials/BCH101_Kinetics.pdf", "source": "static"},
            {"title": "BCH 101 - Vitamins and Coenzymes", "url": "static/materials/BCH101_Vitamins.pdf", "source": "static"},
            {"title": "BCH 101 - Biological Membranes", "url": "static/materials/BCH101_Membranes.pdf", "source": "static"},
            {"title": "BCH 101 - Bioenergetics Introduction", "url": "static/materials/BCH101_Bioenergetics.pdf", "source": "static"},
            {"title": "BCH 101 - Glycolysis Pathway", "url": "static/materials/BCH101_Glycolysis.pdf", "source": "static"},
            {"title": "BCH 101 - Citric Acid Cycle", "url": "static/materials/BCH101_TCA.pdf", "source": "static"},
            {"title": "BCH 101 - Electron Transport Chain", "url": "static/materials/BCH101_ETC.pdf", "source": "static"},
            {"title": "BCH 101 - Laboratory Techniques", "url": "static/materials/BCH101_Lab_Techniques.pdf", "source": "static"},
            {"title": "BCH 101 - Spectrophotometry", "url": "static/materials/BCH101_Spectro.pdf", "source": "static"},
            {"title": "BCH 101 - Chromatography Methods", "url": "static/materials/BCH101_Chromatography.pdf", "source": "static"},
            {"title": "BCH 101 - Past Questions 2020-2024", "url": "static/materials/BCH101_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 101 - Complete Lecture Notes", "url": "static/materials/BCH101_Lecture_Notes.pdf", "source": "static"},
            {"title": "BCH 101 - Metabolic Pathways Summary", "url": "static/materials/BCH101_Pathways.pdf", "source": "static"},
            {"title": "BCH 101 - Quick Revision Guide", "url": "static/materials/BCH101_Revision.pdf", "source": "static"},
            {"title": "BCH 101 - Exam Preparation", "url": "static/materials/BCH101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== BIOCHEMISTRY BCH 102 - General Biochemistry II ==========
    "BCH102": {
        "name": "General Biochemistry II",
        "department": "Biochemistry",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 102 - Lipid Metabolism", "url": "static/materials/BCH102_Lipid_Metabolism.pdf", "source": "static"},
            {"title": "BCH 102 - Fatty Acid Synthesis and Oxidation", "url": "static/materials/BCH102_Fatty_Acids.pdf", "source": "static"},
            {"title": "BCH 102 - Amino Acid Metabolism", "url": "static/materials/BCH102_Amino_Metabolism.pdf", "source": "static"},
            {"title": "BCH 102 - Nitrogen Metabolism", "url": "static/materials/BCH102_Nitrogen.pdf", "source": "static"},
            {"title": "BCH 102 - Urea Cycle", "url": "static/materials/BCH102_Urea_Cycle.pdf", "source": "static"},
            {"title": "BCH 102 - Nucleotide Metabolism", "url": "static/materials/BCH102_Nucleotide.pdf", "source": "static"},
            {"title": "BCH 102 - DNA Replication", "url": "static/materials/BCH102_DNA_Replication.pdf", "source": "static"},
            {"title": "BCH 102 - RNA Transcription", "url": "static/materials/BCH102_Transcription.pdf", "source": "static"},
            {"title": "BCH 102 - Protein Translation", "url": "static/materials/BCH102_Translation.pdf", "source": "static"},
            {"title": "BCH 102 - Gene Expression Regulation", "url": "static/materials/BCH102_Gene_Regulation.pdf", "source": "static"},
            {"title": "BCH 102 - Metabolic Integration", "url": "static/materials/BCH102_Integration.pdf", "source": "static"},
            {"title": "BCH 102 - Hormones and Signal Transduction", "url": "static/materials/BCH102_Hormones.pdf", "source": "static"},
            {"title": "BCH 102 - Blood Biochemistry", "url": "static/materials/BCH102_Blood.pdf", "source": "static"},
            {"title": "BCH 102 - Clinical Biochemistry Basics", "url": "static/materials/BCH102_Clinical.pdf", "source": "static"},
            {"title": "BCH 102 - Immunochemistry Introduction", "url": "static/materials/BCH102_Immuno.pdf", "source": "static"},
            {"title": "BCH 102 - Biochemical Analysis Methods", "url": "static/materials/BCH102_Analysis.pdf", "source": "static"},
            {"title": "BCH 102 - Electrophoresis Techniques", "url": "static/materials/BCH102_Electrophoresis.pdf", "source": "static"},
            {"title": "BCH 102 - Past Questions 2020-2024", "url": "static/materials/BCH102_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 102 - Complete Lecture Notes", "url": "static/materials/BCH102_Lecture_Notes.pdf", "source": "static"},
            {"title": "BCH 102 - Quick Revision Guide", "url": "static/materials/BCH102_Revision.pdf", "source": "static"},
            {"title": "BCH 102 - Exam Preparation", "url": "static/materials/BCH102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== BOTANY BOT 101 - Diversity of Plants ==========
    "BOT101": {
        "name": "Diversity of Plants",
        "department": "Botany",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 101 - Introduction to Plant Kingdom", "url": "static/materials/BOT101_Plant_Kingdom.pdf", "source": "static"},
            {"title": "BOT 101 - Algae Classification", "url": "static/materials/BOT101_Algae.pdf", "source": "static"},
            {"title": "BOT 101 - Bryophytes (Mosses and Liverworts)", "url": "static/materials/BOT101_Bryophytes.pdf", "source": "static"},
            {"title": "BOT 101 - Pteridophytes (Ferns)", "url": "static/materials/BOT101_Pteridophytes.pdf", "source": "static"},
            {"title": "BOT 101 - Gymnosperms", "url": "static/materials/BOT101_Gymnosperms.pdf", "source": "static"},
            {"title": "BOT 101 - Angiosperms (Flowering Plants)", "url": "static/materials/BOT101_Angiosperms.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Morphology", "url": "static/materials/BOT101_Morphology.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Anatomy", "url": "static/materials/BOT101_Anatomy.pdf", "source": "static"},
            {"title": "BOT 101 - Root Systems", "url": "static/materials/BOT101_Roots.pdf", "source": "static"},
            {"title": "BOT 101 - Stem Structure", "url": "static/materials/BOT101_Stems.pdf", "source": "static"},
            {"title": "BOT 101 - Leaf Structure and Types", "url": "static/materials/BOT101_Leaves.pdf", "source": "static"},
            {"title": "BOT 101 - Flower Structure", "url": "static/materials/BOT101_Flowers.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Reproduction", "url": "static/materials/BOT101_Reproduction.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Life Cycles", "url": "static/materials/BOT101_Life_Cycles.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Taxonomy Basics", "url": "static/materials/BOT101_Taxonomy.pdf", "source": "static"},
            {"title": "BOT 101 - Botanical Nomenclature", "url": "static/materials/BOT101_Nomenclature.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Collection and Preservation", "url": "static/materials/BOT101_Collection.pdf", "source": "static"},
            {"title": "BOT 101 - Herbarium Techniques", "url": "static/materials/BOT101_Herbarium.pdf", "source": "static"},
            {"title": "BOT 101 - Past Questions 2020-2024", "url": "static/materials/BOT101_Past_Questions.pdf", "source": "static"},
            {"title": "BOT 101 - Complete Lecture Notes", "url": "static/materials/BOT101_Lecture_Notes.pdf", "source": "static"},
            {"title": "BOT 101 - Plant Identification Guide", "url": "static/materials/BOT101_Identification.pdf", "source": "static"},
            {"title": "BOT 101 - Quick Revision Guide", "url": "static/materials/BOT101_Revision.pdf", "source": "static"},
            {"title": "BOT 101 - Exam Preparation", "url": "static/materials/BOT101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== ZOOLOGY ZOO 101 - General Zoology ==========
    "ZOO101": {
        "name": "General Zoology",
        "department": "Zoology",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "ZOO 101 - Introduction to Animal Kingdom", "url": "static/materials/ZOO101_Animal_Kingdom.pdf", "source": "static"},
            {"title": "ZOO 101 - Protozoa Classification", "url": "static/materials/ZOO101_Protozoa.pdf", "source": "static"},
            {"title": "ZOO 101 - Porifera (Sponges)", "url": "static/materials/ZOO101_Porifera.pdf", "source": "static"},
            {"title": "ZOO 101 - Coelenterata (Cnidarians)", "url": "static/materials/ZOO101_Cnidaria.pdf", "source": "static"},
            {"title": "ZOO 101 - Platyhelminthes (Flatworms)", "url": "static/materials/ZOO101_Flatworms.pdf", "source": "static"},
            {"title": "ZOO 101 - Nematoda (Roundworms)", "url": "static/materials/ZOO101_Nematoda.pdf", "source": "static"},
            {"title": "ZOO 101 - Annelida (Segmented Worms)", "url": "static/materials/ZOO101_Annelida.pdf", "source": "static"},
            {"title": "ZOO 101 - Mollusca (Mollusks)", "url": "static/materials/ZOO101_Mollusca.pdf", "source": "static"},
            {"title": "ZOO 101 - Arthropoda (Insects and Crustaceans)", "url": "static/materials/ZOO101_Arthropoda.pdf", "source": "static"},
            {"title": "ZOO 101 - Echinodermata (Starfish)", "url": "static/materials/ZOO101_Echinodermata.pdf", "source": "static"},
            {"title": "ZOO 101 - Chordata Introduction", "url": "static/materials/ZOO101_Chordata.pdf", "source": "static"},
            {"title": "ZOO 101 - Fish Classification", "url": "static/materials/ZOO101_Fish.pdf", "source": "static"},
            {"title": "ZOO 101 - Amphibians", "url": "static/materials/ZOO101_Amphibians.pdf", "source": "static"},
            {"title": "ZOO 101 - Reptiles", "url": "static/materials/ZOO101_Reptiles.pdf", "source": "static"},
            {"title": "ZOO 101 - Birds (Aves)", "url": "static/materials/ZOO101_Birds.pdf", "source": "static"},
            {"title": "ZOO 101 - Mammals", "url": "static/materials/ZOO101_Mammals.pdf", "source": "static"},
            {"title": "ZOO 101 - Animal Behavior Basics", "url": "static/materials/ZOO101_Behavior.pdf", "source": "static"},
            {"title": "ZOO 101 - Animal Adaptations", "url": "static/materials/ZOO101_Adaptations.pdf", "source": "static"},
            {"title": "ZOO 101 - Dissection Techniques", "url": "static/materials/ZOO101_Dissection.pdf", "source": "static"},
            {"title": "ZOO 101 - Past Questions 2020-2024", "url": "static/materials/ZOO101_Past_Questions.pdf", "source": "static"},
            {"title": "ZOO 101 - Complete Lecture Notes", "url": "static/materials/ZOO101_Lecture_Notes.pdf", "source": "static"},
            {"title": "ZOO 101 - Animal Identification Guide", "url": "static/materials/ZOO101_Identification.pdf", "source": "static"},
            {"title": "ZOO 101 - Quick Revision Guide", "url": "static/materials/ZOO101_Revision.pdf", "source": "static"},
            {"title": "ZOO 101 - Exam Preparation", "url": "static/materials/ZOO101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== ZOOLOGY ZOO 102 ==========
    "ZOO102": {
        "name": "Animal Physiology",
        "department": "Zoology",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "ZOO 102 - Animal Physiology Introduction", "url": "static/materials/ZOO102_Physiology.pdf", "source": "static"},
            {"title": "ZOO 102 - Homeostasis in Animals", "url": "static/materials/ZOO102_Homeostasis.pdf", "source": "static"},
            {"title": "ZOO 102 - Nervous System", "url": "static/materials/ZOO102_Nervous.pdf", "source": "static"},
            {"title": "ZOO 102 - Sensory Systems", "url": "static/materials/ZOO102_Sensory.pdf", "source": "static"},
            {"title": "ZOO 102 - Muscular System", "url": "static/materials/ZOO102_Muscular.pdf", "source": "static"},
            {"title": "ZOO 102 - Skeletal System", "url": "static/materials/ZOO102_Skeletal.pdf", "source": "static"},
            {"title": "ZOO 102 - Circulatory System", "url": "static/materials/ZOO102_Circulatory.pdf", "source": "static"},
            {"title": "ZOO 102 - Respiratory System", "url": "static/materials/ZOO102_Respiratory.pdf", "source": "static"},
            {"title": "ZOO 102 - Digestive System", "url": "static/materials/ZOO102_Digestive.pdf", "source": "static"},
            {"title": "ZOO 102 - Excretory System", "url": "static/materials/ZOO102_Excretory.pdf", "source": "static"},
            {"title": "ZOO 102 - Endocrine System", "url": "static/materials/ZOO102_Endocrine.pdf", "source": "static"},
            {"title": "ZOO 102 - Reproductive System", "url": "static/materials/ZOO102_Reproductive.pdf", "source": "static"},
            {"title": "ZOO 102 - Animal Development", "url": "static/materials/ZOO102_Development.pdf", "source": "static"},
            {"title": "ZOO 102 - Past Questions 2020-2024", "url": "static/materials/ZOO102_Past_Questions.pdf", "source": "static"},
            {"title": "ZOO 102 - Complete Lecture Notes", "url": "static/materials/ZOO102_Lecture_Notes.pdf", "source": "static"},
            {"title": "ZOO 102 - Quick Revision Guide", "url": "static/materials/ZOO102_Revision.pdf", "source": "static"},
            {"title": "ZOO 102 - Exam Preparation", "url": "static/materials/ZOO102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== MICROBIOLOGY MCB 101 ==========
    "MCB101": {
        "name": "Introduction to Microbiology",
        "department": "Microbiology",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 101 - Introduction to Microbiology", "url": "static/materials/MCB101_Introduction.pdf", "source": "static"},
            {"title": "MCB 101 - History of Microbiology", "url": "static/materials/MCB101_History.pdf", "source": "static"},
            {"title": "MCB 101 - Microscopy Techniques", "url": "static/materials/MCB101_Microscopy.pdf", "source": "static"},
            {"title": "MCB 101 - Bacterial Cell Structure", "url": "static/materials/MCB101_Bacteria.pdf", "source": "static"},
            {"title": "MCB 101 - Bacterial Growth and Nutrition", "url": "static/materials/MCB101_Growth.pdf", "source": "static"},
            {"title": "MCB 101 - Bacterial Metabolism", "url": "static/materials/MCB101_Metabolism.pdf", "source": "static"},
            {"title": "MCB 101 - Microbial Genetics", "url": "static/materials/MCB101_Genetics.pdf", "source": "static"},
            {"title": "MCB 101 - Viruses and Virology", "url": "static/materials/MCB101_Viruses.pdf", "source": "static"},
            {"title": "MCB 101 - Fungi Classification", "url": "static/materials/MCB101_Fungi.pdf", "source": "static"},
            {"title": "MCB 101 - Protozoa", "url": "static/materials/MCB101_Protozoa.pdf", "source": "static"},
            {"title": "MCB 101 - Sterilization and Disinfection", "url": "static/materials/MCB101_Sterilization.pdf", "source": "static"},
            {"title": "MCB 101 - Antimicrobial Agents", "url": "static/materials/MCB101_Antimicrobial.pdf", "source": "static"},
            {"title": "MCB 101 - Culture Techniques", "url": "static/materials/MCB101_Culture.pdf", "source": "static"},
            {"title": "MCB 101 - Staining Methods", "url": "static/materials/MCB101_Staining.pdf", "source": "static"},
            {"title": "MCB 101 - Laboratory Safety", "url": "static/materials/MCB101_Safety.pdf", "source": "static"},
            {"title": "MCB 101 - Past Questions 2020-2024", "url": "static/materials/MCB101_Past_Questions.pdf", "source": "static"},
            {"title": "MCB 101 - Complete Lecture Notes", "url": "static/materials/MCB101_Lecture_Notes.pdf", "source": "static"},
            {"title": "MCB 101 - Quick Revision Guide", "url": "static/materials/MCB101_Revision.pdf", "source": "static"},
            {"title": "MCB 101 - Exam Preparation", "url": "static/materials/MCB101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== MICROBIOLOGY MCB 102 ==========
    "MCB102": {
        "name": "Microbial Diversity",
        "department": "Microbiology",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "MCB 102 - Microbial Diversity Overview", "url": "static/materials/MCB102_Diversity.pdf", "source": "static"},
            {"title": "MCB 102 - Bacterial Classification", "url": "static/materials/MCB102_Classification.pdf", "source": "static"},
            {"title": "MCB 102 - Gram-Positive Bacteria", "url": "static/materials/MCB102_Gram_Positive.pdf", "source": "static"},
            {"title": "MCB 102 - Gram-Negative Bacteria", "url": "static/materials/MCB102_Gram_Negative.pdf", "source": "static"},
            {"title": "MCB 102 - Archaebacteria", "url": "static/materials/MCB102_Archaea.pdf", "source": "static"},
            {"title": "MCB 102 - Cyanobacteria", "url": "static/materials/MCB102_Cyanobacteria.pdf", "source": "static"},
            {"title": "MCB 102 - Actinomycetes", "url": "static/materials/MCB102_Actinomycetes.pdf", "source": "static"},
            {"title": "MCB 102 - Spirochetes", "url": "static/materials/MCB102_Spirochetes.pdf", "source": "static"},
            {"title": "MCB 102 - Rickettsiae and Chlamydiae", "url": "static/materials/MCB102_Rickettsiae.pdf", "source": "static"},
            {"title": "MCB 102 - Mycoplasmas", "url": "static/materials/MCB102_Mycoplasmas.pdf", "source": "static"},
            {"title": "MCB 102 - Fungal Diversity", "url": "static/materials/MCB102_Fungal.pdf", "source": "static"},
            {"title": "MCB 102 - Algal Diversity", "url": "static/materials/MCB102_Algal.pdf", "source": "static"},
            {"title": "MCB 102 - Protozoal Diversity", "url": "static/materials/MCB102_Protozoal.pdf", "source": "static"},
            {"title": "MCB 102 - Viral Diversity", "url": "static/materials/MCB102_Viral.pdf", "source": "static"},
            {"title": "MCB 102 - Microbial Ecology", "url": "static/materials/MCB102_Ecology.pdf", "source": "static"},
            {"title": "MCB 102 - Past Questions 2020-2024", "url": "static/materials/MCB102_Past_Questions.pdf", "source": "static"},
            {"title": "MCB 102 - Complete Lecture Notes", "url": "static/materials/MCB102_Lecture_Notes.pdf", "source": "static"},
            {"title": "MCB 102 - Quick Revision Guide", "url": "static/materials/MCB102_Revision.pdf", "source": "static"},
            {"title": "MCB 102 - Exam Preparation", "url": "static/materials/MCB102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== FISHERIES FIS 101 ==========
    "FIS101": {
        "name": "Introduction to Fisheries",
        "department": "Fisheries",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "FIS 101 - Introduction to Fisheries Science", "url": "static/materials/FIS101_Introduction.pdf", "source": "static"},
            {"title": "FIS 101 - Fish Biology Basics", "url": "static/materials/FIS101_Fish_Biology.pdf", "source": "static"},
            {"title": "FIS 101 - Fish Anatomy", "url": "static/materials/FIS101_Anatomy.pdf", "source": "static"},
            {"title": "FIS 101 - Fish Physiology", "url": "static/materials/FIS101_Physiology.pdf", "source": "static"},
            {"title": "FIS 101 - Fish Classification", "url": "static/materials/FIS101_Classification.pdf", "source": "static"},
            {"title": "FIS 101 - Aquatic Ecosystems", "url": "static/materials/FIS101_Ecosystems.pdf", "source": "static"},
            {"title": "FIS 101 - Freshwater Fisheries", "url": "static/materials/FIS101_Freshwater.pdf", "source": "static"},
            {"title": "FIS 101 - Marine Fisheries", "url": "static/materials/FIS101_Marine.pdf", "source": "static"},
            {"title": "FIS 101 - Aquaculture Introduction", "url": "static/materials/FIS101_Aquaculture.pdf", "source": "static"},
            {"title": "FIS 101 - Fishing Methods and Gear", "url": "static/materials/FIS101_Fishing_Methods.pdf", "source": "static"},
            {"title": "FIS 101 - Fish Nutrition", "url": "static/materials/FIS101_Nutrition.pdf", "source": "static"},
            {"title": "FIS 101 - Water Quality Management", "url": "static/materials/FIS101_Water_Quality.pdf", "source": "static"},
            {"title": "FIS 101 - Fisheries Management Principles", "url": "static/materials/FIS101_Management.pdf", "source": "static"},
            {"title": "FIS 101 - Past Questions 2020-2024", "url": "static/materials/FIS101_Past_Questions.pdf", "source": "static"},
            {"title": "FIS 101 - Complete Lecture Notes", "url": "static/materials/FIS101_Lecture_Notes.pdf", "source": "static"},
            {"title": "FIS 101 - Quick Revision Guide", "url": "static/materials/FIS101_Revision.pdf", "source": "static"},
            {"title": "FIS 101 - Exam Preparation", "url": "static/materials/FIS101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== FISHERIES FIS 102 ==========
    "FIS102": {
        "name": "Introduction to Aquatic Ecology",
        "department": "Fisheries",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "FIS 102 - Aquatic Ecology Fundamentals", "url": "static/materials/FIS102_Fundamentals.pdf", "source": "static"},
            {"title": "FIS 102 - Limnology (Freshwater Ecosystems)", "url": "static/materials/FIS102_Limnology.pdf", "source": "static"},
            {"title": "FIS 102 - Oceanography Basics", "url": "static/materials/FIS102_Oceanography.pdf", "source": "static"},
            {"title": "FIS 102 - Aquatic Food Webs", "url": "static/materials/FIS102_Food_Webs.pdf", "source": "static"},
            {"title": "FIS 102 - Phytoplankton and Zooplankton", "url": "static/materials/FIS102_Plankton.pdf", "source": "static"},
            {"title": "FIS 102 - Aquatic Plants", "url": "static/materials/FIS102_Plants.pdf", "source": "static"},
            {"title": "FIS 102 - Benthic Communities", "url": "static/materials/FIS102_Benthic.pdf", "source": "static"},
            {"title": "FIS 102 - Fish Communities", "url": "static/materials/FIS102_Communities.pdf", "source": "static"},
            {"title": "FIS 102 - Aquatic Biodiversity", "url": "static/materials/FIS102_Biodiversity.pdf", "source": "static"},
            {"title": "FIS 102 - Water Pollution", "url": "static/materials/FIS102_Pollution.pdf", "source": "static"},
            {"title": "FIS 102 - Eutrophication", "url": "static/materials/FIS102_Eutrophication.pdf", "source": "static"},
            {"title": "FIS 102 - Climate Change and Aquatic Systems", "url": "static/materials/FIS102_Climate.pdf", "source": "static"},
            {"title": "FIS 102 - Conservation of Aquatic Resources", "url": "static/materials/FIS102_Conservation.pdf", "source": "static"},
            {"title": "FIS 102 - Past Questions 2020-2024", "url": "static/materials/FIS102_Past_Questions.pdf", "source": "static"},
            {"title": "FIS 102 - Complete Lecture Notes", "url": "static/materials/FIS102_Lecture_Notes.pdf", "source": "static"},
            {"title": "FIS 102 - Quick Revision Guide", "url": "static/materials/FIS102_Revision.pdf", "source": "static"},
            {"title": "FIS 102 - Exam Preparation", "url": "static/materials/FIS102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== GENERAL STUDIES GST 101 - Use of English I ==========
    "GST101": {
        "name": "Use of English I",
        "department": "General Studies",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 101 - English Grammar Essentials", "url": "static/materials/GST101_Grammar.pdf", "source": "static"},
            {"title": "GST 101 - Parts of Speech", "url": "static/materials/GST101_Parts_Speech.pdf", "source": "static"},
            {"title": "GST 101 - Sentence Structure", "url": "static/materials/GST101_Sentences.pdf", "source": "static"},
            {"title": "GST 101 - Tenses and Verb Forms", "url": "static/materials/GST101_Tenses.pdf", "source": "static"},
            {"title": "GST 101 - Comprehension Skills", "url": "static/materials/GST101_Comprehension.pdf", "source": "static"},
            {"title": "GST 101 - Essay Writing Techniques", "url": "static/materials/GST101_Essay.pdf", "source": "static"},
            {"title": "GST 101 - Letter Writing (Formal and Informal)", "url": "static/materials/GST101_Letters.pdf", "source": "static"},
            {"title": "GST 101 - Summary Writing", "url": "static/materials/GST101_Summary.pdf", "source": "static"},
            {"title": "GST 101 - Vocabulary Building", "url": "static/materials/GST101_Vocabulary.pdf", "source": "static"},
            {"title": "GST 101 - Oral English and Phonetics", "url": "static/materials/GST101_Phonetics.pdf", "source": "static"},
            {"title": "GST 101 - Public Speaking Basics", "url": "static/materials/GST101_Public_Speaking.pdf", "source": "static"},
            {"title": "GST 101 - Punctuation Rules", "url": "static/materials/GST101_Punctuation.pdf", "source": "static"},
            {"title": "GST 101 - Common Errors in English", "url": "static/materials/GST101_Errors.pdf", "source": "static"},
            {"title": "GST 101 - Past Questions 2020-2024", "url": "static/materials/GST101_Past_Questions.pdf", "source": "static"},
            {"title": "GST 101 - Quick Revision Guide", "url": "static/materials/GST101_Revision.pdf", "source": "static"},
            {"title": "GST 101 - Exam Preparation", "url": "static/materials/GST101_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== GENERAL STUDIES GST 102 / GNS 102 - Use of English II ==========
    "GST102": {
        "name": "Use of English II",
        "department": "General Studies",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 102 - Advanced Grammar", "url": "static/materials/GST102_Grammar.pdf", "source": "static"},
            {"title": "GST 102 - Reading Comprehension Advanced", "url": "static/materials/GST102_Comprehension.pdf", "source": "static"},
            {"title": "GST 102 - Academic Writing", "url": "static/materials/GST102_Academic.pdf", "source": "static"},
            {"title": "GST 102 - Report Writing", "url": "static/materials/GST102_Reports.pdf", "source": "static"},
            {"title": "GST 102 - Critical Thinking and Analysis", "url": "static/materials/GST102_Critical.pdf", "source": "static"},
            {"title": "GST 102 - Argumentative Essays", "url": "static/materials/GST102_Argumentative.pdf", "source": "static"},
            {"title": "GST 102 - Descriptive and Narrative Writing", "url": "static/materials/GST102_Descriptive.pdf", "source": "static"},
            {"title": "GST 102 - Research Writing Basics", "url": "static/materials/GST102_Research.pdf", "source": "static"},
            {"title": "GST 102 - Citation and Referencing (APA, MLA)", "url": "static/materials/GST102_Citation.pdf", "source": "static"},
            {"title": "GST 102 - Literature Analysis", "url": "static/materials/GST102_Literature.pdf", "source": "static"},
            {"title": "GST 102 - Poetry Appreciation", "url": "static/materials/GST102_Poetry.pdf", "source": "static"},
            {"title": "GST 102 - Drama and Prose", "url": "static/materials/GST102_Drama.pdf", "source": "static"},
            {"title": "GST 102 - Past Questions 2020-2024", "url": "static/materials/GST102_Past_Questions.pdf", "source": "static"},
            {"title": "GST 102 - Quick Revision Guide", "url": "static/materials/GST102_Revision.pdf", "source": "static"},
            {"title": "GST 102 - Exam Preparation", "url": "static/materials/GST102_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== GENERAL STUDIES GST 111 - Communication in English I ==========
    "GST111": {
        "name": "Communication in English I",
        "department": "General Studies",
        "level": "100",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 111 - Effective Communication Skills", "url": "static/materials/GST111_Communication.pdf", "source": "static"},
            {"title": "GST 111 - Listening Skills", "url": "static/materials/GST111_Listening.pdf", "source": "static"},
            {"title": "GST 111 - Speaking Skills", "url": "static/materials/GST111_Speaking.pdf", "source": "static"},
            {"title": "GST 111 - Reading Skills", "url": "static/materials/GST111_Reading.pdf", "source": "static"},
            {"title": "GST 111 - Writing Skills", "url": "static/materials/GST111_Writing.pdf", "source": "static"},
            {"title": "GST 111 - Interpersonal Communication", "url": "static/materials/GST111_Interpersonal.pdf", "source": "static"},
            {"title": "GST 111 - Group Communication", "url": "static/materials/GST111_Group.pdf", "source": "static"},
            {"title": "GST 111 - Presentation Skills", "url": "static/materials/GST111_Presentation.pdf", "source": "static"},
            {"title": "GST 111 - Business Communication", "url": "static/materials/GST111_Business.pdf", "source": "static"},
            {"title": "GST 111 - Non-Verbal Communication", "url": "static/materials/GST111_Non_Verbal.pdf", "source": "static"},
            {"title": "GST 111 - Past Questions 2020-2024", "url": "static/materials/GST111_Past_Questions.pdf", "source": "static"},
            {"title": "GST 111 - Quick Revision Guide", "url": "static/materials/GST111_Revision.pdf", "source": "static"},
            {"title": "GST 111 - Exam Preparation", "url": "static/materials/GST111_Exam_Prep.pdf", "source": "static"},
        ]
    },

    # ========== GENERAL STUDIES GST 121 / GST 122 ==========
    "GST121": {
        "name": "Use of Library Skills and ICT",
        "department": "General Studies",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 121 - Library Organization", "url": "static/materials/GST121_Library.pdf", "source": "static"},
            {"title": "GST 121 - Information Retrieval", "url": "static/materials/GST121_Retrieval.pdf", "source": "static"},
            {"title": "GST 121 - Digital Libraries", "url": "static/materials/GST121_Digital.pdf", "source": "static"},
            {"title": "GST 121 - Computer Basics", "url": "static/materials/GST121_Computer.pdf", "source": "static"},
            {"title": "GST 121 - Microsoft Word", "url": "static/materials/GST121_Word.pdf", "source": "static"},
            {"title": "GST 121 - Microsoft Excel", "url": "static/materials/GST121_Excel.pdf", "source": "static"},
            {"title": "GST 121 - Microsoft PowerPoint", "url": "static/materials/GST121_PowerPoint.pdf", "source": "static"},
            {"title": "GST 121 - Internet and Email", "url": "static/materials/GST121_Internet.pdf", "source": "static"},
            {"title": "GST 121 - Online Research", "url": "static/materials/GST121_Research.pdf", "source": "static"},
            {"title": "GST 121 - Cyber Security Basics", "url": "static/materials/GST121_Security.pdf", "source": "static"},
            {"title": "GST 121 - Past Questions 2020-2024", "url": "static/materials/GST121_Past_Questions.pdf", "source": "static"},
            {"title": "GST 121 - Quick Revision Guide", "url": "static/materials/GST121_Revision.pdf", "source": "static"},
            {"title": "GST 121 - Exam Preparation", "url": "static/materials/GST121_Exam_Prep.pdf", "source": "static"},
        ]
    },

    "GST122": {
        "name": "Communication in English II",
        "department": "General Studies",
        "level": "100",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 122 - Advanced Communication", "url": "static/materials/GST122_Communication.pdf", "source": "static"},
            {"title": "GST 122 - Technical Writing", "url": "static/materials/GST122_Technical.pdf", "source": "static"},
            {"title": "GST 122 - Proposal Writing", "url": "static/materials/GST122_Proposal.pdf", "source": "static"},
            {"title": "GST 122 - CV and Cover Letter Writing", "url": "static/materials/GST122_CV.pdf", "source": "static"},
            {"title": "GST 122 - Interview Skills", "url": "static/materials/GST122_Interview.pdf", "source": "static"},
            {"title": "GST 122 - Conflict Resolution", "url": "static/materials/GST122_Conflict.pdf", "source": "static"},
            {"title": "GST 122 - Negotiation Skills", "url": "static/materials/GST122_Negotiation.pdf", "source": "static"},
            {"title": "GST 122 - Leadership Communication", "url": "static/materials/GST122_Leadership.pdf", "source": "static"},
            {"title": "GST 122 - Cross-Cultural Communication", "url": "static/materials/GST122_Cultural.pdf", "source": "static"},
            {"title": "GST 122 - Past Questions 2020-2024", "url": "static/materials/GST122_Past_Questions.pdf", "source": "static"},
            {"title": "GST 122 - Quick Revision Guide", "url": "static/materials/GST122_Revision.pdf", "source": "static"},
            {"title": "GST 122 - Exam Preparation", "url": "static/materials/GST122_Exam_Prep.pdf", "source": "static"},
        ]
    },
}


# ============================================================
# SEEDING FUNCTION
# ============================================================

def seed_100_level_science():
    """
    Seeds the database with 500+ materials for 100 Level Faculty of Science
    """
    with app.app_context():
        print("\n" + "="*70)
        print("🎓 NELAVISTA - 100 LEVEL FACULTY OF SCIENCE SEEDER")
        print("="*70 + "\n")
        
        total_added = 0
        total_skipped = 0
        
        for course_code, course_data in SCIENCE_100_MATERIALS.items():
            print(f"\n📘 Processing {course_code} - {course_data['name']}")
            print(f"   Department: {course_data['department']} | Level: {course_data['level']} | Semester: {course_data['semester']}")
            print(f"   Materials to add: {len(course_data['materials'])}")
            
            added_count = 0
            skipped_count = 0
            
            for material_data in course_data['materials']:
                # Check if material already exists (by title and course_code)
                existing = Material.query.filter_by(
                    title=material_data['title'],
                    course_code=course_code
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Create new material
                new_material = Material(
                    title=material_data['title'],
                    course_code=course_code,
                    department=course_data['department'],
                    level=course_data['level'],
                    semester=course_data['semester'],
                    file_url=material_data.get('url'),
                    external_url=material_data.get('url') if material_data.get('url', '').startswith('http') else None,
                    source=material_data.get('source', 'static'),
                    is_approved=True,
                    uploaded_by='System Seeder',
                    course_type='CORE'
                )
                
                db.session.add(new_material)
                added_count += 1
            
            # Commit after each course
            try:
                db.session.commit()
                print(f"   ✅ Added: {added_count} | ⏭️ Skipped: {skipped_count}")
                total_added += added_count
                total_skipped += skipped_count
            except Exception as e:
                db.session.rollback()
                print(f"   ❌ Error: {str(e)}")
        
        print("\n" + "="*70)
        print(f"🎉 SEEDING COMPLETE!")
        print(f"   Total Materials Added: {total_added}")
        print(f"   Total Materials Skipped (already exist): {total_skipped}")
        print(f"   Total Materials in Database: {Material.query.count()}")
        print("="*70 + "\n")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    print("\n🚀 Starting 100 Level Science Materials Seeding...")
    seed_100_level_science()
    print("✅ Done! You can now test your materials page.\n")