from images.tasks import process_images_async
result = process_images_async.delay(product_id=1, image_urls=["https://example.com/image.jpg"])

# Check if the task was sent
print(result.task_id)
