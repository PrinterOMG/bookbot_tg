import pandas as pd
import aiofiles as aiof


async def search(filename, s_type, value):
    reader = pd.read_csv("../admin/" + filename, delimiter=";")
    reader.year = reader.year.astype(str)

    return reader[reader[s_type].str.contains(str(value), case=False)].to_dict()


async def get_book(filename, book_id):
    reader = pd.read_csv(filename, delimiter=";")

    result = reader[reader.index == book_id].to_dict()
    for key in result.keys():
        result[key] = result[key][book_id]

    return result


async def create_txt_with_books(books, user_id):
    filename = f"data/temp/{user_id}_books.txt"
    async with aiof.open(filename, "w") as out:
        await out.write(books)
        await out.flush()

    return filename
