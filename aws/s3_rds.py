from aws import s3, rds


def save_image_(product_id, img_url, s3_obj, conn, cursor, thumbnail):
    fname = s3.upload_image(s3_obj, img_url)
    imagepath_dict = {"url": fname, "product_id": product_id, "thumbnail": thumbnail}
    rds.insert_imagepath(conn, cursor, imagepath_dict)


def save_image(product_id, thumbnail_img_url, img_url_lst, s3_obj, conn, cursor):
    save_image_(product_id, thumbnail_img_url, s3_obj, conn, cursor, "TRUE")
    for img_url in img_url_lst:
        save_image_(product_id, img_url, s3_obj, conn, cursor, "FALSE")


def save_image2_(product_id, img_dict, s3_obj, conn, cursor, thumbnail):
    fname = s3.upload_image2(s3_obj, img_dict)
    imagepath_dict = {"url": fname, "product_id": product_id, "thumbnail": thumbnail}
    rds.insert_imagepath(conn, cursor, imagepath_dict)


def save_image2(product_id, thumbnail_img_dict, img_dicts, s3_obj, conn, cursor):
    save_image2_(product_id, thumbnail_img_dict, s3_obj, conn, cursor, "TRUE")
    for img_dict in img_dicts:
        save_image2_(product_id, img_dict, s3_obj, conn, cursor, "FALSE")
