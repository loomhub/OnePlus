from ..repositories.balance_repository import balanceRepository
from .myservice import MyService

class balanceService(MyService):
    def __init__(self, balance_repository: balanceRepository):
        super().__init__(balance_repository)
   
