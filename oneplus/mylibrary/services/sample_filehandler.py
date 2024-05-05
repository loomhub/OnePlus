from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.sample_dto import SAMPLE_COLUMNS, sampleDTO, samplesListDTO

class sampleFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> samplesListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=SAMPLE_COLUMNS, inplace=True)
        df=self.convert_columns_to_date(df, ['formation_date'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                samples_data = self.convert_dataframe_to_list_dto(df,sampleDTO)
                return samplesListDTO(samples=samples_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
