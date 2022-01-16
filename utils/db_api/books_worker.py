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

    def is_user_payed_for_book(self, user_id, book_id):
        sql = f"SELECT * FROM BookBotAdmin_books_userId WHERE books_id={book_id} AND users_id={user_id}"

        records = self.send_query(sql)
        if records:
            return True
        return False

    def add_payed_book_for_user(self, user_id, book_id):
        sql = f"INSERT INTO BookBotAdmin_books_userId(users_id, books_id) VALUES({user_id}, {book_id})"

        self.send_query(sql)

    def add_to_collected_sum(self, book_id, amount):
        sql = f"UPDATE BookBotAdmin_books SET collectedSum=collectedSum+{amount} WHERE bookId={book_id}"

        self.send_query(sql)

    def make_book_done(self, book_id):
        sql = f"UPDATE BookBotAdmin_books SET isDone=1 WHERE bookId={book_id}"

        self.send_query(sql)

    def get_payed_users(self, book_id):
        sql = f"SELECT users_id FROM BookBotAdmin_books_userId books " \
              f"LEFT JOIN BookBotAdmin_users users " \
              f"on books.users_id = users.userId " \
              f"WHERE books_id={book_id} AND isBlock=0"

        records = self.send_query(sql)
        return [el["users_id"] for el in records]
