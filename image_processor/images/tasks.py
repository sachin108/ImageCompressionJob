import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from celery import shared_task
from .models import ProcessedImage

@shared_task
def process_images_async(product, image_urls):
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # Compress image by 50%
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=50)
        img_io.seek(0)

        processed_image = ProcessedImage(
            product=product,
            original_url=url
        )
        processed_image.processed_image.save(f'{product.name}_compressed.jpg', ContentFile(img_io.read()))
        processed_image.save()
