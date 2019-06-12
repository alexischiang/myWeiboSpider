import requests 
from urllib.parse import urlencode

# 异常处理库
import traceback
from lxml import etree

class weibo:
    def __init__(self, user_id, cookies, filter):
        """初始化"""
        self.user_id = user_id
        self.cookies = {
            'Cookie' : cookies
        }
        self.name = []
        self.sex = []
        self.area = []
        self.birthday = []
        self.intro = []
        self.total_weibo = []
        self.following = []
        self.follower = []
        self.total_page:int
        self.filter = filter #所有微博 = 0; 原创微博 =1
        self.blog = []

    def get_html(self,url,*params):
        """获取传入url的html文本"""
        try:
            html = requests.get(url= url, cookies= self.cookies, params= params).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error:',e)
            traceback.print_exc()

    def get_userinfo(self):
        """获取昵称、性别等信息"""
        # 读取html
        url = 'https://weibo.cn/' + self.user_id + '/info'
        selector = self.get_html(url)
        # 筛选html
        info_list = selector.xpath('/html/body/div[8]/text()')
        # 存储
        self.name.append(info_list[0][1:])
        self.sex.append(info_list[1][1:])
        self.area.append(info_list[2][1:])
        self.birthday.append(info_list[3][1:])
        self.intro.append(info_list[5][1:])

    def get_userinfo2(self):
        """获取微博条数、关注数、粉丝数"""
        # 读取html
        url = 'https://weibo.cn/' + self.user_id + '/profile'
        selector = self.get_html(url)
        # 筛选html + 存储
        self.total_weibo.append(selector.xpath('/html/body/div[3]/div[2]/span/text()')[0])
        self.following.append(selector.xpath('/html/body/div[3]/div[2]/a[1]/text()')[0])
        self.follower.append(selector.xpath('/html/body/div[3]/div[2]/a[2]/text()')[0])

        # 筛选 + 存储（法2）
        # info_list = selector.xpath("//div[@class='tip2']/*/text()")
        # self.total_weibo.append(info_list[0])
        # self.following(info_list[1])
        # self.follower(info_list[2])

    def get_total_page_num(self):
        """获取微博总页数"""
        # 读取html
        url = 'https://weibo.cn/' + self.user_id + '/profile'
        selector = self.get_html(url)
        # 筛选html
        self.total_page = selector.xpath("/html/body/div[@class='pa']/form/div/text()")[1][-4:-1]

    def get_one_page(self,page_num):
        # 读取html
        params = {
            'filter' : self.filter,
            'page' : page_num
        }
        base_url = 'https://weibo.cn/' + self.user_id + '/profile?'
        url = base_url + urlencode(params)
        selector = self.get_html(url)
        # 筛选html
        for index in range(2,11):
            self.blog.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[1]//text()"))


           


    def show(self):
        self.get_userinfo()
        self.get_userinfo2()
        self.get_total_page_num()
        self.get_one_page(1)

        print(self.name)
        print(self.sex)
        print(self.area)
        print(self.birthday)
        print(self.intro)
        print(self.total_weibo)
        print(self.following)
        print(self.follower)
        print(self.total_page)
        for index in range(0,9):
            print(self.blog[index])


if __name__ == "__main__":
    cookies = 'SCF=AmMdYdAD8xDP84Xc7sEtL9WXFMVx_fALJyadgeh6G41PUqyXV4VQ_9g8MWqBiH82U_5rDZFKsxg0w-CrGae8IXg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFr0NVib_A0gaGkWL.D5ObN5JpX5K-hUgL.FozceK2R1K2cSKe2dJLoI0qLxKqLBKBLBo5LxK-LB-BL1K5LxKqLBo2L1h2LxKqL1hnL1K2LxKML1hnLBo2LxK-L1KqL1-Bt; _T_WM=52050499844; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; MLOGIN=0; SUB=_2A25x-7enDeRhGeRI6lMZ-S_Kzj-IHXVTB9nvrDV6PUJbkdBeLVrMkW1NUtpT2XBkCAb9xERrHGGHTjLUkQZBtos0; SUHB=08J6kbAgs1djdm; SSOLoginState=1560266743'
    weibo = weibo('2611891653',cookies,1)
    weibo.show()


