import bcrypt
from .schemas import UserSchema
from app.models.models import User
from app.repositories.user_repository import UserRepository
from fastapi import APIRouter
from fastapi.param_functions import Depends

router = APIRouter()

@router.post('/')
def create(user: UserSchema, repository: UserRepository = Depends()):
    user.password = bcrypt.hashpw(
        user.password.encode('utf8'), bcrypt.gensalt())
    repository.create(User(**user.dict()))
