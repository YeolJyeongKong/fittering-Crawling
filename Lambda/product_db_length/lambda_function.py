import pymysql
import rds_info
import json
import boto3

conn = pymysql.connect(
    host=rds_info.db_host,
    user=rds_info.db_username,
    passwd=rds_info.db_password,
    db=rds_info.db_name,
    port=rds_info.db_port,
)


def handler(event, context):
    cursor = conn.cursor()
    query = """
    SELECT MAX(PRODUCT_ID) FROM PRODUCT
    """
    cursor.execute(query)
    length = cursor.fetchall()[0][0]

    return {"statusCode": 200, "body": json.dumps(length)}


if __name__ == "__main__":
    print(handler(None, None))
