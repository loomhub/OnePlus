from ..repositories.sample_repository import sampleRepository
from .myservice import MyService

class sampleService(MyService):
    def __init__(self, sample_repository: sampleRepository):
        super().__init__(sample_repository)
   
