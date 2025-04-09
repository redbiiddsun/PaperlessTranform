from pydantic import BaseModel

class ResetPasswordModel(BaseModel):

    token: str

    password: str
