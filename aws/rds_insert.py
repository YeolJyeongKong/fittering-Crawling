import pyrootutils

root_dir = pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import paths, constants
from lmood.utils import utils


def insert_mall(conn, cursor, mall_dict):
    query = f"""
    INSERT INTO MALL (NAME, URL, DESCRIPTION, IMAGE) 
        VALUES('{mall_dict['name']}', '{mall_dict['url']}', '{mall_dict['description']}', '{mall_dict['image']}');
    """
    cursor.execute(query)
    return conn.insert_id()


def insert_product(conn, cursor, product_dict):
    query = f"""
    INSERT INTO PRODUCT(PRICE, NAME, GENDER, CATEGORY_ID, SUB_CATEGORY_ID, URL, MALL_ID, DESCRIPTION_PATH) 
        VALUES({product_dict['price']}, '{product_dict['name']}', '{product_dict['gender']}', {product_dict['category_id']}, {product_dict['sub_category_id']}, '{product_dict['url']}', {product_dict['mall_id']}, '{product_dict['description_path']}');
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


def insert_cat_size(conn, cursor, row, category_id, product_id):
    if category_id == 2:
        row.index = constants.LMOOD_TOP_SIZE_COL_NAME
        top_size_dict = {
            db_col: float(row[df_col])
            for df_col, db_col in constants.LMOOD_TOP_SIZE_COL.items()
        }
        top_size_id = insert_top_size(conn, cursor, top_size_dict)

        size_dict = {
            "name": row.name,
            "product_id": product_id,
            "top_id": top_size_id,
            "outer_id": "NULL",
            "bottom_id": "NULL",
            "dress_id": "NULL",
        }
        insert_size(conn, cursor, size_dict)

    elif category_id == 1:
        row.index = constants.LMOOD_OUTER_SIZE_COL_NAME
        outer_size_dict = {
            db_col: float(row[df_col])
            for df_col, db_col in constants.LMOOD_OUTER_SIZE_COL.items()
        }
        outer_size_id = insert_outer_size(conn, cursor, outer_size_dict)

        size_dict = {
            "name": row.name,
            "product_id": product_id,
            "top_id": "NULL",
            "outer_id": outer_size_id,
            "bottom_id": "NULL",
            "dress_id": "NULL",
        }
        insert_size(conn, cursor, size_dict)

    elif category_id == 4:
        row.index = constants.LMOOD_BOTTOM_SIZE_COL_NAME
        bottom_size_dict = {
            db_col: float(row[df_col])
            for df_col, db_col in constants.LMOOD_BOTTOM_SIZE_COL.items()
        }
        bottom_size_dict["hip_width"] = "NULL"
        bottom_size_id = insert_bottom_size(conn, cursor, bottom_size_dict)

        size_dict = {
            "name": row.name,
            "product_id": product_id,
            "top_id": "NULL",
            "outer_id": "NULL",
            "bottom_id": bottom_size_id,
            "dress_id": "NULL",
        }
        insert_size(conn, cursor, size_dict)
