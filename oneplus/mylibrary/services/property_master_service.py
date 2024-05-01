from ..repositories.property_master_repository import propertyMasterRepository
from .myservice import MyService

class propertyMasterService(MyService):
    def __init__(self, propertyMaster_repository: propertyMasterRepository):
        super().__init__(propertyMaster_repository)
   
