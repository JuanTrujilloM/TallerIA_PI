import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Muestra los embeddings de una película seleccionada al azar"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        if not movies:
            self.stderr.write("No hay películas en la base de datos.")
            return
        movie = random.choice(movies)
        self.stdout.write(self.style.SUCCESS(f"Película seleccionada: {movie.title}"))
        # Supongamos que el campo embeddings está en el modelo Movie
        if hasattr(movie, 'emb'):
            self.stdout.write(f"Embeddings: {movie.emb}")
        else:
            self.stderr.write("La película no tiene embeddings almacenados.")
