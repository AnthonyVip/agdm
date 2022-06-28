from app.v1.model.transaction_model import Transaction, Action
from app.v1.schema.transaction_schema import Transaction as TransactionSchema
import datetime
from typing import Optional


class TransactionQueries:
    def add_actions(self):
        Action.objects.create(name='deposit',
                              description='the user has received a deposit')
        Action.objects.create(name='withdraw',
                              description='the user has make a  withdrawal')
        return True

    def add_transaction(self, transaction: TransactionSchema):
        try:
            Transaction.objects.create(user_id=transaction.user_id,
                                       amount=transaction.amount,
                                       old_balance=transaction.old_balance,
                                       new_balance=transaction.new_balance,
                                       date=datetime.datetime.utcnow(),
                                       memo=transaction.memo,
                                       action_id=transaction.action_id)
            return transaction
        except Exception:
            return False

    def get_transaction(self, user_id: int,
                        start_date: Optional[datetime.datetime],
                        end_date: Optional[datetime.datetime]):
        try:
            if start_date and end_date:
                transactions = Transaction.objects.filter(user_id=user_id,
                                                          date__gte=start_date,
                                                          date__lte=end_date)
            else:
                transactions = Transaction.objects.filter(user_id=user_id)
            return transactions
        except Exception:
            return False
