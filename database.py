import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT", 3306),
            ssl_verify_identity=False
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_users_table():
    """Creates the 'users' table in the database if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                patronymic VARCHAR(255),
                customer_phone VARCHAR(20) NOT NULL,
                contact_phone VARCHAR(20) NOT NULL,
                organization_name VARCHAR(255) NOT NULL,
                social_media_platform VARCHAR(50),
                social_media_handle VARCHAR(255)
            )
        """)
        print("Table 'users' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_user(user_data):
    """Adds a new user to the 'users' table."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO users (
                first_name, last_name, patronymic, customer_phone,
                contact_phone, organization_name, social_media_platform, social_media_handle
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            user_data['first_name'],
            user_data['last_name'],
            user_data['patronymic'],
            user_data['customer_phone'],
            user_data['contact_phone'],
            user_data['organization_name'],
            user_data['social_media_platform'],
            user_data['social_media_handle']
        ))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")
        conn.rollback()
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # This will be executed when the script is run directly
    # It's a good practice to create the table on the first run
    create_users_table()