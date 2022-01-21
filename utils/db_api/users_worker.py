from .db_core import DatabaseCore


class UsersWorker(DatabaseCore):
    def register_new_user(self, user_id, username, language_id, ref):
        sql = f"INSERT INTO " \
              f"BookBotAdmin_users(userId, username, balance, isBlock, showProgress, deposit, subscribeTime, languageId_id, referral_id, notEndPayment, isAutoPay, lastMenu) " \
              f"VALUES({user_id}, '{username}', 0, 0, 0, 0, 0, {language_id}, {ref}, 0, 1, 0)"

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
        if "-" in action:
            sql = f"UPDATE BookBotAdmin_users SET balance=balance{action} WHERE userId={user_id}"
        else:
            sql = f"UPDATE BookBotAdmin_users SET balance=balance{action}, deposit=deposit{action} WHERE userId={user_id}"

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

    def add_to_deposit(self, user_id, amount):
        sql = f"UPDATE BookBotAdmin_users SET deposit=deposit+{amount} WHERE userId={user_id}"

        self.send_query(sql)

    def change_is_blocked(self, user_id, is_block):
        sql = f"UPDATE BookBotAdmin_users SET isBlock={is_block} WHERE userId={user_id}"

        self.send_query(sql)

    def get_all_subs(self):
        sql = "SELECT userId, languageId_id FROM BookBotAdmin_users users " \
              "LEFT JOIN BookBotAdmin_subscribes subs " \
              "on subs.user_id = users.UserId " \
              "WHERE isActive=1"

        return self.send_query(sql)

    def is_auto_pay(self, user_id):
        sql = f"SELECT * FROM BookBotAdmin_users WHERE userId={user_id}"

        response = self.send_query(sql)

        return response[0]["isAutoPay"]

    def change_is_auto_pay(self, user_id, action):
        sql = f"UPDATE BookBotAdmin_users SET isAutoPay={action} WHERE userId={user_id}"

        self.send_query(sql)

    def get_filtered_users(self, filters):
        sql_add = list()

        sql_add.append(f"languageId_id={filters['languageId_id']}")
        sql_add.append(f'isActive={filters["isSubscribed"]}')
        sql_add.append(f'notEndPayment={filters["notEndPayment"]}')

        sql_add.append(f'balance>={filters["balanceFrom"]}')
        if int(filters["balanceTo"]):
            sql_add.append(f'balance<={filters["balanceTo"]}')

        sql_add.append(f'subscribeTime>={filters["subscribeTimeFrom"]}')
        if int(filters["subscribeTimeTo"]):
            sql_add.append(f'subscribeTime<={filters["subscribeTimeTo"]}')

        sql_add.append(f'deposit>={filters["depositFrom"]}')
        if int(filters["depositTo"]):
            sql_add.append(f'deposit<={filters["depositTo"]}')

        sql_add = " AND ".join(sql_add)

        sql = f"SELECT userId FROM BookBotAdmin_users users " \
              f"LEFT JOIN BookBotAdmin_subscribes subs on users.userId = subs.user_id " \
              f"WHERE {sql_add}"

        records = self.send_query(sql)
        if records:
            return [el["userId"] for el in records]
        return False

    def get_last_menu(self, user_id):
        sql = f"SELECT lastMenu FROM BookBotAdmin_users WHERE userId={user_id}"

        record = self.send_query(sql)[0]
        return int(record["lastMenu"])

    def update_last_menu(self, user_id, new_menu):
        sql = f"UPDATE BookBotAdmin_users SET lastMenu={new_menu} WHERE userId={user_id}"

        self.send_query(sql)