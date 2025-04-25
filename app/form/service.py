
from fastapi import Response
from sqlmodel import Session, select

from app.common.errors.user_error import  ExistingEmail, UserNotFound
from app.common.jwt import TokenPayload
from app.form.models.add_form_model import AddFormModel
from app.schemas import User
from app.schemas.form import Forms
from app.users.models.update_user_model import UpdateUserModel
from app.users.models.user_response import UserResponse


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
            schemas = addFormModel.schemas,
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
FormService = FormService()