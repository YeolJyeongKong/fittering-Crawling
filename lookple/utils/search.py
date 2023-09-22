import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import constants
from aws import rds, s3, s3_rds
from lookple.utils import utils


def get_product_li(page_url):
    response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup.select('ul.prdList.grid3 > [id^="anchorBoxId_"]')


def get_url(product_li):
    product_url = (
        constants.LOOKPLE_ROOT_URL
        + product_li.select_one("div.prdBox > div.thumbnail > a")["href"]
    )
    thumbnail_img_url = (
        "https:" + product_li.select_one("div.prdBox > div.thumbnail > a > img")["src"]
    )
    return product_url, thumbnail_img_url


def get_price(info_df):
    if "할인판매가" in info_df.index:
        price = int(re.sub(r"\([^)]*\)|,|원", "", info_df.loc["할인판매가", 1]).strip())
    else:
        price = int(re.sub(r"\([^)]*\)|,|원", "", info_df.loc["판매가", 1]).strip())
    return price


def get_img_url_lst(soup):
    img_url_lst = [
        constants.LOOKPLE_ROOT_URL + img_tag["ec-data-src"]
        for img_tag in soup.select_one("div#prdDetail").select("img")
    ]
    return img_url_lst


def get_size_dict_lst(text, category_id):
    size_df = utils.text2sizedf(text)
    if not all(map(utils.is_english, size_df["사이즈"].to_list())):
        raise ValueError(f"{size_df['사이즈'].to_list()} is not all english")
    size_dict_lst = utils.df2size_dict_lst(size_df, category_id)
    return size_dict_lst


def crawling_product(subcategory_id, product_url):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    info_df = utils.table2df(soup.select_one("table"))

    product_dict = {}

    not_sold_out = soup.select("div.btnArea > span.displaynone.sold")

    if not_sold_out:
        product_dict["disabled"] = "FALSE"
    else:
        product_dict["disabled"] = "TRUE"

    product_dict["price"] = get_price(info_df)
    product_dict["name"] = info_df.loc["상품명", 1].strip()
    product_dict["gender"] = "M"
    product_dict["sub_category_id"] = subcategory_id
    product_dict["category_id"] = constants.SUB2CAT[product_dict["sub_category_id"]]
    product_dict["url"] = product_url
    product_dict["mall_id"] = constants.LOOKPLE_ID

    text = info_df.loc["상품설명", 1]
    img_url_lst = get_img_url_lst(soup)
    size_dict_lst = get_size_dict_lst(text, product_dict["category_id"])
    utils.not_null_check(size_dict_lst[0][1], product_dict["category_id"])

    return product_dict, size_dict_lst, img_url_lst, text


def crawling_page(subcategory_id, page_url, s3_obj, conn, cursor):
    product_li_lst = get_product_li(page_url)

    if not product_li_lst:
        return False

    print(f"crawling page {page_url}")
    for product_li in tqdm(product_li_lst, total=len(product_li_lst)):
        try:
            product_url, thumbnail_image_url = get_url(product_li)
            product_dict, size_dict_lst, img_url_lst, text = crawling_product(
                subcategory_id, product_url
            )
            thumbnail_img_dict, img_dicts = get_image_bodies(
                thumbnail_image_url, img_url_lst
            )

            product_dict["description_path"] = s3.upload_text(s3_obj, text)
            product_id = rds.insert_product(conn, cursor, product_dict)

            for size_dict, cat_size_dict in size_dict_lst:
                cat_size_id = rds.insert_cat_size(
                    conn, cursor, cat_size_dict, product_dict["category_id"]
                )
                size_dict["product_id"] = product_id

                size_dict[
                    constants.CAT_SIZE_ID[product_dict["category_id"]]
                ] = cat_size_id
                rds.insert_size(conn, cursor, size_dict)
            s3_rds.save_image2(
                product_id, thumbnail_img_dict, img_dicts, s3_obj, conn, cursor
            )
        except IndexError as e:
            print(f"error: {e} | product_url: {product_url}")
        # except requests.exceptions.InvalidURL as e:
        #     print(f"error: {e} | product_url: {product_url}")
        except requests.exceptions.ConnectionError as e:
            print(f"error: {e} | product_url: {product_url}")
        except ValueError as e:
            print(f"error: {e} | product_url: {product_url}")
    return True


def get_disabled_price(product_url):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    info_df = utils.table2df(soup.select_one("table"))
    price = get_price(info_df)

    not_sold_out = soup.select("div.btnArea > span.displaynone.sold")
    if not_sold_out:
        disabled = 0
    else:
        disabled = 1

    return disabled, price


def get_image_body(img_url):
    response = requests.get(img_url, headers=constants.HEADER)
    image_data = response.content
    if img_url.endswith(".jpg"):
        extension = ".jpg"
        content_type = "image/jpg"
    elif img_url.endswith(".gif"):
        extension = ".gif"
        content_type = "image/jpg"
    elif img_url.endswith(".svg"):
        extension = ".svg"
        content_type = "image/svg+xml"
    else:
        raise ValueError(f"img_url: {img_url} is not image")
    return {"body": image_data, "extension": extension, "content_type": content_type}


def get_image_bodies(thumbnail_img_url, img_url_lst):
    thumbnail_img_dict = get_image_body(thumbnail_img_url)
    img_dicts = [get_image_body(img_url) for img_url in img_url_lst]
    return thumbnail_img_dict, img_dicts


def update_page(products_url_set, subcategory_id, page_url, s3_obj, conn, cursor):
    product_li_lst = get_product_li(page_url)

    if not product_li_lst:
        return False

    print(f"update page {page_url}")
    for product_li in tqdm(product_li_lst, total=len(product_li_lst)):
        try:
            product_url, thumbnail_image_url = get_url(product_li)
            if product_url in products_url_set:
                continue

            product_dict, size_dict_lst, img_url_lst, text = crawling_product(
                subcategory_id, product_url
            )
            thumbnail_img_dict, img_dicts = get_image_bodies(
                thumbnail_image_url, img_url_lst
            )

            product_dict["description_path"] = s3.upload_text(s3_obj, text)
            product_id = rds.insert_product(conn, cursor, product_dict)

            for size_dict, cat_size_dict in size_dict_lst:
                cat_size_id = rds.insert_cat_size(
                    conn, cursor, cat_size_dict, product_dict["category_id"]
                )
                size_dict["product_id"] = product_id

                size_dict[
                    constants.CAT_SIZE_ID[product_dict["category_id"]]
                ] = cat_size_id
                rds.insert_size(conn, cursor, size_dict)
            s3_rds.save_image2(
                product_id, thumbnail_img_dict, img_dicts, s3_obj, conn, cursor
            )
        except IndexError as e:
            print(f"error: {e} | product_url: {product_url}")
        # except requests.exceptions.InvalidURL as e:
        #     print(f"error: {e} | product_url: {product_url}")
        # except requests.exceptions.ConnectionError as e:
        #     print(f"error: {e} | product_url: {product_url}")
        except ValueError as e:
            print(f"error: {e} | product_url: {product_url}")
    return True
