from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

DB_HOST = env.str("DB_HOST")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")

# paypal
client_id = env.str("client_id")
client_secret = env.str("client_secret")
return_url = env.str("return_url")

# yoomoney
account_id = "867452"
secret_key = "test_Bufj8lzLeS4W8ZFBRgJ7WmWunxJe_FeyvLcsZSJHAL4"

# telegram_payment
PAYMENTS_PROVIDER_TOKEN = env.str("PAYMENTS_PROVIDER_TOKEN")

PARSING_INTERVAL = 15
