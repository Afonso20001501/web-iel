from django.core.management.base import BaseCommand
from django.utils import timezone
from webiel.models import Photo

class Command(BaseCommand):
    help = 'Excluir fotos expiradas'

    def handle(self, *args, **kwargs):
        expired_photos = Photo.objects.filter(expires_on__lt=timezone.now())
        for photo in expired_photos:
            photo.image.delete()
            photo.delete()
        self.stdout.write(self.style.SUCCESS(f'Excluiu {expired_photos.count()} fotos expiradas.'))