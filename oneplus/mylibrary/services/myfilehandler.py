import os, shutil
from typing import List, Type
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel
from ..dtos.llc_dto import LLC_COLUMNS, llcsListDTO, llcDTO


class myFileHandler:
    def __init__(self, file):
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
        self.file=file
        self.file_location = f"uploads/{file.filename}"
        self.dir='uploads'

    def save_file_to_disk(self):
        # Check if the uploads directory exists, if not, create it
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        # Write the contents of the uploaded file to a new file in the server
        try:
            with open(self.file_location, "wb") as buffer:
                shutil.copyfileobj(self.file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not write to file: {str(e)}")

    def read_data(self):
        try:
            return pd.read_csv(self.file_location)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load file into DataFrame: {str(e)}")

    def convert_dataframe_to_list_dto(
            self,
            df: pd.DataFrame, #pandas.DataFrame containing the data.
            dto_class: Type[BaseModel] #The DTO class to which rows will be converted.
            )  -> List[BaseModel]: #Return a list of DTO instances.
    
        dto_list = []
        for index, row in df.iterrows():
        # Use dictionary unpacking to initialize the DTO from a row.
            dto_instance = dto_class(**row.to_dict())
            dto_list.append(dto_instance)

        print(type(dto_list))   
    
        return dto_list

    def convert_columns_to_date(self, 
                        df: pd.DataFrame, 
                        column_names: List[str]) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                try:
                    df[column_name] = pd.to_datetime(df[column_name]).dt.date
                except Exception as e:
                    print(f"Error converting {column_name}: {e}")
            else:
                print(f"Column {column_name} not found in DataFrame.")
            return df