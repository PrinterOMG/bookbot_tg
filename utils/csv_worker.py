import pandas as pd
import aiofiles as aiof


async def search(filename, s_type, value):
    reader = pd.read_csv("../admin/" + filename, delimiter="\t")
    # reader = pd.read_csv("books_russian.csv", delimiter=";")
    print(reader.head())

    if s_type == "year":
        if value.isdigit():
            return reader[reader["year"] == int(value)].to_dict()
        else:
            return {"title": {}}
    else:
        return reader[reader[s_type].str.contains(str(value), case=False)].to_dict()


async def create_txt_with_books(books, user_id):
    filename = f"data/temp/{user_id}_books.txt"
    async with aiof.open(filename, "w") as out:
        await out.write(books)
        await out.flush()

    return filename
