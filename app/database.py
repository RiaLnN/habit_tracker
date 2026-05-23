from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

sessionLocal = sessionmaker(
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_session():
    with sessionLocal() as session:
        yield session