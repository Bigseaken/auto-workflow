import requests
import os
import json

requests.packages.urllib3.disable_warnings()
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


# 掘金签到
class board(object):
    def __init__(self):
        # 登陆需要图像验证 麻烦了
        self.cookies = os.environ['COOKIES']

        self.dd_token = os.environ['dd_token']

    def checkin(self):
        if self.cookies == '':
            print('未设置cookies')
            return
        cookie = self.cookies.split(',')
        index = 0
        for c in cookie:
            index += 1
            headers = {
                'User-Agent': ua,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': c
            }
            with requests.post('https://api.juejin.cn/growth_api/v1/check_in', data=None, headers=headers,
                               verify=False) as response:
                print(response.text)
                juejin_result = json.loads(response.text)
                if juejin_result['err_msg'] == 'success':
                    push_msg = '掘金账号' + str(c + 1) + '签到成功，获取砖石：' \
                               + str(juejin_result['data']['incr_point']) \
                               + '当前砖石总数：' + str(juejin_result['data']['sum_point'])
                    # 免费抽奖一次

                else:
                    push_msg = '掘金签到失败'

            with requests.post('https://api.juejin.cn/growth_api/v1/lottery/draw', data=None, headers=headers,
                               verify=False) as response:
                print(response.text)
                lottery_result = json.loads(response.text)
                push_msg += ' 账号' + str(index) + '免费抽奖：' + lottery_result['data']['lottery_name']
            # 发送钉钉通知
            if self.dd_token:
                url = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.dd_token
                data = {
                    "msgtype": "text",
                    "text": {
                        "content": "gui => juejin panel " + push_msg
                    }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                with requests.post(url, data=json.dumps(data), headers=headers) as r:
                    print(r.text)


if __name__ == '__main__':
    run = board()
    run.checkin()
