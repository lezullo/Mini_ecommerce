from typing import List
from app.db.db import get_db
from app.models.models import Customer
from app.api.customers.schemas import CustomerSchema, ShowCustomerSchema
from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get('/', response_model=List[ShowCustomerSchema])
def index(db: Session = Depends(get_db)):
    return db.query(Customer).all()
    
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(custumer: CustomerSchema, db: Session = Depends(get_db)): 
    db.add(Customer(**custumer.dict())) 
    db.commit()

@router.put('/{id}')
def update(id: int, custumer: CustomerSchema, db: Session = Depends(get_db)):
    query = db.query(Customer).filter_by(id=id) 
    query.update(custumer.dict())
    db.commit()

@router.get('/{id}', response_model=ShowCustomerSchema)
def show(id: int, db: Session = Depends(get_db)):
    return db.query(Customer).filter_by(id=id).first()