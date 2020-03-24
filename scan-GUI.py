from tkinter import *
from tkinter import scrolledtext
#from crawl import crawl
from config import proxies,threadCount,headers,xsschecker
from utils import getVar
import config
import requests
import re
from urllib.parse import urlparse
#import thread 
import concurrent.futures
import random
import copy
from filterChecker import filterChecker
from generator import generator
from requester import requester
from htmlparser import htmlParser
from photon import photon

#from tkinter.ttk import *
import tkinter.messagebox as mesgbox
import sys


#所以在定义全局变量的时候必须在执行crawl或者scan函数的时候定义才有效


    # target=''
    # path=''
    # jsonData=''
    # paramData=''
    # proxy=''
    # recursive=''#判断是否递归
def start():
    target=e1.get()#从GUI传入的待检测url参数
    #Scan_area.insert(END,target)
    config.globalVariables['target']=target#target赋值成功
    #Scan_area.insert(END,config.globalVariables['target'])
    threadCount=int(e2.get())#线程数情况
    Scan_area.insert(END,threadCount)
    config.globalVariables[threadCount]=threadCount#将线程数赋值为全局都可以使用的数值
    # skipDOM=''#
    timeout=config.timeout
    # encode=config.encode
    level=config.level#level表示的是爬虫爬取的深度
    delay=config.delay
    timeout=config.timeout
    config.globalVariables['headers']=headers
    config.globalVariables['checkedScripts']=set()
    config.globalVariables['checkedForms']={}
    #encoding=base64 if encode and encode=='base64' else False



    url=target
    scheme = urlparse(url).scheme
    host = urlparse(url).netloc
    main_url = scheme + '://' + host
    #Scan_area.insert(END,main_url)


    # show_message={'info':'the crawl results is:',}
    crawlingResult=photon(url,headers,level,threadCount,delay,timeout,False)#爬取页面的结果：表单和URL链接
    forms=crawlingResult[0]#获取爬取的表单，表单获取成功
    Scan_area.insert(END,forms[0])
    urls=crawlingResult[1]
    Scan_area.insert(END,urls)
    crawl(scheme,host,url,forms[0],headers,delay,timeout)
    # threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=threadCount)
    # futures = (threadpool.submit(crawl,scheme, host, main_url, form,headers, delay, timeout) for main_url , form in zip(urls, forms))
    # for i, _ in enumerate(concurrent.futures.as_completed(futures)):
    #     if i + 1 == len(forms) or (i + 1) % threadCount == 0:
    #         s='Progress: %i/%i\r\n' % (i + 1, len(forms))
    #         Scan_area.insert(END,s)

    # domURLs=list(crawlingResult[1])#爬虫爬出来的URL
    # difference=abs(len(domURLs)-len(forms))
    # if len(domURLs) > len(forms):
    #     for i in range(difference):
    #             forms.append(0)
    # elif len(forms) > len(domURLs):
    #     for i in range(difference):
    #         domURLs.append(0)

    # threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=threadCount)
    # futures = (threadpool.submit(crawl,scheme, host, main_url, form,headers, delay, timeout) for domURL , form in zip(domURLs, forms))
    # for i, _ in enumerate(concurrent.futures.as_completed(futures)):
    #     if i + 1 == len(forms) or (i + 1) % threadCount == 0:
    #         s='Progress: %i/%i\r\n' % (i + 1, len(forms))
    #         Scan_area.insert(END,s)





def crawl(scheme,host,main_url,form,headers,delay,timeout):
    if form:#这个form是一个表单，应该是从返回页面中提取出来的表单集合
        for each in form.values():
            url=each['action']
            url=main_url
            if url:
                # if url.startswith(main_url):
                #     pass
                # elif url.startswith('//') and url[2:].startswith(host):
                #     url=scheme+'://'+url[2:]
                # elif url.startswith('/'):
                #     url=scheme+'://'+host+url
                if url not in config.globalVariables['checkedForms']:
                    config.globalVariables['checkedForms'][url]=[]
                method=each['method']
                GET=True if method=='get' else False
                inputs=each['inputs']#一个form表单中的input标签的集合
                Scan_area.insert(END,inputs)
                paramData={}
                for one in inputs:
                    paramData[one['name']]=one['value']
                    for paramName in paramData.keys():
                        if paramName not in config.globalVariables['checkedForms'][url]:
                            config.globalVariables['checkedForms'][url].append(paramName)
                            paramsCopy=copy.deepcopy(paramData)
                            paramsCopy[paramName]=xsschecker
                            response=requester(url,paramsCopy,headers,GET,delay,timeout)#发送GET请求
                            #Scan_area.insert(END,response.text)
                            occurences=htmlParser(response,False)#返回的是html网页中输出点的上下文信息
                            positions=occurences.keys()#注入点位置
                            #模糊测试，判断xss漏洞的 匹配度？？
                            efficiences=filterChecker(url,paramsCopy,headers,GET,delay,occurences,timeout,False)
                            vectors=generator(occurences,response.text)#生成攻击向量？？
                            #存储攻击向量的数据结构
                            payloads=[]
                            if vectors:
                                for confidence,vects in vectors.items():
                                    try:
                                        payload=list(vects)[0]
                                        s="this is payload area"
                                        #Scan_area.insert(END,s)
                                        Scan_area.insert(END,payload)
                                        Scan_area.insert(END,'\n')
                                        payloads.append(payload)
                                        break
                                    except IndexError:
                                        pass



def scan():
    m=e1.get()
    Scan_area.insert(END,m)






root=Tk()#根窗口
root.title('XSScan')
root.iconbitmap("xss.ico")
#self.root.geometry('600x600')

#建立菜单栏
menuBar=Menu(root)
for item in["文件","个性化"]:
    menuBar.add_command(label=item)
root["menu"]=menuBar

#建立设置的子菜单栏
eMenu=Menu(menuBar)
for item in ["线程设置","爬虫设置"]:
    eMenu.add_command(label=item)
menuBar.add_cascade(label="设置",menu=eMenu)




#显示主页面的欢迎内容
frame_1=Frame(root,height=50,width=600)
frame_1.pack_propagate(0)#使得组件大小不变，此时height和width才起作用
frame_1.pack(side='top',fill='both')
label_e=Label(frame_1,text="Welcome To XSScan!",bg='green',font=('宋体',15),width=100,height=5).pack(side='top',fill='both')


#frame2中放扫描的URL和其他信息
frame_2=Frame(root,height=50,width=600)
frame_2.pack(side='top')
label_url=Label(frame_2,text="URL:",font=('宋体',10),width=10,height=2).grid(row=0,column=0)

#定义URL输入框的内容
e1=StringVar()
URL_entry=Entry(frame_2,textvariable=e1,width=50,font=('宋体',10)).grid(row=0,column=1)
config.globalVariables['main_url']=e1.get()
#Btn_act=Button(self.frame_2,text="开始扫描",bg='grey',command=self.scan).grid(row=0,column=2,sticky=E)


#线程数输入设计
e2=StringVar()
Label(frame_2,text="线程数:",font=('宋体',10),width=10,height=2).grid(row=1,column=0)
thread_entry=Entry(frame_2,textvariable=e2,width=15,font=('宋体',10)).grid(row=1,column=1,sticky=W)
config.globalVariables['thread_count']=e2.get()#设置线程数,保存在config的globalVariables中





#模式选择设计 是一个单选框 选项有crawl模式和 scan模式
e3=IntVar()
Label(frame_2,text="模式:",font=('宋体',10),width=10,height=2).grid(row=2,column=0)
mode_1=Radiobutton(frame_2,text="爬虫模式",value=1,variable=e3)
mode_1.grid(row=2,column=1,sticky=W)
mode_2=Radiobutton(frame_2,text="扫描模式",value=2,variable=e3)
mode_2.grid(row=3,column=1,sticky=W)



#frame_3用来输出扫描结果
frame_3=Frame(root,height=100,width=600).pack(side='top',fill='both')
Scan_area=scrolledtext.ScrolledText(frame_3,font=('宋体',10))
Scan_area.pack()
#Scan_area.insert(END,'liu')

#用户自定义参数
e4=StringVar()
Label(frame_2,text="参数设置:",font=('宋体',10),width=10,height=2).grid(row=4,column=0)
thread_entry=Entry(frame_2,textvariable=e4,width=15,font=('宋体',10)).grid(row=4,column=1,sticky=W)


Btn_act=Button(frame_2,text="开始扫描",bg='grey',command=start).grid(row=6,column=1,sticky=W)




root.mainloop()

#成功显示了



