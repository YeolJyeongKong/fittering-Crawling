BUCKET_NAME = "fittering-crawling-image"
HEADER = {"User-Agent": "Mozilla/5.0"}
SUB2CAT = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 3,
    12: 4,
    13: 4,
}

# LMOOD
LMOOD_PAGE_URL = "https://lmood.co.kr/product/list.html?cate_no=198&"
LMOOD_ROOT_URL = "https://lmood.co.kr"
LMOOD_ID = 1

LMOOD_CAT_SIZE_COL_NAME = {
    1: ["총장", "어깨너비", "가슴단면", "소매길이"],
    2: ["총장", "어깨너비", "가슴단면", "소매길이"],
    4: ["총장", "허리단면", "허벅지단면", "밑위", "밑단단면"],
}

LMOOD_CAT_SIZE_ID = {
    1: "outer_id",
    2: "top_id",
    4: "bottom_id",
}

LMOOD_CAT_SIZE_COL = {
    1: {
        "총장": "full",
        "어깨너비": "shoulder",
        "가슴단면": "chest",
        "소매길이": "sleeve",
    },
    2: {
        "총장": "full",
        "어깨너비": "shoulder",
        "가슴단면": "chest",
        "소매길이": "sleeve",
    },
    4: {
        "총장": "full",
        "허리단면": "waist",
        "허벅지단면": "thigh",
        "밑위": "rise",
        "밑단단면": "bottom_width",
    },
}

LMOOD_TOP_SIZE_COL_NAME = ["총장", "어깨너비", "가슴단면", "소매길이"]
LMOOD_TOP_SIZE_COL = {
    "총장": "full",
    "어깨너비": "shoulder",
    "가슴단면": "chest",
    "소매길이": "sleeve",
}

LMOOD_OUTER_SIZE_COL_NAME = ["총장", "어깨너비", "가슴단면", "소매길이"]
LMOOD_OUTER_SIZE_COL = {
    "총장": "full",
    "어깨너비": "shoulder",
    "가슴단면": "chest",
    "소매길이": "sleeve",
}

LMOOD_BOTTOM_SIZE_COL_NAME = ["총장", "허리단면", "허벅지단면", "밑위", "밑단단면"]
LMOOD_BOTTOM_SIZE_COL = {
    "총장": "full",
    "허리단면": "waist",
    "허벅지단면": "thigh",
    "밑위": "rise",
    "밑단단면": "bottom_width",
}


# SLOWAND
SLOWAND_ROOT_URL = "https://www.slowand.com/"
SLOWAND_ID = 2
