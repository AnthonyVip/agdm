from mongoengine import Document, IntField, DecimalField
from mongoengine import DateTimeField, StringField
from app.v1.model.get_mongo_engine import CreateMongoEngine

EngineClass = CreateMongoEngine()
ENGINE = EngineClass.__open__()


class Transaction(Document):
    user_id = IntField(required=True)
    amount = DecimalField(required=True, precision=6)
    old_balance = DecimalField(required=True, precision=6)
    new_balance = DecimalField(required=True, precision=6)
    date = DateTimeField(required=True)
    memo = StringField(required=True)
    action_id = IntField(required=True)
    meta = {'collection': 'transactions'}


class Action(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    meta = {'collection': 'actions'}
