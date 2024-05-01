
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.vendor_dto import vendorQueryEmail, vendorQueryPrimaryKey,vendorsListDTO, vendorsDelListDTO, vendorDTO
from ..database.db import get_session
from ..repositories.vendor_repository import vendorRepository
from ..services.vendor_service import vendorService
from ..services.vendor_filehandler import vendorFileHandler
from ..models.vendor_model import vendorsModel
import logging

# DEFINITIONS
get_pkey="/vendors/pkey"
get_all=post_all="/vendors"
send_vendor_report="/vendors/email"
del_all = "/vendorsdel"
excel_upload = "/vendorsxl"
myObjects="vendors"
get_response_model=vendorsListDTO
get_pkey_model = vendorDTO
del_response_model=vendorsDelListDTO
myModel=vendorsModel

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
    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_vendor_report,
        summary="Send vendor report to email",
        description="Send vendor report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_vendor_report(
     query_params: vendorQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
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
    query_params: vendorQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
    try:
        key_fields = {'vendor': query_params.vendor}  # Adjust according to actual key fields
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
    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
    results = []
    for record in input_data.vendors:
        try:
            key_fields = {'vendor': record.vendor}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save vendors data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = vendorFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
    results = []
    for record in input_data.vendors:
        try:
            key_fields = {'vendor': record.vendor}  # Adjust according to actual key fields
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
    my_repository = vendorRepository(db)
    my_service = vendorService(my_repository)
    results = []
    for record in input_data.vendorsDel:   
        try:
            key_fields = {'vendor': record.vendor}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
