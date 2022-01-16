from .db_core import DatabaseCore


class QuestionsWorker(DatabaseCore):
    def make_question(self, user_id, question):
        sql = f"INSERT INTO BookBotAdmin_questions(fromUser_id, text, isAnswered) VALUES({user_id}, '{question}', 0)"

        self.send_query(sql)

    def get_answered_questions(self):
        sql = "SELECT * FROM BookBotAdmin_questions WHERE isAnswered=0 and answer!=''"

        response = self.send_query(sql)

        return response

    def set_is_answered_true(self, question_id):
        sql = f"UPDATE BookBotAdmin_questions SET isAnswered=1 WHERE questionId={question_id}"

        self.send_query(sql)
