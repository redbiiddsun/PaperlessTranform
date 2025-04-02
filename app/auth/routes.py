from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.auth.models.register_user_model import RegisterUserModel
from app.auth.service import AuthService
from app.database import get_session

class AuthRouter:
    def __init__(self):
        self.router = APIRouter(
            prefix="/auth",
            tags=["authentication"]
        )
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/signup", self.signup, methods=["POST"], status_code=status.HTTP_201_CREATED)

    async def signup(self, registerUserModel: RegisterUserModel, session: Session = Depends(get_session)):
        return await AuthService.register_user(registerUserModel, session)
        


auth_router = AuthRouter().router