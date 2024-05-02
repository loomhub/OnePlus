from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.transaction_dto import transactionQueryEmail, transactionQueryPrimaryKey, transactionQueryUpdateFlag,transactionsListDTO, transactionsDelListDTO, transactionDTO
from ..database.db import get_session
from ..repositories.transaction_repository import transactionRepository
from ..services.transaction_service import transactionService
from ..services.transaction_filehandler import transactionFileHandler
from ..models.transactions_model import transactionsModel
import logging

# DEFINITIONS
get_pkey="/transactions/pkey"
get_all=post_all="/transactions"
send_transaction_report="/transactions/email"
del_all = "/transactionsdel"
excel_upload = "/transactionsxl"
myObjects="transactions"
get_response_model=transactionsListDTO
get_pkey_model = transactionDTO
del_response_model=transactionsDelListDTO
myModel=transactionsModel

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
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_transaction_report,
        summary="Send transaction report to email",
        description="Send transaction report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_transaction_report(
     query_params: transactionQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
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
    query_params: transactionQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    try:
        key_fields = {'bank_account_key': query_params.bank_account_key,
                        'tdate': query_params.tdate,
                        'description': query_params.description,
                        'details': query_params.details,
                        'amount': query_params.amount
                      }  # Adjust according to actual key fields
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
     query_params: transactionQueryUpdateFlag = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    results = []
    for record in input_data.transactions:
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                        'tdate': record.tdate,
                        'description': record.description,
                        'details': record.details,
                        'amount': record.amount
                          }  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields,update=query_params.update)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save transactions data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: transactionQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = transactionFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    results = []
    for record in input_data.transactions:
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                        'tdate': record.tdate,
                        'description': record.description,
                        'details': record.details,
                        'amount': record.amount
                          }  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields,update = query_params.update)
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
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    results = []
    for record in input_data.transactionsDel:   
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                        'tdate': record.tdate,
                        'description': record.description,
                        'details': record.details,
                        'amount': record.amount
                          }  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
