"""
Handles database connection for the application.

Retrieves database credentials from environment variables to establish a 
secure connection with a PostgreSQL database.

Functions:
    connect_db(): Establishes a connection and returns a connection object.
"""

import os
import psycopg2

# Load environment variables with default values for local development
DB_NAME = os.getenv("DB_NAME", "vacation_portal")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

# PostgreSQL connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def connect_db():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        psycopg2.extensions.connection: Database connection object if successful.
        None: If the connection fails.

    Raises:
        psycopg2.DatabaseError: If an issue occurs while connecting.
    """
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.DatabaseError as error:
        print(f"Database connection failed: {error}")
        return None
