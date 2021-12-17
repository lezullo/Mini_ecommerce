from pydantic import BaseModel
from enum import Enum
from sqlalchemy.sql.functions import mode, percent_rank
from app.api.product.schemas import ProductSchema
from app.api.payment_methods.schemas import PaymentMethodSchema

class DiscountMode(str, Enum):
    Value = 'value'
    Percentage = 'percentage'
    
class ProductDiscountSchema(BaseModel):
    product_id: int
    mode: DiscountMode
    value: float
    payment_method_id: int

class ShowProductDiscountSchema(ProductDiscountSchema):
    id: int
    product: ProductSchema
    payment_methods: PaymentMethodSchema    
    
    class Config:
        orm_mode = True