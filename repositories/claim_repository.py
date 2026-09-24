from database.db import get_db_connection
import mysql.connector

class ClaimRepository:
    def create_claim(self, match_id, claimant_id, verification_answer):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO claims (match_id, claimant_id, verification_answer, status)
                VALUES (%s, %s, %s, 'pending')
            """
            cursor.execute(query, (match_id, claimant_id, verification_answer))
            connection.commit()
            return {"claim_id": cursor.lastrowid, "status": "pending"}
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error creating claim: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def get_claims(self, user_id=None, role='user'):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            if role == 'admin':
                query = "SELECT * FROM claims ORDER BY created_at DESC"
                cursor.execute(query)
            else:
                query = "SELECT * FROM claims WHERE claimant_id = %s ORDER BY created_at DESC"
                cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def update_claim_status(self, claim_id, status):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            connection.start_transaction()
            
            # Update claim status
            query = "UPDATE claims SET status = %s, reviewed_at = CURRENT_TIMESTAMP WHERE claim_id = %s"
            cursor.execute(query, (status, claim_id))
            
            if status == 'approved':
                # If approved, update item statuses
                cursor.execute("SELECT match_id FROM claims WHERE claim_id = %s", (claim_id,))
                match = cursor.fetchone()
                if match:
                    cursor.execute("SELECT lost_id, found_id FROM matches WHERE match_id = %s", (match[0],))
                    ids = cursor.fetchone()
                    if ids:
                        cursor.execute("UPDATE lost_items SET status = 'claimed' WHERE lost_id = %s", (ids[0],))
                        cursor.execute("UPDATE found_items SET status = 'claimed' WHERE found_id = %s", (ids[1],))
            
            connection.commit()
            return True
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error updating claim: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    def create_return(self, claim_id, returned_by, received_by, confirmation):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            connection.start_transaction()
            
            # 1. Create return record
            query = """
                INSERT INTO returns (claim_id, returned_by, received_by, confirmation)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (claim_id, returned_by, received_by, confirmation))
            
            # 2. Update item status to 'returned'
            cursor.execute("SELECT match_id FROM claims WHERE claim_id = %s", (claim_id,))
            match = cursor.fetchone()
            if match:
                cursor.execute("SELECT lost_id, found_id FROM matches WHERE match_id = %s", (match[0],))
                ids = cursor.fetchone()
                if ids:
                    cursor.execute("UPDATE lost_items SET status = 'returned' WHERE lost_id = %s", (ids[0],))
                    cursor.execute("UPDATE found_items SET status = 'returned' WHERE found_id = %s", (ids[1],))
            
            # 3. Create notification for the user who received the item
            notif_query = """
                INSERT INTO notifications (user_id, title, message, notification_type)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(notif_query, (received_by, "Item Returned", "Your item has been successfully returned.", "return"))
            
            connection.commit()
            return True
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error in return process: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
