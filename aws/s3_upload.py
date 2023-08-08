import requests
import base64
import boto3
import pandas as pd
import pyrootutils
from datetime import datetime

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths, constants


def upload(s3, image_url):
    response = requests.get(image_url, headers=constants.HEADER)
    image_data = response.content

    fname = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        s3.put_object(
            Bucket=constants.BUCKET_NAME,
            Key=fname + ".jpg",
            Body=image_data,
            ContentType="image/jpg",
        )
    except Exception as e:
        print(e)

    return fname
