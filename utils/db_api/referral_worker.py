from .db_core import DatabaseCore


class ReferralWorker(DatabaseCore):
    def is_code_exists(self, code):
        sql = f"SELECT name FROM BookBotAdmin_referrals WHERE code='{code}'"
        records = self.send_query(sql)

        if records:
            return True
        return False

    def add_to_register_count(self, code):
        sql = f"UPDATE BookBotAdmin_referrals SET registerCount=registerCount+1 WHERE code='{code}'"

        self.send_query(sql)
