from os import stat
from typing import List
from app.models.models import User
from app.services.auth_service import only_admin
from app.repositories.user_repository import UserRepository
from app.services.user_service import UsersService
from app.api.admin.schemas import AdminSchema, ShowAdminSchema
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

router = APIRouter(dependencies=[Depends(only_admin)])

@router.get('/', response_model=List[ShowAdminSchema])
def index(repository: UserRepository = Depends()):
    return repository.get_all_admins()
    
@router.get('/{id}', response_model=ShowAdminSchema)
def show(id: int, repository: UserRepository = Depends()):
    return repository.get_admin_by_id(id)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(admin_schema: AdminSchema ,service: UsersService = Depends()):
    service.create(admin_schema)

@router.put('/{id}')
def update(id: int,admin_schema: AdminSchema, service: UsersService = Depends()):
    service.update(id, admin_schema)

@router.delete('/{id}')
def delete(id: int, repository: UserRepository = Depends()):
    repository.delete_admin(id)