from .db_core import DatabaseCore


class FilterWorker(DatabaseCore):
    def get_filter(self, filter_id):
        sql = f"SELECT * FROM BookBotAdmin_filters WHERE filterId={filter_id}"

        response = self.send_query(sql)

        return response[0]
