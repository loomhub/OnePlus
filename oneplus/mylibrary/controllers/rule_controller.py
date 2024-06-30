from fastapi import APIRouter, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.rule_dto import ruleQueryPrimaryKey,ruleQueryUpdateFlag
from ..dtos.service_dto import QueryEmail
from ..dtos.rule_dto import rulesListDTO, rulesDelListDTO, ruleDTO,RULES_COLUMNS
from ..database.db import get_session
from ..repositories.rule_repository import ruleRepository
from ..services.rule_service import ruleService
from ..models.rules_model import rulesModel

# DEFINITIONS
get_pkey="/rules/pkey"
get_all=post_all="/rules"
search="/rules/search"
send_rule_report="/rules/email"
del_all = "/rulesdel"
truncate="/rulestruncate"
myObjects="rules"
get_response_model=rulesListDTO
get_pkey_model = ruleDTO
del_response_model=rulesDelListDTO
myModel=rulesModel

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
    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_rule_report,
        summary="Send rule report to email",
        description="Send rule report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_rule_report(
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)
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
    query_params: ruleQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)
    try:
        key_fields = {'ttype': query_params.ttype,
                        'description': query_params.description
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
     query_params: ruleQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.rules, myModel, query_params.update,myObjects)
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
    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)
    results = []
    for record in input_data.rulesDel:   
        try:
            key_fields = {'ttype': record.ttype,
                        'description': record.description
                          }  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
@router.delete(
        truncate,
        summary="Truncate table",
        description="Truncate table",
        tags=["Truncate"],
        )
async def truncate_table(db: AsyncSession = Depends(get_session)):
    my_repository = ruleRepository(db)
    my_service = ruleService(my_repository)
       
    try:
        deleted = await my_service.truncate_records(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return deleted
############################################################################################################

