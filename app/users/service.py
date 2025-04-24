from datetime import timezone
import secrets
import bcrypt
from fastapi import HTTPException, Response, status
from sqlmodel import Session, select
from app.auth.models.otp_user_model import RequestOtpModel
from app.auth.models.reset_password_model import ResetPasswordModel
from app.auth.models.signin_model import SignInModel
from app.auth.models.register_user_model import RegisterUserModel
from app.auth.models.verify_otp_model import VerifyOtpModel
from app.common.errors.user_error import ExistingEmail, ExpiredOTP, InvalidEmailFormat, InvalidEmailPassword, InvalidOTP, InvalidToken, MaximumAttempOTP, OTPAlreadyVerified, TokenExpired, UserNotFound
from app.common.jwt import TokenPayload, signJwt
from app.common.regex import EMAIL_REGEX
from app.common.time import utc_now
from app.common.util import generate_otp, generate_otp_reference
from app.common.email import email_sender
from app.schemas import User
from app.schemas.otp import Otp
from app.schemas.reset_password_session import ResetPasswordSession
from app.users.models.user_response import UserResponse

class UserService:

    def __init__(self):
        pass

    async def user_information(self, response: Response, current_user: TokenPayload, session: Session):

        user_info = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        print(type(user_info))

        response = UserResponse.model_validate(user_info)

        return {
            "status": "success",
            "user": response,
        }


UserService = UserService()
