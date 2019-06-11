import requests 

# 异常处理库
import traceback
from lxml import etree

class weibo:
    def __init__(self, user_id, cookies):
        self.user_id = user_id
        self.cookies = {
            'Cookie' : cookies
        }
        self.name = []
        self.sex = []
        self.area = []
        self.birthday = []
        self.intro = []

    def get_html(self):
        try:
            url = 'https://weibo.cn/' + self.user_id + '/info'
            html = requests.get(url= url, cookies= self.cookies).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error:',e)
            traceback.print_exc()

    def get_userinfo(self):
        selector = self.get_html()
        info_list = selector.xpath('/html/body/div[8]/text()')
        self.name.append(info_list[0][1:])
        self.sex.append(info_list[1][1:])
        self.area.append(info_list[2][1:])
        self.birthday.append(info_list[3][1:])
        self.intro.append(info_list[5][1:])

    def show(self):
        self.get_userinfo()
        print(self.name)
        print(self.sex)
        print(self.area)
        print(self.birthday)
        print(self.intro)

if __name__ == "__main__":
    cookies = 'SCF=AmMdYdAD8xDP84Xc7sEtL9WXFMVx_fALJyadgeh6G41PUqyXV4VQ_9g8MWqBiH82U_5rDZFKsxg0w-CrGae8IXg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFr0NVib_A0gaGkWL.D5ObN5JpX5K-hUgL.FozceK2R1K2cSKe2dJLoI0qLxKqLBKBLBo5LxK-LB-BL1K5LxKqLBo2L1h2LxKqL1hnL1K2LxKML1hnLBo2LxK-L1KqL1-Bt; _T_WM=52050499844; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; MLOGIN=0; SUB=_2A25x-7enDeRhGeRI6lMZ-S_Kzj-IHXVTB9nvrDV6PUJbkdBeLVrMkW1NUtpT2XBkCAb9xERrHGGHTjLUkQZBtos0; SUHB=08J6kbAgs1djdm; SSOLoginState=1560266743'
    weibo = weibo('2611891653',cookies)
    weibo.show()


