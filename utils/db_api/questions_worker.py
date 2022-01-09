from .db_core import DatabaseCore


class QuestionsWorker(DatabaseCore):
    def make_question(self, user_id, question):
        sql = f"INSERT INTO BookBotAdmin_questions(fromUser_id, text, isAnswered) VALUES({user_id}, '{question}', 0)"

        self.send_query(sql)
