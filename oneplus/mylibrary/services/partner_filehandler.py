from fastapi import HTTPException
from .myfilehandler import myFileHandler
from ..dtos.partner_dto import VENDOR_COLUMNS, partnerDTO, partnersListDTO

class partnerFileHandler(myFileHandler):
    def __init__(self, file):
        super().__init__(file)
        
    def extract_data_from_file(self) -> partnersListDTO:
        self.save_file_to_disk()
        df = self.read_data()
        df.rename(columns=VENDOR_COLUMNS, inplace=True)
        df=self.convert_columns_to_string(df, ['partner', 'recipient_type', 'recipient_tin_type', 'recipient_tin',
                                            'last_name', 'first_name', 'address', 'city', 'state', 'zip_code', 'country'])
        try:
            partners_data = self.convert_dataframe_to_list_dto(df,partnerDTO)
            return partnersListDTO(partners=partners_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")
