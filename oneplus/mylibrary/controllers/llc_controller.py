
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.llc_dto import LLCQueryParams, llcDTO, llcsListDTO, llcsDelListDTO
from ..database.db import get_session
from ..repositories.llc_repository import LLCRepository
from ..services.llc_service import llcService
from ..services.llc_filehandler import llcFileHandler
from ..models.llc_model import Llcs
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
        results = await llc_service.extract_all(Llcs)
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
            key_fields = {'llc': llc.llc}  # Adjust according to actual key fields
            created, result = await llc_service.upsert_records(llc, Llcs, key_fields)
            results.append( {"created": created, "llc": result} )
        except Exception as e:
            logging.error(f"Failed to update or create LLC: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post("/llcsxl", summary="Upload and save LLCs data from a CSV file")
async def upload_and_save_llc_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    llc_filehandler = llcFileHandler(file)
    llcs_data = llc_filehandler.extract_data_from_file()

    llc_repository = LLCRepository(db)
    llc_service = llcService(llc_repository)
    results = []
    for llc in llcs_data.llcs:
        try:
            key_fields = {'llc': llc.llc}  # Adjust according to actual key fields
            created, result = await llc_service.upsert_records(llc, Llcs, key_fields)
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
            #deleted, result = await llc_service.delete_llc(llc)
            key_fields = {'llc': llc.llc}  # Adjust according to actual key fields
            deleted = await llc_service.delete_records(llc, Llcs, key_fields)
            results.append( {"deleted": deleted} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
