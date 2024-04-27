from datetime import date
from typing import Optional
from ..repositories.sample_repository import sampleRepository
from ..dtos.sample_dto import samplesListDTO
from .myservice import MyService

class sampleService(MyService):
    def __init__(self, sample_repository: sampleRepository):
        super().__init__(sample_repository)
   
############################################################################################################
    async def extract_llcs_by_name_and_date(
            self,
            llc_name:Optional[str] = None,
            start_date:Optional[date] = None) -> samplesListDTO:
        """
        CGet LLC entities 
        :param llc_name: Name of the LLC to filter by
        :param start_date: Query LLCs created on or after this date
        :return: list of llcs
        """
        try:
            return await self.repository.retrieve_llcs_by_name_and_date(llc_name, start_date)

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
    
############################################################################################################
