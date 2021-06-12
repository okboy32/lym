import datetime
import random
import threading
import time

import requests
from cookies import save_cookies as sc, get_cookies as gc
from notify import send_dd


class Fhxz:
    token = '1040314_1623436650_ad2826d3ba35f81fa9aeb0ce789cc736'
    headers = {
        'Host': 'sunnytown.hyskgame.com',
        'accept': '*/*',
        'content-type': 'application/octet-stream',
        'x-unity-version': '2019.2.9f1',
        'user-agent': 'fuhaoxiaozhen/23 CFNetwork/1237 Darwin/20.4.0',
        'accept-language': 'zh-cn',
    }

    def __init__(self):
        cookies = self.get_cookies().get('token')
        Fhxz.token = cookies if cookies else self.token
        self.frame_list = []
        self.user_info = {}
        self.have_tixian = False

        self.get_token()

        self.enter_game()
        self.gcfun()
        self.pet_house()
        self.invitation()
        self.daily()
        self.user_ads_info()

        t1 = threading.Thread(target=self.sub_thread)
        t1.start()

    @staticmethod
    def random_wait(a, b):
        r = random.randint(a, b)
        time.sleep(r)
        return r

    @staticmethod
    def get_cookies():
        return gc('富豪小镇')

    @staticmethod
    def save_cookies(data):
        sc('富豪小镇', data)

    @staticmethod
    def get_data(res):
        try:
            if res.status_code == 200:
                data = res.json()[0]
                return data['data']
        except Exception as e:
            print(res.text, e)

    def get_token(self):
        params = (
            ('accessToken', ''),
            ('msgtype', 'account_signInAccessToken'),
        )
        data = '[{"type":"account_signInAccessToken","data":{"accessToken":"' + self.token + '"}}]'
        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = self.get_data(response)
        token = data['accessToken']
        self.token = token
        self.save_cookies({'token': token})

    def sub_thread(self):
        while True:
            self.gpv()
            time.sleep(10)
            self.heartbeat()
            time.sleep(20)
            self.keep_alive()
            time.sleep(30)

    def keep_alive(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'system_keep_alive'),
        )

        data = '[{"type":"system_keep_alive","data":{"clientTimeMillis":"' + str(
            int(time.time())) + '","pingTimeMillis":"100"}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        # print('keep_alive:', response.text)

    def heartbeat(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'stealingVege_checkHeartBeat'),
        )

        data = '[{"type":"stealingVege_checkHeartBeat","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        # print('heartbeat: ', response.text)

    def gpv(self):
        params = (
            ('accessToken', self.token),
            ('msgtype', 'system_getGpvGameOptions'),
        )

        data = '[{"type":"system_getGpvGameOptions","data":{"gameId":"sunnytown-cn","runtimePlatform":"ios","versionName":"1.0.9"}}]'
        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        # print('gpv: ', response.text)

    def enter_game(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'user_enterGame'),
        )

        data = '[{"type":"user_enterGame","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = response.json()
        for item in data:
            if item['type'] == 'farmland_getFarmlandList':
                frame_list = item['data']['farmlandList']
                self.frame_list = frame_list

            if item['type'] == 'user_getUserInfo':
                user_info = item['data']['userInfo']
                self.user_info = user_info
        # print('enter_game: ', data)

    def gcfun(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'gfunc_getGfuncInfo'),
        )

        data = '[{"type":"gfunc_getGfuncInfo","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        # print('gcfun: ', response.text)

    def invitation(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'invitation_getInvitationBag'),
        )

        data = '[{"type":"invitation_getInvitationBag","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = self.get_data(response)
        # print('invitation', data)

    def pet_house(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'pet_getPetHouse'),
        )

        data = '[{"type":"pet_getPetHouse","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = self.get_data(response)
        # print('pet_house', data)

    def daily(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'dailyQuest_getQuestList'),
        )

        data = '[{"type":"dailyQuest_getQuestList","data":{"questType":1}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = self.get_data(response)
        # print('daily', data)

    def user_ads_info(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'userAdsInfo_getAdsInfo'),
        )

        data = '[{"type":"userAdsInfo_getAdsInfo","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = self.get_data(response)
        print('user_ads_info', data)
        time.sleep(5)

    def repair(self, frame_id):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'farmland_repair'),
        )

        data = '[{"type":"farmland_repair","data":{"farmlandDefId":' + str(frame_id) + '}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        for item in response.json():
            if item.get('type') == 'farmland_repair':
                data = item['data']

        print(f'地块{frame_id}修理成功')
        self.random_wait(30, 50)

    def collect(self, frame_id):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'farmland_harvest'),
        )

        data = '[{"type":"farmland_harvest","data":{"farmlandDefId":' + str(frame_id) + '}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        for item in response.json():
            if item.get('type') == 'farmland_harvest':
                data = item['data']

        print(f'地块{frame_id}收获成功')

    def plant(self, frame_id):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'farmland_plant'),
        )

        data = '[{"type":"farmland_plant","data":{"farmlandDefId": ' + str(frame_id) + ',"priceType":2001}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)

        for item in response.json():
            if item.get('type') == 'farmland_plant':
                data = item['data']

        print(f'地块{frame_id}种植成功')
        self.random_wait(2, 5)

    def get_frame_list(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'farmland_getFarmlandList'),
        )

        data = '[{"type":"farmland_getFarmlandList","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)
        data = response.json()
        for item in data:
            if item['type'] == 'farmland_getFarmlandList':
                frame_list = item['data']['farmlandList']
                self.frame_list = frame_list

    def check_market(self):

        params = (
            ('accessToken', self.token),
            ('msgtype', 'market_getItemList'),
        )

        data = '[{"type":"market_getItemList","data":{}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)

        data = response.json()
        for item in data:
            if item['type'] == 'market_getItemList':
                data = item['data']
                for market_item in data['marketItemList']:
                    item_id = market_item['itemDefId']
                    title = market_item['title']
                    amount = market_item['cashAmount']
                    if market_item['progress'] >= market_item['targetNumber']:
                        print(f'{item_id} {title} 可提现{amount}元')
                        if amount < 1:
                            self.tixian(item_id)

    def tixian(self, item_id):
        self.random_wait(1, 3)
        params = (
            ('accessToken', self.token),
            ('msgtype', 'market_exchange'),
        )

        data = '[{"type":"market_exchange","data":{"itemDefId":' + item_id + '}}]'

        response = requests.post('https://sunnytown.hyskgame.com/api/messages', headers=self.headers, params=params,
                                 data=data)

        data = response.json()
        for item in data:
            if item['type'] == 'market_exchange':
                data = item['data']['marketItem']
                status = data['stateCode']
                amount = data['cashAmount']
                no_audit = data['noAudit']
                notify_str = f'{amount}元提现成功 status: {status} {"无需审核" if no_audit else "待审核"}'
                send_dd("富豪小镇", 1, self.user_info["nickname"], notify_str)
                self.have_tixian = True
                self.gcfun()
                self.check_market()
            elif item['type'] == 'system_error':
                message = item['data']['message']
                notify_str = f'提现失败 {message}'
                send_dd("富豪小镇", 1, self.user_info["nickname"], notify_str)
                self.have_tixian = True




    def handle_frame(self):
        # troubleStateCode 1 需维修
        for item in self.frame_list:
            status_code = item.get('stateCode')
            frame_id = item.get('farmlandDefId')
            if status_code == 2:
                self.plant(frame_id)
            elif status_code == 5:
                self.repair(frame_id)
            elif status_code == 6:
                self.collect(frame_id)
                self.plant(frame_id)

    def run(self):
        self.handle_frame()
        self.get_frame_list()
        self.handle_frame()
        if not self.have_tixian:
            self.check_market()


if __name__ == '__main__':
    for i in range(30):
        start_time = time.time()
        fhxz = Fhxz()
        fhxz.run()

        random_sleep = random.randint(120, 1500)
        print(f'等待{random_sleep}秒')
        time.sleep(random_sleep)
