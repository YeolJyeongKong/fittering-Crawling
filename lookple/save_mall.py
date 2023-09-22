import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import rds, s3


if __name__ == "__main__":
    image_url = "https://dailyjou.com/web/upload/yangji_pc_ether/main_logo.svg"
    s3_obj = s3.connect()
    fname = "lookple_logo.jpg"

    conn, cursor = rds.connect()
    mall_dict = {
        "mall_id": 3,
        "name": "룩플",
        "url": "https://lookple.com/index.html",
        "description": "룩플,20대남성의류 쇼핑몰,데일리룩,남친룩,루즈핏,오버핏,자체제작.",
        "image": fname,
    }
    mall_id = rds.insert_mall(conn, cursor, mall_dict)
    rds.close(conn, cursor)

    print("mall_id: ", mall_id)
