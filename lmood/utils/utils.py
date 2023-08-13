import re
import pandas as pd


def price_str2int(amount_str):
    pattern = r"\d+"  # 하나 이상의 숫자에 매칭하는 정규표현식 패턴
    matches = re.findall(pattern, amount_str)

    if matches:
        amount = int("".join(matches))
        return amount
    else:
        return None


def table2df(table):
    data = []
    for row in table.find_all("tr"):
        row_data = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
        data.append(row_data)

    # DataFrame 생성 후 행과 열을 바꿈
    df = pd.DataFrame(data)
    df = df.transpose()
    df.set_index(0, inplace=True)

    # 첫 번째 행을 헤더로 설정
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def del_space(text):
    return re.sub(r"\s+", "", text)
