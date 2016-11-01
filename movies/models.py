from imdbpie import Imdb

from django.db import models


class Genre(models.Model):

    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class MovieManager(models.Manager):

    def create_from_url(self, url):

        # check if the movie is already on the DB
        try:
            movie = Movie.objects.get(imdb=url)
            movie.watched = None
            movie.save()
            return movie
        except Movie.DoesNotExist:
            pass

        imdb_list = url.split('/')
        if imdb_list[-1]:
            imdb_id = url.split('/')[-1]
        else:
            imdb_id = url.split('/')[-2]

        imdb = Imdb(anonymize=True)

        imdb_movie = imdb.get_title_by_id(imdb_id)

        # creating movie instance
        movie = Movie.objects.create(
            imdb=url,
            name=imdb_movie.title,
            poster=imdb_movie.poster_url,
        )

        # creating needed Genre instances
        for genre in imdb_movie.genres:
            genre_instance, _ = Genre.objects.get_or_create(name=genre)
            MovieGenre.objects.create(movie=movie, genre=genre_instance)

        return movie


class Movie(models.Model):

    imdb = models.URLField()
    name = models.CharField(max_length=64)
    poster = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    watched = models.DateTimeField(null=True)

    objects = MovieManager()

    def __unicode__(self):
        return self.name


class MovieGenre(models.Model):

    movie = models.ForeignKey(Movie, related_name='genres')
    genre = models.ForeignKey(Genre, related_name='movies')

    def __unicode__(self):
        return "{} {}".format(self.movie.name, self.genre.name)
