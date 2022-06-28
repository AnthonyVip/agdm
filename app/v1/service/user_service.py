from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.v1.schema.user_schema import UserRegister
from app.v1.model.user_queries import UserQueries


class CreateUser:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.QueryClass = UserQueries()

    def register_user(self, user: UserRegister):
        if self.QueryClass.check_username(user.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Username already exists")
        if self.QueryClass.check_email(user.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already exists")

        _user = self.QueryClass.create_user(user)
        return _user
