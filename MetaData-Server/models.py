from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Niemals Klartext!
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 1:1 Beziehung zu Settings
    settings = relationship("Settings", back_populates="account", uselist=False)


class Settings(Base):
    __tablename__ = "account_settings"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, default="de")
    dark_mode = Column(Boolean, default=True)

    # Fremdschlüssel zum Account
    account_id = Column(Integer, ForeignKey("accounts.id"), unique=True)
    account = relationship("Account", back_populates="settings")