import os
import pyrootutils

pyrootutils.setup_root(os.curdir, indicator=".project-root", pythonpath=True)
from lmood.utils import utils, search, category
from extras import constants, paths
from aws import connect, rds_insert, s3_upload


def main():
    s3 = connect.connect_s3()
    conn, cursor = connect.connect_RDS()
    page = 1
    while True:
        page_url = constants.LMOOD_PAGE_URL + f"&page={page}"
        if not search.crawling_page(page_url, s3, conn, cursor):
            break
        page += 1

    connect.close_RDS(conn, cursor)


if __name__ == "__main__":
    main()
