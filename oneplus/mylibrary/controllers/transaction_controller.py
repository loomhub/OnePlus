from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.transaction_dto import transactionQueryPrimaryKey,transactionQueryUpdateFlag, transactionSearchQuery
from ..dtos.service_dto import QueryEmail
from ..dtos.transaction_dto import transactionsListDTO, transactionsDelListDTO, transactionDTO,TRANSACTIONS_COLUMNS_FINAL
from ..database.db import get_session
from ..repositories.transaction_repository import transactionRepository
from ..services.transaction_service import transactionService
from ..services.transaction_filehandler import transactionFileHandler
from ..models.transactions_model import transactionsModel
from ..models.transactionstmp_model import transactionstmpModel
from ..models.cashflows_model import cashflowsModel

# DEFINITIONS
get_pkey="/transactions/pkey"
get_all=post_all="/transactions"
search="/transactions/search"
period_close = "/periodclose"
send_transaction_report="/transactions/email"
del_all = "/transactionsdel"
excel_upload = "/transactionsxl"
myObjects="transactions"
get_response_model=transactionsListDTO
get_pkey_model = transactionDTO
del_response_model=transactionsDelListDTO
myModel=transactionsModel
transtmpModel=transactionstmpModel
cashModel=cashflowsModel
myDTO=transactionDTO

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
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
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
    query_params: transactionQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
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
@router.get(
        search,
        summary="Search records",
        description="Search records from database based on search model",
        status_code=200,
        response_model=get_response_model,
        tags=["Search"],
        )

async def search_records(
    query_params: transactionSearchQuery = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    try:
        key_fields = {  'start_date': query_params.start_date,
                        'end_date': query_params.end_date,
                        'min_amount': query_params.min_amount,
                        'max_amount': query_params.max_amount,
                        'classification': query_params.classification,
                        'transaction_group': query_params.transaction_group,
                        'transaction_type': query_params.transaction_type,
                        'description': query_params.description,
                        'vendor': query_params.vendor,
                        'customer': query_params.customer
                      }  # Adjust according to actual key fields
        results = await my_service.search_records(myModel,key_fields)
        if results is None:
            return {}
        return {myObjects:results}
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
    db: AsyncSession = Depends(get_session)):

    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.transactions, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save transactions data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: transactionQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)

    my_filehandler = transactionFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file(column_names = TRANSACTIONS_COLUMNS_FINAL)
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.transactions, myModel, query_params.update,myObjects)
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
    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)
    results = []
    for record in input_data.transactionsDel:   
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
@router.post(
        period_close,
        summary="Period Close",
        description="Close period and store data in database",
        tags=["Period Close"],
        )
async def close_period(
     query_params: transactionSearchQuery = Depends(),
     db: AsyncSession = Depends(get_session)):

    my_repository = transactionRepository(db)
    my_service = transactionService(my_repository)

    resultTransList,errorTransList = await my_service.period_close(myModel,transtmpModel,cashModel,myDTO)
    if errorTransList:
        return errorTransList
    else:
        resultsList,errorsList = await my_service.post_data(resultTransList, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
############################################################################################################
