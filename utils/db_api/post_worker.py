from .db_core import DatabaseCore


class PostWorker(DatabaseCore):
    def get_posts(self):
        sql = "SELECT * FROM BookBotAdmin_posts WHERE isSend=0"

        response = self.send_query(sql)

        return response

    def set_is_send(self, post_id):
        sql = f"UPDATE BookBotAdmin_posts SET isSend=1 WHERE postId={post_id}"

        self.send_query(sql)
