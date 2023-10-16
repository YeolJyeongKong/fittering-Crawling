import random
import requests
import base64
import boto3
import pandas as pd
import pyrootutils
from datetime import datetime

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths, constants


def connect():
    s3_obj = boto3.client("s3")
    return s3_obj


def upload_image(s3_obj, image_url, extension=".jpg", content_type="image/jpg"):
    response = requests.get(image_url, headers=constants.HEADER)
    image_data = response.content
    if image_url.endswith(".jpg"):
        extension = ".jpg"
        content_type = "image/jpg"
    elif image_url.endswith(".gif"):
        extension = ".gif"
        content_type = "image/jpg"
    elif image_url.endswith(".svg"):
        extension = ".svg"
        content_type = "image/svg+xml"

    fname = (
        datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        + str(random.randint(0, 1000000))
        + extension
    )
    try:
        s3_obj.put_object(
            Bucket=constants.S3_BUCKET_NAME,
            Key=constants.S3_PATH + fname,
            Body=image_data,
            ContentType=content_type,
        )
    except Exception as e:
        print(e)

    return fname


def upload_image2(s3_obj, image_dict):
    fname = (
        datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        + str(random.randint(0, 1000000))
        + image_dict["extension"]
    )
    try:
        s3_obj.put_object(
            Bucket=constants.S3_BUCKET_NAME,
            Key=constants.S3_PATH + fname,
            Body=image_dict["body"],
            ContentType=image_dict["content_type"],
        )
    except Exception as e:
        print(e)

    return fname


def upload_text(s3_obj, text):
    fname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
    try:
        s3_obj.put_object(
            Bucket=constants.S3_BUCKET_NAME, Key=constants.S3_PATH + fname, Body=text
        )
    except Exception as e:
        print(e)

    return fname
