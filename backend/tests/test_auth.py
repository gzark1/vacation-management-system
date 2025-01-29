import unittest
import jwt
from api.auth import AuthService

class TestAuthService(unittest.TestCase):

    def test_generate_jwt(self):
        """ Test if JWT is generated properly """
        token = AuthService.generate_jwt(1, "manager")
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)

    def test_password_hashing(self):
        """ Test password hashing and verification """
        password = "securepassword"
        hashed_pw = AuthService.hash_password(password)
        self.assertTrue(AuthService.verify_password(password, hashed_pw))
        self.assertFalse(AuthService.verify_password("wrongpassword", hashed_pw))

if __name__ == '__main__':
    unittest.main()
