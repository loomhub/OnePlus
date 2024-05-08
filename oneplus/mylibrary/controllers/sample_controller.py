
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.sample_dto import sampleQueryPrimaryKey, sampleQueryUpdateFlag,samplesListDTO, samplesDelListDTO, sampleDTO
from ..dtos.service_dto import QueryEmail
from ..database.db import get_session
from ..repositories.sample_repository import sampleRepository
from ..services.sample_service import sampleService
from ..services.sample_filehandler import sampleFileHandler
from ..models.samples_model import samplesModel
import logging

# DEFINITIONS
get_pkey="/samples/pkey"
get_all=post_all="/samples"
send_sample_report="/samples/email"
del_all = "/samplesdel"
excel_upload = "/samplesxl"
myObjects="samples"
get_response_model=samplesListDTO
get_pkey_model = sampleDTO
del_response_model=samplesDelListDTO
myModel=samplesModel

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
    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_sample_report,
        summary="Send sample report to email",
        description="Send sample report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_sample_report(
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
        sent = await my_service.check_keyword_and_send_email(results,
                                                             get_all,
                                                             receiver=query_params.receiver,
                                                             keyword=query_params.keyword)
        if sent == False:
            results = []

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
    query_params: sampleQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)
    try:
        key_fields = {'primary': query_params.primary}  # Adjust according to actual key fields
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
async def create_or_update_data(
     input_data: get_response_model,
     query_params: sampleQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.samples, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save samples data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: sampleQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)

    my_filehandler = sampleFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.samples, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
############################################################################################################

@router.delete(
        del_all,
        summary="Delete multiple record",
        description="Delete multiple records",
        tags=["Delete"],
        )
async def delete_record(input_data: del_response_model, db: AsyncSession = Depends(get_session)):
    my_repository = sampleRepository(db)
    my_service = sampleService(my_repository)
    results = []
    for record in input_data.samplesDel:   
        try:
            key_fields = {'primary': record.primary}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
