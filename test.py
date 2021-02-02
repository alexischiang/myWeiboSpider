import requests 
from lxml import etree


headers = {
    'Host' : 'weibo.cn',
    'Referer' : 'https://weibo.cn/?pos=65&s2w=admin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
cookies = {
    'Cookie' : ''
}
html = requests.get('https://weibo.cn//profile?filter=0&page=5', headers= headers, cookies= cookies).content
selector = etree.HTML(html)

re_content_list = []
# for index in range(1,10):
index = 6
temp_lists = selector.xpath("/html/body/div[@class='c'][" + str(index) + "]/div[1]//text()")
print(temp_lists)
print(len(temp_lists))
for index in range(len(temp_lists)):
    if '赞[' in temp_lists[index]:
        final_lists =  temp_lists[:index]
    
print(''.join(final_lists))
