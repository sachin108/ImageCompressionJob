from django.db import models

class ImageRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    request_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='PENDING')

class Product(models.Model):
    serial_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image_request = models.ForeignKey(ImageRequest, related_name='products', on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255, null=True)  # Store Celery task ID here

class ProcessedImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    original_url = models.URLField()
    processed_image = models.ImageField(upload_to='processed_images/')
    created_at = models.DateTimeField(auto_now_add=True)
