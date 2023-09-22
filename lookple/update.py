from tqdm import tqdm
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from lookple.utils import search
from extras import constants
from aws import s3, rds


def existing_product_update(cursor, products_df):
    for row in tqdm(
        products_df.iterrows(), total=len(products_df), desc="existing product update"
    ):
        disabled, price = search.get_disabled_price(row[1]["url"])
        if disabled != row[1]["DISABLED"]:
            rds.update_product(row[1]["product_id"], disabled, cursor)
        if price != row[1]["price"]:
            rds.update_price_t(cursor, row[1]["url"], price)


def main():
    s3_obj = s3.connect()
    conn, cursor = rds.connect()
    products_df = rds.get_product_df(cursor, mall_id=constants.LOOKPLE_ID)
    products_url_set = set(products_df["url"].to_list())
    # existing_product_update(cursor, products_df)

    for (
        subcategory_id,
        subcategory_url_lst,
    ) in constants.LOOKPLE_SUBCATEGORY2PAGE_URL.items():
        if subcategory_id != 9:
            continue

        for subcategory_url in subcategory_url_lst:
            page = 1
            while True:
                page_url = subcategory_url + f"?page={page}"
                if not search.update_page(
                    products_url_set, subcategory_id, page_url, s3_obj, conn, cursor
                ):
                    break
                page += 1

    rds.close(conn, cursor)


if __name__ == "__main__":
    main()
