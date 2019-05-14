import requests,random
from bs4 import BeautifulSoup
import lxml
import json
from selenium import webdriver
import time

def phantom_browser():
    """使用phantom先预算滚轮滚到2000像素的总共数据"""
    bro = webdriver.PhantomJS(executable_path='./phantomjs')

    print('\033[33;1m开始预算....\033[0m')
    bro.get('https://movie.douban.com/chart')
    print('正在访问电影排行榜，请稍候')
    time.sleep(1)
    # bro.save_screenshot('./db/base.png')

    # 经测试，各种分类的url的xpath值为1-29
    # kind_id_list =  [i for i in range(1,39)]
    # kind_list = [
    #     '剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','纪录片','短片','情色','同性',\
    #     '音乐','歌舞','家庭','儿童','传记','历史','战争','犯罪','西部','奇幻','冒险','灾难','武侠','古装','运动','黑色电影']
    # kind_id = random.choice(kind_id_list)
    # a = bro.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div/span[%s]/a'%kind_id)

    '但是由于此xpath与不同分类的id值并不能和后面ajax请求url带的参数分类id对应'
    '所以暂且固定取分类为“剧情”的电影数据'

    a = bro.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div/span[1]/a')
    a.click()
    print('正在访问剧情分类下电影，请稍候')
    time.sleep(4)
    # bro.save_screenshot('./db/2.png')
    # 滑动滚轮到2000像素
    js = 'window.scrollTo(0,2000)'
    bro.execute_script(js)
    print('正在访问滑动2000像素之后的数据，请稍候')
    time.sleep(3)
    bro.save_screenshot('./db/all.png')
    print('--------预算完毕，开始下载数据-------')

def main(start=0,types=11,limit=20):
    """主函数，请求分类下的电影数据"""

    # starts 为当前页开始第一个数据
    # types 为电影分类
    # limit 为每页最多显示个数

    session = requests.session()
    # 请求参数
    data = {
        'source':'movie',
        # 'redir':'https://movie.douban.com/typerank?type_name=%s&type=6&interval_id=100:90&action='%kind,
        'form_email':'15027900535',
        'form_password':'bobo@15027900535',
        'login':'登录'
    }
    # 请求头
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # 代理
    proxy_list = [{
        'http':'39.137.2.214:8080'
    },{
        'http':'221.7.255.167:8080'
    },{
        'http':'39.137.2.218:8080'
    }]

    # 登录并保存cookie
    login_url = 'https://accounts.douban.com/login'
    session.post(url = login_url,data = data,headers = header,proxies=random.choice(proxy_list))

    # 停顿1秒请求电影数据
    time.sleep(1)
    request_url = 'https://movie.douban.com/j/chart/top_list'

    # 请求参数
    param = {
        'type':'11',
        'interval_id':'100:90',
        'action':'',
        'start':start,
        'limit':limit
    }
    response = session.get(url=request_url,headers=header,proxies=random.choice(proxy_list),params = param)
    # 返回的数据是json字符串，反解json数据
    content_list = json.loads(response.text)
    message = ''

    for movie in content_list:
        try:
            poster_img = movie.get('cover_url')         #海报
            name = movie.get('title')                   #名称
            print('正在下载《%s》的相关数据'%name)
            actors = movie.get('actors')                #主演
            types = movie.get('types')                  #类型
            release_date = movie.get('release_date')    #上映时间
            score = movie.get('score')                  #评分
            movie_url = movie.get('url')                #详情页url

            # 第二次请求电影详情页，为了获得语言、导演、编剧、时长字段的值
            time.sleep(1)
            detail = session.get(url=movie_url,headers= header,proxies=random.choice(proxy_list)).text

            # 解析数据
            soup = BeautifulSoup(detail,'lxml')
            result = soup.find(id='info')
            director = result.find(rel="v:directedBy").text                 #导演
            screenwriter = result.find_all('span',class_='attrs')[1].text   #编剧
            time_length = result.find(property="v:runtime").text            #时长

            # 字符串解析，获取语言
            strs = result.text
            lang = strs[strs.find('语言: ')+len('语言: '):strs.find('上映日期')].replace('\n','')

            # 拼接所获得的数据
            message += "海报url: %s\n"\
                       "电影名称: %s\n" \
                       "导演: %s\n" \
                       "编剧: %s\n" \
                       "主演: %s\n" \
                       "类型: %s\n" \
                       "语言: %s\n" \
                       "上映日期: %s\n" \
                       "片长: %s\n" \
                       "豆瓣评分: %s\n\n\n"%(poster_img,name,director,screenwriter,actors,types,lang,release_date,
                               time_length,score
                                     )
        except AttributeError as e:
            print('\033[32;1m《%s》详情页不存在\033[0m'%name)
            print(e)
    # 持久化存储
    f.write(message)


if __name__ == '__main__':
    phantom_browser()
    '根据上面测试，滑动滚轮到2000像素时，只再做了一次ajax请求，默认一页加载20个数据，总共则为40'

    # 标准版爬虫
    f = open('./db/douban.json','w',encoding='utf-8')
    for start in [0,20]:
        main(start=start)
    f.close()

    # 暴力版爬虫，一次性获取多个数据，不需要循环翻页ajax请求，总共只请求一次
    # f = open('./db/douban_violence.json','w',encoding='utf-8')
    # limit = input('请输入需要爬取个数：')
    # if limit.isdigit():
    #     main(limit=limit)
    print('-----------end--------------')

