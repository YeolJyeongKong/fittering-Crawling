import re
import pandas as pd
import pyrootutils

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)
from extras import constants


def table2df(table):
    data = []
    for row in table.find_all("tr"):
        row_data = [cell.get_text() for cell in row.find_all(["th", "td"])]
        data.append(row_data)

    df = pd.DataFrame(data)
    df = df.set_index(0)

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
            for col, key in constants.LOOKPLE_TOP_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 4:
            for col, key in constants.LOOKPLE_BOTTOM_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 3:
            for col, key in constants.LOOKPLE_DRESS_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
        elif category_id == 1:
            for col, key in constants.LOOKPLE_OUTER_SIZE_COL2KEY.items():
                if col not in row.index:
                    cat_size_dict[key] = "NULL"
                else:
                    cat_size_dict[key] = float(row[col])
            size_dict_lst += [[size_dict, cat_size_dict]]
    return size_dict_lst


def size2dict(x):
    x = x.strip()
    x = x.split(" : ")
    matches = re.findall(r"(\w+) (\d+)", x[1])

    size_dict = {key: int(value) for key, value in matches}
    size_dict["사이즈"] = x[0].strip()
    return size_dict


def text2sizedf(text):
    pattern = r"SIZE([\s\S]*?)\r\n(.*?)\n\r\n"
    size_text = re.search(pattern, text, re.DOTALL).group(2).strip()
    size_text_lst = size_text.split("\n")
    size_dict_lst = [size2dict(s) for s in size_text_lst]
    size_df = pd.DataFrame(size_dict_lst)
    return size_df


def is_english(text):
    if text in ["2XL", "3XL", "4XL"]:
        return True
    return text.encode().isalpha()


def not_null_check(size_dict, category_id):
    for col in constants.CAT_SIZE_NOT_NULL_COL[category_id]:
        if size_dict[col] == "NULL":
            raise ValueError(f"{col} is NULL, {size_dict}")
