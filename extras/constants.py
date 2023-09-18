S3_BUCKET_NAME = "fittering-images-bucket"
S3_PATH = "images/"
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


# DAILYJOU
DAILYJOU_ROOT_URL = "https://dailyjou.com"
DAILYJOU_ID = 2

DAILYJOU_CAT_SIZE_ID = {
    1: "outer_id",
    2: "top_id",
    3: "dress_id",
    4: "bottom_id",
}
DAILYJOU_CAT_SIZE_COL_NAME_DICT = {
    "총기장": "총길이",
}

DAILYJOU_SUBCATEGORY2PAGE_URL = {
    9: ["https://dailyjou.com/product/list.html?cate_no=46"],
    10: ["https://dailyjou.com/product/list.html?cate_no=89"],
    8: ["https://dailyjou.com/product/list.html?cate_no=55"],
    7: [
        "https://dailyjou.com/product/list.html?cate_no=51",
        "https://dailyjou.com/product/list.html?cate_no=47",
    ],
    12: [
        "https://dailyjou.com/product/list.html?cate_no=148",
        "https://dailyjou.com/product/list.html?cate_no=150",
        "https://dailyjou.com/product/list.html?cate_no=82",
        "https://dailyjou.com/product/list.html?cate_no=84",
        "https://dailyjou.com/product/list.html?cate_no=85",
    ],
    13: ["https://dailyjou.com/product/list.html?cate_no=48"],
    11: ["https://dailyjou.com/product/list.html?cate_no=80"],
    3: ["https://dailyjou.com/product/list.html?cate_no=44"],
    6: ["https://dailyjou.com/product/list.html?cate_no=45"],
    2: ["https://dailyjou.com/product/list.html?cate_no=52"],
    5: ["https://dailyjou.com/product/list.html?cate_no=53"],
}
DAILYJOU_TOP_SIZE_COL_NAME = ["총길이", "어깨", "가슴", "소매길이"]
DAILYJOU_TOP_SIZE_COL2KEY = {
    "총길이": "full",
    "어깨": "shoulder",
    "가슴": "chest",
    "소매길이": "sleeve",
}

DAILYJOU_BOTTOM_SIZE_COL2KEY = {
    "총길이": "full",
    "허리": "waist",
    "허벅지": "thigh",
    "밑위": "rise",
    "밑단": "bottom_width",
    "엉덩이": "hip_width",
}

DAILYJOU_DRESS_SIZE_COL2KEY = {
    "총길이": "full",
    "어깨": "shoulder",
    "허리": "waist",
    "허벅지": "thigh",
    "암홀": "arm_hall",
    "엉덩이": "hip_width",
    "소매길이": "sleeve",
    "소매통": "sleeve_width",
    "밑단": "bottom_width",
}

DAILYJOU_OUTER_SIZE_COL2KEY = {
    "총길이": "full",
    "어깨": "shoulder",
    "가슴": "chest",
    "소매길이": "sleeve",
}
