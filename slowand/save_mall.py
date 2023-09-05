import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from aws import rds, s3


if __name__ == "__main__":
    image_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAbFBMVEWYZCqaYimXYyeZYimaYyqXZCWbYyiYZCiaZCiZYyeaYyubYyqZYiqaZCaXYynNtqbg0crz7uuoflTg0sX////4+fT+//vayr2hcUHIrJbu5uPUwbPQtKbn3NbHqpi5lHft4+Kxi2e9oYncysBwCBNzAAAAvElEQVR4AQ3NhWEEMQwF0S+wLPMtQzjpv8fsFPAGIIaoBIvkAiak6CGbeKmerHkDN+49jdc0ZoEQIKiZlvVpG+JIYFgY+3GGa7o5UYORh7c1UVI/7cHQHfF9PWa2XIFASOglfazrfczaUqvoyTr75zKt+6CeA1hTtF7cv77XHzdFEiSvEPHf9eIYoWQ83XPR9Ld+tSzgJjoec5rW49lGWA+Vf5Zt/x7RJDZ0K+YaO3lkF3R4Fw0szlbj4+s/PHMKRt308k8AAAAASUVORK5CYII="
    s3_obj = s3.connect()
    fname = s3.upload_image(s3_obj, image_url)

    conn, cursor = rds.connect()
    mall_dict = {
        "name": "슬로우엔드",
        "url": "https://www.slowand.com/",
        "description": "차가운 인터넷 속에서도 따뜻한 나의 쇼핑메이트이고 싶습니다. 화려하지 않아도 편안하고 담백한 나만의 분위기, 그 속에서 자주 손이 갈 실용적인 옷들을 제작합니다.",
        "image": fname,
    }
    mall_id = rds.insert_mall(conn, cursor, mall_dict)
    rds.close(conn, cursor)

    print("mall_id: ", mall_id)
