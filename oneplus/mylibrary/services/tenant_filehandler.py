from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.tenant_dto import TENANTS_COLUMNS, tenantDTO, tenantsListDTO

class tenantFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> tenantsListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=TENANTS_COLUMNS, inplace=True)
        df=self.convert_columns_to_date(df, ['lease_start','lease_end'])
        df=self.convert_columns_to_numeric(df, ['rent','security_deposit'])
        df=self.convert_columns_to_string(df, ['unit_name'], na_values='NA')
        try:
            tenants_data = self.convert_dataframe_to_list_dto(df,tenantDTO)
            return tenantsListDTO(tenants=tenants_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
