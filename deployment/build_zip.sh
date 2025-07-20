#!/bin/bash
set -e

# Clean previous builds
rm -rf package lambda_function.zip

# Create folder for dependencies and change into the project directory
mkdir package
cd package

# Install dependencies to package folder from requirements file
pip install -r ../../requirements.txt -t . &> /dev/null 

# Copy your lambda function code into package folder
cp ../../lambda-S3-thumbnail.py .

# Zip all contents into deployment package
zip -r ../lambda_function.zip . &> /dev/null

# Go back to deployment folder
cd ..

echo "Created lambda_function.zip for deployment"

