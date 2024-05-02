
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.transaction_type_dto import transactionTypeQueryEmail, transactionTypeQueryPrimaryKey, transactionTypeQueryUpdateFlag,transactionTypesListDTO, transactionTypesDelListDTO, transactionTypeDTO
from ..database.db import get_session
from ..repositories.transaction_type_repository import transactionTypeRepository
from ..services.transaction_type_service import transactionTypeService
from ..services.transaction_type_filehandler import transactionTypeFileHandler
from ..models.transaction_types_model import transactionTypesModel
import logging

# DEFINITIONS
get_pkey="/transactionTypes/pkey"
get_all=post_all="/transactionTypes"
send_transactionType_report="/transactionTypes/email"
del_all = "/transactionTypesdel"
excel_upload = "/transactionTypesxl"
myObjects="transactionTypes"
get_response_model=transactionTypesListDTO
get_pkey_model = transactionTypeDTO
del_response_model=transactionTypesDelListDTO
myModel=transactionTypesModel

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
    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_transactionType_report,
        summary="Send transactionType report to email",
        description="Send transactionType report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_transactionType_report(
     query_params: transactionTypeQueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
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
    query_params: transactionTypeQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
    try:
        key_fields = {'transaction_group': query_params.transaction_group,
                      'transaction_type':query_params.transaction_type}  # Adjust according to actual key fields
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
     query_params: transactionTypeQueryUpdateFlag = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
    results = []
    for record in input_data.transactionTypes:
        try:
            key_fields = {'transaction_group': record.transaction_group,
                      'transaction_type':record.transaction_type}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields, query_params.update)
            results.append( {"created": created, myObjects: result} )
        except Exception as e:
            logging.error(f"Failed to update or create record: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################

@router.post(excel_upload, summary="Upload and save transactionTypes data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: transactionTypeQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_filehandler = transactionTypeFileHandler(file)
    input_data = my_filehandler.extract_data_from_file()

    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
    results = []
    for record in input_data.transactionTypes:
        try:
            key_fields = {'transaction_group': record.transaction_group,
                      'transaction_type':record.transaction_type}  # Adjust according to actual key fields
            created, result = await my_service.upsert_records(record, myModel, key_fields, query_params.update)
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
    my_repository = transactionTypeRepository(db)
    my_service = transactionTypeService(my_repository)
    results = []
    for record in input_data.transactionTypesDel:   
        try:
            key_fields = {'transaction_group': record.transaction_group,
                      'transaction_type':record.transaction_type}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
