from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.auth import auth_router


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://paperless-tranform-frontend.vercel.app",
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