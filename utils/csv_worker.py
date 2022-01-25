import pandas as pd
import aiofiles as aiof


async def search(filename, s_type, value):
    reader = pd.read_csv("../admin/" + filename, delimiter=";")
    reader.year = reader.year.astype(str)

    print(reader.head())

    return reader[reader[s_type].str.contains(str(value), case=False)].to_dict()


async def get_book(filename, book_id):
    reader = pd.read_csv("../admin/" + filename, delimiter=";")

    result = reader[reader.id == book_id].to_dict()
    print(result)
    i = get_key(result["id"], book_id)
    for key in result.keys():
        result[key] = result[key][i]

    return result


async def create_txt_with_books(books, user_id):
    filename = f"data/temp/{user_id}_books.txt"
    async with aiof.open(filename, "w") as out:
        await out.write(books)
        await out.flush()

    return filename


def get_key(d, value):
    for k, v in d.items():
        if int(v) == int(value):
            return k
