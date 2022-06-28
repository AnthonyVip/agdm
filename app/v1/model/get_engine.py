# -*- coding: UTF-8 -*
from sqlmodel import create_engine
from app.v1.settings.settings import Settings
from app.v1.utils.singleton import singleton


@singleton
class CreateEngine():
    def __init__(self) -> None:
        self._settings = Settings()
        self._db_dict = self._settings.get_db_dict

    def __open__(self):
        self.engine = create_engine(f'postgresql+psycopg2://{self._db_dict["user"]}:{self._db_dict["password"]}@{self._db_dict["host"]}:{self._db_dict["port"]}/{self._db_dict["db"]}')  # noqa: E501
        return self.engine
