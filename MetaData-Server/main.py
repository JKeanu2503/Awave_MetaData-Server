from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, security
from database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm

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

@app.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. User suchen
    user = db.query(models.Account).filter(models.Account.username == form_data.username).first()

    # 2. Existiert der User und stimmt das Passwort?
    if not user or not security.pwd_context.verify(form_data.password, user.hashed_pw):
        raise HTTPException(status_code=401, detail="Falscher Username oder Passwort")

    # 3. Token erstellen
    access_token = security.create_access_token(data={"sub": user.username, "id": user.account_id})

    return {"access_token": access_token, "token_type": "bearer"}