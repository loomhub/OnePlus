from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional, Tuple, Type, TypeVar
import pandas as pd
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from ..models.emailConfig_model import emailsConfigModel
from ..models.bird_model import birdsModel
from ..repositories.myrepository import myRepository  # Assuming a base repository exists
# Define a type variable that can be any subclass of BaseModel
DTO = TypeVar('DTO', bound=BaseModel)


class MyService:
    def __init__(self, repository: myRepository):
        self.repository = repository

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
        # except Exception as e:  # General exception if needed, though specific ones are preferred
        #     await self.repository.rollback_changes()
        #     raise Exception(f"Unexpected error: {str(e)}")

    ############################################################################################################

    async def upsert_records(self, data_dto:DTO, model: Type[BaseModel], key_fields: dict) -> Tuple[bool, BaseModel]:
        """
        Upsert an entity based on the provided data.
        :param data_dto: Data transfer object containing entity details
        :param model: The SQLAlchemy model class of the entity
        :param key_fields: Dictionary of key fields and their corresponding values from data_dto
        :return: Tuple containing boolean (True if created, False if updated) and entity instance
        """
        try:
            filters = {field: getattr(data_dto, field) for field in key_fields}
            entity_instance = await self.repository.retrieve_unique_record(model, filters)

            if entity_instance:
                # Update it
                deleted = await self.repository.delete_data(entity_instance)
                await self.repository.commit_changes()
            
            entity_instance = model(**data_dto.dict())
            self.repository.db_session.add(entity_instance)
            await self.repository.db_session.commit()
            created = True
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
    def set_email_addresses(self, msg, emailsConfig:list[BaseModel],bird:BaseModel) -> str:
        """
        Creates email.
        :param data: List of data to be sent
        :param emailsConfig: Email configuration
        :param bird: Sender email
        :return: Email message
        """
        try:
            msg['From'] = bird.sender
            # Accumulate email addresses from all configs
            to_addresses = []
            cc_addresses = []
            bcc_addresses = []

            for config in emailsConfig:
                subject=config.subject
                if config.to:
                    to_addresses.append(config.to)
                if config.cc:
                    cc_addresses.append(config.cc)
                if config.bcc:
                    bcc_addresses.append(config.bcc)

            # Join addresses with a comma
            if to_addresses:
                msg['To'] = ', '.join(to_addresses)
            if cc_addresses:
                msg['Cc'] = ', '.join(cc_addresses)
            if bcc_addresses:
                msg['Bcc'] = ', '.join(bcc_addresses)
            
            msg['Subject'] = subject

            return msg
        except Exception as e:
            raise Exception(f"Email creation error: {str(e)}")
############################################################################################################
    def create_excel_file(self, data:list[BaseModel],subject:str) -> str:
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
            filePath = f"{subject}.xlsx"
            # Create Excel file
            df.to_excel(filePath, index=False)
            return filePath
        except Exception as e:
            raise Exception(f"Excel file creation error: {str(e)}")
############################################################################################################
    def attach_file(self, msg, filePath:str) -> str:
        """
        Attaches file to email.
        :param msg: Email message
        :param filePath: File path
        :return: Email message
        """
        try:
            attachment = open(filePath, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filePath}')
            msg.attach(part)
            return msg
        except Exception as e:
            raise Exception(f"Attachment error: {str(e)}")

############################################################################################################

    async def send_email(self, data:list[BaseModel],endpoint:str) -> bool:
        """
        Sends email.
        :param data: List of data to be sent
        :param endpoint: Email endpoint
        :return: True if successful
        """
        try:
            bird = await self.repository.retrieve_unique_record(birdsModel, {"active": "X"}) #Get sender email
            search = {"endpoint": endpoint, "inactive": ""}
            emailsConfig = await self.repository.retrieve_unique_record(emailsConfigModel,search,multiple="X") #Get email config
            msg = MIMEMultipart()
            print(type(msg))
            msg = self.set_email_addresses(msg,emailsConfig,bird)
            filePath = self.create_excel_file(data,msg['Subject'])
            msg=self.attach_file(msg,filePath)
            # Send email
            server = smtplib.SMTP(bird.server, bird.port)
            server.starttls()
            server.login(bird.sender, bird.pwd) 
            server.send_message(msg)
            server.quit()
            print("Email sent successfully!")

            return True
        except Exception as e:
            raise Exception(f"Email send error: {str(e)}")  