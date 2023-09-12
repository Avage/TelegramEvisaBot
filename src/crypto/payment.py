import requests
import base64
import hashlib
import hmac
from src.utils import var_extractor


def get_pay_link(currency, price, buyer_id, row_id):
    headers = {
        'Wpay-Store-Api-Key': var_extractor.get_env_var("WALLET_APY_KEY"),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    payload = {
        'amount': {
            'currencyCode': currency,
            'amount': price,
        },
        'description': 'Dubai E-Visa',
        'externalId': var_extractor.get_env_var("EXTERNAL_ID"),  # Invoice ID for payment in your bot
        'timeoutSeconds': 60 * 60 * 24,  # Invoice lifetime in seconds
        'customerTelegramUserId': buyer_id,
        'customData': row_id,
        'returnUrl': 'https://t.me/DubaiEvisaBot',
        'failReturnUrl': 'https://t.me/wallet',
    }
    try:
        response = requests.post(
            "https://pay.wallet.tg/wpay/store-api/v1/order",
            json=payload, headers=headers, timeout=10
        )
        data = response.json()

        if (response.status_code != 200) or (data['status'] not in ["ACTIVE", "PAID"]):
            return "Error: " + data
        return data['data']['payLink']
    except Exception as err:
        print('Cause: {}'.format(err))
        return "Error: " + str(err)


def is_valid(flask_request):
    encoding = 'utf-8'
    text = '.'.join([
        flask_request.method,
        flask_request.path,  # Need to use part of the address without the domain name, '/tgwallet/ipn' in our case
        flask_request.headers.get('WalletPay-Timestamp'),
        base64.b64encode(flask_request.get_data()).decode(encoding),
    ])
    signature = base64.b64encode(hmac.new(
        bytes('YOUR-API-KEY', encoding),
        msg=bytes(text, encoding),
        digestmod=hashlib.sha256
    ).digest())

    return flask_request.headers.get('Walletpay-Signature') == signature.decode(encoding)
