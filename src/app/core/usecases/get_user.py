from app.adapters.user_repository import UserRepository

def get_user_by_id(user_id: str):
    repo = UserRepository()
    return repo.find_by_id(user_id)
