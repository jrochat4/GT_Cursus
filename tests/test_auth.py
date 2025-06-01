# tests/test_auth.py
import unittest
from app import create_app
from app.models import User, users_db, get_user_by_username, add_user
from flask_login import current_user

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms
        self.app.config['SECRET_KEY'] = 'test_secret_key_auth'
        # It's crucial that the in-memory 'users_db' is clean for each test method,
        # or that tests use unique usernames to avoid interference.
        # We'll manually clear and re-initialize the admin user for some tests.
        users_db.clear()
        # Re-initialize next_user_id_counter from the User model if it exists as a global
        # This is a bit of a hack for module-level state. A better way would be a fixture
        # or ensuring the model's state management is more robust for testing.
        try:
            from app.models.user import next_user_id_counter as user_model_next_id
            # This direct manipulation is not ideal, but necessary for current model structure
            import app.models.user
            app.models.user.next_user_id_counter = 1
        except ImportError:
            pass # If not defined or refactored

        add_user("admin_auth", "adminpass") # Add a known user for login tests

        self.client = self.app.test_client()

    def tearDown(self):
        # Ensure users_db is cleared after each test to prevent state leakage
        users_db.clear()
        # Reset counter again
        try:
            import app.models.user
            app.models.user.next_user_id_counter = 1
        except ImportError:
            pass


    def test_register_new_user_success(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful! Please login.', response.data)
        # Check if user was actually added (optional, but good)
        user = get_user_by_username('newuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('newpassword'))

    def test_register_existing_user_fail(self):
        # First, register a user
        self.client.post('/register', data={'username': 'existinguser', 'password': 'password'})
        # Then, try to register the same username again
        response = self.client.post('/register', data={
            'username': 'existinguser',
            'password': 'anotherpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on register page
        self.assertIn(b'Username already exists.', response.data)

    def test_login_correct_credentials(self):
        response = self.client.post('/login', data={
            'username': 'admin_auth',
            'password': 'adminpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Should redirect to questionnaire list
        self.assertIn(b'Logged in successfully.', response.data)
        self.assertIn(b'Available Questionnaires', response.data) # Check for redirect content
        # With app.test_request_context() we could check current_user more directly if needed
        # For now, checking flash message and redirect is fine.

    def test_login_incorrect_username(self):
        response = self.client.post('/login', data={
            'username': 'wronguser',
            'password': 'adminpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Invalid username or password.', response.data)

    def test_login_incorrect_password(self):
        response = self.client.post('/login', data={
            'username': 'admin_auth',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Invalid username or password.', response.data)

    def test_logout_success(self):
        # First, log in
        self.client.post('/login', data={'username': 'admin_auth', 'password': 'adminpass'})
        # Then, log out
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Redirects to login page
        self.assertIn(b'You have been logged out.', response.data)
        self.assertIn(b'Login', response.data) # Check we are back on login page

    def test_protected_route_unauthenticated(self):
        # /questionnaires/new is protected by @login_required
        response = self.client.get('/questionnaires/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Redirects to login
        self.assertIn(b'Please log in to access this page.', response.data) # Flask-Login default message
        self.assertIn(b'Login', response.data) # Check it's the login page

    def test_protected_route_authenticated(self):
        # Log in first
        self.client.post('/login', data={'username': 'admin_auth', 'password': 'adminpass'})
        # Then access protected route
        response = self.client.get('/questionnaires/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Questionnaire', response.data) # Check content of the protected page

    # Helper to check current_user status if needed, though flash messages often suffice
    # def test_current_user_status_after_login(self):
    #     with self.client: # Ensures context is active
    #         self.client.post('/login', data={'username': 'admin_auth', 'password': 'adminpass'})
    #         # After login, current_user should be authenticated within this context
    #         # This requires flask_login.current_user to be proxied correctly in tests
    #         # For more direct check, you might need to inspect session or use test_request_context
    #         # For now, we rely on behavior like redirection and flash messages.
    #         # A more direct way with test_request_context:
    #         with self.app.test_request_context():
    #             # Simulate login if client session doesn't carry over perfectly for current_user
    #             # This part is tricky because current_user is context-local.
    #             # The client.post above should handle session correctly.
    #             # A simple check could be if a logout link appears:
    #             response = self.client.get('/questionnaires') # A page that shows login/logout status
    #             self.assertIn(b'Logout', response.data)


if __name__ == '__main__':
    unittest.main()
