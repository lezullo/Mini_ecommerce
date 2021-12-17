from pydantic import BaseModel
from app.api.category.schemas import ShowCategorySchema
from app.api.supplier.schemas import ShowSupplierSchema

class ProductSchema(BaseModel):
    description: str
    price: float
    technical_details: str
    image: str
    visible: bool
    supplier_id: int
    category_id: int
    
class ShowProductSchema(ProductSchema):
    id: int
    category: ShowCategorySchema
    supplier: ShowSupplierSchema
    
    class Config:
        orm_mode = True