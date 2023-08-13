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
from aws import connect, rds_insert, s3_upload


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


def crawling_size(product_id, category_id, soup, conn, cursor):
    table = soup.select("div.guideBoard > table")[0]
    size_df = utils.table2df(table)

    for size_name in size_df.index:
        row = size_df.loc[size_name]
        rds_insert.insert_cat_size(conn, cursor, row, category_id, product_id)


def crawling_image(soup):
    img_url_lst = soup.select("div.imgitem > a > img")
    img_url_lst = list(
        map(lambda x: constants.LMOOD_ROOT_URL + x.attrs["src"], img_url_lst)
    )
    return img_url_lst


def s3_rds_image_(product_id, img_url, s3, conn, cursor, thumbnail):
    fname = s3_upload.upload_image(s3, img_url)
    imagepath_dict = {"url": fname, "product_id": product_id, "thumbnail": thumbnail}
    rds_insert.insert_imagepath(conn, cursor, imagepath_dict)


def s3_rds_image(product_id, thumbnail_img_url, img_url_lst, s3, conn, cursor):
    s3_rds_image_(product_id, thumbnail_img_url, s3, conn, cursor, "TRUE")

    for img_url in img_url_lst:
        s3_rds_image_(product_id, img_url, s3, conn, cursor, "FALSE")


def crawling_product(product_url, s3, conn, cursor):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    product_dict = {}

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
    product_dict["description_path"] = s3_upload.upload_text(s3, text)

    product_id = rds_insert.insert_product(conn, cursor, product_dict)
    crawling_size(product_id, product_dict["category_id"], soup, conn, cursor)

    img_url_lst = crawling_image(soup)
    return product_id, img_url_lst


def crawling_page(page_url, s3, conn, cursor):
    product_li_lst = search.get_product_li(page_url)
    if not product_li_lst:
        return False

    for product_li in tqdm(
        product_li_lst, total=len(product_li_lst), desc="crawling page"
    ):
        try:
            product_url, thumbnail_image_url = search.get_url(product_li)
            product_id, img_url_lst = search.crawling_product(
                product_url, s3, conn, cursor
            )

            search.s3_rds_image(
                product_id, thumbnail_image_url, img_url_lst, s3, conn, cursor
            )
        except Exception as e:
            product_url = (
                constants.LMOOD_ROOT_URL
                + product_li.select("div.thumbnail-image > a")[0].attrs["href"]
            )
            print(f"누락된 product url: {product_url}, 누락이유: {e}")
    return True
