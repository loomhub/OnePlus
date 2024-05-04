from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.bankaccount_dto import BANK_ACCOUNTS_COLUMNS, bankaccountDTO, bankaccountsListDTO

class bankaccountFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> bankaccountsListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=BANK_ACCOUNTS_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['bank_account_key','bank','account_type','account_number','llc'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                bankaccounts_data = self.convert_dataframe_to_list_dto(df,bankaccountDTO)
                return bankaccountsListDTO(bankaccounts=bankaccounts_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
