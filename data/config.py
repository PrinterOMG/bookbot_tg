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
