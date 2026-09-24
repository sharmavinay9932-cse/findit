"""
AuthService — registration, login, and user lookup.

Depends on UserRepository which returns dicts with key 'password_hash'.
"""
from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    @staticmethod
    def _clean(user):
        """Strip the password hash before returning user data to routes."""
        if not user:
            return None
        return {k: v for k, v in user.items()
                if k not in ('password', 'password_hash')}

    def register_user(self, data):
        email = data.get('email')
        if self.user_repo.get_by_email(email):
            return False, "Email already exists"

        hashed = generate_password_hash(data.get('password'))

        new_user = {
            'name': data.get('name'),
            'email': email,
            'password_hash': hashed,
            'role': data.get('role', 'user'),
        }

        user = self.user_repo.create(new_user)

        if not user:
            return False, "Registration failed"

        return True, self._clean(user)

    def authenticate_user(self, email, password):
        user = self.user_repo.get_by_email(email)

        if user and user.get('password_hash') and check_password_hash(
            user.get('password_hash'), password
        ):
            return True, self._clean(user)

        return False, "Invalid credentials"

    def get_user_by_id(self, user_id):
        return self._clean(self.user_repo.get_by_id(user_id))