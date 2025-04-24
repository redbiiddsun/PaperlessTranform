
from fastapi import Response
from sqlmodel import Session, select

from app.common.errors.user_error import  ExistingEmail, UserNotFound
from app.common.jwt import TokenPayload
from app.schemas import User
from app.users.models.update_user_model import UpdateUserModel
from app.users.models.user_response import UserResponse


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
    
    async def update_user(self, response: Response, userUpdateModel: UpdateUserModel, current_user: TokenPayload, session: Session):

        user = session.exec(
            select(User).where(User.id == current_user.user_id)
        ).first()

        if user is None:
            raise UserNotFound()


        if userUpdateModel.firstname is not None:
            user.firstname = userUpdateModel.firstname

        if userUpdateModel.lastname is not None:
            user.lastname = userUpdateModel.lastname

        if userUpdateModel.email is not None:

            exiting_email = session.exec(
            select(User).where(User.email == userUpdateModel.email)).first()

            if(exiting_email):
                raise ExistingEmail()

            user.email = userUpdateModel.email

        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "first_name": user.firstname,
                "last_name": user.lastname,
                "email": user.email
            }
        }

UserService = UserService()