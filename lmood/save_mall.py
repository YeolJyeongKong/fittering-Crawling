import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import rds, s3


if __name__ == "__main__":
    image_url = (
        "https://image.msscdn.net/mfile_s01/_brand/free_medium/lmood.png?202307141541"
    )
    s3_obj = s3.connect()
    fname = s3.upload_image(s3_obj, image_url)

    conn, cursor = rds.connect()
    mall_dict = {
        "mall_id": 1,
        "name": "엘무드",
        "url": "https://lmood.co.kr/index.html",
        "description": "엘무드(LMOOD)는 미니멀과 컴포트를 중점으로 이 시대 트렌드를 반영한 컨템포러리 감성 브랜드입니다.",
        "image": fname,
    }
    mall_id = rds.insert_mall(conn, cursor, mall_dict)
    rds.close(conn, cursor)

    print("mall_id: ", mall_id)
