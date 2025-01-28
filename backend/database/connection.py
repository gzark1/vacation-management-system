import psycopg2

# Database connection string (keeping DB_NAME, HOST, and PORT fixed)
DATABASE_URL = f"postgresql://myuser:mypassword@db:5432/vacation_portal"

def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
