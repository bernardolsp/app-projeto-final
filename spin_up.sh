#!/bin/bash

docker run -v ~/.aws:/root/.aws:ro --env S3_BUCKET_NAME=files-bucket-fastapi-testing simple-s3-api:1.0