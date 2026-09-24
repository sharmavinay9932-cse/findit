from database.db import get_db_connection
import mysql.connector

class UserRepository:
    def get_by_email(self, email):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                # Rename user_id to id to maintain compatibility with existing frontend
                user['id'] = user.pop('user_id')
            return user
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, user_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                user['id'] = user.pop('user_id')
            return user
        finally:
            cursor.close()
            connection.close()

    def create(self, user_data):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """
            values = (
                user_data.get('name'),
                user_data.get('email'),
                user_data.get('password'),
                user_data.get('role', 'user')
            )
            cursor.execute(query, values)
            connection.commit()
            
            user_id = cursor.lastrowid
            
            # Fetch the newly created user
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                user['id'] = user.pop('user_id')
            return user
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error creating user: {err}")
            return None
        finally:
            cursor.close()
            connection.close()
