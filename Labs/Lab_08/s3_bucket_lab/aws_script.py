#!/usr/bin/env python3
import boto3
import sys
import os
import requests

file_url = sys.argv[1]
bucket_name = sys.argv[2]
expiration = int(sys.argv[3])

local_filename = os.path.basename(file_url.split("?")[0])

response = requests.get(file_url, stream=True)
response.raise_for_status()

with open(local_filename, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

s3_client = boto3.client("s3")
s3_client.upload_file(local_filename, bucket_name, local_filename)

url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": local_filename},
        ExpiresIn=expiration
    )

print(f"\n🔗 Presigned URL (valid for {expiration} seconds):\n{url}")