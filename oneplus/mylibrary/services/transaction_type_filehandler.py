from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.transaction_type_dto import TRANSACTION_TYPES_COLUMNS, transactionTypeDTO, transactionTypesListDTO

class transactionTypeFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> transactionTypesListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=TRANSACTION_TYPES_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['transaction_group','transaction_type','transaction_description'])
        try:
            transactionTypes_data = self.convert_dataframe_to_list_dto(df,transactionTypeDTO)
            return transactionTypesListDTO(transactionTypes=transactionTypes_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
