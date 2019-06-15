import requests 
from urllib.parse import urlencode

# 异常处理库
import traceback
from lxml import etree

# \xa0 是不间断空白符 &nbsp;

class weibo:
    def __init__(self, user_id, cookies, filter):
        """初始化"""
        # 请求信息
        self.user_id = user_id
        self.cookies = {
            'Cookie' : cookies
        }
        # 个人信息
        self.name = []
        self.sex = []
        self.area = []
        self.birthday = []
        self.intro = []
        self.total_weibo = []
        self.following = []
        self.follower = []
        self.total_page:int
        # 所有微博 = 0; 原创微博 =1
        self.filter = filter 
        # 微博属性
        self.blog_content = []
        self.blog_likes = []
        self.blog_retweets = []
        self.blog_comments = []
        self.pics_info = []
        self.blog_time = []
        self.blog_device = []
        self.retweet_info = []
        self.ori_in_all = []

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

    def get_total_page_num(self):
        """获取微博总页数"""
        # 读取html
        url = 'https://weibo.cn/' + self.user_id + '/profile'
        selector = self.get_html(url)
        # 筛选html
        self.total_page = selector.xpath("/html/body/div[@class='pa']/form/div/text()")[1][-4:-1]

    def get_zan_index(self,likes_text):
        """在列表中找到赞的索引并返回该索引的内容"""
        try:
            for index in range(0,len(likes_text)):
                if '赞[' in likes_text[index]:
                    return likes_text[index]
        except Exception as e:
            print('Error:',e)
            traceback.print_exc()

    def get_zhuanfa_index(self,retweets_text):
        """在列表中找到转发的索引并返回该索引的内容"""
        try:
            for index in range(0,len(retweets_text)):
                if '发[' in retweets_text[index]:
                    return retweets_text[index]
        except Exception as e:
            print('Error:',e)
            traceback.print_exc()

    def get_zutu_index(self,text_list): # text_list 来自 div[index]//text()
        """在列表中找到组图的索引并返回该索引的内容"""
        for index in range(0,len(text_list)):
            if '\xa0[' in text_list[index]:
                return text_list[index+1]

    def check_with_pic(self,href_list):
        """检索URL中是否含有带图片的URL"""
        for index in range(0,len(href_list)):
            if '/pic' in href_list[index]:
                return True
            else:
                return False

    def check_pics_num(self,text_list,href_list):
        """检查该条微博是否含有图片并返回图片张数"""
        if self.check_with_pic(href_list):
            if self.get_zutu_index(text_list) != None:
                return '['+self.get_zutu_index(text_list)+']'
            else:
                return '[共1张]'
        else:
            return None

    def cut_device_text(self,device_texts):
        """分割发布时间与发布设备分别返回字符串"""
        index = device_texts.rfind('\xa0')
            #先返回时间 后返回设备
        return device_texts[:index],device_texts[(index+3):]

    def check_long_weibo(self,lists):
        """判断是否长微博 是则返回url 否则返回none"""
        if lists == []:
            return None
        else:
            if '/comment/' in lists[0]:
                return 'https://weibo.cn/'+ lists[0]
            else:
                return None

    def check_original(self,lists):
        """判断是原创还是转发微博
        lists: 传入span的text
        return: true - 原创 false - zhuanfa
        """
        if lists == []:
            return True
        elif '转发理由:' in lists[0]:
            return False

    def get_content_re(self,selector,index):
        """
        获得需要加入content的text
        return：转发了xxx微博，微博内容
        """
        global re_content_list
        # 整理转发信息
        re_info_list = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[@class='cmt']//text()")
        # 处理文本：['转发了\xa0', '椰子汁我爱喝', '\xa0的微博:'] -> ['转发了','@椰子汁我爱喝','的微博']
        re_info_list[0] = re_info_list[0][:-1]
        re_info_list[1] = '@' + re_info_list[1][:]
        re_info_list[2] = ' ' + re_info_list[2][1:-1]
        re_info_text = re_info_list[0] + re_info_list[1] + re_info_list[2]
        # 整理转发内容
        temp_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
        for index in range(0,len(temp_lists)):
            if '赞[' in temp_lists[index]:
                re_content_list = temp_lists[:index]
                re_content_list.insert(1,'@'+self.name[0]+':')
        re_content_text = ''.join(re_content_list)
        return re_info_text,re_content_text

    def get_one_page(self,page_num):
        """爬取单页10条微博内容+点赞数+评论数+转发数"""
        # 读取html
        params = {
            'filter' : self.filter,
            'page' : page_num
        }
        base_url = 'https://weibo.cn/' + self.user_id + '/profile?'
        url = base_url + urlencode(params)
        selector = self.get_html(url)

        # 筛选html
        if self.filter == 1: # 获取原创
            # 获取当前页面微博数量
            for index in range(1,len(selector.xpath("/html/body/div[@class='c']"))-1):
                # 设置原创标志为true
                self.ori_in_all.append(True)
                # 处理 博文
                lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//span[@class='ctt']/*/@href")
                if self.check_long_weibo(lists) == None:
                    # 判断不是长微博时 
                    self.blog_content.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[1]//text()"))
                else:
                    # 是长微博时
                    long_url = self.check_long_weibo(lists)
                    long_selector = self.get_html(long_url)
                    long_weibo = long_selector.xpath("/html/body/div[@id='M_']/div[1]/span[1]//text()")
                    long_weibo[0] = long_weibo[0][1:]
                    self.blog_content.append(''.join(long_weibo))

                # 处理 发布时间、设备
                device_lists = selector.xpath("/html/body/div[@class='c']["+str(index)+"]/div[last()]/span[@class='ct']//text()")
                device_texts = ''.join(device_lists)
                time, device = self.cut_device_text(device_texts) 
                self.blog_time.append(time)
                self.blog_device.append(device)

                # 处理 "已赞"
                likes_text =  selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                likes = self.get_zan_index(likes_text)   
                self.blog_likes.append(likes[likes.rfind('[')+1:-1])     

                # 处理 好友圈无法转发问题 
                retweets_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                retweets = self.get_zhuanfa_index(retweets_text)
                self.blog_retweets.append(retweets[retweets.rfind('[')+1:-1])  
                
                # 处理 评论
                self.blog_comments.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/a[last()-3]/text()")[0][3:-1])
                
                # 处理 有无图片与张数
                text_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//text()")
                href_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//a/@href")
                self.pics_info.append(self.check_pics_num(text_lists,href_lists))
            
                
                
        elif self.filter == 0: # 获取所有微博
            # 获取当前页面微博数量
            for index in range(1,len(selector.xpath("/html/body/div[@class='c']"))-1):
                # print(index)
                # print('---')
                # 判断是否原创
                span_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/span[@class='cmt']/text()")

                if self.check_original(span_text): #原创
                    # 设置原创标志为true
                    self.ori_in_all.append(True)
                    # 处理 博文
                    lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//span[@class='ctt']/*/@href")
                    if self.check_long_weibo(lists) == None:
                        # 判断不是长微博时 
                        self.blog_content.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[1]//text()"))
                    else:
                        # 是长微博时
                        long_url = self.check_long_weibo(lists)
                        long_selector = self.get_html(long_url)
                        long_weibo = long_selector.xpath("/html/body/div[@id='M_']/div[1]/span[1]//text()")
                        long_weibo[0] = long_weibo[0][1:]
                        self.blog_content.append(''.join(long_weibo))

                    # 处理 发布时间、设备
                    device_lists = selector.xpath("/html/body/div[@class='c']["+str(index)+"]/div[last()]/span[@class='ct']//text()")
                    device_texts = ''.join(device_lists)
                    time, device = self.cut_device_text(device_texts) 
                    self.blog_time.append(time)
                    self.blog_device.append(device)

                    # 处理 "已赞"
                    likes_text =  selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                    likes = self.get_zan_index(likes_text)   
                    self.blog_likes.append(likes[likes.rfind('[')+1:-1])     

                    # 处理 好友圈无法转发问题 
                    retweets_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                    retweets = self.get_zhuanfa_index(retweets_text)
                    self.blog_retweets.append(retweets[retweets.rfind('[')+1:-1])  
                    
                    # 处理 评论
                    self.blog_comments.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/a[last()-3]/text()")[0][3:-1])
                    
                    # 处理 有无图片与张数
                    text_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//text()")
                    href_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//a/@href")
                    self.pics_info.append(self.check_pics_num(text_lists,href_lists))

                    self.retweet_info.append('【原创微博】')
                
                else: #转发
                    # 设置原创标志为false
                    self.ori_in_all.append(False)
                    # 处理 博文                   
                    # 判断长微博
                    if self.check_long_weibo(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//span[@class='ctt']/*/@href")) == None:
                        # 不是长微博时 
                        re_info_text, re_content_text = self.get_content_re(selector,index)
                        self.blog_content.append(re_content_text)
                        self.retweet_info.append('【'+ re_info_text+ '】')
                    else:
                        print('confirm long!')
                        # 是长微博时
                        # self.blog_content.append('该条可能是转发长微博【bug未修复】')
                        long_url = self.check_long_weibo(lists)
                        long_selector = self.get_html(long_url)
                        long_weibo = long_selector.xpath("/html/body/div[@id='M_']/div[1]/span[1]//text()")
                        long_weibo[0] = long_weibo[0][1:]
                        self.blog_content.append(''.join(long_weibo))

                    # 处理 发布时间、设备
                    device_lists = selector.xpath("/html/body/div[@class='c']["+str(index)+"]/div[last()]/span[@class='ct']//text()")
                    device_texts = ''.join(device_lists)
                    time, device = self.cut_device_text(device_texts) 
                    self.blog_time.append(time)
                    self.blog_device.append(device)

                    # 处理 "已赞"
                    likes_text =  selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                    likes = self.get_zan_index(likes_text)   
                    self.blog_likes.append(likes[likes.rfind('[')+1:-1])     

                    # 处理 好友圈无法转发问题 
                    retweets_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
                    retweets = self.get_zhuanfa_index(retweets_text)
                    self.blog_retweets.append(retweets[retweets.rfind('[')+1:-1])  
                    
                    # 处理 评论
                    self.blog_comments.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/a[last()-3]/text()")[0][3:-1])
                    
                    # 处理 有无图片与张数
                    text_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//text()")
                    href_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//a/@href")
                    self.pics_info.append(self.check_pics_num(text_lists,href_lists))


           


    def show(self):
        self.get_userinfo()
        self.get_userinfo2()
        self.get_total_page_num()

        for index in range(1, 2):
            self.get_one_page(index)
            # print(self.blog_content)
        
        print('*' *20 + ' 我的资料 ' + '*' *20)
        print("昵称："+self.name[0])
        print("性别："+self.sex[0])
        print("地区："+self.area[0])
        print("生日："+self.birthday[0])
        print("简介："+self.intro[0])
        print("微博数："+self.total_weibo[0][3:-1]+" 条")
        print("关注："+self.following[0][3:-1]+" 人")
        print("粉丝："+self.follower[0][3:-1]+" 人")
        print('*' *20 + ' 我的微博 ' + '*' *20)
        # print(self.total_page)
        # print(self.blog_content)
        # print(self.blog_likes)
        # print(self.blog_retweets)
        # print(self.blog_comments)
        for index in range(0,len(self.blog_content)):
            if self.ori_in_all[index] == False:
                print(self.retweet_info[index])
                print(''.join(self.blog_content[index])) 
            else:
                print('【原创微博】')
                print("微博内容："+''.join(self.blog_content[index]))# 修正合并单条博文
            if self.pics_info[index] != None:
                print("图片："+self.pics_info[index])
            print("赞："+self.blog_likes[index][0])
            print("转发："+self.blog_retweets[index][0])
            print("评论："+self.blog_comments[index][0])
            print("发布时间："+self.blog_time[index])
            print("微博来源："+self.blog_device[index])
            print('-'*8)
        print('*' *20 + ' 爬取结束 ' + '*' *20)


if __name__ == "__main__":
    cookies = 'SCF=AmMdYdAD8xDP84Xc7sEtL9WXFMVx_fALJyadgeh6G41PUqyXV4VQ_9g8MWqBiH82U_5rDZFKsxg0w-CrGae8IXg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFr0NVib_A0gaGkWL.D5ObN5JpX5K-hUgL.FozceK2R1K2cSKe2dJLoI0qLxKqLBKBLBo5LxK-LB-BL1K5LxKqLBo2L1h2LxKqL1hnL1K2LxKML1hnLBo2LxK-L1KqL1-Bt; _T_WM=52050499844; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; MLOGIN=0; SUB=_2A25x-7enDeRhGeRI6lMZ-S_Kzj-IHXVTB9nvrDV6PUJbkdBeLVrMkW1NUtpT2XBkCAb9xERrHGGHTjLUkQZBtos0; SUHB=08J6kbAgs1djdm; SSOLoginState=1560266743'
    weibo = weibo('2611891653',cookies,0)
    weibo.show()


