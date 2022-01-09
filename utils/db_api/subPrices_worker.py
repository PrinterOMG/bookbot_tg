from .db_core import DatabaseCore


class SubPricesWorker(DatabaseCore):
    def get_all_subs(self):
        sql = "SELECT subPriceId, value, duration FROM BookBotAdmin_subprices"

        return self.send_query(sql)
