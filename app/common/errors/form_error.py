from app.common.errors.base_http_exception import BaseHTTPException
from fastapi import status

class FormNotFound(BaseHTTPException):
    def __init__(self, detail: str = "Form not found"):
        super().__init__(status_code = status.HTTP_404_NOT_FOUND,
                         status = "error",
                         detail = detail,
                         error_code = "ERR_FORM_NOT_FOUND")