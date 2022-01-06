from .db_core import DatabaseCore


class UsersWorker(DatabaseCore):
    def register_new_user(self, user_id, username, language_id, ref):
        sql = f"INSERT INTO BookBotAdmin_users(userId, username, balance, isBlock, showProgress, deposit, subscribeTime, languageId_id, referral_id) " \
              f"VALUES({user_id}, '{username}', 0, 0, 0, 0, 0, {language_id}, '{ref}')"

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

    def get_text_on_user_language(self, user_id, args):
        sql = f"SELECT {args} FROM BookBotAdmin_languages WHERE " \
              f"languageId=(SELECT languageId_id FROM BookBotAdmin_users WHERE userId={user_id})"

        return self.send_query(sql)
