from pydantic import BaseModel

class AdressSchema(BaseModel):
    address: str
    city: str
    state: str
    number: str
    zipcode: str
    neighbourhood: str
    primary: bool
    customer_id: int

class ShowAdressSchema(AdressSchema):
    id: int
    
    class Config:
        orm_mode = True
