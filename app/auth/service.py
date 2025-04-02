import bcrypt
from fastapi import Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.auth.models.register_user_model import RegisterUserModel
from app.common.regex import EMAIL_REGEX
from app.database import get_session
from app.schemas import User

class AuthService:
    def __init__(self):
        pass

    async def register_user(self, registerUserModel: RegisterUserModel, session: Session):

        new_user = User(
            email= registerUserModel.email,
            password= bcrypt.hashpw(registerUserModel.password.encode("utf-8"), bcrypt.gensalt()),
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

AuthService = AuthService()
