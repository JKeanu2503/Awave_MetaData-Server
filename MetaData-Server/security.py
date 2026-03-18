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