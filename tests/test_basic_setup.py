# tests/test_basic_setup.py
import unittest
from app import create_app

class BasicSetupTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms if not explicitly handled
        self.app.config['SECRET_KEY'] = 'test_secret_key' # Ensure a consistent secret key for tests
        self.client = self.app.test_client()

    def tearDown(self):
        pass # Clean up if needed

    def test_app_exists(self):
        self.assertIsNotNone(self.app)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_index_redirects_to_questionnaires(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302) # Redirect
        self.assertTrue('/questionnaires' in response.location)

    def test_questionnaires_page_loads(self):
        response = self.client.get('/questionnaires')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Available Questionnaires', response.data)

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

if __name__ == '__main__':
    unittest.main()
