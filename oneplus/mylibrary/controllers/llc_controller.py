
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.llc_dto import LLCQueryParams,LLCQueryPrimaryKey,llcsListDTO, llcsDelListDTO, llcDTO
from ..database.db import get_session
from ..repositories.llc_repository import LLCRepository
from ..services.llc_service import llcService
from ..services.llc_filehandler import llcFileHandler
from ..models.llc_model import llcsModel
import logging

# DEFINITIONS
get_all=post_all="/llcs"
get_pkey="/llcs/pkey"
del_all = "/llcsdel"
excel_upload = "/llcsxl"
myObjects="llcs"
get_response_model=llcsListDTO
del_response_model=llcsDelListDTO
get_pkey_model = llcDTO
myModel=llcsModel

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
        get_all,
        summary="Get all records",
        description="Get all records from database",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def get_all_records(db: AsyncSession = Depends(get_session)):
    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
        sent = await my_service.send_email(results,get_all)
        print(sent)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        get_pkey,
        summary="Get record by primary key",
        description="Get record from database by primary key",
        status_code=200,
        response_model=get_pkey_model,
        tags=["Get"],
        )

async def get_record_by_pkey(
    query_params: LLCQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    try:
        key_fields = {'llc': query_params.llc_name}  # Adjust according to actual key fields
        result = await my_service.extract_pkey(myModel,key_fields)
        if result is None:
            return {}
        return result
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

############################################################################################################
@router.get(
        "/search/llcs",
        summary="Get LLCs by name and start date",
        description="Get LLCs from database by name and start date",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def get_llcs_by_name_and_date(
    query_params: LLCQueryParams = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    try:
        results = await my_service.extract_llcs_by_name_and_date(query_params.llc_name, query_params.start_date)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.post(
        post_all,
        summary="Create or edit multiple records",
        description="Create or edit multiple records",
        tags=["Upsert"],
        )
async def create_or_update_data(input_data: get_response_model, db: AsyncSession = Depends(get_session)):
    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    results = []
    for record in input_data.llcs:
        try:
            key_fields = {'llc': record.llc}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save LLCs data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = llcFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    results = []
    for record in input_data.llcs:
        try:
            key_fields = {'llc': record.llc}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
    
############################################################################################################

@router.delete(
        del_all,
        summary="Delete multiple record",
        description="Delete multiple records",
        tags=["Delete"],
        )
async def delete_record(input_data: del_response_model, db: AsyncSession = Depends(get_session)):
    my_repository = LLCRepository(db)
    my_service = llcService(my_repository)
    results = []
    for record in input_data.llcsDel:   
        try:
            key_fields = {'llc': record.llc}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
