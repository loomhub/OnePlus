from datetime import date
from typing import Optional
from pydantic import BaseModel
import logging
from ..repositories.llc_repository import LLCRepository
from ..models.llc_model import Llcs
from ..dtos.llc_dto import llcDTO, llcsDelListDTO, llcsListDTO

class llcService:
    def __init__(self, llc_repository: LLCRepository):
        self.llc_repository = llc_repository

############################################################################################################
    async def extract_llcs(self) -> llcsListDTO:
        """
        CGet LLC entities 
        :param 
        :return: list of llcs
        """
        try:
            return await self.llc_repository.retrieve_llcs()

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.llc_repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
    
############################################################################################################
    async def extract_llcs_by_name_and_date(
            self,
            llc_name:Optional[str] = None,
            start_date:Optional[date] = None) -> llcsListDTO:
        """
        CGet LLC entities 
        :param llc_name: Name of the LLC to filter by
        :param start_date: Query LLCs created on or after this date
        :return: list of llcs
        """
        try:
            return await self.llc_repository.retrieve_llcs_by_name_and_date(llc_name, start_date)

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.llc_repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
    
############################################################################################################
    async def create_or_update_llc(self, llc_data: llcDTO) -> tuple:
        """
        Create or update an LLC entity based on the provided data.
        :param llc_data: Data transfer object containing llc details
        :return: Tuple containing boolean (True if created, False if updated) and llc instance
        """
        try:
            llc_instance = await self.llc_repository.retrieve_llc_by_name(llc_data.llc)

            if llc_instance:
                llc_instance = await self.llc_repository.delete_llc(llc_instance)
             
            llc_instance = Llcs(
                    llc=llc_data.llc,
                    ein=llc_data.ein,
                    llc_address=llc_data.llc_address,
                    llc_description=llc_data.llc_description,
                    formation_date=llc_data.formation_date
                )
            llc_instance = await self.llc_repository.add_llc(llc_instance)
            created = True

            await self.llc_repository.commit_changes()
            return created, llc_instance

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.llc_repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
        
############################################################################################################    
    async def delete_llc(self, llc_data: llcsDelListDTO) -> tuple:
        """
        Delete an LLC entity based on the provided data.
        :param llc_data: Data transfer object containing llcs
        :return: Tuple containing boolean (True if deleted, False if not deleted) and llc instance
        """
        try:
            llc_instance = await self.llc_repository.retrieve_llc_by_name(llc_data.llc)

            if llc_instance:
                # LLC exists, delete it
                llc_instance = await self.llc_repository.delete_llc(llc_instance)
                deleted = True
            else:
                # LLC not found
                deleted = False
                
            await self.llc_repository.commit_changes()
            return deleted, llc_instance

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.llc_repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
