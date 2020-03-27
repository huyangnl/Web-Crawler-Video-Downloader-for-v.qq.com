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

'''=====Gereral Setup====='''
#采集页面 url地址 xpath
xpathURL='//div[@class="feed_info"]//@href'
xpathTitle='//a[@class="feed_title"]/text()'
#采集记录存放地址
recordspath='/Users/huyang/Documents/python/My Python/qq.com/VideoRecords.csv'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


'''=====Main Function====='''
def Task(url,video_downloadpath,channel,TV):
    
    # 获取采集页面的信息并重新编码，放入一个DataFrame
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    mytree = etree.HTML(r.text)
    videorecords = pd.read_csv(recordspath)
    
    def get_url_list(): #获取网页中的视频地址
        url=mytree.xpath(xpathURL) 
        return url
    
    def get_url_linkname(): #获取网页中的视频标题
        linkname=mytree.xpath(xpathTitle)
        return linkname
    
    def download_video(start_url): #用you-get开始下载
        if os.system('you-get -o {path} {url}'.format(path=video_downloadpath,url=start_url)) == 0: # 如果下载命令行执行成功， os.system()返回0值，成功下载标签downloaded设为1
            downloaded = 1
        else: #下载命令行执行不成功
            downloaded = 0
        return downloaded;
    
    def write_record(timestr,start_url,linkname): #写入下载记录
        new_record = {'date':timestr,'url':start_url,'title':linkname,'downloaded':1,'uploaded':0}
        global videorecords
        videorecords = videorecords.append(new_record, ignore_index = True)
        
    def File_rename(): #批量处理下载文件夹内的视频标题，加入日期/来源信息
        fileList = os.listdir(video_downloadpath)
        n=0
        for i in fileList:
            if i != '.DS_Store': # MacOS目录下默认有一个隐藏文件，要跳过
                if i[0] != '【':  # 文件名第一个字符是中括号，说明已经被重命名过一次了，跳过                  
                    oldname=video_downloadpath + os.sep + i   # os.sep添加系统分隔符
                    newname=video_downloadpath + os.sep + Date + i[:-4] + channel + TV + '.mp4'
                    os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
                    print(oldname,'======>',newname)
                    n+=1
                else:
                    continue
            else:
                continue
        print('本次下载/更名一共{}个文件'.format(n))
        
    # 执行Task的主程序
    urls=get_url_list() # 获取要下载的视频地址列表
    linknames=get_url_linkname() # 获取要下载的视频标题列表
    named_tuple = time.localtime()
    timestr = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple) # 获取下载文件的执行时间戳
    Date = time.strftime("【%Y%m%d】", named_tuple) # 获取Task执行日期
    for i in urls: # 遍历视频地址列表
        start_url='https:{i}'.format(i=i) # 重新构造完整的下载地址
        linkname=linknames[urls.index(i)] # 用下载地址索引在标题列表里找到该视频对应的标题
        if start_url in videorecords['url'].values: # 这个视频之前是否被下载记录过？
            print('已有记录:', start_url, linkname)
            continue #已有记录 跳出循环 执行下一个链接地址检查
        else:
            print('新记录:', start_url, linkname)
        if download_video(start_url) == 0: # 开始下载，如果下载不成功，跳出循环
            continue
        else: # 下载成功，则调用写记录函数，向记录中追加一条新记录
            write_record(timestr,start_url,linkname)
 
    File_rename() # 全部下载完成，执行改名函数，对视频目录文件批量改名
    videorecords.to_csv(recordspath, encoding='utf_8_sig',index=0) # 写入下载记录csv文件保存
    print('========本次下载记录已保存，运行结束！=========')

'''=====Task Lists====='''

Task('https://v.qq.com/vplus/7d66b5aaee4a4296#uin=7d66b5aaee4a4296?page=video','/Users/huyang/Documents/python/My Python/qq.com/videos/帮女郎','【帮女郎大视野】','【湖南公共频道】')
Task('https://v.qq.com/vplus/65586ea58193e745a25e9827b38c171e#uin=65586ea58193e745a25e9827b38c171e?page=index','/Users/huyang/Documents/python/My Python/qq.com/videos/湖南经视','【经视新闻】','【湖南经视】')
Task('https://v.qq.com/vplus/41e98d08f3d241cee370ba49c9e883e0#uin=41e98d08f3d241cee370ba49c9e883e0?page=video','/Users/huyang/Documents/python/My Python/qq.com/videos/湖南笑工厂','【湖南笑工厂】','')
Task('https://v.qq.com/vplus/28e8a2ced275f7be67d5bd9617482a49?page=index','/Users/huyang/Documents/python/My Python/qq.com/videos/株洲的脱口秀','【株洲的脱口秀】','')
    



