from fastapi import FastAPI

from app.db import create_tables, engine
from app.router.auth import app as auth_router

create_tables(engine)

app = FastAPI(title="Simple JWT Auth API")
app.include_router(auth_router, prefix="", tags=["auth"])
