import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pyrootutils

pyrootutils.setup_root(os.curdir, indicator=".project-root", pythonpath=True)
from lmood.utils import search, utils
from extras import constants
from aws import rds, s3


s3_obj = s3.connect()
conn, cursor = rds.connect()

thumbnail_image_url = "https://lmood.co.kr/renewal/22/WINTER/01_BIG-MOM%20heringbone%20single%20coat/BRWON/1-1.jpg"
product_url = "https://lmood.co.kr/product/detail.html?product_no=2225&cate_no=198&display_group=1"
product_id, img_url_lst = search.crawling_product(product_url, s3_obj, conn, cursor)

search.s3_rds_image(product_id, thumbnail_image_url, img_url_lst, s3_obj, conn, cursor)
