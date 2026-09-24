import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "findit_db"),
}

# Create a connection pool to avoid creating new connections constantly
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="findit_pool",
        pool_size=5,
        pool_reset_session=True,
        **dbconfig
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

def get_db_connection():
    if not connection_pool:
        # Fallback to direct connection if pool fails
        return mysql.connector.connect(**dbconfig)
    return connection_pool.get_connection()
