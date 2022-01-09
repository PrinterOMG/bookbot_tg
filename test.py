from loader import languages_worker, users_worker, referral_worker, promo_worker


# print(promo_worker.get_user_discount(688305373))


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result[:-1]


print(strike("100"))

