import requests
import os

requests.packages.urllib3.disable_warnings()
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


# 掘金签到
class board(object):
    def __init__(self):
        # 登陆需要图像验证 麻烦了
        self.cookies = os.environ['cookies']

    def checkin(self):
        headers = {
            'User-Agent': ua,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': self.cookies
        }
        response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', None, headers=headers, verify=False)
        print(response.text)


if __name__ == '__main__':
    run = board()
    run.checkin()
