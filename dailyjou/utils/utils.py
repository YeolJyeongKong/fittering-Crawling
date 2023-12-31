import re
import pandas as pd
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import constants
from aws import rds, s3


def table2df(table):
    data = []
    for row in table.find_all("tr"):
        row_data = [cell.get_text() for cell in row.find_all(["th", "td"])]
        data.append(row_data)

    df = pd.DataFrame(data)

    # # 첫 번째 행을 헤더로 설정
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.columns = [re.sub(r"\([^)]*\)", "", col).strip() for col in df.columns]
    df.columns = [
        constants.DAILYJOU_CAT_SIZE_COL_NAME_DICT[col]
        if col in constants.DAILYJOU_CAT_SIZE_COL_NAME_DICT
        else col
        for col in df.columns
    ]
    return df


def df2size_dict_lst(size_df, category_id):
    size_dict_lst = []
    for idx in size_df.index:
        row = size_df.loc[idx]
        size_dict = {
            "name": row["사이즈"],
            "product_id": "NULL",
            "top_id": "NULL",
            "outer_id": "NULL",
            "bottom_id": "NULL",
            "dress_id": "NULL",
        }

        cat_size_dict = {}

        if category_id == 2:
            for col, key in constants.DAILYJOU_TOP_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    try:
                        cat_size_dict[key] = float(row[col])
                    except ValueError:
                        cat_size_dict[key] = size_value_process(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 4:
            for col, key in constants.DAILYJOU_BOTTOM_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    try:
                        cat_size_dict[key] = float(row[col])
                    except ValueError:
                        cat_size_dict[key] = size_value_process(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 3:
            for col, key in constants.DAILYJOU_DRESS_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    try:
                        cat_size_dict[key] = float(row[col])
                    except ValueError:
                        cat_size_dict[key] = size_value_process(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 1:
            for col, key in constants.DAILYJOU_OUTER_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    try:
                        cat_size_dict[key] = float(row[col])
                    except ValueError:
                        cat_size_dict[key] = size_value_process(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
    return size_dict_lst


def s3_rds_image_(product_id, img_url, s3_obj, conn, cursor, thumbnail):
    fname = s3.upload_image(s3_obj, img_url)
    imagepath_dict = {"url": fname, "product_id": product_id, "thumbnail": thumbnail}
    rds.insert_imagepath(conn, cursor, imagepath_dict)


def s3_rds_image(product_id, thumbnail_img_url, img_url_lst, s3_obj, conn, cursor):
    s3_rds_image_(product_id, thumbnail_img_url, s3_obj, conn, cursor, "TRUE")
    for img_url in img_url_lst:
        s3_rds_image_(product_id, img_url, s3_obj, conn, cursor, "FALSE")


def replace_average(match):
    min_value = float(match.group(1))
    max_value = float(match.group(2))
    average = (min_value + max_value) / 2
    return str(average)


def size_value_process(size_value):
    if "최소" in size_value:
        matches = re.findall(r"(\d+\.\d+|\d+)\(최대\)|(\d+\.\d+|\d+)\(최소\)", size_value)
        numbers = [float(match[0] if match[0] else match[1]) for match in matches]
        average = sum(numbers) / len(numbers)
        return average
    elif "펼쳤을때" in size_value:
        s_lst = size_value.split("/")
        input_text = s_lst[0]
    elif "~" in size_value:
        s_lst = size_value.split("~")
        s_lst = [del_round(s) for s in s_lst]
        return (float(s_lst[0]) + float(s_lst[1])) / 2
    elif "/" in size_value:
        s_lst = size_value.split("/")
        s_lst = [del_round(s) for s in s_lst]
        return (float(s_lst[0]) + float(s_lst[1])) / 2
    elif "-" in size_value:
        s_lst = size_value.split("-")
        s_lst = [del_round(s) for s in s_lst]
        return (float(s_lst[0]) + float(s_lst[1])) / 2
    elif "긴소매" in size_value:
        pattern = r"\d+\(긴소매\)"
        matches = re.search(pattern, size_value)

        if matches:
            result = matches.group()
            input_text = re.search(r"\d+", result).group()
    elif "X" == size_value:
        return "NULL"
    elif "" == size_value:
        return "NULL"
    else:
        input_text = del_round(size_value)
    return float(input_text)


def del_round(text):
    pattern = r"\([^)]*\)"
    return re.sub(pattern, "", text)


def name2subcategory(name):
    if "후드 집업" in name or "후드집업" in name:
        return 1
    if "점퍼" in name:
        return 6
    if "패딩" in name:
        return 4
    if "자켓" in name:
        return 5
    else:
        return 6
