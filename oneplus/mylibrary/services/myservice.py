from datetime import date
from email import encoders
import imaplib, email, re
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import smtplib
from typing import BinaryIO, List, Optional, Tuple, Type, TypeVar,Dict
import pandas as pd
from sqlalchemy.orm import class_mapper
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from ..dtos.service_dto import processedDTO, listProcessedDTO
from ..models.emailConfig_model import emailsConfigModel
from ..models.birds_model import birdsModel
from ..repositories.myrepository import myRepository  # Assuming a base repository exists
DTO = TypeVar('DTO', bound=BaseModel) # Define a type variable that can be any subclass of BaseModel


class MyService:
    def __init__(self, repository: myRepository):
        self.repository = repository
        self.html="oneplus/mylibrary/templates/email_template.html"
        self.imapServer = 'imap.gmail.com'
        self.inbox = 'inbox'
        self.server = ''
        self.port = 0
        self.sender = ''
        self.pwd = ''
        self.subject = ''
        self.emailSentCompleted = listProcessedDTO()

    ############################################################################################################    

    async def extract_all(self, model: Type[BaseModel]) -> Optional[list]:
        try:
            return await self.repository.retrieve_all(model)
        except Exception as e:
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")

    ############################################################################################################
    async def extract_pkey(self,model: Type[BaseModel],pkey: dict) -> Optional[BaseModel]:
        try:
            result = await self.repository.retrieve_unique_record(model, pkey)
            if result is None:
                print("Record not found")
            return result
        except SQLAlchemyError as e:  # Handling more specific database errors
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")

    ############################################################################################################
    async def search_records(self,model: Type[BaseModel],search_fields: dict) -> Optional[list]:
        try:
            result = await self.repository.retrieve_unique_record(model, search_fields,multiple='X')
            if result is None:
                print("Record not found")
            return result
        except SQLAlchemyError as e:  # Handling more specific database errors
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
    ############################################################################################################

    async def upsert_records(self, data_dto:DTO, model: Type[BaseModel], key_fields: dict,**kwargs) -> Tuple[bool, BaseModel]:
        """
        Upsert an entity based on the provided data.
        :param data_dto: Data transfer object containing entity details
        :param model: The SQLAlchemy model class of the entity
        :param key_fields: Dictionary of key fields and their corresponding values from data_dto
        :return: Tuple containing boolean (True if created, False if updated) and entity instance
        """
        update = kwargs.get('update', None)
        try:
            filters = {field: getattr(data_dto, field) for field in key_fields}
            entity_instance = await self.repository.retrieve_unique_record(model, filters)

            if not(entity_instance): # Entity instance does not exist -> Create
                entity_instance = model(**data_dto.dict())
                self.repository.db_session.add(entity_instance)
                await self.repository.db_session.commit()
                created = True
            
            elif update == 'X': # Update = 'X' , Entity instance exists -> Edit entity
                for key, value in data_dto.dict().items():
                    if hasattr(entity_instance, key):
                        setattr(entity_instance, key, value)

                self.repository.db_session.add(entity_instance)  # In case the session doesn't track the instance
                await self.repository.db_session.commit()
                created = True  # Since this is an update, not a create

            else: # Update = None , Entity instance exists -> Dont delete, don't create
                created = False
            
            return created, entity_instance

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
############################################################################################################
    async def delete_records(self, data_dto:DTO, model: Type[BaseModel], key_fields: dict) -> Tuple[bool, BaseModel]:
           """
           Delete an entity based on the provided data.
            :param data_dto: Data transfer object containing entity details
            :param model: The SQLAlchemy model class of the entity
            :param key_fields: Dictionary of key fields and their corresponding values from data_dto
            :return: Tuple containing boolean and entity instance
           """
           try:
            filters = {field: getattr(data_dto, field) for field in key_fields}
            entity_instance = await self.repository.retrieve_unique_record(model, filters)

            if entity_instance:
                deleted = await self.repository.delete_data(entity_instance)
                await self.repository.commit_changes()
            else:
                   # LLC not found
                deleted = False

            await self.repository.commit_changes()
            return deleted,entity_instance

           except Exception as e:
               # Handle specific database errors or re-raise
               await self.repository.rollback_changes()
               raise Exception(f"Database error: {str(e)}")
    
    ############################################################################################################
    # Truncate table
    async def truncate_records(self, model: Type[BaseModel]) -> bool:
        try:
            await self.repository.truncate_table(model)
            await self.repository.commit_changes()
            return True
        except Exception as e:
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
     
    ############################################################################################################    
    async def validate_data(self, records:List[Type[BaseModel]], fkey_checks: Dict[Type[BaseModel], str]) -> List[str]:
        errors = []
        for record in records:
            for model, field_mappings in fkey_checks.items():
                filters = {model_field: getattr(record, record_field) for record_field, model_field in field_mappings.items()}
                record_exists = await self.repository.retrieve_unique_record(model, filters)
                if not record_exists:
                    errors.append(f"Foreign key validation failed for {filters} in {model.__tablename__}")
        return errors

    ############################################################################################################
    async def validate_value_constraints(self,records:List[Type[BaseModel]], validate_keys: Dict[str, Tuple]) -> List[str]:
        errors = []
        for index, record in enumerate(records):
            for key, valid_values in validate_keys.items():
                # Using hasattr and getattr to handle attributes in BaseModel-derived classes.
                if hasattr(record, key):
                    value = getattr(record, key)
                    if value not in valid_values:
                        errors.append(f"Record {index} error: {key}='{value}' is not one of {valid_values}")
                else:
                    errors.append(f"Record {index} error: {key} is missing from the record")
        return errors
############################################################################################################
#############################################################################################################
    def parse_date(self,date_str):
        """Parse a date string into a date object with coercion for two different year formats."""
        if pd.isna(date_str):
            return None  # Directly return None for NaN values
        # Check if the date is in the format "YYYY-MM-DD"
        if len(date_str.split('-')) == 3 and len(date_str.split('-')[0]) == 4:
            return pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')
        
        if len(date_str.split('/')[-1]) == 4:
            return pd.to_datetime(date_str, format='%m/%d/%Y', errors='coerce')
        else:
            return pd.to_datetime(date_str, format='%m/%d/%y', errors='coerce')
#############################################################################################################
    # Convert the DataFrame to a list of dictionaries
    def format_date(self,x):
        return x.strftime('%Y-%m-%d') if not pd.isna(x) and isinstance(x, date) else None
#############################################################################################################
    def convert_variable_to_date(self,input):
        if not pd.api.types.is_datetime64_any_dtype(input):
            input = input.apply(self.parse_date)
            input = pd.to_datetime(input).dt.normalize()
        return input
#############################################################################################################
    def convert_columns_to_date(self, 
                        df: pd.DataFrame, 
                        column_names: List[str],
                        **kwargs) -> pd.DataFrame:
        null_value_date = kwargs.get('null_value_date', '2099-12-31')
  
        for column_name in column_names:
            if column_name in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df[column_name]):
                    df[column_name] = df[column_name].astype(str)
                    # Apply the date parsing method and handle NaN values after conversion
                    df[column_name] = df[column_name].apply(self.parse_date)
                    # Replace NaT with a default date and ensure all operations are on datetime format
                    df[column_name] = df[column_name].fillna(pd.Timestamp(null_value_date))
                    df[column_name] = pd.to_datetime(df[column_name]).dt.normalize()
            else:
                print(f"Column {column_name} not found in DataFrame.")
        
        return df
############################################################################################################  
    def convert_columns_to_datetime_to_date(self,
                        df: pd.DataFrame,
                        column_names: List[str],
                        **kwargs) -> pd.DataFrame:
        for column_name in column_names:
            if column_name in df.columns:
                df[column_name] = pd.to_datetime(df[column_name], errors='coerce').dt.date
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
    def convert_dataframe_columns(self,dfs: List[pd.DataFrame], column_names: List[str],conversion:str) -> List[pd.DataFrame]:
        if conversion == 'string':        
            for df in dfs:
                if df.empty == False:
                    df= self.convert_columns_to_string(df, column_names)
        elif conversion == 'numeric':
            for df in dfs:
                if df.empty == False:
                    df= self.convert_columns_to_numeric(df, column_names)
        elif conversion == 'int':
            for df in dfs:
                if df.empty == False:
                    df= self.convert_columns_to_int(df, column_names)
        elif conversion == 'date':
            for df in dfs:
                if df.empty == False:
                    df= self.convert_columns_to_date(df, column_names)
        elif conversion == 'datetime_to_date':
            for df in dfs:
                if df.empty == False:
                    df= self.convert_columns_to_datetime_to_date(df, column_names)
        return dfs
############################################################################################################
    def download_files(self,dfs: List[Tuple[pd.DataFrame, str]], title) -> None:
        for df,name in dfs:
            filename = f"{title}{name}.xlsx"
            df.to_excel(filename, index=False)
        return dfs
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
            if data:
                df = self.models_to_dataframe(data)
                dataframes.append(df)  # Append dataframe to list
            else:
                dataframes.append(pd.DataFrame())  # Append an empty dataframe if no data
        return dataframes
############################################################################################################

    def create_excel_file(self, data:list[BaseModel]) -> BytesIO:
        """
        Creates Excel file.
        :param data: List of data to be sent
        :param subject: Email subject
        :return: File path
        """
        try:
            # Verifying if all items can be converted to a dictionary
            dict_list = []
            for item in data:
                item_dict = {key: value for key, value in item.__dict__.items() if not key.startswith('_')}
                dict_list.append(item_dict)
            # Create a DataFrame
            df = pd.DataFrame(dict_list)
            # Create a BytesIO buffer
            output = BytesIO()
            
            # Write DataFrame to the buffer as an Excel file
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            # Rewind the buffer
            output.seek(0)
        
            return output
        except Exception as e:
            raise Exception(f"Excel file creation error: {str(e)}")
############################################################################################################
    def attach_file(self, msg: EmailMessage, inMemoryExcel: BinaryIO) -> EmailMessage:
        """
        Attaches file to email.
        :param msg: Email message
        :param inMemoryExcel: Binary IO file in memory
        :return: Email message
        """
        try:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(inMemoryExcel.read())
            encoders.encode_base64(part)    
            subject=f"{msg['Subject']}.xlsx"
            part.add_header('Content-Disposition', 'attachment', filename=subject)
            msg.attach(part)
            return msg
        except Exception as e:
            raise Exception(f"Attachment error: {str(e)}")

############################################################################################################
    def smpt_send_email(self,message:EmailMessage) -> bool:
        """
        Sends email.
        :param bird: Sender email
        :param msg: Email message
        :return: True if successful
        """
        try:
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.sender, self.pwd) 
            server.send_message(message)
            server.quit()
            print("Email sent successfully!")
            return True
        except Exception as e:
            raise Exception(f"Email send error: {str(e)}")
############################################################################################################
    def set_email_body(self, msg:EmailMessage,template:str) -> EmailMessage:
        """
        Creates email body.
        :param msg: Email message
        :param template: Email template
        :return: Email message
        """
        try:
            with open(template, 'r') as file:
                html = file.read()
            msg.attach(MIMEText(html, 'html'))
            return msg
        except Exception as e:
            raise Exception(f"Email body creation error: {str(e)}")
############################################################################################################

    def send_email(self, response_data:list[BaseModel],receiver:str,**kwargs) -> bool:
        """
        Sends email.
        :param data: List of data to be sent
        :param endpoint: Email endpoint
        :return: True if successful
        """
        try:
            message = MIMEMultipart()
            message['From'] = self.sender
            message['To'] = receiver
            message['Subject'] = self.subject
            message = self.set_email_body(message,self.html)
            inMemoryExcel = self.create_excel_file(response_data)
            message=self.attach_file(message,inMemoryExcel)
            result=self.smpt_send_email(message)
            return result
        except Exception as e:
            raise Exception(f"Email send error: {str(e)}")  
############################################################################################################ 
    async def set_server_settings(self):  
        bird = await self.repository.retrieve_unique_record(birdsModel, {"active": "X"}) #Get sender email
        if bird == None:
            return False
        else:
            self.server = bird.server
            self.port = bird.port
            self.sender = bird.sender
            self.pwd = bird.pwd
            return True 
############################################################################################################        
    def select_inbox(self):
        mail = imaplib.IMAP4_SSL(self.imapServer)
        mail.login(self.sender, self.pwd)
        mail.select(self.inbox)
        return mail
############################################################################################################
    def extract_email(self,address):
        match = re.search(r'<([^>]+)>', address)
        if match:
            return match.group(1)
        else:
            return address   
############################################################################################################
    async def check_receiver_access(self,from_address:str,endpoint:str,receiver:str) -> str:
        
        from_address=self.extract_email(from_address)
        if receiver == from_address:
            # Check receiver access
            active_endpoint = {"endpoint": endpoint, "to":receiver, "active": "Yes"}
            emailsConfig = await self.repository.retrieve_unique_record(emailsConfigModel,active_endpoint) #Get email config
            if emailsConfig == None:
                return None
            else:
                self.subject = emailsConfig.subject
                return receiver
        else:
            return None
                        
############################################################################################################
    def process_email(self,
                      response_data:list[BaseModel],
                      receiver:str,keyword:str,
                      mail:imaplib.IMAP4_SSL,
                      num) -> bool:
        sent=False
        if not any(done.receiver == receiver and done.report == keyword for done in self.emailSentCompleted.done):
            sent=self.send_email(response_data,receiver)
            print(f"Email sent to {receiver}")
            new_done = processedDTO(report=keyword, receiver=receiver)
            self.emailSentCompleted.done.append(new_done)
            mail.store(num, '+X-GM-LABELS', '\\Trash')
        else:
            print(f"Email already sent to {receiver}")
            mail.store(num, '+X-GM-LABELS', '\\Trash')
        return sent
############################################################################################################
    async def check_keyword_and_process_email(self,response_data:list[BaseModel],mail,endpoint:str,receiver:str,formatted_keyword:str,keyword:str) -> bool:
        
        sent = False
        ttype, data = mail.search(None, formatted_keyword)
      
        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            receiver = await self.check_receiver_access(msg['from'],endpoint,receiver)
            if receiver:
                sent = self.process_email(response_data,receiver,keyword,mail,num)
        return sent
############################################################################################################
    async def check_keyword_and_send_email(self, response_data:list[BaseModel],endpoint:str,**kwargs) -> bool:
            """
            Sends email.
            :param data: List of data to be sent
            :param endpoint: Email endpoint
            :return: True if successful
            """
            receiver = kwargs.get('receiver', None) 
            keyword = kwargs.get('keyword', None) 
            formatted_keyword = f'(SUBJECT "{keyword}")'
            sent = False

            try:
                # Get email
                success= await self.set_server_settings()
                if not success:
                    return False
                
                mail = self.select_inbox()
                if mail:
                    sent = await self.check_keyword_and_process_email(response_data,mail,endpoint,receiver,formatted_keyword,keyword)                
                    mail.close()
                    mail.logout()
                return sent
                
            except Exception as e:
                raise Exception(f"Email send error: {str(e)}")
############################################################################################################
    def set_dates(self, tdate):
        start_date = tdate.replace(day=1).date()
        end_date = (start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)).normalize().date()
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        return start_date_str, end_date_str, end_date

############################################################################################################
    def perform_period_close(self,historyDF, transtmpDF, cashDF):
        resultsDF=pd.DataFrame()
        startDatesDF = historyDF.groupby('bank_account_key')['tdate'].max().reset_index()
        
        # Loop over each row in startDatesDF
        for _, row in startDatesDF.iterrows():
            flag = 'closed'
            start_date_str, end_date_str, end_date = self.set_dates(row['tdate'])

            while flag == 'closed':
                # Read cashflowDF with the specified conditions
                cashflow_cond = (cashDF['bank_account_key'] == row['bank_account_key']) &\
                                (cashDF['start_date'] == start_date_str) &\
                                (cashDF['end_date'] == end_date_str) &\
                                (cashDF['period_status'] == 'closed')
                cashflow_subset = cashDF[cashflow_cond]

                if not cashflow_subset.empty:
                    # Read transactionstmpDF with the specified conditions
                    transactions_cond = (transtmpDF['bank_account_key'] == row['bank_account_key']) &\
                                        (transtmpDF['tdate'] >= start_date_str) & \
                                        (transtmpDF['tdate'] <= end_date_str)
                    transactions_subset = transtmpDF[transactions_cond]

                    if not transactions_subset.empty:

                        # Check if all rows in the transactions_subset have classification = 'clean'
                        if (transactions_subset['classification'] == 'clean').all():
                            # Set period_status = closed for these rows
                            transactions_subset['period_status'] = 'closed'
                            # Append these rows to resultsDF
                            resultsDF = pd.concat([resultsDF, transactions_subset])
                        else:
                            flag = 'open'
                else:
                    flag = 'open'
                # Move to the next month
                start_date = (pd.Timestamp(end_date) + pd.DateOffset(days=1)).normalize()
                start_date_str,end_date_str,end_date = self.set_dates(start_date)
                
        return resultsDF
            
############################################################################################################
    async def period_close(self, historyModel: Type[BaseModel], transactionstmpModel: Type[BaseModel],
                                 cashflowsModel: Type[BaseModel], outputDTO: Type[BaseModel]) :
        
        pkey=['bank_account_key', 'tdate', 'description', 'amount']

        #Step 1 Load Dataframes 
        historyDF, transtmpDF,cashDF = await self.load_data(historyModel,transactionstmpModel,cashflowsModel) # Load data from database
        
        #Step 2 Convert columns to appropriate data types
        historyDF, transtmpDF = self.convert_dataframe_columns([historyDF, transtmpDF],
                                                                             ['bank_account_key','tdate','description',
                                                                              'classification','period_status',
                                                                              'transaction_group','transaction_type',
                                                                              'vendor','customer','comments',
                                                                              'vendor_no_w9','customer_no_w9'],
                                                                             'string')
        historyDF, transtmpDF = self.convert_dataframe_columns([historyDF, transtmpDF],
                                                                             ['tdate'],
                                                                             'date')
        historyDF, transtmpDF = self.convert_dataframe_columns([historyDF, transtmpDF],
                                                                             ['amount'],
                                                                             'numeric')
        cashlist = self.convert_dataframe_columns([cashDF],['bank_account_key','start_date','end_date','period_status'],
                                                                             'string')
        cashDF = cashlist[0]
        
        cashlist = self.convert_dataframe_columns([cashDF],['start_date','end_date'],'date')
        cashDF = cashlist[0]

        cashlist = self.convert_dataframe_columns([cashDF],['cash_change','ending_balance','calc_balance'],
                                                                             'numeric')
        cashDF = cashlist[0]

        #Step 3 Perform period close
        resultsDF = self.perform_period_close(historyDF, transtmpDF, cashDF)
    #    self.download_files([(historyDF,'Transactions'),(transtmpDF,'Transactionstmp'),(cashDF,'Cashflows')],'STEP2')

        #Step 4 Convert DataFrame to ListDTO
        newDataList, errorList = self.convert_dataframe_to_list_dto(resultsDF, outputDTO)
        return newDataList, errorList

                