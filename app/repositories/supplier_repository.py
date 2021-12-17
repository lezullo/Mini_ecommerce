from app.api.repositories.base_repository import BaseRepository
from app.db.db import get_db
from app.models.models import Supplier
from fastapi import Depends
from sqlalchemy.orm import Session

class SupplierRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, Supplier)