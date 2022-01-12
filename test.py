from loader import languages_worker, users_worker, referral_worker, promo_worker
from utils.csv_worker import search


# print(promo_worker.get_user_discount(688305373))


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result[:-1]


print(search("books_russian.csv", "genre", 123))

