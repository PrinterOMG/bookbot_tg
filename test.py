from loader import books_worker


books = (books_worker.get_all_books())
[print(el) for el in books]
