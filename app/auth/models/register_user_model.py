from pydantic import BaseModel

class RegisterUserModel(BaseModel):

    firstname: str

    lastname: str

    email: str

    password: str
