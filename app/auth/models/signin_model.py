from pydantic import BaseModel

class SignInModel(BaseModel):

    email: str
    
    password: str