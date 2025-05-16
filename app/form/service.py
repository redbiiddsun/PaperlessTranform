
import pprint
import uuid
from fastapi import Response, UploadFile
from sqlmodel import Session, select

from app.common.errors.form_error import FormNotFound
from app.common.errors.user_error import  ExistingEmail, UserNotFound
from app.common.jwt import TokenPayload
from app.form.models.add_form_model import AddFormModel
from app.form.models.submit_form_model import SubmitFormModel
from app.schemas import User
from app.schemas.form import Forms
from app.schemas.form_result import FormResult
from app.text_processing.data_type_analyzer import DataTypeAnalyzer
from app.text_processing.form import Form
from app.text_processing.translation import Translation
from app.users.models.update_user_model import UpdateUserModel
from app.users.models.user_response import UserResponse
from app.text_processing.pdf_extractor import PDFExtractor

class FormService:

    def __init__(self):
        pass

    async def add_form(self, response: Response, addFormModel: AddFormModel, current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()
        
        new_form = Forms(
            name = addFormModel.name,
            schemas = addFormModel.model_dump(by_alias=True).get("schemas"),
            description = addFormModel.description,
            width = addFormModel.width,   
            requiredLogin = addFormModel.requiredLogin,
            userId = user.id,
        )

        session.add(new_form)
        session.commit()
        session.refresh(new_form)

        return {
            "status": "success",
            "form": new_form,
        }
    
    async def receive_form(self, response: Response, current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()
        
        all_form = session.exec(
            select(Forms).where(Forms.userId == current_user.user_id)
        )

        forms_data = [form.dict() for form in all_form.all()]


        return {
            "status": "success",
            "form": forms_data,
        }
    
    async def receive_form_with_id(self, form_id: uuid.UUID, session: Session):
        
        form = session.exec(
            select(Forms).where(Forms.id == form_id)
        ).first()

        if form is None:
            raise FormNotFound()

        return {
            "status": "success",
            "form": form,
        }
    
    async def delete_form(self, form_id: uuid.UUID,current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()
        
        form = session.exec(
            select(Forms).where(Forms.userId == current_user.user_id, Forms.id == form_id)
        ).first()

        if form is None:
            raise FormNotFound()
        
        session.delete(form)
        session.commit()

        return {
            "status": "success",
            "message": "Form deleted successfully",
            "form": form,
        }
    
    async def submit_form(self, form_id: uuid.UUID, submitFormModel: SubmitFormModel, current_user: TokenPayload, session: Session):

        if current_user is not None:

            user = session.exec(
                select(User).where(User.id == current_user.user_id)
            ).first()

            if user is None:
                raise UserNotFound()
            
        form = session.exec(
            select(Forms).where(Forms.id == form_id)
        ).first()

        if form is None:
            raise FormNotFound()
            
        new_form_result = FormResult(
            formId = form_id,
            userId = current_user.user_id if current_user is not None else None,
            result = submitFormModel.model_dump(by_alias=True).get("data"),
        )

        session.add(new_form_result)
        session.commit()
        session.refresh(new_form_result)

        return {
            "status": "success",
            "message": "Form has been submitted successfully",
        }
    

    async def receive_form_result(self, form_id: uuid.UUID, current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()
            
        form = session.exec(
            select(Forms).where(Forms.id == form_id)
        ).first()

        if form is None:
            raise FormNotFound()
        
        form_result = session.exec(
            select(FormResult).where(FormResult.formId == form_id)
        ).all()

        results_only = [item.result for item in form_result]

        return {
            "status": "success",
            "form_result": results_only,
        }
    
    async def upload_pdf_form(self, file: UploadFile, current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()
        
        file_bytes = await file.read()

        pdf_text = PDFExtractor().extract_text(file_bytes)

        extracted_text = Form().extract_labels(pdf_text)

        translated_text = await Translation().translate(extracted_text)

        translated_fields = [item['translated_field'] for item in translated_text]

        data_type = await DataTypeAnalyzer().analyze_fields_async(translated_fields)

        mapping_value = DataTypeAnalyzer().mapping_value(data_type, translated_text)

        return {
            "status": "success",
            "result": mapping_value,
        }

FormService = FormService()