from database.db import get_db_connection
import mysql.connector

class MatchRepository:
    def get_by_lost_item_id(self, lost_item_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT m.*, 
                       f.item_name as found_name,
                       img.image_path as found_image,
                       l.location_name as found_location,
                       f.date_found,
                       f.status as found_status
                FROM matches m
                JOIN found_items f ON m.found_id = f.found_id
                LEFT JOIN locations l ON f.location_id = l.location_id
                LEFT JOIN item_images img ON f.found_id = img.found_id
                WHERE m.lost_id = %s
                ORDER BY m.match_score DESC
            """
            cursor.execute(query, (lost_item_id,))
            rows = cursor.fetchall()
            
            # Format the data to match the frontend expectations
            formatted_matches = []
            for row in rows:
                score = float(row['match_score'])
                classification = "Strong potential match" if score >= 80 else "Possible match" if score >= 60 else "Low similarity"
                
                formatted_matches.append({
                    'id': row['match_id'],
                    'lost_item_id': row['lost_id'],
                    'found_item_id': row['found_id'],
                    'score': score,
                    'classification': classification,
                    'status': row['status'],
                    'found_item': {
                        'id': row['found_id'],
                        'name': row['found_name'],
                        'image': row['found_image'],
                        'location': row['found_location'],
                        'date': str(row['date_found']),
                        'type': 'found'
                    }
                })
            return formatted_matches
        finally:
            cursor.close()
            connection.close()

    def upsert_match(self, lost_id, found_id, score):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Using INSERT ... ON DUPLICATE KEY UPDATE for MySQL
            query = """
                INSERT INTO matches (lost_id, found_id, match_score, status)
                VALUES (%s, %s, %s, 'potential')
                ON DUPLICATE KEY UPDATE match_score = VALUES(match_score)
            """
            cursor.execute(query, (lost_id, found_id, score))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error upserting match: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
