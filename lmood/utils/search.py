from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import pyrootutils
import pandas as pd
import boto3
from datetime import datetime

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from lmood.utils import utils, search, category
from extras import constants, paths
from aws import rds, s3


def get_product_li(page_url):
    response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(
        "#contents > div.xans-element-.xans-product.xans-product-listnormal.shop-wrap > ul > li"
    )


def get_url(product_li):
    product_url = (
        constants.LMOOD_ROOT_URL
        + product_li.select("div.thumbnail-image > a")[0].attrs["href"]
    )
    thumbnail_image_url = (
        "https:" + product_li.select("div.thumbnail-image > a > img")[0]["src"]
    )
    return product_url, thumbnail_image_url


def get_product_size_name(soup):
    size_li_lst = list(
        filter(
            lambda li: li.select("label")[0].text == "사이즈",
            soup.select(
                "li.xans-element-.xans-product.xans-product-option.xans-record-"
            ),
        )
    )
    if not size_li_lst:
        return []

    sizes_name = list(
        map(
            lambda x: x.text,
            size_li_lst[0].select("li"),
        )
    )
    return sizes_name


def get_product_all_size_df(soup):
    table = soup.select("div.guideBoard > table")[0]
    size_df = utils.table2df(table)
    return size_df


def get_product_price(soup):
    price = utils.price_str2int(
        soup.select("div#span_prd_price_sale_text")[0].get_text().strip()
    )
    return price


def crawling_size(sizes_name, product_id, category_id, soup, conn, cursor):
    table = soup.select("div.guideBoard > table")[0]
    size_df = utils.table2df(table)
    sizes_name = [
        size_name for size_name in sizes_name if size_name in list(size_df.index)
    ]
    size_df = size_df.loc[sizes_name]

    for size_name in size_df.index:
        row = size_df.loc[size_name]
        rds.insert_cat_size(conn, cursor, row, category_id, product_id)


def crawling_image(soup):
    img_url_lst = soup.select("div.imgitem > a > img")
    img_url_lst = list(
        map(lambda x: constants.LMOOD_ROOT_URL + x.attrs["src"], img_url_lst)
    )
    return img_url_lst


def s3_rds_image_(product_id, img_url, s3_obj, conn, cursor, thumbnail):
    fname = s3.upload_image(s3_obj, img_url)
    imagepath_dict = {"url": fname, "product_id": product_id, "thumbnail": thumbnail}
    rds.insert_imagepath(conn, cursor, imagepath_dict)


def s3_rds_image(product_id, thumbnail_img_url, img_url_lst, s3_obj, conn, cursor):
    s3_rds_image_(product_id, thumbnail_img_url, s3_obj, conn, cursor, "TRUE")

    for img_url in img_url_lst:
        s3_rds_image_(product_id, img_url, s3_obj, conn, cursor, "FALSE")


def update_product(product_url, products_df, conn, cursor):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    update = False
    product_id = products_df[products_df["url"] == product_url]["product_id"].values[0]
    new_price = get_product_price(soup)
    old_price = products_df[products_df["url"] == product_url]["price"].values[0]
    if new_price != old_price:
        update = True
        rds.update_price(cursor, product_url, new_price)

    new_sizes_name = get_product_size_name(soup)
    old_sizes_df = rds.get_product_size_df(cursor, product_id)
    if old_sizes_df.empty:
        old_sizes_df = pd.DataFrame(
            columns=[
                "SIZE_ID",
                "NAME",
                "PRODUCT_ID",
                "TOP_ID",
                "OUTER_ID",
                "BOTTOM_ID",
                "DRESS_ID",
            ]
        )
    size_df = get_product_all_size_df(soup)
    category_id = products_df[products_df["url"] == product_url]["category_id"].values[
        0
    ]
    update, disabled = rds.update_size(
        conn,
        cursor,
        new_sizes_name,
        old_sizes_df,
        size_df,
        category_id,
        product_id,
        update,
    )
    if update:
        rds.update_product(product_id, disabled, cursor)


def crawling_product(product_url, s3_obj, conn, cursor):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    product_dict = {}
    sizes_name = get_product_size_name(soup)
    if sizes_name:
        product_dict["disabled"] = "FALSE"
    else:
        product_dict["disabled"] = "TRUE"

    product_dict["price"] = utils.price_str2int(
        soup.select("div#span_prd_price_sale_text")[0].get_text().strip()
    )
    product_dict["name"] = soup.select("h3.product-name")[0].get_text().strip()
    product_dict["gender"] = "M"
    sub_category_id = category.classify(product_dict["name"])
    product_dict["sub_category_id"] = sub_category_id
    product_dict["category_id"] = constants.SUB2CAT[product_dict["sub_category_id"]]
    product_dict["url"] = product_url
    product_dict["mall_id"] = constants.LMOOD_ID

    text = soup.find("p", {"class": "ko"}).find_all(string=True)
    text = "\n".join(list(map(lambda x: x.strip(), text)))
    product_dict["description_path"] = s3.upload_text(s3_obj, text)

    product_id = rds.insert_product(conn, cursor, product_dict)

    if sizes_name:
        crawling_size(
            sizes_name, product_id, product_dict["category_id"], soup, conn, cursor
        )

    img_url_lst = crawling_image(soup)
    return product_id, img_url_lst


def update_page(page_url, products_df, s3_obj, conn, cursor):
    product_li_lst = search.get_product_li(page_url)
    if not product_li_lst:
        return False

    for product_li in tqdm(
        product_li_lst, total=len(product_li_lst), desc="crawling page"
    ):
        try:
            product_url, thumbnail_image_url = search.get_url(product_li)
            if product_url not in products_df["url"].values:
                product_id, img_url_lst = search.crawling_product(
                    product_url, s3_obj, conn, cursor
                )

                search.s3_rds_image(
                    product_id, thumbnail_image_url, img_url_lst, s3_obj, conn, cursor
                )
            else:
                update_product(product_url, products_df, conn, cursor)

        except Exception as e:
            product_url = (
                constants.LMOOD_ROOT_URL
                + product_li.select("div.thumbnail-image > a")[0].attrs["href"]
            )
            print(f"누락된 product url: {product_url}, 누락이유: {e}")
    return True


def crawling_page(page_url, s3_obj, conn, cursor):
    product_li_lst = search.get_product_li(page_url)
    if not product_li_lst:
        return False

    for product_li in tqdm(
        product_li_lst, total=len(product_li_lst), desc="crawling page"
    ):
        try:
            product_url, thumbnail_image_url = search.get_url(product_li)
            product_id, img_url_lst = search.crawling_product(
                product_url, s3_obj, conn, cursor
            )
            if not product_id:
                continue

            search.s3_rds_image(
                product_id, thumbnail_image_url, img_url_lst, s3_obj, conn, cursor
            )
        except Exception as e:
            product_url = (
                constants.LMOOD_ROOT_URL
                + product_li.select("div.thumbnail-image > a")[0].attrs["href"]
            )
            print(f"누락된 product url: {product_url}, 누락이유: {e}")
    return True
