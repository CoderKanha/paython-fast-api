from fastapi import APIRouter

router = APIRouter(
    prefix="/user"
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]