from datetime import date
from typing import Optional
from ..repositories.oneplus_email_repository import BirdRepository
from ..dtos.llc_dto import llcsListDTO
from .myservice import MyService

class birdService(MyService):
    def __init__(self, bird_repository: BirdRepository):
        super().__init__(bird_repository)
   
class oneplus_mailService(MyService):
    def __init__(self, bird_repository: BirdRepository):
        super().__init__(bird_repository)
   