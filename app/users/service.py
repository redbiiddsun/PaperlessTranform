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

from passlib.context import CryptContext
from app.users.schemas.user_request import UserUpdateRequest
from app.users.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self):
        pass

    async def user_information(self, response: Response, current_user: TokenPayload, session: Session):

        user_info = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if not user_info:
            raise UserNotFound(user_id=current_user.user_id)

        response = UserResponse.model_validate(user_info)

        return {
            "status": "success",
            "user": response,
        }
    
    async def update_user(payload: UserUpdateRequest, response: Response, current_user: TokenPayload, session: Session):
        user = session.get(User, current_user.sub)
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"detail": "User not found"}

        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.last_name is not None:
            user.last_name = payload.last_name
        if payload.email is not None:
            user.email = payload.email

        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
        }
    


UserService = UserService()
