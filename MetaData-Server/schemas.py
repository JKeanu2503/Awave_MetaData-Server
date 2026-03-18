from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Was der User bei der Registrierung schickt
class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Prüft automatisch, ob es eine echte E-Mail-Adresse ist
    password: str
    date_of_birth: date

# Was der Server dem Client zurückgibt (Sicherheit: Kein Passwort!)
class UserResponse(BaseModel):
    account_id: int
    username: str
    email: str
    date_of_birth: date
    is_active: bool

    class Config:
        from_attributes = True