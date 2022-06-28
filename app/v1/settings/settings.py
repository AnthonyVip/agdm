# -*- coding: UTF-8 -*
from os.path import dirname, abspath
import configparser


class Settings:
    """Clase que lee el settings.cfg para obtener
       los datos de conecion a db, con esto datos
       se arma y se retorna el diccionario db_dict"""
    def __init__(self):
        d = dirname(dirname(abspath(__file__)))
        _current_cfg = f"{d}/settings/settings.cfg"
        self.config = configparser.RawConfigParser()
        self.config.read(_current_cfg)
        self.db_dict = {'host': self.config.get('database', 'host'),
                        'user': self.config.get('database', 'user'),
                        'password': self.config.get('database', 'password'),
                        'db': self.config.get('database', 'db'),
                        'port': int(self.config.get('database', 'port'))}
        self.token_dict = {'secret_key': self.config.get('token',
                           'secret_key'),
                           'expires': self.config.get(
                                                      'token',
                                                      'access_token_expire')}
        self.mongo_dict = {'host': self.config.get('mongodb', 'host'),
                           'user': self.config.get('mongodb', 'user'),
                           'password': self.config.get('mongodb', 'password'),
                           'db': self.config.get('mongodb', 'db'),
                           'port': int(self.config.get('mongodb', 'port'))}

    @property
    def get_db_dict(self):
        return self.db_dict

    @property
    def get_token_dict(self):
        return self.token_dict

    @property
    def get_mongo_dict(self):
        return self.mongo_dict
