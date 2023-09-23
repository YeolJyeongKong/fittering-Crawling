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


CAT_SIZE_ID = {
    1: "outer_id",
    2: "top_id",
    3: "dress_id",
    4: "bottom_id",
}

CAT_SIZE_NOT_NULL_COL = {
    1: ["full", "sleeve"],
    2: ["full", "chest"],
    3: [
        "full",
        "bottom_width",
    ],
    4: [
        "full",
        "waist",
        "bottom_width",
    ],
}


# ----------------------LMOOD----------------------
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


# ----------------------DAILYJOU----------------------
DAILYJOU_ROOT_URL = "https://dailyjou.com"
DAILYJOU_ID = 2

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


# ----------------------LOOKPLE----------------------
LOOKPLE_ROOT_URL = "https://lookple.com"
LOOKPLE_ID = 3

LOOKPLE_SUBCATEGORY2PAGE_URL = {
    9: [
        "https://lookple.com/category/%EB%B0%98%ED%8C%94%ED%8B%B0%EB%AF%BC%EC%86%8C%EB%A7%A4%ED%8B%B0/59/",
        "https://lookple.com/category/%EA%B8%B4%ED%8C%94%ED%8B%B0/60/",
        "https://lookple.com/category/%ED%8F%B4%EB%9D%BC%ED%8B%B0/123/",
    ],
    10: [
        "https://lookple.com/category/%EB%A7%A8%ED%88%AC%EB%A7%A8%ED%9B%84%EB%93%9C/65/"
    ],
    8: [
        "https://lookple.com/category/%EB%8B%88%ED%8A%B8/128/",
        "https://lookple.com/category/%EC%A1%B0%EB%81%BC/130/",
        "https://lookple.com/category/%ED%8F%B4%EB%9D%BC/131/",
        "https://lookple.com/category/%EB%B0%98%ED%8C%94%EB%8B%88%ED%8A%B8/144/",
    ],
    7: [
        "https://lookple.com/category/%EB%B2%A0%EC%9D%B4%EC%A7%81%EB%AC%B4%EC%A7%80%EA%B8%B4%ED%8C%94/53/",
        "https://lookple.com/category/%EB%B0%98%ED%8C%94-%EC%85%94%EC%B8%A0/57/",
        "https://lookple.com/category/%EC%8A%A4%ED%8A%B8%EB%9D%BC%EC%9D%B4%ED%94%84/102/",
        "https://lookple.com/category/%EC%B2%B4%ED%81%AC%ED%8C%A8%ED%84%B4/103/",
    ],
    12: [
        "https://lookple.com/category/%EC%8A%AC%EB%9E%99%EC%8A%A4/71/",
        "https://lookple.com/category/%EC%B2%AD%EB%B0%94%EC%A7%80/73/",
        "https://lookple.com/category/%EB%A9%B4%EB%B0%94%EC%A7%80%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D/72/",
        "https://lookple.com/category/%EB%B0%98%EB%B0%94%EC%A7%80/100/",
        "https://lookple.com/category/%EB%B0%B4%EB%94%A9%EB%B0%94%EC%A7%80/149/",
    ],
    # 13: ["https://dailyjou.com/product/list.html?cate_no=48"],
    # 11: ["https://dailyjou.com/product/list.html?cate_no=80"],
    6: [
        "https://lookple.com/category/%EC%A0%90%ED%8D%BC/115/",
        "https://lookple.com/category/%EB%A0%88%EB%8D%94/121/",
    ],
    2: ["https://lookple.com/category/%EC%BD%94%ED%8A%B8/46/"],
    3: ["https://lookple.com/category/%EA%B0%80%EB%94%94%EA%B1%B4/129/"],
    4: ["https://lookple.com/category/%ED%8C%A8%EB%94%A9/47/"],
    5: ["https://lookple.com/category/%EC%9E%90%EC%BC%93/45/"],
}

LOOKPLE_TOP_SIZE_COL2KEY = {
    "총장": "full",
    "어깨": "shoulder",
    "가슴": "chest",
    "소매": "sleeve",
}

LOOKPLE_BOTTOM_SIZE_COL2KEY = {
    "총장": "full",
    "허리": "waist",
    "허벅지": "thigh",
    "밑위": "rise",
    "밑단": "bottom_width",
    "엉덩이": "hip_width",
}

LOOKPLE_DRESS_SIZE_COL2KEY = {
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

LOOKPLE_OUTER_SIZE_COL2KEY = {
    "총장": "full",
    "어깨": "shoulder",
    "가슴": "chest",
    "소매": "sleeve",
}
