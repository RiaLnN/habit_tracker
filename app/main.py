from fastapi import FastAPI
from app.database import Base, engine
from app.routes import api
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def get_app():
    app = FastAPI(docs_url='/docs', lifespan=lifespan, debug=True)
    app.include_router(api.router)
    return app

app = get_app()