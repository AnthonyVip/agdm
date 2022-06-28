from app.v1.model.mongo_queries import TransactionQueries
from app.v1.model.user_queries import UserQueries
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from app.v1.schema.transaction_schema import TransactionBalance
from app.v1.schema.user_schema import UserProfile


class TransactionService:
    def __init__(self):
        self._transaction_class = TransactionQueries()
        self._user_class = UserQueries()

    def make_transaction(self, _transaction):
        _profile = self._user_class.get_profile(_transaction.user_id)
        if not _profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if _transaction.amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Amount must be greater than 0")

        if _transaction.action_id not in [1, 2]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Action must be Deposit or Withdraw")

        if not _transaction.memo:
            _transaction.memo = ""

        if _transaction.action_id == 2:
            if _transaction.amount > _profile.balance:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Insufficient balance")

        old_balance, new_balance = self._user_class.update_balance(_transaction.user_id,    # noqa:E501
                                                                   _transaction.amount,     # noqa:E501
                                                                   _transaction.action_id)  # noqa:E501

        _transaction_balance = TransactionBalance(amount=_transaction.amount,
                                                  old_balance=old_balance,
                                                  new_balance=new_balance,
                                                  memo=_transaction.memo,
                                                  action_id=_transaction.action_id,  # noqa:E501
                                                  user_id=_transaction.user_id)

        make_transaction = self._transaction_class.add_transaction(_transaction_balance)  # noqa:E501
        if not make_transaction:
            self._user_class.rollback_balance(_transaction.user_id,
                                              old_balance)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Transaction failed")

        _new_profile = UserProfile(user_id=_transaction.user_id,
                                   balance=new_balance)

        return _new_profile

    def get_transactions(self, _user_id: int,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None):
        _transaction = self._transaction_class.get_transaction(_user_id,
                                                               start_date,
                                                               end_date)

        return _transaction
