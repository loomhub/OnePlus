
from ..repositories.bird_repository import birdRepository
from .myservice import MyService

class birdService(MyService):
    def __init__(self, bird_repository: birdRepository):
        super().__init__(bird_repository)
   
