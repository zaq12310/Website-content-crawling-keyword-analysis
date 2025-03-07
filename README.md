# 基于Python进行web网页内容爬取，实现内容关键字权重可视化（小米微博贴文评论舆情分析）

------

[TOC]



## 一、工具

1. 解释器：python 3.13
2. 四大模块：requests、re、WordCloud、matplotlib

```python
import requests  # 导入请求模块
import re  # 文本的匹配
from wordcloud import WordCloud  # 词云模块
import matplotlib.pyplot  # 画图模块
```

> 没有这些模块的话，请先下载

```cmd
pip install requests
#re是python自带，因此无需下载
pip install WordCloud
pip install matplotlib
```

## 二、代码解析（逻辑分析）

用edge浏览器打开[小米微博贴](https://weibo.com/1771925961/PgmLUCYFa)

#### 2.1 定义请求头请求数据

为什么要定义请求头，因为从网站的设置初衷，它是不想服务于我们的爬虫程序的，网站正常只想服务于客户的访问服务，那么我们要将我们的爬虫程序伪装成为正常的服务。

（在不定义请求头的情况下无法获取网页数据，只能获取到html）

> 此时我们需要定义一些数据来伪装，通常我们只需要设置 cookie 、referee、user-agent就够了(如果有些特殊的网站可能需要我们有其他的参数) 

```python
#定义请求头
headers = {
    #用户身份信息
    'user-agent': '填写标头中的user-agent',
    #防盗链
    'cookie': '填写标头中的cookie',
    #浏览器基本信息
    'referer': '填写标头中的referer'}
```

根据以下步骤找到所需要的数据，将 cookie 、referer 、user-agent 的数据分别粘贴在代码里面

1. 打开检查页面

   ![image-20250306125630446](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061256830.png)

2. 点击标头，请求头(headers)的检查元素界面 找到url，向下滑动找到cookie 、referer 、user-agent 的数据粘贴到代码里

   ![image-20250306130706841](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061307398.png)

#### 2.2 建立循环遍历所有分页

根据以下步骤找到页面下所有分页，并使用代码遍历分页

1. 在这里我们可以看到这个“buildComments”，这是对应的整篇帖子的评论的包，我们复制这一小部分，筛选器搜索

   ![image-20250306133644012](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061336331.png)

2. 获取分页数据组

   ![image-20250306134426264](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061344129.png)

3. 复制各个分页url到txt文件中，发现各个分页在某处不同

   ![image=202503061354779](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora img/202503061354779.png)

   ![image-20250306141559699](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061416989.png)

4. 将变化的变量定义为一个next字符串，建立循环

   ```python
   next = 'count=10' #多个页面读取所需要的页面自变量
   while True: #死循环
       url = f'...{next}...' #复制页面链接，将各页面不同之处用{变量}表达
       res = requests.get(url, headers=headers)  # 请求网址
       #    print(res) #打印请求状态，直接打印res是打印当前请求的状态码，200是成功，404是错误
       JSON = res.json()  # 定义一个JOSN来存储 res.json()的数据
   
       if JSON['max_id'] == 0: #发现max_id为0 结束循环
           break
       #建立第二次循环条件
       max_id = JSON['max_id'] #获取现在的JOSN中的max_id
       next = 'max_id=' + str(max_id) #为下一次循环做准备
   ```

   > max_id是直接存储在JOSN中的，因此不需要定义，直接让代码找到位置读取出来就可以

   ![image-20250306143529519](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061435686.png)

#### 2.3 在循环中提取所需要的数据

例：提取所有的评论内容存储在字符串text_long中

```
text_long = '' #存储所有评论内容
开始循环
    JSON = 请求返回数据  # 定义一个JOSN来存储请求返回的数据

    com20 = JSON['data']  # 把20条评论（com20）拿出来，
    #其实是拿出整体的评论，但这里的data整体数据只有20条，因此为拿出20条评论
    # print(com20)
    for com1 in com20: #遍历com20中的每个数组（【0】，【1】，【2】...）
        # 这里 com1 代表着 com20的第一个数也就是 ['data'][0]
        com0 = com1['text_raw']  # 一条评论（com1）里面的text里面 有一条评论的话（com0）
        text_long += com0  # 得到一条评论 把它添加到text_long
        print(com0)
        循环结束/继续条件筛选
```

> 请求返回数据中，每条评论都存储在 JSON→ data→com1（0 1 2...19）→text_raw 中

![image-20250306144924166](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061449819.png)

#### 2.4 可视化操作

获取到的字符串数据text_long ，初步处理（去除表情符）后，进行可视化操作

```python
open('评论.txt', 'w', encoding='utf-8').write(text_long) #将text_long数据写入 评论.txt文件中
# （没有 评论.txt文件的话就自己新建一个）

text_long = open('评论.txt', 'r', encoding='utf-8').read()  # 字符串读取出来
text_long = re.sub(r'\[.*?\]', '', text_long)  # 把【xxx】去掉
wordcloud = WordCloud(font_path='字魂联盟综艺体.ttf', width=1920, height=1080, background_color='white').generate(text_long) #建立词云
matplotlib.pyplot.imshow(wordcloud)  # 把词云画在画板上
matplotlib.pyplot.show()  # 显示这个画板
```

## 三、运行代码输出

运行【小米微博主页视频舆论词云分析-2.py】

获得在这篇贴文下评论的关键词显示图表（字体越大，说明出现次数越多）

![image-20250306154216034](https://cdn.jsdelivr.net/gh/zaq12310/cloud-image-hosting/Typora%20img/202503061542212.png)

## 四、参考资料

1. wyw在路上. python爬虫爬取微博评论--完整版(超详细，大学生不骗大学生)[EB/OL]. 2024[2024年05月29日]. https://blog.csdn.net/m0_68325382/article/details/137435906.
