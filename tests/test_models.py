# tests/test_models.py
import unittest
from app.models import Questionnaire, Question, User
# For User model, we might need app context if Flask-Login or other extensions are deeply tied
# but for basic instantiation and password hashing, it should be fine.
# from werkzeug.security import check_password_hash

class ModelTests(unittest.TestCase):

    def test_create_questionnaire(self):
        q = Questionnaire(id=1, title="Test Title", description="Test Desc")
        self.assertEqual(q.id, 1)
        self.assertEqual(q.title, "Test Title")
        self.assertEqual(q.description, "Test Desc")
        self.assertEqual(len(q.questions), 0)

    def test_create_question_text(self):
        # Resetting Question class's internal ID counter for predictable test IDs
        Question.next_question_id = 1
        q = Question(text="Is this a test?", question_type="TEXT", questionnaire_id=1)
        self.assertEqual(q.id, 1) # First question created
        self.assertEqual(q.text, "Is this a test?")
        self.assertEqual(q.question_type, "TEXT")
        self.assertEqual(len(q.choices), 0)
        Question.next_question_id = 1 # Reset again for other tests if they run in same suite without re-init

    def test_create_question_multiple_choice(self):
        Question.next_question_id = 1
        choices = ["Yes", "No", "Maybe"]
        q = Question(text="Choose one.", question_type="MULTIPLE_CHOICE", questionnaire_id=1, choices=choices)
        self.assertEqual(q.id, 1)
        self.assertEqual(q.question_type, "MULTIPLE_CHOICE")
        self.assertEqual(len(q.choices), 3)
        self.assertEqual(q.choices, choices)
        Question.next_question_id = 1


    def test_question_invalid_type(self):
        with self.assertRaises(ValueError):
            Question(text="Invalid type q", question_type="INVALID_TYPE", questionnaire_id=1)

    def test_question_multiple_choice_requires_choices(self):
        with self.assertRaises(ValueError):
            Question(text="No choices here", question_type="MULTIPLE_CHOICE", questionnaire_id=1, choices=[])
        with self.assertRaises(ValueError):
            Question(text="No choices here", question_type="LIKERT_SCALE", questionnaire_id=1, choices=None)

    def test_add_question_to_questionnaire(self):
        Question.next_question_id = 1
        qn = Questionnaire(id=1, title="Qnaire", description="Desc")
        q1 = Question(text="Q1", question_type="TEXT", questionnaire_id=1)
        qn.add_question(q1)
        self.assertEqual(len(qn.questions), 1)
        self.assertEqual(qn.questions[0].text, "Q1")
        Question.next_question_id = 1


    def test_create_user_and_password_hashing(self):
        # User model's add_user and users_db are module-level, so they persist.
        # For isolated tests, we might need to clear users_db or use unique usernames.
        # For now, let's assume a clean state or use a unique username.

        # We are not using the add_user function here, but direct User instantiation
        # to test the User class's methods more directly.
        # The User class itself does not auto-increment ID.
        user = User(id=100, username="testuser_models", password_hash_str="") # id is just for the object
        user.set_password("testpass123")

        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, "testpass123")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.check_password("wrongpassword"))

if __name__ == '__main__':
    unittest.main()
