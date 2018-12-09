import requests
from lxml import etree
import re
import random


class SpiderV2:

    def __init__(self):
        self.base_url = 'https://www.v2ex.com/signin'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
            'cookie': '__guid=96143386.3629491029809490400.1529738874018.4578; _ga=GA1.2.1933997822.1529738878; PB3_SESSION="2|1:0|10:1544013681|11:PB3_SESSION|40:djJleDoyMTguMjQxLjI0My4xOTg6NjkwMzk2NDk=|13c94b8e1eedda13b92536f39753f6bec6c017bacd5bb55b41c5485be280f8b7"; _gid=GA1.2.929363471.1544109734; V2EX_TAB="2|1:0|10:1544234160|8:V2EX_TAB|8:dGVjaA==|f51db0e4c5c3cf47dd70f2a9a10fd3ad3742cc113fc0157a9f52fc709afb8401"; V2EX_REFERRER="2|1:0|10:1544279587|13:V2EX_REFERRER|12:bGRtc29mdA==|236ecc63e2fcbe0c5dc1253d179f0d3d4111fd2b66bd6c6261db13c7316e62b4"; V2EX_LANG=zhcn; _gat=1; monitor_count=71'
        }

    def set_proxy(self):
        """
        设置代理ip
        """
        proxy = [
            {'https': 'https://139.129.207.72:808'},
            # {'https': 'https://117.114.149.66:53281'},
            # {'https': 'https://222.223.115.30:51618'}
        ]
        p = random.choice(proxy)
        return p

    def send_request(self):
        proxies = self.set_proxy()
        response = requests.get(self.base_url, headers=self.headers, proxies=proxies)
        data = response.content.decode('utf-8')
        return data

    def get_all(self, res_data):
        html_str = etree.HTML(res_data)
        temp = []
        try:
            tr_all = html_str.xpath('//*[@id="Main"]/div[2]/div[@class="cell"]/form[@action="/signin"]//tr')
            user_name_key = tr_all[0].xpath('./td[2]/input/@name')[0]
            password_key = tr_all[1].xpath('./td[2]/input/@name')[0]
            verify_code_key = tr_all[2].xpath('./td[2]/input/@name')[0]
            once_str = tr_all[2].xpath('./td[2]/div/@style')[0]
            once_t = once_str
            once = re.search(r'\d+', once_t).group()
            temp = [user_name_key, password_key, verify_code_key, once]
        except Exception as e:
            print('登录次数太多,你的ip已被限制')
            exit()
        return temp

    def save_image(self, once):
        """
        请求图片
        :return:
        """
        print(once)
        image_url = 'https://www.v2ex.com/_captcha?once={}'.format(once)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
            'referer': 'https://www.v2ex.com/signin',
            'cookie': '__guid=96143386.3629491029809490400.1529738874018.4578; _ga=GA1.2.1933997822.1529738878; PB3_SESSION="2|1:0|10:1544013681|11:PB3_SESSION|40:djJleDoyMTguMjQxLjI0My4xOTg6NjkwMzk2NDk=|13c94b8e1eedda13b92536f39753f6bec6c017bacd5bb55b41c5485be280f8b7"; _gid=GA1.2.929363471.1544109734; V2EX_TAB="2|1:0|10:1544234160|8:V2EX_TAB|8:dGVjaA==|f51db0e4c5c3cf47dd70f2a9a10fd3ad3742cc113fc0157a9f52fc709afb8401"; V2EX_REFERRER="2|1:0|10:1544279587|13:V2EX_REFERRER|12:bGRtc29mdA==|236ecc63e2fcbe0c5dc1253d179f0d3d4111fd2b66bd6c6261db13c7316e62b4"; V2EX_LANG=zhcn; _gat=1; monitor_count=71',
        }
        image = requests.get(url=image_url, headers=headers).content

        with open('verify_image.jpg', 'wb') as f:
            f.write(image)
        print('保存验证码图片成功。。。')

    def login(self, user_name=None, password=None):
        """
        登录
        """
        # 发送请求，拼接参数，登录
        res_data = self.send_request()
        temp_key = self.get_all(res_data)

        self.save_image(temp_key[3])
        # 获取验证码
        verify_code = input('请输入图片验证码:')
        result = {
            temp_key[0]: user_name,
            temp_key[1]: password,
            temp_key[2]: verify_code,
            'once': temp_key[3],
            'next': '/'
        }
        self.headers['referer'] = 'https://www.v2ex.com/'
        proxies = self.set_proxy()
        response = requests.post(url=self.base_url, headers=self.headers, data=result, proxies=proxies)
        print('\n')
        html = etree.HTML(response.content.decode('utf-8'))
        try:
            user_neike = html.xpath('//*[@id="Rightbar"]/div[2]/div[1]/table[1]/tbody/tr/td[3]/span/a')
            print('用户登录成功，用户昵称为：{}'.format(user_neike))
        except Exception as e:
            print('用户登录失败')
        print('\n')
        print(response.text)

    def save_file(self, data):
        with open('v2.html', 'w', encoding='utf-8') as f:
            f.write(data)

    def run(self, user_name, password):
        # data = self.send_request()
        # self.save_file(data)
        self.login(user_name, password)
        print('运行结束')


if __name__ == '__main__':
    user_name = 'your name'
    password = 'your id'
    SpiderV2().run(user_name, password)

