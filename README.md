# Image Processing with Webhook Notification

This Django-based system processes image data provided through a CSV file and compresses images by 50% of their original quality. The system is designed to handle image processing asynchronously using Celery, with Amazon SQS as the message broker, and it also triggers a webhook upon successful completion of the task.

## Features

- **CSV Upload:** The system accepts a CSV file containing product details and image URLs.
- **Asynchronous Processing:** Image compression is handled asynchronously using Celery, allowing the system to scale and handle multiple tasks concurrently.
- **Image Compression:** Each image is compressed by 50% of its original quality before being saved.
- **Webhook Integration:** Once image processing is complete, the system triggers a webhook to notify external services. The webhook sends product information and URLs of the compressed images.
- **API-Driven:** After submitting a CSV file, the user receives a unique request ID. The system also provides an API to check the status of the image processing job using this request ID.

## Flow Overview

1. **Upload CSV File:** Users submit a CSV file with product names and comma-separated image URLs.
2. **Validation:** The system validates the format of the CSV.
3. **Processing:** Celery processes the images asynchronously, compressing them by 50%.
4. **Webhook Trigger:** After all images are processed, the system sends a POST request to a specified webhook URL, notifying that the task is complete and sending relevant data.
5. **Status Check:** Users can check the status of image processing through a separate API using the unique request ID provided at the time of file submission.

## Prerequisites

- Python 3.7+
- Django 3.0+
- Celery 5.0+
- Amazon SQS for message queue
- PostgreSQL (or any preferred database)
- `Pillow` for image handling
- `boto3` for Amazon SQS integration

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/image-processing-webhook.git
cd image-processing-webhook
