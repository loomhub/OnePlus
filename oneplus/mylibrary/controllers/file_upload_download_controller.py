
from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from ..dtos.upload_download_dto import fileListDTO
from ..services.upload_download_filehandler import uploadDownloadFileHandler


# DEFINITIONS
excel_upload = "/formatxl"
myObjects="objects"
get_response_model=fileListDTO
router = APIRouter()


############################################################################################################

@router.post(excel_upload, summary="Upload, format data and download a CSV file")
async def upload_and_download_data(
    file: UploadFile = File(...)):
    
    try:
        my_filehandler = uploadDownloadFileHandler(file)
        formatted_data = my_filehandler.format_data_from_file()
        #results = input_data.objects
        return formatted_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
############################################################################################################

