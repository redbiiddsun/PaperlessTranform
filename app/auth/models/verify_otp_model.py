from pydantic import BaseModel

class VerifyOtpModel(BaseModel):

    token: str

    otp: str