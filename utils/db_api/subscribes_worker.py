from .db_core import DatabaseCore


class SubscribesWorker(DatabaseCore):
    def is_user_have_active_subscribe(self, user_id):
        sql = f"SELECT isActive FROM  BookBotAdmin_subscribes WHERE user_id={user_id}"

        records = self.send_query(sql)

        if records:
            return records[0]

        return False
