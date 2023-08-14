import rds_info


def get_product(product):
    row = {}
    row["product"] = {key: value for key, value in zip(rds_info.product_keys, product)}
    return row


def get_mall(row, cursor):
    query = f"""
    SELECT * FROM MALL WHERE MALL_ID={row['product']['mall_id']};
    """
    cursor.execute(query)
    mall = cursor.fetchall()[0]
    row["mall"] = {key: value for key, value in zip(rds_info.mall_keys, mall)}
    return row


def get_size(row, cursor):
    if row["product"]["category_id"] == 1:
        query = f"""
        SELECT * FROM SIZE 
        JOIN OUTER_SIZE ON SIZE.OUTER_ID = OUTER_SIZE.OUTER_ID
        WHERE PRODUCT_ID = {row['product']['product_id']};
        """
        cursor.execute(query)
        sizes = cursor.fetchall()

        row["size"] = []
        for size in sizes:
            size_dict = {
                key: value for key, value in zip(rds_info.outer_keys, size[-4:])
            }
            size_dict["name"] = size[1]
            row["size"] += [size_dict]
        return row

    if row["product"]["category_id"] == 2:
        query = f"""
        SELECT * FROM SIZE 
        JOIN TOP_SIZE ON SIZE.TOP_ID = TOP_SIZE.TOP_ID
        WHERE PRODUCT_ID = {row['product']['product_id']};
        """
        cursor.execute(query)
        sizes = cursor.fetchall()

        row["size"] = []
        for size in sizes:
            size_dict = {key: value for key, value in zip(rds_info.top_keys, size[-4:])}
            size_dict["name"] = size[1]
            row["size"] += [size_dict]
        return row

    if row["product"]["category_id"] == 3:
        query = f"""
        SELECT * FROM SIZE 
        JOIN DRESS_SIZE ON SIZE.DRESS_ID = DRESS_SIZE.DRESS_ID
        WHERE PRODUCT_ID = {row['product']['product_id']};
        """
        cursor.execute(query)
        sizes = cursor.fetchall()

        row["size"] = []
        for size in sizes:
            size_dict = {
                key: value for key, value in zip(rds_info.dress_keys, size[-9:])
            }
            size_dict["name"] = size[1]
            row["size"] += [size_dict]
        return row

    if row["product"]["category_id"] == 4:
        query = f"""
        SELECT * FROM SIZE 
        JOIN BOTTOM_SIZE ON SIZE.BOTTOM_ID = BOTTOM_SIZE.BOTTOM_ID
        WHERE PRODUCT_ID = {row['product']['product_id']};
        """
        cursor.execute(query)
        sizes = cursor.fetchall()

        row["size"] = []
        for size in sizes:
            size_dict = {
                key: value for key, value in zip(rds_info.bottom_keys, size[-6:])
            }
            size_dict["name"] = size[1]
            row["size"] += [size_dict]
        return row


def get_imagepath(row, cursor):
    query = f"""
    SELECT * FROM IMAGEPATH
    WHERE PRODUCT_ID = {row['product']['product_id']} AND THUMBNAIL = 1;
    """
    cursor.execute(query)

    row["imagepath"] = []
    row["imagepath"] += [cursor.fetchall()[0][1]]

    query = f"""
    SELECT * FROM IMAGEPATH
    WHERE PRODUCT_ID = {row['product']['product_id']} AND NOT THUMBNAIL = 1;
    """
    cursor.execute(query)
    row["imagepath"] += [imagepath[1] for imagepath in cursor.fetchall()]

    return row
