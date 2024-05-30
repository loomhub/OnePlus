
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.cashflow_dto import cashflowQueryPrimaryKey, cashflowQueryUpdateFlag,cashflowsListDTO, cashflowsDelListDTO, cashflowDTO
from ..dtos.service_dto import QueryEmail
from ..database.db import get_session
from ..repositories.cashflow_repository import cashflowRepository
from ..services.cashflow_service import cashflowService
from ..services.cashflow_filehandler import cashflowFileHandler
from ..models.cashflows_model import cashflowsModel
import logging

# DEFINITIONS
get_pkey="/cashflows/pkey"
get_all=post_all="/cashflows"
send_cashflow_report="/cashflows/email"
del_all = "/cashflowsdel"
excel_upload = "/cashflowsxl"
myObjects="cashflows"
get_response_model=cashflowsListDTO
get_pkey_model = cashflowDTO
del_response_model=cashflowsDelListDTO
myModel=cashflowsModel

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
    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_cashflow_report,
        summary="Send cashflow report to email",
        description="Send cashflow report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_cashflow_report(
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)
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
    query_params: cashflowQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)
    try:
        key_fields = {'bank_account_key': query_params.bank_account_key,
                      'start_date': query_params.start_date,
                      'end_date': query_params.end_date}  # Adjust according to actual key fields
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
     query_params: cashflowQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.cashflows, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save cashflows data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: cashflowQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)

    my_filehandler = cashflowFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.cashflows, myModel, query_params.update,myObjects)
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
    my_repository = cashflowRepository(db)
    my_service = cashflowService(my_repository)
    results = []
    for record in input_data.cashflowsDel:   
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                      'start_date': record.start_date,
                      'end_date': record.end_date}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
