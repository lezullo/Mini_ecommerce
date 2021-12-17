from os import name
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.db.db import get_db
from sqlalchemy.orm import Session
from app.models.models import *

router = APIRouter()


@router.get('/seed')
def index(db: Session = Depends(get_db)):
    db.add(Category(name='Celular'))
    db.add(Supplier(name='Xiomi'))
    db.add(Product(description='Redmi note 2', price=1400, image='',
           visible=True, technical_details="2", category_id=1, supplier_id=1))

    db.commit()
