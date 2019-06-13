import requests 
from lxml import etree


headers = {
    'Host' : 'weibo.cn',
    'Referer' : 'https://weibo.cn/?pos=65&s2w=admin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
cookies = {
    'Cookie' : 'SCF=AmMdYdAD8xDP84Xc7sEtL9WXFMVx_fALJyadgeh6G41PUqyXV4VQ_9g8MWqBiH82U_5rDZFKsxg0w-CrGae8IXg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFr0NVib_A0gaGkWL.D5ObN5JpX5K-hUgL.FozceK2R1K2cSKe2dJLoI0qLxKqLBKBLBo5LxK-LB-BL1K5LxKqLBo2L1h2LxKqL1hnL1K2LxKML1hnLBo2LxK-L1KqL1-Bt; _T_WM=52050499844; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; MLOGIN=0; SUB=_2A25x-7enDeRhGeRI6lMZ-S_Kzj-IHXVTB9nvrDV6PUJbkdBeLVrMkW1NUtpT2XBkCAb9xERrHGGHTjLUkQZBtos0; SUHB=08J6kbAgs1djdm; SSOLoginState=1560266743'
}
html = requests.get('https://weibo.cn/2611891653/profile?filter=1&page=1', headers= headers, cookies= cookies).content
selector = etree.HTML(html)

index1 = 1
index2 = 9
a = selector.xpath("/html/body/div[@class='c'][" + str(index1) + "]//text()")
b = selector.xpath("/html/body/div[@class='c'][" + str(index2) + "]/div[last()]//a/@href")

def get_zutu_index(a):
    for index in range(0,len(a)):
        if '\xa0[' in a[index]:
            return a[index+1]

def get_yuantu_index(b):
    for index in range(0,len(b)):
        if '赞[' in b[index]:
            return b[index-2]


# print(a)
# print(b)
print(get_zutu_index(a))
print(type(get_zutu_index(a)))
# print(get_yuantu_index(b))
