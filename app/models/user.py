# app/models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash_str): # Renamed for clarity
        self.id = id
        self.username = username
        self.password_hash = password_hash_str

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

users_db = {} # username: User object
next_user_id_counter = 1 # Use a different name to avoid conflict with previous 'next_user_id' import if any lingering state

def get_user_by_username(username):
    return users_db.get(username) # Simpler lookup if username is the key

def get_user_by_id(user_id):
    for user in users_db.values():
        if user.id == user_id:
            return user
    return None

def add_user(username, password):
    global next_user_id_counter
    if username in users_db:
        return None # User already exists
    new_user = User(id=next_user_id_counter, username=username, password_hash_str="")
    new_user.set_password(password)
    users_db[username] = new_user
    next_user_id_counter += 1
    return new_user

# Initialize the admin user with a hashed password
# To avoid running generate_password_hash() at module load time for existing user,
# we can pre-hash or set it up differently. For this subtask, let's re-add the admin
# user with a hashed password if the db is empty.
if not users_db: # Only if db is empty
    admin_user = User(id=next_user_id_counter, username="admin", password_hash_str=generate_password_hash("securepassword"))
    users_db["admin"] = admin_user
    next_user_id_counter +=1
