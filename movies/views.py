from random import choice

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, DeleteView
from django.utils import timezone


from utils import build_response
from .models import Movie


class GetMovie(DetailView):
    model = Movie
    queryset = Movie.objects.filter(watched__isnull=True)
    template_name = "movie.html"

    def get_object(self):
        qs = self.get_queryset()
        if qs.exists():
            return choice(qs)
        self.template_name = "empty.html"
        return None


class AddMovie(CreateView):

    def get(self, request, *args, **kwargs):
        imdb_url = request.GET.get('imdb')
        if not imdb_url:
            return build_response(HttpResponse(status=400))

        imdb_url = imdb_url.split('?')[0]

        movie = Movie.objects.create_from_url(imdb_url)

        if movie:
            return build_response(HttpResponse(status=201))
        return build_response(HttpResponse(status=400))


class RemoveMovie(DeleteView):
    model = Movie
    queryset = Movie.objects.all()

    def get(self, request, *args, **kwargs):
        movie_id = request.GET.get('movieId')
        if not movie_id:
            return build_response(HttpResponse(status=400))

        movie = get_object_or_404(Movie, id=movie_id)
        movie.watched = timezone.now()
        movie.save()

        return build_response(HttpResponse(status=200))
