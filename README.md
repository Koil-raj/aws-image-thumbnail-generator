# aws-image-thumbnail-generator
AWS Lambda function that automatically creates 128x128 JPEG thumbnails for images uploaded to an S3 bucket. Built with Python 3.12 and Pillow 10.2, it checks file size (max 2MB) before processing. Uses S3 event notifications to trigger thumbnail creation, saving results in a dedicated folder within the same bucket.
