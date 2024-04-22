
import os
import shutil
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.llc_dto import LLCQueryParams, llcDTO, llcsListDTO, llcsDelListDTO, llcsListFullDTO
from ..database.db import get_session
from ..repositories.llc_repository import LLCRepository
from ..services.llc_service import llcService
from ..services.llc_filehandler import llcFileHandler
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

################################################################################################################
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
@router.post("/upload_llcs_old", summary="Upload and save LLCs data from a CSV file")
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
            created, result = await llc_service.create_or_update_llc(llc)
            results.append( {"created": created, "llc": result} )
        except Exception as e:
            logging.error(f"Failed to update or create LLC: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
    

############################################################################################################
@router.post("/upload_llcs", summary="Upload, save, and load LLCs data from a CSV file")
async def upload_save_and_load_llc_file(file: UploadFile = File(...)):
    # Define the path where you want to save the file
    file_location = f"uploads/{file.filename}"

    # Check if the uploads directory exists, if not, create it
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Write the contents of the uploaded file to a new file in the server
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not write to file: {str(e)}")

    # Read the file into a DataFrame
    try:
        df = pd.read_csv(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load file into DataFrame: {str(e)}")

    return JSONResponse(status_code=200, content={"message": "File processed successfully", "data": df.to_dict(orient='records')})
    
############################################################################################################
@router.post(
        "/llcsxl",
        summary="Create or edit multiple LLCs using excel file",
        description="Create or edit multiple LLCs using excel file",
        tags=["Upsert"],
        )
async def create_or_update_llc_excel(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_session)):

    llc_filehandler = llcFileHandler(file)
    llcs_data = llc_filehandler.extract_data_from_file()
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
