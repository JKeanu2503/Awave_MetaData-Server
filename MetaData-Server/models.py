from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_pw = Column(String, nullable=False)  # Niemals Klartext!
    profilpicture_url = Column(String)
    date_of_birth = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    # 1:1 Beziehung zu Settings
    settings = relationship("Settings", back_populates="account", uselist=False)


class Settings(Base):
    __tablename__ = "account_settings"

    settings_id = Column(Integer, primary_key=True, index=True)
    preferred_language = Column(String, default="de")
    audio_language = Column(String, default="de")
    subtitle_language = Column(String, default="de")
    seen_media_progress_value = Column(Integer, default=0)
    select_autoplay = Column(Boolean, default=True)

    # Fremdschlüssel zum Account
    account_id = Column(Integer, ForeignKey("accounts.id"), unique=True)
    account = relationship("Account", back_populates="settings")