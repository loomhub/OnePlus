from ..repositories.vendor_repository import vendorRepository
from .myservice import MyService

class vendorService(MyService):
    def __init__(self, vendor_repository: vendorRepository):
        super().__init__(vendor_repository)
   
