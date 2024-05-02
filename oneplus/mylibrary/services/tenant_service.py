from ..repositories.tenant_repository import tenantRepository
from .myservice import MyService

class tenantService(MyService):
    def __init__(self, tenant_repository: tenantRepository):
        super().__init__(tenant_repository)
   
