import urllib.request
import http.cookiejar
import http.cookies
import urllib.parse
import re
import time
import os
import random



cookiejar=http.cookiejar.LWPCookieJar('tieba')
CookieHandle=urllib.request.HTTPCookieProcessor(cookiejar)
opener=urllib.request.build_opener(CookieHandle,urllib.request.HTTPHandler)


def make_cookie(name,value):
    cookie=http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="baidu.com",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )
    return cookie

def get_barurl(name):
    url='http://tieba.baidu.com/f?kw='
    url=url+urllib.parse.quote(name)
    return url

def add_sign(name):
    url='http://tieba.baidu.com/sign/add'
    data={
        'ie':'utf-8',
        'kw':name,
        'tbs':'6ac12c1c8431559d1424007047'
        }
    try:
        result=opener.open(url,urllib.parse.urlencode(data).encode())
        return result.read().decode('utf-8')
    except:
        print("签到%s失败" %name)
        return 0
def match_bar(string):
    result=[]
    a=r'title="(.+?)">\1</a></td>'
    a=re.compile(a)
    result=re.findall(a,string)
    return result

def get_all_bar():
    url='http://tieba.baidu.com/f/like/mylike?pn='
    page=1
    result=[]
    while(1):
        url2=url+str(page)
        print(url2)
        html=opener.open(url2)
        html=html.read()
        html=html.decode('gbk')
        result+=match_bar(html)
        if(html.find('下一页') == -1):
            break
        page+=1
    return result
def add_all_sign(bars):
    for index,i in enumerate(bars):
        result=add_sign(i)
        print("%s吧 签到成功" % i)
        sptime=random.randint(5,10)
        time.sleep(sptime)


BDUSS=''#此处请修改为自己的BDUSS
cookie=make_cookie('BDUSS',BDUSS)
cookiejar.set_cookie(cookie)


bars=get_all_bar()
add_all_sign(bars)
