from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str    
    password: str
    email: str
    role: str