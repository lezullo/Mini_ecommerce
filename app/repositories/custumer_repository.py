from fastapi import Depends
from app.api.repositories.base_repository import BaseRepository
from app.db.db import Session, get_db
from app.models.models import Customer

class CustomerRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Customer)