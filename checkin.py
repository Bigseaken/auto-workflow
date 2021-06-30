import requests
import re
import os

requests.packages.urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self):
        # 机场地址

        self.base_url = os.environ['web']
        # 登录信息

        self.email = os.environ['user']

        self.password = os.environ['pwd']

    def checkin(self):
        msgall = '签到成功'
        try:

            session = requests.session()

            login_url = self.base_url + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = 'email='+self.email+'&passwd='+self.password
            post_data = post_data.encode()
            response = session.post(login_url, post_data, headers=headers, verify=False)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': self.base_url + '/user'
            }

            response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
            msg = (response.json()).get('msg')

            msgall = msgall + self.base_url + '\n\n' + msg + '\n\n'
            print(msg)

            # info_url = self.base_url[i] + '/user'
            # response = session.get(info_url, verify=False)
        except Exception as e:
            msgall = '签到失败'
            print(e)
        return msgall

    def main(self):
        msg = self.checkin()
        with open('log.txt', 'w') as f:
            f.write(msg)


if __name__ == '__main__':
    run = SspanelQd()
    run.main()
