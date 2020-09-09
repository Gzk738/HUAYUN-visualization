# -*- encoding: utf-8 -*-
'''
@File    :   demo01.py.py
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/9/9 9:58   gxrao      1.0         None
'''
import threading
import time

flog = 0
threadLock = threading.Lock()

class myThread_0 (threading.Thread):
    def run(self):
        global flog
        while True:
            threadLock.acquire()
            flog = flog + 1
            threadLock.release()
            print(flog)
            time.sleep(1)

class myThread_1 (threading.Thread):
    def run(self):
        global flog
        while True:
            threadLock.acquire()
            flog = flog - 1
            threadLock.release()
            print(flog)
            time.sleep(1)
# 创建新线程
thread1 = myThread_0()
thread2 = myThread_1()

# 开启新线程
thread1.start()
thread2.start()

