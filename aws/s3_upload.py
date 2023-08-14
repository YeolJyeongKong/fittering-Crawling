import requests
import base64
import boto3
import pandas as pd
import pyrootutils
from datetime import datetime

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths, constants


def upload_image(s3, image_url):
    response = requests.get(image_url, headers=constants.HEADER)
    image_data = response.content

    fname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
    try:
        s3.put_object(
            Bucket=constants.BUCKET_NAME,
            Key=fname,
            Body=image_data,
            ContentType="image/jpg",
        )
    except Exception as e:
        print(e)

    return fname


def upload_text(s3, text):
    fname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
    try:
        s3.put_object(Bucket=constants.BUCKET_NAME, Key=fname, Body=text)
    except Exception as e:
        print(e)

    return fname
