# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Comprehensive curricula data with proper naming conventions
CURRICULA_DATA = {
    "nigeria": {
        "name": "Nigerian Curriculum",
        "grades": {
            "primary": ["Primary 1", "Primary 2", "Primary 3", "Primary 4", "Primary 5", "Primary 6"],
            "junior_secondary": ["JSS 1", "JSS 2", "JSS 3"],
            "senior_secondary": ["SSS 1", "SSS 2", "SSS 3"]
        },
        "subjects": {
            "core": [
                {"id": 1, "name": "Mathematics", "description": "Number work, Algebra, Geometry", "icon": "fa-calculator"},
                {"id": 2, "name": "English Studies", "description": "Grammar, Composition, Literature", "icon": "fa-language"},
                {"id": 3, "name": "Basic Science", "description": "Physics, Chemistry, Biology fundamentals", "icon": "fa-flask"},
                {"id": 4, "name": "Social Studies", "description": "Civic Education, History, Geography", "icon": "fa-landmark"},
                {"id": 5, "name": "Yoruba/Igbo/Hausa", "description": "Nigerian Languages", "icon": "fa-globe-africa"}
            ],
            "science": [
                {"id": 6, "name": "Physics", "description": "Mechanics, Thermodynamics, Waves", "icon": "fa-atom"},
                {"id": 7, "name": "Chemistry", "description": "Organic, Inorganic, Physical Chemistry", "icon": "fa-vial"},
                {"id": 8, "name": "Biology", "description": "Living organisms, Genetics, Ecology", "icon": "fa-dna"},
                {"id": 9, "name": "Further Mathematics", "description": "Advanced Mathematics topics", "icon": "fa-square-root-alt"}
            ],
            "arts": [
                {"id": 10, "name": "Literature in English", "description": "Prose, Poetry, Drama", "icon": "fa-book"},
                {"id": 11, "name": "Government", "description": "Political systems, Governance", "icon": "fa-university"},
                {"id": 12, "name": "Economics", "description": "Microeconomics, Macroeconomics", "icon": "fa-chart-line"},
                {"id": 13, "name": "Commerce", "description": "Trade, Business, Finance", "icon": "fa-shopping-cart"}
            ]
        }
    },
    "cambridge": {
        "name": "Cambridge International",
        "grades": {
            "lower_secondary": ["Year 7", "Year 8", "Year 9"],
            "igcse": ["Year 10", "Year 11"],
            "alevel": ["AS Level", "A Level"]
        },
        "subjects": {
            "core": [
                {"id": 1, "name": "Mathematics", "description": "Pure Mathematics, Statistics", "icon": "fa-calculator"},
                {"id": 2, "name": "English Language", "description": "Reading, Writing, Speaking", "icon": "fa-language"},
                {"id": 3, "name": "Combined Science", "description": "Biology, Chemistry, Physics", "icon": "fa-flask"},
                {"id": 4, "name": "Global Perspectives", "description": "Critical thinking, Research", "icon": "fa-globe"}
            ],
            "sciences": [
                {"id": 5, "name": "Physics", "description": "Forces, Energy, Waves, Electricity", "icon": "fa-atom"},
                {"id": 6, "name": "Chemistry", "description": "Elements, Reactions, Organic Chemistry", "icon": "fa-vial"},
                {"id": 7, "name": "Biology", "description": "Cells, Organisms, Ecology", "icon": "fa-dna"},
                {"id": 8, "name": "Additional Mathematics", "description": "Advanced mathematical concepts", "icon": "fa-square-root-alt"},
                {"id": 9, "name": "Computer Science", "description": "Programming, Algorithms", "icon": "fa-laptop-code"}
            ],
            "humanities": [
                {"id": 10, "name": "Geography", "description": "Physical and Human Geography", "icon": "fa-mountain"},
                {"id": 11, "name": "History", "description": "World History, Modern Studies", "icon": "fa-monument"},
                {"id": 12, "name": "Economics", "description": "Market systems, International trade", "icon": "fa-chart-line"},
                {"id": 13, "name": "Business Studies", "description": "Business organization, Marketing", "icon": "fa-briefcase"}
            ]
        }
    },
    "american": {
        "name": "American Curriculum",
        "grades": {
            "elementary": ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"],
            "middle_school": ["Grade 6", "Grade 7", "Grade 8"],
            "high_school": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"]
        },
        "subjects": {
            "core": [
                {"id": 1, "name": "Mathematics", "description": "Algebra, Geometry, Calculus", "icon": "fa-calculator"},
                {"id": 2, "name": "English Language Arts", "description": "Reading, Writing, Literature", "icon": "fa-language"},
                {"id": 3, "name": "Science", "description": "Physical, Life, Earth Sciences", "icon": "fa-flask"},
                {"id": 4, "name": "Social Studies", "description": "History, Geography, Civics", "icon": "fa-landmark"}
            ],
            "advanced": [
                {"id": 5, "name": "Physics", "description": "AP Physics, Modern Physics", "icon": "fa-atom"},
                {"id": 6, "name": "Chemistry", "description": "AP Chemistry, Organic Chemistry", "icon": "fa-vial"},
                {"id": 7, "name": "Biology", "description": "AP Biology, Anatomy & Physiology", "icon": "fa-dna"},
                {"id": 8, "name": "Calculus", "description": "AP Calculus AB/BC", "icon": "fa-square-root-alt"},
                {"id": 9, "name": "Computer Science", "description": "AP Computer Science", "icon": "fa-laptop-code"}
            ],
            "electives": [
                {"id": 10, "name": "US History", "description": "American History and Government", "icon": "fa-flag-usa"},
                {"id": 11, "name": "Economics", "description": "Micro and Macroeconomics", "icon": "fa-chart-line"},
                {"id": 12, "name": "Psychology", "description": "Human behavior and mind", "icon": "fa-brain"},
                {"id": 13, "name": "Environmental Science", "description": "Ecology and sustainability", "icon": "fa-leaf"}
            ]
        }
    },
    "ib": {
        "name": "International Baccalaureate",
        "grades": {
            "myp": ["MYP 1", "MYP 2", "MYP 3", "MYP 4", "MYP 5"],
            "dp": ["DP Year 1", "DP Year 2"]
        },
        "subjects": {
            "core": [
                {"id": 1, "name": "Mathematics", "description": "Analysis, Applications, Interpretation", "icon": "fa-calculator"},
                {"id": 2, "name": "English A", "description": "Language and Literature", "icon": "fa-language"},
                {"id": 3, "name": "Sciences", "description": "Biology, Chemistry, Physics, ESS", "icon": "fa-flask"},
                {"id": 4, "name": "Individuals & Societies", "description": "History, Economics, Geography", "icon": "fa-globe"}
            ],
            "sciences": [
                {"id": 5, "name": "Physics", "description": "HL and SL Physics", "icon": "fa-atom"},
                {"id": 6, "name": "Chemistry", "description": "HL and SL Chemistry", "icon": "fa-vial"},
                {"id": 7, "name": "Biology", "description": "HL and SL Biology", "icon": "fa-dna"},
                {"id": 8, "name": "Computer Science", "description": "Programming and algorithms", "icon": "fa-laptop-code"},
                {"id": 9, "name": "Environmental Systems", "description": "Ecology and sustainability", "icon": "fa-leaf"}
            ],
            "humanities": [
                {"id": 10, "name": "History", "description": "World history topics", "icon": "fa-monument"},
                {"id": 11, "name": "Economics", "description": "Global economics", "icon": "fa-chart-line"},
                {"id": 12, "name": "Psychology", "description": "Human behavior studies", "icon": "fa-brain"},
                {"id": 13, "name": "Business Management", "description": "International business", "icon": "fa-briefcase"}
            ]
        }
    }
}

# Comprehensive topics for each subject (15+ topics each)
TOPICS_DATA = {
    # Mathematics topics (15+)
    "Mathematics": [
        {"id": "number-theory", "name": "Number Theory", "icon": "fa-hashtag"},
        {"id": "algebra-basics", "name": "Algebra Basics", "icon": "fa-superscript"},
        {"id": "linear-equations", "name": "Linear Equations", "icon": "fa-equals"},
        {"id": "quadratic-equations", "name": "Quadratic Equations", "icon": "fa-project-diagram"},
        {"id": "polynomials", "name": "Polynomials", "icon": "fa-superscript"},
        {"id": "geometry", "name": "Geometry", "icon": "fa-shapes"},
        {"id": "trigonometry", "name": "Trigonometry", "icon": "fa-calculator"},
        {"id": "calculus", "name": "Calculus", "icon": "fa-infinity"},
        {"id": "statistics", "name": "Statistics", "icon": "fa-chart-bar"},
        {"id": "probability", "name": "Probability", "icon": "fa-dice"},
        {"id": "vectors", "name": "Vectors", "icon": "fa-arrow-right"},
        {"id": "matrices", "name": "Matrices", "icon": "fa-table"},
        {"id": "complex-numbers", "name": "Complex Numbers", "icon": "fa-square-root-alt"},
        {"id": "sequences-series", "name": "Sequences & Series", "icon": "fa-list-ol"},
        {"id": "coordinate-geometry", "name": "Coordinate Geometry", "icon": "fa-map"},
        {"id": "functions", "name": "Functions", "icon": "fa-project-diagram"},
        {"id": "logarithms", "name": "Logarithms", "icon": "fa-superscript"}
    ],
    
    # Physics topics (15+)
    "Physics": [
        {"id": "mechanics", "name": "Mechanics", "icon": "fa-cogs"},
        {"id": "kinematics", "name": "Kinematics", "icon": "fa-running"},
        {"id": "dynamics", "name": "Dynamics", "icon": "fa-weight-hanging"},
        {"id": "energy-work", "name": "Energy & Work", "icon": "fa-bolt"},
        {"id": "thermodynamics", "name": "Thermodynamics", "icon": "fa-temperature-high"},
        {"id": "waves", "name": "Waves", "icon": "fa-wave-square"},
        {"id": "optics", "name": "Optics", "icon": "fa-lightbulb"},
        {"id": "electricity", "name": "Electricity", "icon": "fa-bolt"},
        {"id": "magnetism", "name": "Magnetism", "icon": "fa-magnet"},
        {"id": "electromagnetism", "name": "Electromagnetism", "icon": "fa-bolt"},
        {"id": "modern-physics", "name": "Modern Physics", "icon": "fa-atom"},
        {"id": "quantum-mechanics", "name": "Quantum Mechanics", "icon": "fa-atom"},
        {"id": "nuclear-physics", "name": "Nuclear Physics", "icon": "fa-radiation"},
        {"id": "astrophysics", "name": "Astrophysics", "icon": "fa-star"},
        {"id": "fluid-mechanics", "name": "Fluid Mechanics", "icon": "fa-tint"},
        {"id": "sound-waves", "name": "Sound Waves", "icon": "fa-volume-up"}
    ],
    
    # Chemistry topics (15+)
    "Chemistry": [
        {"id": "atomic-structure", "name": "Atomic Structure", "icon": "fa-atom"},
        {"id": "periodic-table", "name": "Periodic Table", "icon": "fa-table"},
        {"id": "chemical-bonding", "name": "Chemical Bonding", "icon": "fa-link"},
        {"id": "stoichiometry", "name": "Stoichiometry", "icon": "fa-balance-scale"},
        {"id": "organic-chemistry", "name": "Organic Chemistry", "icon": "fa-atom"},
        {"id": "inorganic-chemistry", "name": "Inorganic Chemistry", "icon": "fa-vial"},
        {"id": "physical-chemistry", "name": "Physical Chemistry", "icon": "fa-flask"},
        {"id": "acids-bases", "name": "Acids & Bases", "icon": "fa-vial"},
        {"id": "electrochemistry", "name": "Electrochemistry", "icon": "fa-bolt"},
        {"id": "thermochemistry", "name": "Thermochemistry", "icon": "fa-temperature-high"},
        {"id": "chemical-kinetics", "name": "Chemical Kinetics", "icon": "fa-clock"},
        {"id": "chemical-equilibrium", "name": "Chemical Equilibrium", "icon": "fa-balance-scale"},
        {"id": "analytical-chemistry", "name": "Analytical Chemistry", "icon": "fa-search"},
        {"id": "biochemistry", "name": "Biochemistry", "icon": "fa-dna"},
        {"id": "environmental-chemistry", "name": "Environmental Chemistry", "icon": "fa-leaf"},
        {"id": "nuclear-chemistry", "name": "Nuclear Chemistry", "icon": "fa-radiation"}
    ],
    
    # Biology topics (15+)
    "Biology": [
        {"id": "cell-biology", "name": "Cell Biology", "icon": "fa-microscope"},
        {"id": "molecular-biology", "name": "Molecular Biology", "icon": "fa-dna"},
        {"id": "genetics", "name": "Genetics", "icon": "fa-dna"},
        {"id": "evolution", "name": "Evolution", "icon": "fa-dna"},
        {"id": "ecology", "name": "Ecology", "icon": "fa-leaf"},
        {"id": "anatomy", "name": "Anatomy", "icon": "fa-heart"},
        {"id": "physiology", "name": "Physiology", "icon": "fa-lungs"},
        {"id": "botany", "name": "Botany", "icon": "fa-seedling"},
        {"id": "zoology", "name": "Zoology", "icon": "fa-paw"},
        {"id": "microbiology", "name": "Microbiology", "icon": "fa-bacteria"},
        {"id": "biochemistry", "name": "Biochemistry", "icon": "fa-flask"},
        {"id": "immunology", "name": "Immunology", "icon": "fa-shield-virus"},
        {"id": "neuroscience", "name": "Neuroscience", "icon": "fa-brain"},
        {"id": "marine-biology", "name": "Marine Biology", "icon": "fa-water"},
        {"id": "environmental-biology", "name": "Environmental Biology", "icon": "fa-tree"},
        {"id": "biotechnology", "name": "Biotechnology", "icon": "fa-dna"}
    ],
    
    # English Language topics (15+)
    "English Studies": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen"},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book"},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader"},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit"},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt"},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather"},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt"},
        {"id": "prose", "name": "Prose", "icon": "fa-book"},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks"},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone"},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones"},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract"},
        {"id": "letter-writing", "name": "Letter Writing", "icon": "fa-envelope"},
        {"id": "report-writing", "name": "Report Writing", "icon": "fa-clipboard"}
    ],
    
    "English Language": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen"},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book"},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader"},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit"},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt"},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather"},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt"},
        {"id": "prose", "name": "Prose", "icon": "fa-book"},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks"},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone"},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones"},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract"},
        {"id": "letter-writing", "name": "Letter Writing", "icon": "fa-envelope"},
        {"id": "report-writing", "name": "Report Writing", "icon": "fa-clipboard"}
    ],
    
    "English Language Arts": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen"},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book"},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader"},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit"},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt"},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather"},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt"},
        {"id": "prose", "name": "Prose", "icon": "fa-book"},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks"},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone"},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones"},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract"},
        {"id": "letter-writing", "name": "Letter Writing", "icon": "fa-envelope"},
        {"id": "report-writing", "name": "Report Writing", "icon": "fa-clipboard"}
    ],
    
    "English A": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen"},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book"},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader"},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit"},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt"},
        {"id": "creative-writing", "name": "Creative Writing", "icon": "fa-feather"},
        {"id": "poetry", "name": "Poetry", "icon": "fa-feather-alt"},
        {"id": "prose", "name": "Prose", "icon": "fa-book"},
        {"id": "drama", "name": "Drama", "icon": "fa-theater-masks"},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone"},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones"},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract"},
        {"id": "letter-writing", "name": "Letter Writing", "icon": "fa-envelope"},
        {"id": "report-writing", "name": "Report Writing", "icon": "fa-clipboard"}
    ]
}

# Add topics for other subjects
for subject in ["Basic Science", "Combined Science", "Science", "Sciences"]:
    TOPICS_DATA[subject] = [
        {"id": "scientific-method", "name": "Scientific Method", "icon": "fa-flask"},
        {"id": "matter", "name": "Matter", "icon": "fa-atom"},
        {"id": "energy", "name": "Energy", "icon": "fa-bolt"},
        {"id": "forces-motion", "name": "Forces & Motion", "icon": "fa-running"},
        {"id": "electricity-magnetism", "name": "Electricity & Magnetism", "icon": "fa-bolt"},
        {"id": "waves-sound", "name": "Waves & Sound", "icon": "fa-wave-square"},
        {"id": "light-optics", "name": "Light & Optics", "icon": "fa-lightbulb"},
        {"id": "earth-science", "name": "Earth Science", "icon": "fa-globe"},
        {"id": "weather-climate", "name": "Weather & Climate", "icon": "fa-cloud"},
        {"id": "solar-system", "name": "Solar System", "icon": "fa-sun"},
        {"id": "cells", "name": "Cells", "icon": "fa-microscope"},
        {"id": "plants", "name": "Plants", "icon": "fa-seedling"},
        {"id": "animals", "name": "Animals", "icon": "fa-paw"},
        {"id": "human-body", "name": "Human Body", "icon": "fa-heart"},
        {"id": "environment", "name": "Environment", "icon": "fa-tree"},
        {"id": "chemistry-basics", "name": "Chemistry Basics", "icon": "fa-vial"}
    ]

for subject in ["Social Studies", "Global Perspectives", "Individuals & Societies"]:
    TOPICS_DATA[subject] = [
        {"id": "civics", "name": "Civics", "icon": "fa-landmark"},
        {"id": "history", "name": "History", "icon": "fa-monument"},
        {"id": "geography", "name": "Geography", "icon": "fa-globe"},
        {"id": "economics", "name": "Economics", "icon": "fa-chart-line"},
        {"id": "culture", "name": "Culture", "icon": "fa-globe-americas"},
        {"id": "government", "name": "Government", "icon": "fa-university"},
        {"id": "citizenship", "name": "Citizenship", "icon": "fa-user-friends"},
        {"id": "human-rights", "name": "Human Rights", "icon": "fa-handshake"},
        {"id": "global-issues", "name": "Global Issues", "icon": "fa-globe"},
        {"id": "sustainable-development", "name": "Sustainable Development", "icon": "fa-leaf"},
        {"id": "peace-conflict", "name": "Peace & Conflict", "icon": "fa-peace"},
        {"id": "technology-society", "name": "Technology & Society", "icon": "fa-laptop"},
        {"id": "media-literacy", "name": "Media Literacy", "icon": "fa-newspaper"},
        {"id": "ethical-thinking", "name": "Ethical Thinking", "icon": "fa-balance-scale"},
        {"id": "research-skills", "name": "Research Skills", "icon": "fa-search"},
        {"id": "critical-thinking", "name": "Critical Thinking", "icon": "fa-brain"}
    ]

# Question generator with grade-appropriate content
def generate_questions_by_grade(subject, topic, grade_level, count=30):
    questions = []
    
    # Grade-appropriate question templates
    question_templates = {
        "Mathematics": {
            "elementary": [
                f"What is {{num1}} + {{num2}}?",
                f"Solve: {{num1}} - {{num2}} = ?",
                f"{{num1}} × {{num2}} = ?",
                f"{{num1}} ÷ {{num2}} = ?"
            ],
            "middle": [
                f"Solve for x: {{num1}}x + {{num2}} = {{num3}}",
                f"Calculate the area of a {{shape}} with {{dimension}}",
                f"What is {{percentage}}% of {{number}}?",
                f"Simplify: {{expression}}"
            ],
            "high": [
                f"Differentiate {{function}} with respect to x",
                f"Integrate {{function}} dx",
                f"Solve the quadratic equation: {{equation}}",
                f"Find the limit: lim(x→{{num1}}) {{function}}"
            ]
        },
        "Physics": {
            "elementary": [
                f"What is the unit of {{quantity}}?",
                f"Which force pulls objects toward Earth?",
                f"What type of energy does a moving object have?",
                f"Name one source of {{energy_type}} energy"
            ],
            "middle": [
                f"Calculate the velocity of an object moving {{distance}} in {{time}}",
                f"What is the acceleration due to gravity on Earth?",
                f"Explain {{concept}} in physics",
                f"Solve this force problem: {{scenario}}"
            ],
            "high": [
                f"Apply Newton's {{law_number}} law to {{situation}}",
                f"Calculate the work done when {{scenario}}",
                f"Solve this kinematics equation: {{equation}}",
                f"Explain the principle of {{advanced_concept}}"
            ]
        }
    }
    
    # Generate questions based on grade level
    for i in range(count):
        if "Mathematics" in subject:
            if grade_level <= 5:  # Elementary
                template = random.choice(question_templates["Mathematics"]["elementary"])
                question_text = template.format(
                    num1=random.randint(1, 100),
                    num2=random.randint(1, 50),
                    num3=random.randint(1, 200),
                    shape=random.choice(["circle", "square", "triangle", "rectangle"]),
                    dimension=f"radius {random.randint(1, 10)}",
                    percentage=random.randint(1, 100),
                    number=random.randint(10, 1000)
                )
            elif grade_level <= 8:  # Middle
                template = random.choice(question_templates["Mathematics"]["middle"])
                question_text = template.format(
                    num1=random.randint(1, 10),
                    num2=random.randint(1, 20),
                    num3=random.randint(10, 50),
                    shape=random.choice(["circle", "square", "triangle"]),
                    dimension=f"side {random.randint(1, 10)}",
                    percentage=random.randint(1, 100),
                    number=random.randint(10, 1000),
                    expression=f"{random.randint(2,5)}x + {random.randint(1,10)}"
                )
            else:  # High school
                template = random.choice(question_templates["Mathematics"]["high"])
                question_text = template.format(
                    function=random.choice(["x²", "sin(x)", "cos(x)", "e^x"]),
                    num1=random.randint(1, 5),
                    equation=f"x² + {random.randint(1,5)}x + {random.randint(1,10)} = 0"
                )
        else:
            # Generic question for other subjects
            question_text = f"Grade {grade_level} {subject} question about {topic}: What is the correct answer to this {subject.lower()} problem?"
        
        questions.append({
            "id": i + 1,
            "text": question_text,
            "options": [
                f"Option A - Answer choice 1",
                f"Option B - Answer choice 2", 
                f"Option C - Answer choice 3",
                f"Option D - Answer choice 4"
            ],
            "correctAnswer": random.randint(0, 3),
            "explanation": f"This is the detailed explanation for the {subject} question about {topic} at grade level {grade_level}.",
            "difficulty": "Easy" if grade_level <= 5 else "Medium" if grade_level <= 8 else "Hard"
        })
    
    return questions

@app.route('/')
def home():
    """Home endpoint - returns API information"""
    return jsonify({
        "message": "Ideolix Learning Hub API",
        "version": "2.0.0",
        "curricula": list(CURRICULA_DATA.keys()),
        "endpoints": {
            "GET /": "API information",
            "POST /api/subjects": "Get subjects by curriculum and grade",
            "POST /api/topics": "Get topics by subject and curriculum",
            "POST /api/questions": "Get questions for practice/assessment",
            "GET /api/health": "Health check",
            "GET /api/curricula": "Get all available curricula"
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "curricula_count": len(CURRICULA_DATA)
    })

@app.route('/api/curricula')
def get_curricula():
    """Get all available curricula"""
    return jsonify({
        "success": True,
        "curricula": CURRICULA_DATA
    })

@app.route('/api/subjects', methods=['POST'])
def get_subjects():
    """Get subjects based on curriculum and grade level"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        curriculum = data.get('curriculum', 'nigeria')
        grade = data.get('grade', 10)
        
        if curriculum not in CURRICULA_DATA:
            return jsonify({"error": f"Curriculum '{curriculum}' not found. Available: {list(CURRICULA_DATA.keys())}"}), 400
        
        curriculum_info = CURRICULA_DATA[curriculum]
        
        # Determine grade level category
        grade_categories = curriculum_info["grades"]
        grade_category = None
        for category, grades in grade_categories.items():
            if str(grade) in [g.split()[-1] for g in grades]:
                grade_category = category
                break
        
        if not grade_category:
            grade_category = "core"  # Default category
        
        # Get appropriate subjects for grade level
        if grade_category in curriculum_info["subjects"]:
            subjects = curriculum_info["subjects"][grade_category]
        else:
            subjects = curriculum_info["subjects"]["core"]
        
        return jsonify({
            "success": True,
            "curriculum": curriculum,
            "curriculum_name": curriculum_info["name"],
            "grade": grade,
            "grade_category": grade_category,
            "subjects": subjects
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/topics', methods=['POST'])
def get_topics():
    """Get topics for a specific subject and curriculum"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        subject = data.get('subject')
        curriculum = data.get('curriculum', 'nigeria')
        grade = data.get('grade', 10)
        
        if not subject:
            return jsonify({"error": "Subject parameter is required"}), 400
        
        if subject not in TOPICS_DATA:
            # Generate generic topics if subject not found
            topics = [
                {"id": f"{subject.lower()}-1", "name": f"{subject} Fundamentals", "icon": "fa-book"},
                {"id": f"{subject.lower()}-2", "name": f"{subject} Principles", "icon": "fa-book"},
                {"id": f"{subject.lower()}-3", "name": f"{subject} Applications", "icon": "fa-book"},
                {"id": f"{subject.lower()}-4", "name": f"{subject} Theory", "icon": "fa-book"},
                {"id": f"{subject.lower()}-5", "name": f"{subject} Practice", "icon": "fa-book"}
            ]
        else:
            topics = TOPICS_DATA[subject]
        
        return jsonify({
            "success": True,
            "subject": subject,
            "curriculum": curriculum,
            "grade": grade,
            "topics": topics,
            "total_topics": len(topics)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/questions', methods=['POST'])
def get_questions():
    """Get questions for practice or assessment with grade-appropriate content"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        subject = data.get('subject')
        topic = data.get('topic')
        exam_type = data.get('examType', 'practice')
        curriculum = data.get('curriculum', 'nigeria')
        grade = data.get('grade', 10)
        count = data.get('count', 30)
        
        if not subject or not topic:
            return jsonify({"error": "Subject and topic parameters are required"}), 400
        
        # Generate grade-appropriate questions
        questions = generate_questions_by_grade(subject, topic, grade, count)
        
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
        return jsonify({"error": str(e)}), 500

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "Ideolix Learning Hub API is working!",
        "method": request.method,
        "timestamp": datetime.now().isoformat(),
        "curricula_available": list(CURRICULA_DATA.keys()),
        "subjects_available": list(TOPICS_DATA.keys())
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Ideolix Learning Hub API Server...")
    print("📚 Available Curricula:", list(CURRICULA_DATA.keys()))
    print("🔢 Grades: 1-12 with proper naming conventions")
    print("📖 Subjects:", len(TOPICS_DATA), "subjects with 15+ topics each")
    print("\n🌐 Available endpoints:")
    print("  GET  / - API information")
    print("  GET  /api/health - Health check") 
    print("  GET  /api/curricula - Get all curricula")
    print("  POST /api/subjects - Get subjects by curriculum and grade")
    print("  POST /api/topics - Get topics by subject and curriculum")
    print("  POST /api/questions - Get grade-appropriate questions")
    print("  GET  /api/test - Test endpoint")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
