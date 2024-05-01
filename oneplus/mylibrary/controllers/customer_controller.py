
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.customer_dto import customerQueryEmail, customerQueryPrimaryKey,customersListDTO, customersDelListDTO, customerDTO
from ..database.db import get_session
from ..repositories.customer_repository import customerRepository
from ..services.customer_service import customerService
from ..services.customer_filehandler import customerFileHandler
from ..models.customers_model import customersModel
import logging

# DEFINITIONS
get_pkey="/customers/pkey"
get_all=post_all="/customers"
send_customer_report="/customers/email"
del_all = "/customersdel"
excel_upload = "/customersxl"
myObjects="customers"
get_response_model=customersListDTO
get_pkey_model = customerDTO
del_response_model=customersDelListDTO
myModel=customersModel

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
    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_customer_report,
        summary="Send customer report to email",
        description="Send customer report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_customer_report(
     query_params: customerQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
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
    query_params: customerQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
    try:
        key_fields = {'customer': query_params.customer}  # Adjust according to actual key fields
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
    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
    results = []
    for record in input_data.customers:
        try:
            key_fields = {'customer': record.customer}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save customers data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = customerFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
    results = []
    for record in input_data.customers:
        try:
            key_fields = {'customer': record.customer}  # Adjust according to actual key fields
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
    my_repository = customerRepository(db)
    my_service = customerService(my_repository)
    results = []
    for record in input_data.customersDel:   
        try:
            key_fields = {'customer': record.customer}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
