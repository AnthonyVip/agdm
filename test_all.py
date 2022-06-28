from app.v1.model.user_queries import UserQueries
from app.v1.service.auth_service import AuthService
import unittest
from decimal import Decimal
from fastapi.testclient import TestClient
from main import app


class TestUserQuerys(unittest.TestCase):
    """
    ## Unit test for UserQuerys class
    actual test:
    - check_username
    - check_email
    - get_profile
    - update_balance
    - rollback_balance
    - update_login
    """
    @classmethod
    def setUpClass(cls):
        cls.QueryClass = UserQueries()
        cls.username_true = "devuser"
        cls.username_false = "otrouser"
        cls.email_true = "email@mattilda.io"
        cls.email_false = "othermail.com"
        cls.profile_true = 1
        cls.profile_false = 0

    def test_check_username(self):
        self.assertTrue(self.QueryClass.check_username(self.username_true))
        self.assertFalse(self.QueryClass.check_username(self.username_false))

    def test_check_email(self):
        self.assertTrue(self.QueryClass.check_email(self.email_true))
        self.assertFalse(self.QueryClass.check_email(self.email_false))

    def test_get_profile(self):
        self.assertTrue(self.QueryClass.get_profile(self.profile_true))
        self.assertFalse(self.QueryClass.get_profile(self.profile_false))

    def test_update_balance(self):
        _actual_balance = self.QueryClass.get_profile(self.profile_true).balance  # noqa: E501
        _amount = Decimal(2.00)
        _action = 1
        _final_balance = _actual_balance + _amount
        _old_balance, _new_balance = self.QueryClass.update_balance(self.profile_true, _amount, _action)  # noqa: E501
        self.assertEqual(_new_balance, _final_balance)
        self.assertEqual(_old_balance, _actual_balance)

    def test_rollback_balance(self):
        _old_balance = 10.00
        _new_balance = self.QueryClass.rollback_balance(self.profile_true, _old_balance)  # noqa: E501
        self.assertEqual(_old_balance, _new_balance)

    def test_update_login(self):
        _old_update = self.QueryClass.check_username(self.username_true).last_login  # noqa: E501
        _new_update = self.QueryClass.update_login(self.profile_true)
        self.assertNotEqual(_old_update, _new_update)


class TestAuthService(unittest.TestCase):
    """
    ## Unit test for AuthService class
    actual test:
    """
    @classmethod
    def setUpClass(cls):
        cls.AuthClass = AuthService()
        cls.username_true = "devuser"
        cls.username_false = "otrouser"
        cls.password_true = "test1234"
        cls.password_false = "test1235"

    def test_authenticate_user(self):
        self.assertTrue(self.AuthClass.authenticate_user(self.username_true, self.password_true))  # noqa: E501
        self.assertFalse(self.AuthClass.authenticate_user(self.username_false, self.password_false))  # noqa: E501


class TestEndpoints(unittest.TestCase):
    """
    ## Unit test for endpoints
    actual test:
    - test_login_for_access_token
    """
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.username_true = "devuser"
        cls.username_false = "otrouser"
        cls.password_true = "test1234"
        cls.password_false = "test1235"
        cls.AuthClass = AuthService()

    def test_login_for_access_token(self):
        response = self.client.post("/api/v1/user/login/", json={"username": self.username_true, "password": self.password_true})  # noqa: E501
        self.assertEqual(response.status_code, 200)
        bad_response = self.client.post("/api/v1/user/login/", json={"username": self.username_false, "password": self.password_false})  # noqa: E501
        self.assertEqual(bad_response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
