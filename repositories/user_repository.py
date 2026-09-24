"""
UserRepository — MySQL persistence for the users table.

Returns dicts with keys expected by the services/routes.
"""
from database.db import get_db_connection
import mysql.connector


def _format_user(row):
    """Map MySQL columns to application dictionary keys."""
    if not row:
        return None

    return {
        'id': row['user_id'],
        'name': row['name'],
        'email': row['email'],
        'password_hash': row['password_hash'],
        'role': row['role'],
        'created_at': str(row['created_at']),
    }


class UserRepository:

    def get_by_email(self, email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            return _format_user(cursor.fetchone())

        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (int(user_id),)
            )
            return _format_user(cursor.fetchone())

        finally:
            cursor.close()
            conn.close()

    def create(self, user_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (
                user_data.get('name'),
                user_data.get('email'),
                user_data.get('password_hash'),
                user_data.get('role', 'user'),
            ))

            conn.commit()
            new_id = cursor.lastrowid

            return self.get_by_id(new_id)

        except mysql.connector.Error as err:
            conn.rollback()
            print(f"[UserRepository] Error creating user: {err}")
            return None

        finally:
            cursor.close()
            conn.close()