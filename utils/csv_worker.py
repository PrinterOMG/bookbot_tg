import pandas as pd


async def search(filename, s_type, value):
    reader = pd.read_csv("../admin/" + filename, delimiter=";")

    if s_type == "year":
        return reader[reader.year == str(value)].to_dict()
    else:
        return reader[reader[s_type].str.contains(value, case=False)].to_dict()


def create_txt_with_books():
    pass
