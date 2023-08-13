from tqdm import tqdm
import pandas as pd
import boto3
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths


if __name__ == "__main__":
    s3_access_key = pd.read_csv(paths.S3_ACCESS_KEY_PATH)
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=s3_access_key["Access key ID"].values[0],
        aws_secret_access_key=s3_access_key["Secret access key"].values[0],
        region_name="ap-northeast-2",
    )
    bucket = s3.Bucket("fittering-crawling-image")
    for i in tqdm(bucket.objects.all()):
        s3.Object("fittering-crawling-image", i.key).delete()
