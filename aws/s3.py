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
    try:
        s3_access_key = pd.read_csv(paths.S3_ACCESS_KEY_PATH)
        s3_obj = boto3.client(
            "s3",
            aws_access_key_id=s3_access_key["Access key ID"].values[0],
            aws_secret_access_key=s3_access_key["Secret access key"].values[0],
            region_name="ap-northeast-2",
        )
    except:
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
            Bucket=constants.BUCKET_NAME,
            Key=fname,
            Body=image_data,
            ContentType=content_type,
        )
    except Exception as e:
        print(e)

    return fname


def upload_text(s3_obj, text):
    fname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
    try:
        s3_obj.put_object(Bucket=constants.BUCKET_NAME, Key=fname, Body=text)
    except Exception as e:
        print(e)

    return fname
