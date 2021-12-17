from pydantic import BaseModel
from datetime import date, datetime

class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    genre: str
    birth_date: date
    phone: str
    document_id: int     
    
class ShowCustomerSchema(CustomerSchema):
    id: int

    class Config:
        orm_mode = True
