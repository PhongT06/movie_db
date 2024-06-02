from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

movie_genre_association = db.Table(
    "movie_genre",
    Base.metadata,
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True),
)

class Movie(Base):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255))
    description: Mapped[str] = mapped_column(db.Text)
    release_year: Mapped[int] = mapped_column(db.Integer)
    genres = relationship("Genre", secondary=movie_genre_association, back_populates="movies")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))
    movies = relationship("Movie", secondary=movie_genre_association, back_populates="genres")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()