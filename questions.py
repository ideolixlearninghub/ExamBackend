import random

# Example subjects and question templates
subjects = {
    "Mathematics": [
        {"type": "mcq", "question": "What is {a} + {b}?", "choices": [], "answer": None},
        {"type": "numeric", "question": "Multiply {a} by {b}", "answer": None}
    ],
    "English": [
        {"type": "mcq", "question": "Select the synonym of '{word}'", "choices": [], "answer": None}
    ]
}

def generate_question_set(curriculum, grade, subject, count=1):
    questions_list = []
    if subject not in subjects:
        subject = random.choice(list(subjects.keys()))
    templates = subjects[subject]

    for _ in range(count):
        template = random.choice(templates)
        q = template.copy()

        # Randomize numbers for math questions
        if "{a}" in q["question"] and "{b}" in q["question"]:
            a, b = random.randint(1, 20), random.randint(1, 20)
            q["question"] = q["question"].replace("{a}", str(a)).replace("{b}", str(b))
            if q["type"] == "mcq":
                # Generate choices
                correct = a + b
                q["choices"] = [correct, correct+1, correct-1, correct+2]
                random.shuffle(q["choices"])
                q["answer"] = correct
            elif q["type"] == "numeric":
                q["answer"] = a * b

        # Randomize word for English
        if "{word}" in q["question"]:
            words = ["happy", "sad", "big", "small"]
            word = random.choice(words)
            q["question"] = q["question"].replace("{word}", word)
            q["choices"] = ["joyful", "angry", "tiny", "large"]
            q["answer"] = "joyful"

        questions_list.append(q)
    return questions_list
