# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Comprehensive curricula data with simplified structure
CURRICULA_DATA = {
    "nigeria": {
        "name": "Nigerian Curriculum",
        "subjects": [
            {"id": 1, "name": "Mathematics", "description": "Number work, Algebra, Geometry", "icon": "fa-calculator"},
            {"id": 2, "name": "English Studies", "description": "Grammar, Composition, Literature", "icon": "fa-language"},
            {"id": 3, "name": "Basic Science", "description": "Physics, Chemistry, Biology fundamentals", "icon": "fa-flask"},
            {"id": 4, "name": "Social Studies", "description": "Civic Education, History, Geography", "icon": "fa-landmark"},
            {"id": 5, "name": "Physics", "description": "Mechanics, Thermodynamics, Waves", "icon": "fa-atom"},
            {"id": 6, "name": "Chemistry", "description": "Organic, Inorganic, Physical Chemistry", "icon": "fa-vial"},
            {"id": 7, "name": "Biology", "description": "Living organisms, Genetics, Ecology", "icon": "fa-dna"},
            {"id": 8, "name": "Further Mathematics", "description": "Advanced Mathematics topics", "icon": "fa-square-root-alt"},
            {"id": 9, "name": "Economics", "description": "Microeconomics, Macroeconomics", "icon": "fa-chart-line"},
            {"id": 10, "name": "Geography", "description": "Physical and Human Geography", "icon": "fa-globe"}
        ]
    },
    "cambridge": {
        "name": "Cambridge International",
        "subjects": [
            {"id": 1, "name": "Mathematics", "description": "Pure Mathematics, Statistics", "icon": "fa-calculator"},
            {"id": 2, "name": "English Language", "description": "Reading, Writing, Speaking", "icon": "fa-language"},
            {"id": 3, "name": "Combined Science", "description": "Biology, Chemistry, Physics", "icon": "fa-flask"},
            {"id": 4, "name": "Physics", "description": "Forces, Energy, Waves, Electricity", "icon": "fa-atom"},
            {"id": 5, "name": "Chemistry", "description": "Elements, Reactions, Organic Chemistry", "icon": "fa-vial"},
            {"id": 6, "name": "Biology", "description": "Cells, Organisms, Ecology", "icon": "fa-dna"},
            {"id": 7, "name": "Additional Mathematics", "description": "Advanced mathematical concepts", "icon": "fa-square-root-alt"},
            {"id": 8, "name": "Computer Science", "description": "Programming, Algorithms", "icon": "fa-laptop-code"},
            {"id": 9, "name": "Geography", "description": "Physical and Human Geography", "icon": "fa-mountain"},
            {"id": 10, "name": "Economics", "description": "Market systems, International trade", "icon": "fa-chart-line"}
        ]
    },
    "american": {
        "name": "American Curriculum",
        "subjects": [
            {"id": 1, "name": "Mathematics", "description": "Algebra, Geometry, Calculus", "icon": "fa-calculator"},
            {"id": 2, "name": "English Language Arts", "description": "Reading, Writing, Literature", "icon": "fa-language"},
            {"id": 3, "name": "Science", "description": "Physical, Life, Earth Sciences", "icon": "fa-flask"},
            {"id": 4, "name": "Social Studies", "description": "History, Geography, Civics", "icon": "fa-landmark"},
            {"id": 5, "name": "Physics", "description": "AP Physics, Modern Physics", "icon": "fa-atom"},
            {"id": 6, "name": "Chemistry", "description": "AP Chemistry, Organic Chemistry", "icon": "fa-vial"},
            {"id": 7, "name": "Biology", "description": "AP Biology, Anatomy & Physiology", "icon": "fa-dna"},
            {"id": 8, "name": "Calculus", "description": "AP Calculus AB/BC", "icon": "fa-square-root-alt"},
            {"id": 9, "name": "Computer Science", "description": "AP Computer Science", "icon": "fa-laptop-code"},
            {"id": 10, "name": "US History", "description": "American History and Government", "icon": "fa-flag-usa"}
        ]
    },
    "ib": {
        "name": "International Baccalaureate",
        "subjects": [
            {"id": 1, "name": "Mathematics", "description": "Analysis, Applications, Interpretation", "icon": "fa-calculator"},
            {"id": 2, "name": "English A", "description": "Language and Literature", "icon": "fa-language"},
            {"id": 3, "name": "Sciences", "description": "Biology, Chemistry, Physics, ESS", "icon": "fa-flask"},
            {"id": 4, "name": "Individuals & Societies", "description": "History, Economics, Geography", "icon": "fa-globe"},
            {"id": 5, "name": "Physics", "description": "HL and SL Physics", "icon": "fa-atom"},
            {"id": 6, "name": "Chemistry", "description": "HL and SL Chemistry", "icon": "fa-vial"},
            {"id": 7, "name": "Biology", "description": "HL and SL Biology", "icon": "fa-dna"},
            {"id": 8, "name": "Computer Science", "description": "Programming and algorithms", "icon": "fa-laptop-code"},
            {"id": 9, "name": "Economics", "description": "Global economics", "icon": "fa-chart-line"},
            {"id": 10, "name": "Business Management", "description": "International business", "icon": "fa-briefcase"}
        ]
    }
}

# Comprehensive topics for each subject with grade-level appropriateness
TOPICS_DATA = {
    # Mathematics topics
    "Mathematics": [
        # Elementary School Topics (Grades 1-5)
        {"id": "number-theory", "name": "Number Theory", "icon": "fa-hashtag", "levels": ["elementary"]},
        {"id": "basic-arithmetic", "name": "Basic Arithmetic", "icon": "fa-calculator", "levels": ["elementary"]},
        {"id": "fractions", "name": "Fractions", "icon": "fa-divide", "levels": ["elementary"]},
        {"id": "measurement", "name": "Measurement", "icon": "fa-ruler", "levels": ["elementary"]},
        {"id": "time-money", "name": "Time & Money", "icon": "fa-clock", "levels": ["elementary"]},
        {"id": "basic-geometry", "name": "Basic Geometry", "icon": "fa-shapes", "levels": ["elementary"]},
        
        # Middle School Topics (Grades 6-8)
        {"id": "algebra-basics", "name": "Algebra Basics", "icon": "fa-superscript", "levels": ["middle"]},
        {"id": "linear-equations", "name": "Linear Equations", "icon": "fa-equals", "levels": ["middle"]},
        {"id": "geometry", "name": "Geometry", "icon": "fa-shapes", "levels": ["middle"]},
        {"id": "basic-statistics", "name": "Basic Statistics", "icon": "fa-chart-bar", "levels": ["middle"]},
        {"id": "probability", "name": "Probability", "icon": "fa-dice", "levels": ["middle"]},
        {"id": "ratio-proportion", "name": "Ratio & Proportion", "icon": "fa-percentage", "levels": ["middle"]},
        
        # High School Topics (Grades 9-12)
        {"id": "advanced-algebra", "name": "Advanced Algebra", "icon": "fa-superscript", "levels": ["high"]},
        {"id": "quadratic-equations", "name": "Quadratic Equations", "icon": "fa-project-diagram", "levels": ["high"]},
        {"id": "trigonometry", "name": "Trigonometry", "icon": "fa-calculator", "levels": ["high"]},
        {"id": "calculus", "name": "Calculus", "icon": "fa-infinity", "levels": ["high"]},
        {"id": "statistics", "name": "Statistics", "icon": "fa-chart-bar", "levels": ["high"]},
        {"id": "functions", "name": "Functions", "icon": "fa-project-diagram", "levels": ["high"]},
        {"id": "vectors", "name": "Vectors", "icon": "fa-arrow-right", "levels": ["high"]},
        {"id": "matrices", "name": "Matrices", "icon": "fa-table", "levels": ["high"]},
        {"id": "complex-numbers", "name": "Complex Numbers", "icon": "fa-square-root-alt", "levels": ["high"]}
    ],
    
    # Physics topics
    "Physics": [
        # Elementary School Topics
        {"id": "forces-motion", "name": "Forces & Motion", "icon": "fa-running", "levels": ["elementary"]},
        {"id": "simple-machines", "name": "Simple Machines", "icon": "fa-cogs", "levels": ["elementary"]},
        {"id": "energy-basics", "name": "Energy Basics", "icon": "fa-bolt", "levels": ["elementary"]},
        {"id": "magnetism", "name": "Magnetism", "icon": "fa-magnet", "levels": ["elementary"]},
        {"id": "sound-basics", "name": "Sound Basics", "icon": "fa-volume-up", "levels": ["elementary"]},
        {"id": "light-basics", "name": "Light Basics", "icon": "fa-lightbulb", "levels": ["elementary"]},
        
        # Middle School Topics
        {"id": "mechanics", "name": "Mechanics", "icon": "fa-cogs", "levels": ["middle"]},
        {"id": "kinematics", "name": "Kinematics", "icon": "fa-running", "levels": ["middle"]},
        {"id": "energy-work", "name": "Energy & Work", "icon": "fa-bolt", "levels": ["middle"]},
        {"id": "waves", "name": "Waves", "icon": "fa-wave-square", "levels": ["middle"]},
        {"id": "electricity", "name": "Electricity", "icon": "fa-bolt", "levels": ["middle"]},
        {"id": "optics", "name": "Optics", "icon": "fa-lightbulb", "levels": ["middle"]},
        
        # High School Topics
        {"id": "thermodynamics", "name": "Thermodynamics", "icon": "fa-temperature-high", "levels": ["high"]},
        {"id": "electromagnetism", "name": "Electromagnetism", "icon": "fa-bolt", "levels": ["high"]},
        {"id": "modern-physics", "name": "Modern Physics", "icon": "fa-atom", "levels": ["high"]},
        {"id": "quantum-mechanics", "name": "Quantum Mechanics", "icon": "fa-atom", "levels": ["high"]},
        {"id": "nuclear-physics", "name": "Nuclear Physics", "icon": "fa-radiation", "levels": ["high"]},
        {"id": "astrophysics", "name": "Astrophysics", "icon": "fa-star", "levels": ["high"]}
    ],
    
    # Chemistry topics
    "Chemistry": [
        # Elementary School Topics
        {"id": "matter", "name": "Matter", "icon": "fa-atom", "levels": ["elementary"]},
        {"id": "elements", "name": "Elements", "icon": "fa-table", "levels": ["elementary"]},
        {"id": "simple-reactions", "name": "Simple Reactions", "icon": "fa-vial", "levels": ["elementary"]},
        {"id": "states-of-matter", "name": "States of Matter", "icon": "fa-temperature-low", "levels": ["elementary"]},
        {"id": "mixtures", "name": "Mixtures", "icon": "fa-flask", "levels": ["elementary"]},
        {"id": "solutions", "name": "Solutions", "icon": "fa-tint", "levels": ["elementary"]},
        
        # Middle School Topics
        {"id": "atomic-structure", "name": "Atomic Structure", "icon": "fa-atom", "levels": ["middle"]},
        {"id": "periodic-table", "name": "Periodic Table", "icon": "fa-table", "levels": ["middle"]},
        {"id": "chemical-bonding", "name": "Chemical Bonding", "icon": "fa-link", "levels": ["middle"]},
        {"id": "acids-bases", "name": "Acids & Bases", "icon": "fa-vial", "levels": ["middle"]},
        {"id": "chemical-reactions", "name": "Chemical Reactions", "icon": "fa-vial", "levels": ["middle"]},
        {"id": "stoichiometry", "name": "Stoichiometry", "icon": "fa-balance-scale", "levels": ["middle"]},
        
        # High School Topics
        {"id": "organic-chemistry", "name": "Organic Chemistry", "icon": "fa-atom", "levels": ["high"]},
        {"id": "inorganic-chemistry", "name": "Inorganic Chemistry", "icon": "fa-vial", "levels": ["high"]},
        {"id": "physical-chemistry", "name": "Physical Chemistry", "icon": "fa-flask", "levels": ["high"]},
        {"id": "electrochemistry", "name": "Electrochemistry", "icon": "fa-bolt", "levels": ["high"]},
        {"id": "thermochemistry", "name": "Thermochemistry", "icon": "fa-temperature-high", "levels": ["high"]},
        {"id": "chemical-kinetics", "name": "Chemical Kinetics", "icon": "fa-clock", "levels": ["high"]}
    ],
    
    # Biology topics
    "Biology": [
        # Elementary School Topics
        {"id": "plants-animals", "name": "Plants & Animals", "icon": "fa-leaf", "levels": ["elementary"]},
        {"id": "human-body", "name": "Human Body", "icon": "fa-heart", "levels": ["elementary"]},
        {"id": "ecosystems", "name": "Ecosystems", "icon": "fa-tree", "levels": ["elementary"]},
        {"id": "life-cycles", "name": "Life Cycles", "icon": "fa-recycle", "levels": ["elementary"]},
        {"id": "food-chains", "name": "Food Chains", "icon": "fa-link", "levels": ["elementary"]},
        {"id": "habitats", "name": "Habitats", "icon": "fa-home", "levels": ["elementary"]},
        
        # Middle School Topics
        {"id": "cell-biology", "name": "Cell Biology", "icon": "fa-microscope", "levels": ["middle"]},
        {"id": "genetics", "name": "Genetics", "icon": "fa-dna", "levels": ["middle"]},
        {"id": "evolution", "name": "Evolution", "icon": "fa-dna", "levels": ["middle"]},
        {"id": "ecology", "name": "Ecology", "icon": "fa-leaf", "levels": ["middle"]},
        {"id": "anatomy", "name": "Anatomy", "icon": "fa-heart", "levels": ["middle"]},
        {"id": "physiology", "name": "Physiology", "icon": "fa-lungs", "levels": ["middle"]},
        
        # High School Topics
        {"id": "molecular-biology", "name": "Molecular Biology", "icon": "fa-dna", "levels": ["high"]},
        {"id": "biochemistry", "name": "Biochemistry", "icon": "fa-flask", "levels": ["high"]},
        {"id": "microbiology", "name": "Microbiology", "icon": "fa-bacteria", "levels": ["high"]},
        {"id": "immunology", "name": "Immunology", "icon": "fa-shield-virus", "levels": ["high"]},
        {"id": "neuroscience", "name": "Neuroscience", "icon": "fa-brain", "levels": ["high"]},
        {"id": "biotechnology", "name": "Biotechnology", "icon": "fa-dna", "levels": ["high"]}
    ],
    
    # English Language topics
    "English Studies": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen", "levels": ["elementary", "middle", "high"]},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book", "levels": ["elementary", "middle", "high"]},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader", "levels": ["elementary", "middle", "high"]},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit", "levels": ["elementary", "middle", "high"]},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt", "levels": ["middle", "high"]},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather", "levels": ["middle", "high"]},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt", "levels": ["middle", "high"]},
        {"id": "prose", "name": "Prose", "icon": "fa-book", "levels": ["middle", "high"]},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks", "levels": ["middle", "high"]},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right", "levels": ["high"]}
    ],
    
    "English Language": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen", "levels": ["elementary", "middle", "high"]},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book", "levels": ["elementary", "middle", "high"]},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader", "levels": ["elementary", "middle", "high"]},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit", "levels": ["elementary", "middle", "high"]},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt", "levels": ["middle", "high"]},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone", "levels": ["middle", "high"]},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones", "levels": ["middle", "high"]},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right", "levels": ["high"]},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search", "levels": ["high"]},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract", "levels": ["middle", "high"]}
    ],
    
    "English Language Arts": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen", "levels": ["elementary", "middle", "high"]},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book", "levels": ["elementary", "middle", "high"]},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader", "levels": ["elementary", "middle", "high"]},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit", "levels": ["elementary", "middle", "high"]},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt", "levels": ["middle", "high"]},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather", "levels": ["middle", "high"]},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt", "levels": ["middle", "high"]},
        {"id": "prose", "name": "Prose", "icon": "fa-book", "levels": ["middle", "high"]},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks", "levels": ["middle", "high"]},
        {"id": "literary-analysis", "name": "Literary Analysis", "icon": "fa-search", "levels": ["high"]}
    ],
    
    "English A": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen", "levels": ["elementary", "middle", "high"]},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book", "levels": ["elementary", "middle", "high"]},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader", "levels": ["elementary", "middle", "high"]},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit", "levels": ["elementary", "middle", "high"]},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt", "levels": ["middle", "high"]},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather", "levels": ["middle", "high"]},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt", "levels": ["middle", "high"]},
        {"id": "prose", "name": "Prose", "icon": "fa-book", "levels": ["middle", "high"]},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks", "levels": ["middle", "high"]},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search", "levels": ["high"]}
    ]
}

# Add topics for other subjects
for subject in ["Basic Science", "Combined Science", "Science", "Sciences"]:
    TOPICS_DATA[subject] = [
        {"id": "scientific-method", "name": "Scientific Method", "icon": "fa-flask", "levels": ["elementary", "middle", "high"]},
        {"id": "matter", "name": "Matter", "icon": "fa-atom", "levels": ["elementary", "middle"]},
        {"id": "energy", "name": "Energy", "icon": "fa-bolt", "levels": ["elementary", "middle", "high"]},
        {"id": "forces-motion", "name": "Forces & Motion", "icon": "fa-running", "levels": ["elementary", "middle"]},
        {"id": "electricity-magnetism", "name": "Electricity & Magnetism", "icon": "fa-bolt", "levels": ["middle", "high"]},
        {"id": "waves-sound", "name": "Waves & Sound", "icon": "fa-wave-square", "levels": ["middle", "high"]},
        {"id": "light-optics", "name": "Light & Optics", "icon": "fa-lightbulb", "levels": ["middle", "high"]},
        {"id": "earth-science", "name": "Earth Science", "icon": "fa-globe", "levels": ["elementary", "middle"]},
        {"id": "weather-climate", "name": "Weather & Climate", "icon": "fa-cloud", "levels": ["elementary", "middle"]},
        {"id": "human-body", "name": "Human Body", "icon": "fa-heart", "levels": ["elementary", "middle"]}
    ]

for subject in ["Social Studies", "Global Perspectives", "Individuals & Societies"]:
    TOPICS_DATA[subject] = [
        {"id": "civics", "name": "Civics", "icon": "fa-landmark", "levels": ["elementary", "middle", "high"]},
        {"id": "history", "name": "History", "icon": "fa-monument", "levels": ["elementary", "middle", "high"]},
        {"id": "geography", "name": "Geography", "icon": "fa-globe", "levels": ["elementary", "middle", "high"]},
        {"id": "economics", "name": "Economics", "icon": "fa-chart-line", "levels": ["middle", "high"]},
        {"id": "culture", "name": "Culture", "icon": "fa-globe-americas", "levels": ["elementary", "middle", "high"]},
        {"id": "government", "name": "Government", "icon": "fa-university", "levels": ["middle", "high"]},
        {"id": "citizenship", "name": "Citizenship", "icon": "fa-user-friends", "levels": ["elementary", "middle"]},
        {"id": "human-rights", "name": "Human Rights", "icon": "fa-handshake", "levels": ["middle", "high"]},
        {"id": "global-issues", "name": "Global Issues", "icon": "fa-globe", "levels": ["middle", "high"]},
        {"id": "sustainable-development", "name": "Sustainable Development", "icon": "fa-leaf", "levels": ["middle", "high"]}
    ]

# Add topics for other subjects
for subject in ["Further Mathematics", "Additional Mathematics", "Calculus"]:
    TOPICS_DATA[subject] = [
        {"id": "advanced-algebra", "name": "Advanced Algebra", "icon": "fa-superscript", "levels": ["high"]},
        {"id": "calculus", "name": "Calculus", "icon": "fa-infinity", "levels": ["high"]},
        {"id": "vectors", "name": "Vectors", "icon": "fa-arrow-right", "levels": ["high"]},
        {"id": "matrices", "name": "Matrices", "icon": "fa-table", "levels": ["high"]},
        {"id": "complex-numbers", "name": "Complex Numbers", "icon": "fa-square-root-alt", "levels": ["high"]},
        {"id": "differential-equations", "name": "Differential Equations", "icon": "fa-equals", "levels": ["high"]},
        {"id": "numerical-methods", "name": "Numerical Methods", "icon": "fa-calculator", "levels": ["high"]},
        {"id": "probability-advanced", "name": "Probability", "icon": "fa-dice", "levels": ["high"]},
        {"id": "statistics-advanced", "name": "Statistics", "icon": "fa-chart-bar", "levels": ["high"]},
        {"id": "mechanics-math", "name": "Mechanics", "icon": "fa-cogs", "levels": ["high"]}
    ]

for subject in ["Economics", "Business Management", "Commerce"]:
    TOPICS_DATA[subject] = [
        {"id": "microeconomics", "name": "Microeconomics", "icon": "fa-chart-line", "levels": ["high"]},
        {"id": "macroeconomics", "name": "Macroeconomics", "icon": "fa-chart-bar", "levels": ["high"]},
        {"id": "market-structures", "name": "Market Structures", "icon": "fa-store", "levels": ["high"]},
        {"id": "supply-demand", "name": "Supply & Demand", "icon": "fa-balance-scale", "levels": ["high"]},
        {"id": "international-trade", "name": "International Trade", "icon": "fa-globe", "levels": ["high"]},
        {"id": "business-organization", "name": "Business Organization", "icon": "fa-briefcase", "levels": ["high"]},
        {"id": "marketing", "name": "Marketing", "icon": "fa-bullhorn", "levels": ["high"]},
        {"id": "finance", "name": "Finance", "icon": "fa-money-bill-wave", "levels": ["high"]},
        {"id": "accounting", "name": "Accounting", "icon": "fa-calculator", "levels": ["high"]},
        {"id": "entrepreneurship", "name": "Entrepreneurship", "icon": "fa-lightbulb", "levels": ["high"]}
    ]

for subject in ["Geography", "US History"]:
    TOPICS_DATA[subject] = [
        {"id": "physical-geography", "name": "Physical Geography", "icon": "fa-mountain", "levels": ["middle", "high"]},
        {"id": "human-geography", "name": "Human Geography", "icon": "fa-users", "levels": ["middle", "high"]},
        {"id": "climate", "name": "Climate", "icon": "fa-cloud", "levels": ["middle", "high"]},
        {"id": "population", "name": "Population", "icon": "fa-user-friends", "levels": ["middle", "high"]},
        {"id": "economic-geography", "name": "Economic Geography", "icon": "fa-industry", "levels": ["high"]},
        {"id": "historical-events", "name": "Historical Events", "icon": "fa-monument", "levels": ["middle", "high"]},
        {"id": "cultural-geography", "name": "Cultural Geography", "icon": "fa-globe-americas", "levels": ["middle", "high"]},
        {"id": "political-geography", "name": "Political Geography", "icon": "fa-flag", "levels": ["high"]},
        {"id": "urban-geography", "name": "Urban Geography", "icon": "fa-city", "levels": ["high"]},
        {"id": "environmental-geography", "name": "Environmental Geography", "icon": "fa-tree", "levels": ["middle", "high"]}
    ]

for subject in ["Computer Science"]:
    TOPICS_DATA[subject] = [
        {"id": "programming-basics", "name": "Programming Basics", "icon": "fa-code", "levels": ["middle", "high"]},
        {"id": "algorithms", "name": "Algorithms", "icon": "fa-project-diagram", "levels": ["high"]},
        {"id": "data-structures", "name": "Data Structures", "icon": "fa-database", "levels": ["high"]},
        {"id": "web-development", "name": "Web Development", "icon": "fa-laptop-code", "levels": ["high"]},
        {"id": "databases", "name": "Databases", "icon": "fa-server", "levels": ["high"]},
        {"id": "networking", "name": "Networking", "icon": "fa-network-wired", "levels": ["high"]},
        {"id": "cybersecurity", "name": "Cybersecurity", "icon": "fa-shield-alt", "levels": ["high"]},
        {"id": "artificial-intelligence", "name": "Artificial Intelligence", "icon": "fa-robot", "levels": ["high"]},
        {"id": "software-engineering", "name": "Software Engineering", "icon": "fa-cogs", "levels": ["high"]},
        {"id": "mobile-development", "name": "Mobile Development", "icon": "fa-mobile-alt", "levels": ["high"]}
    ]

def filter_topics_by_grade(all_topics, grade_level):
    """Filter topics based on grade level appropriateness"""
    if grade_level <= 5:
        target_level = "elementary"
    elif grade_level <= 8:
        target_level = "middle"
    else:
        target_level = "high"
    
    filtered_topics = [topic for topic in all_topics if target_level in topic.get("levels", [])]
    
    # If no specific filtering or topics not found, return first 6 topics
    if not filtered_topics and all_topics:
        return all_topics[:6]
    
    return filtered_topics

def generate_math_question(template, level, question_id):
    """Generate math questions with realistic answers"""
    if level == "elementary":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 50)
        if "×" in template or "x" in template:
            correct_answer = num1 * num2
            options = [
                correct_answer,
                correct_answer + random.randint(1, 10),
                correct_answer - random.randint(1, 10),
                correct_answer + random.randint(5, 15)
            ]
        elif "÷" in template or "/" in template:
            num2 = random.randint(1, 10)  # Avoid division by zero
            correct_answer = num1 // num2
            options = [
                correct_answer,
                correct_answer + random.randint(1, 5),
                correct_answer - random.randint(1, 5),
                (num1 * num2) // 2
            ]
        elif "area" in template.lower():
            correct_answer = num1 * num1
            options = [
                correct_answer,
                num1 * 4,  # perimeter
                num1 + num1,
                num1 * 2
            ]
        elif "perimeter" in template.lower():
            correct_answer = 2 * (num1 + num2)
            options = [
                correct_answer,
                num1 * num2,  # area
                num1 + num2,
                (num1 + num2) * 4
            ]
        else:  # addition/subtraction
            if "+" in template:
                correct_answer = num1 + num2
            else:
                correct_answer = num1 - num2
            options = [
                correct_answer,
                correct_answer + random.randint(1, 20),
                correct_answer - random.randint(1, 20),
                num1 + num2 + random.randint(1, 10)
            ]
    
    elif level == "middle":
        if "x +" in template:  # Linear equation
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            c = random.randint(10, 50)
            correct_answer = (c - b) // a
            options = [
                correct_answer,
                correct_answer + random.randint(1, 5),
                correct_answer - random.randint(1, 5),
                (c + b) // a
            ]
        elif "area of a circle" in template.lower():
            radius = random.randint(1, 10)
            correct_answer = round(3.14 * radius * radius, 2)
            options = [
                correct_answer,
                round(2 * 3.14 * radius, 2),  # circumference
                radius * radius,
                round(3.14 * radius, 2)
            ]
        elif "% of" in template:
            percentage = random.randint(1, 100)
            number = random.randint(10, 1000)
            correct_answer = round((percentage / 100) * number, 2)
            options = [
                correct_answer,
                round((percentage / 100) * number * 2, 2),
                round(number / percentage, 2),
                round(percentage * number / 50, 2)
            ]
        else:
            correct_answer = random.randint(1, 100)
            options = [
                correct_answer,
                correct_answer + random.randint(1, 20),
                correct_answer - random.randint(1, 20),
                correct_answer * 2
            ]
    
    else:  # high school
        correct_answer = random.randint(1, 50)
        options = [
            correct_answer,
            correct_answer + random.randint(1, 10),
            correct_answer - random.randint(1, 10),
            correct_answer * 2
        ]
    
    # Shuffle options and find correct index
    correct_index = options.index(correct_answer)
    random.shuffle(options)
    correct_index = options.index(correct_answer)  # Update index after shuffle
    
    return {
        "text": template.format(num1=num1, num2=num2, num3=(num1 + num2) if 'num3' in template else 0,
                               percentage=percentage if 'percentage' in template else 0,
                               number=number if 'number' in template else 0),
        "options": options,
        "correctAnswer": correct_index,
        "explanation": f"This is a grade-appropriate {level} level mathematics question.",
        "difficulty": "Easy" if level == "elementary" else "Medium" if level == "middle" else "Hard"
    }

def generate_science_question(template, level, subject, question_id):
    """Generate science questions with realistic answers"""
    science_answers = {
        "unit of force": ["Newton", "Joule", "Watt", "Pascal"],
        "force pulls objects toward earth": ["Gravity", "Magnetism", "Friction", "Tension"],
        "energy moving object": ["Kinetic energy", "Potential energy", "Thermal energy", "Chemical energy"],
        "speed of light": ["299,792 km/s", "150,000 km/s", "450,000 km/s", "100,000 km/s"],
        "action reaction law": ["Newton's 3rd Law", "Newton's 1st Law", "Newton's 2nd Law", "Law of Gravity"],
        "acceleration due to gravity": ["9.8 m/s²", "6.7 m/s²", "10.2 m/s²", "8.5 m/s²"],
        "chemical symbol oxygen": ["O", "Ox", "Og", "Om"],
        "ph neutral solution": ["7", "0", "14", "1"],
        "states of matter": ["Solid, Liquid, Gas", "Hot, Cold, Warm", "Big, Small, Medium", "Hard, Soft, Medium"],
        "atomic number hydrogen": ["1", "2", "3", "4"],
        "gas plants photosynthesis": ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"]
    }
    
    # Find matching answer pattern
    question_lower = template.lower()
    correct_answer = ""
    options = []
    
    for key, possible_answers in science_answers.items():
        if key in question_lower:
            correct_answer = possible_answers[0]
            options = possible_answers.copy()
            random.shuffle(options)
            break
    
    # If no specific match found, use generic answers
    if not correct_answer:
        correct_answer = f"Correct {subject} Answer"
        options = [
            correct_answer,
            f"Alternative {subject} Answer 1",
            f"Alternative {subject} Answer 2", 
            f"Alternative {subject} Answer 3"
        ]
        random.shuffle(options)
    
    correct_index = options.index(correct_answer)
    
    return {
        "text": template,
        "options": options,
        "correctAnswer": correct_index,
        "explanation": f"This is a grade-appropriate {level} level {subject} question.",
        "difficulty": "Easy" if level == "elementary" else "Medium" if level == "middle" else "Hard"
    }

# Question generator with grade-appropriate content
def generate_questions_by_grade(subject, topic, grade_level, count=30):
    questions = []
    
    # Determine grade level category
    if grade_level <= 5:
        level = "elementary"
    elif grade_level <= 8:
        level = "middle"
    else:
        level = "high"
    
    # Grade-appropriate question templates
    question_templates = {
        "Mathematics": {
            "elementary": [
                "What is {num1} + {num2}?",
                "Solve: {num1} - {num2} = ?",
                "{num1} × {num2} = ?",
                "{num1} ÷ {num2} = ?",
                "What is the area of a square with side {num1}?",
                "Calculate the perimeter of a rectangle with length {num1} and width {num2}"
            ],
            "middle": [
                "Solve for x: {num1}x + {num2} = {num3}",
                "Calculate the area of a circle with radius {num1}",
                "What is {percentage}% of {number}?",
                "Simplify: 2x + 3x - x",
                "Factorize: x² + 5x + 6",
                "Solve the equation: 2x - 5 = 15"
            ],
            "high": [
                "Differentiate f(x) = x² with respect to x",
                "Integrate ∫2x dx",
                "Solve the quadratic equation: x² + 5x + 6 = 0",
                "Find the limit: lim(x→2) (x² - 4)/(x - 2)",
                "Calculate the derivative of f(x) = 3x³ at x = 2",
                "Solve the system: 2x + y = 7, x - y = -1"
            ]
        },
        "Physics": {
            "elementary": [
                "What is the unit of force?",
                "Which force pulls objects toward Earth?",
                "What type of energy does a moving object have?",
                "Name one source of renewable energy",
                "What is the speed of light?",
                "Which law states that every action has an equal and opposite reaction?"
            ],
            "middle": [
                "Calculate the velocity of an object moving 100m in 10s",
                "What is the acceleration due to gravity on Earth?",
                "Explain the concept of inertia in physics",
                "A 5kg object is pushed with 10N force. What is its acceleration?",
                "Calculate the work done when a force of 20N moves an object 5m",
                "What is the power if 100J of work is done in 5s?"
            ],
            "high": [
                "Apply Newton's 2nd law to a car accelerating on a highway",
                "Calculate the work done when lifting a 10kg object 2m vertically",
                "Solve this kinematics equation: v² = u² + 2as",
                "Explain the principle of conservation of energy",
                "Calculate the electric field strength at a point 2m from a 4C charge",
                "A gas expands from 2L to 5L at constant pressure. Calculate the work done."
            ]
        },
        "Chemistry": {
            "elementary": [
                "What is the chemical symbol for Oxygen?",
                "How many electrons does Hydrogen have?",
                "What is the pH of a neutral solution?",
                "Name the three states of matter",
                "What is the atomic number of Hydrogen?",
                "Which gas do plants use for photosynthesis?"
            ],
            "middle": [
                "Balance this chemical equation: H₂ + O₂ → H₂O",
                "Calculate the molar mass of H₂O",
                "Explain the difference between elements and compounds",
                "What is the concentration if 10g of salt is dissolved in 2L of water?",
                "Name the type of reaction: CH₄ + 2O₂ → CO₂ + 2H₂O",
                "Calculate the number of moles in 36g of water"
            ],
            "high": [
                "Explain the concept of chemical equilibrium",
                "Calculate the pH of a 0.01M HCl solution",
                "Solve this stoichiometry problem: How many grams of O₂ are needed to burn 16g of CH₄?",
                "Describe the mechanism of SN2 reaction",
                "Calculate the equilibrium constant for N₂ + 3H₂ ⇌ 2NH₃",
                "Explain the principles of gas chromatography"
            ]
        },
        "Biology": {
            "elementary": [
                "What is the basic unit of life?",
                "Which organ pumps blood in the human body?",
                "What process do plants use to make food?",
                "Name one adaptation of desert animals",
                "What are the stages of a butterfly's life cycle?",
                "Which gas do animals breathe out?"
            ],
            "middle": [
                "Describe the structure of a plant cell",
                "What is the function of mitochondria?",
                "Explain the process of natural selection",
                "How does the circulatory system work?",
                "What is DNA and what is its role?",
                "Describe the process of photosynthesis"
            ],
            "high": [
                "Explain the central dogma of molecular biology",
                "Describe the process of protein synthesis",
                "What is the role of enzymes in biochemical reactions?",
                "Explain the principles of Mendelian genetics",
                "Describe the immune response to pathogens",
                "What is CRISPR and how does it work?"
            ]
        }
    }
    
    # Generate questions
    for i in range(count):
        if subject in question_templates and level in question_templates[subject]:
            template = random.choice(question_templates[subject][level])
            
            if subject == "Mathematics":
                question_data = generate_math_question(template, level, i)
            elif subject in ["Physics", "Chemistry", "Biology"]:
                question_data = generate_science_question(template, level, subject, i)
            else:
                # Generic question for other subjects
                correct_answer = f"Correct {subject} Answer"
                options = [
                    correct_answer,
                    f"Alternative {subject} Answer 1",
                    f"Alternative {subject} Answer 2",
                    f"Alternative {subject} Answer 3"
                ]
                random.shuffle(options)
                correct_index = options.index(correct_answer)
                
                question_data = {
                    "text": template,
                    "options": options,
                    "correctAnswer": correct_index,
                    "explanation": f"This is a grade-appropriate {level} level {subject} question about {topic}.",
                    "difficulty": "Easy" if level == "elementary" else "Medium" if level == "middle" else "Hard"
                }
        else:
            # Generic question for subjects not in templates
            correct_answer = f"Correct {subject} Answer"
            options = [
                correct_answer,
                f"Alternative {subject} Answer 1",
                f"Alternative {subject} Answer 2",
                f"Alternative {subject} Answer 3"
            ]
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            
            question_data = {
                "text": f"Grade {grade_level} {subject} question about {topic}: What is the correct answer?",
                "options": options,
                "correctAnswer": correct_index,
                "explanation": f"This is a grade-appropriate {level} level {subject} question about {topic}.",
                "difficulty": "Easy" if level == "elementary" else "Medium" if level == "middle" else "Hard"
            }
        
        questions.append({
            "id": i + 1,
            **question_data
        })
    
    return questions

@app.route('/')
def home():
    """Home endpoint - returns API information"""
    return jsonify({
        "message": "Ideolix Learning Hub API",
        "version": "2.2.0",
        "curricula": list(CURRICULA_DATA.keys()),
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "features": ["grade_appropriate_topics", "multiple_curricula", "comprehensive_subjects"],
        "endpoints": {
            "GET /": "API information",
            "POST /api/subjects": "Get subjects by curriculum and grade",
            "POST /api/topics": "Get grade-appropriate topics by subject and grade",
            "POST /api/questions": "Get grade-appropriate questions",
            "GET /api/health": "Health check",
            "GET /api/curricula": "Get all available curricula",
            "GET /api/debug/subjects": "Debug endpoint for subjects",
            "GET /api/debug/topics": "Debug endpoint for topics"
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.2.0",
        "curricula_count": len(CURRICULA_DATA),
        "subjects_count": len(TOPICS_DATA),
        "feature": "grade_appropriate_topics_active",
        "message": "Ideolix Learning Hub API is running smoothly with grade-appropriate topics"
    })

@app.route('/api/curricula')
def get_curricula():
    """Get all available curricula"""
    return jsonify({
        "success": True,
        "curricula": {name: data["name"] for name, data in CURRICULA_DATA.items()},
        "total_curricula": len(CURRICULA_DATA)
    })

@app.route('/api/subjects', methods=['POST'])
def get_subjects():
    """Get subjects based on curriculum and grade level - SIMPLIFIED"""
    try:
        data = request.get_json()
        
        # Use defaults if no data provided
        if not data:
            curriculum = 'nigeria'
            grade = 10
        else:
            curriculum = data.get('curriculum', 'nigeria')
            grade = data.get('grade', 10)
        
        print(f"📥 Received subjects request: curriculum={curriculum}, grade={grade}")
        
        if curriculum not in CURRICULA_DATA:
            return jsonify({
                "success": False,
                "error": f"Curriculum '{curriculum}' not found. Available: {list(CURRICULA_DATA.keys())}"
            }), 400
        
        curriculum_info = CURRICULA_DATA[curriculum]
        subjects = curriculum_info["subjects"]
        
        print(f"📤 Sending response: {len(subjects)} subjects for {curriculum_info['name']}")
        
        return jsonify({
            "success": True,
            "curriculum": curriculum,
            "curriculum_name": curriculum_info["name"],
            "grade": grade,
            "subjects": subjects,
            "total_subjects": len(subjects)
        })
        
    except Exception as e:
        print(f"❌ Error in get_subjects: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/topics', methods=['POST'])
def get_topics():
    """Get topics for a specific subject and curriculum with grade-based filtering"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        subject = data.get('subject')
        curriculum = data.get('curriculum', 'nigeria')
        grade = int(data.get('grade', 10))
        
        if not subject:
            return jsonify({
                "success": False,
                "error": "Subject parameter is required"
            }), 400
        
        print(f"📥 Received topics request: subject={subject}, curriculum={curriculum}, grade={grade}")
        
        # Get all topics for the subject
        all_topics = TOPICS_DATA.get(subject, [])
        
        # Filter topics based on grade level
        filtered_topics = filter_topics_by_grade(all_topics, grade)
        
        print(f"📤 Sending response: {len(filtered_topics)} grade-appropriate topics for {subject} Grade {grade}")
        
        return jsonify({
            "success": True,
            "subject": subject,
            "curriculum": curriculum,
            "grade": grade,
            "topics": filtered_topics,
            "total_topics": len(filtered_topics),
            "grade_level": "Elementary" if grade <= 5 else "Middle School" if grade <= 8 else "High School"
        })
        
    except Exception as e:
        print(f"❌ Error in get_topics: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/questions', methods=['POST'])
def get_questions():
    """Get questions for practice or assessment with grade-appropriate content"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        subject = data.get('subject')
        topic = data.get('topic')
        exam_type = data.get('examType', 'practice')
        curriculum = data.get('curriculum', 'nigeria')
        grade = data.get('grade', 10)
        count = data.get('count', 30)
        
        if not subject or not topic:
            return jsonify({
                "success": False,
                "error": "Subject and topic parameters are required"
            }), 400
        
        print(f"📥 Received questions request: subject={subject}, topic={topic}, grade={grade}, count={count}")
        
        # Generate grade-appropriate questions
        questions = generate_questions_by_grade(subject, topic, int(grade), count)
        
        print(f"📤 Sending response: {len(questions)} questions for {subject} - {topic}")
        
        return jsonify({
            "success": True,
            "subject": subject,
            "topic": topic,
            "examType": exam_type,
            "curriculum": curriculum,
            "grade": grade,
            "count": len(questions),
            "questions": questions
        })
        
    except Exception as e:
        print(f"❌ Error in get_questions: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Debug endpoints for easy testing
@app.route('/api/debug/subjects', methods=['GET'])
def debug_subjects():
    """Debug endpoint to test subjects without POST data"""
    curriculum = request.args.get('curriculum', 'nigeria')
    grade = request.args.get('grade', '10')
    
    if curriculum not in CURRICULA_DATA:
        return jsonify({
            "success": False,
            "error": f"Curriculum '{curriculum}' not found"
        }), 400
    
    curriculum_info = CURRICULA_DATA[curriculum]
    subjects = curriculum_info["subjects"]
    
    return jsonify({
        "success": True,
        "curriculum": curriculum,
        "grade": grade,
        "subjects": subjects,
        "total_subjects": len(subjects)
    })

@app.route('/api/debug/topics', methods=['GET'])
def debug_topics():
    """Debug endpoint to test topics without POST data"""
    subject = request.args.get('subject', 'Mathematics')
    grade = int(request.args.get('grade', '10'))
    
    all_topics = TOPICS_DATA.get(subject, [
        {"id": "topic-1", "name": f"{subject} Fundamentals", "icon": "fa-book", "levels": ["elementary", "middle", "high"]},
        {"id": "topic-2", "name": f"{subject} Principles", "icon": "fa-book", "levels": ["middle", "high"]},
        {"id": "topic-3", "name": f"{subject} Applications", "icon": "fa-book", "levels": ["high"]}
    ])
    
    # Filter topics based on grade level
    filtered_topics = filter_topics_by_grade(all_topics, grade)
    
    return jsonify({
        "success": True,
        "subject": subject,
        "grade": grade,
        "topics": filtered_topics,
        "total_topics": len(filtered_topics),
        "grade_level": "Elementary" if grade <= 5 else "Middle School" if grade <= 8 else "High School"
    })

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "Ideolix Learning Hub API is working!",
        "method": request.method,
        "timestamp": datetime.now().isoformat(),
        "curricula_available": list(CURRICULA_DATA.keys()),
        "subjects_available": list(TOPICS_DATA.keys())[:10],  # First 10 subjects
        "feature": "grade_appropriate_topics"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET /",
            "POST /api/subjects", 
            "POST /api/topics",
            "POST /api/questions",
            "GET /api/health",
            "GET /api/curricula",
            "GET /api/debug/subjects",
            "GET /api/debug/topics"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405

if __name__ == '__main__':
    print("🚀 Starting Ideolix Learning Hub API Server...")
    print("📚 Available Curricula:", list(CURRICULA_DATA.keys()))
    print("🎯 Subjects per curriculum:", {name: len(data["subjects"]) for name, data in CURRICULA_DATA.items()})
    print("📖 Total subjects with topics:", len(TOPICS_DATA))
    print("🎓 Grade Level Filtering: ACTIVE")
    print("   - Elementary (Grades 1-5): Basic concepts")
    print("   - Middle School (Grades 6-8): Intermediate topics") 
    print("   - High School (Grades 9-12): Advanced concepts")
    print("\n🌐 Available endpoints:")
    print("  GET  / - API information")
    print("  GET  /api/health - Health check") 
    print("  GET  /api/curricula - Get all curricula")
    print("  POST /api/subjects - Get subjects by curriculum and grade")
    print("  POST /api/topics - Get grade-appropriate topics")
    print("  POST /api/questions - Get grade-appropriate questions")
    print("  GET  /api/debug/subjects - Debug endpoint for subjects")
    print("  GET  /api/debug/topics - Debug endpoint for topics")
    print("  GET  /api/test - Test endpoint")
    print(f"\n⏰ Server started at: {datetime.now().isoformat()}")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
