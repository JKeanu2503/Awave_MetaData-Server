from fastapi import FastAPI
from database import engine, Base
import models # Wichtig, damit SQLAlchemy die Modelle registriert

app = FastAPI()

# Das hier ist der "Zündschlüssel": 
# Er erstellt die Tabellen in Postgres, falls sie nicht existieren.
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"status": "MetadataServer läuft und DB ist verbunden"}