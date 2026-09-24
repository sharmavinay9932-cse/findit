from database.db import get_db_connection
import mysql.connector

class ItemRepository:
    def __init__(self, type='lost'):
        self.type = type
        self.table_name = 'lost_items' if type == 'lost' else 'found_items'
        self.id_col = 'lost_id' if type == 'lost' else 'found_id'

    def _get_category_id(self, cursor, category_name):
        cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
        res = cursor.fetchone()
        if res:
            return res['category_id']
        # If category doesn't exist, use 'Other'
        cursor.execute("SELECT category_id FROM categories WHERE category_name = 'Other'")
        res = cursor.fetchone()
        return res['category_id'] if res else 1

    def _get_or_create_location(self, cursor, location_name):
        cursor.execute("SELECT location_id FROM locations WHERE location_name = %s", (location_name,))
        res = cursor.fetchone()
        if res:
            return res['location_id']
        
        cursor.execute("INSERT INTO locations (location_name) VALUES (%s)", (location_name,))
        return cursor.lastrowid

    def _format_item(self, row):
        if not row:
            return None
            
        return {
            'id': row[self.id_col],
            'user_id': row['user_id'],
            'name': row['item_name'],
            'category': row.get('category_name', ''),
            'brand': row['brand'],
            'color': row['color'],
            'location': row.get('location_name', ''),
            'date': str(row[f'date_{self.type}']),
            'time': str(row[f'time_{self.type}']) if row[f'time_{self.type}'] else '',
            'description': row['description'],
            'unique_features': row['identifying_features'],
            'status': row['status'],
            'created_at': str(row['created_at']),
            'type': self.type,
            'image': row.get('image_path')
        }

    def get_by_user_id(self, user_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = f"""
                SELECT i.*, c.category_name, l.location_name, img.image_path
                FROM {self.table_name} i
                LEFT JOIN categories c ON i.category_id = c.category_id
                LEFT JOIN locations l ON i.location_id = l.location_id
                LEFT JOIN item_images img ON i.{self.id_col} = img.{self.id_col}
                WHERE i.user_id = %s
                ORDER BY i.created_at DESC
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return [self._format_item(row) for row in rows]
        finally:
            cursor.close()
            connection.close()
            
    def get_all(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = f"""
                SELECT i.*, c.category_name, l.location_name, img.image_path
                FROM {self.table_name} i
                LEFT JOIN categories c ON i.category_id = c.category_id
                LEFT JOIN locations l ON i.location_id = l.location_id
                LEFT JOIN item_images img ON i.{self.id_col} = img.{self.id_col}
                ORDER BY i.created_at DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._format_item(row) for row in rows]
        finally:
            cursor.close()
            connection.close()
            
    def get_by_id(self, item_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = f"""
                SELECT i.*, c.category_name, l.location_name, img.image_path
                FROM {self.table_name} i
                LEFT JOIN categories c ON i.category_id = c.category_id
                LEFT JOIN locations l ON i.location_id = l.location_id
                LEFT JOIN item_images img ON i.{self.id_col} = img.{self.id_col}
                WHERE i.{self.id_col} = %s
            """
            cursor.execute(query, (item_id,))
            row = cursor.fetchone()
            return self._format_item(row)
        finally:
            cursor.close()
            connection.close()

    def create(self, item):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            connection.start_transaction()
            
            category_id = self._get_category_id(cursor, item.get('category'))
            location_id = self._get_or_create_location(cursor, item.get('location'))
            
            query = f"""
                INSERT INTO {self.table_name} 
                (user_id, category_id, location_id, item_name, brand, color, description, identifying_features, date_{self.type}, time_{self.type}, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Handle empty time strings from frontend
            time_val = item.get('time')
            if not time_val:
                time_val = None
                
            values = (
                item.get('user_id'),
                category_id,
                location_id,
                item.get('name'),
                item.get('brand'),
                item.get('color'),
                item.get('description'),
                item.get('unique_features'),
                item.get('date'),
                time_val,
                'active' # Default status
            )
            cursor.execute(query, values)
            item_id = cursor.lastrowid
            
            # Insert image if present
            image_filename = item.get('image')
            if image_filename:
                img_query = f"""
                    INSERT INTO item_images ({self.id_col}, image_path)
                    VALUES (%s, %s)
                """
                cursor.execute(img_query, (item_id, image_filename))
            
            connection.commit()
            
            return self.get_by_id(item_id)
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error creating item: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def update(self, item_id, updated_item):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # We only support updating status right now based on frontend needs, 
            # but can extend if necessary.
            if 'status' in updated_item:
                status = updated_item['status']
                if status == 'reported':
                    status = 'active'
                    
                query = f"UPDATE {self.table_name} SET status = %s WHERE {self.id_col} = %s"
                cursor.execute(query, (status, item_id))
                connection.commit()
            return self.get_by_id(item_id)
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error updating item: {err}")
            return None
        finally:
            cursor.close()
            connection.close()
            
    def delete(self, item_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = f"DELETE FROM {self.table_name} WHERE {self.id_col} = %s"
            cursor.execute(query, (item_id,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error deleting item: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
