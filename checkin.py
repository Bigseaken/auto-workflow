import requests
import os
import json
import time

requests.packages.urllib3.disable_warnings()
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


class SspanelQd(object):
    def __init__(self):
        # 机场地址

        self.base_url = os.environ['web'].split(',')
        # 登录信息

        self.email = os.environ['user'].split(',')

        self.password = os.environ['pwd'].split(',')

        self.dd_token = os.environ['dd_token']

    def checkin(self):

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        msgall = '签到成功'
        try:
            for i in range(len(self.base_url)):
                session = requests.session()

                login_url = self.base_url[i] + '/auth/login'
                headers = {
                    'User-Agent': ua,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                }

                post_data = 'email=' + self.email[i] + '&passwd=' + self.password[i]
                post_data = post_data.encode()
                response = session.post(login_url, post_data, headers=headers, verify=False)
                login_result = json.loads(response.text)
                if login_result.get('ret') == 0:
                    print(self.base_url[i] + ' ' + '登陆失败')
                    continue

                headers = {
                    'User-Agent': ua,
                    'Referer': self.base_url[i] + '/user'
                }

                response = session.post(self.base_url[i] + '/user/checkin', headers=headers, verify=False)
                msg = (response.json()).get('msg')
                print(self.base_url[i] + ' \n' + msg)
                # 发送钉钉通知
                if self.dd_token:
                    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.dd_token
                    data = {
                        "msgtype": "text",
                        "text": {
                            "content": "gui =>  " + self.base_url[i] + msg
                        }
                    }
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    requests.post(url, data=json.dumps(data), headers=headers)

        except Exception as e:
            msgall = '签到失败'
            print(e)
        return msgall

    def main(self):
        self.checkin()


if __name__ == '__main__':
    run = SspanelQd()
    run.main()
