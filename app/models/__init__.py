# app/models/__init__.py
from .questionnaire import Questionnaire, Question
from .user import User, get_user_by_id, get_user_by_username, users_db, add_user # Ensure add_user is here
# Removed next_user_id from here as it's managed internally by user.py now
