from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from loader import questions_worker, bot, languages_worker, post_worker, users_worker, filter_worker


async def update():
    answered_questions = questions_worker.get_answered_questions()
    for question in answered_questions:
        text = languages_worker.get_text_on_user_language(question["fromUser_id"], "answerText, closeButton")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text["closeButton"], callback_data="close")
            ]
        ])
        await bot.send_message(question["fromUser_id"], text=text["answerText"].format(question=question["text"], answer=question["answer"]), reply_markup=keyboard)
        questions_worker.set_is_answered_true(question["questionId"])

    posts = post_worker.get_posts()
    for post in posts:
        filters = filter_worker.get_filter(post["filter_id"])
        users = users_worker.get_filtered_users(filters)
        if users:
            text = languages_worker.get_text(filters["languageId_id"], "closeButton")
            for user_id in users:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text["closeButton"], callback_data="close")
                    ]
                ])
                if post["photo"]:
                    await bot.send_photo(user_id, InputFile(r"../admin/" + post["photo"]), caption=post["title"] + "\n" + post["text"],
                                         reply_markup=keyboard)
                else:
                    await bot.send_message(user_id, text=post["title"] + "\n" + post["text"], reply_markup=keyboard)
            post_worker.set_is_send(post["postId"])

