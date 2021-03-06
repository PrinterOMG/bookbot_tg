from .db_core import DatabaseCore


class LanguagesWorker(DatabaseCore):
    def get_all_languages(self):
        sql = "SELECT languageId, name FROM BookBotAdmin_languages"

        return self.send_query(sql)

    def get_text(self, language_id, args):
        sql = f"SELECT {args} FROM BookBotAdmin_languages WHERE languageId={language_id}"

        return self.send_query(sql)[0]

    def get_text_on_user_language(self, user_id, args):
        sql = f"SELECT {args} FROM BookBotAdmin_languages WHERE " \
              f"languageId=(SELECT languageId_id FROM BookBotAdmin_users WHERE userId={user_id})"

        return self.send_query(sql)[0]
