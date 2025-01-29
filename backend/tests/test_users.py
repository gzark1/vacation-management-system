import unittest
import psycopg2
import random
import time
from database.connection import connect_db

class TestUserDatabase(unittest.TestCase):

    def setUp(self):
        """ Connect to test database before each test """
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """ Delete test users and rollback changes """
        self.cursor.execute("DELETE FROM users WHERE email LIKE 'testuser%@example.com';")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_create_user(self):
        """ Test inserting a new user into the database """
        # Generate a unique email and employee_code
        unique_suffix = str(int(time.time()))[-6:]  # Use timestamp to ensure uniqueness
        unique_email = f"testuser{unique_suffix}@example.com"
        unique_employee_code = str(random.randint(1000000, 9999999))
        self.cursor.execute(
            "INSERT INTO users (name, email, employee_code, password_hash, role) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            ("Test User", unique_email, unique_employee_code, "hashedpassword", "employee")
        )
        user_id = self.cursor.fetchone()[0]
        self.assertIsNotNone(user_id)

if __name__ == '__main__':
    unittest.main()
