from .db_core import DatabaseCore


class StatisticWorker(DatabaseCore):
    def update_all_subs_counter(self):
        sql = f"SELECT * FROM BookBotAdmin_subscribes WHERE isActive=1"

        response = self.send_query(sql)
        count = len(response)

        sql = f"UPDATE BookBotAdmin_statistic SET allSubsCounter={count}"

        self.send_query(sql)

    def update_no_buy_users(self):
        sql = f"SELECT * FROM BookBotAdmin_users"
        response = self.send_query(sql)
        count = len(response)

        sql = f"SELECT * FROM BookBotAdmin_statistic"
        response = self.send_query(sql)[0]
        buy_count = response["allSubsCounter"]

        sql = f'UPDATE BookBotAdmin_statistic SET noBuyUsersCounter={count - buy_count}'

        self.send_query(sql)

    def init_update_no_buy_users(self):
        sql = f"UPDATE BookBotAdmin_statistic SET noBuyUsersCounter=noBuyUsersCounter+1"

        self.send_query(sql)

    def update_block_users(self, action):
        sql = f"UPDATE BookBotAdmin_statistic SET blockUsersCounter=blockUsersCounter{action}1"

        self.send_query(sql)

    def update_interrupt_payments(self, action):
        sql = f"UPDATE BookBotAdmin_statistic SET interruptedPaymentsCount=interruptedPaymentsCount{action}1"

        self.send_query(sql)

    def update_archive_books_sum(self, amount):
        sql = f"UPDATE BookBotAdmin_statistic SET archiveBooksSum=archiveBooksSum+{amount}"

        self.send_query(sql)

    def update_archive_books_count(self):
        sql = f"UPDATE BookBotAdmin_statistic SET archiveBooksCount=archiveBooksCount+1"

        self.send_query(sql)
