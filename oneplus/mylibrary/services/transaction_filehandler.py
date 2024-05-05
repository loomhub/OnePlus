from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.transaction_dto import TRANSACTIONS_COLUMNS, transactionDTO, transactionsListDTO

class transactionFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> transactionsListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=TRANSACTIONS_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['bank_account_key','description','details','classification','period_status',
                                               'transaction_group','transaction_type','comments',
                                               'vendor_no_w9','customer_no_w9'])
        df=self.convert_columns_to_string(df, ['vendor','customer'], na_values='NA')
        df=self.convert_columns_to_date(df, ['tdate'])
        df=self.convert_columns_to_numeric(df, ['amount'])
        errorsList = self.validate_null(df)
        
        try:
            if errorsList:
                return {},errorsList
            else:
                transactions_data = self.convert_dataframe_to_list_dto(df,transactionDTO)
                return transactionsListDTO(transactions=transactions_data),[]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
   
