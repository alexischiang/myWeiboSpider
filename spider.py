#coding=utf-8
import progressbar
import time

import requests 
from urllib.parse import urlencode

# 异常处理库
import traceback
from lxml import etree

import csv
# \xa0 是不间断空白符 &nbsp;

class weibo:
    def __init__(self, user_id, cookies, filter, print_ori):
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
        # 显示转发微博原内容 = 1; 不显示 = 0
        self.print_ori = print_ori
        # 微博属性
        self.blog_content = []
        self.blog_content_total = []
        self.blog_likes = []
        self.blog_retweets = []
        self.blog_comments = []
        self.pics_info = []
        self.pics_info_re = []
        self.blog_time = []
        self.blog_device = []
        self.retweet_info = []
        self.ori_in_all = []
        self.original_blog_content = []

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

    def check_pics_num(self,selector,index):
        """检查该条微博是否含有图片并返回图片张数"""
        text_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//text()")
        href_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//a/@href")
        if self.check_with_pic(href_lists):
            if self.get_zutu_index(text_lists) != None:
                return '['+self.get_zutu_index(text_lists)+']'
            else:
                return '[共1张]'
        else:
            return None

    def check_pics_re(self,selector,index):
        """检查转发原内容里是否含有图片"""
        href_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[2]//a/@href")
        if self.check_with_pic(href_lists):
            return '[包含图片]'
        else:
            return None

    def cut_device_text(self,device_texts):
        """分割发布时间与发布设备分别返回字符串"""
        index = device_texts.rfind('\xa0')
            #先返回时间 后返回设备
        return device_texts[:index],device_texts[(index+3):]

    def check_long_weibo(self,selector,index):
        """判断是否长微博 是则返回url 否则返回none
        lists:含有值或[]的href列表
        """
        lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]//span[@class='ctt']/*/@href")
        if lists == []:
            return None
        else:
            if '/comment/' in lists[0]:
                return 'https://weibo.cn/'+ lists[0]
            else:
                return None

    def get_long_weibo(self,url):
        """获取filter1下的长微博内容
        lists:含有值或[]的href列表
        """
        long_selector = self.get_html(url)
        long_weibo = long_selector.xpath("/html/body/div[@id='M_']/div[1]/span[1]//text()")
        long_weibo[0] = long_weibo[0][1:]
        return ''.join(long_weibo)

    def check_original(self,lists,freindcircle):
        """判断是原创还是转发微博
        lists: 传入div[last]/span[cmt]的text
        friendcircle: 传入div[1]/span[cmt]的text
        return: true - 原创 false - zhuanfa
        """
        if lists == [] or freindcircle[0] == '[仅好友圈可见]' :
            return True
        elif '已赞[' in lists[0]:
            return True
        elif '转发理由:' in lists[0]:
            return False

    def get_content_re(self,selector,index):
        """
        获得需要加入content的text
        return：转发了xxx微博，转发理由
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

    def get_retweetblog_content(self,selector,index):
        """获得原微博的内容 返回字符串"""
        if self.check_long_weibo(selector,index) == None:
            # 不是长微博时 
            final_lists = []
            # temp_lists_cmt = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[@class='cmt']//text()")
            temp_lists_ctt = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[@class='ctt']//text()")
            final_lists = ''.join(temp_lists_ctt)
            return final_lists
        else:
            # 是长微博时
            return self.get_long_weibo(self.check_long_weibo(selector,index))


    def get_devices(self,index,selector):
        """获取设备和发布时间"""
        device_lists = selector.xpath("/html/body/div[@class='c']["+str(index)+"]/div[last()]/span[@class='ct']//text()")
        device_texts = ''.join(device_lists)
        time, device = self.cut_device_text(device_texts) 
        self.blog_time.append(time)
        self.blog_device.append(device)

    def get_blog_while_ori(self,index,selector):
        """整合获取原创微博所有信息的函数"""
        # 设置原创标志为true
        self.ori_in_all.append(True)
        # 处理 博文
        if self.check_long_weibo(selector,index) == None:
            # 判断不是长微博时 
            self.blog_content.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[1]//text()"))
        else:
            # 是长微博时
            self.blog_content.append(self.get_long_weibo(self.check_long_weibo(selector,index)))
        
        # 处理 发布时间、设备
        self.get_devices(index,selector)

        # 处理 "已赞"
        likes_text =  selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
        likes = self.get_zan_index(likes_text)   
        #添加操作
        self.blog_likes.append(likes[likes.rfind('[')+1:-1])     

        # 处理 好友圈无法转发问题 
        retweets_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]//text()")
        retweets = self.get_zhuanfa_index(retweets_text)
        #添加操作
        self.blog_retweets.append(retweets[retweets.rfind('[')+1:-1])  
        
        # 处理 评论
        #添加操作
        self.blog_comments.append(selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/a[last()-3]/text()")[0][3:-1])
        
        # 处理 有无图片与张数
        self.pics_info.append(self.check_pics_num(selector,index))
        self.pics_info_re.append(None)

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
                self.get_blog_while_ori(index,selector)
                     
        elif self.filter == 0: # 获取所有微博
            # 获取当前页面微博数量
            for index in range(1,len(selector.xpath("/html/body/div[@class='c']"))-1):
                # print(index)
                # print('---')
                # 判断是否原创
                span_text = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[last()]/span[@class='cmt']/text()")
                freindcircle = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]/span[@class='cmt']/text()")
                # print(span_text)
                # print(freindcircle)
                if self.check_original(span_text,freindcircle): #原创
                    self.get_blog_while_ori(index,selector)
                    self.retweet_info.append('【原创微博】')
                    self.original_blog_content.append('')
                else: #转发
                    # 设置原创标志为false
                    self.ori_in_all.append(False)
                    
                    # 处理 转发信息+理由
                    # （转发理由不能超过140字，不必判断是否为长微博）
                    re_info_text, re_content_text = self.get_content_re(selector,index)
                    self.blog_content.append(re_content_text)
                    self.retweet_info.append('【'+ re_info_text+ '】')

                    # 处理 原内容
                    self.original_blog_content.append(self.get_retweetblog_content(selector,index))
                    
                    # 处理 发布时间、设备
                    self.get_devices(index,selector)

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
                    self.pics_info.append(self.check_pics_num(selector,index))
                    self.pics_info_re.append(self.check_pics_re(selector,index))

                # print(self.blog_content)


    def enable_progressbar(self,page):
        for i in progressbar.progressbar(range(int(page))):
            self.get_one_page(i)
            time.sleep(0.2)
            progressbar.streams.flush()

        flag = input("print out the result? [y/n]：")

        if flag.lower() == 'y':
            # 格式化输出
            self.formal_output()
        else:
            print("end!")

    def formal_output(self):
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
        for index in range(0,len(self.blog_content)):
            if self.ori_in_all[index] == False:
                print(self.retweet_info[index])
                if self.print_ori == 1:
                    if self.pics_info_re[index] != None:
                        print('【'+self.original_blog_content[index] + self.pics_info_re[index]+'】')
                    else:
                        print('【'+self.original_blog_content[index]+'】')
                print('')
                print(''.join(self.blog_content[index])) 
            else:
                print('【原创微博】\n')
                print("微博内容："+''.join(self.blog_content[index]))# 修正合并单条博文
            if self.pics_info[index] != None:
                print("图片："+self.pics_info[index])
            print("赞："+self.blog_likes[index][0])
            print("转发："+self.blog_retweets[index][0])
            print("评论："+self.blog_comments[index][0])
            print("发布时间："+self.blog_time[index])
            print("微博来源："+self.blog_device[index])
            print('-'*8)
            print('')
        print('*' *20 + ' 爬取结束 ' + '*' *20)



    def save_as_csv(self):
        if self.filter == 0:
            csv_headers = [
                "微博内容", # 转发理由
                "转发来源",
                "转发内容",
                "图片信息",
                "点赞数",
                "转发数",
                "评论数",
                "发布时间",
                "微博来源",
            ]
            csv_datas = zip(
                self.blog_content_total,
                self.retweet_info,
                self.original_blog_content,
                self.pics_info,
                self.blog_likes,
                self.blog_retweets,
                self.blog_comments,
                self.blog_time,
                self.blog_device
            )
        else:
            csv_headers = [
                "微博内容", 
                "图片信息",
                "点赞数",
                "转发数",
                "评论数",
                "发布时间",
                "微博来源",
            ]
            csv_datas = zip(
                self.blog_content_total,
                self.pics_info,
                self.blog_likes,
                self.blog_retweets,
                self.blog_comments,
                self.blog_time,
                self.blog_device
            )
        with open('data.csv','w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)
            for i in csv_datas:
                writer.writerow(i)


    def main(self):
        # 获得个人信息
        self.get_userinfo()
        self.get_userinfo2()
        self.get_total_page_num()
        self.enable_progressbar(10)
        # self.get_one_page(4)
        for index in range(0,len(self.blog_content)):
            self.blog_content_total.append(''.join(self.blog_content[index])) 
        self.save_as_csv()


if __name__ == "__main__":
    cookies = '你的cookies'
    weibo = weibo('',cookies,1,0)
    weibo.main()


