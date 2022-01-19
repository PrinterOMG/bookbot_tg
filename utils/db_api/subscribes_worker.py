from .db_core import DatabaseCore
import datetime


class SubscribesWorker(DatabaseCore):
    def is_user_have_active_subscribe(self, user_id):
        sql = f"SELECT isActive, endDate FROM BookBotAdmin_subscribes WHERE user_id={user_id} AND isActive=1"

        records = self.send_query(sql)

        if records:
            return records[0]["endDate"]

        return False

    def is_sub_expired(self, user_id):
        sql = f"SELECT endDate FROM BookBotAdmin_subscribes WHERE user_id={user_id} AND isActive=0"

        records = self.send_query(sql)

        if records:
            return records[0]["endDate"]

        return False


    def create_subscribe_record(self, user_id, sub_type):
        sql = f"SELECT duration FROM BookBotAdmin_subprices WHERE subPriceId={sub_type}"
        records = self.send_query(sql)
        sub_duration = records[0]["duration"]
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30 * sub_duration)
        sql = f"INSERT INTO BookBotAdmin_subscribes(startDate, endDate, subPriceId_id, user_id, isActive) VALUES('{start_date}', '{end_date}', {sub_type}, {user_id}, 1)"

        self.send_query(sql)

    def make_is_active_false(self, user_id):
        sql = f"UPDATE BookBotAdmin_subscribes SET isActive=0 WHERE user_id={user_id}"

        self.send_query(sql)

    def update_subscribe_record(self, user_id, sub_type):
        sql = f"SELECT duration FROM BookBotAdmin_subprices WHERE subPriceId={sub_type}"
        sub_duration = self.send_query(sql)[0]["duration"]
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30 * sub_duration)
        sql = f"UPDATE BookBotAdmin_subscribes SET isActive=1, startDate='{start_date}', endDate='{end_date}', " \
              f"subPriceId_id={sub_type} WHERE user_id={user_id} "

        self.send_query(sql)

    def check_subscribe(self, user_id):
        sql = f"SELECT * FROM BookBotAdmin_subscribes WHERE user_id={user_id}"

        response = self.send_query(sql)
        if response:
            return True
        return False
