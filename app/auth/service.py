import bcrypt
from fastapi import Depends, HTTPException, Response, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.auth.models.otp_user_model import RequestOtpModel
from app.auth.models.signin_model import SignInModel
from app.auth.models.register_user_model import RegisterUserModel
from app.common.jwt import signJwt
from app.common.regex import EMAIL_REGEX
from app.common.util import generate_otp, generate_otp_reference
from app.common.email import email_sender
from app.database import get_session
from app.schemas import User
from app.schemas.otp import Otp

class AuthService:
    def __init__(self):
        pass

    async def register_user(self, registerUserModel: RegisterUserModel, session: Session):

        HASH_SALT = bcrypt.gensalt(10)

        new_user = User(
            email= registerUserModel.email,
            password= bcrypt.hashpw(registerUserModel.password.encode("utf-8"), HASH_SALT).decode("utf-8"),
            firstname= registerUserModel.firstname,
            lastname= registerUserModel.lastname,
        )

        if EMAIL_REGEX.match(registerUserModel.email) is None:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email format")

        # Check if the email already exists
        existing_email = session.exec(
            select(User).where(User.email == registerUserModel.email)
        ).first()

        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {
            "status": "success",
            "message": "User registered successfully",
        }
    

    async def signIn(self, response: Response, loginModel: SignInModel, session: Session):

        if EMAIL_REGEX.match(loginModel.email) is None:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email format")
        
        # Check if the email already exists
        current_user = session.exec(
            select(User).where(User.email == loginModel.email)
        ).first()

        if current_user is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid email or password")
        
        if not bcrypt.checkpw(loginModel.password.encode("utf-8"), current_user.password.encode("utf-8")):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid email or password")
        
        response.set_cookie(key="session", value=signJwt(current_user.id))

        return {
            "status": "success",
            "message": "Signin successfully",
        }
    
    async def requestOtp(self, response: Response, requestOtpModel: RequestOtpModel, session: Session):
        if EMAIL_REGEX.match(requestOtpModel.email) is None:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email format")
        
        # Check if the email already exists
        current_user = session.exec(
            select(User).where(User.email == requestOtpModel.email)
        ).first()

        if current_user is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found")
        
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
        email_sender.send_email('sunphanasorn@gmail.com', 
                                'Paperlesstranform - OTP to Reset Your Password', 
                                'Your OTP is: {} with ref code: {}'.format(new_otp.otp, new_otp.referenceCode), 
                                from_email='noreply@paperlesstranform.com')

        return {
            "status": "success",
            "message": "OTP sent successfully",
            "refCode": new_otp.referenceCode,
            "token": new_otp.id,
        }


AuthService = AuthService()
