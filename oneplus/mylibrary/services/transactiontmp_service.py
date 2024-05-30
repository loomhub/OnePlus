from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Type
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel, ValidationError
from ..models.bankaccounts_model import bankaccountsModel
from ..models.transaction_types_model import transactionTypesModel
from ..models.partners_model import partnersModel
from sqlalchemy.orm import class_mapper
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.feature_extraction.text import TfidfVectorizer


from ..repositories.transactiontmp_repository import transactiontmpRepository
from .myservice import MyService


class transactiontmpService(MyService):
    def __init__(self, transactiontmp_repository: transactiontmpRepository):
        super().__init__(transactiontmp_repository)
############################################################################################################
    async def post_data(self, 
                            records:List[Type[BaseModel]], 
                            model: Type[BaseModel], 
                            update_flag:str,myObjects:str):

            results=[]
            errors=[]

            # Validate data
            fkey_checks = {bankaccountsModel: {'bank_account_key': 'bank_account_key'},
                           transactionTypesModel: {'transaction_group': 'transaction_group',
                                                   'transaction_type': 'transaction_type'},
                            partnersModel: {'vendor':'partner'},
                            partnersModel: {'customer':'partner'}
                            }  # Fkey Model: {input data column: Model column}} 
            errors = await self.validate_data(records, fkey_checks)

            # Post data if no errors
            if not errors:
                for record in records:
                    try:
                        key_fields = {'bank_account_key': record.bank_account_key,
                                        'tdate': record.tdate,
                                        'description': record.description,
                                        'amount': record.amount}  # Adjust according to actual key fields
                        created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                        results.append( {"created": created, myObjects: result} )
                    except Exception as e:
                        logging.error(f"Failed to update or create record: {str(e)}")
                        raise HTTPException(status_code=400, detail=str(e))

            return results, errors
############################################################################################################
    def convert_dataframe_to_list_dto(
            self,
            df: pd.DataFrame, #pandas.DataFrame containing the data.
            dto_class: Type[BaseModel] #The DTO class to which rows will be converted.
            )  -> Tuple[List[BaseModel],List[str]]: #Return a list of DTO instances.
    
        # Get the fields of the dto_class
        dto_fields = list(dto_class.__fields__.keys())

        # Filter the DataFrame to only include columns that exist in dto_fields
        df_filtered = df[dto_fields]

        dto_list = []
        error_list = []

        for index, row in df_filtered.iterrows():
            try:
                dto_instance = dto_class(**row.to_dict())  # Use dictionary unpacking to initialize the DTO from a row.
                dto_list.append(dto_instance)
            except ValidationError as e:
                error_message = f"Error occurred at row index {index}: {e}"
                error_list.append(error_message)
                print(error_message)

        print(type(dto_list))

        return dto_list, error_list

############################################################################################################
    def sqlalchemy_model_to_dict(self,model):
    #Convert SQLAlchemy model instance to dictionary."
        return {column.key: getattr(model, column.key) for column in class_mapper(model.__class__).columns}
#############################################################################################################    
    def models_to_dataframe(self,models: List[BaseModel]) -> pd.DataFrame:
        # Convert list of Pydantic models to list of dictionaries
        data = [self.sqlalchemy_model_to_dict(model) for model in models]
        # Create DataFrame from list of dictionaries
        df = pd.DataFrame(data)
        return df
############################################################################################################
    async def load_data(self, *models: Type[BaseModel]):
        dataframes = []
        for model in models:
            data = await self.repository.retrieve_all(model)
            df = self.models_to_dataframe(data)
            dataframes.append(df)
        return dataframes
############################################################################################################
    # async def load_data(self, historyModel: Type[BaseModel], 
    #                     newDataModel: Type[BaseModel],
    #                     rulesModel: Type[BaseModel]):
        
    #     history = await self.repository.retrieve_all(historyModel)
    #     historyDF = self.models_to_dataframe(history)

    #     newData = await self.repository.retrieve_all(newDataModel)
    #     newDataDF = self.models_to_dataframe(newData)

    #     rulesData = await self.repository.retrieve_all(rulesModel)
    #     rulesDF = self.models_to_dataframe(rulesData)

    #     return historyDF, newDataDF, rulesDF
############################################################################################################
    def filter_data(self,historyDF,newDataDF, columns_to_check,start_date,end_date):

        merged_df = newDataDF.merge(historyDF, on=columns_to_check, how='left', indicator=True)
        self.download_files([(merged_df,'Merge01')],'STEP3A')

        newDataDF_filtered = merged_df[merged_df['_merge'] == 'left_only']
        self.download_files([(newDataDF_filtered,'Merge02')],'STEP3A')

        newDataDF_filtered = newDataDF_filtered.drop(columns=['_merge'])
        self.download_files([(newDataDF_filtered,'Merge03')],'STEP3A')

        newDataDF_filtered = newDataDF_filtered.drop_duplicates(subset=columns_to_check)
        self.download_files([(newDataDF_filtered,'Merge04')],'STEP3A')

        start_date = pd.to_datetime(start_date).normalize()
        end_date = pd.to_datetime(end_date).normalize()

        newDataDF_filtered = newDataDF_filtered[
            (newDataDF_filtered['tdate'] >= start_date) & (newDataDF_filtered['tdate'] <= end_date)]
        self.download_files([(newDataDF_filtered,'Merge05')],'STEP3A')
        return newDataDF_filtered
############################################################################################################
    def credit_debit_rule(self, df):
        df.loc[df['amount'] <= 0,
                ['customer', 'customer_no_w9']] = df.loc[df['amount'] < 0, 'bank_account_key'].apply(lambda x: [x, x]).to_list()
        df.loc[df['amount'] > 0,
                ['vendor', 'vendor_no_w9']] = df.loc[df['amount'] > 0, 'bank_account_key'].apply(lambda x: [x, x]).to_list()
        return df    
############################################################################################################
    def apply_business_logic(self, df, rule):
         # Step 1: Convert descriptions to lowercase
        df['description_lower'] = df['description'].str.lower()
        # Convert comma-separated keywords to a list and convert them to lowercase
        keywords = [keyword.strip().lower() for keyword in rule['description'].split(',')]

        if rule['ttype']=='credit':
            condition = ((df['classification'] != 'clean') & (df['amount'] <= 0)) & df['description_lower'].str.contains('|'.join(keywords), na=False)
            df.loc[condition, 'transaction_group'] = rule['transaction_group']
            df.loc[condition, 'transaction_type'] = rule['transaction_type']
            df.loc[condition, ['vendor', 'vendor_no_w9']] = rule['vendor_no_w9']
            df.loc[condition, ['customer_no_w9']] = rule['customer_no_w9']
        else:
            condition = ((df['classification'] != 'clean') & (df['amount'] > 0)) & df['description_lower'].str.contains('|'.join(keywords), na=False)
            df.loc[condition, 'transaction_group'] = rule['transaction_group']
            df.loc[condition, 'transaction_type'] = rule['transaction_type']
            df.loc[condition, ['customer', 'customer_no_w9']] = rule['customer_no_w9']
            df.loc[condition, ['vendor_no_w9']] = rule['vendor_no_w9']

        # Remove the temporary 'description_lower' column
        df.drop(columns=['description_lower'], inplace=True)
        return df
############################################################################################################
    def apply_business_rules(self, df, rulesDF):
        
        df=self.credit_debit_rule(df)

        for index, row in rulesDF.iterrows():
             try:
                 df=self.apply_business_logic(df, row)
             except Exception as e:
                 print(f"Error occurred at row index {index}: {e}")
        return df
############################################################################################################
    def update_from_records(self, newDataDF: pd.DataFrame, recordsDF: pd.DataFrame,pkey) -> pd.DataFrame:

        # Perform the merge to identify rows to update
        if not recordsDF.empty:
            merged_df = newDataDF.merge(
                recordsDF, 
                on=pkey, 
                suffixes=('', '_new')
            )

            # Update rows in newDataDF where the classification is "clean"
            for index, row in merged_df.iterrows():
                if pd.notna(row['classification_new']) and row['classification_new'] == 'clean':
                    condition = (
                        (newDataDF['bank_account_key'] == row['bank_account_key']) &
                        (newDataDF['tdate'] == row['tdate']) &
                        (newDataDF['description'] == row['description']) &
                        (newDataDF['amount'] == row['amount'])
                    )
                    update_columns = [col for col in recordsDF.columns if col not in pkey and col != 'classification_new' and col != 'id']
                    #update_values = {col: row[f'{col}_new'] for col in update_columns}
                    update_values = {}
                    for col in update_columns:
                        col_new = f'{col}_new'
                        if col_new in row:
                            update_values[col] = row[col_new]
                        else:
                            print(f"Column {col_new} not found in row")
                    # Prepare the update values
                    update_values = {col: row[f'{col}_new'] for col in update_columns}

                    # Ensure the index is correct
                    newDataDF.loc[condition, update_columns] = pd.DataFrame([update_values], index=newDataDF.loc[condition].index)

        return newDataDF
############################################################################################################
    def initialize_data(self, df):
        columns_to_initialize = ['vendor_no_w9', 'customer_no_w9','comments']
        df.loc[:, columns_to_initialize] = 'Initial'
        df.loc[:, 'transaction_group'] = 'X-Review'
        df.loc[:, 'transaction_type'] = 'Review'
        df.loc[:, 'vendor'] = 'GeneralVendor'
        df.loc[:, 'customer'] = 'GeneralCustomer'
        df.loc[df['period_status'].isnull(), 'period_status'] = 'open'
        df.loc[df['classification'].isnull(), 'classification'] = 'review'
        return df
############################################################################################################
    def set_date_range(self, start_date, end_date, df):
        if not start_date:
            start_date = df['tdate'].max()
        if not end_date:
            end_date = (datetime.now() + timedelta(days=1))
        return start_date, end_date
############################################################################################################
    async def apply_rules(self, 
                            records:List[Type[BaseModel]], 
                            myModel: Type[BaseModel], 
                            outputDTO: Type[BaseModel], 
                            historyModel: Type[BaseModel], 
                            newDataModel: Type[BaseModel], 
                            rulesModel: Type[BaseModel],
                            start_date: str,
                            end_date: str):
        
        
        pkey=['bank_account_key', 'tdate', 'description', 'amount']
        #Step 1 Load Dataframes
        myDF,historyDF, newDataDF,rulesDF = await self.load_data(myModel,historyModel, newDataModel,rulesModel) # Load data from database
        records_df = pd.DataFrame([record.dict() for record in records])

        start_date, end_date = self.set_date_range(start_date, end_date, historyDF)

        #Step 2 Convert columns to appropriate data types
        myDF,historyDF,newDataDF,records_df = self.convert_dataframe_columns([myDF,historyDF,newDataDF,records_df],
                                                                             ['bank_account_key','tdate','description'],
                                                                             'string')
        myDF,historyDF,newDataDF,records_df = self.convert_dataframe_columns([myDF,historyDF,newDataDF,records_df],
                                                                             ['tdate'],
                                                                             'date')
        myDF,historyDF,newDataDF,records_df = self.convert_dataframe_columns([myDF,historyDF,newDataDF,records_df],
                                                                             ['amount'],
                                                                             'numeric')
        self.download_files([(myDF,'Transactionstmp'),(historyDF,'Transactions'),(newDataDF,'IncomingData'),(records_df,'PostData')],'STEP2')

        #Step 3 Filter incoming data to keep transactions within the date range
        newDataDF=self.filter_data(historyDF,newDataDF,pkey,start_date,end_date)
        self.download_files([(newDataDF,'IncomingData')],'STEP3')

        #Step 4 Initialize Data
        newDataDF = self.initialize_data(newDataDF)
        self.download_files([(newDataDF,'IncomingData')],'STEP4')

        #Step 5A Update incoming data with transactionstmp
        newDataDF = self.update_from_records(newDataDF, myDF,pkey)
        self.download_files([(newDataDF,'IncomingData')],'STEP5A')

         #Step 5B Update incoming data with post data records
        newDataDF = self.update_from_records(newDataDF, records_df,pkey)
        self.download_files([(newDataDF,'IncomingData')],'STEP5B')
        
        #Step 6 Apply Business Rules
        newDataDF = self.apply_business_rules(newDataDF,rulesDF)
        self.download_files([(newDataDF,'IncomingData')],'STEP6')

        #Step 7 Convert DataFrame to ListDTO
        newDataList, errorList = self.convert_dataframe_to_list_dto(newDataDF, outputDTO)
        return newDataList, errorList
############################################################################################################
    # def encode_categorical_data(self, df, columns):
    #     for column in columns:
    #         le = LabelEncoder()
    #         df[column] = le.fit_transform(df[column])
    #     return df,le
############################################################################################################
#     def extract_dd_mm_yy(self, df, date_column, day_column, month_column, year_column):
#         df[date_column] = pd.to_datetime(df[date_column])
#         df[day_column] = df[date_column].dt.day
#         df[month_column] = df[date_column].dt.month
#         df[year_column] = df[date_column].dt.year
#         return df
# ############################################################################################################
#     def vectorize_text_data(self, df, text_column):
#         # Vectorizing text data
#         tfidf = TfidfVectorizer()
#         tfidf_text_column = tfidf.fit_transform(df[text_column])
#         return tfidf, tfidf_text_column
# ############################################################################################################
#     def build_independent_fields(self, df,independent_fields ,description_tfidf):
#         other_features = df[independent_fields].values
#         return pd.DataFrame.sparse.from_spmatrix(description_tfidf).join(pd.DataFrame(other_features, columns=independent_fields))
# ############################################################################################################
#     def model_fit(self, df,X, dependent_fields,**kwargs):

#         ts = kwargs.get('test_size', 0.2)
#         rs = kwargs.get('random_state', 42)

#         models = {}
#         label_encoders = {}

#         for field in dependent_fields:
#             print(f"Fitting model for field: {field}")
#             y = df[field].fillna('Unknown')
#             le = LabelEncoder()
#             y_encoded = le.fit_transform(y)
#             label_encoders[field] = le
#             X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=ts, random_state=rs)
#             model = RandomForestClassifier()
#             model.fit(X_train, y_train)
#             models[field] = model
#         return models, label_encoders

############################################################################################################
#     def prepare_data(self, transactions_df):
#         independent_fields = ['bank_account_key', 'tdate', 'description', 'amount']
#         dependent_fields = ['transaction_group', 'transaction_type', 'vendor', 'customer', 'vendor_no_w9', 'customer_no_w9']

#         # Encoding categorical data
#         le_bank_account_key = LabelEncoder()
#         transactions_df['bank_account_key'] = le_bank_account_key.fit_transform(transactions_df['bank_account_key'])

#         # Extracting day, month, year from date for better modeling
#         transactions_df['tday'] = transactions_df['tdate'].dt.day
#         transactions_df['tmonth'] = transactions_df['tdate'].dt.month
#         transactions_df['tyear'] = transactions_df['tdate'].dt.year

#         independent_fields = ['bank_account_key', 'tday', 'tmonth', 'tyear', 'description', 'amount']

#         X = transactions_df[independent_fields]
#         models = {}
#         label_encoders = {}

#         for field in dependent_fields:
#             y = transactions_df[field].fillna('Unknown')
#             le = LabelEncoder()
#             y_encoded = le.fit_transform(y)
#             label_encoders[field] = le
#             X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
#             model = RandomForestClassifier()
#             model.fit(X_train, y_train)
#             models[field] = model

#         return models, label_encoders, le_bank_account_key
# ############################################################################################################
#     def populate_dependent_fields(self,row, row_index, total_count,models, label_encoders, le_bank_account_key,tfidf):
        
#         print(f"Now predicting row {row_index + 1} of {total_count} rows...")

#         row['tdate'] = pd.to_datetime(row['tdate'])
#         row['tday'] = row['tdate'].day
#         row['tmonth'] = row['tdate'].month
#         row['tyear'] = row['tdate'].year
#         original_bank_account_key = row['bank_account_key']
#         row['bank_account_key'] = le_bank_account_key.transform([row['bank_account_key']])[0]

#         description_tfidf = tfidf.transform([row['description']])
#         input_data = pd.DataFrame.sparse.from_spmatrix(description_tfidf).join(pd.DataFrame([{
#             'bank_account_key': row['bank_account_key'],
#             'tday': row['tday'],
#             'tmonth': row['tmonth'],
#             'tyear': row['tyear'],
#             'amount': row['amount']
#         }]))
#         input_data.columns = input_data.columns.astype(str) # Convert column names to string for machine learning
#         for field in label_encoders.keys():
#             model = models[field]
#             le = label_encoders[field]
#             prediction = model.predict(input_data)[0]
#             row[field] = le.inverse_transform([prediction])[0]
        
#         row['bank_account_key'] = original_bank_account_key

#         return row


# ############################################################################################################
#     def dataframe_to_models(self,df: pd.DataFrame, model: Type[BaseModel]) -> List[BaseModel]:
#         model_columns = model.__table__.columns.keys()
    
#     # Remove columns from df that don't exist in model_columns
#         df_filtered = df[model_columns]
    
#         model_instances = []
#         for _, row in df_filtered.iterrows():
#             model_instance = model(**row.to_dict())
#             model_instances.append(model_instance)
    
#         return model_instances
############################################################################################################
    # async def machine_learn(self, outputModel: Type[BaseModel], 
    #                         historyModel: Type[BaseModel], 
    #                         newDataModel: Type[BaseModel], 
    #                         start_date: str,
    #                         end_date: str,
    #                         myObjects:str):
        
    #     historyDF, newDataDF = await self.load_data(historyModel, newDataModel) # Load data from database
    # #   historyDF.to_excel('HistoryDF.xlsx', index=False)
    #     newDataDF.to_excel('newDataDF.xlsx', index=False)

    #     newDataDF=self.filter_data(historyDF,newDataDF, ['bank_account_key', 'tdate', 'description', 'amount'],start_date,end_date)
    #     newDataDF.to_excel('newDataFiltered.xlsx', index=False)

    #     # Prepare data for machine learning
    #     historyDF,le_bank_account_key=self.encode_categorical_data(historyDF,['bank_account_key'])
    #     historyDF=self.extract_dd_mm_yy(historyDF,'tdate','tday','tmonth','tyear')
    #     tfidf,description_tfidf=self.vectorize_text_data(historyDF,'description') 

    #     # Build independent fields
    #     X = self.build_independent_fields(historyDF,['bank_account_key', 'tday', 'tmonth', 'tyear', 'amount'],description_tfidf)
    #     X.columns = X.columns.astype(str) # Convert column names to string for machine learning

    #     # Fit models
    #     models, label_encoders = self.model_fit(historyDF, X, 
    #                             ['transaction_type', 'vendor_no_w9', 'customer_no_w9'],
    #                             test_size=0.2, random_state=42)
            
    #     # Apply models to new data
    #     total_count = len(newDataDF)
    #     newDataDF = newDataDF.reset_index(drop=True)
    #     newDataDF = newDataDF.apply(lambda row: self.populate_dependent_fields(row, row.name, total_count,
    #                                 models, label_encoders, le_bank_account_key,tfidf), axis=1)
    #     newDataDF['period_status'] = 'open'
    #     newDataDF['classification'] = 'review'
    #     newDataDF.to_excel('newDataPredictions.xlsx', index=False)

    #     newDataList = self.dataframe_to_models(newDataDF, outputModel)
        
    #     return {myObjects:newDataList}