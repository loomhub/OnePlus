from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.llc_dto import llcDTO
from ..database.db import get_session
from ..repositories.llc_repository import LLCRepository
from ..services.llc_service import llcService


router = APIRouter()

@router.get(
        "/",
        summary="Welcome message",
        description="Welcome message for the Oneplus API.",
        status_code=200,
        tags=["Root"],
        )
async def root():
    return {"message": "Welcome to Oneplus API!"}


@router.post(
        "/llcs",
        summary="Create or edit LLCs",
        description="Create or edit LLCs",
        tags=["Upsert"],
        )
async def create_or_update_llc(llc: llcDTO, db: AsyncSession = Depends(get_session)):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    try:
        created, result = await llc_service.create_or_update_llc(llc)
        return {"created": created, "llc": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))