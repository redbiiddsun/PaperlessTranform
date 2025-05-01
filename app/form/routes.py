from typing import Optional
import uuid
from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.service import AuthService
from app.common.jwt import TokenPayload
from app.database import get_session
from app.form.models.add_form_model import AddFormModel
from app.form.models.submit_form_model import SubmitFormModel
from app.form.service import FormService

class FormRouter:
    def __init__(self):
        self.router = APIRouter(
            prefix="/form",
            tags=["Forms"]
        )
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("", self.receive_form, methods=["GET"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/{form_id}", self.receive_form_with_id, methods=["GET"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("", self.add_form, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/{form_id}", self.delete_form, methods=["DELETE"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/{form_id}/submit", self.submit_form, methods=["POST"], status_code=status.HTTP_200_OK)



    async def add_form(self, response: Response, addFormModel: AddFormModel, current_user: TokenPayload = Depends(AuthService.get_current_user_token), session: Session = Depends(get_session)):
        return await FormService.add_form(response, addFormModel, current_user, session)

    async def receive_form(self, response: Response, current_user: TokenPayload = Depends(AuthService.get_current_user_token), session: Session = Depends(get_session)):
        return await FormService.receive_form(response, current_user, session)
    
    async def receive_form_with_id(self, form_id: uuid.UUID, session: Session = Depends(get_session)):
        return await FormService.receive_form_with_id(form_id, session)
    
    async def delete_form(self, form_id: uuid.UUID, current_user: TokenPayload = Depends(AuthService.get_current_user_token), session: Session = Depends(get_session)):
        return await FormService.delete_form(form_id, current_user, session)
    
    async def submit_form(self, form_id: uuid.UUID, submitFormModel: SubmitFormModel, current_user: Optional[TokenPayload] = Depends(AuthService.get_optional_current_user), session: Session = Depends(get_session)):
        return await FormService.submit_form(form_id, submitFormModel, current_user, session)
    

form_router = FormRouter().router