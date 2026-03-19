import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

# Wir sagen passlib, dass wir den "bcrypt"-Algorithmus nutzen wollen.
# bcrypt ist der Goldstandard für Passwort-Hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Wandelt ein Klartext-Passwort in sicheres 'Hackfleisch' um."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Prüft beim Login, ob das getippte Passwort zum Salat in der DB passt."""
    return pwd_context.verify(plain_password, hashed_password)

# Das ist dein geheimer Schlüssel – in echt sollte der in einer .env Datei stehen!
SECRET_KEY = "DEIN_SUPER_GEHEIMER_SCHLÜSSEL_VON_AWAVE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12 # Token ist 12h gültig

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt