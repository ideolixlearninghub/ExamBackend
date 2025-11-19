<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ideolix Learning Hub</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Welcome Page */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            text-align: center;
            color: white;
        }

        .welcome-container h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .welcome-container p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }

        .btn {
            padding: 15px 30px;
            font-size: 1.1rem;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 0 10px;
        }

        .btn-primary {
            background: #ff6b6b;
            color: white;
        }

        .btn-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* Auth Forms */
        .auth-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 50px auto;
        }

        .auth-container h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn-full {
            width: 100%;
            margin: 10px 0;
        }

        .auth-link {
            text-align: center;
            margin-top: 20px;
        }

        /* Dashboard */
        .dashboard {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .dashboard-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 30px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-avatar {
            width: 50px;
            height: 50px;
            background: #667eea;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }

        /* Selection Grid */
        .selection-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .selection-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .selection-card:hover {
            transform: translateY(-5px);
            border-color: #667eea;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        }

        .selection-card i {
            font-size: 2.5rem;
            color: #667eea;
            margin-bottom: 15px;
        }

        .selection-card h3 {
            margin-bottom: 10px;
            color: #333;
        }

        /* Question Interface */
        .question-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .question-text {
            font-size: 1.2rem;
            margin-bottom: 25px;
            line-height: 1.6;
        }

        .options-container {
            display: grid;
            gap: 15px;
        }

        .option {
            padding: 15px 20px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .option:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }

        .option.selected {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }

        .option.correct {
            border-color: #28a745;
            background: #28a745;
            color: white;
        }

        .option.incorrect {
            border-color: #dc3545;
            background: #dc3545;
            color: white;
        }

        .navigation {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }

        /* Progress Bar */
        .progress-container {
            margin: 20px 0;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            overflow: hidden;
        }

        .progress {
            height: 100%;
            background: #667eea;
            transition: width 0.3s ease;
        }

        /* Results */
        .results-container {
            text-align: center;
            padding: 40px;
        }

        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: #667eea;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: bold;
            margin: 0 auto 30px;
        }

        /* Utility Classes */
        .hidden {
            display: none !important;
        }

        .text-center {
            text-align: center;
        }

        .mt-20 {
            margin-top: 20px;
        }

        .mb-20 {
            margin-bottom: 20px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .welcome-container h1 {
                font-size: 2.5rem;
            }
            
            .auth-container {
                margin: 20px;
                padding: 30px 20px;
            }
            
            .selection-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Welcome Page -->
    <div id="welcomePage" class="welcome-container">
        <div class="container">
            <h1>🎓 Ideolix Learning Hub</h1>
            <p>Your personalized learning journey starts here</p>
            <div>
                <button class="btn btn-primary" onclick="showAuth('login')">Sign In</button>
                <button class="btn btn-secondary" onclick="showAuth('register')">Sign Up</button>
            </div>
        </div>
    </div>

    <!-- Authentication Pages -->
    <div id="authPage" class="hidden">
        <div class="container">
            <!-- Login Form -->
            <div id="loginForm" class="auth-container">
                <h2>Welcome Back</h2>
                <form id="loginFormElement">
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="loginEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="loginPassword" required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Sign In</button>
                </form>
                <div class="auth-link">
                    <p>Don't have an account? <a href="#" onclick="showAuth('register')">Sign Up</a></p>
                </div>
            </div>

            <!-- Registration Form -->
            <div id="registerForm" class="auth-container hidden">
                <h2>Create Account</h2>
                <form id="registerFormElement">
                    <div class="form-group">
                        <label>First Name</label>
                        <input type="text" id="registerFirstName" required>
                    </div>
                    <div class="form-group">
                        <label>Last Name</label>
                        <input type="text" id="registerLastName" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="registerEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="registerPassword" required>
                    </div>
                    <div class="form-group">
                        <label>Grade Level</label>
                        <select id="registerGrade" required>
                            <option value="">Select Grade</option>
                            <option value="1">Grade 1</option>
                            <option value="2">Grade 2</option>
                            <option value="3">Grade 3</option>
                            <option value="4">Grade 4</option>
                            <option value="5">Grade 5</option>
                            <option value="6">Grade 6</option>
                            <option value="7">Grade 7</option>
                            <option value="8">Grade 8</option>
                            <option value="9">Grade 9</option>
                            <option value="10">Grade 10</option>
                            <option value="11">Grade 11</option>
                            <option value="12">Grade 12</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Curriculum</label>
                        <select id="registerCurriculum" required>
                            <option value="">Select Curriculum</option>
                            <option value="nigeria">Nigerian Curriculum</option>
                            <option value="cambridge">Cambridge International</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Create Account</button>
                </form>
                <div class="auth-link">
                    <p>Already have an account? <a href="#" onclick="showAuth('login')">Sign In</a></p>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Dashboard -->
    <div id="dashboard" class="hidden">
        <div class="container">
            <div class="dashboard">
                <div class="dashboard-header">
                    <h1>Learning Dashboard</h1>
                    <div class="user-info">
                        <div class="user-avatar" id="userAvatar">JD</div>
                        <div>
                            <div id="userName">John Doe</div>
                            <div id="userGrade">Grade 10 - Nigerian Curriculum</div>
                        </div>
                        <button class="btn btn-secondary" onclick="logout()">Logout</button>
                    </div>
                </div>

                <!-- Curriculum Selection -->
                <div id="curriculumSelection">
                    <h2>Select Your Learning Path</h2>
                    <div class="selection-grid">
                        <div class="selection-card" onclick="selectCurriculum('nigeria')">
                            <i class="fas fa-graduation-cap"></i>
                            <h3>Nigerian Curriculum</h3>
                            <p>WAEC, NECO, JAMB preparation</p>
                        </div>
                        <div class="selection-card" onclick="selectCurriculum('cambridge')">
                            <i class="fas fa-globe"></i>
                            <h3>Cambridge International</h3>
                            <p>IGCSE, A-Levels preparation</p>
                        </div>
                    </div>
                </div>

                <!-- Grade Selection -->
                <div id="gradeSelection" class="hidden">
                    <h2>Select Your Grade Level</h2>
                    <div class="selection-grid">
                        <!-- Grades 1-12 will be populated here -->
                    </div>
                </div>

                <!-- Subject Selection -->
                <div id="subjectSelection" class="hidden">
                    <h2>Select a Subject</h2>
                    <div class="selection-grid" id="subjectGrid">
                        <!-- Subjects will be populated here -->
                    </div>
                </div>

                <!-- Topic Selection -->
                <div id="topicSelection" class="hidden">
                    <h2>Select a Topic</h2>
                    <div class="selection-grid" id="topicGrid">
                        <!-- Topics will be populated here -->
                    </div>
                </div>

                <!-- Mode Selection -->
                <div id="modeSelection" class="hidden">
                    <h2>Choose Learning Mode</h2>
                    <div class="selection-grid">
                        <div class="selection-card" onclick="startPractice()">
                            <i class="fas fa-book-open"></i>
                            <h3>Practice Mode</h3>
                            <p>30 questions with instant feedback</p>
                        </div>
                        <div class="selection-card" onclick="startAssessment()">
                            <i class="fas fa-clipboard-list"></i>
                            <h3>Assessment Mode</h3>
                            <p>70 questions - CBT standard</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Question Interface -->
    <div id="questionInterface" class="hidden">
        <div class="container">
            <div class="dashboard">
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress" id="progressBar" style="width: 0%"></div>
                    </div>
                    <div class="text-center" id="progressText">Question 1 of 30</div>
                </div>

                <div class="question-container">
                    <div class="question-text" id="questionText"></div>
                    <div class="options-container" id="optionsContainer"></div>
                </div>

                <div class="navigation">
                    <button class="btn btn-secondary" onclick="previousQuestion()" id="prevBtn">Previous</button>
                    <button class="btn btn-primary" onclick="nextQuestion()" id="nextBtn">Next</button>
                    <button class="btn btn-primary" onclick="submitQuiz()" id="submitBtn" style="display: none">Submit</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Results Page -->
    <div id="resultsPage" class="hidden">
        <div class="container">
            <div class="dashboard">
                <div class="results-container">
                    <div class="score-circle" id="scoreCircle">85%</div>
                    <h2 id="resultsTitle">Practice Completed!</h2>
                    <p id="resultsDescription">You scored <span id="scoreValue">25</span> out of <span id="totalQuestions">30</span> questions correctly</p>
                    
                    <div class="navigation mt-20">
                        <button class="btn btn-secondary" onclick="showDashboard()">Back to Dashboard</button>
                        <button class="btn btn-primary" onclick="reviewAnswers()">Review Answers</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global state
        const state = {
            currentUser: null,
            token: null,
            currentCurriculum: null,
            currentGrade: null,
            currentSubject: null,
            currentTopic: null,
            currentMode: null,
            questions: [],
            currentQuestionIndex: 0,
            userAnswers: [],
            quizStarted: false
        };

        // API Base URL
        const API_BASE = 'http://localhost:5000/api';

        // Authentication functions
        async function registerUser(userData) {
            try {
                const response = await fetch(`${API_BASE}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData)
                });

                const data = await response.json();
                
                if (data.success) {
                    alert('Registration successful! Please login.');
                    showAuth('login');
                } else {
                    alert('Registration failed: ' + data.error);
                }
            } catch (error) {
                alert('Registration error: ' + error.message);
            }
        }

        async function loginUser(credentials) {
            try {
                const response = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(credentials)
                });

                const data = await response.json();
                
                if (data.success) {
                    state.token = data.token;
                    state.currentUser = data.user;
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    showDashboard();
                    loadUserProfile();
                } else {
                    alert('Login failed: ' + data.error);
                }
            } catch (error) {
                alert('Login error: ' + error.message);
            }
        }

        // Page navigation functions
        function showAuth(formType) {
            document.getElementById('welcomePage').classList.add('hidden');
            document.getElementById('authPage').classList.remove('hidden');
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('registerForm').classList.add('hidden');
            
            if (formType === 'login') {
                document.getElementById('loginForm').classList.remove('hidden');
            } else {
                document.getElementById('registerForm').classList.remove('hidden');
            }
        }

        function showDashboard() {
            hideAllPages();
            document.getElementById('dashboard').classList.remove('hidden');
            resetSelectionState();
        }

        function hideAllPages() {
            const pages = ['welcomePage', 'authPage', 'dashboard', 'questionInterface', 'resultsPage'];
            pages.forEach(page => document.getElementById(page).classList.add('hidden'));
        }

        function resetSelectionState() {
            document.getElementById('curriculumSelection').classList.remove('hidden');
            document.getElementById('gradeSelection').classList.add('hidden');
            document.getElementById('subjectSelection').classList.add('hidden');
            document.getElementById('topicSelection').classList.add('hidden');
            document.getElementById('modeSelection').classList.add('hidden');
        }

        // Curriculum and subject selection
        function selectCurriculum(curriculum) {
            state.currentCurriculum = curriculum;
            document.getElementById('curriculumSelection').classList.add('hidden');
            document.getElementById('gradeSelection').classList.remove('hidden');
            
            const gradeGrid = document.getElementById('gradeSelection').querySelector('.selection-grid');
            gradeGrid.innerHTML = '';
            
            for (let grade = 1; grade <= 12; grade++) {
                gradeGrid.innerHTML += `
                    <div class="selection-card" onclick="selectGrade(${grade})">
                        <i class="fas fa-user-graduate"></i>
                        <h3>Grade ${grade}</h3>
                        <p>Continue your learning journey</p>
                    </div>
                `;
            }
        }

        function selectGrade(grade) {
            state.currentGrade = grade;
            document.getElementById('gradeSelection').classList.add('hidden');
            document.getElementById('subjectSelection').classList.remove('hidden');
            
            loadSubjects();
        }

        async function loadSubjects() {
            try {
                const response = await fetch(`${API_BASE}/subjects`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    },
                    body: JSON.stringify({
                        curriculum: state.currentCurriculum,
                        grade: state.currentGrade.toString()
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    const subjectGrid = document.getElementById('subjectGrid');
                    subjectGrid.innerHTML = '';
                    
                    data.subjects.forEach(subject => {
                        subjectGrid.innerHTML += `
                            <div class="selection-card" onclick="selectSubject('${subject}')">
                                <i class="fas fa-book"></i>
                                <h3>${subject}</h3>
                                <p>Explore ${subject} topics</p>
                            </div>
                        `;
                    });
                }
            } catch (error) {
                alert('Error loading subjects: ' + error.message);
            }
        }

        function selectSubject(subject) {
            state.currentSubject = subject;
            document.getElementById('subjectSelection').classList.add('hidden');
            document.getElementById('topicSelection').classList.remove('hidden');
            
            loadTopics();
        }

        async function loadTopics() {
            try {
                const response = await fetch(`${API_BASE}/topics`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    },
                    body: JSON.stringify({
                        subject: state.currentSubject,
                        grade: state.currentGrade.toString()
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    const topicGrid = document.getElementById('topicGrid');
                    topicGrid.innerHTML = '';
                    
                    data.topics.forEach(topic => {
                        topicGrid.innerHTML += `
                            <div class="selection-card" onclick="selectTopic('${topic}')">
                                <i class="fas fa-star"></i>
                                <h3>${topic}</h3>
                                <p>Practice ${topic}</p>
                            </div>
                        `;
                    });
                }
            } catch (error) {
                alert('Error loading topics: ' + error.message);
            }
        }

        function selectTopic(topic) {
            state.currentTopic = topic;
            document.getElementById('topicSelection').classList.add('hidden');
            document.getElementById('modeSelection').classList.remove('hidden');
        }

        // Quiz functions
        async function startPractice() {
            state.currentMode = 'practice';
            await loadQuestions();
        }

        async function startAssessment() {
            state.currentMode = 'assessment';
            await loadQuestions();
        }

        async function loadQuestions() {
            try {
                const endpoint = state.currentMode === 'practice' ? 'practice' : 'assessment';
                const requestBody = state.currentMode === 'practice' ? {
                    subject: state.currentSubject,
                    topic: state.currentTopic,
                    grade: state.currentGrade.toString(),
                    count: 30
                } : {
                    subject: state.currentSubject,
                    grade: state.currentGrade.toString(),
                    count: 70
                };

                const response = await fetch(`${API_BASE}/questions/${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    },
                    body: JSON.stringify(requestBody)
                });

                const data = await response.json();
                
                if (data.success) {
                    state.questions = data.questions;
                    state.currentQuestionIndex = 0;
                    state.userAnswers = new Array(data.questions.length).fill(null);
                    state.quizStarted = true;
                    
                    showQuestionInterface();
                    displayQuestion(0);
                }
            } catch (error) {
                alert('Error loading questions: ' + error.message);
            }
        }

        function showQuestionInterface() {
            hideAllPages();
            document.getElementById('questionInterface').classList.remove('hidden');
        }

        function displayQuestion(index) {
            const question = state.questions[index];
            document.getElementById('questionText').textContent = question.question;
            
            const optionsContainer = document.getElementById('optionsContainer');
            optionsContainer.innerHTML = '';
            
            question.options.forEach((option, optionIndex) => {
                const optionElement = document.createElement('div');
                optionElement.className = 'option';
                if (state.userAnswers[index] === optionIndex) {
                    optionElement.classList.add('selected');
                }
                optionElement.textContent = option;
                optionElement.onclick = () => selectOption(optionIndex);
                optionsContainer.appendChild(optionElement);
            });
            
            updateProgress();
            updateNavigationButtons();
        }

        function selectOption(optionIndex) {
            state.userAnswers[state.currentQuestionIndex] = optionIndex;
            displayQuestion(state.currentQuestionIndex);
        }

        function updateProgress() {
            const progress = ((state.currentQuestionIndex + 1) / state.questions.length) * 100;
            document.getElementById('progressBar').style.width = `${progress}%`;
            document.getElementById('progressText').textContent = 
                `Question ${state.currentQuestionIndex + 1} of ${state.questions.length}`;
        }

        function updateNavigationButtons() {
            document.getElementById('prevBtn').style.display = 
                state.currentQuestionIndex > 0 ? 'inline-block' : 'none';
            
            if (state.currentQuestionIndex === state.questions.length - 1) {
                document.getElementById('nextBtn').style.display = 'none';
                document.getElementById('submitBtn').style.display = 'inline-block';
            } else {
                document.getElementById('nextBtn').style.display = 'inline-block';
                document.getElementById('submitBtn').style.display = 'none';
            }
        }

        function previousQuestion() {
            if (state.currentQuestionIndex > 0) {
                state.currentQuestionIndex--;
                displayQuestion(state.currentQuestionIndex);
            }
        }

        function nextQuestion() {
            if (state.currentQuestionIndex < state.questions.length - 1) {
                state.currentQuestionIndex++;
                displayQuestion(state.currentQuestionIndex);
            }
        }

        async function submitQuiz() {
            try {
                const answers = state.questions.map((question, index) => ({
                    question: question,
                    answer: state.userAnswers[index]
                }));

                const response = await fetch(`${API_BASE}/questions/submit`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    },
                    body: JSON.stringify({
                        answers: answers,
                        subject: state.currentSubject,
                        topic: state.currentTopic,
                        grade: state.currentGrade.toString(),
                        mode: state.currentMode
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    showResults(data);
                }
            } catch (error) {
                alert('Error submitting quiz: ' + error.message);
            }
        }

        function showResults(data) {
            hideAllPages();
            document.getElementById('resultsPage').classList.remove('hidden');
            
            document.getElementById('scoreCircle').textContent = `${data.percentage}%`;
            document.getElementById('scoreValue').textContent = data.score;
            document.getElementById('totalQuestions').textContent = data.total;
            
            // Store results for review
            state.quizResults = data;
        }

        function reviewAnswers() {
            // Implement answer review functionality
            alert('Answer review feature coming soon!');
        }

        function logout() {
            state.token = null;
            state.currentUser = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            hideAllPages();
            document.getElementById('welcomePage').classList.remove('hidden');
        }

        function loadUserProfile() {
            if (state.currentUser) {
                document.getElementById('userName').textContent = 
                    `${state.currentUser.firstName} ${state.currentUser.lastName}`;
                document.getElementById('userAvatar').textContent = 
                    state.currentUser.firstName[0] + state.currentUser.lastName[0];
                document.getElementById('userGrade').textContent = 
                    `Grade ${state.currentUser.gradeLevel} - ${getCurriculumName(state.currentUser.curriculum)}`;
            }
        }

        function getCurriculumName(curriculum) {
            const names = {
                'nigeria': 'Nigerian Curriculum',
                'cambridge': 'Cambridge International'
            };
            return names[curriculum] || curriculum;
        }

        // Event listeners
        document.getElementById('registerFormElement').addEventListener('submit', function(e) {
            e.preventDefault();
            const userData = {
                email: document.getElementById('registerEmail').value,
                password: document.getElementById('registerPassword').value,
                firstName: document.getElementById('registerFirstName').value,
                lastName: document.getElementById('registerLastName').value,
                gradeLevel: parseInt(document.getElementById('registerGrade').value),
                curriculum: document.getElementById('registerCurriculum').value
            };
            registerUser(userData);
        });

        document.getElementById('loginFormElement').addEventListener('submit', function(e) {
            e.preventDefault();
            const credentials = {
                email: document.getElementById('loginEmail').value,
                password: document.getElementById('loginPassword').value
            };
            loginUser(credentials);
        });

        // Check for existing session on load
        window.addEventListener('load', function() {
            const savedToken = localStorage.getItem('token');
            const savedUser = localStorage.getItem('user');
            
            if (savedToken && savedUser) {
                state.token = savedToken;
                state.currentUser = JSON.parse(savedUser);
                showDashboard();
                loadUserProfile();
            }
        });
    </script>
</body>
</html>
