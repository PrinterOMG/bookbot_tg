from aiogram.types import CallbackQuery, LabeledPrice

from data.config import PAYMENTS_PROVIDER_TOKEN
from loader import dp, bot, languages_worker
from keyboards.inline.callbacks import telegram_pay_callback


@dp.callback_query_handler(telegram_pay_callback.filter())
async def tg_payment(call: CallbackQuery, callback_data: dict):
    user_id = callback_data["user_id"]
    amount = callback_data["amount"]

    text = languages_worker.get_text_on_user_language(user_id, "payTitle, payDescription")

    prices = [
        LabeledPrice(label=text["payTitle"], amount=amount * 100),
    ]
    await call.message.delete()
    await bot.send_invoice(call.from_user.id, title=text["payTitle"],
                           description=text["payDescription"].format(amount=amount),
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           prices=prices,
                           start_parameter='yesy',
                           payload='some-invoice-payload-for-our-internal-use')
