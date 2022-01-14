from .db_core import DatabaseCore

import datetime


class BooksWorker(DatabaseCore):
    def get_all_books(self):
        cur_date = datetime.date.today()
        sql = f"SELECT * FROM BookBotAdmin_books " \
              f"WHERE " \
              f"STR_TO_DATE('{cur_date}', '%Y-%m-%d') " \
              f"BETWEEN STR_TO_DATE(startDate, '%Y-%m-%d') AND STR_TO_DATE(endDate, '%Y-%m-%d')"

        return self.send_query(sql)

    def get_book(self, book_id):
        sql = f"SELECT * FROM BookBotAdmin_books WHERE bookId={book_id}"

        return self.send_query(sql)[0]
