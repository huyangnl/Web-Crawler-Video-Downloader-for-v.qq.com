#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 23:53:39 2020

@author: huyang
"""
import requests
from lxml import etree#xpath
import os
import pandas as pd
import time

'''=====主函数====='''
def Task(url,video_downloadpath,channel,TV):

    def get_url_list(): #获取网页中的视频地址
        url=mytree.xpath(xpathURL) 
        return url
    
    def get_url_linkname(): #获取网页中的视频标题
        linkname=mytree.xpath(xpathTitle)
        return linkname
     
    def write_record(timestr,start_url,linkname,downloaded,uploaded): #写入下载记录
        new_record = {'date':timestr,'url':start_url,'title':linkname,'downloaded':downloaded,'uploaded':0}
        global VideoRecords
        VideoRecords = VideoRecords.append(new_record, ignore_index = True)
        
    def download_video(start_url): #用you-get开始下载
        if os.system('you-get -o {path} {url}'.format(path=video_downloadpath,url=start_url)) == 0: 
            write_record(timestr,start_url,linkname,1,0)
        
    def File_rename(): #批量处理下载文件夹内的视频标题，加入日期/来源信息  
        renamefileList = os.listdir(video_downloadpath)
        print('***下载文件夹有{}个文件，开始更名'.format(len(renamefileList)-1))
        m=0
        for i in renamefileList:
            if i != '.DS_Store': # MacOS目录下默认有一个隐藏文件，要跳过
                if i[0] == '【' or i[-8:-1] =='download':  # 文件名第一个字符是中括号，说明已经被重命名过一次了; 文件名末尾是download，说明下载未完成，跳过
                    continue
                else:
                    oldname=video_downloadpath + os.sep + i   # os.sep添加系统分隔符
                    newname=video_downloadpath + os.sep + Date + i[:-4] + channel + TV + '.mp4'
                    os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
                    m+=1
        print('***一共更名完成{}个文件 \n'.format(m))
        
            
    # 获取采集页面的信息并重新编码，放入一个DataFrame
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    mytree = etree.HTML(r.text)
    VideoRecords = pd.read_csv(Recordscsv)
    fileList = os.listdir(video_downloadpath)
    
    # 执行Task的主程序
    urls=get_url_list() # 获取要下载的视频地址列表
    linknames=get_url_linkname() # 获取要下载的视频标题列表
    named_tuple = time.localtime()
    timestr = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple) # 获取下载文件的执行时间戳
    Date = time.strftime("【%Y%m%d】", named_tuple) # 获取Task执行日期
    print('========任务名：{}========='.format(channel))
    n=0
    for i in urls: # 遍历视频地址列表
        start_url='https:{i}'.format(i=i) # 重新构造完整的下载地址
        linkname=linknames[urls.index(i)] # 用下载地址索引在标题列表里找到该视频对应的标题
        if start_url in VideoRecords['url'].values: # 视频记录已存在
            continue #跳出循环 执行下一个链接地址检查
        else: #视频记录不存在
            print('新记录:', start_url, linkname)
        download_video(start_url)
        n += 1
        
    VideoRecords.to_csv(Recordscsv, encoding='utf_8_sig',index=0) # 写入下载记录csv文件保存
        
    if n == 0:
        print('***本次没有下载任何文件')
    else:
        print('***下载{}条记录成功'.format(n))

    if len(fileList) <= 1:
        print('***下载文件夹空 \n')
    else:
        File_rename() # 全部下载完成，执行改名函数，对视频目录文件批量改名


'''=====通用设置====='''
#采集页面 url地址 xpath
xpathURL='//div[@class="feed_info"]//@href'
xpathTitle='//a[@class="feed_title"]/text()'
#采集记录存放地址
Recordscsv='/Users/huyang/Documents/python/My Python/qq.com/VideoRecords.csv'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

'''=====Task Lists====='''
Task('https://v.qq.com/vplus/7d66b5aaee4a4296#uin=7d66b5aaee4a4296?page=video','/Users/huyang/Movies/Youtubecache/帮女郎','【帮女郎大视野】','【湖南公共频道】')
Task('https://v.qq.com/vplus/65586ea58193e745a25e9827b38c171e#uin=65586ea58193e745a25e9827b38c171e?page=index','/Users/huyang/Movies/Youtubecache/湖南经视','【经视新闻】','【湖南经视】')
Task('https://v.qq.com/vplus/41e98d08f3d241cee370ba49c9e883e0#uin=41e98d08f3d241cee370ba49c9e883e0?page=video','/Users/huyang/Movies/Youtubecache/湖南笑工厂','【湖南笑工厂】','')
Task('https://v.qq.com/vplus/28e8a2ced275f7be67d5bd9617482a49?page=index','/Users/huyang/Movies/Youtubecache/株洲的脱口秀','【株洲的脱口秀】','')
Task('https://v.qq.com/vplus/8b58a07cdebda4ecced49e3d6d74a98f#uin=8b58a07cdebda4ecced49e3d6d74a98f?page=video','/Users/huyang/Movies/Youtubecache/都市1时间','【都市1时间】','【湖南都市频道】')
Task('https://v.qq.com/vplus/7e98174dbea4e215bcfe344f11a106c5#uin=7e98174dbea4e215bcfe344f11a106c5?page=video','/Users/huyang/Movies/Youtubecache/长沙军哥','【长沙军哥】','')
Task('https://v.qq.com/vplus/6e02875647660256def1e7c7ee68744c#uin=6e02875647660256def1e7c7ee68744c?page=video','/Users/huyang/Movies/Youtubecache/都市晚间','【都市晚间】','【湖南都市频道】')
print('''
========全部任务运行结束=========

          ''')
