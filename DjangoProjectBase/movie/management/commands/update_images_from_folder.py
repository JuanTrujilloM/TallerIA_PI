import os
import unicodedata
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Actualiza la ruta de la imagen de cada película desde la carpeta media/movie/images/"

    import unicodedata

    def normalize_title(self, title):
        # Elimina tildes y caracteres especiales, convierte a minúsculas y reemplaza espacios por guiones bajos
        title = title.strip()
        title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
        title = title.replace('?', '').replace(':', '').replace("'", '').replace('"', '')
        title = title.replace(' ', ' ')
        return title.lower()

    def handle(self, *args, **kwargs):
        images_folder = os.path.join('media', 'movie', 'images')
        updated_count = 0
        not_found = 0
        image_files = os.listdir(images_folder)

        for movie in Movie.objects.all():
            norm_title = self.normalize_title(movie.title)
            found = False
            for file in image_files:
                # Busca archivos que empiecen con 'm_' y contengan el título normalizado
                file_norm = self.normalize_title(file)
                if file_norm.startswith('m_' + norm_title):
                    image_rel_path = os.path.join('movie', 'images', file)
                    movie.image = image_rel_path
                    movie.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Imagen asignada: {movie.title} -> {image_rel_path}"))
                    found = True
                    break
            if not found:
                # Asigna la imagen por defecto si no se encontró ninguna
                default_image = os.path.join('movie', 'images', 'default.JPG')
                movie.image = default_image
                movie.save()
                not_found += 1
                self.stderr.write(f"Imagen no encontrada para: {movie.title}. Se asignó imagen por defecto.")

        self.stdout.write(self.style.SUCCESS(f"Actualizadas {updated_count} películas con imagen. {not_found} sin imagen."))
