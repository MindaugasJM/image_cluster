from .models import Image

pictures_from_db = Image.objects.all()

print(pictures_from_db)
