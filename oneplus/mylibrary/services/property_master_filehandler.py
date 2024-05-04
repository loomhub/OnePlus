from datetime import datetime
from typing import Tuple, List
from fastapi import HTTPException
import pandas as pd
from .myfilehandler import myFileHandler
from ..dtos.property_master_dto import PROPERTY_MASTER_COLUMNS, propertyMasterDTO, propertyMastersListDTO

class propertyMasterFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) :   #-> Tuple[propertyMastersListDTO, List[str]]:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=PROPERTY_MASTER_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['property_name','property_description','llc','note','county'])
        df=self.convert_columns_to_date(df, ['purchase_date','sell_date'])
        df=self.convert_columns_to_numeric(df, ['purchase_price','sell_price'])
        df=self.convert_columns_to_int(df, ['units'])
        errorsList = self.validate_null(df)
        try:
            if errorsList:
                return {},errorsList
            else:
                propertyMasters_data = self.convert_dataframe_to_list_dto(df,propertyMasterDTO)
                return propertyMastersListDTO(propertyMasters=propertyMasters_data),[]
           
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
    
    def extract_data_from_file_new(self):
        return {}
