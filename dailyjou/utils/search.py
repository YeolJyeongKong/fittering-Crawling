import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from tqdm import tqdm
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import constants
from aws import rds
from dailyjou.utils import utils


def get_product_li(page_url):
    response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup.select('ul.prdList2.grid4 > [id^="anchorBoxId_"]')


def get_url(product_li):
    product_url = (
        "https://dailyjou.com"
        + product_li.select_one("div.thumbnail > div.prdImg > a")["href"]
    )
    thumbnail_img_url = (
        "https:" + product_li.select_one("div.thumbnail > div.prdImg > a > img")["src"]
    )
    return product_url, thumbnail_img_url


def get_price(soup):
    try:
        price = int(
            re.sub(
                r"\([^)]*\)|,", "", soup.select_one("span#span_product_price_sale").text
            ).strip()
        )
    except AttributeError:
        price = int(
            re.sub(
                r"\([^)]*\)|,",
                "",
                soup.select_one("strong#span_product_price_text").text,
            ).strip()
        )
    return price


def get_img_url_lst(soup):
    img_url_lst = list(
        map(
            lambda x: constants.DAILYJOU_ROOT_URL + x["ec-data-src"],
            soup.select_one("div.cont").select("img"),
        )
    )
    return img_url_lst


def get_size_dict_lst(soup, category_id):
    size_url = "https:" + soup.select_one("iframe")["src"]

    response = requests.get(size_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.content.decode("utf-8", "replace")
    soup = BeautifulSoup(html, "html.parser")

    size_table = soup.select_one(
        "table.sf_size_view.sfc_2baeb41-table.sfc_2baeb41-sf_size_view"
    )
    size_df = utils.table2df(size_table)
    size_dict_lst = utils.df2size_dict_lst(size_df, category_id)
    return size_dict_lst


def crawling_product(subcategory_id, product_url):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    product_dict = {}

    product_dict["disabled"] = "FALSE"
    product_dict["price"] = get_price(soup)
    product_dict["name"] = soup.select_one(
        "div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr.xans-record- > td > span"
    ).text
    product_dict["gender"] = "F"
    product_dict["sub_category_id"] = subcategory_id
    product_dict["category_id"] = constants.SUB2CAT[product_dict["sub_category_id"]]
    product_dict["url"] = product_url
    product_dict["mall_id"] = constants.DAILYJOU_ID
    product_dict["description_path"] = "NULL"

    img_url_lst = get_img_url_lst(soup)
    size_dict_lst = get_size_dict_lst(soup, product_dict["category_id"])

    return product_dict, size_dict_lst, img_url_lst


def crawling_page(subcategory_id, page_url, s3_obj, conn, cursor):
    product_li_lst = get_product_li(page_url)

    if not product_li_lst:
        return False

    for product_li in tqdm(
        product_li_lst, total=len(product_li_lst), desc=f"crawling page {page_url}"
    ):
        try:
            product_url, thumbnail_image_url = get_url(product_li)
            product_dict, size_dict_lst, img_url_lst = crawling_product(
                subcategory_id, product_url
            )
            if not product_dict:
                print(f"pass product url: {product_url}")
                continue

            product_id = rds.insert_product(conn, cursor, product_dict)

            for size_dict, cat_size_dict in size_dict_lst:
                cat_size_id = rds.insert_cat_size(
                    conn, cursor, cat_size_dict, product_dict["category_id"]
                )
                size_dict["product_id"] = product_id

                size_dict[
                    constants.DAILYJOU_CAT_SIZE_ID[product_dict["category_id"]]
                ] = cat_size_id
                rds.insert_size(conn, cursor, size_dict)
            utils.s3_rds_image(
                product_id, thumbnail_image_url, img_url_lst, s3_obj, conn, cursor
            )
        except TypeError as e:
            print(f"error: {e} | product_url: {product_url}")
        except requests.exceptions.InvalidURL as e:
            print(f"error: {e} | product_url: {product_url}")
        except requests.exceptions.ConnectionError as e:
            print(f"error: {e} | product_url: {product_url}")
        except ValueError as e:
            print(f"error: {e} | product_url: {product_url}")
    return True
