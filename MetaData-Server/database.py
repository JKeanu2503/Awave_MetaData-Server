from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Die URL kennst du schon - echo=True hilft dir beim Lernen (SQL-Log)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Dasselt12@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Diese Funktion gibt uns eine saubere Verbindung für jeden Request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()