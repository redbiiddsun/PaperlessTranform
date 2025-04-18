from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.models.otp_user_model import RequestOtpModel
from app.auth.models.register_user_model import RegisterUserModel
from app.auth.models.reset_password_model import ResetPasswordModel
from app.auth.models.signin_model import SignInModel
from app.auth.models.verify_otp_model import VerifyOtpModel
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
        self.router.add_api_route("/request-reset", self.requestOtp, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/verify-otp", self.verifyOtp, methods=["POST"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/reset-password", self.resetPassword, methods=["POST"], status_code=status.HTTP_200_OK)




    async def signup(self, registerUserModel: RegisterUserModel, session: Session = Depends(get_session)):
        return await AuthService.register_user(registerUserModel, session)
    
    async def signin(self, response: Response, signInModel: SignInModel, session: Session = Depends(get_session)):
        return await AuthService.signIn(response, signInModel, session)
    
    async def requestOtp(self, response: Response, requestOtpModel: RequestOtpModel, session: Session = Depends(get_session)):
        return await AuthService.requestOtp(response, requestOtpModel, session)
    
    async def verifyOtp(self, response: Response, verifyOtpModel: VerifyOtpModel, session: Session = Depends(get_session)):
        return await AuthService.verifyOtp(response, verifyOtpModel, session)

    async def resetPassword(self, response: Response, resetPasswordModel: ResetPasswordModel, session: Session = Depends(get_session)):
        return await AuthService.resetPassword(response, resetPasswordModel, session)

auth_router = AuthRouter().router