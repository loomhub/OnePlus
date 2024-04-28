from datetime import date
from typing import Optional
from ..repositories.sample_repository import sampleRepository
from ..dtos.sample_dto import samplesListDTO
from .myservice import MyService

class sampleService(MyService):
    def __init__(self, sample_repository: sampleRepository):
        super().__init__(sample_repository)
   
