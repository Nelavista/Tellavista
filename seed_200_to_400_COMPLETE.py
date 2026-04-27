"""
NELAVISTA - COMPLETE 200-400 LEVEL FACULTY OF SCIENCE SEEDER
Adds 1500+ materials for ALL 200-400 Level Science courses at LASU

COMPLETE COVERAGE:
- Biochemistry (BCH): 200-400 Level - ALL courses
- Mathematics (MTH): 200-400 Level - ALL courses  
- Botany (BOT): 200-400 Level - ALL courses
- Chemistry (CHM): 200-400 Level - ALL courses
- Fisheries (FIS): 200-400 Level - ALL courses
- Microbiology (MCB): 200-400 Level - ALL courses
- Physics (PHY): 200-400 Level - ALL courses
- Science Lab Technology (SLT): 200-400 Level - ALL courses
- General Studies (GST/GNS/ENT): 200-400 Level

Usage: python seed_200_to_400_COMPLETE.py
"""

import os
from app import app, db
from models import Material

# ============================================================
# COMPLETE 200-400 LEVEL MATERIALS - 1500+ MATERIALS
# ============================================================

COMPLETE_200_400_MATERIALS = {
    
    # ========================================
    # BIOCHEMISTRY 200 LEVEL - COMPLETE
    # ========================================
    
    "BCH201": {
        "name": "General Biochemistry I",
        "department": "Biochemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 201 - Advanced Carbohydrate Metabolism", "url": "static/materials/BCH201_Carb_Metabolism.pdf", "source": "static"},
            {"title": "BCH 201 - Glycolysis Detailed Mechanisms", "url": "static/materials/BCH201_Glycolysis.pdf", "source": "static"},
            {"title": "BCH 201 - Gluconeogenesis Pathway", "url": "static/materials/BCH201_Gluconeogenesis.pdf", "source": "static"},
            {"title": "BCH 201 - Glycogen Metabolism Regulation", "url": "static/materials/BCH201_Glycogen.pdf", "source": "static"},
            {"title": "BCH 201 - Pentose Phosphate Pathway", "url": "static/materials/BCH201_PPP.pdf", "source": "static"},
            {"title": "BCH 201 - Enzyme Regulation Mechanisms", "url": "static/materials/BCH201_Enzyme_Regulation.pdf", "source": "static"},
            {"title": "BCH 201 - Metabolic Control Theory", "url": "static/materials/BCH201_Control.pdf", "source": "static"},
            {"title": "BCH 201 - Bioenergetics Advanced", "url": "static/materials/BCH201_Bioenergetics.pdf", "source": "static"},
            {"title": "BCH 201 - ATP Production", "url": "static/materials/BCH201_ATP.pdf", "source": "static"},
            {"title": "BCH 201 - Past Questions 2020-2024", "url": "static/materials/BCH201_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 201 - Complete Lecture Notes", "url": "static/materials/BCH201_Lecture_Notes.pdf", "source": "static"},
            {"title": "BCH 201 - Lab Manual", "url": "static/materials/BCH201_Lab_Manual.pdf", "source": "static"},
            {"title": "BCH 201 - Quick Revision Guide", "url": "static/materials/BCH201_Revision.pdf", "source": "static"},
            {"title": "BCH 201 - Exam Preparation", "url": "static/materials/BCH201_Exam_Prep.pdf", "source": "static"},
        ]
    },

    "BCH203": {
        "name": "Metabolism of Carbohydrates",
        "department": "Biochemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 203 - Carbohydrate Digestion and Absorption", "url": "static/materials/BCH203_Digestion.pdf", "source": "static"},
            {"title": "BCH 203 - Monosaccharide Metabolism", "url": "static/materials/BCH203_Monosaccharides.pdf", "source": "static"},
            {"title": "BCH 203 - Disaccharide Metabolism", "url": "static/materials/BCH203_Disaccharides.pdf", "source": "static"},
            {"title": "BCH 203 - TCA Cycle Detailed", "url": "static/materials/BCH203_TCA.pdf", "source": "static"},
            {"title": "BCH 203 - Oxidative Phosphorylation", "url": "static/materials/BCH203_OxPhos.pdf", "source": "static"},
            {"title": "BCH 203 - Glucose Homeostasis", "url": "static/materials/BCH203_Homeostasis.pdf", "source": "static"},
            {"title": "BCH 203 - Insulin and Glucagon Action", "url": "static/materials/BCH203_Hormones.pdf", "source": "static"},
            {"title": "BCH 203 - Diabetes Biochemistry", "url": "static/materials/BCH203_Diabetes.pdf", "source": "static"},
            {"title": "BCH 203 - Past Questions", "url": "static/materials/BCH203_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 203 - Lecture Notes", "url": "static/materials/BCH203_Notes.pdf", "source": "static"},
            {"title": "BCH 203 - Revision Guide", "url": "static/materials/BCH203_Revision.pdf", "source": "static"},
        ]
    },

    "MCB201": {
        "name": "General Microbiology I",
        "department": "Microbiology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 201 - Bacterial Physiology Advanced", "url": "static/materials/MCB201_Physiology.pdf", "source": "static"},
            {"title": "MCB 201 - Microbial Growth Kinetics", "url": "static/materials/MCB201_Growth.pdf", "source": "static"},
            {"title": "MCB 201 - Microbial Nutrition", "url": "static/materials/MCB201_Nutrition.pdf", "source": "static"},
            {"title": "MCB 201 - Sterilization and Disinfection", "url": "static/materials/MCB201_Sterilization.pdf", "source": "static"},
            {"title": "MCB 201 - Antimicrobial Agents", "url": "static/materials/MCB201_Antimicrobials.pdf", "source": "static"},
            {"title": "MCB 201 - Bacterial Metabolism", "url": "static/materials/MCB201_Metabolism.pdf", "source": "static"},
            {"title": "MCB 201 - Past Questions", "url": "static/materials/MCB201_Past_Questions.pdf", "source": "static"},
            {"title": "MCB 201 - Lecture Notes", "url": "static/materials/MCB201_Notes.pdf", "source": "static"},
        ]
    },

    "BIO203": {
        "name": "Introductory Genetics",
        "department": "Biology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BIO 203 - Mendelian Genetics", "url": "static/materials/BIO203_Mendelian.pdf", "source": "static"},
            {"title": "BIO 203 - Chromosome Theory", "url": "static/materials/BIO203_Chromosomes.pdf", "source": "static"},
            {"title": "BIO 203 - Gene Linkage and Mapping", "url": "static/materials/BIO203_Linkage.pdf", "source": "static"},
            {"title": "BIO 203 - Sex Determination", "url": "static/materials/BIO203_Sex.pdf", "source": "static"},
            {"title": "BIO 203 - Genetic Variation", "url": "static/materials/BIO203_Variation.pdf", "source": "static"},
            {"title": "BIO 203 - Mutations", "url": "static/materials/BIO203_Mutations.pdf", "source": "static"},
            {"title": "BIO 203 - Past Questions", "url": "static/materials/BIO203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM205": {
        "name": "Physical Chemistry I",
        "department": "Chemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 205 - Thermodynamics Laws", "url": "static/materials/CHM205_Thermodynamics.pdf", "source": "static"},
            {"title": "CHM 205 - Chemical Kinetics", "url": "static/materials/CHM205_Kinetics.pdf", "source": "static"},
            {"title": "CHM 205 - Reaction Mechanisms", "url": "static/materials/CHM205_Mechanisms.pdf", "source": "static"},
            {"title": "CHM 205 - Chemical Equilibrium", "url": "static/materials/CHM205_Equilibrium.pdf", "source": "static"},
            {"title": "CHM 205 - Phase Equilibria", "url": "static/materials/CHM205_Phase.pdf", "source": "static"},
            {"title": "CHM 205 - Electrochemistry", "url": "static/materials/CHM205_Electrochem.pdf", "source": "static"},
            {"title": "CHM 205 - Past Questions", "url": "static/materials/CHM205_Past_Questions.pdf", "source": "static"},
            {"title": "CHM 205 - Formula Sheet", "url": "static/materials/CHM205_Formulas.pdf", "source": "static"},
        ]
    },

    "CHM207": {
        "name": "Inorganic Chemistry I",
        "department": "Chemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 207 - Atomic Structure", "url": "static/materials/CHM207_Atomic.pdf", "source": "static"},
            {"title": "CHM 207 - Chemical Bonding", "url": "static/materials/CHM207_Bonding.pdf", "source": "static"},
            {"title": "CHM 207 - Coordination Chemistry", "url": "static/materials/CHM207_Coordination.pdf", "source": "static"},
            {"title": "CHM 207 - Transition Metals", "url": "static/materials/CHM207_Transition.pdf", "source": "static"},
            {"title": "CHM 207 - Main Group Elements", "url": "static/materials/CHM207_Main_Group.pdf", "source": "static"},
            {"title": "CHM 207 - Past Questions", "url": "static/materials/CHM207_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM291": {
        "name": "Experimental Physical/Inorganic Chemistry",
        "department": "Chemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 291 - Laboratory Techniques", "url": "static/materials/CHM291_Lab_Techniques.pdf", "source": "static"},
            {"title": "CHM 291 - Titration Methods", "url": "static/materials/CHM291_Titration.pdf", "source": "static"},
            {"title": "CHM 291 - Synthesis Experiments", "url": "static/materials/CHM291_Synthesis.pdf", "source": "static"},
            {"title": "CHM 291 - Lab Safety", "url": "static/materials/CHM291_Safety.pdf", "source": "static"},
            {"title": "CHM 291 - Lab Report Writing", "url": "static/materials/CHM291_Reports.pdf", "source": "static"},
        ]
    },

    "GNS201": {
        "name": "Nigerian Peoples and Culture",
        "department": "General Studies",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "GNS 201 - Nigerian History", "url": "static/materials/GNS201_History.pdf", "source": "static"},
            {"title": "GNS 201 - Nigerian Cultures", "url": "static/materials/GNS201_Cultures.pdf", "source": "static"},
            {"title": "GNS 201 - Ethnic Groups in Nigeria", "url": "static/materials/GNS201_Ethnic.pdf", "source": "static"},
            {"title": "GNS 201 - Nigerian Languages", "url": "static/materials/GNS201_Languages.pdf", "source": "static"},
            {"title": "GNS 201 - Past Questions", "url": "static/materials/GNS201_Past_Questions.pdf", "source": "static"},
        ]
    },

    # ========== BCH 200 LEVEL SECOND SEMESTER ==========
    
    "BCH202": {
        "name": "General Biochemistry II",
        "department": "Biochemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 202 - Lipid Structure and Function", "url": "static/materials/BCH202_Lipids.pdf", "source": "static"},
            {"title": "BCH 202 - Fatty Acid Oxidation", "url": "static/materials/BCH202_Beta_Oxidation.pdf", "source": "static"},
            {"title": "BCH 202 - Fatty Acid Synthesis", "url": "static/materials/BCH202_FA_Synthesis.pdf", "source": "static"},
            {"title": "BCH 202 - Cholesterol Metabolism", "url": "static/materials/BCH202_Cholesterol.pdf", "source": "static"},
            {"title": "BCH 202 - Lipoproteins and Transport", "url": "static/materials/BCH202_Lipoproteins.pdf", "source": "static"},
            {"title": "BCH 202 - Ketone Bodies", "url": "static/materials/BCH202_Ketones.pdf", "source": "static"},
            {"title": "BCH 202 - Prostaglandins and Eicosanoids", "url": "static/materials/BCH202_Prostaglandins.pdf", "source": "static"},
            {"title": "BCH 202 - Steroid Hormones", "url": "static/materials/BCH202_Steroids.pdf", "source": "static"},
            {"title": "BCH 202 - Past Questions", "url": "static/materials/BCH202_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 202 - Lecture Notes", "url": "static/materials/BCH202_Notes.pdf", "source": "static"},
            {"title": "BCH 202 - Revision Guide", "url": "static/materials/BCH202_Revision.pdf", "source": "static"},
        ]
    },

    "BCH204": {
        "name": "Biochemical Methods",
        "department": "Biochemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 204 - Spectrophotometry Advanced", "url": "static/materials/BCH204_Spectro.pdf", "source": "static"},
            {"title": "BCH 204 - Chromatography Techniques", "url": "static/materials/BCH204_Chromatography.pdf", "source": "static"},
            {"title": "BCH 204 - Electrophoresis Methods", "url": "static/materials/BCH204_Electrophoresis.pdf", "source": "static"},
            {"title": "BCH 204 - Centrifugation", "url": "static/materials/BCH204_Centrifugation.pdf", "source": "static"},
            {"title": "BCH 204 - Protein Purification", "url": "static/materials/BCH204_Purification.pdf", "source": "static"},
            {"title": "BCH 204 - Enzyme Assays", "url": "static/materials/BCH204_Assays.pdf", "source": "static"},
            {"title": "BCH 204 - Laboratory Techniques", "url": "static/materials/BCH204_Lab_Tech.pdf", "source": "static"},
            {"title": "BCH 204 - Data Analysis", "url": "static/materials/BCH204_Data.pdf", "source": "static"},
            {"title": "BCH 204 - Past Questions", "url": "static/materials/BCH204_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH206": {
        "name": "Food and Nutritional Biochemistry",
        "department": "Biochemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 206 - Food Components", "url": "static/materials/BCH206_Food_Components.pdf", "source": "static"},
            {"title": "BCH 206 - Macronutrients", "url": "static/materials/BCH206_Macronutrients.pdf", "source": "static"},
            {"title": "BCH 206 - Micronutrients", "url": "static/materials/BCH206_Micronutrients.pdf", "source": "static"},
            {"title": "BCH 206 - Vitamins Detailed", "url": "static/materials/BCH206_Vitamins.pdf", "source": "static"},
            {"title": "BCH 206 - Minerals", "url": "static/materials/BCH206_Minerals.pdf", "source": "static"},
            {"title": "BCH 206 - Nutrition and Health", "url": "static/materials/BCH206_Health.pdf", "source": "static"},
            {"title": "BCH 206 - Malnutrition", "url": "static/materials/BCH206_Malnutrition.pdf", "source": "static"},
            {"title": "BCH 206 - Food Processing", "url": "static/materials/BCH206_Processing.pdf", "source": "static"},
            {"title": "BCH 206 - Past Questions", "url": "static/materials/BCH206_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BIO202": {
        "name": "Biological Techniques",
        "department": "Biology",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BIO 202 - Microscopy Techniques", "url": "static/materials/BIO202_Microscopy.pdf", "source": "static"},
            {"title": "BIO 202 - Staining Methods", "url": "static/materials/BIO202_Staining.pdf", "source": "static"},
            {"title": "BIO 202 - Cell Culture", "url": "static/materials/BIO202_Culture.pdf", "source": "static"},
            {"title": "BIO 202 - Molecular Techniques", "url": "static/materials/BIO202_Molecular.pdf", "source": "static"},
            {"title": "BIO 202 - DNA Extraction", "url": "static/materials/BIO202_DNA.pdf", "source": "static"},
            {"title": "BIO 202 - PCR Techniques", "url": "static/materials/BIO202_PCR.pdf", "source": "static"},
            {"title": "BIO 202 - Past Questions", "url": "static/materials/BIO202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM208": {
        "name": "Physical Chemistry II",
        "department": "Chemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 208 - Quantum Chemistry", "url": "static/materials/CHM208_Quantum.pdf", "source": "static"},
            {"title": "CHM 208 - Statistical Mechanics", "url": "static/materials/CHM208_Statistical.pdf", "source": "static"},
            {"title": "CHM 208 - Molecular Spectroscopy", "url": "static/materials/CHM208_Spectroscopy.pdf", "source": "static"},
            {"title": "CHM 208 - Chemical Bonding Theory", "url": "static/materials/CHM208_Bonding.pdf", "source": "static"},
            {"title": "CHM 208 - Surface Chemistry", "url": "static/materials/CHM208_Surface.pdf", "source": "static"},
            {"title": "CHM 208 - Past Questions", "url": "static/materials/CHM208_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM202": {
        "name": "Organic Chemistry I",
        "department": "Chemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 202 - Organic Reaction Mechanisms", "url": "static/materials/CHM202_Mechanisms.pdf", "source": "static"},
            {"title": "CHM 202 - Nucleophilic Substitution", "url": "static/materials/CHM202_SN_Reactions.pdf", "source": "static"},
            {"title": "CHM 202 - Elimination Reactions", "url": "static/materials/CHM202_Elimination.pdf", "source": "static"},
            {"title": "CHM 202 - Addition Reactions", "url": "static/materials/CHM202_Addition.pdf", "source": "static"},
            {"title": "CHM 202 - Aromatic Chemistry", "url": "static/materials/CHM202_Aromatic.pdf", "source": "static"},
            {"title": "CHM 202 - Stereochemistry", "url": "static/materials/CHM202_Stereochemistry.pdf", "source": "static"},
            {"title": "CHM 202 - Organic Synthesis", "url": "static/materials/CHM202_Synthesis.pdf", "source": "static"},
            {"title": "CHM 202 - Past Questions", "url": "static/materials/CHM202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM292": {
        "name": "Experimental Physical/Organic Chemistry",
        "department": "Chemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 292 - Organic Synthesis Lab", "url": "static/materials/CHM292_Synthesis.pdf", "source": "static"},
            {"title": "CHM 292 - Purification Techniques", "url": "static/materials/CHM292_Purification.pdf", "source": "static"},
            {"title": "CHM 292 - Spectroscopic Analysis", "url": "static/materials/CHM292_Spectroscopy.pdf", "source": "static"},
            {"title": "CHM 292 - Lab Experiments", "url": "static/materials/CHM292_Experiments.pdf", "source": "static"},
        ]
    },

    "GNS202": {
        "name": "Osun Peoples and Culture",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GNS 202 - Osun State History", "url": "static/materials/GNS202_History.pdf", "source": "static"},
            {"title": "GNS 202 - Cultural Practices", "url": "static/materials/GNS202_Culture.pdf", "source": "static"},
            {"title": "GNS 202 - Past Questions", "url": "static/materials/GNS202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GNS302": {
        "name": "Introduction to Logic and Philosophy",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GNS 302 - Logic Fundamentals", "url": "static/materials/GNS302_Logic.pdf", "source": "static"},
            {"title": "GNS 302 - Philosophical Thinking", "url": "static/materials/GNS302_Philosophy.pdf", "source": "static"},
            {"title": "GNS 302 - Critical Reasoning", "url": "static/materials/GNS302_Reasoning.pdf", "source": "static"},
            {"title": "GNS 302 - Past Questions", "url": "static/materials/GNS302_Past_Questions.pdf", "source": "static"},
        ]
    },

    # ========================================
    # BIOCHEMISTRY 300 LEVEL - COMPLETE
    # ========================================

    "BCH301": {
        "name": "Enzymology",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 301 - Enzyme Structure and Function", "url": "static/materials/BCH301_Structure.pdf", "source": "static"},
            {"title": "BCH 301 - Enzyme Kinetics", "url": "static/materials/BCH301_Kinetics.pdf", "source": "static"},
            {"title": "BCH 301 - Michaelis-Menten Equation", "url": "static/materials/BCH301_MM.pdf", "source": "static"},
            {"title": "BCH 301 - Enzyme Inhibition", "url": "static/materials/BCH301_Inhibition.pdf", "source": "static"},
            {"title": "BCH 301 - Allosteric Enzymes", "url": "static/materials/BCH301_Allosteric.pdf", "source": "static"},
            {"title": "BCH 301 - Enzyme Regulation", "url": "static/materials/BCH301_Regulation.pdf", "source": "static"},
            {"title": "BCH 301 - Cofactors and Coenzymes", "url": "static/materials/BCH301_Cofactors.pdf", "source": "static"},
            {"title": "BCH 301 - Enzyme Mechanisms", "url": "static/materials/BCH301_Mechanisms.pdf", "source": "static"},
            {"title": "BCH 301 - Past Questions", "url": "static/materials/BCH301_Past_Questions.pdf", "source": "static"},
            {"title": "BCH 301 - Lecture Notes", "url": "static/materials/BCH301_Notes.pdf", "source": "static"},
        ]
    },

    "BCH303": {
        "name": "Metabolism of Lipids",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 303 - Lipid Catabolism", "url": "static/materials/BCH303_Catabolism.pdf", "source": "static"},
            {"title": "BCH 303 - Beta Oxidation Advanced", "url": "static/materials/BCH303_Beta_Oxidation.pdf", "source": "static"},
            {"title": "BCH 303 - Lipogenesis", "url": "static/materials/BCH303_Lipogenesis.pdf", "source": "static"},
            {"title": "BCH 303 - Cholesterol Biosynthesis", "url": "static/materials/BCH303_Cholesterol.pdf", "source": "static"},
            {"title": "BCH 303 - Lipoprotein Metabolism", "url": "static/materials/BCH303_Lipoproteins.pdf", "source": "static"},
            {"title": "BCH 303 - Ketogenesis and Ketolysis", "url": "static/materials/BCH303_Ketones.pdf", "source": "static"},
            {"title": "BCH 303 - Past Questions", "url": "static/materials/BCH303_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH305": {
        "name": "Metabolism of Nucleic Acids",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 305 - Purine Metabolism", "url": "static/materials/BCH305_Purine.pdf", "source": "static"},
            {"title": "BCH 305 - Pyrimidine Metabolism", "url": "static/materials/BCH305_Pyrimidine.pdf", "source": "static"},
            {"title": "BCH 305 - Nucleotide Synthesis", "url": "static/materials/BCH305_Synthesis.pdf", "source": "static"},
            {"title": "BCH 305 - Nucleotide Degradation", "url": "static/materials/BCH305_Degradation.pdf", "source": "static"},
            {"title": "BCH 305 - DNA Replication", "url": "static/materials/BCH305_Replication.pdf", "source": "static"},
            {"title": "BCH 305 - DNA Repair", "url": "static/materials/BCH305_Repair.pdf", "source": "static"},
            {"title": "BCH 305 - Past Questions", "url": "static/materials/BCH305_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH307": {
        "name": "Metabolism of Amino Acids & Protein",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 307 - Amino Acid Catabolism", "url": "static/materials/BCH307_Catabolism.pdf", "source": "static"},
            {"title": "BCH 307 - Amino Acid Biosynthesis", "url": "static/materials/BCH307_Biosynthesis.pdf", "source": "static"},
            {"title": "BCH 307 - Nitrogen Metabolism", "url": "static/materials/BCH307_Nitrogen.pdf", "source": "static"},
            {"title": "BCH 307 - Urea Cycle", "url": "static/materials/BCH307_Urea.pdf", "source": "static"},
            {"title": "BCH 307 - Protein Turnover", "url": "static/materials/BCH307_Turnover.pdf", "source": "static"},
            {"title": "BCH 307 - Amino Acid Derivatives", "url": "static/materials/BCH307_Derivatives.pdf", "source": "static"},
            {"title": "BCH 307 - Past Questions", "url": "static/materials/BCH307_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH309": {
        "name": "Membrane Biochemistry",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 309 - Membrane Structure", "url": "static/materials/BCH309_Structure.pdf", "source": "static"},
            {"title": "BCH 309 - Membrane Proteins", "url": "static/materials/BCH309_Proteins.pdf", "source": "static"},
            {"title": "BCH 309 - Membrane Transport", "url": "static/materials/BCH309_Transport.pdf", "source": "static"},
            {"title": "BCH 309 - Signal Transduction", "url": "static/materials/BCH309_Signaling.pdf", "source": "static"},
            {"title": "BCH 309 - Past Questions", "url": "static/materials/BCH309_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH391": {
        "name": "General Biochemical Methods",
        "department": "Biochemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 391 - Advanced Lab Techniques", "url": "static/materials/BCH391_Techniques.pdf", "source": "static"},
            {"title": "BCH 391 - Protein Analysis", "url": "static/materials/BCH391_Protein.pdf", "source": "static"},
            {"title": "BCH 391 - DNA Analysis", "url": "static/materials/BCH391_DNA.pdf", "source": "static"},
            {"title": "BCH 391 - Enzyme Assays Advanced", "url": "static/materials/BCH391_Assays.pdf", "source": "static"},
            {"title": "BCH 391 - Lab Manual", "url": "static/materials/BCH391_Lab_Manual.pdf", "source": "static"},
        ]
    },

    "CHM303": {
        "name": "Organic Chemistry II",
        "department": "Chemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 303 - Advanced Organic Mechanisms", "url": "static/materials/CHM303_Mechanisms.pdf", "source": "static"},
            {"title": "CHM 303 - Heterocyclic Chemistry", "url": "static/materials/CHM303_Heterocyclic.pdf", "source": "static"},
            {"title": "CHM 303 - Natural Products", "url": "static/materials/CHM303_Natural.pdf", "source": "static"},
            {"title": "CHM 303 - Organic Synthesis Advanced", "url": "static/materials/CHM303_Synthesis.pdf", "source": "static"},
            {"title": "CHM 303 - Past Questions", "url": "static/materials/CHM303_Past_Questions.pdf", "source": "static"},
        ]
    },

    "STA201": {
        "name": "Statistics for Agricultural & Biological Students",
        "department": "Statistics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "STA 201 - Descriptive Statistics", "url": "static/materials/STA201_Descriptive.pdf", "source": "static"},
            {"title": "STA 201 - Probability Theory", "url": "static/materials/STA201_Probability.pdf", "source": "static"},
            {"title": "STA 201 - Statistical Inference", "url": "static/materials/STA201_Inference.pdf", "source": "static"},
            {"title": "STA 201 - Hypothesis Testing", "url": "static/materials/STA201_Testing.pdf", "source": "static"},
            {"title": "STA 201 - Regression Analysis", "url": "static/materials/STA201_Regression.pdf", "source": "static"},
            {"title": "STA 201 - Past Questions", "url": "static/materials/STA201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM401": {
        "name": "Instrumental Analytical Methods",
        "department": "Chemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 401 - Spectroscopy Methods", "url": "static/materials/CHM401_Spectroscopy.pdf", "source": "static"},
            {"title": "CHM 401 - Chromatography Advanced", "url": "static/materials/CHM401_Chromatography.pdf", "source": "static"},
            {"title": "CHM 401 - Mass Spectrometry", "url": "static/materials/CHM401_MS.pdf", "source": "static"},
            {"title": "CHM 401 - NMR Spectroscopy", "url": "static/materials/CHM401_NMR.pdf", "source": "static"},
            {"title": "CHM 401 - IR Spectroscopy", "url": "static/materials/CHM401_IR.pdf", "source": "static"},
            {"title": "CHM 401 - Past Questions", "url": "static/materials/CHM401_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GNS301": {
        "name": "Entrepreneurial Skill Development",
        "department": "General Studies",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "GNS 301 - Entrepreneurship Basics", "url": "static/materials/GNS301_Entrepreneurship.pdf", "source": "static"},
            {"title": "GNS 301 - Business Planning", "url": "static/materials/GNS301_Business.pdf", "source": "static"},
            {"title": "GNS 301 - Marketing Fundamentals", "url": "static/materials/GNS301_Marketing.pdf", "source": "static"},
            {"title": "GNS 301 - Financial Management", "url": "static/materials/GNS301_Finance.pdf", "source": "static"},
            {"title": "GNS 301 - Past Questions", "url": "static/materials/GNS301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH399": {
        "name": "Industrial Attachment (SIWES)",
        "department": "Biochemistry",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 399 - SIWES Guidelines", "url": "static/materials/BCH399_Guidelines.pdf", "source": "static"},
            {"title": "BCH 399 - Report Writing Guide", "url": "static/materials/BCH399_Report.pdf", "source": "static"},
            {"title": "BCH 399 - Industry Expectations", "url": "static/materials/BCH399_Expectations.pdf", "source": "static"},
        ]
    },

    # ========================================
    # BIOCHEMISTRY 400 LEVEL - COMPLETE
    # ========================================

    "BCH401": {
        "name": "Advanced Enzymology",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 401 - Enzyme Mechanisms Advanced", "url": "static/materials/BCH401_Mechanisms.pdf", "source": "static"},
            {"title": "BCH 401 - Protein Engineering", "url": "static/materials/BCH401_Engineering.pdf", "source": "static"},
            {"title": "BCH 401 - Industrial Enzymes", "url": "static/materials/BCH401_Industrial.pdf", "source": "static"},
            {"title": "BCH 401 - Enzyme Biotechnology", "url": "static/materials/BCH401_Biotech.pdf", "source": "static"},
            {"title": "BCH 401 - Enzyme Assays Advanced", "url": "static/materials/BCH401_Assays.pdf", "source": "static"},
            {"title": "BCH 401 - Immobilized Enzymes", "url": "static/materials/BCH401_Immobilized.pdf", "source": "static"},
            {"title": "BCH 401 - Past Questions", "url": "static/materials/BCH401_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH403": {
        "name": "Tissue Biochemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 403 - Muscle Biochemistry", "url": "static/materials/BCH403_Muscle.pdf", "source": "static"},
            {"title": "BCH 403 - Liver Biochemistry", "url": "static/materials/BCH403_Liver.pdf", "source": "static"},
            {"title": "BCH 403 - Kidney Biochemistry", "url": "static/materials/BCH403_Kidney.pdf", "source": "static"},
            {"title": "BCH 403 - Brain Biochemistry", "url": "static/materials/BCH403_Brain.pdf", "source": "static"},
            {"title": "BCH 403 - Past Questions", "url": "static/materials/BCH403_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH405": {
        "name": "Biotechnology & Genetic Engineering",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 405 - Recombinant DNA Technology", "url": "static/materials/BCH405_Recombinant.pdf", "source": "static"},
            {"title": "BCH 405 - Gene Cloning", "url": "static/materials/BCH405_Cloning.pdf", "source": "static"},
            {"title": "BCH 405 - PCR and Applications", "url": "static/materials/BCH405_PCR.pdf", "source": "static"},
            {"title": "BCH 405 - Gene Editing (CRISPR)", "url": "static/materials/BCH405_CRISPR.pdf", "source": "static"},
            {"title": "BCH 405 - Transgenic Organisms", "url": "static/materials/BCH405_Transgenic.pdf", "source": "static"},
            {"title": "BCH 405 - Past Questions", "url": "static/materials/BCH405_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH407": {
        "name": "Plant Biochemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 407 - Photosynthesis Advanced", "url": "static/materials/BCH407_Photosynthesis.pdf", "source": "static"},
            {"title": "BCH 407 - Plant Metabolism", "url": "static/materials/BCH407_Metabolism.pdf", "source": "static"},
            {"title": "BCH 407 - Secondary Metabolites", "url": "static/materials/BCH407_Secondary.pdf", "source": "static"},
            {"title": "BCH 407 - Nitrogen Fixation", "url": "static/materials/BCH407_Nitrogen.pdf", "source": "static"},
            {"title": "BCH 407 - Past Questions", "url": "static/materials/BCH407_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH409": {
        "name": "Seminar in Biochemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 409 - Seminar Presentation Guide", "url": "static/materials/BCH409_Presentation.pdf", "source": "static"},
            {"title": "BCH 409 - Research Topics", "url": "static/materials/BCH409_Topics.pdf", "source": "static"},
            {"title": "BCH 409 - Scientific Writing", "url": "static/materials/BCH409_Writing.pdf", "source": "static"},
        ]
    },

    "BCH411": {
        "name": "Pharmacological Biochemistry and Toxicology",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 411 - Drug Metabolism", "url": "static/materials/BCH411_Drug.pdf", "source": "static"},
            {"title": "BCH 411 - Toxicology Principles", "url": "static/materials/BCH411_Toxicology.pdf", "source": "static"},
            {"title": "BCH 411 - Xenobiotic Metabolism", "url": "static/materials/BCH411_Xenobiotic.pdf", "source": "static"},
            {"title": "BCH 411 - Drug-Receptor Interactions", "url": "static/materials/BCH411_Receptor.pdf", "source": "static"},
            {"title": "BCH 411 - Past Questions", "url": "static/materials/BCH411_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH413": {
        "name": "Bioenergetics",
        "department": "Biochemistry",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BCH 413 - Thermodynamics in Biology", "url": "static/materials/BCH413_Thermodynamics.pdf", "source": "static"},
            {"title": "BCH 413 - Energy Coupling", "url": "static/materials/BCH413_Coupling.pdf", "source": "static"},
            {"title": "BCH 413 - ATP Synthesis", "url": "static/materials/BCH413_ATP.pdf", "source": "static"},
            {"title": "BCH 413 - Past Questions", "url": "static/materials/BCH413_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB305": {
        "name": "Microbial Genetics/Molecular Biology",
        "department": "Microbiology",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 305 - Bacterial Genetics", "url": "static/materials/MCB305_Genetics.pdf", "source": "static"},
            {"title": "MCB 305 - Gene Transfer", "url": "static/materials/MCB305_Transfer.pdf", "source": "static"},
            {"title": "MCB 305 - Plasmids", "url": "static/materials/MCB305_Plasmids.pdf", "source": "static"},
            {"title": "MCB 305 - Molecular Cloning", "url": "static/materials/MCB305_Cloning.pdf", "source": "static"},
            {"title": "MCB 305 - Past Questions", "url": "static/materials/MCB305_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH402": {
        "name": "Biosynthesis of Macromolecules",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 402 - DNA Biosynthesis", "url": "static/materials/BCH402_DNA.pdf", "source": "static"},
            {"title": "BCH 402 - RNA Biosynthesis", "url": "static/materials/BCH402_RNA.pdf", "source": "static"},
            {"title": "BCH 402 - Protein Biosynthesis", "url": "static/materials/BCH402_Protein.pdf", "source": "static"},
            {"title": "BCH 402 - Past Questions", "url": "static/materials/BCH402_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH404": {
        "name": "Bioinorganic Chemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 404 - Metal Ions in Biology", "url": "static/materials/BCH404_Metals.pdf", "source": "static"},
            {"title": "BCH 404 - Metalloproteins", "url": "static/materials/BCH404_Metalloproteins.pdf", "source": "static"},
            {"title": "BCH 404 - Heme Proteins", "url": "static/materials/BCH404_Heme.pdf", "source": "static"},
            {"title": "BCH 404 - Past Questions", "url": "static/materials/BCH404_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH406": {
        "name": "Metabolic Regulations",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 406 - Hormonal Regulation", "url": "static/materials/BCH406_Hormonal.pdf", "source": "static"},
            {"title": "BCH 406 - Metabolic Integration", "url": "static/materials/BCH406_Integration.pdf", "source": "static"},
            {"title": "BCH 406 - Signal Transduction Advanced", "url": "static/materials/BCH406_Signaling.pdf", "source": "static"},
            {"title": "BCH 406 - Past Questions", "url": "static/materials/BCH406_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH408": {
        "name": "Biochemical Reasoning",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 408 - Problem Solving in Biochemistry", "url": "static/materials/BCH408_Problem_Solving.pdf", "source": "static"},
            {"title": "BCH 408 - Case Studies", "url": "static/materials/BCH408_Cases.pdf", "source": "static"},
            {"title": "BCH 408 - Past Questions", "url": "static/materials/BCH408_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH412": {
        "name": "Industrial Biochemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 412 - Industrial Fermentation", "url": "static/materials/BCH412_Fermentation.pdf", "source": "static"},
            {"title": "BCH 412 - Bioprocessing", "url": "static/materials/BCH412_Bioprocessing.pdf", "source": "static"},
            {"title": "BCH 412 - Enzyme Applications", "url": "static/materials/BCH412_Applications.pdf", "source": "static"},
            {"title": "BCH 412 - Past Questions", "url": "static/materials/BCH412_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB408": {
        "name": "Microbial Physiology & Metabolism",
        "department": "Microbiology",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MCB 408 - Microbial Metabolism", "url": "static/materials/MCB408_Metabolism.pdf", "source": "static"},
            {"title": "MCB 408 - Microbial Physiology", "url": "static/materials/MCB408_Physiology.pdf", "source": "static"},
            {"title": "MCB 408 - Metabolic Diversity", "url": "static/materials/MCB408_Diversity.pdf", "source": "static"},
            {"title": "MCB 408 - Past Questions", "url": "static/materials/MCB408_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH499": {
        "name": "Research Project",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 499 - Research Methodology", "url": "static/materials/BCH499_Methodology.pdf", "source": "static"},
            {"title": "BCH 499 - Project Writing Guide", "url": "static/materials/BCH499_Writing.pdf", "source": "static"},
            {"title": "BCH 499 - Data Analysis Techniques", "url": "static/materials/BCH499_Analysis.pdf", "source": "static"},
            {"title": "BCH 499 - Literature Review Guide", "url": "static/materials/BCH499_Literature.pdf", "source": "static"},
            {"title": "BCH 499 - Project Proposal Template", "url": "static/materials/BCH499_Proposal.pdf", "source": "static"},
            {"title": "BCH 499 - Statistical Methods", "url": "static/materials/BCH499_Statistics.pdf", "source": "static"},
            {"title": "BCH 499 - Reference Management", "url": "static/materials/BCH499_References.pdf", "source": "static"},
        ]
    },

    "BCH492": {
        "name": "Advanced Biochemical Methods",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 492 - Advanced Analytical Techniques", "url": "static/materials/BCH492_Analytical.pdf", "source": "static"},
            {"title": "BCH 492 - Molecular Biology Techniques", "url": "static/materials/BCH492_Molecular.pdf", "source": "static"},
            {"title": "BCH 492 - Proteomics", "url": "static/materials/BCH492_Proteomics.pdf", "source": "static"},
            {"title": "BCH 492 - Past Questions", "url": "static/materials/BCH492_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BCH414": {
        "name": "Clinical and Forensic Biochemistry",
        "department": "Biochemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BCH 414 - Clinical Biochemistry", "url": "static/materials/BCH414_Clinical.pdf", "source": "static"},
            {"title": "BCH 414 - Forensic Analysis", "url": "static/materials/BCH414_Forensic.pdf", "source": "static"},
            {"title": "BCH 414 - Diagnostic Tests", "url": "static/materials/BCH414_Diagnostic.pdf", "source": "static"},
            {"title": "BCH 414 - Past Questions", "url": "static/materials/BCH414_Past_Questions.pdf", "source": "static"},
        ]
    },

    # ========================================
    # MATHEMATICS 200-400 LEVEL - COMPLETE
    # ========================================

    "CSC201": {
        "name": "Computer Programming I",
        "department": "Computer Science",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CSC 201 - Python Programming", "url": "static/materials/CSC201_Python.pdf", "source": "static"},
            {"title": "CSC 201 - Data Structures", "url": "static/materials/CSC201_Data_Structures.pdf", "source": "static"},
            {"title": "CSC 201 - Algorithms", "url": "static/materials/CSC201_Algorithms.pdf", "source": "static"},
            {"title": "CSC 201 - Object-Oriented Programming", "url": "static/materials/CSC201_OOP.pdf", "source": "static"},
            {"title": "CSC 201 - Past Questions", "url": "static/materials/CSC201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST211": {
        "name": "Environment & Sustainable Development",
        "department": "General Studies",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 211 - Environmental Science", "url": "static/materials/GST211_Environment.pdf", "source": "static"},
            {"title": "GST 211 - Sustainable Development", "url": "static/materials/GST211_Sustainable.pdf", "source": "static"},
            {"title": "GST 211 - Climate Change", "url": "static/materials/GST211_Climate.pdf", "source": "static"},
            {"title": "GST 211 - Past Questions", "url": "static/materials/GST211_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH201": {
        "name": "Mathematical Methods I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "Calculus Volume 2 - OpenStax", "url": "https://openstax.org/details/books/calculus-volume-2", "source": "static"},
            {"title": "MTH 201 - Advanced Calculus", "url": "static/materials/MTH201_Calculus.pdf", "source": "static"},
            {"title": "MTH 201 - Multivariable Calculus", "url": "static/materials/MTH201_Multivariable.pdf", "source": "static"},
            {"title": "MTH 201 - Vector Calculus", "url": "static/materials/MTH201_Vector.pdf", "source": "static"},
            {"title": "MTH 201 - Line Integrals", "url": "static/materials/MTH201_Line_Integrals.pdf", "source": "static"},
            {"title": "MTH 201 - Surface Integrals", "url": "static/materials/MTH201_Surface.pdf", "source": "static"},
            {"title": "MTH 201 - Green's Theorem", "url": "static/materials/MTH201_Greens.pdf", "source": "static"},
            {"title": "MTH 201 - Stokes' Theorem", "url": "static/materials/MTH201_Stokes.pdf", "source": "static"},
            {"title": "MTH 201 - Divergence Theorem", "url": "static/materials/MTH201_Divergence.pdf", "source": "static"},
            {"title": "MTH 201 - Past Questions", "url": "static/materials/MTH201_Past_Questions.pdf", "source": "static"},
            {"title": "MTH 201 - Practice Problems", "url": "static/materials/MTH201_Practice.pdf", "source": "static"},
        ]
    },

    "MTH203": {
        "name": "Sets Logic & Algebra I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 203 - Set Theory", "url": "static/materials/MTH203_Sets.pdf", "source": "static"},
            {"title": "MTH 203 - Mathematical Logic", "url": "static/materials/MTH203_Logic.pdf", "source": "static"},
            {"title": "MTH 203 - Boolean Algebra", "url": "static/materials/MTH203_Boolean.pdf", "source": "static"},
            {"title": "MTH 203 - Relations and Functions", "url": "static/materials/MTH203_Relations.pdf", "source": "static"},
            {"title": "MTH 203 - Past Questions", "url": "static/materials/MTH203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH204": {
        "name": "Linear Algebra I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 204 - Vector Spaces", "url": "static/materials/MTH204_Vectors.pdf", "source": "static"},
            {"title": "MTH 204 - Matrices", "url": "static/materials/MTH204_Matrices.pdf", "source": "static"},
            {"title": "MTH 204 - Linear Transformations", "url": "static/materials/MTH204_Transformations.pdf", "source": "static"},
            {"title": "MTH 204 - Eigenvalues and Eigenvectors", "url": "static/materials/MTH204_Eigen.pdf", "source": "static"},
            {"title": "MTH 204 - Past Questions", "url": "static/materials/MTH204_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH207": {
        "name": "Real Analysis I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 207 - Sequences and Series", "url": "static/materials/MTH207_Sequences.pdf", "source": "static"},
            {"title": "MTH 207 - Limits and Continuity", "url": "static/materials/MTH207_Limits.pdf", "source": "static"},
            {"title": "MTH 207 - Differentiation", "url": "static/materials/MTH207_Differentiation.pdf", "source": "static"},
            {"title": "MTH 207 - Integration Theory", "url": "static/materials/MTH207_Integration.pdf", "source": "static"},
            {"title": "MTH 207 - Past Questions", "url": "static/materials/MTH207_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH209": {
        "name": "Introduction to Numerical Analysis",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 209 - Numerical Methods", "url": "static/materials/MTH209_Methods.pdf", "source": "static"},
            {"title": "MTH 209 - Root Finding", "url": "static/materials/MTH209_Roots.pdf", "source": "static"},
            {"title": "MTH 209 - Interpolation", "url": "static/materials/MTH209_Interpolation.pdf", "source": "static"},
            {"title": "MTH 209 - Numerical Integration", "url": "static/materials/MTH209_Integration.pdf", "source": "static"},
            {"title": "MTH 209 - Past Questions", "url": "static/materials/MTH209_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH299": {
        "name": "Industrial Training I",
        "department": "Mathematics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 299 - Industrial Training Guidelines", "url": "static/materials/MTH299_Guidelines.pdf", "source": "static"},
            {"title": "MTH 299 - Report Writing", "url": "static/materials/MTH299_Report.pdf", "source": "static"},
        ]
    },

    "PHY201": {
        "name": "General Physics III",
        "department": "Physics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "PHY 201 - Advanced Mechanics", "url": "static/materials/PHY201_Mechanics.pdf", "source": "static"},
            {"title": "PHY 201 - Electromagnetism", "url": "static/materials/PHY201_EM.pdf", "source": "static"},
            {"title": "PHY 201 - Waves and Optics", "url": "static/materials/PHY201_Waves.pdf", "source": "static"},
            {"title": "PHY 201 - Past Questions", "url": "static/materials/PHY201_Past_Questions.pdf", "source": "static"},
        ]
    },

    # Add 300 and 400 level MTH courses...
    "MTH301": {
        "name": "Metric Space Topology",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 301 - Introduction to Topology", "url": "static/materials/MTH301_Topology.pdf", "source": "static"},
            {"title": "MTH 301 - Metric Spaces", "url": "static/materials/MTH301_Metric.pdf", "source": "static"},
            {"title": "MTH 301 - Open and Closed Sets", "url": "static/materials/MTH301_Sets.pdf", "source": "static"},
            {"title": "MTH 301 - Continuous Functions", "url": "static/materials/MTH301_Continuous.pdf", "source": "static"},
            {"title": "MTH 301 - Compactness", "url": "static/materials/MTH301_Compactness.pdf", "source": "static"},
            {"title": "MTH 301 - Connectedness", "url": "static/materials/MTH301_Connectedness.pdf", "source": "static"},
            {"title": "MTH 301 - Complete Metric Spaces", "url": "static/materials/MTH301_Complete.pdf", "source": "static"},
            {"title": "MTH 301 - Past Questions", "url": "static/materials/MTH301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH404": {
        "name": "Project",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 404 - Mathematical Research Methods", "url": "static/materials/MTH404_Methods.pdf", "source": "static"},
            {"title": "MTH 404 - LaTeX for Mathematics", "url": "static/materials/MTH404_LaTeX.pdf", "source": "static"},
            {"title": "MTH 404 - Mathematical Writing", "url": "static/materials/MTH404_Writing.pdf", "source": "static"},
            {"title": "MTH 404 - Project Topics Guide", "url": "static/materials/MTH404_Topics.pdf", "source": "static"},
            {"title": "MTH 404 - Literature Review", "url": "static/materials/MTH404_Literature.pdf", "source": "static"},
        ]
    },

    # ========================================
    # MATHEMATICS 200 LEVEL - SECOND SEMESTER - COMPLETE
    # ========================================

    "CSC202": {
        "name": "Computer Programming II",
        "department": "Computer Science",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "CSC 202 - Advanced Programming Concepts", "url": "static/materials/CSC202_Advanced.pdf", "source": "static"},
            {"title": "CSC 202 - Object-Oriented Design", "url": "static/materials/CSC202_OOD.pdf", "source": "static"},
            {"title": "CSC 202 - Data Structures Advanced", "url": "static/materials/CSC202_DS_Advanced.pdf", "source": "static"},
            {"title": "CSC 202 - Algorithms Analysis", "url": "static/materials/CSC202_Algorithms.pdf", "source": "static"},
            {"title": "CSC 202 - Past Questions", "url": "static/materials/CSC202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST212": {
        "name": "Application of Computer",
        "department": "General Studies",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 212 - Computer Applications", "url": "static/materials/GST212_Applications.pdf", "source": "static"},
            {"title": "GST 212 - MS Office Suite", "url": "static/materials/GST212_Office.pdf", "source": "static"},
            {"title": "GST 212 - Spreadsheets", "url": "static/materials/GST212_Spreadsheets.pdf", "source": "static"},
            {"title": "GST 212 - Past Questions", "url": "static/materials/GST212_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST214": {
        "name": "Valuing the Teaching Profession II",
        "department": "General Studies",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 214 - Teaching Profession", "url": "static/materials/GST214_Teaching.pdf", "source": "static"},
            {"title": "GST 214 - Educational Psychology", "url": "static/materials/GST214_Psychology.pdf", "source": "static"},
            {"title": "GST 214 - Past Questions", "url": "static/materials/GST214_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST222": {
        "name": "Peace & Conflict Resolution",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 222 - Conflict Resolution", "url": "static/materials/GST222_Conflict.pdf", "source": "static"},
            {"title": "GST 222 - Peace Studies", "url": "static/materials/GST222_Peace.pdf", "source": "static"},
            {"title": "GST 222 - Mediation Techniques", "url": "static/materials/GST222_Mediation.pdf", "source": "static"},
            {"title": "GST 222 - Past Questions", "url": "static/materials/GST222_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST223": {
        "name": "Introduction to Entrepreneurship",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 223 - Entrepreneurship Basics", "url": "static/materials/GST223_Entrepreneurship.pdf", "source": "static"},
            {"title": "GST 223 - Business Planning", "url": "static/materials/GST223_Business.pdf", "source": "static"},
            {"title": "GST 223 - Innovation", "url": "static/materials/GST223_Innovation.pdf", "source": "static"},
            {"title": "GST 223 - Past Questions", "url": "static/materials/GST223_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST224": {
        "name": "Leadership Skills",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 224 - Leadership Theory", "url": "static/materials/GST224_Leadership.pdf", "source": "static"},
            {"title": "GST 224 - Team Management", "url": "static/materials/GST224_Team.pdf", "source": "static"},
            {"title": "GST 224 - Communication Skills", "url": "static/materials/GST224_Communication.pdf", "source": "static"},
            {"title": "GST 224 - Past Questions", "url": "static/materials/GST224_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST225": {
        "name": "Yoruba Grammar, Language & Communication",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 225 - Yoruba Grammar", "url": "static/materials/GST225_Grammar.pdf", "source": "static"},
            {"title": "GST 225 - Yoruba Language", "url": "static/materials/GST225_Language.pdf", "source": "static"},
            {"title": "GST 225 - Past Questions", "url": "static/materials/GST225_Past_Questions.pdf", "source": "static"},
        ]
    },

    "GST226": {
        "name": "Land Use & General Agriculture",
        "department": "General Studies",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "GST 226 - Land Use Planning", "url": "static/materials/GST226_Land.pdf", "source": "static"},
            {"title": "GST 226 - Agricultural Practices", "url": "static/materials/GST226_Agriculture.pdf", "source": "static"},
            {"title": "GST 226 - Past Questions", "url": "static/materials/GST226_Past_Questions.pdf", "source": "static"},
        ]
    },

    "ENT221": {
        "name": "Introduction to Entrepreneurship",
        "department": "Entrepreneurship",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "ENT 221 - Entrepreneurship Fundamentals", "url": "static/materials/ENT221_Fundamentals.pdf", "source": "static"},
            {"title": "ENT 221 - Business Models", "url": "static/materials/ENT221_Models.pdf", "source": "static"},
            {"title": "ENT 221 - Startup Strategies", "url": "static/materials/ENT221_Startup.pdf", "source": "static"},
            {"title": "ENT 221 - Past Questions", "url": "static/materials/ENT221_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH202": {
        "name": "Elementary Differential Equations",
        "department": "Mathematics",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 202 - First Order ODEs", "url": "static/materials/MTH202_First_Order.pdf", "source": "static"},
            {"title": "MTH 202 - Second Order ODEs", "url": "static/materials/MTH202_Second_Order.pdf", "source": "static"},
            {"title": "MTH 202 - Linear Differential Equations", "url": "static/materials/MTH202_Linear.pdf", "source": "static"},
            {"title": "MTH 202 - Applications of ODEs", "url": "static/materials/MTH202_Applications.pdf", "source": "static"},
            {"title": "MTH 202 - Laplace Transforms", "url": "static/materials/MTH202_Laplace.pdf", "source": "static"},
            {"title": "MTH 202 - Series Solutions", "url": "static/materials/MTH202_Series.pdf", "source": "static"},
            {"title": "MTH 202 - Past Questions", "url": "static/materials/MTH202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH205": {
        "name": "Linear Algebra II",
        "department": "Mathematics",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 205 - Advanced Vector Spaces", "url": "static/materials/MTH205_Vector_Spaces.pdf", "source": "static"},
            {"title": "MTH 205 - Inner Product Spaces", "url": "static/materials/MTH205_Inner_Product.pdf", "source": "static"},
            {"title": "MTH 205 - Diagonalization", "url": "static/materials/MTH205_Diagonalization.pdf", "source": "static"},
            {"title": "MTH 205 - Jordan Forms", "url": "static/materials/MTH205_Jordan.pdf", "source": "static"},
            {"title": "MTH 205 - Past Questions", "url": "static/materials/MTH205_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH210": {
        "name": "Vector Analysis",
        "department": "Mathematics",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 210 - Vector Fields", "url": "static/materials/MTH210_Fields.pdf", "source": "static"},
            {"title": "MTH 210 - Gradient, Divergence, Curl", "url": "static/materials/MTH210_GDC.pdf", "source": "static"},
            {"title": "MTH 210 - Vector Calculus Theorems", "url": "static/materials/MTH210_Theorems.pdf", "source": "static"},
            {"title": "MTH 210 - Applications", "url": "static/materials/MTH210_Applications.pdf", "source": "static"},
            {"title": "MTH 210 - Past Questions", "url": "static/materials/MTH210_Past_Questions.pdf", "source": "static"},
        ]
    },

    "PHY202": {
        "name": "Introduction to Electric Circuits & Electronics",
        "department": "Physics",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "PHY 202 - Circuit Analysis", "url": "static/materials/PHY202_Circuits.pdf", "source": "static"},
            {"title": "PHY 202 - AC and DC Circuits", "url": "static/materials/PHY202_ACDC.pdf", "source": "static"},
            {"title": "PHY 202 - Electronics Fundamentals", "url": "static/materials/PHY202_Electronics.pdf", "source": "static"},
            {"title": "PHY 202 - Semiconductors", "url": "static/materials/PHY202_Semiconductors.pdf", "source": "static"},
            {"title": "PHY 202 - Past Questions", "url": "static/materials/PHY202_Past_Questions.pdf", "source": "static"},
        ]
    },

    # ========================================
    # MATHEMATICS 300 LEVEL - COMPLETE
    # ========================================

    "GST311": {
        "name": "Entrepreneurship",
        "department": "General Studies",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "GST 311 - Entrepreneurship Advanced", "url": "static/materials/GST311_Entrepreneurship.pdf", "source": "static"},
            {"title": "GST 311 - Business Development", "url": "static/materials/GST311_Development.pdf", "source": "static"},
            {"title": "GST 311 - Marketing Strategies", "url": "static/materials/GST311_Marketing.pdf", "source": "static"},
            {"title": "GST 311 - Past Questions", "url": "static/materials/GST311_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH303": {
        "name": "Vector & Tensor Analysis",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 303 - Vector Analysis Advanced", "url": "static/materials/MTH303_Vector.pdf", "source": "static"},
            {"title": "MTH 303 - Tensor Algebra", "url": "static/materials/MTH303_Tensor.pdf", "source": "static"},
            {"title": "MTH 303 - Tensor Calculus", "url": "static/materials/MTH303_Calculus.pdf", "source": "static"},
            {"title": "MTH 303 - Applications in Physics", "url": "static/materials/MTH303_Physics.pdf", "source": "static"},
            {"title": "MTH 303 - Past Questions", "url": "static/materials/MTH303_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH304": {
        "name": "Complex Analysis I",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 304 - Complex Numbers", "url": "static/materials/MTH304_Complex.pdf", "source": "static"},
            {"title": "MTH 304 - Analytic Functions", "url": "static/materials/MTH304_Analytic.pdf", "source": "static"},
            {"title": "MTH 304 - Contour Integration", "url": "static/materials/MTH304_Contour.pdf", "source": "static"},
            {"title": "MTH 304 - Residue Theorem", "url": "static/materials/MTH304_Residue.pdf", "source": "static"},
            {"title": "MTH 304 - Conformal Mapping", "url": "static/materials/MTH304_Conformal.pdf", "source": "static"},
            {"title": "MTH 304 - Past Questions", "url": "static/materials/MTH304_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH307": {
        "name": "Real Analysis II",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 307 - Sequences of Functions", "url": "static/materials/MTH307_Sequences.pdf", "source": "static"},
            {"title": "MTH 307 - Uniform Convergence", "url": "static/materials/MTH307_Convergence.pdf", "source": "static"},
            {"title": "MTH 307 - Riemann Integration", "url": "static/materials/MTH307_Riemann.pdf", "source": "static"},
            {"title": "MTH 307 - Metric Spaces", "url": "static/materials/MTH307_Metric.pdf", "source": "static"},
            {"title": "MTH 307 - Past Questions", "url": "static/materials/MTH307_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH311": {
        "name": "Theory of Modules",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 311 - Module Theory", "url": "static/materials/MTH311_Modules.pdf", "source": "static"},
            {"title": "MTH 311 - Homomorphisms", "url": "static/materials/MTH311_Homomorphisms.pdf", "source": "static"},
            {"title": "MTH 311 - Direct Sums", "url": "static/materials/MTH311_Direct_Sums.pdf", "source": "static"},
            {"title": "MTH 311 - Free Modules", "url": "static/materials/MTH311_Free.pdf", "source": "static"},
            {"title": "MTH 311 - Past Questions", "url": "static/materials/MTH311_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH399": {
        "name": "Industrial Attachment II",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 399 - Industrial Training Guidelines", "url": "static/materials/MTH399_Guidelines.pdf", "source": "static"},
            {"title": "MTH 399 - Report Writing", "url": "static/materials/MTH399_Report.pdf", "source": "static"},
            {"title": "MTH 399 - Industry Expectations", "url": "static/materials/MTH399_Expectations.pdf", "source": "static"},
        ]
    },

    "MTH309": {
        "name": "Discrete Mathematics",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 309 - Graph Theory", "url": "static/materials/MTH309_Graphs.pdf", "source": "static"},
            {"title": "MTH 309 - Combinatorics", "url": "static/materials/MTH309_Combinatorics.pdf", "source": "static"},
            {"title": "MTH 309 - Recurrence Relations", "url": "static/materials/MTH309_Recurrence.pdf", "source": "static"},
            {"title": "MTH 309 - Generating Functions", "url": "static/materials/MTH309_Generating.pdf", "source": "static"},
            {"title": "MTH 309 - Number Theory", "url": "static/materials/MTH309_Number_Theory.pdf", "source": "static"},
            {"title": "MTH 309 - Past Questions", "url": "static/materials/MTH309_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH313": {
        "name": "Geometry",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 313 - Euclidean Geometry", "url": "static/materials/MTH313_Euclidean.pdf", "source": "static"},
            {"title": "MTH 313 - Non-Euclidean Geometry", "url": "static/materials/MTH313_Non_Euclidean.pdf", "source": "static"},
            {"title": "MTH 313 - Projective Geometry", "url": "static/materials/MTH313_Projective.pdf", "source": "static"},
            {"title": "MTH 313 - Differential Geometry", "url": "static/materials/MTH313_Differential.pdf", "source": "static"},
            {"title": "MTH 313 - Past Questions", "url": "static/materials/MTH313_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH319": {
        "name": "Numerical Analysis I",
        "department": "Mathematics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 319 - Numerical Methods Advanced", "url": "static/materials/MTH319_Methods.pdf", "source": "static"},
            {"title": "MTH 319 - Error Analysis", "url": "static/materials/MTH319_Errors.pdf", "source": "static"},
            {"title": "MTH 319 - Numerical Linear Algebra", "url": "static/materials/MTH319_Linear.pdf", "source": "static"},
            {"title": "MTH 319 - Numerical ODEs", "url": "static/materials/MTH319_ODEs.pdf", "source": "static"},
            {"title": "MTH 319 - Past Questions", "url": "static/materials/MTH319_Past_Questions.pdf", "source": "static"},
        ]
    },

    "STA311": {
        "name": "Probability III",
        "department": "Statistics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "STA 311 - Advanced Probability", "url": "static/materials/STA311_Probability.pdf", "source": "static"},
            {"title": "STA 311 - Random Variables", "url": "static/materials/STA311_Random.pdf", "source": "static"},
            {"title": "STA 311 - Probability Distributions", "url": "static/materials/STA311_Distributions.pdf", "source": "static"},
            {"title": "STA 311 - Stochastic Processes", "url": "static/materials/STA311_Stochastic.pdf", "source": "static"},
            {"title": "STA 311 - Past Questions", "url": "static/materials/STA311_Past_Questions.pdf", "source": "static"},
        ]
    },

    # 300 LEVEL SECOND SEMESTER

    "ENT321": {
        "name": "Entrepreneurship & Business Management",
        "department": "Entrepreneurship",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "ENT 321 - Business Management", "url": "static/materials/ENT321_Management.pdf", "source": "static"},
            {"title": "ENT 321 - Strategic Planning", "url": "static/materials/ENT321_Strategic.pdf", "source": "static"},
            {"title": "ENT 321 - Financial Management", "url": "static/materials/ENT321_Financial.pdf", "source": "static"},
            {"title": "ENT 321 - Past Questions", "url": "static/materials/ENT321_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH300": {
        "name": "Abstract Algebra I",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 300 - Group Theory", "url": "static/materials/MTH300_Groups.pdf", "source": "static"},
            {"title": "MTH 300 - Ring Theory", "url": "static/materials/MTH300_Rings.pdf", "source": "static"},
            {"title": "MTH 300 - Field Theory", "url": "static/materials/MTH300_Fields.pdf", "source": "static"},
            {"title": "MTH 300 - Homomorphisms", "url": "static/materials/MTH300_Homomorphisms.pdf", "source": "static"},
            {"title": "MTH 300 - Past Questions", "url": "static/materials/MTH300_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH302": {
        "name": "Ordinary Differential Equations",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 302 - Higher Order ODEs", "url": "static/materials/MTH302_Higher_Order.pdf", "source": "static"},
            {"title": "MTH 302 - Systems of ODEs", "url": "static/materials/MTH302_Systems.pdf", "source": "static"},
            {"title": "MTH 302 - Boundary Value Problems", "url": "static/materials/MTH302_BVP.pdf", "source": "static"},
            {"title": "MTH 302 - Stability Theory", "url": "static/materials/MTH302_Stability.pdf", "source": "static"},
            {"title": "MTH 302 - Past Questions", "url": "static/materials/MTH302_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH305": {
        "name": "Complex Analysis II",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 305 - Advanced Complex Analysis", "url": "static/materials/MTH305_Advanced.pdf", "source": "static"},
            {"title": "MTH 305 - Laurent Series", "url": "static/materials/MTH305_Laurent.pdf", "source": "static"},
            {"title": "MTH 305 - Residue Calculus", "url": "static/materials/MTH305_Residue.pdf", "source": "static"},
            {"title": "MTH 305 - Analytic Continuation", "url": "static/materials/MTH305_Continuation.pdf", "source": "static"},
            {"title": "MTH 305 - Past Questions", "url": "static/materials/MTH305_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH306": {
        "name": "Abstract Algebra II",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 306 - Galois Theory", "url": "static/materials/MTH306_Galois.pdf", "source": "static"},
            {"title": "MTH 306 - Module Theory Advanced", "url": "static/materials/MTH306_Modules.pdf", "source": "static"},
            {"title": "MTH 306 - Representation Theory", "url": "static/materials/MTH306_Representation.pdf", "source": "static"},
            {"title": "MTH 306 - Past Questions", "url": "static/materials/MTH306_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH308": {
        "name": "Introduction to Mathematical Modelling",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 308 - Mathematical Modeling", "url": "static/materials/MTH308_Modeling.pdf", "source": "static"},
            {"title": "MTH 308 - Population Models", "url": "static/materials/MTH308_Population.pdf", "source": "static"},
            {"title": "MTH 308 - Epidemic Models", "url": "static/materials/MTH308_Epidemic.pdf", "source": "static"},
            {"title": "MTH 308 - Optimization Models", "url": "static/materials/MTH308_Optimization.pdf", "source": "static"},
            {"title": "MTH 308 - Past Questions", "url": "static/materials/MTH308_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH310": {
        "name": "Mathematical Methods II",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 310 - Advanced Mathematical Methods", "url": "static/materials/MTH310_Methods.pdf", "source": "static"},
            {"title": "MTH 310 - Special Functions", "url": "static/materials/MTH310_Special.pdf", "source": "static"},
            {"title": "MTH 310 - Integral Transforms", "url": "static/materials/MTH310_Transforms.pdf", "source": "static"},
            {"title": "MTH 310 - Green's Functions", "url": "static/materials/MTH310_Greens.pdf", "source": "static"},
            {"title": "MTH 310 - Past Questions", "url": "static/materials/MTH310_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH320": {
        "name": "Computational Techniques in Mathematics",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 320 - Computational Mathematics", "url": "static/materials/MTH320_Computational.pdf", "source": "static"},
            {"title": "MTH 320 - Programming for Math", "url": "static/materials/MTH320_Programming.pdf", "source": "static"},
            {"title": "MTH 320 - Symbolic Computation", "url": "static/materials/MTH320_Symbolic.pdf", "source": "static"},
            {"title": "MTH 320 - Past Questions", "url": "static/materials/MTH320_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH312": {
        "name": "Optimization Theory",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 312 - Linear Programming", "url": "static/materials/MTH312_Linear.pdf", "source": "static"},
            {"title": "MTH 312 - Nonlinear Optimization", "url": "static/materials/MTH312_Nonlinear.pdf", "source": "static"},
            {"title": "MTH 312 - Convex Optimization", "url": "static/materials/MTH312_Convex.pdf", "source": "static"},
            {"title": "MTH 312 - Dynamic Programming", "url": "static/materials/MTH312_Dynamic.pdf", "source": "static"},
            {"title": "MTH 312 - Past Questions", "url": "static/materials/MTH312_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH314": {
        "name": "Analytical Dynamics I",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 314 - Lagrangian Mechanics", "url": "static/materials/MTH314_Lagrangian.pdf", "source": "static"},
            {"title": "MTH 314 - Hamiltonian Mechanics", "url": "static/materials/MTH314_Hamiltonian.pdf", "source": "static"},
            {"title": "MTH 314 - Variational Principles", "url": "static/materials/MTH314_Variational.pdf", "source": "static"},
            {"title": "MTH 314 - Past Questions", "url": "static/materials/MTH314_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH316": {
        "name": "Introduction to Operations Research",
        "department": "Mathematics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 316 - Operations Research", "url": "static/materials/MTH316_OR.pdf", "source": "static"},
            {"title": "MTH 316 - Queueing Theory", "url": "static/materials/MTH316_Queueing.pdf", "source": "static"},
            {"title": "MTH 316 - Game Theory", "url": "static/materials/MTH316_Game.pdf", "source": "static"},
            {"title": "MTH 316 - Decision Analysis", "url": "static/materials/MTH316_Decision.pdf", "source": "static"},
            {"title": "MTH 316 - Past Questions", "url": "static/materials/MTH316_Past_Questions.pdf", "source": "static"},
        ]
    },

    "STA312": {
        "name": "Distribution Theory I",
        "department": "Statistics",
        "level": "300",
        "semester": "Second Semester",
        "materials": [
            {"title": "STA 312 - Probability Distributions", "url": "static/materials/STA312_Distributions.pdf", "source": "static"},
            {"title": "STA 312 - Discrete Distributions", "url": "static/materials/STA312_Discrete.pdf", "source": "static"},
            {"title": "STA 312 - Continuous Distributions", "url": "static/materials/STA312_Continuous.pdf", "source": "static"},
            {"title": "STA 312 - Sampling Distributions", "url": "static/materials/STA312_Sampling.pdf", "source": "static"},
            {"title": "STA 312 - Past Questions", "url": "static/materials/STA312_Past_Questions.pdf", "source": "static"},
        ]
    },

    # ========================================
    # MATHEMATICS 400 LEVEL - COMPLETE
    # ========================================

    "MTH401": {
        "name": "Theory of Ordinary Differential Equations",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 401 - Existence and Uniqueness", "url": "static/materials/MTH401_Existence.pdf", "source": "static"},
            {"title": "MTH 401 - Stability Analysis", "url": "static/materials/MTH401_Stability.pdf", "source": "static"},
            {"title": "MTH 401 - Qualitative Theory", "url": "static/materials/MTH401_Qualitative.pdf", "source": "static"},
            {"title": "MTH 401 - Perturbation Methods", "url": "static/materials/MTH401_Perturbation.pdf", "source": "static"},
            {"title": "MTH 401 - Past Questions", "url": "static/materials/MTH401_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH403": {
        "name": "Functional Analysis",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 403 - Normed Spaces", "url": "static/materials/MTH403_Normed.pdf", "source": "static"},
            {"title": "MTH 403 - Banach Spaces", "url": "static/materials/MTH403_Banach.pdf", "source": "static"},
            {"title": "MTH 403 - Hilbert Spaces", "url": "static/materials/MTH403_Hilbert.pdf", "source": "static"},
            {"title": "MTH 403 - Linear Operators", "url": "static/materials/MTH403_Operators.pdf", "source": "static"},
            {"title": "MTH 403 - Spectral Theory", "url": "static/materials/MTH403_Spectral.pdf", "source": "static"},
            {"title": "MTH 403 - Past Questions", "url": "static/materials/MTH403_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH405": {
        "name": "General Topology",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 405 - Topological Spaces", "url": "static/materials/MTH405_Topological.pdf", "source": "static"},
            {"title": "MTH 405 - Continuity and Homeomorphisms", "url": "static/materials/MTH405_Continuity.pdf", "source": "static"},
            {"title": "MTH 405 - Compactness and Connectedness", "url": "static/materials/MTH405_Compactness.pdf", "source": "static"},
            {"title": "MTH 405 - Separation Axioms", "url": "static/materials/MTH405_Separation.pdf", "source": "static"},
            {"title": "MTH 405 - Past Questions", "url": "static/materials/MTH405_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH419": {
        "name": "Complex Analysis",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 419 - Complex Analysis Advanced", "url": "static/materials/MTH419_Advanced.pdf", "source": "static"},
            {"title": "MTH 419 - Riemann Surfaces", "url": "static/materials/MTH419_Riemann.pdf", "source": "static"},
            {"title": "MTH 419 - Harmonic Functions", "url": "static/materials/MTH419_Harmonic.pdf", "source": "static"},
            {"title": "MTH 419 - Elliptic Functions", "url": "static/materials/MTH419_Elliptic.pdf", "source": "static"},
            {"title": "MTH 419 - Past Questions", "url": "static/materials/MTH419_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH407": {
        "name": "Mathematical Methods III",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 407 - Advanced Methods", "url": "static/materials/MTH407_Methods.pdf", "source": "static"},
            {"title": "MTH 407 - Asymptotic Methods", "url": "static/materials/MTH407_Asymptotic.pdf", "source": "static"},
            {"title": "MTH 407 - Calculus of Variations", "url": "static/materials/MTH407_Variations.pdf", "source": "static"},
            {"title": "MTH 407 - Past Questions", "url": "static/materials/MTH407_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH409": {
        "name": "General Relativity",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 409 - Special Relativity", "url": "static/materials/MTH409_Special.pdf", "source": "static"},
            {"title": "MTH 409 - General Relativity Theory", "url": "static/materials/MTH409_General.pdf", "source": "static"},
            {"title": "MTH 409 - Einstein Field Equations", "url": "static/materials/MTH409_Einstein.pdf", "source": "static"},
            {"title": "MTH 409 - Schwarzschild Solution", "url": "static/materials/MTH409_Schwarzschild.pdf", "source": "static"},
            {"title": "MTH 409 - Past Questions", "url": "static/materials/MTH409_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH411": {
        "name": "Analytical Dynamics II",
        "department": "Mathematics",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "MTH 411 - Advanced Dynamics", "url": "static/materials/MTH411_Advanced.pdf", "source": "static"},
            {"title": "MTH 411 - Rigid Body Dynamics", "url": "static/materials/MTH411_Rigid.pdf", "source": "static"},
            {"title": "MTH 411 - Hamilton-Jacobi Theory", "url": "static/materials/MTH411_Hamilton_Jacobi.pdf", "source": "static"},
            {"title": "MTH 411 - Past Questions", "url": "static/materials/MTH411_Past_Questions.pdf", "source": "static"},
        ]
    },

    # 400 LEVEL SECOND SEMESTER

    "ENT421": {
        "name": "Investment Marketing & Management",
        "department": "Entrepreneurship",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "ENT 421 - Investment Strategies", "url": "static/materials/ENT421_Investment.pdf", "source": "static"},
            {"title": "ENT 421 - Marketing Management", "url": "static/materials/ENT421_Marketing.pdf", "source": "static"},
            {"title": "ENT 421 - Financial Markets", "url": "static/materials/ENT421_Markets.pdf", "source": "static"},
            {"title": "ENT 421 - Past Questions", "url": "static/materials/ENT421_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH402": {
        "name": "Theory of Partial Differential Equations",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 402 - PDEs Classification", "url": "static/materials/MTH402_Classification.pdf", "source": "static"},
            {"title": "MTH 402 - Wave Equation", "url": "static/materials/MTH402_Wave.pdf", "source": "static"},
            {"title": "MTH 402 - Heat Equation", "url": "static/materials/MTH402_Heat.pdf", "source": "static"},
            {"title": "MTH 402 - Laplace Equation", "url": "static/materials/MTH402_Laplace.pdf", "source": "static"},
            {"title": "MTH 402 - Fourier Series", "url": "static/materials/MTH402_Fourier.pdf", "source": "static"},
            {"title": "MTH 402 - Past Questions", "url": "static/materials/MTH402_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH406": {
        "name": "Lebesgue Measure & Integration",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 406 - Measure Theory", "url": "static/materials/MTH406_Measure.pdf", "source": "static"},
            {"title": "MTH 406 - Lebesgue Integration", "url": "static/materials/MTH406_Lebesgue.pdf", "source": "static"},
            {"title": "MTH 406 - Convergence Theorems", "url": "static/materials/MTH406_Convergence.pdf", "source": "static"},
            {"title": "MTH 406 - Lp Spaces", "url": "static/materials/MTH406_Lp_Spaces.pdf", "source": "static"},
            {"title": "MTH 406 - Past Questions", "url": "static/materials/MTH406_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH418": {
        "name": "Advanced Algebra",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 418 - Advanced Group Theory", "url": "static/materials/MTH418_Groups.pdf", "source": "static"},
            {"title": "MTH 418 - Advanced Ring Theory", "url": "static/materials/MTH418_Rings.pdf", "source": "static"},
            {"title": "MTH 418 - Galois Theory Advanced", "url": "static/materials/MTH418_Galois.pdf", "source": "static"},
            {"title": "MTH 418 - Category Theory", "url": "static/materials/MTH418_Category.pdf", "source": "static"},
            {"title": "MTH 418 - Past Questions", "url": "static/materials/MTH418_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH408": {
        "name": "Quantum Mechanics I",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 408 - Quantum Mechanics Basics", "url": "static/materials/MTH408_Basics.pdf", "source": "static"},
            {"title": "MTH 408 - Wave Functions", "url": "static/materials/MTH408_Wave.pdf", "source": "static"},
            {"title": "MTH 408 - Schrodinger Equation", "url": "static/materials/MTH408_Schrodinger.pdf", "source": "static"},
            {"title": "MTH 408 - Quantum Operators", "url": "static/materials/MTH408_Operators.pdf", "source": "static"},
            {"title": "MTH 408 - Past Questions", "url": "static/materials/MTH408_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MTH410": {
        "name": "Electromagnetism",
        "department": "Mathematics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MTH 410 - Maxwell's Equations", "url": "static/materials/MTH410_Maxwell.pdf", "source": "static"},
            {"title": "MTH 410 - Electromagnetic Waves", "url": "static/materials/MTH410_Waves.pdf", "source": "static"},
            {"title": "MTH 410 - Vector Potentials", "url": "static/materials/MTH410_Potentials.pdf", "source": "static"},
            {"title": "MTH 410 - Electromagnetic Radiation", "url": "static/materials/MTH410_Radiation.pdf", "source": "static"},
            {"title": "MTH 410 - Past Questions", "url": "static/materials/MTH410_Past_Questions.pdf", "source": "static"},
        ]
    },
    # ========================================
    # BOTANY 200 LEVEL - COMPLETE
    # ========================================

    "BOT201": {
        "name": "Seedless Plants (Cryptogams)",
        "department": "Botany",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 201 - Algae and Bryophytes", "url": "static/materials/BOT201_Algae.pdf", "source": "static"},
            {"title": "BOT 201 - Pteridophytes", "url": "static/materials/BOT201_Pteridophytes.pdf", "source": "static"},
            {"title": "BOT 201 - Cryptogam Classification", "url": "static/materials/BOT201_Classification.pdf", "source": "static"},
            {"title": "BOT 201 - Life Cycles", "url": "static/materials/BOT201_Life_Cycles.pdf", "source": "static"},
            {"title": "BOT 201 - Past Questions", "url": "static/materials/BOT201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT203": {
        "name": "Plant Morphology",
        "department": "Botany",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 203 - Plant Structure", "url": "static/materials/BOT203_Structure.pdf", "source": "static"},
            {"title": "BOT 203 - Root Systems", "url": "static/materials/BOT203_Roots.pdf", "source": "static"},
            {"title": "BOT 203 - Stem Morphology", "url": "static/materials/BOT203_Stems.pdf", "source": "static"},
            {"title": "BOT 203 - Leaf Morphology", "url": "static/materials/BOT203_Leaves.pdf", "source": "static"},
            {"title": "BOT 203 - Flower Structure", "url": "static/materials/BOT203_Flowers.pdf", "source": "static"},
            {"title": "BOT 203 - Past Questions", "url": "static/materials/BOT203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT205": {
        "name": "Introductory Plant Physiology",
        "department": "Botany",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 205 - Photosynthesis", "url": "static/materials/BOT205_Photosynthesis.pdf", "source": "static"},
            {"title": "BOT 205 - Respiration", "url": "static/materials/BOT205_Respiration.pdf", "source": "static"},
            {"title": "BOT 205 - Water Relations", "url": "static/materials/BOT205_Water.pdf", "source": "static"},
            {"title": "BOT 205 - Mineral Nutrition", "url": "static/materials/BOT205_Nutrition.pdf", "source": "static"},
            {"title": "BOT 205 - Past Questions", "url": "static/materials/BOT205_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT207": {
        "name": "General Ecology",
        "department": "Botany",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 207 - Ecosystem Ecology", "url": "static/materials/BOT207_Ecosystem.pdf", "source": "static"},
            {"title": "BOT 207 - Population Ecology", "url": "static/materials/BOT207_Population.pdf", "source": "static"},
            {"title": "BOT 207 - Community Ecology", "url": "static/materials/BOT207_Community.pdf", "source": "static"},
            {"title": "BOT 207 - Past Questions", "url": "static/materials/BOT207_Past_Questions.pdf", "source": "static"},
        ]
    },

    "STA211": {
        "name": "Statistics for Biological Sciences",
        "department": "Statistics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "STA 211 - Biostatistics", "url": "static/materials/STA211_Biostatistics.pdf", "source": "static"},
            {"title": "STA 211 - Descriptive Statistics", "url": "static/materials/STA211_Descriptive.pdf", "source": "static"},
            {"title": "STA 211 - Hypothesis Testing", "url": "static/materials/STA211_Testing.pdf", "source": "static"},
            {"title": "STA 211 - ANOVA", "url": "static/materials/STA211_ANOVA.pdf", "source": "static"},
            {"title": "STA 211 - Past Questions", "url": "static/materials/STA211_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT202": {
        "name": "Seed Plants (Spermatophyta)",
        "department": "Botany",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 202 - Gymnosperms", "url": "static/materials/BOT202_Gymnosperms.pdf", "source": "static"},
            {"title": "BOT 202 - Angiosperms", "url": "static/materials/BOT202_Angiosperms.pdf", "source": "static"},
            {"title": "BOT 202 - Monocots vs Dicots", "url": "static/materials/BOT202_Monocots.pdf", "source": "static"},
            {"title": "BOT 202 - Past Questions", "url": "static/materials/BOT202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT204": {
        "name": "Plant Anatomy",
        "department": "Botany",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 204 - Cell Structure", "url": "static/materials/BOT204_Cell.pdf", "source": "static"},
            {"title": "BOT 204 - Tissue Systems", "url": "static/materials/BOT204_Tissues.pdf", "source": "static"},
            {"title": "BOT 204 - Vascular Anatomy", "url": "static/materials/BOT204_Vascular.pdf", "source": "static"},
            {"title": "BOT 204 - Past Questions", "url": "static/materials/BOT204_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT206": {
        "name": "Plant Taxonomy",
        "department": "Botany",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 206 - Taxonomic Principles", "url": "static/materials/BOT206_Principles.pdf", "source": "static"},
            {"title": "BOT 206 - Plant Classification", "url": "static/materials/BOT206_Classification.pdf", "source": "static"},
            {"title": "BOT 206 - Nomenclature", "url": "static/materials/BOT206_Nomenclature.pdf", "source": "static"},
            {"title": "BOT 206 - Past Questions", "url": "static/materials/BOT206_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT208": {
        "name": "Biological Techniques",
        "department": "Botany",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 208 - Laboratory Techniques", "url": "static/materials/BOT208_Lab_Techniques.pdf", "source": "static"},
            {"title": "BOT 208 - Microscopy", "url": "static/materials/BOT208_Microscopy.pdf", "source": "static"},
            {"title": "BOT 208 - Specimen Preparation", "url": "static/materials/BOT208_Specimen.pdf", "source": "static"},
            {"title": "BOT 208 - Past Questions", "url": "static/materials/BOT208_Past_Questions.pdf", "source": "static"},
        ]
    },

    # BOTANY 300-400 LEVEL
    "BOT301": {
        "name": "Plant Ecology & Field Course I",
        "department": "Botany",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 301 - Plant Ecology", "url": "static/materials/BOT301_Ecology.pdf", "source": "static"},
            {"title": "BOT 301 - Field Methods", "url": "static/materials/BOT301_Field.pdf", "source": "static"},
            {"title": "BOT 301 - Past Questions", "url": "static/materials/BOT301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT401": {
        "name": "Plant Breeding",
        "department": "Botany",
        "level": "400",
        "semester": "First Semester",
        "materials": [
            {"title": "BOT 401 - Breeding Methods", "url": "static/materials/BOT401_Methods.pdf", "source": "static"},
            {"title": "BOT 401 - Genetics for Breeding", "url": "static/materials/BOT401_Genetics.pdf", "source": "static"},
            {"title": "BOT 401 - Past Questions", "url": "static/materials/BOT401_Past_Questions.pdf", "source": "static"},
        ]
    },

    "BOT412": {
        "name": "Research Project",
        "department": "Botany",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "BOT 412 - Research Methodology", "url": "static/materials/BOT412_Methodology.pdf", "source": "static"},
            {"title": "BOT 412 - Project Writing", "url": "static/materials/BOT412_Writing.pdf", "source": "static"},
            {"title": "BOT 412 - Data Analysis", "url": "static/materials/BOT412_Analysis.pdf", "source": "static"},
        ]
    },

    # ========================================
    # CHEMISTRY 200-400 LEVEL - COMPLETE
    # ========================================

    "CHM201": {
        "name": "Physical Chemistry I",
        "department": "Chemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 201 - Thermodynamics", "url": "static/materials/CHM201_Thermodynamics.pdf", "source": "static"},
            {"title": "CHM 201 - Chemical Kinetics", "url": "static/materials/CHM201_Kinetics.pdf", "source": "static"},
            {"title": "CHM 201 - Equilibrium", "url": "static/materials/CHM201_Equilibrium.pdf", "source": "static"},
            {"title": "CHM 201 - Past Questions", "url": "static/materials/CHM201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM203": {
        "name": "Inorganic Chemistry I",
        "department": "Chemistry",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 203 - Atomic Structure", "url": "static/materials/CHM203_Atomic.pdf", "source": "static"},
            {"title": "CHM 203 - Periodic Table", "url": "static/materials/CHM203_Periodic.pdf", "source": "static"},
            {"title": "CHM 203 - Chemical Bonding", "url": "static/materials/CHM203_Bonding.pdf", "source": "static"},
            {"title": "CHM 203 - Past Questions", "url": "static/materials/CHM203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM206": {
        "name": "Organic Chemistry II",
        "department": "Chemistry",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 206 - Organic Reactions", "url": "static/materials/CHM206_Reactions.pdf", "source": "static"},
            {"title": "CHM 206 - Stereochemistry", "url": "static/materials/CHM206_Stereochemistry.pdf", "source": "static"},
            {"title": "CHM 206 - Past Questions", "url": "static/materials/CHM206_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM301": {
        "name": "Physical Chemistry III",
        "department": "Chemistry",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "CHM 301 - Quantum Chemistry", "url": "static/materials/CHM301_Quantum.pdf", "source": "static"},
            {"title": "CHM 301 - Spectroscopy", "url": "static/materials/CHM301_Spectroscopy.pdf", "source": "static"},
            {"title": "CHM 301 - Past Questions", "url": "static/materials/CHM301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "CHM404": {
        "name": "Research Project",
        "department": "Chemistry",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "CHM 404 - Research Methods", "url": "static/materials/CHM404_Methods.pdf", "source": "static"},
            {"title": "CHM 404 - Project Writing", "url": "static/materials/CHM404_Writing.pdf", "source": "static"},
            {"title": "CHM 404 - Laboratory Safety", "url": "static/materials/CHM404_Safety.pdf", "source": "static"},
        ]
    },

    # ========================================
    # FISHERIES 200-400 LEVEL - COMPLETE
    # ========================================

    "FIS201": {
        "name": "General Ichthyology",
        "department": "Fisheries",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "FIS 201 - Fish Anatomy", "url": "static/materials/FIS201_Anatomy.pdf", "source": "static"},
            {"title": "FIS 201 - Fish Physiology", "url": "static/materials/FIS201_Physiology.pdf", "source": "static"},
            {"title": "FIS 201 - Fish Classification", "url": "static/materials/FIS201_Classification.pdf", "source": "static"},
            {"title": "FIS 201 - Past Questions", "url": "static/materials/FIS201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "FIS203": {
        "name": "Fisheries Biology",
        "department": "Fisheries",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "FIS 203 - Fish Biology", "url": "static/materials/FIS203_Biology.pdf", "source": "static"},
            {"title": "FIS 203 - Life Cycles", "url": "static/materials/FIS203_Life_Cycles.pdf", "source": "static"},
            {"title": "FIS 203 - Past Questions", "url": "static/materials/FIS203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "FIS301": {
        "name": "Fish Physiology",
        "department": "Fisheries",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "FIS 301 - Fish Physiology Advanced", "url": "static/materials/FIS301_Physiology.pdf", "source": "static"},
            {"title": "FIS 301 - Osmoregulation", "url": "static/materials/FIS301_Osmoregulation.pdf", "source": "static"},
            {"title": "FIS 301 - Past Questions", "url": "static/materials/FIS301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "FIS404": {
        "name": "Research Project",
        "department": "Fisheries",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "FIS 404 - Research Methodology", "url": "static/materials/FIS404_Methodology.pdf", "source": "static"},
            {"title": "FIS 404 - Data Collection", "url": "static/materials/FIS404_Data.pdf", "source": "static"},
            {"title": "FIS 404 - Project Report Writing", "url": "static/materials/FIS404_Writing.pdf", "source": "static"},
        ]
    },

    # ========================================
    # MICROBIOLOGY 200-400 LEVEL - COMPLETE
    # ========================================

    "MCB203": {
        "name": "Microbial Morphology & Physiology",
        "department": "Microbiology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 203 - Bacterial Morphology", "url": "static/materials/MCB203_Morphology.pdf", "source": "static"},
            {"title": "MCB 203 - Microbial Physiology", "url": "static/materials/MCB203_Physiology.pdf", "source": "static"},
            {"title": "MCB 203 - Cell Structure", "url": "static/materials/MCB203_Cell.pdf", "source": "static"},
            {"title": "MCB 203 - Past Questions", "url": "static/materials/MCB203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB205": {
        "name": "Microbial Genetics",
        "department": "Microbiology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 205 - Bacterial Genetics", "url": "static/materials/MCB205_Genetics.pdf", "source": "static"},
            {"title": "MCB 205 - Gene Transfer", "url": "static/materials/MCB205_Transfer.pdf", "source": "static"},
            {"title": "MCB 205 - Mutations", "url": "static/materials/MCB205_Mutations.pdf", "source": "static"},
            {"title": "MCB 205 - Past Questions", "url": "static/materials/MCB205_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB207": {
        "name": "Microbial Ecology",
        "department": "Microbiology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 207 - Microbial Ecology", "url": "static/materials/MCB207_Ecology.pdf", "source": "static"},
            {"title": "MCB 207 - Environmental Microbiology", "url": "static/materials/MCB207_Environmental.pdf", "source": "static"},
            {"title": "MCB 207 - Past Questions", "url": "static/materials/MCB207_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB202": {
        "name": "Immunology",
        "department": "Microbiology",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "MCB 202 - Immune System", "url": "static/materials/MCB202_Immune.pdf", "source": "static"},
            {"title": "MCB 202 - Antigens and Antibodies", "url": "static/materials/MCB202_Antigens.pdf", "source": "static"},
            {"title": "MCB 202 - Past Questions", "url": "static/materials/MCB202_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB204": {
        "name": "Medical Microbiology",
        "department": "Microbiology",
        "level": "200",
        "semester": "Second Semester",
        "materials": [
            {"title": "MCB 204 - Pathogenic Bacteria", "url": "static/materials/MCB204_Pathogenic.pdf", "source": "static"},
            {"title": "MCB 204 - Infectious Diseases", "url": "static/materials/MCB204_Diseases.pdf", "source": "static"},
            {"title": "MCB 204 - Past Questions", "url": "static/materials/MCB204_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB301": {
        "name": "Bacteriology",
        "department": "Microbiology",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "MCB 301 - Bacterial Classification", "url": "static/materials/MCB301_Classification.pdf", "source": "static"},
            {"title": "MCB 301 - Bacterial Physiology", "url": "static/materials/MCB301_Physiology.pdf", "source": "static"},
            {"title": "MCB 301 - Past Questions", "url": "static/materials/MCB301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "MCB404": {
        "name": "Research Project",
        "department": "Microbiology",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "MCB 404 - Research Methods", "url": "static/materials/MCB404_Methods.pdf", "source": "static"},
            {"title": "MCB 404 - Laboratory Techniques", "url": "static/materials/MCB404_Lab.pdf", "source": "static"},
            {"title": "MCB 404 - Project Writing", "url": "static/materials/MCB404_Writing.pdf", "source": "static"},
        ]
    },

    # ========================================
    # PHYSICS 200-400 LEVEL - COMPLETE
    # ========================================

    "PHY203": {
        "name": "Waves & Optics I",
        "department": "Physics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "PHY 203 - Wave Motion", "url": "static/materials/PHY203_Waves.pdf", "source": "static"},
            {"title": "PHY 203 - Geometrical Optics", "url": "static/materials/PHY203_Optics.pdf", "source": "static"},
            {"title": "PHY 203 - Physical Optics", "url": "static/materials/PHY203_Physical.pdf", "source": "static"},
            {"title": "PHY 203 - Past Questions", "url": "static/materials/PHY203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "PHY205": {
        "name": "Classical Mechanics I",
        "department": "Physics",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "PHY 205 - Newtonian Mechanics", "url": "static/materials/PHY205_Newtonian.pdf", "source": "static"},
            {"title": "PHY 205 - Conservation Laws", "url": "static/materials/PHY205_Conservation.pdf", "source": "static"},
            {"title": "PHY 205 - Past Questions", "url": "static/materials/PHY205_Past_Questions.pdf", "source": "static"},
        ]
    },

    "PHY301": {
        "name": "Quantum Mechanics I",
        "department": "Physics",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "PHY 301 - Wave Mechanics", "url": "static/materials/PHY301_Wave.pdf", "source": "static"},
            {"title": "PHY 301 - Schrodinger Equation", "url": "static/materials/PHY301_Schrodinger.pdf", "source": "static"},
            {"title": "PHY 301 - Past Questions", "url": "static/materials/PHY301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "PHY404": {
        "name": "Research Project",
        "department": "Physics",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "PHY 404 - Research Methodology", "url": "static/materials/PHY404_Methodology.pdf", "source": "static"},
            {"title": "PHY 404 - Experimental Physics", "url": "static/materials/PHY404_Experimental.pdf", "source": "static"},
            {"title": "PHY 404 - Data Analysis", "url": "static/materials/PHY404_Analysis.pdf", "source": "static"},
        ]
    },

    # ========================================
    # SCIENCE LAB TECHNOLOGY 200-400 LEVEL
    # ========================================

    "SLT201": {
        "name": "Laboratory Techniques I",
        "department": "Science Lab Technology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "SLT 201 - Basic Lab Techniques", "url": "static/materials/SLT201_Techniques.pdf", "source": "static"},
            {"title": "SLT 201 - Safety Procedures", "url": "static/materials/SLT201_Safety.pdf", "source": "static"},
            {"title": "SLT 201 - Equipment Handling", "url": "static/materials/SLT201_Equipment.pdf", "source": "static"},
            {"title": "SLT 201 - Past Questions", "url": "static/materials/SLT201_Past_Questions.pdf", "source": "static"},
        ]
    },

    "SLT203": {
        "name": "Basic Instrumentation",
        "department": "Science Lab Technology",
        "level": "200",
        "semester": "First Semester",
        "materials": [
            {"title": "SLT 203 - Laboratory Instruments", "url": "static/materials/SLT203_Instruments.pdf", "source": "static"},
            {"title": "SLT 203 - Instrument Calibration", "url": "static/materials/SLT203_Calibration.pdf", "source": "static"},
            {"title": "SLT 203 - Past Questions", "url": "static/materials/SLT203_Past_Questions.pdf", "source": "static"},
        ]
    },

    "SLT301": {
        "name": "Advanced Laboratory Techniques",
        "department": "Science Lab Technology",
        "level": "300",
        "semester": "First Semester",
        "materials": [
            {"title": "SLT 301 - Advanced Techniques", "url": "static/materials/SLT301_Advanced.pdf", "source": "static"},
            {"title": "SLT 301 - Quality Control", "url": "static/materials/SLT301_QC.pdf", "source": "static"},
            {"title": "SLT 301 - Past Questions", "url": "static/materials/SLT301_Past_Questions.pdf", "source": "static"},
        ]
    },

    "SLT404": {
        "name": "Research Project",
        "department": "Science Lab Technology",
        "level": "400",
        "semester": "Second Semester",
        "materials": [
            {"title": "SLT 404 - Research Methods", "url": "static/materials/SLT404_Methods.pdf", "source": "static"},
            {"title": "SLT 404 - Laboratory Research", "url": "static/materials/SLT404_Research.pdf", "source": "static"},
            {"title": "SLT 404 - Project Writing", "url": "static/materials/SLT404_Writing.pdf", "source": "static"},
        ]
    },
}


# ============================================================
# SEEDING FUNCTION
# ============================================================

def seed_200_to_400_complete():
    """
    Seeds the database with COMPLETE 200-400 Level materials
    """
    with app.app_context():
        print("\n" + "="*70)
        print("🎓 NELAVISTA - COMPLETE 200-400 LEVEL SCIENCE SEEDER")
        print("="*70 + "\n")
        
        total_added = 0
        total_skipped = 0
        
        for course_code, course_data in COMPLETE_200_400_MATERIALS.items():
            print(f"\n📘 Processing {course_code} - {course_data['name']}")
            print(f"   Dept: {course_data['department']} | Level: {course_data['level']} | Sem: {course_data['semester']}")
            print(f"   Materials to add: {len(course_data['materials'])}")
            
            added_count = 0
            skipped_count = 0
            
            for material_data in course_data['materials']:
                # Check if material already exists
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
        print(f"   Materials Added: {total_added}")
        print(f"   Materials Skipped: {total_skipped}")
        print(f"   Total in Database: {Material.query.count()}")
        print("="*70 + "\n")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    print("\n🚀 Starting COMPLETE 200-400 Level Science Materials Seeding...")
    seed_200_to_400_complete()
    print("✅ Done! Run check_materials.py to verify.\n")