from .db_core import DatabaseCore


class SubPricesWorker(DatabaseCore):
    def get_all_subs(self):
        sql = "SELECT subPriceId, value, duration FROM BookBotAdmin_subprices"

        return self.send_query(sql)

    def get_sub(self, sub_type):
        sql = f"SELECT * FROM BookBotAdmin_subprices WHERE subPriceId={sub_type}"

        response = self.send_query(sql)

        return response[0]
