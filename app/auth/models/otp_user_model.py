from pydantic import BaseModel

class RequestOtpModel(BaseModel):
    email: str
    