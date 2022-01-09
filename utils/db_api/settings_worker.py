from .db_core import DatabaseCore


class SettingsWorker(DatabaseCore):
    def get_limit_for_question(self):
        sql = "SELECT questionSymbolsLimit FROM BookBotAdmin_settings"

        return self.send_query(sql)[0]["questionSymbolsLimit"]

    def get_choose_languages_text(self):
        sql = "SELECT registerMenu FROM BookBotAdmin_settings"

        return self.send_query(sql)[0]["registerMenu"]
