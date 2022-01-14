from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from data.config import client_id, client_secret, return_url

from paypalcheckoutsdk.orders import OrdersCaptureRequest, OrdersGetRequest, OrdersCreateRequest

environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)


class SubscriptionRequest:
    """
    Создает подписку
    """

    def __init__(self):
        self.verb = "POST"
        self.path = "/v1/billing/subscriptions"
        self.headers = {"Content-Type": "application/json"}
        self.body = None

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order):
        self.body = order
        return self


class SubscriptionActivate:
    """
    Проверяет статус подписки
    """

    def __init__(self, order_id):
        self.verb = "GET"
        self.path = f"/v1/billing/subscriptions/{order_id}"
        self.headers = {"Content-Type": "application/json"}
        self.body = None

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order):
        self.body = order
        return self


def create_sub_paypal_payment(plan_id: str):
    request = SubscriptionRequest()
    request.request_body({
          "plan_id": plan_id,
          "application_context": {
            "brand_name": "book bot",
            "user_action": "SUBSCRIBE_NOW",
            "return_url": return_url,
            "cancel_url": return_url
          }
        })

    response = client.execute(request)
    print(response.result.links[0].href)
    print(response.result.id)
    return response.result.links[0].href, response.result.id


def check_paypal_sub(order_id: str) -> str:
    request = SubscriptionActivate(order_id)
    response = client.execute(request)
    return response.result.status


def capture_onetime_order(order_id: str):
    request = OrdersCaptureRequest(order_id)

    print('Capturing Order...')
    response = client.execute(request)
    if response.status_code == 201:
        print('Status: ', response.result.status)
        return response.result.status


def create_payment_paypal(amount: int):
    request = OrdersCreateRequest()

    request.prefer('return=representation')

    request.request_body(
        {
            "intent": "CAPTURE",
            "application_context": {
                "return_url": return_url,
                "cancel_url": return_url,
                "brand_name": "book bot",
                "landing_page": "BILLING",
                "user_action": "CONTINUE"
            },
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "RUB",
                        "value": str(amount)
                    }
                }
            ]
        }
    )

    try:
        response = client.execute(request)
        print(response.result)
        print('Order With Complete Payload:')
        print('Order ID:', response.result.id)
        print(response.result.links[1].href)
        return response.result.links[1].href, response.result.id
    except IOError as ioe:
        print(ioe)


def check_paypal_order(order_id: str) -> str:
    request = OrdersGetRequest(order_id)

    response = client.execute(request)

    return response.result.status
