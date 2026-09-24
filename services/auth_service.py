from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, data):
        email = data.get('email')
        if self.user_repo.get_by_email(email):
            return False, "Email already exists"
        
        hashed_password = generate_password_hash(data.get('password'))
        new_user = {
            'name': data.get('name'),
            'email': email,
            'password': hashed_password,
            'role': data.get('role', 'user'),
            'member_since': data.get('member_since')
        }
        user = self.user_repo.create(new_user)
        # return user without password
        user_clean = {k:v for k,v in user.items() if k != 'password'}
        return True, user_clean

    def authenticate_user(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user and check_password_hash(user.get('password'), password):
            user_clean = {k:v for k,v in user.items() if k != 'password'}
            return True, user_clean
        return False, "Invalid credentials"
    
    def get_user_by_id(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if user:
            return {k:v for k,v in user.items() if k != 'password'}
        return None
