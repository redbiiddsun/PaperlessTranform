import bcrypt
from fastapi import Depends, HTTPException, Response, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.auth.models.signin_model import SignInModel
from app.auth.models.register_user_model import RegisterUserModel
from app.common.jwt import signJwt
from app.common.regex import EMAIL_REGEX
from app.database import get_session
from app.schemas import User

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
            print("User not found")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid email or password")
        
        if not bcrypt.checkpw(loginModel.password.encode("utf-8"), current_user.password.encode("utf-8")):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid email or password")
        
        response.set_cookie(key="session", value=signJwt(current_user.id))

        return {
            "status": "success",
            "message": "Signin successfully",
        }

AuthService = AuthService()
