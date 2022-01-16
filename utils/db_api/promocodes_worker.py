from .db_core import DatabaseCore


class PromocodesWorker(DatabaseCore):
    def cancel_user_promocode(self, user_id):
        sql = f"UPDATE BookBotAdmin_promocodes SET whoUsed_id=NULL, isActive=0 WHERE whoUsed_id={user_id}"

        self.send_query(sql)

    def is_user_have_active_promocode(self, user_id):
        sql = f"SELECT * FROM BookBotAdmin_promocodes WHERE whoUsed_id={user_id} AND isActive=1"
        records = self.send_query(sql)

        if records:
            return True
        return False

    def check_promocode(self, code):
        sql = f"SELECT * FROM BookBotAdmin_promocodes WHERE promocode='{code}'"

        record = self.send_query(sql)

        if not record:
            return "not exists"

        if record[0]["isActive"] or record[0]["isUsed"]:
            return "already used"

        return record

    def set_user_promocode(self, user_id, code):
        sql = f"UPDATE BookBotAdmin_promocodes SET whoUsed_id={user_id}, isActive=1 WHERE promocode='{code}'"

        self.send_query(sql)

    def get_user_discount(self, user_id):
        sql = f"SELECT subprice.subprices_id, promo.discount FROM BookBotAdmin_promocodes promo " \
              f"LEFT JOIN BookBotAdmin_promocodes_subPriceId subprice " \
              f"on promo.promocodeId = subprice.promocodes_id " \
              f"WHERE whoUsed_id={user_id} AND isActive=1"

        records = self.send_query(sql)
        if records:
            sub_prices = [el["subprices_id"] for el in records]
            discount = records[0]["discount"]

            return sub_prices, discount
        else:
            return False, False

    def use_promocode(self, user_id):
        sql = f"UPDATE BookBotAdmin_promocodes SET isActive=0, isUsed=1 WHERE isActive=1 AND whoUsed_id={user_id}"

        self.send_query(sql)
