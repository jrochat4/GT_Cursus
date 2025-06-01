# app/models/questionnaire.py

class Questionnaire:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.questions = [] # List to hold Question objects

    def add_question(self, question):
        self.questions.append(question)

    def get_question_by_id(self, question_id):
        for q in self.questions:
            if q.id == question_id:
                return q
        return None

    def __repr__(self):
        return f"<Questionnaire {self.id}: {self.title}>"

class Question:
    QUESTION_TYPES = [
        ('TEXT', 'Text Input'),
        ('MULTIPLE_CHOICE', 'Multiple Choice'),
        ('LIKERT_SCALE', 'Likert Scale'),
    ]
    next_question_id = 1 # Class variable to auto-increment question IDs for simplicity

    def __init__(self, text, question_type, questionnaire_id, choices=None, id=None):
        if not text: # Basic validation
            raise ValueError("Question text cannot be empty.")

        # Ensure question_type is valid
        valid_types = [qt[0] for qt in self.QUESTION_TYPES]
        if question_type not in valid_types:
            raise ValueError(f"Invalid question type: {question_type}. Must be one of {valid_types}")

        self.id = id if id is not None else Question.next_question_id
        if id is None: # Only increment if we are assigning a new ID
             Question.next_question_id +=1

        self.text = text
        self.question_type = question_type
        self.questionnaire_id = questionnaire_id

        self.choices = choices if choices else []

        if question_type in ['MULTIPLE_CHOICE', 'LIKERT_SCALE'] and not self.choices:
            raise ValueError("Choices must be provided for MULTIPLE_CHOICE or LIKERT_SCALE questions.")

    def __repr__(self):
        return f"<Question {self.id}: {self.text[:30]}... ({self.question_type})>"

# Reset next_question_id for consistent behavior if the module is reloaded (mainly for dev)
Question.next_question_id = 1
