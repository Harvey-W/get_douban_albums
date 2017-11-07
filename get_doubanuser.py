'''V1.0版
+++++++++++++++++++++
1. 实现搜索功能 X
2. 根据关键词抓取
3. 调试bug，异常处理
4. 不支持检索，很难区分同名
5. 只抓取第一个相册



+++++++++++++++++++++
'''




import urllib.request
import urllib.error
import urllib.parse
import os
from lxml import etree
import time

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36')
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print ('错误：',e.code,' 无此用户！')
        print ('=========================\n')
        download_imgs()
    except urllib.error.URLError as e:
        print ('错误：',e.reason,'（连接错误）请检查网络连接或重启程序！')
        time.sleep(2.5)
        exit(0)
    else:
        html = resp.read()
        return html

def imgs_store (url):
    folder = etree.HTML(url_open(url)).\
         xpath('//*[@id="db-usr-profile"]/div[1]/a/img/@alt')[0]
    if os.path.exists('Douban') == 0:
        os.mkdir('Douban')
        os.chdir('Douban')
        os.mkdir(folder)
        os.chdir(folder)
    else:
        os.chdir('Douban')
        if os.path.exists(folder) == 0:
            os.mkdir(folder)
            os.chdir(folder)
        else:
            os.chdir(folder)
            
    return folder

def get_imgs(url):
    html = etree.HTML(url_open(url))
    img_urllst = html.xpath('//a[@class="photolst_photo"]/img/@src')

    return img_urllst

def save_imgs(img_url):
    for each in img_url:
        img_name = each.split('/')[-1]
        with open(img_name,'wb') as f:
            img = url_open(each)
            f.write(img)

def download_imgs():
    doubanNAME = input('请输入豆瓣用户ID：\n')
    print ('=========================')
    main_url = 'https://www.douban.com/people/'\
               +urllib.parse.quote(doubanNAME)+'/photos'

    folder = imgs_store(main_url)    
    for i in range(1,5):
        time.sleep(0.5)
        print('.'*i)
    print ('用户名：%s'%folder)
    dots = [1,2,3,4]
    for dot in dots[::-1]:
        time.sleep(0.5)
        print('.'*dot)
    
    newest_album = etree.HTML(url_open(main_url)).\
                   xpath('//a[@class="album_photo"]/@href')[0]

    total_page = int(etree.HTML(url_open(newest_album)).\
                     xpath('//span/@data-total-page')[0])
    title = etree.HTML(url_open(newest_album)).\
            xpath('//title/text()')[0]
    print ('%s 共有%d页'%(title,total_page))
    
    for i in range(1,total_page+1):
        page_current = newest_album + '?start=' + str(18*(i-1))
        print('第%d页 --->'%i)
        img_url = get_imgs(page_current)
        save_imgs(img_url)

    print('\n相册生产完毕，请于同目录下Douban文件夹查看。')
    time.sleep(2.5)
    exit(0)
    
if __name__ == '__main__':
    download_imgs()
