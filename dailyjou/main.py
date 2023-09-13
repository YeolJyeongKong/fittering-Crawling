import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from dailyjou.utils import search
from extras import constants
from aws import s3, rds


def main():
    s3_obj = s3.connect()
    conn, cursor = rds.connect()
    page = 1
    while True:
        page_url = constants.DAILYJOU_TOP_PAGE_URL + f"&page={page}"
        if not search.crawling_page(page_url, s3_obj, conn, cursor):
            break
        page += 1

    rds.close(conn, cursor)


if __name__ == "__main__":
    main()
