from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text, Boolean, UniqueConstraint, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional

from database import Base

# ===== Assoziationstabelle ohne Attributen =====

# Relationstabelle des ERM Nr. 3
publisher_movie_link = Table(
    "publisher_movie_link",
    Base.metadata,
    Column("publisher_id", ForeignKey("publisher.publisher_id"), primary_key=True),
    Column("movie_id", ForeignKey("movie.movie_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 5
movie_tag_link = Table(
    "movie_tag_link",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.movie_id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.tag_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 10
publisher_series_link = Table (
    "publisher_series_link",
    Base.metadata,
    Column("publisher_id", ForeignKey("publisher.publisher_id"), primary_key=True),
    Column("series_id", ForeignKey("series.series_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 12
series_tag_link = Table(
    "series_tag_link",
    Base.metadata,
    Column("series_id", ForeignKey("series.series_id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.tag_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 13
series_language_link = Table(
    "series_language_link",
    Base.metadata,
    Column("series_id", ForeignKey("series.series_id"), primary_key=True),
    Column("language_id", ForeignKey("language.language_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 14
media_language_link = Table(
    "media_language_link",
    Base.metadata,
    Column("media_id", ForeignKey("media.media_id"), primary_key=True),
    Column("language_id", ForeignKey("language.language_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 17
media_playlist_link = Table(
    "media_playlist_link",
    Base.metadata,
    Column("media_id", ForeignKey("media.media_id"), primary_key=True),
    Column("playlist_id", ForeignKey("playlist.playlist_id"), primary_key=True)
)

# Relationstabelle des ERM Nr. 21
account_category_link = Table(
    "account_category_link",
    Base.metadata,
    Column("account_id", ForeignKey("account.account_id"), primary_key=True),
    Column("category_id", ForeignKey("category.category_id"), primary_key=True)
)

# ===== Assoziationstabelle mit Attributen =====

# Relationstabelle des ERM Nr. 4
class MovieActorPlayedAs(Base):
    __tablename__ = "movie_actor_played_as_link"
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.movie_id"), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actor.actor_id"), primary_key=True)

    played_as: Mapped[str] = mapped_column(String)
    is_only_voice: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    movie: Mapped["Movie"] = relationship(back_populates="movie_played_by_association")
    actor: Mapped["Actor"] = relationship(back_populates="movie_played_in_association")


# Relationstabelle des ERM Nr. 11
class SeriesActorPlayedAs(Base):
    __tablename__ = "series_actor_played_as_link"
    series_id: Mapped[int] = mapped_column(ForeignKey("series.series_id"), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actor.actor_id"), primary_key=True)

    played_as: Mapped[str] = mapped_column(String)
    is_only_voice: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    series: Mapped["Series"] = relationship(back_populates="series_played_by_association")
    actor: Mapped["Actor"] = relationship(back_populates="series_played_in_association")


# Relationstabelle des ERM Nr. 20
class AccountMediaHasSeen(Base):
    __tablename__ = "account_media_has_seen_link"
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.media_id"), primary_key=True)

    progress_in_seconds: Mapped[int] = mapped_column(Integer)

    account: Mapped["Account"] = relationship(back_populates="media_has_seen_association")
    media: Mapped["Media"] = relationship(back_populates="media_has_seen_by_association")


# ===== Basis-Klassen Definitionen =====

class Media(Base):
    __tablename__ = "media"
    media_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    title_alternative: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    release_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)
    duration_in_seconds: Mapped[int] = mapped_column(Integer)
    age_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    upload_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    media_url: Mapped[str] = mapped_column(String)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timestamp_intro_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timestamp_intro_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timestamp_outro_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timestamp_outro_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    type: Mapped[str] = mapped_column(String)

    # Relationstabelle des ERM Nr. 1/2
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "video"
    }

    # Relationstabelle des ERM Nr. 14
    languages: Mapped[List["Language"]] = relationship(
        secondary=media_language_link,
        back_populates="media"
    )

    # Relationstabelle des ERM Nr. 17
    playlists: Mapped[List["Playlist"]] = relationship(
        secondary=media_playlist_link,
        back_populates="media"
    )

    # Relationstabelle des ERM Nr. 20
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    media_has_seen_by_association: Mapped[List["AccountMediaHasSeen"]] = relationship(
        back_populates="media"
    )
    media_was_seen_by_accounts: Mapped[List["Account"]] = relationship(
        secondary=AccountMediaHasSeen.__table__,
        back_populates="account_has_seen_media"
    )


class Movie(Media):
    __tablename__ = "movie"
    movie_id: Mapped[int] = mapped_column(ForeignKey("media.media_id"), primary_key=True)

    # Relationstabelle des ERM Nr. 2
    __mapper_args__ = {
        "polymorphic_identity": "movie",
        "inherit_condition": (movie_id == Media.media_id)
    }

    # Relationstabelle des ERM Nr. 6
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    category: Mapped["Category"] = relationship(back_populates="movies")

    # Relationstabelle des ERM Nr. 7
    collection_id: Mapped[Optional[int]] = mapped_column(ForeignKey("collection.collection_id"), nullable=True)
    collection: Mapped[Optional["Collection"]] = relationship(back_populates="movies")

    # Relationstabelle des ERM Nr. 3
    publishers: Mapped[List["Publisher"]] = relationship(
        secondary=publisher_movie_link,
        back_populates="movies"
    )

    # Relationstabelle des ERM Nr. 5
    tags: Mapped[List["Tag"]] = relationship(
        secondary=movie_tag_link,
        back_populates="movies"
    )

    # Relationstabelle des ERM Nr. 4
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    movie_played_by_association: Mapped[List["MovieActorPlayedAs"]] = relationship(
        back_populates="movie"
    )
    played_by_actor_in_movie: Mapped[List["Actor"]] = relationship(
        secondary=MovieActorPlayedAs.__table__,
        back_populates="played_in_movies"
    )


class Episode(Media):
    __tablename__ = "episode"
    episode_id: Mapped[int] = mapped_column(ForeignKey("media.media_id"), primary_key=True)
    episode_number: Mapped[int] = mapped_column(Integer)

    # Relationstabelle des ERM Nr. 1
    __mapper_args__ = {
        "polymorphic_identity": "episode",
        "inherit_condition": (episode_id == Media.media_id)
    }

    # Relationstabelle des ERM Nr. 8
    # Fremdschlüssel zu Season
    season_id: Mapped[int] = mapped_column(Integer, ForeignKey("season.season_id"))
    # 1:N von Episode zu Season
    season: Mapped["Season"] = relationship(back_populates="episodes")


class Season(Base):
    __tablename__ = "season"
    season_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    season_number: Mapped[int] = mapped_column(Integer)
    cover_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    release_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)


    # Relationstabelle des ERM Nr. 9
    series_id: Mapped[int] = mapped_column(ForeignKey("series.series_id"))
    series: Mapped["Series"] = relationship(back_populates="seasons")

    # Relationstabelle des ERM Nr. 8
    episodes: Mapped[List["Episode"]] = relationship(back_populates="season")

    __table_args__ = (UniqueConstraint('series_id', 'season_number', name='_series_season_uc'),)


class Series(Base):
    __tablename__ = "series"
    series_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    title_alternative: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    cover_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    release_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)

    # Relationstabelle des ERM Nr. 9
    # 1:N von Series zu Season (N-Seite)
    seasons: Mapped[List["Season"]] = relationship(back_populates="series")

    # Relationstabelle des ERM Nr. 15
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    category: Mapped["Category"] = relationship(back_populates="series")

    # Relationstabelle des ERM Nr. 10
    publishers: Mapped[List["Publisher"]] = relationship(
        secondary=publisher_series_link,
        back_populates="series"
    )

    # Relationstabelle des ERM Nr. 12
    tags: Mapped[List["Tag"]] = relationship(
        secondary=series_tag_link,
        back_populates="series"
    )

    # Relationstabelle des ERM Nr. 13
    languages: Mapped[List["Language"]] = relationship(
        secondary=series_language_link,
        back_populates="series"
    )

    # Relationstabelle des ERM Nr. 11
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    series_played_by_association: Mapped[List["SeriesActorPlayedAs"]] = relationship(
        back_populates="series"
    )
    played_by_actor_in_series: Mapped[List["Actor"]] = relationship(
        secondary=SeriesActorPlayedAs.__table__,
        back_populates="played_in_series"
    )


class Category(Base):
    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    icon_type: Mapped[int] = mapped_column(Integer)

    # Relationstabelle des ERM Nr. 6
    movies: Mapped[List["Movie"]] = relationship(back_populates="category")

    # Relationstabelle des ERM Nr. 15
    series: Mapped[List["Series"]] = relationship(back_populates="category")

    # Relationstabelle des ERM Nr. 16
    collections: Mapped[List["Collection"]] = relationship(back_populates="category")

    # Relationstabelle des ERM Nr. 21
    accounts: Mapped[List["Account"]] = relationship(
        secondary=account_category_link,
        back_populates="categories"
    )


class Collection(Base):
    __tablename__ = "collection"
    collection_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    cover_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationstabelle des ERM Nr. 7
    movies: Mapped[List["Movie"]] = relationship(back_populates="collection")

    # Relationstabelle des ERM Nr. 16
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    category: Mapped["Category"] = relationship(back_populates="collections")


class Publisher(Base):
    __tablename__ = "publisher"
    publisher_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)

    # Relationstabelle des ERM Nr. 3
    movies: Mapped[List["Movie"]] = relationship(
        secondary=publisher_movie_link,
        back_populates="publishers"
    )

    # Relationstabelle des ERM Nr. 10
    series: Mapped[List["Series"]] = relationship(
        secondary=publisher_series_link,
        back_populates="publishers"
    )


class Actor(Base):
    __tablename__ = "actor"
    actor_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    pic_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationstabelle des ERM Nr. 4
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    movie_played_in_association: Mapped[List["MovieActorPlayedAs"]] = relationship(
        back_populates="actor"
    )
    played_in_movies: Mapped[List["Movie"]] = relationship(
        secondary=MovieActorPlayedAs.__table__,
        back_populates="played_by_actor_in_movie"
    )

    # Relationstabelle des ERM Nr. 11
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    series_played_in_association: Mapped[List["SeriesActorPlayedAs"]] = relationship(
        back_populates="actor"
    )
    played_in_series: Mapped[List["Series"]] = relationship(
        secondary=SeriesActorPlayedAs.__table__,
        back_populates="played_by_actor_in_series"
    )


class Tag(Base):
    __tablename__ = "tag"
    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tag_category: Mapped[str] = mapped_column(String, index=True)
    tag_attribute: Mapped[str] = mapped_column(String, index=True)

    # Relationstabelle des ERM Nr. 5
    movies: Mapped[List["Movie"]] = relationship(
        secondary=movie_tag_link,
        back_populates="tags"
    )

    # Relationstabelle des ERM Nr. 12
    series: Mapped[List["Series"]] = relationship(
        secondary=series_tag_link,
        back_populates="tags"
    )


class Language(Base):
    __tablename__ = "language"
    language_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language_def: Mapped[str] = mapped_column(String)
    track_type_subtitle: Mapped[bool] = mapped_column(Boolean)

    # Relationstabelle des ERM Nr. 13
    series: Mapped[List["Series"]] = relationship(
        secondary=series_language_link,
        back_populates="languages"
    )

    # Relationstabelle des ERM Nr. 14
    media: Mapped[List["Media"]] = relationship(
        secondary=media_language_link,
        back_populates="languages"
    )


class Account(Base):
    __tablename__ = "account"
    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    hashed_pw: Mapped[str] = mapped_column(String)
    profilpicture_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationstabelle des ERM Nr. 19
    settings: Mapped["Settings"] = relationship(back_populates="account")

    # Relationstabelle des ERM Nr. 18
    playlists: Mapped[List["Playlist"]] = relationship(back_populates="account")

    # Relationstabelle des ERM Nr. 21
    categories: Mapped[List["Category"]] = relationship(
        secondary=account_category_link,
        back_populates="accounts"
    )

    # Relationstabelle des ERM Nr. 20
    # + direkte, vereinfachte Variante über Assoziation hinweg an eigentliche Entitäten zu kommen
    media_has_seen_association: Mapped[List["AccountMediaHasSeen"]] = relationship(
        back_populates="account"
    )
    account_has_seen_media: Mapped[List["Media"]] = relationship(
        secondary=AccountMediaHasSeen.__table__,
        back_populates="media_was_seen_by_accounts"
    )


class Settings(Base):
    __tablename__ = "settings"
    settings_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    auto_select_language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    audio_language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subtitle_language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    seen_media_progress_value: Mapped[int] = mapped_column(Integer)

    # Relationstabelle des ERM Nr. 19
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), unique=True)
    account: Mapped["Account"] = relationship(back_populates="settings")


class Playlist(Base):
    __tablename__ = "playlist"
    playlist_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)

    is_dynamic: Mapped[bool] = mapped_column(Boolean, default=False)

    filter_tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tag.tag_id"), nullable=True)
    filter_language_id: Mapped[Optional[int]] = mapped_column(ForeignKey("language.language_id"), nullable=True)
    filter_actor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("actor.actor_id"), nullable=True)
    filter_publisher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("publisher.publisher_id"), nullable=True)

    # Relationstabelle des ERM Nr. 18
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"))
    account: Mapped["Account"] = relationship(back_populates="playlists")

    # Relationstabelle des ERM Nr. 17
    media: Mapped[List["Media"]] = relationship(
        secondary=media_playlist_link,
        back_populates="playlists"
    )