import datetime

from aiogram.types import InputFile

from keyboards.inline import get_close_keyboard
from loader import questions_worker, bot, languages_worker, post_worker, users_worker, filter_worker


async def update():
    answered_questions = questions_worker.get_answered_questions()
    for question in answered_questions:
        text = languages_worker.get_text_on_user_language(question["fromUser_id"], "answerText")
        keyboard = await get_close_keyboard(question["fromUser_id"], 0)
        await bot.send_message(question["fromUser_id"],
                               text=text["answerText"].format(question=question["text"], answer=question["answer"]),
                               reply_markup=keyboard)
        questions_worker.set_is_answered_true(question["questionId"])

    posts = post_worker.get_posts()
    for post in posts:
        print(post)
        print(post["sendDate"])

        # cur_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # cur_date = datetime.datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
        # if post["sendDate"] and (post["sendDate"] > cur_date):
        #     continue

        if post["filter_id"]:
            print("with_filter")
            filters = filter_worker.get_filter(post["filter_id"])
            users = users_worker.get_filtered_users(filters)
            if users:
                for user_id in users:
                    keyboard = await get_close_keyboard(user_id, 0)
                    try:
                        if post["photo"]:
                            await bot.send_photo(user_id, InputFile(r"../admin/" + post["photo"]),
                                                 caption=post["title"] + "\n" + post["text"],
                                                 reply_markup=keyboard)
                        else:
                            await bot.send_message(user_id, text=post["title"] + "\n" + post["text"],
                                                   reply_markup=keyboard)
                    except Exception as e:
                        print('post send error', e)
                post_worker.set_is_send(post["postId"])
            else:
                print("no users")
                post_worker.set_is_send(post["postId"])
        else:
            print("no_filter")
            users = users_worker.get_all_users()
            if users:
                for user in users:
                    keyboard = await get_close_keyboard(user["userId"], 0)
                    try:
                        if post["photo"]:
                            await bot.send_photo(user["userId"], InputFile(r"../admin/" + post["photo"]),
                                                 caption=post["title"] + "\n" + post["text"],
                                                 reply_markup=keyboard)
                        else:
                            await bot.send_message(user["userId"], text=post["title"] + "\n" + post["text"],
                                                   reply_markup=keyboard)
                    except Exception as e:
                        print('post send error', e)
                post_worker.set_is_send(post["postId"])
