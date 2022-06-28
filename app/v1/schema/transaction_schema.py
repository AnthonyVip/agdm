from pydantic import BaseModel
from pydantic import Field


class Transaction(BaseModel):
    amount: float = Field(..., example=0.0)
    memo: str = Field(..., example="This is a memo")
    action_id: int = Field(..., example=1)


class TransactionUser(Transaction):
    user_id: int = Field(..., example=1)


class TransactionBalance(TransactionUser):
    old_balance: float = Field(..., example=0.0)
    new_balance: float = Field(..., example=0.0)
