
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.balance_dto import balanceQueryEmail, balanceQueryPrimaryKey, balanceQueryUpdateFlag,balancesListDTO, balancesDelListDTO, balanceDTO
from ..database.db import get_session
from ..repositories.balance_repository import balanceRepository
from ..services.balance_service import balanceService
from ..services.balance_filehandler import balanceFileHandler
from ..models.balances_model import balancesModel
import logging

# DEFINITIONS
get_pkey="/balances/pkey"
get_all=post_all="/balances"
send_balance_report="/balances/email"
del_all = "/balancesdel"
excel_upload = "/balancesxl"
myObjects="balances"
get_response_model=balancesListDTO
get_pkey_model = balanceDTO
del_response_model=balancesDelListDTO
myModel=balancesModel

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
    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_balance_report,
        summary="Send balance report to email",
        description="Send balance report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_balance_report(
     query_params: balanceQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)
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
    query_params: balanceQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)
    try:
        key_fields = {'bank_account_key': query_params.bank_account_key,
                      'snapshot': query_params.snapshot}  # Adjust according to actual key fields
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
     query_params: balanceQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.balances, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save balances data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: balanceQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)

    my_filehandler = balanceFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.balances, myModel, query_params.update,myObjects)
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
    my_repository = balanceRepository(db)
    my_service = balanceService(my_repository)
    results = []
    for record in input_data.balancesDel:   
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                      'snapshot': record.snapshot}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
