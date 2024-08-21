import time
import hmac
import hashlib
from decouple import config



SUMSUB_SECRET_KEY = config('SUMSUB_SECRET_KEY')
SUMSUB_APP_TOKEN = config('SUMSUB_APP_TOKEN')

def signed_payload(request):
    now = int(time.time())
    headers = {
        'Content-Type': 'application/json',
        'Content-Encoding': 'utf-8'
    }

    signed_request = request.prepare()

    method = request.method.upper()
    path_url = signed_request.path_url  # includes encoded query params
    
    # could be None so we use an empty **byte** string here
    body = b'' if signed_request.body is None else signed_request.body
    if type(body) == str:
        body = body.encode('utf-8')
    payload_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
    
    # hmac needs bytes
    signature = hmac.new(
        SUMSUB_SECRET_KEY.encode('utf-8'),
        payload_to_sign,
        digestmod=hashlib.sha256
    )

    signed_request.headers['X-App-Token'] = SUMSUB_APP_TOKEN
    signed_request.headers['X-App-Access-Ts'] = str(now)
    signed_request.headers['X-App-Access-Sig'] = signature.hexdigest()

    return signed_request


