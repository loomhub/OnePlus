from pydantic import BaseModel
from ..repositories.llc_repository import LLCRepository
from ..models.llc_model import Llcs
from ..dtos.llc_dto import llcDTO

class llcService:
    def __init__(self, llc_repository: LLCRepository):
        self.llc_repository = llc_repository

    async def create_or_update_llc(self, llc_data: llcDTO) -> tuple:
        """
        Create or update an LLC entity based on the provided data.
        :param llc_data: Data transfer object containing llc details
        :return: Tuple containing boolean (True if created, False if updated) and llc instance
        """
        try:
            llc_instance = await self.llc_repository.get_llc_by_name(llc_data.llc)

            if llc_instance:
                # LLC exists, update it
                llc_instance.ein = llc_data.ein
                llc_instance.llc_address = llc_data.llc_address
                llc_instance.llc_description = llc_data.llc_description
                llc_instance.formation_date = llc_data.formation_date
                created = False
            else:
                # Create new LLC
                llc_instance = Llcs(
                    llc=llc_data.llc,
                    ein=llc_data.ein,
                    llc_address=llc_data.llc_address,
                    llc_description=llc_data.llc_description,
                    formation_date=llc_data.formstion_date
                )
                llc_instance = await self.llc_repository.add_llc(llc_instance)
                created = True

            await self.llc_repository.commit_changes()
            return created, llc_instance

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.llc_repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
