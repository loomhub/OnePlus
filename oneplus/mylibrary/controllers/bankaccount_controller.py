
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.bankaccount_dto import bankaccountQueryEmail, bankaccountQueryPrimaryKey,bankaccountsListDTO, bankaccountsDelListDTO, bankaccountDTO
from ..database.db import get_session
from ..repositories.bankaccount_repository import bankaccountRepository
from ..services.bankaccount_service import bankaccountService
from ..services.bankaccount_filehandler import bankaccountFileHandler
from ..models.bankaccounts_model import bankaccountsModel
import logging

# DEFINITIONS
get_pkey="/bankaccounts/pkey"
get_all=post_all="/bankaccounts"
send_bankaccount_report="/bankaccounts/email"
del_all = "/bankaccountsdel"
excel_upload = "/bankaccountsxl"
myObjects="bankaccounts"
get_response_model=bankaccountsListDTO
get_pkey_model = bankaccountDTO
del_response_model=bankaccountsDelListDTO
myModel=bankaccountsModel

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
    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_bankaccount_report,
        summary="Send bankaccount report to email",
        description="Send bankaccount report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_bankaccount_report(
     query_params: bankaccountQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
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
    query_params: bankaccountQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
    try:
        key_fields = {'bank': query_params.bank,
                      'account_type':query_params.account_type,
                      'account_number':query_params.account_number}  # Adjust according to actual key fields
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
    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
    results = []
    for record in input_data.bankaccounts:
        try:
            key_fields = {'bank': record.bank,
                      'account_type':record.account_type,
                      'account_number':record.account_number}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save bankaccounts data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = bankaccountFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
    results = []
    for record in input_data.bankaccounts:
        try:
            key_fields = {'bank': record.bank,
                      'account_type':record.account_type,
                      'account_number':record.account_number}  # Adjust according to actual key fields
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
    my_repository = bankaccountRepository(db)
    my_service = bankaccountService(my_repository)
    results = []
    for record in input_data.bankaccountsDel:   
        try:
            key_fields = {'bank': record.bank,
                      'account_type':record.account_type,
                      'account_number':record.account_number}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
