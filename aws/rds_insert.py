def insert_product(conn, cursor, product_dict):
    query = f"""
    INSERT INTO PRODUCT(PRICE, NAME, GENDER, CATEGORY_ID, SUB_CATEGORY_ID, URL, MALL_ID) 
    VALUES({product_dict['price']}, '{product_dict['name']}', '{product_dict['gender']}', {product_dict['category_id']}, {product_dict['sub_category_id']}, '{product_dict['url']}', {product_dict['mall_id']})
    """
    cursor.execute(query)


def insert_mall(conn, cursor, mall_dict):
    query = f"""
    INSERT INTO MALL (NAME, URL, DESCRIPTION, IMAGE) VALUES('{mall_dict['name']}', '{mall_dict['url']}', '{mall_dict['description']}', '{mall_dict['image']}')
    """
    cursor.execute(query)
