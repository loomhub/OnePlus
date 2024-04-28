
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.emailConfig_dto import emailConfigQueryPrimaryKey,emailsConfigListDTO, emailsConfigDelListDTO, emailConfigDTO
from ..database.db import get_session
from ..repositories.emailConfig_repository import emailConfigRepository
from ..services.emailConfig_service import emailConfigService
from ..services.emailConfig_filehandler import emailConfigFileHandler
from ..models.emailConfig_model import emailsConfigModel
import logging

# DEFINITIONS
get_pkey="/emailsConfig/pkey"
get_all=post_all="/emailsConfig"
del_all = "/emailsConfigdel"
excel_upload = "/emailsConfigxl"
myObjects="emailsConfig"
get_response_model=emailsConfigListDTO
get_pkey_model = emailConfigDTO
del_response_model=emailsConfigDelListDTO
myModel=emailsConfigModel

router = APIRouter()

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
    my_repository = emailConfigRepository(db)
    my_service = emailConfigService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
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
    query_params: emailConfigQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = emailConfigRepository(db)
    my_service = emailConfigService(my_repository)
    try:
        key_fields = {'subject': query_params.subject}  # Adjust according to actual key fields
        result = await my_service.extract_pkey(myModel,key_fields)
        if result is None:
            return {}
        return result
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

############################################################################################################
@router.post(
        post_all,
        summary="Create or edit multiple records",
        description="Create or edit multiple records",
        tags=["Upsert"],
        )
async def create_or_update_data(input_data: get_response_model, db: AsyncSession = Depends(get_session)):
    my_repository = emailConfigRepository(db)
    my_service = emailConfigService(my_repository)
    results = []
    for record in input_data.emailsConfig:
        try:
            key_fields = {'subject': record.subject}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save emailsConfig data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = emailConfigFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = emailConfigRepository(db)
    my_service = emailConfigService(my_repository)
    results = []
    for record in input_data.emailsConfig:
        try:
            key_fields = {'subject': record.subject}  # Adjust according to actual key fields
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
    my_repository = emailConfigRepository(db)
    my_service = emailConfigService(my_repository)
    results = []
    for record in input_data.emailsConfigDel:   
        try:
            key_fields = {'subject': record.subject}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
