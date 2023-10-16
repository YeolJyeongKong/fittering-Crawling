import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import rds, s3


if __name__ == "__main__":
    image_url = "https://dailyjou.com/web/upload/yangji_pc_ether/main_logo.svg"
    s3_obj = s3.connect()
    fname = "merryaround_logo.png"

    conn, cursor = rds.connect()
    mall_dict = {
        "mall_id": 4,
        "name": "메리어라운드",
        "url": "https://merryaround.co.kr",
        "description": "10대, 20대 여성 쇼핑몰",
        "image": fname,
    }
    mall_id = rds.insert_mall(conn, cursor, mall_dict)
    rds.close(conn, cursor)

    print("mall_id: ", mall_id)
