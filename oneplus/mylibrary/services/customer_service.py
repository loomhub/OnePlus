from ..repositories.customer_repository import customerRepository
from .myservice import MyService

class customerService(MyService):
    def __init__(self, customer_repository: customerRepository):
        super().__init__(customer_repository)
   
