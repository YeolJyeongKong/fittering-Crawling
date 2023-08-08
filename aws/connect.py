import logging
import sys
import json
import pymysql
import pyrootutils
import pandas as pd
import boto3

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths


def connect_RDS():
    json_path = paths.RDS_PASSWORD_PATH
    with open(json_path) as f:
        json_object = json.load(f)

    try:
        conn = pymysql.connect(
            host=json_object["host"],
            user=json_object["username"],
            passwd=json_object["password"],
            db=json_object["database"],
            port=json_object["port"],
            use_unicode=True,
            charset="utf8",
        )
        cursor = conn.cursor()
    except:
        logging.error("RDS에 연결되지 않았습니다.")
        sys.exit(1)

    return conn, cursor


def close_RDS(conn, cursor):
    conn.commit()
    conn.close()


def connect_s3():
    try:
        s3_access_key = pd.read_csv(paths.S3_ACCESS_KEY_PATH)
        s3 = boto3.client(
            "s3",
            aws_access_key_id=s3_access_key["Access key ID"].values[0],
            aws_secret_access_key=s3_access_key["Secret access key"].values[0],
            region_name="ap-northeast-2",
        )
    except:
        s3 = boto3.client("s3")

    return s3
