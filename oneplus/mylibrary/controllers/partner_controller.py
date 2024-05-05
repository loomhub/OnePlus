
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.partner_dto import partnerQueryEmail, partnerQueryPrimaryKey, partnerQueryUpdateFlag,partnersListDTO, partnersDelListDTO, partnerDTO
from ..database.db import get_session
from ..repositories.partner_repository import partnerRepository
from ..services.partner_service import partnerService
from ..services.partner_filehandler import partnerFileHandler
from ..models.partners_model import partnersModel
import logging

# DEFINITIONS
get_pkey="/partners/pkey"
get_all=post_all="/partners"
send_partner_report="/partners/email"
del_all = "/partnersdel"
excel_upload = "/partnersxl"
myObjects="partners"
get_response_model=partnersListDTO
get_pkey_model = partnerDTO
del_response_model=partnersDelListDTO
myModel=partnersModel

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
    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_partner_report,
        summary="Send partner report to email",
        description="Send partner report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_partner_report(
     query_params: partnerQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)
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
    query_params: partnerQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)
    try:
        key_fields = {'partner': query_params.partner}  # Adjust according to actual key fields
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
     query_params: partnerQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.partners, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save partners data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: partnerQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)

    my_filehandler = partnerFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.partners, myModel, query_params.update,myObjects)
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
    my_repository = partnerRepository(db)
    my_service = partnerService(my_repository)
    results = []
    for record in input_data.partnersDel:   
        try:
            key_fields = {'partner': record.partner}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
