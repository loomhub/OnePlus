from ..repositories.bankaccount_repository import bankaccountRepository
from .myservice import MyService

class bankaccountService(MyService):
    def __init__(self, bankaccount_repository: bankaccountRepository):
        super().__init__(bankaccount_repository)
   
