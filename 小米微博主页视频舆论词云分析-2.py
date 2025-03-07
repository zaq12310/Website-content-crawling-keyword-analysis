import requests  # 导入请求模块
import re  # 文本的匹配
from wordcloud import WordCloud  # 词云模块
import matplotlib.pyplot  # 画图模块

headers = {
    # 用户身份信息
    'cookie': 'SINAGLOBAL=1365051632167.873.1622200456029; SCF=AgYvC4Sp396afaFdc7s3xbtCk97vGk_0eGuu9G3X8CNVhTA6WJlRJhIWttCcs4CGQ_EPav6oXg56oaOZQQl1-jc.; SUB=_2A25KzPXVDeRhGeFP41oS9CrIzzuIHXVpoHcdrDV8PUNbmtANLVDhkW9NQRaAbohaTZXi1manEtfzTQXRC9nOsbyD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPFLf0.gvTvBDLNsOqQ8ck5JpX5KzhUgL.FoMp1hn0ShBXShM2dJLoI7LKUcHLUh8AMK2t; ALF=02_1743786629; XSRF-TOKEN=CL10fA98JhPMySokEPufnPDO; WBPSESS=cn65pq1p5rIVPAlaX8-mxf5zRp-5k9WtG5l5Os_z77pEr6u-7zlU99eiA6komOWNy4kWDggEBfd_XXmApB73334Wb_b6-HeXfxAuPSApTRX3fmS42OD14eCF8uPAzAsM3QXCSjNCDDqoDEPkjkzTAA==',
    # 防盗链
    'referer': 'https://weibo.com/1771925961/PgmLUCYFa',
    # 浏览器基本信息
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}
text_long =''
next='count=10'
while True: #死循环
    # url是一访问网站的地址(这个不是很了解，但是我们代码是需要通过url来找到你要爬取的网页
    url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5139007869289656&is_show_bulletin=2&is_mix=0&{next}&uid=1771925961&fetch_level=0&locale=zh-CN'
    res = requests.get(url, headers=headers)  # 请求网址
    #    print(res) #打印请求状态，直接打印res是打印当前请求的状态码，200是成功，404是错误
    JSON = res.json()  # 定义一个JOSN来存储 res.json()的数据

    com20 = JSON['data']  # 把20条评论（com20）拿出来
    # print(com20)
    for com1 in com20: #遍历com20中的每个数组（【0】，【1】，【2】...）
        # 这里 com1 代表着 com20的第一个数也就是 ['data'][0]
        com0 = com1['text_raw']  # 一条评论（com1）里面的text里面 有一条评论的话（com0）
        text_long += com0  # 得到一条评论 把它添加到text_long
        print(com0)

    if JSON['max_id'] == 0: #发现has_more为0 结束循环
        break
    #建立第二次循环条件
    max_id = JSON['max_id']
    next = 'max_id=' + str(max_id)

#get_next函数行不通（因为脱离不了循环）
# 定义一个get_next宏函数，在函数里面定一个next变量，它的初值是'count=10'
# def get_next(next='count=10',text_long=text_long):
#     # url是一访问网站的地址(这个不是很了解，但是我们代码是需要通过url来找到你要爬取的网页
#     url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5139007869289656&is_show_bulletin=2&is_mix=0&{next}&uid=1771925961&fetch_level=0&locale=zh-CN'
#     res = requests.get(url, headers=headers)  # 请求网址
#     #    print(res) #打印请求状态，直接打印res是打印当前请求的状态码，200是成功，404是错误
#     JSON = res.json()  # 定义一个JOSN来存储 res.json()的数据
#
#     com20 = JSON['data']  # 把20条评论（com20）拿出来
#     # print(com20)
#     for com1 in com20:
#         # 这里 data 代表着 com20的第一个数也就是 ['data'][0]
#         com0 = com1['text_raw']  # 一条评论（com1）里面的text里面 有一条评论的话（com0）
#         text_long += com0  # 得到一条评论 把它添加到text_long
#         print(com0)
#     #建立循环条件
#     max_id = JSON['max_id']
#     max_str = 'max_id=' + str(max_id)
#     if JSON['max_id'] == 0: #发现has_more为0 结束循环
#         return text_long
#     get_next(max_str)
# text_long = get_next() #运行get_next函数


open('评论.txt', 'w', encoding='utf-8').write(text_long)

text_long = open('评论.txt', 'r', encoding='utf-8').read()  # 字符串读取出来
text_long = re.sub(r'\[.*?\]', '', text_long)  # 把【xxx】去掉
wordcloud = WordCloud(font_path='字魂联盟综艺体.ttf', width=1920, height=1080, background_color='white').generate(
    text_long)
matplotlib.pyplot.imshow(wordcloud)  # 把词云画在画板上
matplotlib.pyplot.show()  # 显示这个画板
#
