import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Genre as GenreModel, Movie as MovieModel, db, Genre, Movie


class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

    movies = graphene.List(lambda: MovieType)

    def resolve_movies(self, info):
        return self.movies.all()

class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        exclude_fields = ("genres",)

    genres = graphene.List(GenreType)

    def resolve_genres(self, info):
        return self.genres

class Query(graphene.ObjectType):
    genres = graphene.List(GenreType)
    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, movie_id=graphene.ID(required=True))
    genre = graphene.Field(GenreType, genre_id=graphene.ID(required=True))
    movies_by_genre = graphene.List(MovieType, genre_id=graphene.Int(required=True))
    genre_by_movie = graphene.Field(GenreType, movie_id=graphene.Int(required=True))

    def resolve_genres(self, info):
        return db.session.query(GenreModel).all()

    def resolve_movies(self, info):
        return db.session.query(MovieModel).all()
    
    def resolve_movie(self, info, movie_id):
        movie = db.session.get(MovieModel, movie_id)
        return movie
    
    def resolve_genre(self, info, genre_id):
        genre = db.session.get(GenreModel, genre_id)
        return genre

    def resolve_movies_by_genre(self, info, genre_id):
        genre = db.session.get(GenreModel, genre_id) 
        if not genre:
            raise ValueError(f"Genre with id {genre_id} does not exist.")
        return genre.movies

    def resolve_genre_by_movie(self, info, movie_id):
        movie = db.session.get(MovieModel, movie_id)
        if not movie:
            raise ValueError(f"Movie with id {movie_id} does not exist.")
        return movie.genre

class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, name):
        if not name or len(name) > 50:
            raise ValueError("Genre name must not be empty and should be less than 50 characters.")

        genre = GenreModel(name=name)
        db.session.add(genre)
        db.session.commit()
        return CreateGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, id, name):
        genre = db.session.get(GenreModel, id)
        if not genre:
            raise ValueError(f"Genre with id {id} does not exist.")
        if not name or len(name) > 50:
            raise ValueError("Genre name must not be empty and should be less than 50 characters.")

        genre.name = name
        db.session.commit()
        return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        genre = db.session.get(GenreModel, id)
        if not genre:
            raise ValueError(f"Genre with id {id} does not exist.")

        db.session.delete(genre)
        db.session.commit()
        return DeleteGenre(success=True)

class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

