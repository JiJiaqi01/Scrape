# -*- coding: utf-8 -*-
"""

"""

import requests
from bs4 import BeautifulSoup
import re
import json

headers={
    "User_Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

#建立函数方便爬取不同网页
def get_text_json(url,fileName,headers=headers):    #url 为对应网页
    #filename为存储的文件名(带.json)
    #返回页面源代码
    response=requests.get(url=url,headers=headers)
    html_text=response.text
    #用soup筛选<p>获取文本
    soup=BeautifulSoup(html_text,'html.parser')
    ele=soup.select('p')
    #用full_text来存储页面文本信息
    full_text=""
    #遍历response set去除<xxx> 保留文本
    for element in ele[0:-1]:
        full_text=full_text+element.get_text(separator="\n",strip=True)
    #现在已有  htmltext 和 full_text
    #合并json
    json_content={
        "url" : url,
        "html" : html_text,
        "text" : full_text
    }
    #将dictionary转换成json格式
    json_text=json.dumps(json_content)
    #写入文件
    with open(fileName,'w',encoding='utf-8') as fp:
        fp.write(json_text)
        
    
#获取industry_eu相关的所有可爬网页
url='https://www.iata.org/sitemap.xml'
response=requests.get(url=url,headers=headers)
html_text=response.text
#用soup筛选<p>获取文本
soup=BeautifulSoup(html_text,'xml')
ele=soup.select('loc')
'''
#用full_text来存储页面文本信息
full_text=""
#遍历response set去除<xxx> 保留文本
for element in ele:
    #每运行一次，获取一次网页地址，然后换行
    full_text=full_text+element.get_text(separator="\n",strip=True)+'\n'
#输出结果， sites.txt存储所有的网页，一行一个
with open("sites.txt",'w',encoding='utf-8') as fp:
    fp.write(full_text)
'''
# 建立一个list,储存所有网址
sitemap_set=[]
for element in ele:
    #ele[x]都是str type
    #去除<loc>,<\loc>
    sitemap_set.append(element.get_text(separator="\n",strip=True))

#count is use for pre-test
#count=0
for url in sitemap_set:
    #我们调用的get_json_text用的url就是for 的那个url
    #接下来创建fileName
    #对url稍作修改,先去除https://www.iata.org/,因为所有url都有这个前缀
    temp=url[24:]
    temp="iata_"+temp
    #用正则表达替换除了数字和字母之外的部分
    trans=re.sub('\W',"_",temp)
    #生成fileName
    fileName= trans+".json"
    #调用get_json_text
    #加一个try防止某一个网页因格式问题报错
    '''
    if count>200:
        break
    count=count+1
'''
    try:
        get_text_json(url,fileName)
    except:
        continue
