#!/bin/bash
# Upload local file to aws s3 bucket

LOCAL_FILE="$1"
BUCKET="$2"
EXPIRATION="$3"
FILE_NAME=$(basename "$LOCAL_FILE")

echo "Uploading '$LOCAL_FILE' to '$BUCKET'..."

aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/$FILE_NAME"

URL=$(aws s3 presign "s3://$BUCKET/$FILE_NAME" --expires-in "$EXPIRATION")

echo "URL: $URL"
