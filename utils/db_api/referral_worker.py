from .db_core import DatabaseCore


class ReferralWorker(DatabaseCore):
    def is_code_exists(self, code):
        sql = f"SELECT name FROM BookBotAdmin_referrals WHERE code='{code}'"
        records = self.send_query(sql)

        if records:
            return True
        return False

    def get_id_by_code(self, code):
        sql = f"SELECT referralId FROM BookBotAdmin_referrals WHERE code='{code}'"
        records = self.send_query(sql)

        if records:
            return str(records[0]["referralId"])
        return None

    def add_to_register_count(self, ref_id):
        sql = f"UPDATE BookBotAdmin_referrals SET registerCount=registerCount+1 WHERE referralId={ref_id}"

        self.send_query(sql)
