from playwright.sync_api import sync_playwright
import time
import re
import json
from time import sleep
from bs4 import BeautifulSoup
import requests

url='https://www.spglobal.com/marketintelligence/en/mi-news-sitemap.xml'

#实时加载sitemap
with sync_playwright() as driver:
    browser=driver.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto(url)
    #选取loc to get full urls
    tag=page.locator('loc')
    sites=tag.all_text_contents()
    browser.close()
#返回的sites 储存了所有待爬的网页

#now change a little to the original list since all it starts with ishmarkit,
#change them into www.spglobal
    '''
index=0
for element in sites:
    new=element.replace("ihsmarkit","www.spglobal",1)
    sites[index]=new
    index=index+1
'''
#now we have a list of urls
#write a def for all of them for scraping.

def get_json(url,fileName):
    #url is each element in the list and fileName is how we save them in file.
    with sync_playwright() as driver:
        browser=driver.chromium.launch(headless=False)
        context=browser.new_context()
        page=context.new_page()
        #set a higher timeout default so some websites can be able to generate
        page.set_default_timeout(100000)
        page.goto(url)
        #get the html_text first
        html_text=page.content()
        browser.close()
        
    #用soup和ele筛选
    soup=BeautifulSoup(html_text,'html.parser')
    ele=soup.select('p')
    
    #用full_text来存储页面文本信息
    full_text=""
    #遍历response set去除<xxx> 保留文本
    for element in ele:
        full_text=full_text+element.get_text(separator="\n",strip=True)   
    json_content={
        "url" : url,
        "html" : html_text,
        "text" : full_text
        }
    json_text=json.dumps(json_content)
    #save as file
    with open(fileName,'w',encoding='utf-8') as fp:
        fp.write(json_text)

#end of def
#start scraping using url list and for loop
#count is for testing several cases to test the code since there are 10000+ urls   
#count=0
for url in sites:
    #each url are easily generated
    #now name the fileName
    #all url starts with https://www.spglobal.com/......,
    #start from index 61
    name="mi_news_"+url[61:]
    #change all other -/ into _
    trans=re.sub('\W',"_",name)
    fileName=trans+'.json'
    '''
    if count>30:
        break
    count=count+1
    #'''
    try:
        get_json(url,fileName)
    except:
        continue


