from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.balance_dto import BALANCES_COLUMNS, balanceDTO, balancesListDTO

class balanceFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> balancesListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=BALANCES_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['bank_account_key'])
       # df=self.convert_columns_to_date(df, ['snapshot'])
        df=self.convert_month_to_date(df, ['snapshot'])
        df=self.convert_columns_to_numeric(df, ['balance'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                balances_data = self.convert_dataframe_to_list_dto(df,balanceDTO)
                return balancesListDTO(balances=balances_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
