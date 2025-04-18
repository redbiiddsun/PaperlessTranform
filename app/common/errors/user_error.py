from app.common.errors.base_http_exception import BaseHTTPException
from fastapi import  status


class UserNotFound(BaseHTTPException):
    def __init__(self, user_id: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         status="error",
                         detail=f"User with id {user_id} not found",
                         error_code="ERR_USER_NOT_FOUND")
        
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         status="error",
                         detail=f"User not found",
                         error_code="ERR_USER_NOT_FOUND")
        
class InvalidEmailPassword(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         status="error",
                         detail=f"Invalid email or password",
                         error_code="ERR_INVALID_CRED")
        
class ExistingEmail(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         status="error",
                         detail=f"Email already exists",
                         error_code="ERR_EMAIL_EXISTS")
        
class InvalidEmailFormat(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail=f"Invalid email format",
                         error_code="ERR_EMAIL_FORMAT")
        
class InvalidOTP(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail=f"Invalid OTP",
                         error_code="ERR_INVALID_OTP")
        
class ExpiredOTP(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail=f"Expired OTP",
                         error_code="ERR_EXPIRED_OTP")
        
class MaximumAttempOTP(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail="OTP exceeded maximum attempts",
                         error_code="ERR_MAX_ATTEMPT_OTP")
        
class OTPAlreadyVerified(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail="OTP already verified",
                         error_code="ERR_OTP_USED")
        
class InvalidToken(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail="Invalid token",
                         error_code="ERR_INVALID_TOKEN")
        
class TokenExpired(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         status="error",
                         detail="Token expired",
                         error_code="ERR_TOKEN_EXPIRED")


                         