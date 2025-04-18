class BaseHTTPException(Exception):
    def __init__(self, status_code: int, status: str, detail: str, error_code: str) -> None:
        self.status_code = status_code
        self.status = status
        self.detail = detail
        self.error_code = error_code