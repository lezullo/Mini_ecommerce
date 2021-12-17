from fastapi import Depends
from app.db.db import Session, get_db
from app.api.repositories.base_repository import BaseRepository
from app.models.models import PaymentMethods

class PaymentMethodRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, PaymentMethods)