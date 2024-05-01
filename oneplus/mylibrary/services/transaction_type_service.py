from ..repositories.transaction_type_repository import transactionTypeRepository
from .myservice import MyService

class transactionTypeService(MyService):
    def __init__(self, transactionType_repository: transactionTypeRepository):
        super().__init__(transactionType_repository)
   
