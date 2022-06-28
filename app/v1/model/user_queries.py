from sqlmodel import Session, select
from app.v1.model.get_engine import CreateEngine
from app.v1.model.user_model import User, Profile
from app.v1.schema.user_schema import UserRegister
from app.v1.scripts.helper_encrypt import HelperEncrypt
import datetime
from decimal import Decimal


class UserQueries:
    def __init__(self):
        self.EngineClass = CreateEngine()
        self.EncryptClass = HelperEncrypt()
        self.__engine__ = self.EngineClass.__open__()

    def check_username(self, username: str):
        with Session(self.__engine__) as session:
            statement = select(User).where(User.username == username)
            results = session.exec(statement)
            _user = results.first()
            return _user

    def check_email(self, email: str):
        with Session(self.__engine__) as session:
            statement = select(User).where(User.email == email)
            results = session.exec(statement)
            _user = results.first()
            return _user

    def create_user(self, user: UserRegister):
        with Session(self.__engine__) as session:
            session.add(User(username=user.username, email=user.email,
                             password=self.EncryptClass.get_password_hash(user.password),  # noqa: E501
                             is_active=1, last_login=datetime.datetime.utcnow))
            session.commit()
            _user = self.check_username(user.username)
            if _user:
                session.add(Profile(user_id=_user.id, balance=0.00))
                session.commit()
        return _user

    def update_login(self, user_id: int):
        with Session(self.__engine__) as session:
            statement = select(User).where(User.id == user_id)
            try:
                results = session.exec(statement)
                _user = results.one()
                _user.last_login = datetime.datetime.utcnow()
                session.add(_user)
                session.commit()
                return True
            except Exception:
                return False

    def get_profile(self, user_id: int):
        with Session(self.__engine__) as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            try:
                results = session.exec(statement)
                _profile = results.one()
                return _profile
            except Exception:
                return False

    def update_balance(self, user_id: int, amount: float, action_id: int):
        old_balance = 0.00
        new_balance = 0.00
        with Session(self.__engine__) as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            results = session.exec(statement)
            _profile = results.one()
            old_balance = _profile.balance
            amount = Decimal(amount)
            if action_id == 1:
                _profile.balance += amount
                new_balance = old_balance + amount
            elif action_id == 2:
                _profile.balance -= amount
                new_balance = old_balance - amount
            session.add(_profile)
            session.commit()
        return old_balance, new_balance

    def rollback_balance(self, user_id: int, old_balance: float):
        _new_balance = 0.00
        with Session(self.__engine__) as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            results = session.exec(statement)
            _profile = results.one()
            _profile.balance = old_balance
            session.add(_profile)
            session.commit()
            _new_balance = _profile.balance
        return _new_balance
