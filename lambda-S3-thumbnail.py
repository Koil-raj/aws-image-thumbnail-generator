import boto3
import os
from PIL import Image
from io import BytesIO
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.client('s3')
MAX_SIZE_MB = 2  # Maximum allowed image size in MB

def lambda_handler(event, context):
    # Log the full incoming event for debugging
    logger.debug(f"Received event: {event}")

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if key.endswith('_thumbnail.jpg'):  # avoid recursive trigger
        logger.debug(f"Skipping thumbnail creation for {key}")
        return

    try:
        # Fetch object metadata first to check file size
        head = s3.head_object(Bucket=bucket, Key=key)
        content_length = head['ContentLength']

        if content_length > MAX_SIZE_MB * 1024 * 1024:
            logger.warning(f"File {key} is too large to process ({content_length} bytes).")
            return {
                'statusCode': 413,
                'body': 'Image too large to process'
            }

        # Download image from S3
        img_object = s3.get_object(Bucket=bucket, Key=key)
        img = Image.open(img_object['Body'])

        # Create thumbnail
        img.thumbnail((128, 128))  # You can adjust size

        buffer = BytesIO()
        img.save(buffer, 'JPEG')
        buffer.seek(0)

        # Upload thumbnail to the same or different bucket
        thumbnail_key = 'Thumbnail/' + os.path.basename(key)
        s3.put_object(
            Bucket=bucket,
            Key=thumbnail_key,
            Body=buffer,
            ContentType='image/jpeg'
        )
        logger.debug(f"Thumbnail saved as {thumbnail_key}")

        return {
            'statusCode': 200,
            'body': f'Thumbnail saved as {thumbnail_key}'
        }

    except Exception as e:
        logger.error(f"Error processing {key} from bucket {bucket}. Exception: {str(e)}")
        raise e

