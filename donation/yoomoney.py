from django.conf import settings
from urllib.parse import urlencode

YOOMONEY_URL = "https://yoomoney.ru/quickpay/confirm.xml"


def build_payment_url(donation):
    params = {
        "receiver": settings.YOOMONEY_WALLET,
        "quickpay-form": "donate",
        "targets": "Поддержка проекта Class Reunion",
        "paymentType": "AC",
        "sum": donation.amount,
        "label": donation.id,
        "successURL": settings.YOOMONEY_SUCCESS_URL,
    }

    return f"{YOOMONEY_URL}?{urlencode(params)}"