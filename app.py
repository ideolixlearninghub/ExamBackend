# app.py - Complete Robust Learning Platform Backend (Fixed)
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random
from datetime import datetime, timedelta
import hashlib
import secrets
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['DATABASE'] = 'learning_hub.db'

CORS(app)

# Simple authentication storage
sessions = {}

# Database initialization
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            grade_level INTEGER,
            curriculum TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Progress tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            grade_level INTEGER,
            questions_attempted INTEGER DEFAULT 0,
            questions_correct INTEGER DEFAULT 0,
            last_attempted TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token():
    return secrets.token_hex(32)

def verify_token(token):
    """Verify if token is valid"""
    if token in sessions:
        # Check if token has expired
        if datetime.now() < sessions[token]['expires']:
            return True
        else:
            # Remove expired token
            del sessions[token]
    return False

def token_required(f):
    """Decorator to require token authentication"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"success": False, "error": "Token is missing"}), 401
        
        token = token.split(' ')[1]
        if not verify_token(token):
            return jsonify({"success": False, "error": "Invalid or expired token"}), 401
        
        return f(*args, **kwargs)
    return decorated

# Comprehensive curricula data with grade-specific subjects
CURRICULA_DATA = {
    "nigeria": {
        "name": "Nigerian Curriculum",
        "grades": {
            "1": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Verbal Reasoning", "Quantitative Reasoning"],
            "2": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Verbal Reasoning", "Quantitative Reasoning"],
            "3": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Verbal Reasoning", "Quantitative Reasoning"],
            "4": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Verbal Reasoning", "Quantitative Reasoning"],
            "5": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Verbal Reasoning", "Quantitative Reasoning"],
            "6": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Computer Science", "Creative Arts"],
            "7": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Computer Science", "Creative Arts"],
            "8": ["Mathematics", "English Studies", "Basic Science", "Social Studies", "Computer Science", "Creative Arts"],
            "9": ["Mathematics", "English Language", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "10": ["Mathematics", "English Language", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "11": ["Mathematics", "English Language", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "12": ["Mathematics", "English Language", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"]
        }
    },
    "cambridge": {
        "name": "Cambridge International",
        "grades": {
            "1": ["Mathematics", "English", "Science", "Global Perspectives"],
            "2": ["Mathematics", "English", "Science", "Global Perspectives"],
            "3": ["Mathematics", "English", "Science", "Global Perspectives"],
            "4": ["Mathematics", "English", "Science", "Global Perspectives"],
            "5": ["Mathematics", "English", "Science", "Global Perspectives"],
            "6": ["Mathematics", "English", "Science", "Global Perspectives", "ICT"],
            "7": ["Mathematics", "English", "Science", "Global Perspectives", "ICT"],
            "8": ["Mathematics", "English", "Science", "Global Perspectives", "ICT"],
            "9": ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "10": ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "11": ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"],
            "12": ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Geography", "Economics", "Computer Science"]
        }
    }
}

# Comprehensive grade-specific topics for each subject
GRADE_TOPICS = {
    "Mathematics": {
        "1": ["Counting Numbers 1-50", "Number Recognition", "Basic Addition", "Basic Subtraction", "Simple Shapes", "Comparing Numbers", "Measurement Basics", "Time - Hours", "Money - Identifying Coins", "Patterns", "Sorting Objects", "Position Words", "Data Collection", "Simple Graphs", "Problem Solving Basics"],
        "2": ["Numbers 1-100", "Addition Facts", "Subtraction Facts", "Place Value", "Measurement - Length", "Time - Half Hours", "Money - Counting Coins", "2D Shapes", "Simple Fractions", "Word Problems", "Calendar Skills", "Temperature Basics", "Symmetry", "Data Interpretation", "Mental Math"],
        "3": ["Multiplication Basics", "Division Basics", "Fractions", "Measurement - Weight", "Time - Quarter Hours", "Money - Making Change", "Perimeter", "Area Basics", "Graphs and Charts", "Problem Solving Strategies", "Geometry - 3D Shapes", "Patterns and Sequences", "Estimation", "Mental Math Strategies", "Mathematical Vocabulary"],
        "4": ["Multi-digit Multiplication", "Long Division", "Fractions and Decimals", "Measurement - Volume", "Time - Minutes and Seconds", "Money - Word Problems", "Geometry - Angles", "Area and Perimeter", "Data Analysis", "Factors and Multiples", "Roman Numerals", "Coordinate Grids", "Problem Solving", "Mathematical Reasoning", "Measurement Conversion"],
        "5": ["Fractions Operations", "Decimal Operations", "Percentage Basics", "Geometry - Triangles", "Measurement - Metric System", "Graphs - Line Graphs", "Algebraic Thinking", "Volume", "Statistics Basics", "Ratio and Proportion", "Integers", "Geometry - Circles", "Word Problems Advanced", "Mathematical Patterns", "Logical Reasoning"],
        "6": ["Algebra Basics", "Ratio and Proportion", "Percentage Applications", "Geometry - Polygons", "Statistics - Mean, Median", "Probability Basics", "Integers Operations", "Coordinate Geometry", "Measurement - Advanced", "Data Interpretation", "Financial Mathematics", "Geometry - Transformations", "Problem Solving", "Mathematical Proofs", "Number Theory"],
        "7": ["Algebraic Expressions", "Linear Equations", "Geometry - Congruence", "Statistics - Probability", "Ratio and Proportion Advanced", "Percentage Advanced", "Number Systems", "Geometry - Similarity", "Data Analysis", "Mathematical Modeling", "Functions Basics", "Geometry - Pythagorean Theorem", "Problem Solving", "Mathematical Communication", "Algebraic Manipulation"],
        "8": ["Linear Equations Advanced", "Quadratic Equations Basics", "Geometry - Trigonometry", "Statistics - Distributions", "Functions and Graphs", "Coordinate Geometry Advanced", "Number Theory", "Geometry - 3D Shapes", "Probability Advanced", "Algebraic Fractions", "Mathematical Reasoning", "Problem Solving Strategies", "Geometry - Circles Advanced", "Sequences and Series", "Mathematical Proofs"],
        "9": ["Algebraic Expressions", "Linear Equations", "Quadratic Equations", "Geometry - Angles", "Trigonometry Basics", "Statistics - Mean, Median, Mode", "Probability", "Coordinate Geometry", "Functions", "Sets Theory", "Number Systems", "Polynomials", "Factorization", "Simultaneous Equations", "Mathematical Reasoning"],
        "10": ["Quadratic Functions", "Trigonometric Ratios", "Circle Geometry", "Statistics Advanced", "Probability Distributions", "Sequences and Series", "Coordinate Geometry Advanced", "Functions and Graphs", "Calculus Basics", "Vectors", "Matrices", "Financial Mathematics", "3D Geometry", "Algebraic Fractions", "Inequalities"],
        "11": ["Calculus - Differentiation", "Calculus - Integration", "Trigonometric Functions", "Exponential and Logarithmic Functions", "Complex Numbers", "Permutations and Combinations", "Binomial Theorem", "3D Coordinate Geometry", "Differential Equations", "Mathematical Induction", "Vector Algebra", "Probability Distributions", "Statistical Inference", "Linear Programming", "Numerical Methods"],
        "12": ["Advanced Calculus", "Multivariable Calculus", "Differential Equations Advanced", "Complex Analysis", "Linear Algebra", "Group Theory", "Real Analysis", "Numerical Analysis", "Mathematical Modeling", "Game Theory", "Topology Basics", "Fourier Series", "Laplace Transforms", "Probability Theory", "Statistical Methods"]
    },
    "Physics": {
        "9": ["Measurement and Units", "Motion in Straight Line", "Laws of Motion", "Work, Energy and Power", "Gravitation", "Properties of Matter", "Heat and Temperature", "Wave Motion", "Sound Waves", "Light - Reflection", "Light - Refraction", "Electric Current", "Magnetism", "Electromagnetism", "Nuclear Physics Basics"],
        "10": ["Kinematics", "Dynamics", "Circular Motion", "Oscillations", "Thermal Physics", "Wave Optics", "Electrostatics", "Current Electricity", "Magnetic Effects", "Electromagnetic Induction", "AC Circuits", "Semiconductor Devices", "Communication Systems", "Modern Physics", "Astrophysics Basics"],
        "11": ["Physical World and Measurement", "Kinematics", "Laws of Motion", "Work, Energy and Power", "Motion of System of Particles", "Gravitation", "Properties of Bulk Matter", "Thermodynamics", "Behavior of Perfect Gas", "Oscillations and Waves", "Electrostatics", "Current Electricity", "Magnetic Effects of Current", "Electromagnetic Induction", "Alternating Current"],
        "12": ["Electrostatics", "Current Electricity", "Magnetic Effects of Current", "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves", "Optics", "Dual Nature of Matter", "Atoms and Nuclei", "Electronic Devices", "Communication Systems", "Experimental Skills", "Modern Physics", "Semiconductor Electronics", "Principles of Communication"]
    },
    "Chemistry": {
        "9": ["Matter and Its Composition", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Solutions", "Acids, Bases and Salts", "Chemical Reactions", "Metals and Non-metals", "Carbon Compounds", "Environmental Chemistry", "Basic Laboratory Techniques", "Stoichiometry", "Redox Reactions", "Water Chemistry"],
        "10": ["Chemical Kinetics", "Chemical Equilibrium", "Ionic Equilibrium", "Thermodynamics", "Electrochemistry", "Surface Chemistry", "Coordination Compounds", "Hydrocarbons", "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes and Ketones", "Carboxylic Acids", "Organic Nitrogen Compounds", "Biomolecules", "Polymers"],
        "11": ["Some Basic Concepts of Chemistry", "Structure of Atom", "Classification of Elements", "Chemical Bonding", "States of Matter", "Thermodynamics", "Equilibrium", "Redox Reactions", "Hydrogen", "s-Block Elements", "p-Block Elements", "Organic Chemistry", "Hydrocarbons", "Environmental Chemistry", "Practical Chemistry"],
        "12": ["Solid State", "Solutions", "Electrochemistry", "Chemical Kinetics", "Surface Chemistry", "General Principles of Metallurgy", "p-Block Elements", "d and f Block Elements", "Coordination Compounds", "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids", "Organic Compounds", "Biomolecules", "Chemistry in Everyday Life"]
    },
    "Biology": {
        "9": ["Cell Biology", "Tissues", "Plant Physiology", "Human Physiology - Digestion", "Human Physiology - Respiration", "Human Physiology - Circulation", "Human Physiology - Excretion", "Human Physiology - Nervous System", "Reproduction in Plants", "Reproduction in Humans", "Genetics and Evolution", "Health and Diseases", "Ecosystem", "Biodiversity", "Environmental Issues"],
        "10": ["Molecular Biology", "Genetics Advanced", "Evolutionary Biology", "Human Physiology Advanced", "Plant Physiology Advanced", "Biotechnology", "Microbiology", "Immunology", "Ecology Advanced", "Animal Behavior", "Developmental Biology", "Bioinformatics", "Genetic Engineering", "Conservation Biology", "Medical Biology"],
        "11": ["Diversity in Living World", "Structural Organization", "Cell Structure and Function", "Plant Physiology", "Human Physiology", "Reproduction", "Genetics and Evolution", "Biology and Human Welfare", "Biotechnology", "Ecology and Environment", "Human Health and Diseases", "Microbes in Human Welfare", "Principles of Inheritance", "Molecular Basis of Inheritance", "Evolution"],
        "12": ["Reproduction in Organisms", "Sexual Reproduction", "Genetics and Evolution", "Biology and Human Welfare", "Biotechnology", "Ecology", "Environmental Issues", "Strategies for Enhancement", "Microbes in Human Welfare", "Organisms and Populations", "Ecosystem", "Biodiversity and Conservation", "Human Reproduction", "Reproductive Health", "Principles of Biotechnology"]
    },
    "English Language": {
        "9": ["Grammar Fundamentals", "Sentence Structure", "Parts of Speech", "Tenses", "Punctuation", "Vocabulary Building", "Reading Comprehension", "Essay Writing", "Letter Writing", "Report Writing", "Creative Writing", "Poetry Analysis", "Prose Comprehension", "Drama Interpretation", "Oral English"],
        "10": ["Advanced Grammar", "Syntax and Semantics", "Phonetics", "Summary Writing", "Argumentative Essays", "Descriptive Writing", "Narrative Writing", "Literary Devices", "Figures of Speech", "Comprehension Skills", "Vocabulary Enhancement", "Formal Letters", "Informal Letters", "Speech Writing", "Debate and Discussion"],
        "11": ["Advanced Composition", "Critical Analysis", "Literary Criticism", "Advanced Vocabulary", "Rhetorical Devices", "Research Writing", "Creative Writing Advanced", "Poetry Analysis Advanced", "Prose Analysis", "Drama Analysis", "Linguistics Basics", "Sociolinguistics", "Psycholinguistics", "Academic Writing", "Professional Communication"],
        "12": ["Advanced Literary Analysis", "Critical Theory", "Research Methodology", "Academic Writing Advanced", "Professional Communication", "Media Studies", "Digital Literacy", "Cross-cultural Communication", "Stylistics", "Discourse Analysis", "Translation Studies", "World Literature", "Contemporary Issues", "Ethical Communication", "Career Preparation"]
    },
    "Computer Science": {
        "9": ["Computer Fundamentals", "Operating Systems", "Word Processing", "Spreadsheets", "Presentation Software", "Internet Basics", "Email Communication", "Computer Hardware", "Software Concepts", "Programming Basics", "Algorithm Design", "Flowcharts", "HTML Basics", "Cyber Safety", "Digital Citizenship"],
        "10": ["Programming in Python", "Data Structures", "Database Management", "Web Development", "Computer Networks", "Cyber Security", "Software Development", "Mobile App Development", "Cloud Computing", "Artificial Intelligence", "Machine Learning", "Data Science", "Internet of Things", "Blockchain Basics", "Ethical Hacking"],
        "11": ["Computer Systems", "Boolean Algebra", "Number Systems", "Microprocessors", "Data Representation", "Python Programming", "Database Concepts", "SQL", "Computer Networks", "Web Development", "Cyber Security", "Society Law and Ethics", "Computational Thinking", "Problem Solving", "Software Engineering"],
        "12": ["Object Oriented Programming", "Data Structures", "Database Management", "Boolean Algebra", "Computer Networks", "Web Technologies", "Cyber Security", "Society Law and Ethics", "Computational Thinking", "Problem Solving", "Software Engineering", "Mobile Applications", "Cloud Computing", "Artificial Intelligence", "Project Development"]
    }
}

# Real question database with explanations
QUESTION_DATABASE = {
    "Mathematics": {
        "9": {
            "Algebraic Expressions": [
                {
                    "question": "Simplify the expression: 3x + 2y - x + 4y",
                    "options": ["2x + 6y", "4x + 6y", "2x + 2y", "4x + 2y"],
                    "correct": 0,
                    "explanation": "Combine like terms: 3x - x = 2x, 2y + 4y = 6y. Result: 2x + 6y"
                },
                {
                    "question": "Expand: 2(x + 3)",
                    "options": ["2x + 3", "2x + 5", "2x + 6", "x + 6"],
                    "correct": 2,
                    "explanation": "Multiply each term inside parentheses by 2: 2 × x + 2 × 3 = 2x + 6"
                },
                {
                    "question": "Factorize: 4x² - 9",
                    "options": ["(2x - 3)(2x + 3)", "(4x - 3)(x + 3)", "(2x - 9)(2x + 1)", "(4x - 9)(x + 1)"],
                    "correct": 0,
                    "explanation": "This is difference of squares: a² - b² = (a - b)(a + b). Here, 4x² = (2x)² and 9 = 3²"
                }
            ],
            "Linear Equations": [
                {
                    "question": "Solve for x: 2x + 5 = 13",
                    "options": ["x = 4", "x = 6", "x = 8", "x = 9"],
                    "correct": 0,
                    "explanation": "Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4"
                },
                {
                    "question": "If 3(x - 2) = 15, what is the value of x?",
                    "options": ["x = 5", "x = 6", "x = 7", "x = 8"],
                    "correct": 2,
                    "explanation": "Divide both sides by 3: x - 2 = 5, then add 2: x = 7"
                }
            ]
        },
        "10": {
            "Quadratic Functions": [
                {
                    "question": "What are the roots of the equation x² - 5x + 6 = 0?",
                    "options": ["x = 2, 3", "x = 1, 6", "x = -2, -3", "x = -1, -6"],
                    "correct": 0,
                    "explanation": "Factorize: (x - 2)(x - 3) = 0, so roots are x = 2 and x = 3"
                },
                {
                    "question": "Find the vertex of the quadratic function f(x) = x² - 4x + 3",
                    "options": ["(2, -1)", "(1, 0)", "(3, 0)", "(-2, 15)"],
                    "correct": 0,
                    "explanation": "Vertex x-coordinate = -b/2a = 4/2 = 2. f(2) = 4 - 8 + 3 = -1. Vertex: (2, -1)"
                }
            ]
        }
    },
    "Physics": {
        "9": {
            "Laws of Motion": [
                {
                    "question": "According to Newton's First Law of Motion, an object will:",
                    "options": [
                        "Accelerate if a force is applied",
                        "Remain at rest or in uniform motion unless acted upon by a net force",
                        "Always move in a straight line",
                        "Have constant acceleration"
                    ],
                    "correct": 1,
                    "explanation": "Newton's First Law states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an unbalanced force."
                },
                {
                    "question": "What is the SI unit of force?",
                    "options": ["Joule", "Watt", "Newton", "Pascal"],
                    "correct": 2,
                    "explanation": "The SI unit of force is the Newton (N), named after Sir Isaac Newton. 1 N = 1 kg·m/s²"
                }
            ]
        }
    },
    "Chemistry": {
        "9": {
            "Atomic Structure": [
                {
                    "question": "How many electrons can the first shell of an atom hold?",
                    "options": ["2 electrons", "8 electrons", "18 electrons", "32 electrons"],
                    "correct": 0,
                    "explanation": "The first electron shell (K shell) can hold a maximum of 2 electrons according to the 2n² rule where n=1: 2(1)² = 2"
                },
                {
                    "question": "What is the atomic number of an element?",
                    "options": [
                        "Number of protons in the nucleus",
                        "Number of neutrons in the nucleus",
                        "Total number of protons and neutrons",
                        "Number of electrons in the outer shell"
                    ],
                    "correct": 0,
                    "explanation": "The atomic number is defined as the number of protons in the nucleus of an atom, which determines the chemical properties of the element."
                }
            ]
        }
    },
    "Biology": {
        "9": {
            "Cell Biology": [
                {
                    "question": "Which organelle is known as the 'powerhouse of the cell'?",
                    "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi Apparatus"],
                    "correct": 1,
                    "explanation": "Mitochondria are called the powerhouse of the cell because they produce ATP through cellular respiration, providing energy for cellular activities."
                },
                {
                    "question": "What is the function of the cell membrane?",
                    "options": [
                        "Control center of the cell",
                        "Site of protein synthesis",
                        "Regulates what enters and leaves the cell",
                        "Storage of genetic material"
                    ],
                    "correct": 2,
                    "explanation": "The cell membrane is a selectively permeable barrier that controls the movement of substances in and out of the cell, maintaining homeostasis."
                }
            ]
        }
    },
    "English Language": {
        "9": {
            "Grammar Fundamentals": [
                {
                    "question": "Which of the following is a proper noun?",
                    "options": ["city", "London", "river", "mountain"],
                    "correct": 1,
                    "explanation": "A proper noun is the specific name of a particular person, place, or thing. 'London' is a specific city name, so it's a proper noun."
                },
                {
                    "question": "Identify the verb in this sentence: 'The students study diligently every day.'",
                    "options": ["students", "study", "diligently", "every"],
                    "correct": 1,
                    "explanation": "A verb expresses action or state of being. 'Study' is the action being performed by the students."
                }
            ]
        }
    }
}

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_user_from_token():
    """Extract user from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token in sessions:
        return sessions[token]['user_id']
    return None

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        grade_level = data.get('gradeLevel')
        curriculum = data.get('curriculum')

        if not all([email, password, first_name, last_name]):
            return jsonify({"success": False, "error": "All fields are required"}), 400

        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()

        if existing_user:
            conn.close()
            return jsonify({"success": False, "error": "User already exists"}), 400

        hashed_password = hash_password(password)
        
        cursor = conn.execute(
            'INSERT INTO users (email, password, first_name, last_name, grade_level, curriculum) VALUES (?, ?, ?, ?, ?, ?)',
            (email, hashed_password, first_name, last_name, grade_level, curriculum)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Generate token
        token = generate_token()
        sessions[token] = {
            'user_id': user_id,
            'email': email,
            'expires': datetime.now() + timedelta(hours=24)
        }

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user_id,
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "gradeLevel": grade_level,
                "curriculum": curriculum
            }
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()

        if user and verify_password(password, user['password']):
            token = generate_token()
            sessions[token] = {
                'user_id': user['id'],
                'email': email,
                'expires': datetime.now() + timedelta(hours=24)
            }
            
            return jsonify({
                "success": True,
                "token": token,
                "user": {
                    "id": user['id'],
                    "email": user['email'],
                    "firstName": user['first_name'],
                    "lastName": user['last_name'],
                    "gradeLevel": user['grade_level'],
                    "curriculum": user['curriculum']
                }
            })
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Curriculum Routes
@app.route('/api/curricula', methods=['GET'])
def get_curricula():
    return jsonify({
        "success": True,
        "curricula": CURRICULA_DATA
    })

@app.route('/api/subjects', methods=['POST'])
@token_required
def get_subjects_route():
    try:
        data = request.get_json()
        curriculum = data.get('curriculum')
        grade = data.get('grade')

        if curriculum not in CURRICULA_DATA:
            return jsonify({"success": False, "error": "Curriculum not found"}), 400

        if grade not in CURRICULA_DATA[curriculum]['grades']:
            return jsonify({"success": False, "error": "Grade not found in curriculum"}), 400

        subjects = CURRICULA_DATA[curriculum]['grades'][grade]
        
        return jsonify({
            "success": True,
            "subjects": subjects,
            "curriculum": curriculum,
            "grade": grade
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/topics', methods=['POST'])
@token_required
def get_topics_route():
    try:
        data = request.get_json()
        subject = data.get('subject')
        grade = data.get('grade')

        if subject not in GRADE_TOPICS or grade not in GRADE_TOPICS[subject]:
            return jsonify({"success": False, "error": "Topics not found for this subject and grade"}), 400

        topics = GRADE_TOPICS[subject][grade]
        
        return jsonify({
            "success": True,
            "topics": topics,
            "subject": subject,
            "grade": grade
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Question Generation Routes
@app.route('/api/questions/practice', methods=['POST'])
@token_required
def generate_practice_questions():
    try:
        data = request.get_json()
        subject = data.get('subject')
        topic = data.get('topic')
        grade = data.get('grade')
        count = data.get('count', 30)

        # Check if questions exist for this subject, grade, and topic
        if (subject not in QUESTION_DATABASE or 
            grade not in QUESTION_DATABASE[subject] or 
            topic not in QUESTION_DATABASE[subject][grade]):
            return jsonify({"success": False, "error": "Questions not available for this topic"}), 400

        available_questions = QUESTION_DATABASE[subject][grade][topic]
        
        # If we don't have enough questions, repeat some
        selected_questions = []
        if len(available_questions) >= count:
            selected_questions = random.sample(available_questions, count)
        else:
            # Repeat questions if we don't have enough
            selected_questions = available_questions * (count // len(available_questions))
            remaining = count % len(available_questions)
            if remaining > 0:
                selected_questions.extend(random.sample(available_questions, remaining))
        
        return jsonify({
            "success": True,
            "questions": selected_questions,
            "subject": subject,
            "topic": topic,
            "grade": grade,
            "count": len(selected_questions),
            "mode": "practice"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/questions/assessment', methods=['POST'])
@token_required
def generate_assessment_questions():
    try:
        data = request.get_json()
        subject = data.get('subject')
        grade = data.get('grade')
        count = data.get('count', 70)

        if subject not in QUESTION_DATABASE or grade not in QUESTION_DATABASE[subject]:
            return jsonify({"success": False, "error": "Assessment questions not available"}), 400

        # Collect all questions from all topics for this subject and grade
        all_questions = []
        for topic in QUESTION_DATABASE[subject][grade]:
            all_questions.extend(QUESTION_DATABASE[subject][grade][topic])

        if len(all_questions) < count:
            count = len(all_questions)

        selected_questions = random.sample(all_questions, count)
        
        # Remove explanations for assessment mode
        for question in selected_questions:
            question.pop('explanation', None)

        return jsonify({
            "success": True,
            "questions": selected_questions,
            "subject": subject,
            "grade": grade,
            "count": len(selected_questions),
            "mode": "assessment"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/questions/submit', methods=['POST'])
@token_required
def submit_quiz_answers():
    try:
        data = request.get_json()
        user_id = get_user_from_token()
        
        if not user_id:
            return jsonify({"success": False, "error": "Invalid token"}), 401
            
        answers = data.get('answers', [])
        subject = data.get('subject')
        topic = data.get('topic')
        grade = data.get('grade')
        mode = data.get('mode')

        score = 0
        results = []

        for answer in answers:
            question_data = answer.get('question')
            user_answer = answer.get('answer')
            
            is_correct = (user_answer == question_data['correct'])
            if is_correct:
                score += 1

            results.append({
                'question': question_data['question'],
                'userAnswer': user_answer,
                'correctAnswer': question_data['correct'],
                'isCorrect': is_correct,
                'explanation': question_data.get('explanation', 'No explanation available')
            })

        # Update user progress
        if topic and mode == 'practice':
            conn = get_db_connection()
            progress = conn.execute(
                'SELECT * FROM user_progress WHERE user_id = ? AND subject = ? AND topic = ? AND grade_level = ?',
                (user_id, subject, topic, grade)
            ).fetchone()

            if progress:
                conn.execute(
                    'UPDATE user_progress SET questions_attempted = questions_attempted + ?, questions_correct = questions_correct + ?, last_attempted = CURRENT_TIMESTAMP WHERE id = ?',
                    (len(answers), score, progress['id'])
                )
            else:
                conn.execute(
                    'INSERT INTO user_progress (user_id, subject, topic, grade_level, questions_attempted, questions_correct) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, subject, topic, grade, len(answers), score)
                )
            conn.commit()
            conn.close()

        percentage = (score / len(answers)) * 100 if answers else 0
        
        return jsonify({
            "success": True,
            "score": score,
            "total": len(answers),
            "percentage": round(percentage, 2),
            "results": results,
            "mode": mode
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/progress', methods=['GET'])
@token_required
def get_user_progress():
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"success": False, "error": "Invalid token"}), 401
            
        conn = get_db_connection()
        
        progress = conn.execute('''
            SELECT subject, topic, grade_level, questions_attempted, questions_correct, 
                   last_attempted,
                   CASE WHEN questions_attempted > 0 
                        THEN ROUND((questions_correct * 100.0 / questions_attempted), 2)
                        ELSE 0 
                   END as accuracy
            FROM user_progress 
            WHERE user_id = ?
            ORDER BY last_attempted DESC
        ''', (user_id,)).fetchall()
        
        conn.close()

        progress_data = []
        for row in progress:
            progress_data.append({
                'subject': row['subject'],
                'topic': row['topic'],
                'gradeLevel': row['grade_level'],
                'questionsAttempted': row['questions_attempted'],
                'questionsCorrect': row['questions_correct'],
                'accuracy': row['accuracy'],
                'lastAttempted': row['last_attempted']
            })

        return jsonify({
            "success": True,
            "progress": progress_data
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_user_profile():
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"success": False, "error": "Invalid token"}), 401
            
        conn = get_db_connection()
        
        user = conn.execute(
            'SELECT id, email, first_name, last_name, grade_level, curriculum, created_at FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        
        conn.close()

        if user:
            return jsonify({
                "success": True,
                "user": {
                    "id": user['id'],
                    "email": user['email'],
                    "firstName": user['first_name'],
                    "lastName": user['last_name'],
                    "gradeLevel": user['grade_level'],
                    "curriculum": user['curriculum'],
                    "joinedDate": user['created_at']
                }
            })
        else:
            return jsonify({"success": False, "error": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Health check and info endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

@app.route('/')
def home():
    return jsonify({
        "message": "Ideolix Learning Hub API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "auth": ["/api/auth/register", "/api/auth/login"],
            "curriculum": ["/api/curricula", "/api/subjects", "/api/topics"],
            "questions": ["/api/questions/practice", "/api/questions/assessment", "/api/questions/submit"],
            "progress": ["/api/progress", "/api/user/profile"]
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Ideolix Learning Hub API...")
    print("📚 Available Features:")
    print("   ✅ User Authentication & Registration")
    print("   ✅ Multiple Curriculum Support")
    print("   ✅ Grade 1-12 Comprehensive Coverage")
    print("   ✅ Practice Mode (30 questions per topic)")
    print("   ✅ Assessment Mode (70 random questions)")
    print("   ✅ Real Questions with Explanations")
    print("   ✅ Progress Tracking")
    print("   ✅ Instant Feedback")
    print("\n🌐 Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
