from fastapi import APIRouter
from app.core.usecases.get_user import get_user_by_id

user_router = APIRouter()

@user_router.get("/{user_id}")
def get_user(user_id: str):
    return get_user_by_id(user_id)
