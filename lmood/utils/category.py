import re


def classify(name):
    if re.search(r"코트", name):
        return 2

    if re.search(r"후드 집업", name):
        return 1

    if re.search(r"패딩", name):
        return 4

    if re.search(r"티셔츠|슬리브리스", name):
        return 9

    if re.search(r"가디건|니트 집업", name):
        return 3

    if re.search(r"니트|롱 슬리브 니트|롱슬리브 니트", name):
        return 8

    if re.search(r"롱슬리브|롱 슬리브|슬리브리드", name):
        return 9

    if re.search(r"셔츠|데님 셔츠", name):
        return 7

    if re.search(r"재킷|자켓|블레이저|셔켓|트러커", name):
        return 5

    if re.search(r"파일럿|윈드 브레이커|점퍼|블루종", name):
        return 6

    if re.search(r"데님|진|팬츠|슬랙스", name):
        return 12

    if re.search(r"스웻 셔츠|맨투맨|후드", name):
        return 10


if __name__ == "__main__":
    print(classify("에센셜 수피마 슬리브리스 WHITE"))
