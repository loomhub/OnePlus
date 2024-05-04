
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.property_master_dto import propertyMasterQueryEmail, propertyMasterQueryPrimaryKey, propertyMasterQueryUpdateFlag,propertyMastersListDTO, propertyMastersDelListDTO, propertyMasterDTO
from ..database.db import get_session
from ..repositories.property_master_repository import propertyMasterRepository
from ..services.property_master_service import propertyMasterService
from ..services.property_master_filehandler import propertyMasterFileHandler
from ..models.property_master_model import propertyMastersModel
from ..models.llcs_model import llcsModel

import logging

# DEFINITIONS
get_pkey="/propertyMasters/pkey"
get_all=post_all="/propertyMasters"
send_propertyMaster_report="/propertyMasters/email"
del_all = "/propertyMastersdel"
excel_upload = "/propertyMastersxl"
myObjects="propertyMasters"
get_response_model=propertyMastersListDTO
get_pkey_model = propertyMasterDTO
del_response_model=propertyMastersDelListDTO
myModel=propertyMastersModel

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
    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_propertyMaster_report,
        summary="Send propertyMaster report to email",
        description="Send propertyMaster report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_propertyMaster_report(
     query_params: propertyMasterQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
        sent = await my_service.send_email(results,get_all,receiver=query_params.receiver)
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
    query_params: propertyMasterQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)
    try:
        key_fields = {'property_name': query_params.property_name}  # Adjust according to actual key fields
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
     query_params: propertyMasterQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.propertyMasters, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save propertyMasters data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: propertyMasterQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)

    my_filehandler = propertyMasterFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.propertyMasters, myModel, query_params.update,myObjects)
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
    my_repository = propertyMasterRepository(db)
    my_service = propertyMasterService(my_repository)
    results = []
    for record in input_data.propertyMastersDel:   
        try:
            key_fields = {'property_name': record.property_name}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
