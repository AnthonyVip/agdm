# -*- coding: UTF-8 -*
from mongoengine import connect
from app.v1.settings.settings import Settings
from app.v1.utils.singleton import singleton


@singleton
class CreateMongoEngine():
    def __init__(self) -> None:
        self._settings = Settings()
        self._mongo_dict = self._settings.get_mongo_dict

    def __open__(self):
        self.engine = connect(host=self._mongo_dict['host'],
                              port=self._mongo_dict['port'],
                              username=self._mongo_dict['user'],
                              password=self._mongo_dict['password'],
                              db=self._mongo_dict['db'])
        return self.engine
