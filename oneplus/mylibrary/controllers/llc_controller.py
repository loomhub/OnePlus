from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.llc_dto import LLCQueryParams, llcDTO, llcsListDTO, llcsDelListDTO, llcsListFullDTO
from ..database.db import get_session
from ..repositories.llc_repository import LLCRepository
from ..services.llc_service import llcService
from typing import Optional
import logging


router = APIRouter()

############################################################################################################
@router.get(
        "/",
        summary="Welcome message",
        description="Welcome message for the Oneplus API.",
        status_code=200,
        tags=["Root"],
        )
async def root():
    return {"message": "Welcome to Oneplus API!"}

############################################################################################################
@router.get(
        "/llcs",
        summary="Get LLCs",
        description="Get all LLCs from database",
        status_code=200,
        response_model=llcsListDTO,
        tags=["Get"],
        )

async def get_llcs(db: AsyncSession = Depends(get_session)):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    try:
        results = await llc_service.extract_llcs()
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"llcs":results}

############################################################################################################
@router.get(
        "/search/llcs",
        summary="Get LLCs by name and start date",
        description="Get LLCs from database by name and start date",
        status_code=200,
        response_model=llcsListDTO,
        tags=["Get"],
        )

async def get_llcs_by_name_and_date(
    query_params: LLCQueryParams = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    try:
        results = await llc_service.extract_llcs_by_name_and_date(query_params.llc_name, query_params.start_date)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"llcs":results}

############################################################################################################

@router.post(
        "/llcs",
        summary="Create or edit multiple LLCs",
        description="Create or edit multiple LLCs",
        tags=["Upsert"],
        )
async def create_or_update_llc(llcs_data: llcsListDTO, db: AsyncSession = Depends(get_session)):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    results = []
    for llc in llcs_data.llcs:
        try:
            created, result = await llc_service.create_or_update_llc(llc)
            results.append( {"created": created, "llc": result} )
        except Exception as e:
            logging.error(f"Failed to update or create LLC: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
@router.delete(
        "/llcsdel",
        summary="Delete multiple LLCs",
        description="Delete multiple LLCs",
        tags=["Delete"],
        )
async def delete_llc(llcs_data: llcsDelListDTO, db: AsyncSession = Depends(get_session)):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    results = []
    for llc in llcs_data.llcs:
        try:
            deleted, result = await llc_service.delete_llc(llc)
            results.append( {"deleted": deleted, "llc": result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(
        "/llcsxl",
        summary="Create or edit LLCs using excel file",
        description="Create or edit LLCs using excel file",
        tags=["Upsert"],
        )
async def create_or_update_llc_excel(llc: llcDTO, db: AsyncSession = Depends(get_session)):
    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    try:
        created, result = await llc_service.create_or_update_llc(llc)
        return {"created": created, "llc": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
############################################################################################################
# ############################################################################################################
# @router.post(
#         "/llc",
#         summary="Create or edit LLC",
#         description="Create or edit LLC",
#         tags=["Upsert"],
#         )
# async def create_or_update_llc(llc: llcDTO, db: AsyncSession = Depends(get_session)):
#     llc_repository = LLCRepository(db)
#     llc_service = llcService(llc_repository)
#     try:
#         created, result = await llc_service.create_or_update_llc(llc)
#         return {"created": created, "llc": result}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
