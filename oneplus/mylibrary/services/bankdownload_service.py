from ..repositories.bankdownload_repository import bankdownloadRepository
from .myservice import MyService

class bankdownloadService(MyService):
    def __init__(self, bankdownload_repository: bankdownloadRepository):
        super().__init__(bankdownload_repository)
   
