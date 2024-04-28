from datetime import date
from typing import Optional
from ..repositories.emailConfig_repository import emailConfigRepository
from ..dtos.emailConfig_dto import emailsConfigListDTO
from .myservice import MyService

class emailConfigService(MyService):
    def __init__(self, emailConfig_repository: emailConfigRepository):
        super().__init__(emailConfig_repository)
   
