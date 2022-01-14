from .db_core import DatabaseCore
import datetime


class SubscribesWorker(DatabaseCore):
    def is_user_have_active_subscribe(self, user_id):
        sql = f"SELECT isActive FROM  BookBotAdmin_subscribes WHERE user_id={user_id}"

        records = self.send_query(sql)

        if records:
            return records[0]

        return False

    def create_subscribe_record(self, user_id, sub_type):
        sql = f"SELECT duration FROM BookBotAdmin_subprices WHERE subPriceId={sub_type}"
        sub_duration = self.send_query(sql)[0]["duration"]
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30 * sub_duration)
        sql = f"INSERT INTO BookBotAdmin_subscribes(startDate, endDate, subPriceId, user) VALUES({start_date}, {end_date}, {sub_type}, {user_id})"

        self.send_query(sql)

    def make_is_active_false(self, user_id):
        sql = f"UPDATE BookBotAdmin_subscribes SET isActive=0 WHERE user={user_id}"

        self.send_query(sql)

    def update_subscribe_record(self, user_id, sub_type):
        sql = f"SELECT duration FROM BookBotAdmin_subprices WHERE subPriceId={sub_type}"
        sub_duration = self.send_query(sql)[0]["duration"]
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30 * sub_duration)
        sql = f"UPDATE BookBotAdmin_subscribes SET isActive=1, startDate={start_date}, endDate={end_date}, subPriceId={sub_type} WHERE user={user_id}"

        self.send_query(sql)
