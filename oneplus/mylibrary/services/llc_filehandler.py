from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.llc_dto import LLC_COLUMNS, llcDTO, llcsListDTO

class llcFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> llcsListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=LLC_COLUMNS, inplace=True)
        df=self.convert_columns_to_date(df, ['formation_date'])
        try:
            llcs_data = self.convert_dataframe_to_list_dto(df,llcDTO)
            return llcsListDTO(llcs=llcs_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
