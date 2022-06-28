from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.v1.settings.settings import Settings
from app.v1.utils.utils_password import PasswordUtils
from app.v1.model.user_queries import UserQueries


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login_web/")


class AuthService:
    def __init__(self):
        self._settings = Settings()
        self._password_class = PasswordUtils()
        self._user_class = UserQueries()
        self._token_dict = self._settings.get_token_dict
        self._secret_key = self._token_dict['secret_key']
        self._expires = int(self._token_dict['expires'])
        self.algorithm = "HS256"

    def authenticate_user(self, username: str, password: str):
        user = self._user_class.check_username(username)
        if not user:
            return False

        if not self._password_class.verify_password(password, user.password):
            return False

        return user

    def create_access_token(self, data: dict,
                            expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode,
                                 self._secret_key,
                                 algorithm=self.algorithm)
        return encoded_jwt

    def generate_token(self, username, password):
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})

        access_token_expires = timedelta(minutes=self._expires)
        return self.create_access_token(data={"sub": user.username},
                                        expires_delta=access_token_expires)

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
                                              status_code=status.HTTP_401_UNAUTHORIZED,  # noqa: E501
                                              detail="Could not validate credentials",   # noqa: E501
                                              headers={"WWW-Authenticate": "Bearer"},)   # noqa: E501
        try:
            payload = jwt.decode(token,
                                 self._secret_key,
                                 algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self._user_class.check_username(username)
        if user is None:
            raise credentials_exception

        self._user_class.update_login(user.id)

        return user
