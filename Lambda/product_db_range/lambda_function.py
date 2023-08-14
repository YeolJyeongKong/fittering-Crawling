import pymysql
import rds_info
import json
import boto3
import rds

conn = pymysql.connect(
    host=rds_info.db_host,
    user=rds_info.db_username,
    passwd=rds_info.db_password,
    db=rds_info.db_name,
    port=rds_info.db_port,
)


def handler(event, context):
    product_range = event["range"]
    cursor = conn.cursor()
    query = f"""
    SELECT * FROM PRODUCT WHERE PRODUCT_ID BETWEEN {product_range[0]} AND {product_range[1]};
    """
    cursor.execute(query)
    products = cursor.fetchall()

    body = []
    for product in products:
        row = rds.get_product(product)
        row = rds.get_mall(row, cursor)
        row = rds.get_size(row, cursor)
        row = rds.get_imagepath(row, cursor)

        body += [row]

    return {"statusCode": 200, "body": body}
