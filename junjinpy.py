import requests
import os
import json

requests.packages.urllib3.disable_warnings()
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


# 掘金签到
class board(object):
    def __init__(self):
        # 登陆需要图像验证 麻烦了
        self.cookies = os.environ['cookies']

        self.dd_token = os.environ['dd_token']
        
    def checkin(self):
        if self.cookies == '':
            print('未设置cookies')
            return
        headers = {
            'User-Agent': ua,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': self.cookies
        }
        response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', None, headers=headers, verify=False)
        print(response.text)
        # 发送钉钉通知
        if self.dd_token:
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.dd_token
            data = {
                "msgtype": "text",
                "text": {
                    "content": "gui => juejin panel " + response.text
                }
            }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    run = board()
    run.checkin()
