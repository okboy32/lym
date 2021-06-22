import datetime
import json
import random
import time
from pprint import pprint

import requests


class XiMei:

    def __init__(self, user_id, headers):
        # self.user_id = '0ab124e7-108a-4a4e-9ce2-9a417b1bd9d3'
        # self.user_id = 'd311fa0b-540a-42d9-97da-6af264ab75d8'
        self.user_id = user_id
        self.cookies = {
            'gr_user_id': self.user_id,
        }
        self.headers = headers
        # self.headers = {
        #     'Host': 'app.hubonews.com',
        #     'x_client_app': 'com.tigerye.tigerobo',
        #     'user-agent': 'tigerobo/2.8.7 (iPhone; iOS 14.5.1; Scale/3.00)',
        #     'brand_product': 'Apple-iPhone11,6',
        #     'x_client_version': '2.8.7',
        #     'x_client_idfa': '',
        #     'device_id': '70A73029-87AC-427A-BBD9-15EF443BED30',
        #     'x_client_channel': 'App Store',
        #     'x_client_platform': 'iOS',
        #     'x_client_country': 'CN',
        #     'accept-language': 'zh-Hans-CN;q=1',
        #     'x_client_build': '253',
        #     'api_authorization': 'idyyPnwEmfw0BGFXkuZr',
        #     'x_client_translation_language': 'en',
        #     'accept': '*/*',
        #     'content-type': 'application/json',
        #     'x_client_language': 'zh',
        # }
        self.task_info = {}

    def request(self, method='post', **kw):
        cookies_ = self.cookies.copy()
        cookies_.update(kw.get('cookies', {}))
        kw['cookies'] = cookies_
        headers_ = self.headers.copy()
        headers_.update(kw.get('headers', {}))
        kw['headers'] = headers_

        if method == 'post':
            res = requests.post(**kw)
        else:
            res = requests.get(**kw)

        data = res.json()
        if data['code'] == 0:
            return data['data']
        else:
            raise Exception(f'{data["code"]} {e}')

    def random_wait(self, a, b):
        r = a + random.random() * (b - a)
        time.sleep(r)
        return r

    @staticmethod
    def print(*args):
        print(*args, flush=True)

    def get_app_config(self):
        res = self.request(url='https://app.hubonews.com/config', data='{}')
        pprint(res.json())

    def get_user_info(self):
        res = self.request(url='https://app.hubonews.com/v1/user/info')
        pprint(res.json())

    def get_articles(self, page=1, limit=20):

        data = '{"limit":' + str(limit) + ',"page":' + str(page) + '}'
        response = self.request(url='https://app.hubonews.com/v4/articles/list', data=data)
        pprint(response.json())

    def article_detail(self, aid):

        data = '{"id":' + str(aid) + ',"batchNumber":0}'

        response = self.request(url='https://app.hubonews.com/v1/article/content', data=data)
        pprint(response.json())

    def get_article_comment(self, aid):

        data = '{"limit":20,"nextId":0,"commentId":0,"type":0,"articleId":' + str(aid) + '}'

        response = self.request(url='https://app.hubonews.com/v2/comment/getComments', data=data)
        pprint(response.json())

    def comment(self, aid):

        data = {
            'replyCommentId': 0,
            'content': '123',
            'type': 0,
            'articleId': aid,
        }
        # data = json.dumps(data)

        response = self.request(url='https://app.hubonews.com/v2/comment/createByArticleid', json=data)
        pprint(response.json())

    def support_comment(self, aid, comment_id):

        data = {
            'commentId': comment_id,
            'articleId': aid,
            'type': 0,
        }
        response = self.request(url='https://app.hubonews.com/v2/comment/supportByCommentid', json=data)
        pprint(response.json())

    def get_task_info(self):

        data = self.request(url='https://app.hubonews.com/v2/activity/tasks', method='get')
        self.task_info = data

    def get_qiandao_info(self, month=''):

        params = {
            'month': month
        }

        data = self.request(method='get', url='https://app.hubonews.com/v1/activity/signin/record', params=params)
        pprint(data)

    def _qiandao(self):

        data = {}

        data = self.request(url='https://app.hubonews.com/v1/activity/signin', json=data)
        pprint(data)

    def qiandao(self):
        self.random_wait(1, 2)
        self.get_qiandao_info()
        self.random_wait(1, 2)
        self._qiandao()
        self.get_qiandao_info(month=datetime.datetime.now().strftime('%Y%m'))

    def upload_comment(self, aid, comment_id):
        pass

    def upload_support(self):
        pass

    def get_help_comment(self):
        pass

    def check_support_task(self):
        pass

    def run(self):
        self.get_task_info()
        for task in self.task_info['tasks']:
            if task['desc'] == '签到任务':
                for item in task['list']:
                    if item['type'] == 127:
                        if item['completed_times'] == 0:
                            self.qiandao()
                            self.print('签到成功')
                        else:
                            self.print('已签到')

    @classmethod
    def create(cls, user_id, headers):
        return cls(user_id=user_id, headers=headers)


if __name__ == '__main__':
    # ximei = XiMei()
    # ximei.support_comment(3477873, 1434552)
    accounts = [{
        'user_id': '0ab124e7-108a-4a4e-9ce2-9a417b1bd9d3',
        'headers': '',
    }, {
        'user_id': 'd311fa0b-540a-42d9-97da-6af264ab75d8',
        'headers': '',
    }]
    for account in accounts:
        ximei = XiMei.create(**account)
        ximei.run()
