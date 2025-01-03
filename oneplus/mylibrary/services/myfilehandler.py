from datetime import datetime
import os, shutil
from typing import List, Tuple, Type
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel, ValidationError

from ..services.myservice import MyService
from ..dtos.llc_dto import LLC_COLUMNS, llcsListDTO, llcDTO


class myFileHandler:
    def __init__(self, file):
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
        self.file=file
        self.file_location = f"uploads/{file.filename}"
        self.dir='uploads'
#############################################################################################################
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
#############################################################################################################
    def read_data(self,**kwargs):
        column_names = kwargs.get('column_names', None)
        try:
            if column_names:
                return pd.read_csv(self.file_location, na_values=[], header=None, names=column_names,index_col=False)
            else:
                return pd.read_csv(self.file_location, na_values=[],index_col=False)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load file into DataFrame: {str(e)}")
#############################################################################################################
    def convert_dataframe_to_list_dto(
            self,
            df: pd.DataFrame, #pandas.DataFrame containing the data.
            dto_class: Type[BaseModel] #The DTO class to which rows will be converted.
            )  -> Tuple[List[BaseModel],List[str]]: #Return a list of DTO instances.
    
        # errorsList=dto_list = []
        # for index, row in df.iterrows():
        #     for column, value in row.items():
        #             if pd.isna(value):
        #                 errorsList.append(f"Column causing issue: {column}, Value: {value} in row {row}")
        # if len(errorsList)==0:
        dto_list=[]
        for index, row in df.iterrows():
            try:
                dto_instance = dto_class(**row.to_dict()) # Use dictionary unpacking to initialize the DTO from a row.
                dto_list.append(dto_instance)
            except ValidationError as e:
                print(f"Error occurred at row index {index}")
                
        print(type(dto_list))   

        return dto_list
#############################################################################################################
    def parse_date(self,date_str):
        # Convert to string and handle NaN values
        date_str = str(date_str) if pd.notna(date_str) else ''
    
        # Try parsing with different formats
        if len(date_str.split('/')[-1]) == 4:  # Check for MM/DD/YYYY
            return pd.to_datetime(date_str, format='%m/%d/%Y', errors='coerce')
        elif len(date_str.split('-')[0]) == 4:  # Check for YYYY-MM-DD
            return pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')
        else:  # Check for MM/DD/YY
            return pd.to_datetime(date_str, format='%m/%d/%y', errors='coerce')
#############################################################################################################
    def convert_columns_to_date(self, 
                        df: pd.DataFrame, 
                        column_names: List[str],
                        **kwargs) -> pd.DataFrame:
        null_value_date = kwargs.get('null_value_date', '2099-12-31')
  
        for column_name in column_names:
            if column_name in df.columns:
                try:
                    df[column_name] = df[column_name].fillna(pd.Timestamp(null_value_date))
                    df[column_name] = df[column_name].apply(self.parse_date).dt.date
                    print(df[column_name])
                except Exception as e:
                    print(f"Error converting {column_name}: {e}")
            else:
                print(f"Column {column_name} not found in DataFrame.")
        return df
#############################################################################################################   
    def convert_month_to_date(self, 
                            df: pd.DataFrame, 
                            column_names: List[str],
                            **kwargs) -> pd.DataFrame:
            null_value_date = kwargs.get('null_value_date', '2099-12-31')
            for column_name in column_names:
                if column_name in df.columns:
                    try:
                        df[column_name] = df[column_name].fillna(pd.Timestamp(null_value_date))
                        df[column_name] = pd.to_datetime(df[column_name]).dt.date
                        df[column_name] = pd.to_datetime(df[column_name]).dt.to_period('M').dt.to_timestamp()
                    except Exception as e:
                        print(f"Error converting {column_name}: {e}")
                else:
                    print(f"Column {column_name} not found in DataFrame.")
            return df
############################################################################################################# 
    def convert_columns_to_string(self, 
                        df: pd.DataFrame, 
                        column_names: List[str],**kwargs) -> pd.DataFrame:
        na_values = kwargs.get('na_values', '')
        for column_name in column_names:
            if column_name in df.columns:
                try:
                    df[column_name] = df[column_name].fillna(na_values).astype(str)
                except Exception as e:
                    print(f"Error converting {column_name}: {e}")
            else:
                print(f"Column {column_name} not found in DataFrame.")
        return df
#############################################################################################################    
    def convert_columns_to_numeric(self, 
                        df: pd.DataFrame, 
                        column_names: List[str]) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                try:
                    df[column_name] = df[column_name].fillna(0).astype(str)
                    df[column_name] = df[column_name].str.replace(',', '').str.replace('$', '')
                    df[column_name] = df[column_name].str.replace('(', '-').str.replace(')', '')
                    # Handle the case where "-" should be converted to 0, but not affect numbers like "-90"
                    df[column_name] = df[column_name].apply(lambda x: '0' if x.strip() == '-' else x)
                    #df[column_name] = df[column_name].str.replace(r'\((\d+)\)', r'-\1', regex=True).astype(float)
                    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')   
                except Exception as e:
                    print(f"Error converting {column_name}: {e}")
            else:
                print(f"Column {column_name} not found in DataFrame.")
        return df
#############################################################################################################    
    def convert_columns_to_int(self, 
                        df: pd.DataFrame, 
                        column_names: List[str]) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                try:
                    df[column_name] = df[column_name].astype(int)
                except Exception as e:
                    print(f"Error converting {column_name}: {e}")
            else:
                print(f"Column {column_name} not found in DataFrame.")
        return df
#############################################################################################################
    def adjust_columns(self,
                        df: pd.DataFrame, 
                        columns, 
                        **kwargs) -> pd.DataFrame:
        remove_starting_with = kwargs.get('remove_starting_with', None)

        if remove_starting_with:
            columns_to_remove = [value for key, value in columns.items() if value.startswith(remove_starting_with)]
            columns = [col for col in columns if not col.startswith(remove_starting_with)]
            df.drop(columns=columns_to_remove, inplace=True)
            return df
#############################################################################################################

    def validate_null(self,df: pd.DataFrame) -> List[str]:
    # Create a mask that is True wherever there are NaNs
        mask = df.isna().any(axis=1)
    
    # Use the mask to select all rows that have any NaN values
        errorDf = df[mask]
        errorsList = errorDf.to_dict(orient='records')
        if len(errorsList)>0:
            return {'errors':errorsList}
        else:
            return {}
############################################################################################################