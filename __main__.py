from app.api.router import router
from app.models.models import Base
from app.db.db import engine
from fastapi_pagination import add_pagination
from fastapi import FastAPI

app = FastAPI()
add_pagination(app)
app.include_router(router)