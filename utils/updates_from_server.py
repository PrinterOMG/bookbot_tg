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
        bot.send_message(question["fromUser_id"], text["answerText"], reply_markup=keyboard)
        questions_worker.set_is_answered_true(question["questionId"])

    posts = post_worker.get_posts()
    subs = users_worker.get_all_subs()
    for post in posts:
        language_id = filter_worker.get_filter(post["filter_id"])["languageId_id"]
        for sub in subs:
            if sub["languageId_id"] == language_id:
                text = languages_worker.get_text_on_user_language(sub["userId"], "closeButton")
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text["closeButton"], callback_data="close")
                    ]
                ])
                if post["photo"]:
                    await bot.send_photo(sub["userId"], InputFile(r"../admin/" + post["photo"]), caption=post["text"],
                                         reply_markup=keyboard)
                else:
                    await bot.send_message(sub["userId"], text=post["text"], reply_markup=keyboard)

