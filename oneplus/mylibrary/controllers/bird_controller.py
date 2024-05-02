
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos.bird_dto import birdQueryPrimaryKey, birdQueryUpdateFlag,birdsListDTO, birdsDelListDTO, birdDTO  
from ..database.db import get_session
from ..repositories.bird_repository import birdRepository
from ..services.bird_service import birdService
from ..models.birds_model import birdsModel
import logging

# DEFINITIONS
get_pkey="/birds/pkey"
get_all=post_all="/birds"
del_all = "/birdsdel"
myObjects="birds"
get_response_model=birdsListDTO
get_pkey_model = birdDTO
del_response_model=birdsDelListDTO
myModel=birdsModel

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
    my_repository = birdRepository(db)
    my_service = birdService(my_repository)
    try:
        results = await my_service.extract_all(myModel)
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
    query_params: birdQueryPrimaryKey = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    my_repository = birdRepository(db)
    my_service = birdService(my_repository)
    try:
        key_fields = {'sender': query_params.sender}  # Adjust according to actual key fields
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
     query_params: birdQueryUpdateFlag = Depends(),
     db: AsyncSession = Depends(get_session)):
    my_repository = birdRepository(db)
    my_service = birdService(my_repository)
    results = []
    for record in input_data.birds:
        try:
            key_fields = {'sender': record.sender}  # Adjust according to actual key fields
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
    my_repository = birdRepository(db)
    my_service = birdService(my_repository)
    results = []
    for record in input_data.birdsDel:   
        try:
            key_fields = {'sender': record.sender}  # Adjust according to actual key fields
            deleted,result = await my_service.delete_records(record, myModel, key_fields)
            results.append( {"deleted": deleted,myObjects: result} )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return results
############################################################################################################
