from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.common.errors.base_http_exception import BaseHTTPException
from app.database import create_db_and_tables
from app.auth import auth_router
from app.users import user_router
from app.form import form_router



app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://paperless-tranform-frontend.vercel.app",
    "https://www.paperlesstransform.online",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(form_router)



@app.exception_handler(BaseHTTPException)
async def custom_exception_handler(request: Request, exc: BaseHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status, 
                 "detail": exc.detail, 
                 "error_code": exc.error_code},
    )

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
  return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                      content={"status": "error", 
                                "detail": "Internal server error",
                                "error_code": "ERR_INTERNAL_SERVER_ERROR"})

@app.get("/")
async def welcome():
    return "Welcome to the Data Type Analyzer API! Please use /docs for API documentation."

@app.get("/test-schema")
async def temporary_schema():
    return [
    {
        "$el": "h1",
        "children": "Register",
        "attrs": {
            "class": "text-2xl font-bold mb-4",
        },
    },
    {
        "$formkit": "text",
        "name": "email",
        "label": "Email",
        "help": "This will be used for your account.",
        "validation": "required|email",
    },
    {
        "$formkit": "password",
        "name": "password",
        "label": "Password",
        "help": "Enter your new password.",
        "validation": "required|length:5,16",
    },
    {
        "$formkit": "password",
        "name": "password_confirm",
        "label": "Confirm password",
        "help": "Enter your new password again to confirm it.",
        "validation": "required|confirm",
        "validationLabel": "password confirmation",
    },
    {
        "$cmp": "FormKit",
        "props": {
            "name": "eu_citizen",
            "type": "checkbox",
            "id": "eu",
            "label": "Are you a european citizen?",
        },
    },
    {
        "$formkit": "select",
        "if": "$get(eu).value",
        "name": "cookie_notice",
        "label": "Cookie notice frequency",
        "options": {
            "refresh": "Every page load",
            "hourly": "Ever hour",
            "daily": "Every day",
        },
        "help": "How often should we display a cookie notice?",
    },
]

@app.get("/health")
async def health_status():
    return {"status": "OK"}