import random

# Example subjects, topics, and sample templates
curricula = ["nigerian", "british", "us"]
subjects = {
    "Mathematics": {
        "Algebra": [
            {"type": "mcq", "question": "What is {a} + {b}?", "choices": [], "answer": None},
            {"type": "numeric", "question": "Multiply {a} by {b}", "answer": None}
        ],
        "Geometry": [
            {"type": "mcq", "question": "A triangle has angles {a}, {b}, and ? degrees. Find the missing angle.", "choices": [], "answer": None}
        ]
    },
    "English": {
        "Vocabulary": [
            {"type": "mcq", "question": "Select the synonym of '{word}'", "choices": [], "answer": None}
        ],
        "Grammar": [
            {"type": "mcq", "question": "Choose the correct verb form: '{sentence}'", "choices": [], "answer": None}
        ]
    },
    "Science": {
        "Biology": [
            {"type": "mcq", "question": "What is the powerhouse of the cell?", "choices": ["Mitochondria","Nucleus","Ribosome","Chloroplast"], "answer": "Mitochondria"}
        ],
        "Physics": [
            {"type": "numeric", "question": "If a car travels at {a} m/s for {b} seconds, what is the distance?", "answer": None}
        ]
    }
}

# Sample words and sentences for English
sample_words = ["happy", "sad", "big", "small", "fast", "slow"]
sample_sentences = ["He (run) fast.", "They (be) friends.", "She (have) a book."]

# ------------------ PRACTICE MODE ------------------
def generate_questions_for_practice(curriculum, grade, subject, topics=[], count_per_topic=30):
    all_questions = []

    if subject not in subjects:
        subject = random.choice(list(subjects.keys()))

    available_topics = subjects[subject].keys() if not topics else topics

    for topic in available_topics:
        if topic not in subjects[subject]:
            continue
        templates = subjects[subject][topic]
        for _ in range(count_per_topic):
            template = random.choice(templates)
            q = template.copy()

            # Fill in variables for math
            if "{a}" in q["question"] and "{b}" in q["question"]:
                a, b = random.randint(1, 20), random.randint(1, 20)
                q["question"] = q["question"].replace("{a}", str(a)).replace("{b}", str(b))
                if q["type"] == "mcq":
                    correct = a + b
                    q["choices"] = [correct, correct+1, correct-1, correct+2]
                    random.shuffle(q["choices"])
                    q["answer"] = correct
                elif q["type"] == "numeric":
                    if "Multiply" in q["question"]:
                        q["answer"] = a * b
                    else:
                        q["answer"] = 180 - a - b

            # Fill in English words
            if "{word}" in q["question"]:
                word = random.choice(sample_words)
                q["question"] = q["question"].replace("{word}", word)
                q["choices"] = random.sample(sample_words, 4)
                q["answer"] = word

            # Fill in grammar sentences
            if "{sentence}" in q.get("question", ""):
                sentence = random.choice(sample_sentences)
                q["question"] = q["question"].replace("{sentence}", sentence)
                q["choices"] = ["run", "ran", "running", "runs"]
                q["answer"] = "ran"  # placeholder

            q["curriculum"] = curriculum
            q["grade"] = grade
            q["subject"] = subject
            q["topic"] = topic
            all_questions.append(q)

    return all_questions

# ------------------ ASSESSMENT MODE ------------------
def generate_questions_for_assessment(curriculum, grade, subject, count=70):
    questions = []

    if subject not in subjects:
        subject = random.choice(list(subjects.keys()))

    all_topics = list(subjects[subject].keys())

    for _ in range(count):
        topic = random.choice(all_topics)
        template = random.choice(subjects[subject][topic])
        q = template.copy()

        # Fill variables for math
        if "{a}" in q["question"] and "{b}" in q["question"]:
            a, b = random.randint(10, 100), random.randint(1, 50)
            q["question"] = q["question"].replace("{a}", str(a)).replace("{b}", str(b))
            if q["type"] == "mcq":
                correct = a + b
                q["choices"] = [correct, correct+1, correct-1, correct+2]
                random.shuffle(q["choices"])
                q["answer"] = correct
            elif q["type"] == "numeric":
                if "Multiply" in q["question"]:
                    q["answer"] = a * b
                else:
                    q["answer"] = 180 - a - b

        # Fill English
        if "{word}" in q["question"]:
            word = random.choice(sample_words)
            q["question"] = q["question"].replace("{word}", word)
            q["choices"] = random.sample(sample_words, 4)
            q["answer"] = word

        q["curriculum"] = curriculum
        q["grade"] = grade
        q["subject"] = subject
        q["topic"] = topic
        questions.append(q)

    return questions
