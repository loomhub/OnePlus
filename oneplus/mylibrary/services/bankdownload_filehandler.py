from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.bankdownload_dto import bankdownloadDTO, bankdownloadsListDTO

class bankdownloadFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)

    def add_bank_account_key(self, df):
        bank_account_key = self.file.filename.split('/')[-1].split('.')[0]
        df['bank_account_key'] = bank_account_key
        return df    
    
    def extract_data_from_file(self,**kwargs) -> bankdownloadsListDTO:
        column_names = kwargs.get('column_names', None)
        rename_columns = kwargs.get('rename_columns', None) #rename columns for Chase downloads
        fileheaders = kwargs.get('fileheaders', None) #file headers for Wells Fargo downloads

        self.save_file_to_disk()
        df = self.read_data(column_names=fileheaders)
        if rename_columns:
            df.rename(columns=column_names, inplace=True)
        df=self.adjust_columns(df, column_names, remove_starting_with ='not_required')
        df=self.add_bank_account_key(df)
        df=self.convert_columns_to_string(df, ['bank_account_key','description'])
        df=self.convert_columns_to_numeric(df, ['amount'])
        df=self.convert_columns_to_date(df, ['tdate'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                bankdownloads_data = self.convert_dataframe_to_list_dto(df,bankdownloadDTO)
                return bankdownloadsListDTO(bankdownloads=bankdownloads_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
        
# #############################################################################################################