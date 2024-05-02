from ..repositories.transaction_repository import transactionRepository
from .myservice import MyService

class transactionService(MyService):
    def __init__(self, transaction_repository: transactionRepository):
        super().__init__(transaction_repository)