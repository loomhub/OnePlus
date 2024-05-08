
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.tenant_dto import tenantQueryPrimaryKey, tenantQueryUpdateFlag,tenantsListDTO, tenantsDelListDTO, tenantDTO
from ..dtos.service_dto import QueryEmail
from ..database.db import get_session
from ..repositories.tenant_repository import tenantRepository
from ..services.tenant_service import tenantService
from ..services.tenant_filehandler import tenantFileHandler
from ..models.tenants_model import tenantsModel
import logging

# DEFINITIONS
get_pkey="/tenants/pkey"
get_all=post_all="/tenants"
send_tenant_report="/tenants/email"
del_all = "/tenantsdel"
excel_upload = "/tenantsxl"
myObjects="tenants"
get_response_model=tenantsListDTO
get_pkey_model = tenantDTO
del_response_model=tenantsDelListDTO
myModel=tenantsModel

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
    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {myObjects:results}

############################################################################################################
@router.get(
        send_tenant_report,
        summary="Send tenant report to email",
        description="Send tenant report to email",
        status_code=200,
        response_model=get_response_model,
        tags=["Get"],
        )

async def send_tenant_report(
     query_params: QueryEmail = Depends(),
     db: AsyncSession = Depends(get_session)
     ):
    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)
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
    query_params: tenantQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)
    try:
        key_fields = {'customer': query_params.customer,
                    'property_name': query_params.property_name,
                    'unit_name': query_params.unit_name,
                    'lease_start': query_params.lease_start,
                    'lease_end': query_params.lease_end
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
     query_params: tenantQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)):

    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)

    resultsList,errorsList = await my_service.post_data(input_data.tenants, myModel, query_params.update,myObjects)
    if errorsList:
         return errorsList
    else:
         return resultsList  
    
############################################################################################################

@router.post(excel_upload, summary="Upload and save tenants data from a CSV file")
async def upload_and_upsert_records(
    file: UploadFile = File(...),
    query_params: tenantQueryUpdateFlag = Depends(),
    db: AsyncSession = Depends(get_session)
                                   ):
    
    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)

    my_filehandler = tenantFileHandler(file)
    input_data, errorsList = my_filehandler.extract_data_from_file()
    
    if errorsList:
        return errorsList

    resultsList,errorsList = await my_service.post_data(input_data.tenants, myModel, query_params.update,myObjects)
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
    my_repository = tenantRepository(db)
    my_service = tenantService(my_repository)
    results = []
    for record in input_data.tenantsDel:   
        try:
            key_fields = {
                'customer': record.customer,
                'property_name': record.property_name,
                'unit_name': record.unit_name,
                'lease_start': record.lease_start,
                'lease_end': record.lease_end
            }  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
