
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.bankdownload_dto import CHASE_COLUMNS, WELLSFARGO_COLUMNS, WELLSFARGO_FILEHEADERS, bankdownloadQueryEmail, bankdownloadQueryPrimaryKey, bankdownloadQueryUpdateFlag,bankdownloadsListDTO, bankdownloadsDelListDTO, bankdownloadDTO
from ..database.db import get_session
from ..repositories.bankdownload_repository import bankdownloadRepository
from ..services.bankdownload_service import bankdownloadService
from ..services.bankdownload_filehandler import bankdownloadFileHandler
from ..models.bankdownloads_model import bankdownloadsModel
import logging

# DEFINITIONS
get_pkey="/bankdownloads/pkey"
get_all=post_all="/bankdownloads"
send_bankdownload_report="/bankdownloads/email"
del_all = "/bankdownloadsdel"
chase_upload = "/chasexl"
wellsfargo_upload = "/wellsfargoxl"
myObjects="bankdownloads"
get_response_model=bankdownloadsListDTO
get_pkey_model = bankdownloadDTO
del_response_model=bankdownloadsDelListDTO
myModel=bankdownloadsModel

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
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_bankdownload_report,
        summary="Send bankdownload report to email",
        description="Send bankdownload report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_bankdownload_report(
     query_params: bankdownloadQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)
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
    query_params: bankdownloadQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)
    try:
        key_fields = {'bank_account_key': query_params.bank_account_key,
                        'tdate': query_params.tdate,
                        'description': query_params.description,
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
     query_params: bankdownloadQueryUpdateFlag = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.bankdownloads, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
############################################################################################################

@router.post(chase_upload, summary="Upload and save bankdownloads data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: bankdownloadQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)

    my_filehandler = bankdownloadFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file(
        column_names = CHASE_COLUMNS,
        rename_columns = 'X',
        fileheaders = None
    )
    if errorsList:
        return errorsList
   
    resultsList,errorsList = await my_service.post_data(input_data.bankdownloads, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################
@router.post(wellsfargo_upload, summary="Upload and save bankdownloads data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: bankdownloadQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)

    my_filehandler = bankdownloadFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file(
        column_names = WELLSFARGO_COLUMNS,
        rename_columns = None,
        fileheaders = WELLSFARGO_FILEHEADERS
    )
    if errorsList:
        return errorsList
   
    resultsList,errorsList = await my_service.post_data(input_data.bankdownloads, myModel, query_params.update,myObjects)
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
    my_repository = bankdownloadRepository(db)
    my_service = bankdownloadService(my_repository)
    results = []
    for record in input_data.bankdownloadsDel:   
        try:
            key_fields = {'bank_account_key': record.bank_account_key,
                        'tdate': record.tdate,
                        'description': record.description,
                        'amount': record.amount
                          }  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
