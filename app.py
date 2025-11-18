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

# Comprehensive topics for each subject
TOPICS_DATA = {
    # Mathematics topics
    "Mathematics": [
        {"id": "number-theory", "name": "Number Theory", "icon": "fa-hashtag"},
        {"id": "algebra-basics", "name": "Algebra Basics", "icon": "fa-superscript"},
        {"id": "linear-equations", "name": "Linear Equations", "icon": "fa-equals"},
        {"id": "quadratic-equations", "name": "Quadratic Equations", "icon": "fa-project-diagram"},
        {"id": "geometry", "name": "Geometry", "icon": "fa-shapes"},
        {"id": "trigonometry", "name": "Trigonometry", "icon": "fa-calculator"},
        {"id": "calculus", "name": "Calculus", "icon": "fa-infinity"},
        {"id": "statistics", "name": "Statistics", "icon": "fa-chart-bar"},
        {"id": "probability", "name": "Probability", "icon": "fa-dice"},
        {"id": "functions", "name": "Functions", "icon": "fa-project-diagram"}
    ],
    
    # Physics topics
    "Physics": [
        {"id": "mechanics", "name": "Mechanics", "icon": "fa-cogs"},
        {"id": "kinematics", "name": "Kinematics", "icon": "fa-running"},
        {"id": "energy-work", "name": "Energy & Work", "icon": "fa-bolt"},
        {"id": "thermodynamics", "name": "Thermodynamics", "icon": "fa-temperature-high"},
        {"id": "waves", "name": "Waves", "icon": "fa-wave-square"},
        {"id": "optics", "name": "Optics", "icon": "fa-lightbulb"},
        {"id": "electricity", "name": "Electricity", "icon": "fa-bolt"},
        {"id": "magnetism", "name": "Magnetism", "icon": "fa-magnet"},
        {"id": "modern-physics", "name": "Modern Physics", "icon": "fa-atom"},
        {"id": "nuclear-physics", "name": "Nuclear Physics", "icon": "fa-radiation"}
    ],
    
    # Chemistry topics
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
        {"id": "chemical-kinetics", "name": "Chemical Kinetics", "icon": "fa-clock"}
    ],
    
    # Biology topics
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
        {"id": "microbiology", "name": "Microbiology", "icon": "fa-bacteria"}
    ],
    
    # English Language topics
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
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"}
    ],
    
    "English Language": [
        {"id": "grammar", "name": "Grammar", "icon": "fa-pen"},
        {"id": "vocabulary", "name": "Vocabulary", "icon": "fa-book"},
        {"id": "reading-comprehension", "name": "Reading Comprehension", "icon": "fa-book-reader"},
        {"id": "writing-skills", "name": "Writing Skills", "icon": "fa-edit"},
        {"id": "essay-writing", "name": "Essay Writing", "icon": "fa-file-alt"},
        {"id": "speaking-skills", "name": "Speaking Skills", "icon": "fa-microphone"},
        {"id": "listening-skills", "name": "Listening Skills", "icon": "fa-headphones"},
        {"id": "literary-devices", "name": "Literary Devices", "icon": "fa-quote-right"},
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"},
        {"id": "summary-writing", "name": "Summary Writing", "icon": "fa-file-contract"}
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
        {"id": "literary-analysis", "name": "Literary Analysis", "icon": "fa-search"}
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
        {"id": "critical-analysis", "name": "Critical Analysis", "icon": "fa-search"}
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
        {"id": "human-body", "name": "Human Body", "icon": "fa-heart"}
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
        {"id": "sustainable-development", "name": "Sustainable Development", "icon": "fa-leaf"}
    ]

# Add topics for other subjects
for subject in ["Further Mathematics", "Additional Mathematics", "Calculus"]:
    TOPICS_DATA[subject] = [
        {"id": "advanced-algebra", "name": "Advanced Algebra", "icon": "fa-superscript"},
        {"id": "calculus", "name": "Calculus", "icon": "fa-infinity"},
        {"id": "vectors", "name": "Vectors", "icon": "fa-arrow-right"},
        {"id": "matrices", "name": "Matrices", "icon": "fa-table"},
        {"id": "complex-numbers", "name": "Complex Numbers", "icon": "fa-square-root-alt"},
        {"id": "differential-equations", "name": "Differential Equations", "icon": "fa-equals"},
        {"id": "numerical-methods", "name": "Numerical Methods", "icon": "fa-calculator"},
        {"id": "probability-advanced", "name": "Probability", "icon": "fa-dice"},
        {"id": "statistics-advanced", "name": "Statistics", "icon": "fa-chart-bar"},
        {"id": "mechanics-math", "name": "Mechanics", "icon": "fa-cogs"}
    ]

for subject in ["Economics", "Business Management", "Commerce"]:
    TOPICS_DATA[subject] = [
        {"id": "microeconomics", "name": "Microeconomics", "icon": "fa-chart-line"},
        {"id": "macroeconomics", "name": "Macroeconomics", "icon": "fa-chart-bar"},
        {"id": "market-structures", "name": "Market Structures", "icon": "fa-store"},
        {"id": "supply-demand", "name": "Supply & Demand", "icon": "fa-balance-scale"},
        {"id": "international-trade", "name": "International Trade", "icon": "fa-globe"},
        {"id": "business-organization", "name": "Business Organization", "icon": "fa-briefcase"},
        {"id": "marketing", "name": "Marketing", "icon": "fa-bullhorn"},
        {"id": "finance", "name": "Finance", "icon": "fa-money-bill-wave"},
        {"id": "accounting", "name": "Accounting", "icon": "fa-calculator"},
        {"id": "entrepreneurship", "name": "Entrepreneurship", "icon": "fa-lightbulb"}
    ]

for subject in ["Geography", "US History"]:
    TOPICS_DATA[subject] = [
        {"id": "physical-geography", "name": "Physical Geography", "icon": "fa-mountain"},
        {"id": "human-geography", "name": "Human Geography", "icon": "fa-users"},
        {"id": "climate", "name": "Climate", "icon": "fa-cloud"},
        {"id": "population", "name": "Population", "icon": "fa-user-friends"},
        {"id": "economic-geography", "name": "Economic Geography", "icon": "fa-industry"},
        {"id": "historical-events", "name": "Historical Events", "icon": "fa-monument"},
        {"id": "cultural-geography", "name": "Cultural Geography", "icon": "fa-globe-americas"},
        {"id": "political-geography", "name": "Political Geography", "icon": "fa-flag"},
        {"id": "urban-geography", "name": "Urban Geography", "icon": "fa-city"},
        {"id": "environmental-geography", "name": "Environmental Geography", "icon": "fa-tree"}
    ]

for subject in ["Computer Science"]:
    TOPICS_DATA[subject] = [
        {"id": "programming-basics", "name": "Programming Basics", "icon": "fa-code"},
        {"id": "algorithms", "name": "Algorithms", "icon": "fa-project-diagram"},
        {"id": "data-structures", "name": "Data Structures", "icon": "fa-database"},
        {"id": "web-development", "name": "Web Development", "icon": "fa-laptop-code"},
        {"id": "databases", "name": "Databases", "icon": "fa-server"},
        {"id": "networking", "name": "Networking", "icon": "fa-network-wired"},
        {"id": "cybersecurity", "name": "Cybersecurity", "icon": "fa-shield-alt"},
        {"id": "artificial-intelligence", "name": "Artificial Intelligence", "icon": "fa-robot"},
        {"id": "software-engineering", "name": "Software Engineering", "icon": "fa-cogs"},
        {"id": "mobile-development", "name": "Mobile Development", "icon": "fa-mobile-alt"}
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
                f"{{num1}} ÷ {{num2}} = ?",
                f"What is the area of a square with side {{num1}}?",
                f"Calculate the perimeter of a rectangle with length {{num1}} and width {{num2}}"
            ],
            "middle": [
                f"Solve for x: {{num1}}x + {{num2}} = {{num3}}",
                f"Calculate the area of a circle with radius {{num1}}",
                f"What is {{percentage}}% of {{number}}?",
                f"Simplify: {{expression}}",
                f"Factorize: x² + {{num1}}x + {{num2}}",
                f"Solve the equation: {{num1}}x - {{num2}} = {{num3}}"
            ],
            "high": [
                f"Differentiate {{function}} with respect to x",
                f"Integrate {{function}} dx",
                f"Solve the quadratic equation: {{equation}}",
                f"Find the limit: lim(x→{{num1}}) {{function}}",
                f"Calculate the derivative of {{function}} at x = {{num1}}",
                f"Solve the system of equations: {{system}}"
            ]
        },
        "Physics": {
            "elementary": [
                f"What is the unit of {{quantity}}?",
                f"Which force pulls objects toward Earth?",
                f"What type of energy does a moving object have?",
                f"Name one source of {{energy_type}} energy",
                f"What is the speed of light?",
                f"Which law states that every action has an equal and opposite reaction?"
            ],
            "middle": [
                f"Calculate the velocity of an object moving {{distance}}m in {{time}}s",
                f"What is the acceleration due to gravity on Earth?",
                f"Explain {{concept}} in physics",
                f"Solve this force problem: {{scenario}}",
                f"Calculate the work done when a force of {{num1}}N moves an object {{num2}}m",
                f"What is the power if {{work}}J of work is done in {{time}}s?"
            ],
            "high": [
                f"Apply Newton's {{law_number}} law to {{situation}}",
                f"Calculate the work done when {{scenario}}",
                f"Solve this kinematics equation: {{equation}}",
                f"Explain the principle of {{advanced_concept}}",
                f"Calculate the electric field strength at a point {{distance}}m from a charge",
                f"Solve this thermodynamics problem: {{problem}}"
            ]
        },
        "Chemistry": {
            "elementary": [
                f"What is the chemical symbol for {{element}}?",
                f"How many electrons does {{element}} have?",
                f"What is the pH of a neutral solution?",
                f"Name the three states of matter",
                f"What is the atomic number of {{element}}?",
                f"Which gas do plants use for photosynthesis?"
            ],
            "middle": [
                f"Balance this chemical equation: {{equation}}",
                f"Calculate the molar mass of {{compound}}",
                f"Explain the difference between elements and compounds",
                f"What is the concentration if {{mass}}g is dissolved in {{volume}}L?",
                f"Name the type of reaction: {{reaction}}",
                f"Calculate the number of moles in {{mass}}g of {{substance}}"
            ],
            "high": [
                f"Explain the concept of {{advanced_concept}} in chemistry",
                f"Calculate the pH of a {{concentration}}M {{acid_base}} solution",
                f"Solve this stoichiometry problem: {{problem}}",
                f"Describe the mechanism of {{reaction_type}} reaction",
                f"Calculate the equilibrium constant for {{reaction}}",
                f"Explain the principles of {{analytical_technique}}"
            ]
        }
    }
    
    # Generate questions based on grade level and subject
    for i in range(count):
        if subject in question_templates:
            if grade_level <= 5:  # Elementary
                level = "elementary"
                template = random.choice(question_templates[subject][level])
            elif grade_level <= 8:  # Middle
                level = "middle"
                template = random.choice(question_templates[subject][level])
            else:  # High school
                level = "high"
                template = random.choice(question_templates[subject][level])
            
            # Fill template with appropriate values
            if subject == "Mathematics":
                if level == "elementary":
                    question_text = template.format(
                        num1=random.randint(1, 100),
                        num2=random.randint(1, 50),
                        num3=random.randint(10, 200)
                    )
                elif level == "middle":
                    question_text = template.format(
                        num1=random.randint(1, 10),
                        num2=random.randint(1, 20),
                        num3=random.randint(10, 50),
                        percentage=random.randint(1, 100),
                        number=random.randint(10, 1000),
                        expression=f"{random.randint(2,5)}x + {random.randint(1,10)}"
                    )
                else:  # high
                    question_text = template.format(
                        function=random.choice(["x²", "sin(x)", "cos(x)", "e^x", "ln(x)"]),
                        num1=random.randint(1, 5),
                        equation=f"x² + {random.randint(1,5)}x + {random.randint(1,10)} = 0",
                        system=f"{random.randint(1,3)}x + {random.randint(1,3)}y = {random.randint(5,15)}"
                    )
            else:
                # Generic question for other subjects
                question_text = template.format(
                    quantity=random.choice(["force", "energy", "velocity", "acceleration"]),
                    energy_type=random.choice(["renewable", "non-renewable", "kinetic", "potential"]),
                    distance=random.randint(10, 100),
                    time=random.randint(1, 10),
                    concept=random.choice(["gravity", "friction", "momentum", "energy conservation"]),
                    scenario=f"a {random.randint(1,10)}kg object",
                    law_number=random.randint(1, 3),
                    situation=random.choice(["a car accelerating", "a rocket launching", "a ball falling"]),
                    advanced_concept=random.choice(["quantum mechanics", "relativity", "thermodynamics"]),
                    element=random.choice(["Oxygen", "Hydrogen", "Carbon", "Nitrogen"]),
                    compound=random.choice(["H2O", "CO2", "NaCl", "CH4"]),
                    mass=random.randint(1, 100),
                    volume=random.randint(1, 10),
                    reaction=random.choice(["combustion", "synthesis", "decomposition"]),
                    acid_base=random.choice(["HCl", "NaOH", "H2SO4"]),
                    concentration=round(random.uniform(0.01, 1.0), 2),
                    reaction_type=random.choice(["SN1", "SN2", "E1", "E2"]),
                    analytical_technique=random.choice(["chromatography", "spectroscopy", "titration"]),
                    work=random.randint(100, 1000),
                    problem=random.choice(["heating curve", "reaction kinetics", "equilibrium"]),
                    distance=random.randint(1, 10)
                )
        else:
            # Generic question for subjects not in templates
            question_text = f"Grade {grade_level} {subject} question about {topic}: What is the correct answer to this {subject.lower()} problem?"
        
        # Generate realistic options
        options = [
            f"Option A - Correct answer for {subject}",
            f"Option B - Alternative answer 1", 
            f"Option C - Alternative answer 2",
            f"Option D - Alternative answer 3"
        ]
        
        # Shuffle options but remember correct answer
        correct_index = random.randint(0, 3)
        
        questions.append({
            "id": i + 1,
            "text": question_text,
            "options": options,
            "correctAnswer": correct_index,
            "explanation": f"This is the detailed explanation for the {subject} question about {topic} at grade level {grade_level}. The correct answer is {options[correct_index]} because...",
            "difficulty": "Easy" if grade_level <= 5 else "Medium" if grade_level <= 8 else "Hard"
        })
    
    return questions

@app.route('/')
def home():
    """Home endpoint - returns API information"""
    return jsonify({
        "message": "Ideolix Learning Hub API",
        "version": "2.1.0",
        "curricula": list(CURRICULA_DATA.keys()),
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "API information",
            "POST /api/subjects": "Get subjects by curriculum and grade",
            "POST /api/topics": "Get topics by subject and curriculum",
            "POST /api/questions": "Get questions for practice/assessment",
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
        "version": "2.1.0",
        "curricula_count": len(CURRICULA_DATA),
        "subjects_count": len(TOPICS_DATA),
        "message": "Ideolix Learning Hub API is running smoothly"
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
    """Get topics for a specific subject and curriculum"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        subject = data.get('subject')
        curriculum = data.get('curriculum', 'nigeria')
        grade = data.get('grade', 10)
        
        if not subject:
            return jsonify({
                "success": False,
                "error": "Subject parameter is required"
            }), 400
        
        print(f"📥 Received topics request: subject={subject}, curriculum={curriculum}, grade={grade}")
        
        # Get topics for the subject
        if subject in TOPICS_DATA:
            topics = TOPICS_DATA[subject]
        else:
            # Generate generic topics if subject not found
            topics = [
                {"id": f"{subject.lower()}-1", "name": f"{subject} Fundamentals", "icon": "fa-book"},
                {"id": f"{subject.lower()}-2", "name": f"{subject} Principles", "icon": "fa-book"},
                {"id": f"{subject.lower()}-3", "name": f"{subject} Applications", "icon": "fa-book"},
                {"id": f"{subject.lower()}-4", "name": f"{subject} Theory", "icon": "fa-book"},
                {"id": f"{subject.lower()}-5", "name": f"{subject} Practice", "icon": "fa-book"}
            ]
        
        print(f"📤 Sending response: {len(topics)} topics for {subject}")
        
        return jsonify({
            "success": True,
            "subject": subject,
            "curriculum": curriculum,
            "grade": grade,
            "topics": topics,
            "total_topics": len(topics)
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
    
    topics = TOPICS_DATA.get(subject, [
        {"id": "topic-1", "name": f"{subject} Fundamentals", "icon": "fa-book"},
        {"id": "topic-2", "name": f"{subject} Principles", "icon": "fa-book"},
        {"id": "topic-3", "name": f"{subject} Applications", "icon": "fa-book"}
    ])
    
    return jsonify({
        "success": True,
        "subject": subject,
        "topics": topics,
        "total_topics": len(topics)
    })

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "Ideolix Learning Hub API is working!",
        "method": request.method,
        "timestamp": datetime.now().isoformat(),
        "curricula_available": list(CURRICULA_DATA.keys()),
        "subjects_available": list(TOPICS_DATA.keys())[:10]  # First 10 subjects
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
    print("\n🌐 Available endpoints:")
    print("  GET  / - API information")
    print("  GET  /api/health - Health check") 
    print("  GET  /api/curricula - Get all curricula")
    print("  POST /api/subjects - Get subjects by curriculum and grade")
    print("  POST /api/topics - Get topics by subject and curriculum")
    print("  POST /api/questions - Get grade-appropriate questions")
    print("  GET  /api/debug/subjects - Debug endpoint for subjects")
    print("  GET  /api/debug/topics - Debug endpoint for topics")
    print("  GET  /api/test - Test endpoint")
    print(f"\n⏰ Server started at: {datetime.now().isoformat()}")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
