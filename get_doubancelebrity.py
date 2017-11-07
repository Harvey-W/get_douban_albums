print('''
V1.2版
+++++++++++++++++++++
1. 实现搜索功能
2. 判断输入错误，连接错误；判断有无收录和相册
3. 无图片、单页和多页均可分辨
4. 已实现完美提取info和intro
5. 遗留小彩蛋：如果A无图片时，则下一查找B的图片会直接存在A这个人名下
*6. 展现复杂交互：明星关系图-通过合作次数


update:
v1.2 - 完美提取info和intro

v1.1 - 加入逻辑判断和异常处理

v1.0 - 基础功能
+++++++++++++++++++++
''')




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
         xpath('//a[@class="nbg"]/@title')[0]
    print(folder)
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

def get_info(main_url):
    info = etree.HTML(url_open(main_url)). \
           xpath('//*[@id="headline"]/div[2]//li')
    
    dots = [1,2,3,4]
    for i in range(1,5):
        time.sleep(0.5)
        print('.'*i)
    for e in info:
        content = e.xpath('string(.)').replace('\n','').replace(' ','')
        print(content)
    for dot in dots[::-1]:
        time.sleep(0.5)
        print('.'*dot)
    print ('=========================\n') 

def get_intro(main_url):
    print ('\n影人简介 · · · · · ·\n')
    content = etree.HTML(url_open(main_url)).\
              xpath('//span[@class="all hidden"]/text()')
    if content == []:
        content = etree.HTML(url_open(main_url)).\
              xpath('//div[@id="intro"]/div[@class="bd"]/text()')
        
    for i in content:
        print (i)
    print ('=========================\n') 

def get_imgs(url):
    html = etree.HTML(url_open(url))
    img_urllst = html.xpath('//div[@class="cover"]/a/img/@src')

    return img_urllst

def save_imgs(img_url):
    for each in img_url:
        img_name = each.split('/')[-1]
        with open(img_name,'wb') as f:
            img = url_open(each)
            f.write(img)

def download_imgs():
    doubanNAME = input('请输入爱豆的姓名：\n')
    print ('=========================')
    search_url = 'https://movie.douban.com/celebrities/search?search_text='\
               + urllib.parse.quote(doubanNAME)

    try:
        main_url = etree.HTML(url_open(search_url)).\
                   xpath('//h3/a/@href')[0]
    except IndexError as e:
        print('呃..看来是没收录TA！')
        print ('=========================\n')
        download_imgs()
        
    #介绍
    folder = imgs_store(main_url)
    category = get_info(main_url)
    intro = get_intro(main_url) 

    #相册
    album_url = main_url + 'photos/?&sortby=time'

    has_imgs = etree.HTML(url_open(album_url)).\
                     xpath('//div[@class="cover"]/a/@href')
    if has_imgs ==[]:
        print('呃..TA还没有照片！')
        print ('=========================\n')
        time.sleep(2.5)
        download_imgs()
    else:
        total_page = etree.HTML(url_open(album_url)).\
                     xpath('//span/@data-total-page')
        if total_page ==[]:
            img_url = get_imgs(album_url)
            save_imgs(img_url)
            print('您的爱豆只有一页照片喔！ --->')
            print('\n相册生产完毕，请于同目录下Douban文件夹查看。')
            time.sleep(2.5)
            exit(0)
        else:
            total_page = int(total_page[0])
            title = etree.HTML(url_open(album_url)).\
                    xpath('//div[@id="content"]/h1/text()')[0]
            print ('\t%s \n\t\t共有%d页'%(title,total_page))
            
            for i in range(1,total_page+1):
                page_current = album_url + '&start=' + str(30*(i-1))
                print('第%d页 --->'%i)
                img_url = get_imgs(page_current)
                save_imgs(img_url)

            print('\n相册生产完毕，请于同目录下Douban文件夹查看。')
            time.sleep(2.5)
            exit(0)
    
if __name__ == '__main__':
    download_imgs()
