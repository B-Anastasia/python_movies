import graphene
from graphene_django.types import DjangoObjectType
from .models import Movie, Director


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New movie"


class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())
    all_directors = graphene.List(DirectorType)

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            try:
                return Movie.objects.get(pk=id)
            except Movie.DoesNotExist:
                return None

        if title is not None:
            try:
                return Movie.objects.get(title=title)
            except Movie.DoesNotExist:
                return None

        return None;
        # return Movie.objects.all()

    def resolve_all_directors(self, info):
        return Director.objects.all()


class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)

        return MovieCreateMutation(movie=movie)


class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()
        director_id = graphene.Int()
        director_name = graphene.String()
        director_surname = graphene.String()

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title=None, year=None, director_id=None, director_name=None, director_surname=None ):
        movie = Movie.objects.get(pk=id)

        if title is not None:
            movie.title = title

        if year is not None:
            movie.year = year

        if director_id is not None:
            director = Director.objects.get(pk=director_id)
            movie.director = director

        if director_name is not None and director_surname is not None:
            director = Director.objects.create(name=director_name, surname=director_surname)
            movie.director = director

        movie.save()

        return MovieCreateMutation(movie=movie)


class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)
    success = graphene.Boolean()

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()

        return MovieCreateMutation(movie=None, success=True)


class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()


# {
#   first_movie: movie(id: 1){
#     ...movieData
#   }
#   second_movie: movie(id: 2){
#     ...movieData
#   }
# }
#
# fragment movieData on MovieType {
#   title
#   id
#   director{
#     name
#   }
# }

# query MoviesAndDirectors {
#   allMovies {
#     title
#     year
#     director {
#       name
#     }
#   }
# }
#
# query Movies {
#   allMovies {
#     title
#     year
#   }
# }

# query MoviesAndDirectors($id: Int) {
#   movie(id: $id) {
#     title
#     year
#     director {
#       name
#     }
#   }
# }
# {
#   "id": 1
# }

# query MoviesAndDirectors($id: Int, $showDirectors: Boolean = false) {
#   movie(id: $id) {
#     title
#     year
#     id
#     director @include(if: $showDirectors) {
#       name
#     }
#   }
# }
# query MoviesAndDirectors($id: Int, $showDirectors: Boolean = false) {
#   movie(id: $id) {
#     title
#     year
#     id
#     director @skip(if: $showDirectors) {
#       name
#     }
#   }
# }
#
# mutation CreateMovie {
#   createMovie(title: "Wonders of the Sea 3D",  year: 2017){
#     movie{
#       title
#     }
#   }
# }
#
# query GetMovies {
#   allMovies {
#     id
#     title
#     year
#   }
# }
#
# mutation UpdateMovie {
#   updateMovie(id: 5, title: "Wonders of the Sea 3D",  year: 2017){
#     movie{
#       title
#       year
#     }
#   }
# }

# from graphene_django import DjangoObjectType
# import graphene
# from .models import MyModel
#
# class MyModelType(DjangoObjectType):
#     class Meta:
#         model = MyModel
#
# class UpdateMyModel(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         arg1 = graphene.String()
#         arg2 = graphene.String()
#
#     success = graphene.Boolean()
#     my_model = graphene.Field(MyModelType)
#
#     def mutate(self, info, id, arg1=None, arg2=None):
#         try:
#             my_model = MyModel.objects.get(pk=id)
#         except MyModel.DoesNotExist:
#             return UpdateMyModel(success=False, my_model=None)
#
#         if arg1 is not None:
#             my_model.arg1 = arg1
#
#         if arg2 is not None:
#             my_model.arg2 = arg2
#
#         my_model.save()
#
#         return UpdateMyModel(success=True, my_model=my_model)
#
# class Mutation(graphene.ObjectType):
#     update_my_model = UpdateMyModel.Field()

