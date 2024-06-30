from datetime import datetime, timedelta
import logging
from typing import List, Type
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel
from ..models.bankaccounts_model import bankaccountsModel
from ..repositories.cashflow_repository import cashflowRepository
from .myservice import MyService

class cashflowService(MyService):
    def __init__(self, cashflow_repository: cashflowRepository):
        super().__init__(cashflow_repository)
############################################################################################################
    def insert_last_rows(self, df: pd.DataFrame, 
                         recordsDF: pd.DataFrame,
                         myDTO: Type[BaseModel], 
                         group_col: str, 
                         sort_cols: List[str]) -> pd.DataFrame:
        # Sort existing data by specified columns
        df.sort_values(by=sort_cols, inplace=True)
        
        # Get the last row for each group
        last_rows = df.groupby(group_col).last().reset_index()
        
        # Convert the last rows to list of records
        new_records = [myDTO(**row.to_dict()) for _, row in last_rows.iterrows()]
        
        # Convert records to DataFrame and concatenate
        new_records_df = pd.DataFrame([record.dict() for record in new_records])
        recordsDF = pd.concat([recordsDF, new_records_df], ignore_index=True)
    #    recordsDF.sort_values(by=sort_cols, inplace=True)
        
        return recordsDF
############################################################################################################
    def set_gap_dates(self, recordsDF: pd.DataFrame, i: int, record: pd.Series) -> pd.Series:
        prev_record = recordsDF.iloc[i - 1]
        prev_end_date = prev_record['end_date']
        current_start_date = record['start_date']
        gap_start_date = prev_end_date + timedelta(days=1)
        return prev_record, current_start_date, gap_start_date
############################################################################################################
    def fill_gaps_logic(self, recordsDF: pd.DataFrame) -> pd.DataFrame:
        final_recordsDF = pd.DataFrame(columns=recordsDF.columns)
        # Group by bank_account_key and iterate through each group separately
        grouped = recordsDF.groupby('bank_account_key')
        
        # Loop through the records
        for key, group in grouped:
            
            group = group.drop_duplicates(subset=['bank_account_key', 'start_date', 'end_date'])
            group = group.sort_values(by='start_date')  # Ensure the group is sorted by start_date
            group = group.reset_index(drop=True)
            
            for i, record in group.iterrows():
                if isinstance(record['start_date'], datetime):
                    record['start_date'] = record['start_date'].date()    
                if isinstance(record['end_date'], datetime):
                    record['end_date'] = record['end_date'].date()


                if i == 0 or record['start_date'] == group.iloc[i - 1]['end_date'] + timedelta(days=1):
                    final_recordsDF = pd.concat([final_recordsDF, pd.DataFrame([record])], ignore_index=True)
                else:
                    prev_record = group.iloc[i - 1]

                    current_start_date = record['start_date']
                    if isinstance(current_start_date, datetime):
                        current_start_date = current_start_date.date()
                    
                    gap_start_date = prev_record['end_date'] + timedelta(days=1)
                    if isinstance(gap_start_date, datetime):
                        gap_start_date = gap_start_date.date()

                    while gap_start_date < current_start_date:
                        gap_end_date = (gap_start_date + pd.offsets.MonthEnd(0))
                        if isinstance(gap_end_date, datetime):
                            gap_end_date = gap_end_date.date()

                        if gap_end_date >= current_start_date:
                            gap_end_date = current_start_date - timedelta(days=1)
                            if isinstance(gap_end_date, datetime):
                                gap_end_date = gap_end_date.date()

                        gap_record = {'bank_account_key': prev_record['bank_account_key'],
                        'start_date': gap_start_date,
                        'end_date': gap_end_date,
                        'cash_change': 0,
                        'ending_balance': prev_record['ending_balance'],
                        'calc_balance': prev_record['calc_balance'],
                        'period_status': prev_record['period_status']
                    }
                        final_recordsDF = pd.concat([final_recordsDF, pd.DataFrame([gap_record])], ignore_index=True)
                        gap_start_date = gap_end_date + timedelta(days=1)
                        if isinstance(gap_start_date, datetime):
                            gap_end_date = gap_start_date.date()

                    final_recordsDF = pd.concat([final_recordsDF, pd.DataFrame([record])], ignore_index=True)
        return final_recordsDF
    
        
############################################################################################################
    async def fill_gaps_in_months(self, records:List[Type[BaseModel]], 
                                  model: Type[BaseModel],
                                  outputDTO: Type[BaseModel]):
        try:
            #Step 1 Load Dataframes
            recordsDF = pd.DataFrame([record.dict() for record in records])
            cashflowsList = await self.load_data(model) # Load data from database
            cashflowsDataDF = cashflowsList[0]  # Extract the single dataframe from the list

            #Step 2 Convert columns to appropriate data types
            cashflowsDataDF, recordsDF = self.convert_dataframe_columns([cashflowsDataDF,recordsDF],
                                                        ['bank_account_key','period_status'],
                                                                         'string')
            cashflowsDataDF,recordsDF = self.convert_dataframe_columns([cashflowsDataDF,recordsDF],
                                                        ['start_date','end_date'],
                                                        'date')
            cashflowsDataDF,recordsDF = self.convert_dataframe_columns([cashflowsDataDF,recordsDF],
                                                         ['cash_change','ending_balance','calc_balance'],
                                                        'numeric')
            self.download_files([(cashflowsDataDF,'Cashflows'),(recordsDF,'PostData')],'STEP2')
            #Step 3 Insert last rows for each bank_account_key
            if cashflowsDataDF.empty == False:
                cashflowsDataDF = cashflowsDataDF[cashflowsDataDF['period_status'] == 'closed']
                recordsDF = self.insert_last_rows(cashflowsDataDF, recordsDF, outputDTO,
                                                'bank_account_key', ['bank_account_key', 'start_date'])
                
                [recordsDF] = self.convert_dataframe_columns([recordsDF],
                                                        ['start_date','end_date'],
                                                        'datetime_to_date')
                
            
            # Step 4 Create a new DataFrame to hold the final records to be posted
            final_recordsDF = self.fill_gaps_logic(recordsDF)

            #Step 5 Convert DataFrame to ListDTO
            newDataList, errorList = self.convert_dataframe_to_list_dto(final_recordsDF, outputDTO)
            return newDataList, errorList

        except Exception as e:
            logging.error(f"Failed to extract all records: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
############################################################################################################    
    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):  
        results=[]
        errors=[]

        # Validate data
        fkey_checks = {bankaccountsModel: {'bank_account_key': 'bank_account_key'}}  # Fkey Model: {input data column: Model column}} 
        errors = await self.validate_data(records, fkey_checks)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'bank_account_key': record.bank_account_key,
                                'start_date': record.start_date,
                                'end_date':record.end_date}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
############################################################################################################
    def perform_data_conversions(self, dataframes: List[pd.DataFrame]) -> List[pd.DataFrame]:  

        cashflowsDataDF = dataframes[0]
        transactionstmpDF = dataframes[1]

        cashflowslist = self.convert_dataframe_columns([cashflowsDataDF],
                                                        ['bank_account_key','period_status'],'string')
        cashflowsDataDF = cashflowslist[0]
        transactionstmpList = self.convert_dataframe_columns([transactionstmpDF],
                                                    ['bank_account_key'],'string')
        transactionstmpDF = transactionstmpList[0]
        
        cashflowslist = self.convert_dataframe_columns([cashflowsDataDF],
                                                    ['start_date','end_date'],
                                                    'date')
        cashflowsDataDF = cashflowslist[0]
        
        transactionstmpList = self.convert_dataframe_columns([transactionstmpDF],
                                                    ['tdate'],'date')
        transactionstmpDF = transactionstmpList[0]
        
        cashflowslist = self.convert_dataframe_columns([cashflowsDataDF],
                                                     ['cash_change','ending_balance','calc_balance'],
                                                    'numeric')
        cashflowsDataDF = cashflowslist[0]
        transactionstmpList = self.convert_dataframe_columns([transactionstmpDF],
                                                     ['amount'],'numeric')
        transactionstmpDF = transactionstmpList[0]
        self.download_files([(cashflowsDataDF,'Cashflows'),(transactionstmpDF,'Transactionstmp')],'STEP2')
        return [cashflowsDataDF, transactionstmpDF]    

        
############################################################################################################
    def get_last_rows(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        group_by = kwargs.get('group_by')
        latest_by = kwargs.get('latest_by')

        last_rows_idx = df.groupby(group_by)[latest_by].idxmax()
        last_rows = df.loc[last_rows_idx]
        return last_rows
############################################################################################################
    def create_new_cashflowsDF(self, transactionstmpDF: pd.DataFrame, lastrowsDF: pd.DataFrame) -> pd.DataFrame:
        newCashflowsDF = transactionstmpDF[['bank_account_key', 'tdate', 'amount']].copy()
        # Merge newCashflowsDF with last_rows to get the end_date for each bank_account_key
        mergedDF = newCashflowsDF.merge(lastrowsDF[['bank_account_key', 'end_date']], on='bank_account_key', how='left')

        # Filter out rows where tdate <= end_date
        filteredDF = mergedDF[mergedDF['tdate'] > mergedDF['end_date']]

        # Drop the end_date column as it's no longer needed
        newCashflowsDF = filteredDF.drop(columns=['end_date'])
        return newCashflowsDF
############################################################################################################
    def add_start_end_dates(self, newCashflowsDF: pd.DataFrame) -> pd.DataFrame:
        # Convert 'tdate' to datetime objects
        newCashflowsDF['tdate'] = pd.to_datetime(newCashflowsDF['tdate'])

# Calculate start and end of the month for each 'tdate'
        newCashflowsDF['start_date'] = newCashflowsDF['tdate'].dt.to_period('M').dt.to_timestamp()
        newCashflowsDF['end_date'] = newCashflowsDF['tdate'] + pd.offsets.MonthEnd(0)

        listDF = self.convert_dataframe_columns([newCashflowsDF],
                                                    ['tdate','start_date','end_date'],
                                                    'date')
        newCashflowsDF = listDF[0]

        return newCashflowsDF
############################################################################################################
    def calculate_ending_balance(self, newCashflowsDF: pd.DataFrame, lastrowsDF: pd.DataFrame) -> pd.DataFrame:
        # Calculate cash change for each period
        resultsDF = newCashflowsDF.pivot_table(
            index=['bank_account_key', 'start_date', 'end_date'], 
            values='amount', aggfunc='sum').reset_index()
        resultsDF.rename(columns={'amount': 'cash_change'}, inplace=True)

        # Initialize ending_balance, calc_balance, and period_status columns
        resultsDF['ending_balance'] = 0
        resultsDF['calc_balance'] = 0
        resultsDF['period_status'] = 'open'
        
        # Concatenate lastrowsDF and resultsDF
        resultsDF = pd.concat([lastrowsDF, resultsDF], ignore_index=True)
        resultsDF = resultsDF.drop(columns=['id'])
        
        # Caluclate calc_balance
        resultsDF = resultsDF.sort_values(by=['bank_account_key', 'start_date']).reset_index(drop=True)
        for idx, row in resultsDF.iterrows():
            if idx > 0 and row['bank_account_key'] == resultsDF.at[idx - 1, 'bank_account_key']:
                resultsDF.at[idx, 'calc_balance'] = resultsDF.at[idx - 1, 'calc_balance'] + row['cash_change']
        
        return resultsDF
############################################################################################################
    async def calculate_cashflows_from_transactionstmp(
                                              self, 
                                              model: Type[BaseModel], transactionstmp_model: Type[BaseModel],
                                  outputDTO: Type[BaseModel]):
        try:
            #Step 1 Load Dataframes           
            cashflowsDataDF, transactionstmpDF = await self.load_data(model,transactionstmp_model) # Load data from database

            #Step 2 Convert columns to appropriate data types
            cashflowsDataDF, transactionstmpDF = self.perform_data_conversions([cashflowsDataDF,transactionstmpDF])

            #Step 3 # cashflowsDataDF should keep records with period_status equal 'closed'
            cashflowsDataDF = cashflowsDataDF[cashflowsDataDF['period_status'] == 'closed']
            lastrowsDF = self.get_last_rows(cashflowsDataDF, group_by = 'bank_account_key', latest_by = 'start_date')

            # Step 4 Build newcashflowsDataDF
            newCashflowsDF = self.create_new_cashflowsDF(transactionstmpDF, lastrowsDF)

            # Step 5 Add start_date and end_date columns to newCashflowsDF
            newCashflowsDF = self.add_start_end_dates(newCashflowsDF)

            # Step 6 Calculate ending_balance for each month
            resultsDF = self.calculate_ending_balance(newCashflowsDF, lastrowsDF)
            self.download_files([(resultsDF,'Calculated Cashflows')],'STEP6')
            
            #Step 7 Convert DataFrame to ListDTO
            newDataList, errorList = self.convert_dataframe_to_list_dto(resultsDF, outputDTO)
            return newDataList, errorList

        except Exception as e:
            logging.error(f"Failed to extract all records: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

   
