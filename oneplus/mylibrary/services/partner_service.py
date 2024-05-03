from ..repositories.partner_repository import partnerRepository
from .myservice import MyService

class partnerService(MyService):
    def __init__(self, partner_repository: partnerRepository):
        super().__init__(partner_repository)
   
