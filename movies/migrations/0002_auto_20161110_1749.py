# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 17:49
from __future__ import unicode_literals

from imdbpie import Imdb

from django.db import migrations


def fill_movies(apps, schema_editor):

    Movie = apps.get_model('movies', 'Movie')
    Genre = apps.get_model('movies', 'Genre')
    MovieGenre = apps.get_model('movies', 'MovieGenre')

    def create_from_url(url):

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

    urls = [
        u'http://www.imdb.com/title/tt3183660/',
        u'http://www.imdb.com/title/tt3263904/',
        u'http://www.imdb.com/title/tt3631112/',
        u'http://www.imdb.com/title/tt1935859/',
        u'http://www.imdb.com/title/tt1211837/',
        u'http://www.imdb.com/title/tt0110912/',
        u'http://www.imdb.com/title/tt0102926/',
        u'http://www.imdb.com/title/tt0092099/',
    ]

    for url in urls:
        create_from_url(url)


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill_movies)
    ]
