from .db_core import DatabaseCore


class PostWorker(DatabaseCore):
    def get_posts(self):
        print(self.send_query("SELECT NOW()")[0]["NOW()"])

        # sql = "SELECT * FROM BookBotAdmin_posts WHERE isSend=0 " \
        #       "AND NOW() >= STR_TO_DATE(sendDate, '%Y-%m-%d %H:%i:%s')"
        sql = "SELECT * FROM BookBotAdmin_posts WHERE isSend=0 " \
              "AND NOW() >= DATE_ADD(sendDate, INTERVAL 3 HOUR)"

        response = self.send_query(sql)

        return response

    def set_is_send(self, post_id):
        sql = f"UPDATE BookBotAdmin_posts SET isSend=1 WHERE postId={post_id}"

        self.send_query(sql)
