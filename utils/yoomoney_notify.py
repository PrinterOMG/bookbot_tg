from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from flask import Flask, request, Response

from yoomoney_helper import *

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def my_webhook_handler():
    # Извлечение JSON объекта из тела запроса
    event_json = request.json()
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        else:
            # Обработка ошибок
            return Response(status=400)  # Сообщаем кассе об ошибке

        Configuration.configure("867452", "test_Bufj8lzLeS4W8ZFBRgJ7WmWunxJe_FeyvLcsZSJHAL4")
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # logic
        else:
            return Response(status=400)

    except Exception:
        return Response(status=400)

    return Response(status=200)
