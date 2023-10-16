from extras import constants


def not_null_check(size_dict, category_id):
    for col in constants.CAT_SIZE_NOT_NULL_COL[category_id]:
        if size_dict[col] == "NULL":
            raise ValueError(f"{col} is NULL, {size_dict}")
