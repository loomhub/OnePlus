from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.cashflow_dto import CASHFLOWS_COLUMNS, cashflowDTO, cashflowsListDTO

class cashflowFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> cashflowsListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=CASHFLOWS_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['bank_account_key'])
        df=self.convert_month_to_date(df, ['start_date','end_date'])
        df=self.convert_columns_to_numeric(df, ['cash_change','ending_balance','calc_balance'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                cashflows_data = self.convert_dataframe_to_list_dto(df,cashflowDTO)
                return cashflowsListDTO(cashflows=cashflows_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
