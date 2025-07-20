# AWS Image Thumbnail Generator using Lambda and S3

AWS Lambda function that automatically creates 128x128 JPEG thumbnails for images uploaded to an S3 bucket. Built with Python 3.12 and Pillow 10.2, it checks file size (max 2MB) before processing. Uses S3 event notifications to trigger thumbnail creation, saving results in a dedicated folder within the same bucket.

---

## Overview

- **AWS Services used:** S3, Lambda, S3 Event Notifications
- **Language:** Python 3.12
- **Dependencies:** Pillow 10.2
- **Functionality:** When an image is uploaded to the configured S3 bucket, the Lambda function generates a 128x128 thumbnail and uploads it back to the `Thumbnail/` folder in the same bucket.

---

## File Structure

- `lambda-S3-thumbnail.py` — Lambda handler code
- `requirements.txt` — Python dependencies
- `deployment/build_zip.sh` — (Optional) script to bundle dependencies and zip for deployment
- `README.md` — This documentation

---

## Setup & Deployment Instructions

### 1. Prepare Lambda Deployment Package - AWS Lambda requires a deployment package containing your code and dependencies.

#### - Create package folder
mkdir package

#### - Install dependencies (make sure python 3.12 is installed on your local system)
pip install -r requirements.txt -t package/

#### - Copy your lambda function code
cp lambda-S3-thumbnail.py package/

#### - Zip the package contents
cd package

zip -r ../lambda_function.zip .

cd ..

#### Note: Alternatively, you can use the provided deployment/build_zip.sh script package the lambda function (Make sure you give the execute permission for build_zip.sh and get into the `deployment` directory and run `sh build_zip.sh`).


### 2. Create and Configure AWS Lambda Function
- Runtime: `Python 3.12`
- Upload the `lambda_function.zip` deployment package
- Set the handler to:  
  lambda-S3-thumbnail.lambda_handler    
- Increase the timeout as needed (default is 3 seconds, which might be too short for image processing)
- Assign an IAM role with the following permissions:
- `s3:GetObject`
- `s3:PutObject`
- `logs:*` (for CloudWatch logging)


### 3. **Configure S3 Bucket**

- Create or select an existing S3 bucket
- Enable **S3 Event Notifications** for **ObjectCreated** events
- Set the event notification destination as your Lambda function
- (Optional) Add filters to trigger only on specific file suffixes (e.g., `.jpg`, `.png`)

---

## Usage

- Upload an image file to your S3 bucket.
- The Lambda function will automatically generate a thumbnail in the `Thumbnail/` folder inside the same bucket.
- Thumbnail size is 128x128 pixels (modifiable in the code).

## Notes

- The function skips files ending with `_thumbnail.jpg` to avoid recursive triggers.
- Images larger than 2MB are skipped to optimize performance and cost.
- Logging is enabled and can be viewed in CloudWatch Logs for debugging.

## Troubleshooting

- Verify Lambda logs in CloudWatch if thumbnails do not appear.
- Check that the Lambda IAM role has the necessary S3 permissions.
- Confirm that S3 event notifications are properly configured.
