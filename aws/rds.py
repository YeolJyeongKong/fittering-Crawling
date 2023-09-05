from datetime import datetime
import json
import pandas as pd
import pymysql
import pyrootutils

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths, constants, rds_info
from lmood.utils import utils


def connect():
    json_path = paths.RDS_PASSWORD_PATH
    with open(json_path) as f:
        json_object = json.load(f)

    try:
        conn = pymysql.connect(
            host=rds_info.host,
            user=rds_info.user,
            password=rds_info.password,
            db=rds_info.db,
            charset="utf8",
            port=rds_info.port,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        cursor = conn.cursor()
    except:
        logging.error("RDS에 연결되지 않았습니다.")
        sys.exit(1)

    return conn, cursor


def close(conn, cursor):
    conn.commit()
    conn.close()


def get_product_df(cursor):
    query = """
        SELECT * FROM PRODUCT;
    """
    cursor.execute(query)
    products = cursor.fetchall()
    products_df = pd.DataFrame(products)
    return products_df


def get_product_size_df(cursor, product_id):
    query = f"""
        SELECT * FROM SIZE WHERE PRODUCT_ID = {product_id};
    """
    cursor.execute(query)
    size = cursor.fetchall()
    size_df = pd.DataFrame(size)
    return size_df


def insert_mall(conn, cursor, mall_dict):
    query = f"""
    INSERT INTO MALL (NAME, URL, DESCRIPTION, IMAGE) 
        VALUES('{mall_dict['name']}', '{mall_dict['url']}', '{mall_dict['description']}', '{mall_dict['image']}');
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_product(conn, cursor, product_dict):
    query = f"""
    INSERT INTO PRODUCT(PRICE, NAME, GENDER, CATEGORY_ID, SUB_CATEGORY_ID, URL, MALL_ID, DESCRIPTION_PATH, T, DISABLED) 
        VALUES({product_dict['price']}, '{product_dict['name']}', '{product_dict['gender']}', {product_dict['category_id']}, {product_dict['sub_category_id']}, '{product_dict['url']}', {product_dict['mall_id']}, '{product_dict['description_path']}', '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', {product_dict['disabled']});
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_imagepath(conn, cursor, imagepath_dict):
    query = f"""
    INSERT INTO IMAGEPATH (URL, PRODUCT_ID, THUMBNAIL) 
        VALUES('{imagepath_dict['url']}', {imagepath_dict['product_id']}, {imagepath_dict['thumbnail']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_top_size(conn, cursor, top_size_dict):
    query = f"""
    INSERT INTO TOP_SIZE (FULL, SHOULDER, CHEST, SLEEVE) 
        VALUES({top_size_dict['full']}, {top_size_dict['shoulder']}, {top_size_dict['chest']}, {top_size_dict['sleeve']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_outer_size(conn, cursor, outer_size_dict):
    query = f"""
    INSERT INTO OUTER_SIZE (FULL, SHOULDER, CHEST, SLEEVE) 
        VALUES({outer_size_dict['full']}, {outer_size_dict['shoulder']}, {outer_size_dict['chest']}, {outer_size_dict['sleeve']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_bottom_size(conn, cursor, bottom_size_dict):
    if "hip_width" not in bottom_size_dict.keys():
        bottom_size_dict["hip_width"] = "NULL"
    query = f"""
    INSERT INTO BOTTOM_SIZE (FULL, WAIST, THIGH, RISE, BOTTOM_WIDTH, HIP_WIDTH) 
        VALUES({bottom_size_dict['full']}, {bottom_size_dict['waist']}, {bottom_size_dict['thigh']}, {bottom_size_dict['rise']}, {bottom_size_dict['bottom_width']}, {bottom_size_dict['hip_width']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_dress_size(conn, cursor, dress_size_dict):
    query = f"""
    INSERT INTO DRESS_SIZE (FULL, SHOULDER, WAIST, THIGH, ARM_HALL, HIP, SLEEVE, SLEEVE_WIDTH, BOTTOM_WIDTH)
        VALUES({dress_size_dict['full']}, {dress_size_dict['shoulder']}, {dress_size_dict['waist']}, {dress_size_dict['thigh']}, {dress_size_dict['arm_hall']}, {dress_size_dict['hip']}, {dress_size_dict['sleeve']}, {dress_size_dict['sleeve_width']}, {dress_size_dict['bottom_width']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_size(conn, cursor, size_dict):
    query = f"""
    INSERT INTO SIZE (NAME, PRODUCT_ID, TOP_ID, OUTER_ID, BOTTOM_ID, DRESS_ID)
        VALUES('{size_dict['name']}', {size_dict['product_id']}, {size_dict['top_id']}, {size_dict['outer_id']}, {size_dict['bottom_id']}, {size_dict['dress_id']})
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_cat_size(conn, cursor, cat_size_dict, category_id):
    if category_id == 2:
        return insert_top_size(conn, cursor, cat_size_dict)

    elif category_id == 1:
        return insert_outer_size(conn, cursor, cat_size_dict)

    elif category_id == 4:
        return insert_bottom_size(conn, cursor, cat_size_dict)


def update_product(product_id, disabled, cursor):
    query = f"""
        UPDATE PRODUCT
            SET T = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', DISABLED = {disabled}
            WHERE PRODUCT_ID = {product_id}
    """
    cursor.execute(query)


def update_t(cursor, product_url):
    query = f"""
        UPDATE PRODUCT
            SET T = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            WHERE URL = '{product_url}'
    """
    cursor.execute(query)


def update_price(cursor, product_url, new_price):
    query = f"""
        UPDATE PRODUCT
            SET PRICE = {new_price}
            WHERE URL = '{product_url}'
    """
    cursor.execute(query)


def update_size(
    conn, cursor, new_sizes_name, old_sizes_df, size_df, category_id, product_id, update
):
    new_sizes_name_set = set(new_sizes_name)
    old_sizes_name_set = set(old_sizes_df["NAME"].values)

    add_sizes_name_lst = list(new_sizes_name_set - old_sizes_name_set)
    rm_sizes_name_lst = list(old_sizes_name_set - new_sizes_name_set)

    disabled = "FALSE"
    if new_sizes_name_set != old_sizes_name_set:
        update = "TRUE"

    if not new_sizes_name_set:
        disabled = "TRUE"

    if add_sizes_name_lst:
        for add_size_name in add_sizes_name_lst:
            try:
                row = size_df.loc[add_size_name]

                insert_cat_size(conn, cursor, row, category_id, product_id)
            except KeyError:
                pass

    if rm_sizes_name_lst:
        for rm_size_name in rm_sizes_name_lst:
            size_id = old_sizes_df[old_sizes_df["NAME"] == rm_size_name][
                "SIZE_ID"
            ].values[0]
            if category_id == 1:
                category_size_id = old_sizes_df[old_sizes_df["NAME"] == rm_size_name][
                    "OUTER_ID"
                ].values[0]
            elif category_id == 2:
                category_size_id = old_sizes_df[old_sizes_df["NAME"] == rm_size_name][
                    "TOP_ID"
                ].values[0]
            elif category_id == 4:
                category_size_id = old_sizes_df[old_sizes_df["NAME"] == rm_size_name][
                    "BOTTOM_ID"
                ].values[0]
            delete_size(cursor, size_id, category_id, category_size_id)
    return update, disabled


def delete_size(cursor, size_id, category_id, category_size_id):
    query = f"""
        DELETE FROM SIZE WHERE SIZE_ID = {size_id};
    """
    cursor.execute(query)

    if category_id == 1:
        query = f"""
            DELETE FROM OUTER_SIZE WHERE OUTER_ID = {category_size_id};
        """
    elif category_id == 2:
        query = f"""
            DELETE FROM TOP_SIZE WHERE TOP_ID = {category_size_id};
        """
    elif category_id == 4:
        query = f"""
            DELETE FROM BOTTOM_SIZE WHERE BOTTOM_ID = {category_size_id};
        """
    cursor.execute(query)


def delete_ImagePath(cursor, product_id):
    query = f"""
        DELETE FROM IMAGEPATH WHERE PRODUCT_ID = {product_id};
    """
    cursor.execute(query)


def delete_product(cursor, product_id):
    query = f"""
        DELETE FROM PRODUCT WHERE PRODUCT_ID = {product_id};
    """
    cursor.execute(query)
