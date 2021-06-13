# python 3.8
import os
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

DD_TOKEN = os.getenv('DD_BOT_TOKEN')
DD_SECRET = os.getenv('DD_BOT_SECRET')


def send_dd(title, index, nickname, text):
    text = f'{title}\n\t账号{index}\t{nickname}\n\t{text}'
    print('发送通知\n' + text)
    timestamp = str(round(time.time() * 1000))
    secret = DD_SECRET
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # res = requests.post(
    #     f'https://oapi.dingtalk.com/robot/send?access_token={DD_TOKEN}&timestamp={timestamp}&sign={sign}',
    #     headers={'Content-Type': 'application/json'}, json={"text": {
    #         "content": text
    #     }, "msgtype": "text"})
    print('发送通知\t' + text)
    # print(res.text)
