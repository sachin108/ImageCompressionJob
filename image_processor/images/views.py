import csv
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import process_images_async
from .models import ImageRequest, Product, ProcessedImage
import logging

logger = logging.getLogger(__name__)

def process_csv(csv_file):
    data = []
    csv_file.seek(0) 
    reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
    for row in reader:
        logger.info(f"Processing row: {row}")
        if len(row) != 3:
            logger.error(f"Skipping row {row} - incorrect number of columns (expected 3, got {len(row)})")
            continue

        serial_number = row[0]
        product_name = row[1]
        image_urls = row[2].split(',')

        data.append((serial_number, product_name, image_urls))
    logger.info(f"Processed CSV data: {data}")
    return data

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'File must be a CSV.'}, status=400)

        try:
            data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(data)
            request_id = str(uuid.uuid4())
            image_request = ImageRequest.objects.create(request_id=request_id)

            for row in csv_reader:
                serial_number, product_name, image_urls = row
                product = Product.objects.create(
                    serial_number=serial_number,
                    name=product_name,
                    image_request=image_request
                )
                process_images_async(product, image_urls.split(','))
            return JsonResponse({'request_id': request_id}, status=202)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'upload.html')

def check_status(request, request_id):
    try:
        image_request = ImageRequest.objects.get(request_id=request_id)
        return JsonResponse({'status': image_request.status}, status=200)
    except ImageRequest.DoesNotExist:
        return JsonResponse({'error': 'Invalid request ID'}, status=404)


def product_list(request):
    products = Product.objects.all()
    images = ProcessedImage.objects.all()
    
    context = {
        'products': products,
        'images': images,
    }
    return render(request, 'product_list.html', context)
