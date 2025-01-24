from fastapi import APIRouter

from app.auth.models.auth_dto import AuthDto

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/",)
async def login(authDto: AuthDto):
    return authDto


@router.get("/",)
async def loginTemp():
    return {"TEST": "GET COMPLETE AUTH"}