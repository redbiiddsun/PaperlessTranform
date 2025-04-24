from datetime import timezone
import secrets
import bcrypt
from fastapi import Cookie, Response
from sqlmodel import Session, select
from app.auth.models.otp_user_model import RequestOtpModel
from app.auth.models.reset_password_model import ResetPasswordModel
from app.auth.models.signin_model import SignInModel
from app.auth.models.register_user_model import RegisterUserModel
from app.auth.models.verify_otp_model import VerifyOtpModel
from app.common.constance.env import Environment
from app.common.errors.user_error import ExistingEmail, ExpiredOTP, InvalidEmailFormat, InvalidEmailPassword, InvalidOTP, InvalidToken, MaximumAttempOTP, OTPAlreadyVerified, TokenExpired, Unauthorized, UserNotFound
from app.common.jwt import TokenPayload, decodeJwt, signJwt
from app.common.regex import EMAIL_REGEX
from app.common.time import utc_now
from app.common.util import generate_otp, generate_otp_reference
from app.common.email import email_sender
from app.schemas import User
from app.schemas.otp import Otp
from app.schemas.reset_password_session import ResetPasswordSession
from app.config import settings

class AuthService:

    HASH_SALT = bcrypt.gensalt(10)


    def __init__(self):
        pass

    async def register_user(self, registerUserModel: RegisterUserModel, session: Session):

        new_user = User(
            email= registerUserModel.email,
            password= bcrypt.hashpw(registerUserModel.password.encode("utf-8"), self.HASH_SALT).decode("utf-8"),
            firstname= registerUserModel.firstname,
            lastname= registerUserModel.lastname,
        )

        if EMAIL_REGEX.match(registerUserModel.email) is None:
            raise  InvalidEmailFormat()

        # Check if the email already exists
        existing_email = session.exec(
            select(User).where(User.email == registerUserModel.email)
        ).first()

        if existing_email:
            raise ExistingEmail()

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {
            "status": "success",
            "message": "User registered successfully",
        }
    

    async def signIn(self, response: Response, loginModel: SignInModel, session: Session):

        if EMAIL_REGEX.match(loginModel.email) is None:
            raise InvalidEmailFormat()
        
        # Check if the email already exists
        current_user = session.exec(
            select(User).where(User.email == loginModel.email)
        ).first()

        if current_user is None:
            raise InvalidEmailPassword()
        
        if not bcrypt.checkpw(loginModel.password.encode("utf-8"), current_user.password.encode("utf-8")):
            raise InvalidEmailPassword()
        
        if(settings.ENV == Environment.PRODUCTION):
            response.set_cookie(key = "session", 
                                value = signJwt(current_user.id),
                                domain= settings.DOMAIN, 
                                path="/",
                                max_age = 60 * 60 * 24,
                                samesite="none",
                                secure=True,
                                )
        else:
            response.set_cookie(key = "session", 
                                value = signJwt(current_user.id),       
                                path="/",
                                max_age = 60 * 60 * 24,
                                )

        return {
            "status": "success",
            "message": "Signin successfully",
        }
    
    async def requestOtp(self, response: Response, requestOtpModel: RequestOtpModel, session: Session):
        if EMAIL_REGEX.match(requestOtpModel.email) is None:
            raise InvalidEmailFormat()
        
        # Check if the email already exists
        current_user = session.exec(
            select(User).where(User.email == requestOtpModel.email)
        ).first()

        if current_user is None:
            raise UserNotFound()
        
        new_otp = Otp(
            email = requestOtpModel.email,
            otp = generate_otp(),
            referenceCode = generate_otp_reference(),
            userId= current_user.id,
        )

        session.add(new_otp)
        session.commit()
        session.refresh(new_otp)

        # Send OTP to the user's email
        email_sender.send_email(to_email = requestOtpModel.email, 
                                subject = 'Paperlesstranform - OTP to Reset Your Password', 
                                body = 'Your OTP is: {} with ref code: {}'.format(new_otp.otp, new_otp.referenceCode), 
                                from_email = 'noreply@paperlesstranform.com')

        return {
            "status": "success",
            "message": "OTP sent successfully",
            "refCode": new_otp.referenceCode,
            "token": new_otp.id,
        }
    
    async def verifyOtp(self, response: Response, verifyOtpModel: VerifyOtpModel, session: Session):

        current_otp = session.exec(
            select(Otp).where(Otp.id == verifyOtpModel.token)
        ).first()

        if(current_otp is None):
            raise InvalidOTP()
        
        if(current_otp.isVerified):
            raise OTPAlreadyVerified()
        
        if utc_now() > current_otp.expireAt.replace(tzinfo=timezone.utc):
            raise ExpiredOTP()
        
        if(current_otp.attempted >= 3):
            raise MaximumAttempOTP()

        if(current_otp.otp != verifyOtpModel.otp):
            # Add a for the number of attempts
            current_otp.attempted = current_otp.attempted +  1
            session.add(current_otp)
            session.commit()
            session.refresh(current_otp)

            raise InvalidOTP()
        

        #Update the OTP status to Verified
        current_otp.isVerified = True
        session.add(current_otp)
        session.commit()
        session.refresh(current_otp)

        # Create a new reset password session
        new_reset_password_session = ResetPasswordSession(
            userId = current_otp.userId,
            token = secrets.token_hex(32),
            isReset = False,
        )

        # create a new reset password session
        session.add(new_reset_password_session)
        session.commit()
        session.refresh(new_reset_password_session)

        return {
            "status": "success",
            "message": "OTP verified successfully",
            "token": new_reset_password_session.token,
        }
    

    async def resetPassword(self, response: Response, resetPasswordModel: ResetPasswordModel, session: Session):

        current_session = session.exec(
            select(ResetPasswordSession).where(ResetPasswordSession.token == resetPasswordModel.token)
        ).first()

        current_session_user = session.exec(
            select(User).where(User.id == current_session.userId)
        ).first()

        if(current_session is None):
            raise InvalidToken()
        
        if(current_session.isReset):
            raise InvalidToken()
        
        if utc_now() > current_session.expireAt.replace(tzinfo=timezone.utc):
            raise TokenExpired()
        
        #Update the ResetPassword status to Used
        current_session.isReset =True
        session.add(current_session)
        session.commit()
        session.refresh(current_session)

        # Update the user's password
        current_session_user.password = bcrypt.hashpw(resetPasswordModel.password.encode("utf-8"), self.HASH_SALT).decode("utf-8")
        session.add(current_session)
        session.commit()
        session.refresh(current_session)

        return {
            "status": "success",
            "message": "Password reset successfully",
        }
    
    @staticmethod
    def get_current_user_token(token: str = Cookie(None, alias="session")) -> TokenPayload:

        if not token:
            raise Unauthorized()

        token_data = decodeJwt(token)

        if token_data is None:
            raise Unauthorized()
            
        if token_data.expired < int(utc_now().timestamp()):
            raise Unauthorized()

        if token_data.user_id is None:
            raise Unauthorized()

        return token_data
            
AuthService = AuthService()