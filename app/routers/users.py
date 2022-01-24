from fastapi import APIRouter

from schema import UserResponse

router = APIRouter(
    prefix="/user"
)

@router.get("/", response_model=UserResponse)
async def get_users():
    users = UserResponse(
        data= [{
            "id": 1,
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "password": "password"
        }],
        message= "User Fetched Successfully"
    )
    return users