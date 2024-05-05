from fastapi import HTTPException

from ..dtos.upload_download_dto import fileDTO, fileListDTO
from .myfilehandler import myFileHandler
#from ..dtos.sample_dto import SAMPLE_COLUMNS, sampleDTO, samplesListDTO

class uploadDownloadFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def format_data_from_file(self) -> fileListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        melted_df = df.melt(id_vars='Property', var_name='Month', value_name='Balance')
        melted_df=self.convert_month_to_date(melted_df, ['Month'])
        melted_df=self.convert_columns_to_numeric(melted_df, ['Balance'])
        errorsList = self.validate_null(melted_df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                output_file_path = 'uploads/melted_balances.csv'
                melted_df.to_csv(output_file_path, index=False)
                file_data = self.convert_dataframe_to_list_dto(melted_df,fileDTO)
                return fileListDTO(objects=file_data),[]
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
