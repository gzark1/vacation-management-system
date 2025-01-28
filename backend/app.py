from database.connection import connect_db

def check_db_connection():
    """ Test database connection using the existing `connect_db` function. """
    conn = connect_db()
    if conn:
        print("✅ Database connected successfully!")
        conn.close()
    else:
        print("🚨 Failed to connect to the database.")
        exit(1)

if __name__ == "__main__":
    check_db_connection()
