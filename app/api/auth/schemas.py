from pydantic import BaseModel


class ShowUserSchema(BaseModel):
    name: str
    email: str
    id: int

    class Config:
        orm_mode = True