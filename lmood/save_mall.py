import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import connect, rds_insert, s3_upload


if __name__ == "__main__":
    image_url = (
        "https://image.msscdn.net/mfile_s01/_brand/free_medium/lmood.png?202307141541"
    )
    s3 = connect.connect_s3()
    fname = s3_upload.upload_image(s3, image_url)

    conn, cursor = connect.connect_RDS()
    mall_dict = {
        "name": "엘무드",
        "url": "https://lmood.co.kr/index.html",
        "description": "엘무드(LMOOD)는 미니멀과 컴포트를 중점으로 이 시대 트렌드를 반영한 컨템포러리 감성 브랜드입니다.",
        "image": fname,
    }
    mall_id = rds_insert.insert_mall(conn, cursor, mall_dict)
    connect.close_RDS(conn, cursor)

    print("mall_id: ", mall_id)
