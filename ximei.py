import json
from pprint import pprint

import requests


class XiMei:

    def __init__(self):
        self.user_id = '0ab124e7-108a-4a4e-9ce2-9a417b1bd9d3'
        self.cookies = {
            'gr_user_id': self.user_id,
        }
        self.headers = {
            'Host': 'app.hubonews.com',
            'x_client_app': 'com.tigerye.tigerobo',
            'user-agent': 'tigerobo/2.8.7 (iPhone; iOS 14.5.1; Scale/3.00)',
            'brand_product': 'Apple-iPhone11,6',
            'x_client_version': '2.8.7',
            'x_client_idfa': '',
            'device_id': '160925EB-BF27-4001-855E-E4809302AD0C',
            'x_client_channel': 'App Store',
            'x_client_platform': 'iOS',
            'x_client_country': 'CN',
            'accept-language': 'zh-Hans-CN;q=1',
            'x_client_build': '253',
            'api_authorization': 'ULBoPLKVKIiEOlxZjSPz',
            'x_client_translation_language': 'en',
            'accept': '*/*',
            'content-type': 'application/json',
            'x_client_language': 'zh',
        }

    def request(self, method='post', **kw):
        cookies_ = self.cookies.copy()
        cookies_.update(kw.get('cookies', {}))
        kw['cookies'] = cookies_
        headers_ = self.headers.copy()
        headers_.update(kw.get('headers', {}))
        kw['headers'] = headers_

        if method == 'post':
            return requests.post(**kw)
        else:
            return requests.get(**kw)

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

    def upload_comment(self, aid, comment_id):
        pass

    def upload_support(self):
        pass

    def get_help_comment(self):
        pass

    def check_support_task(self):
        pass


if __name__ == '__main__':
    ximei = XiMei()
    # ximei.support_comment(3477873, 1434552)
    ximei.get_article_comment(3477873)

