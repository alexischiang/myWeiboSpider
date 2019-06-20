# myWeiboSpider

<p align="left">
    <a href="">
        <img src="https://img.shields.io/badge/状态-持续更新中-brightgreen.svg">
        </a>
    <a href="https://github.com/python/cpython">
        <img src="https://img.shields.io/badge/Python-3.7-blue.svg">
        </a>
    <a href="https://github.com/alexischiang/myWeiboSpider/stargazers">
        <img src="https://img.shields.io/github/stars/alexischiang/myWeiboSpider.svg?logo=github">
        </a>
</p>
通过xPATH库爬取微博数据(练习用)

## ChangeLog:
#### 2019/6/12 0:37 
*实现爬取用户个人信息*
#### 2019/6/12 9:13
*实现爬取关注粉丝信息*
#### 2019/6/12 11:38
*获取总页数*
#### 2019/6/12 13:33
*初步完成单页原创微博爬取并以列表形式保存*<br>
*还需要对列表的存储内容进行优化*
#### 2019/6/12 20:52
*完成所有原创微博爬取*<br>
*完成微博内容+点赞数+评论数+转发数爬取并格式化显示*
#### 2019/6/13 0:16
*修复“已赞”和好友圈微博无法转发导致的爬取bug*
#### 2019/6/13 11:36
*完成对每条爬取微博所含图片的分析*<br>
*(通过分析herf中URL实现)*
#### 2019/6/13 16:43
*完成长微博的分析及爬取*<br>
*(存在碰到@用户与#标签#时无法爬取的bug)*
#### 2019/6/14 0:17
*修复爬取长微博的bug*
#### 2019/6/14 11:51
*完成微博发布时间、设备的获取并格式化显示*
#### 2019/6/14 12:59
*修复爬取到最后一页报错的bug*
#### 2019/6/16 1:10
*完成了所有微博（原创+转发）的爬取,尚未进行大批量测试*<br>
*代码结构较复杂，需进行初步重构*
*存在“用户有评论转发等消息未查看时无法进行爬取”的bug*
#### 2019/6/17 16:35
*完成初步重构*
#### 2019/6/20 10:09
*完成进度条的添加，更直观的显示了抓取进度与预计剩余时间*
*(用progressbar2实现)*<br>
*爬取转发微博仍存在bug*
#### 2019/6/20 12:45
*修复上述bug*
#### 2019/6/20 13:21
*新增可以选择显示原微博内容的初始化选项*<br>
*添加了转发微博含有图片的提示*
#### 2019/6/20 14:04
*修复了转发原内容是长微博时无法显示完全的bug*
#### 2019/6/21 1:28
*现在已经可以将爬取内容保存成csv格式*




## To-do list:
#### ~~·爬取用户个人信息~~
#### ~~·爬取关注粉丝信息~~
#### ~~·爬取原创微博~~
#### ~~·爬取微博信息（点赞、评论、转发）~~
#### ~~·爬取所有微博（原创+转发）~~
#### ~~·长微博显示~~
#### ~~·获取微博发布时间、设备等信息~~
#### ~~·显示原微博信息（用户可选项）~~
#### ~~·初步重构~~
#### ~~·添加进度条~~
#### ·图片存取
#### ~~·将所有爬取信息存储~~
#### ·封装、异常处理
#### ·发布用法到readme
#### ·重构

## Contact Me:

QQ:1091285927