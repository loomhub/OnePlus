
from typing import List
from fastapi import APIRouter, File, HTTPException, Depends
from pydantic import BaseModel, create_model
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.transreport_dto import reportDTO, transreportQueryPrimaryKey, transreportQueryUpdateFlag,transreportsListDTO, transreportsDelListDTO, transreportDTO
from ..dtos.transreport_dto import reportQuery,reportListDTO
from ..dtos.service_dto import QueryEmail
from ..database.db import get_session
from ..repositories.transreport_repository import transreportRepository
from ..services.transreport_service import transreportService
from ..models.transreports_model import transreportModel
from ..models.transactions_model import transactionsModel
from ..models.cashflows_model import cashflowsModel


# DEFINITIONS
get_pkey="/transreports/pkey"
get_all=post_all="/transreports"
send_transreport_report="/transreports/email"
del_all = "/transreportsdel"
excel_upload = "/transreportsxl"
myObjects="transreports"
perfsummary="/perfsummary"
perfObject="performance"
get_response_model=transreportsListDTO
get_pkey_model = transreportDTO
del_response_model=transreportsDelListDTO
myModel=transreportModel
summary_model=reportListDTO
summary_DTO=reportDTO

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
    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_transreport_report,
        summary="Send transreport report to email",
        description="Send transreport report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_transreport_report(
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)
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
    query_params: transreportQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)
    try:
        key_fields = {'sequence_id': query_params.sequence_id}  # Adjust according to actual key fields
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
     query_params: transreportQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.transreports, myModel, query_params.update,myObjects)
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
    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)
    results = []
    for record in input_data.transreportsDel:   
        try:
            key_fields = {'sequence_id': record.sequence_id}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
@router.get(
        perfsummary,
        summary="Get performance summary report",
        description="Get performance summary report from database",
        status_code=200,
    #    response_model=summary_model,
        tags=["Get"],
        )

async def performance_summary(
    query_params: reportQuery = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = transreportRepository(db)
    my_service = transreportService(my_repository)
    try:
        result = await my_service.summarize_performance(myModel,transactionsModel,cashflowsModel,
                                                        bank_account_key=query_params.bank_account_key,
                                                        years=query_params.years)
        if result is None:
            return {}
        return result
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
