from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp, languages_worker, users_worker, subscribes_worker, bot
from keyboards.inline import get_main_keyboard, get_subscribes_keyboard, get_move_keyboard, get_balance_keyboard, \
    get_cancel_keyboard, get_search_keyboard, get_fundraising_keyboard
from keyboards.inline.callbacks import navigation_callback
from states.make_question import QuestionInput


@dp.message_handler(commands=["menu"])
async def send_menu(message: Message):
    print(message)
    is_paying = users_worker.get_is_paying(message.from_user.id)

    if not is_paying:
        text = languages_worker.get_text_on_user_language(message.from_user.id, "mainMenu")

        last_menu = users_worker.get_last_menu(message.from_user.id)
        if last_menu:
            try:
                await bot.delete_message(message.from_user.id, last_menu)
            except:
                pass

        main_msg = await message.answer(text=text["mainMenu"], reply_markup=await get_main_keyboard(message.from_user.id))
        users_worker.update_last_menu(message.from_user.id, main_msg.message_id)
        await message.delete()
    else:
        text = languages_worker.get_text_on_user_language(message.from_user.id, "blockMenuInfo")
        await message.answer(text["blockMenuInfo"], show_alert=True)


@dp.callback_query_handler(navigation_callback.filter(to="main"))
async def send_main_menu(call: CallbackQuery):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.edit_text(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="subscribes"))
async def send_subscribes_menu(call: CallbackQuery):
    print(call)
    user_id = call.from_user.id
    text = languages_worker.get_text_on_user_language(user_id,
                                                      "subscribesMenu, activeSub, noSub, expiredSub, autoPayOff, autoPayOn")
    is_sub = subscribes_worker.is_user_have_active_subscribe(user_id)
    is_auto_pay = users_worker.is_auto_pay(user_id)

    if is_sub:
        subscribe_status = text["activeSub"].format(end_date=is_sub)
    else:
        is_sub_expired = subscribes_worker.is_sub_expired(user_id)
        if is_sub_expired:
            subscribe_status = text["expiredSub"].format(end_date=is_sub_expired)
        else:
            subscribe_status = text["noSub"]

    if is_auto_pay:
        subscribe_autopay_status = text["autoPayOn"]
    else:
        subscribe_autopay_status = text["autoPayOff"]

    await call.message.edit_text(text["subscribesMenu"].format(subscribe=subscribe_status, auto_pay=subscribe_autopay_status),
                                 reply_markup=await get_subscribes_keyboard(user_id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="info"))
async def send_info(call: CallbackQuery):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "info")

    await call.message.edit_text(text["info"], reply_markup=await get_move_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="balance"))
async def send_balance(call: CallbackQuery):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "balanceMenu, activeSub, noSub, expiredSub")
    is_sub = subscribes_worker.is_user_have_active_subscribe(call.from_user.id)

    if is_sub:
        subscribe_status = text["activeSub"].format(end_date=is_sub)
    else:
        is_sub_expired = subscribes_worker.is_sub_expired(call.from_user.id)
        if is_sub_expired:
            subscribe_status = text["expiredSub"].format(end_date=is_sub_expired)
        else:
            subscribe_status = text["noSub"]

    await call.message.edit_text(text["balanceMenu"].format(balance=users_worker.get_balance(call.from_user.id),
                                                            subscribe=subscribe_status),
                                 reply_markup=await get_balance_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="question"))
async def send_question_input(call: CallbackQuery, state: FSMContext):
    print(call)
    await state.update_data(main_msg=call.message)
    await QuestionInput.input.set()

    text = languages_worker.get_text_on_user_language(call.from_user.id, "questionInput")

    await call.message.edit_text(text["questionInput"], reply_markup=await get_cancel_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="archive"))
async def send_archive_search(call: CallbackQuery):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "booksArchiveMenu")

    await call.message.edit_text(text["booksArchiveMenu"], reply_markup=await get_search_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(navigation_callback.filter(to="fundraising"))
async def send_fundraising_menu(call: CallbackQuery):
    print(call)
    text = languages_worker.get_text_on_user_language(call.from_user.id, "fundraisingMenu")

    await call.message.edit_text(text["fundraisingMenu"], reply_markup=await get_fundraising_keyboard(call.from_user.id))
    await call.answer()
