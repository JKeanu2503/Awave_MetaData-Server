from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, security
from database import engine, get_db

app = FastAPI(title="DIESE DATEI BEARBEITE ICH GERADE")

# Tabellen erstellen (Lila Zone)
models.Base.metadata.create_all(bind=engine)


@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Prüfen, ob der User schon existiert
    db_user = db.query(models.Account).filter(models.Account.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    # 2. Passwort hashen (aus security.py)
    hashed_pw = security.get_password_hash(user.password)

    # 3. Neuen Account-Eintrag erstellen
    new_user = models.Account(
        username=user.username,
        email=user.email,
        hashed_pw=hashed_pw,
        date_of_birth=user.date_of_birth
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Holt die neue ID aus der DB

    return new_user