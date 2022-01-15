from .db_core import DatabaseCore


class UsersWorker(DatabaseCore):
    def register_new_user(self, user_id, username, language_id, ref):
        sql = f"INSERT INTO BookBotAdmin_users(userId, username, balance, isBlock, showProgress, deposit, subscribeTime, languageId_id, referral_id, notEndPayment) " \
              f"VALUES({user_id}, '{username}', 0, 0, 0, 0, 0, {language_id}, {ref}, 0)"

        print(sql)
        self.send_query(sql)

    def is_user_reg(self, user_id):
        sql = f"SELECT username FROM BookBotAdmin_users WHERE userid={user_id}"
        records = self.send_query(sql)

        if records:
            return True
        return False

    def get_user_language(self, user_id):
        sql = f"SELECT languageId_id FROM BookBotAdmin_users WHERE userId={user_id}"

        return self.send_query(sql)

    def change_user_language(self, user_id, new_lang_id):
        sql = f"UPDATE BookBotAdmin_users SET languageId_id={new_lang_id} WHERE userId={user_id}"

        self.send_query(sql)

    def get_balance(self, user_id):
        sql = f"SELECT balance FROM BookBotAdmin_users WHERE userId={user_id}"

        return int(self.send_query(sql)[0]["balance"])

    def change_balance(self, user_id, action):
        sql = f"UPDATE BookBotAdmin_users SET balance=balance{action} WHERE userId={user_id}"

        self.send_query(sql)

    def get_show_progress(self, user_id):
        sql = f"SELECT showProgress FROM BookBotAdmin_users WHERE userId={user_id}"

        return self.send_query(sql)[0]["showProgress"]

    def change_show_progress(self, user_id, new):
        sql = f"UPDATE BookBotAdmin_users SET showProgress={new} WHERE userId={user_id}"

        self.send_query(sql)

    def save_payment_method(self, user_id, payment_method_id):
        sql = f"UPDATE BookBotAdmin_users SET paymentId='{payment_method_id}' WHERE userId={user_id}"

        self.send_query(sql)
