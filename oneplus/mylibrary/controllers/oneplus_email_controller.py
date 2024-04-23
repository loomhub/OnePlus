from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.oneplus_email_dto import birdListDTO, birdsDelListDTO
from ..database.db import get_session
from ..repositories.oneplus_email_repository import BirdRepository
from ..services.oneplus_email import birdService
from ..models.oneplus_email_model import Birds
import logging


router = APIRouter()

############################################################################################################
@router.post(
        "/birds",
        summary="Create or edit multiple birds",
        description="Create or edit birds",
        tags=["Upsert"],
        )
async def create_or_update_bird(birds_data: birdListDTO, db: AsyncSession = Depends(get_session)):
    bird_repository = BirdRepository(db)
    bird_service = birdService(bird_repository)
    results = []
    for bird in birds_data.birds:
        try:
            key_fields = {'sender': bird.sender}  # Adjust according to actual key fields
            created, result = await bird_service.upsert_records(bird, Birds, key_fields)
            results.append( {"created": created, "bird": result} )
        except Exception as e:
            logging.error(f"Failed to update or create Bird: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.delete(
        "/birddel",
        summary="Delete multiple Birds",
        description="Delete multiple Birds",
        tags=["Delete"],
        )
async def delete_llc(birds_data: birdsDelListDTO, db: AsyncSession = Depends(get_session)):
    bird_repository = BirdRepository(db)
    bird_service = birdService(bird_repository)
    results = []
    for bird in birds_data.birds:
        try:
            key_fields = {'sender': bird.sender}  # Adjust according to actual key fields
            deleted = await bird_service.delete_records(bird, Birds, key_fields)
            results.append( {"deleted": deleted} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
