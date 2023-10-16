import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from merryaround.utils import search
from extras import constants
from aws import s3, rds


def main():
    s3_obj = s3.connect()
    conn, cursor = rds.connect()
    for (
        subcategory_id,
        subcategory_url_lst,
    ) in constants.MERRYAROUND_SUBCATEGORY2PAGE_URL.items():
        # if subcategory_id != 6:
        #     continue
        for subcategory_url in subcategory_url_lst:
            page = 1
            while True:
                page_url = subcategory_url + f"?page={page}"
                if not search.crawling_page(
                    subcategory_id, page_url, s3_obj, conn, cursor
                ):
                    break
                page += 1

    rds.close(conn, cursor)


if __name__ == "__main__":
    main()
