# *-* coding:utf-8 *-*
import requests
import urllib.parse
import threading,time,os

#设置照片存放路径
os.mkdir('duitangpic')
base_path = os.path.join(os.path.dirname(__file__),'duitangpic')

#设置最大信号量线程锁
thread_lock=threading.BoundedSemaphore(value=10)

#通过url获取数据
def get_page(url):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page=requests.get(url,headers=header)
    page=page.content #content是byte
    #转为字符串
    page=page.decode('utf-8')
    return page

#label  即是搜索关键词
def page_from_duitang(label):
    pages=[]
    url='https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    label=urllib.parse.quote(label)#将中文转成url(ASCII)编码
    for index in range(0,3600,100):
        u=url.format(label,index)
        #print(u)
        page=get_page(u)
        pages.append(page)
    return pages

def findall_in_page(page,startpart,endpart):
    all_strings=[]
    end=0
    while page.find(startpart,end) !=-1:
        start=page.find(startpart,end)+len(startpart)
        end=page.find(endpart,start)
        string=page[start:end]
        all_strings.append(string)

    return all_strings

def pic_urls_from_pages(pages):
    pic_urls=[]
    for page in pages:
        urls=findall_in_page(page,'path":"','"')
        #print('urls',urls)
        pic_urls.extend(urls)
    return pic_urls

def download_pics(url,n):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r=requests.get(url,headers=header)
    path=base_path+'/'+str(n)+'.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    #下载完，解锁
    thread_lock.release()

def main(label):
    pages=page_from_duitang(label)
    pic_urls=pic_urls_from_pages(pages)
    n=0
    for url in pic_urls:
        n+=1
        print('正在下载第{}张图片'.format(n))
        #上锁
        thread_lock.acquire()
        t=threading.Thread(target=download_pics,args=(url,n))
        t.start()
main('校花')
