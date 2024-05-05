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
        df=self.convert_columns_to_string(df, ['endpoint','to'],na_values='Must maintain')
        df=self.convert_columns_to_string(df, ['cc','bcc'],na_values='Not Manadatory')
        df=self.convert_columns_to_string(df, ['active'],na_values='Yes')
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                emailsConfig_data = self.convert_dataframe_to_list_dto(df,emailConfigDTO)
                return emailsConfigListDTO(emailsConfig=emailsConfig_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
