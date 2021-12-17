from typing import List
from app.api.product_discount.schemas import ProductDiscountSchema, ShowProductDiscountSchema
from app.db.db import get_db
from app.models.models import ProductDiscount, PaymentMethods, Product
from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import query

from .schemas import ProductDiscountSchema

router = APIRouter()

@router.get('/', response_model=List[ShowProductDiscountSchema])
def index(db: Session = Depends(get_db)):
    return db.query(ProductDiscount).all()

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(product_discount: ProductDiscountSchema, db: Session = Depends(get_db)):
    db.add(ProductDiscount(**product_discount.dict()))
    db.commit()

@router.get('/{id}', response_model=ShowProductDiscountSchema)
def show(id: int, db: Session = Depends(get_db)):
    return db.query(ProductDiscount).filter_by(id = id).first()

@router.put('/{id}')
def update(id: int, product_discount: ProductDiscountSchema, db: Session = Depends(get_db)):
    query = db.query(ProductDiscount).filter_by(id=id)
    query.update(product_discount.dict())
    db.commit()

def validate_discount(discount: ProductDiscountSchema, db: Session):
    payment_method_query = db.query(PaymentMethods).filter_by(id=discount.payment_method_id).first()
    if db.query(ProductDiscount).filter_by(product_id=discount.product_id, payment_method_id=discount.payment_method_id).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Payment method for this product is already discounted')  
    elif not db.query(Product).filter_by(id=discount.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')    
    elif not payment_method_query or payment_method_query.enabled == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')  
    elif discount.value == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')