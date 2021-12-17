from typing import get_args
from .base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.models import Category
from fastapi import Depends

class CategorieRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, Category)