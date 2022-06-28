from fastapi import APIRouter
from fastapi import Depends
from typing import List, Optional
from datetime import date
from app.v1.service.transaction_service import TransactionService
from app.v1.service.auth_service import AuthService
from app.v1.schema.transaction_schema import TransactionUser
from app.v1.schema.transaction_schema import TransactionBalance
from app.v1.schema.transaction_schema import Transaction as TransactionSchema
from app.v1.schema.user_schema import UserProfile, User


router = APIRouter(prefix="/api/v1")
auth_class = AuthService()


@router.post("/user/transaction/",
             tags=["transaction"],
             response_model=UserProfile)
def make_transaction(transaction: TransactionSchema,
                     current_user: User = Depends(auth_class.get_current_user)):  # noqa: E501
    """
    ## Create a new transaction

    ### Args
    The app can receive next fields by json data
    - amount: amount to deposit or withdraw
    - action_id: 1 for deposit and 2 for withdraw
    - memo: optional memo
    - need a valid token session

    ### Returns
    - user profile
    """
    TransactionClass = TransactionService()
    _transaction_schema = TransactionUser(user_id=current_user.id,
                                          amount=transaction.amount,
                                          memo=transaction.memo,
                                          action_id=transaction.action_id)
    return TransactionClass.make_transaction(_transaction_schema)


@router.post("/user/get_transactions/", tags=["get transactions"],
             response_model=List[TransactionBalance])
def get_transactions(start_date: Optional[date],
                     end_date: Optional[date],
                     current_user: User = Depends(auth_class.get_current_user)):  # noqa: E501
    """
    ## Get user transactions

    ### Args
    The app can receive next fields by json data
    - start_date in formtat YYYY-MM-DD
    - end_date in formtat YYYY-MM-DD
    - need a valid token session

    ### Returns
    list of user transactions
    """
    _list_transactions = []
    TransactionClass = TransactionService()
    _transactions = TransactionClass.get_transactions(current_user.id,
                                                      start_date, end_date)
    for _transaction in _transactions:
        _list_transactions.append(TransactionBalance(
                                  user_id=_transaction.user_id,
                                  amount=_transaction.amount,
                                  memo=_transaction.memo,
                                  action_id=_transaction.action_id,
                                  date=_transaction.date,
                                  old_balance=_transaction.old_balance,
                                  new_balance=_transaction.new_balance))
    return _list_transactions
