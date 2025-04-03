from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.models.otp_user_model import RequestOtpModel
from app.auth.models.register_user_model import RegisterUserModel
from app.auth.models.signin_model import SignInModel
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
        self.router.add_api_route("/signin", self.signin, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/requestotp", self.requestOtp, methods=["POST"], status_code=status.HTTP_200_OK)



    async def signup(self, registerUserModel: RegisterUserModel, session: Session = Depends(get_session)):
        return await AuthService.register_user(registerUserModel, session)
    
    async def signin(self, response: Response, signInModel: SignInModel, session: Session = Depends(get_session)):
        return await AuthService.signIn(response, signInModel, session)
    
    async def requestOtp(self, response: Response, requestOtpModel: RequestOtpModel, session: Session = Depends(get_session)):
        return await AuthService.requestOtp(response, requestOtpModel, session)

        


auth_router = AuthRouter().router