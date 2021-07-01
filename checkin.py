import requests
import re
import os
import json

requests.packages.urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self):
        # 机场地址
        web_list = os.environ['web']
        self.base_url = web_list.split(',')
        # 登录信息
        user_list = os.environ['user']
        self.email = user_list.split(',')
        pwd_list = os.environ['pwd']
        self.password = pwd_list.split(',')

    def checkin(self):
        msgall = '签到成功'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        try:
            for i in range(len(self.base_url)):

                session = requests.session()
                login_url = self.base_url[i] + '/auth/login'
                post_data = 'email='+self.email[i]+'&passwd='+self.password[i]
                post_data = post_data.encode()
                response = session.post(login_url, post_data, headers=headers, verify=False)
                ret = json.dumps(response.text).get('ret')
                if ret == 1:
                    print(self.base_url[i] + 'login result=====>登陆失败')
                    continue
                else:
                    print(self.base_url[i] + 'login result=====>登陆成功')

                referer_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                    'Referer': self.base_url[i] + '/user'
                }

                response = session.post(self.base_url[i] + '/user/checkin', headers=referer_headers, verify=False)
                msg = (response.json()).get('msg')
                print(msg)

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