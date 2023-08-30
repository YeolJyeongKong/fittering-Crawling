import pymysql
import rds_info
import json
import boto3
import rds
from datetime import datetime

conn = pymysql.connect(
    host=rds_info.db_host,
    user=rds_info.db_username,
    passwd=rds_info.db_password,
    db=rds_info.db_name,
    port=rds_info.db_port,
)


def handler(event, context):
    product_range = event["range"]
    updated_at = datetime.strptime(event["updated_at"], "%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    query = f"""
        SELECT * FROM PRODUCT WHERE PRODUCT_ID BETWEEN {product_range[0]} AND {product_range[1]};
    """
    cursor.execute(query)
    products = cursor.fetchall()

    body = []
    for product in products:
        row = rds.get_product(product)
        if row["product"]["updated_at"] < updated_at:
            continue
        row["product"]["updated_at"] = row["product"]["updated_at"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        row = rds.get_mall(row, cursor)
        row = rds.get_size(row, cursor)
        row = rds.get_imagepath(row, cursor)

        body += [row]

    return {"statusCode": 200, "body": body}


if __name__ == "__main__":
    event = {"range": [1, 12], "updated_at": "2024-08-01 00:00:00"}
    print(handler(event, None))
