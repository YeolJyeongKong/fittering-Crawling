import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from lmood.utils import search
from extras import constants
from aws import rds, s3


def main():
    s3_obj = s3.connect()
    conn, cursor = rds.connect()
    products_df = rds.get_product_df(cursor)
    page = 1
    while True:
        page_url = constants.LMOOD_PAGE_URL + f"&page={page}"
        if not search.update_page(page_url, products_df, s3_obj, conn, cursor):
            break
        page += 1

    rds.close(conn, cursor)


if __name__ == "__main__":
    main()
