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

    return soup.select(
        'div.xans-element-.xans-product.xans-product-listnormal.ec-base-product > ul.prdList.grid3 > [id^="anchorBoxId_"]'
    )


def get_url(product_li):
    product_url = (
        constants.MERRYAROUND_ROOT_URL
        + product_li.select_one("div.box > div.thumbnail > div.prdImg > a")["href"]
    )
    thumbnail_img_url = product_li.select_one(
        "div.box > div.thumbnail > div.prdImg > a > img"
    )["src"]
    if not thumbnail_img_url.startswith("http"):
        thumbnail_img_url = "https:" + thumbnail_img_url
    return product_url, thumbnail_img_url


def get_price(soup):
    price_lst = list(
        filter(
            lambda x: x["rel"] == "할인판매가",
            soup.select_one("div.infowrap").select(
                "div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr"
            ),
        )
    )
    if not price_lst:
        price_lst = list(
            filter(
                lambda x: x["rel"] == "판매가",
                soup.select_one("div.infowrap").select(
                    "div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr"
                ),
            )
        )
    return int("".join(re.findall(r"\d+", price_lst[0].select_one("td").text)))


def get_text(soup):
    text = None
    for p in soup.select_one("ul.sect.deco2").select("p"):
        text = p.find_all(string=True)
        if text:
            break

    if text:
        text = "\n".join(text)
    return text


def get_size_text_dict(soup):
    string_lst = soup.select_one("ul.sect.deco3 > div > div").find_all(string=True)
    size_text_dict = {}
    flag = 0
    for i, string in enumerate(string_lst):
        string = string.strip()
        if flag and string == "":
            break
        if flag:
            size_split = string.split("/")
            if len(size_split) == 1:
                size_name = "FREE"
                size_value_string = size_split[0]
            else:
                size_name, size_value_string = size_split
            size_text_dict[size_name] = size_value_string.strip()
        if string == "Size":
            flag = 1

    return size_text_dict


def get_size_dict_lst(soup, category_id):
    size_text_dict = get_size_text_dict(soup)
    size_dict_lst = []
    for name in size_text_dict:
        matches = re.findall(r"(\D+)(\d+\.\d+|\d+)", size_text_dict[name])
        cat_size_dict_ori = {
            re.sub(r"\([^)]*\)", "", key).strip(): float(value)
            for key, value in matches
        }

        size_dict = {
            "name": name,
            "product_id": "NULL",
            "top_id": "NULL",
            "outer_id": "NULL",
            "bottom_id": "NULL",
            "dress_id": "NULL",
        }

        cat_size_dict = {}

        if category_id == 2:
            for col, key in constants.MERRYAROUND_TOP_SIZE_COL2KEY.items():
                if col not in cat_size_dict_ori:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(cat_size_dict_ori[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 4:
            for col, key in constants.MERRYAROUND_BOTTOM_SIZE_COL2KEY.items():
                if col not in cat_size_dict_ori:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(cat_size_dict_ori[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 3:
            for col, key in constants.MERRYAROUND_DRESS_SIZE_COL2KEY.items():
                if col not in cat_size_dict_ori:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(cat_size_dict_ori[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 1:
            for col, key in constants.MERRYAROUND_OUTER_SIZE_COL2KEY.items():
                if col not in cat_size_dict_ori:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(cat_size_dict_ori[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
    return size_dict_lst


def crawling_product(subcategory_id, product_url):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    product_dict = {}

    product_dict["disabled"] = "FALSE"

    product_dict["price"] = get_price(soup)
    product_dict["name"] = soup.select_one("div.headingArea > h2").text
    product_dict["gender"] = "F"
    product_dict["sub_category_id"] = subcategory_id
    product_dict["category_id"] = constants.SUB2CAT[product_dict["sub_category_id"]]
    product_dict["url"] = product_url
    product_dict["mall_id"] = constants.MERRYAROUND_ID

    img_url_lst = [
        img_tag["src"].replace(" ", "%20")
        for img_tag in soup.select_one("div#prdDetail").select("img")
    ]

    text = get_text(soup)
    size_dict_lst = get_size_dict_lst(soup, product_dict["category_id"])
    for size_dict in size_dict_lst:
        utils.not_null_check(size_dict[1], product_dict["category_id"])

    return product_dict, size_dict_lst, img_url_lst, text


def get_image_body(img_url):
    if not img_url.startswith("http"):
        img_url = constants.MERRYAROUND_ROOT_URL + img_url
    response = requests.get(img_url, headers=constants.HEADER)
    image_data = response.content
    if img_url.endswith(".jpg"):
        extension = ".jpg"
        content_type = "image/jpg"
    elif img_url.endswith(".png"):
        extension = ".png"
        content_type = "image/png"
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

            if text:
                product_dict["description_path"] = s3.upload_text(s3_obj, text)
            else:
                product_dict["description_path"] = "NULL"
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
        except Exception as e:
            print(f"error: {e} | product_url: {product_url}")
        # except IndexError as e:
        #     print(f"error: {e} | product_url: {product_url}")
        # # except requests.exceptions.InvalidURL as e:
        # #     print(f"error: {e} | product_url: {product_url}")
        # except requests.exceptions.ConnectionError as e:
        #     print(f"error: {e} | product_url: {product_url}")
        # except ValueError as e:
        #     print(f"error: {e} | product_url: {product_url}")
    return True
