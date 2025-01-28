import mysql.connector

# Database connection settings
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Sininkii2305200",  # Replace with your MySQL password
        database="db_payment"
    )

# Query to fetch data from the users table
def fetch_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT user_id, username, email, created_at FROM users"
        cursor.execute(query)

        users = cursor.fetchall()
        for user in users:
            print(user)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Fetching users from the database:")
    fetch_users()