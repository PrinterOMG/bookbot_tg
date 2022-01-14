from typing import Union

from pymysql.cursors import DictCursor
import pymysql
from contextlib import closing


class DatabaseCore:
    def __init__(self, username, password, host, db_name):
        self.username = username
        self.password = password
        self.host = host
        self.db_name = db_name

    def send_query(self, sql: str, *args) -> Union[list, tuple]:
        with closing(pymysql.connect(host=self.host, user=self.username, password=self.password, db=self.db_name, cursorclass=DictCursor)) as conn:
            with conn.cursor() as cursor:
                if args:
                    cursor.execute(sql, args)
                else:
                    cursor.execute(sql)

                records = cursor.fetchall()

                conn.commit()

        return records
