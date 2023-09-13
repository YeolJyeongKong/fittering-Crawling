import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import rds, s3


if __name__ == "__main__":
    image_url = "https://dailyjou.com/web/upload/yangji_pc_ether/main_logo.svg"
    s3_obj = s3.connect()
    fname = s3.upload_image(
        s3_obj, image_url, extension=".svg", content_type="image/svg+xml"
    )

    conn, cursor = rds.connect()
    mall_dict = {
        "mall_id": 2,
        "name": "데일리쥬",
        "url": "https://dailyjou.com",
        "description": "20대 여성의류 쇼핑몰,데일리룩,아우터,가디건,원피스,티셔츠,스커트, 팬츠 등 판매.",
        "image": fname,
    }
    mall_id = rds.insert_mall(conn, cursor, mall_dict)
    rds.close(conn, cursor)

    print("mall_id: ", mall_id)
