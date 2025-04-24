from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.service import AuthService
from app.common.jwt import TokenPayload
from app.database import get_session
from app.users.models.update_user_model import UpdateUserModel
from app.users.service import UserService

class UserRouter:
    def __init__(self):
        self.router = APIRouter(
            prefix="/user",
            tags=["Users"]
        )
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("", self.user_information, methods=["GET"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("", self.update_user, methods=["PATCH"], status_code=status.HTTP_200_OK)

    async def user_information(self, response: Response, current_user: TokenPayload = Depends(AuthService.get_current_user_token), session: Session = Depends(get_session)):
        return await UserService.user_information(response, current_user, session)

    async def update_user(self, response: Response, userUpdateModel: UpdateUserModel, current_user: TokenPayload = Depends(AuthService.get_current_user_token), session: Session = Depends(get_session)):
        return await UserService.update_user(response, userUpdateModel, current_user, session)

user_router = UserRouter().router