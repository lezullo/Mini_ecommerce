from fastapi import Depends
from app.db.db import Session, get_db
from app.api.repositories.base_repository import BaseRepository
from app.models.models import ProductDiscount



class ProductDiscountRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, ProductDiscount)
    
    def get_product_payment(self, product_id: int, payment_id: int):
        return self.session.query(self.model).filter(product_id = product_id, payment_id = payment_id).first()

    def delete(self, int:id):
        self.session.query(self.model).filter(id=id).delete()
        self.session.commit()
