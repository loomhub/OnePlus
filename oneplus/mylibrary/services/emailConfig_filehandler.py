from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.emailConfig_dto import EMAIL_CONFIG_COLUMNS, emailConfigDTO, emailsConfigListDTO

class emailConfigFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> emailsConfigListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=EMAIL_CONFIG_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['endpoint','to','cc','bcc','inactive'])
        try:
            emailsConfig_data = self.convert_dataframe_to_list_dto(df,emailConfigDTO)
            return emailsConfigListDTO(emailsConfig=emailsConfig_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
