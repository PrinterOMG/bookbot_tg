from .db_core import DatabaseCore


class ArchiveWorker(DatabaseCore):
    def is_book_in_base(self, book_id):
        sql = f"SELECT * FROM BookBotAdmin_archivestatistic WHERE archivebookId={book_id}"

        records = self.send_query(sql)
        if records:
            return True
        return False

    def add_book(self, book):
        id = book["id"]
        title = book["title"]
        genre = book["genre"]
        author = book["author"]
        year = book["year"]
        price = book["price"]
        link = book["link"]

        sql = f"INSERT INTO BookBotAdmin_archivestatistic(archivebookId, title, author, year, genre, link, price, appeal, buy_count) " \
              f"VALUES({id}, '{title}', '{author}', '{year}', '{genre}', '{link}', '{price}', 0, 0)"

        self.send_query(sql)

    def update_appeal(self, book_id):
        sql = f"UPDATE BookBotAdmin_archivestatistic SET appeal=appeal+1 WHERE archivebookId={book_id}"

        self.send_query(sql)

    def update_buy(self, book_id):
        sql = f"UPDATE BookBotAdmin_archivestatistic SET buy_count=buy_count+1 WHERE archivebookId={book_id}"

        self.send_query(sql)
