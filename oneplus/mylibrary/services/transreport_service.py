from datetime import date
import logging
from typing import List, Type
from fastapi import HTTPException
import pandas as pd
from pydantic import BaseModel, create_model
from ..repositories.transreport_repository import transreportRepository
from .myservice import MyService


class transreportService(MyService):
    def __init__(self, transreport_repository: transreportRepository):
        super().__init__(transreport_repository)

    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]

        for record in records:
            try:
                key_fields = {'sequence_id': record.sequence_id}  # Adjust according to actual key fields
                created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                results.append( {"created": created, myObjects: result} )
            except Exception as e:
                logging.error(f"Failed to update or create record: {str(e)}")
                raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
############################################################################################################
    def set_years(self,years:int):
        if not years:
            years = 2
        
        end_year = date.today().year
        start_year = end_year - years
        return start_year, end_year    

############################################################################################################
    def data_conversions(self,transactionsDF,cashDF):
        transactionsList = self.convert_dataframe_columns([transactionsDF],
                                                ['bank_account_key','transaction_type','transaction_group'],'string')
        transactionsDF = transactionsList[0]

        transactionsList = self.convert_dataframe_columns([transactionsDF],['tdate'],'date')
        transactionsDF = transactionsList[0]

        transactionsList = self.convert_dataframe_columns([transactionsDF],['amount'],'numeric')
        transactionsDF = transactionsList[0]

        cashList = self.convert_dataframe_columns([cashDF],['bank_account_key'],'string')
        cashDF = cashList[0]

        cashList = self.convert_dataframe_columns([cashDF],['start_date'],'date')
        cashDF = cashList[0]

        cashList = self.convert_dataframe_columns([cashDF],['ending_balance'],'numeric')
        cashDF = cashList[0] 

        return transactionsDF,cashDF
############################################################################################################
    def filter_dates(self,transactionsDF,cashDF,start_year,end_year):
        transactionsDF = transactionsDF[
                (transactionsDF['tdate'].dt.year >= start_year) & 
                (transactionsDF['tdate'].dt.year <= end_year)]
        
        cashDF = cashDF[
                (cashDF['start_date'].dt.year >= start_year) & 
                (cashDF['start_date'].dt.year <= end_year)]
        return transactionsDF,cashDF
############################################################################################################
    def perform_report_summary_pivot(self,transactionsDF, row, resultsDF):

        pivot_df = transactionsDF[transactionsDF[row.calc_method].isin(row.fields.split(','))
                       ].groupby([transactionsDF['bank_account_key'], 
                       transactionsDF['tdate'].dt.to_period('M')])['amount'].sum().reset_index()
        
        if pivot_df.shape[0] > 0:
            pivot_df['category'] = row.category
            pivot_df['sequence_id'] = row.sequence_id
            pivot_df['month'] = pivot_df['tdate'].astype(str)
            pivot_df = pivot_df.drop(columns=['tdate'])
            resultsDF = pd.concat([resultsDF, pivot_df], ignore_index=True)
        
        return resultsDF
############################################################################################################
    def perform_calculate_cash(self,cashDF, reportrow, resultsDF):
        for index, cashrow in cashDF.iterrows():
            new_row = {
                'bank_account_key': cashrow['bank_account_key'],
                'category': reportrow.category,
                'sequence_id': reportrow.sequence_id,
                'month': cashrow['start_date'].strftime('%Y-%m'),
                'amount': cashrow['ending_balance']
            }
    # Append the new row to resultsDF
            resultsDF = pd.concat([resultsDF, pd.DataFrame([new_row])], ignore_index=True)
        return resultsDF

############################################################################################################
    def perform_pivot_by_months(self,resultsDF):
        calcDF = resultsDF.pivot(index=['bank_account_key', 'sequence_id','category'], columns='month', values='amount').reset_index()      
        calcDF = calcDF.fillna(0)
        calcDF.columns.name = None
        return calcDF
############################################################################################################
    def initialize_variables(self,reportDF):

        revenue_row = reportDF.loc[reportDF['category'] == 'REVENUE']
        revCategory = revenue_row.to_dict(orient='records')[0]

        expenses_row = reportDF.loc[reportDF['category'] == 'EXPENSES']
        expCategory = expenses_row.to_dict(orient='records')[0]

        netIncome_row = reportDF.loc[reportDF['category'] == 'NET INCOME']
        netIncomeCategory = netIncome_row.to_dict(orient='records')[0]

        variables = {'bank_account_key': '','month': '','revenue':0,'expenses':0,
                     'revCategory': revCategory, 'expCategory': expCategory, 'netIncomeCategory': netIncomeCategory}

        # revCategory = {'sequence_id': 3, 'category': 'REVENUE'}
        # expCategory = {'sequence_id': 14, 'category': 'EXPENSES'}
        # netIncomeCategory = {'sequence_id': 15, 'category': 'NET INCOME'}
        return variables
############################################################################################################
    def insert_calculated_values(self,calcDF, variables):
        if variables['bank_account_key'] != '':
            new_row = {'bank_account_key': variables['bank_account_key'],
                        'category': variables['revCategory']['category'],
                        'sequence_id': variables['revCategory']['sequence_id'],
                        'month': variables['month'],
                        'amount': variables['revenue']
                    }
            calcDF = pd.concat([calcDF, pd.DataFrame([new_row])], ignore_index=True)

            new_row = {'bank_account_key': variables['bank_account_key'],
                        'category': variables['expCategory']['category'],
                        'sequence_id': variables['expCategory']['sequence_id'],
                        'month': variables['month'],
                        'amount': variables['expenses']
                    }
            calcDF = pd.concat([calcDF, pd.DataFrame([new_row])], ignore_index=True)

            new_row = {'bank_account_key': variables['bank_account_key'],
                        'category': variables['netIncomeCategory']['category'],
                        'sequence_id': variables['netIncomeCategory']['sequence_id'],
                        'month': variables['month'],
                        'amount': variables['revenue'] + variables['expenses']
                    }
            calcDF = pd.concat([calcDF, pd.DataFrame([new_row])], ignore_index=True)

        return calcDF

############################################################################################################
    def set_variables(self,variables, row):
        variables['bank_account_key'] = row.bank_account_key
        variables['month'] = row.month
        variables['revenue'] = 0
        variables['expenses'] = 0
        return variables
############################################################################################################
    def calculate_revenue_expenses(self,variables, row):
        if row.category == 'Rent' or row.category == 'Interest':
            variables['revenue'] += row.amount

        elif row.category == 'Insurance' or \
            row.category == 'Taxes' or \
            row.category == 'Repair' or \
            row.category == 'Management' or \
            row.category == 'Utilities' or \
            row.category == 'Cleaning' or \
            row.category == 'Professional Services' or \
            row.category == 'Travel' or \
            row.category == 'HOA' or \
            row.category == 'Allocation'  :
            variables['expenses'] += row.amount
    
        return variables
############################################################################################################
    async def summarize_performance(self,transreportsModel,transactionsModel,cashflowsModel,
                                    bank_account_key:str,years:int):
        
        # Set years
        start_year, end_year = self.set_years(years)

        #Step 1 - Retrieve data from the database
        reportDF,transactionsDF, cashDF = await self.load_data(transreportsModel,transactionsModel,cashflowsModel) # Load data from database
        
        if bank_account_key:
            transactionsDF = transactionsDF[transactionsDF['bank_account_key'] == bank_account_key]
            cashDF = cashDF[cashDF['bank_account_key'] == bank_account_key]

        #Step 2 - Data conversions
        transactionsDF,cashDF = self.data_conversions(transactionsDF,cashDF) # Data conversions  

        # Step 3 - Filter dates
        transactionsDF, cashDF = self.filter_dates(transactionsDF,cashDF,start_year,end_year)
        
        #Step 4 - Perform pivot operation for non-calculated fields
        resultsDF = pd.DataFrame()
        for row in reportDF.itertuples():
            if row.calc_method != 'Calculated':
                resultsDF = self.perform_report_summary_pivot(transactionsDF, row, resultsDF)
            elif row.category == 'CASHFLOW':
                resultsDF = self.perform_calculate_cash(cashDF, row, resultsDF)

#         # #Step 5 - Perform calculations for REVENUE, EXPENSES and NET INCOME
        resultsDF = resultsDF.sort_values(by=['bank_account_key', 'month','sequence_id'])
        self.download_files([(resultsDF,'BeforeExpenseCalculation')],'STEP3A')
        calcDF = pd.DataFrame()
        variables = self.initialize_variables(reportDF)

        for row in resultsDF.itertuples():
            if row.bank_account_key != variables['bank_account_key'] or row.month != variables['month']:
                calcDF = self.insert_calculated_values(calcDF, variables)
                variables = self.set_variables(variables, row)
            variables = self.calculate_revenue_expenses(variables, row)
        
        calcDF = self.insert_calculated_values(calcDF, variables)
        resultsDF = pd.concat([resultsDF, calcDF], ignore_index=True)

        #Step 6 - Prepare list of dictionaries
        resultsDF = self.perform_pivot_by_months(resultsDF)
        resultsDF = resultsDF.sort_values(by=['bank_account_key','sequence_id'])
        resultList = resultsDF.to_dict(orient='records')
        return resultList

            

