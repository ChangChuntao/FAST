#!/usr/bin/python3
# Download       : Sub functions required by the download module
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.25
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.11.02 - Version 1.25

import os
import sys
import time
import timeit
from multiprocessing.pool import ThreadPool
import platform
from ARG_Sub import uncompress_arg
from FAST_Print import PrintGDD
from Format import isinpath


if platform.system() == 'Windows':
    """
    2022-03-27 : 判断操作平台，获取bin下下载程序    by Chang Chuntao -> Version : 1.00
    2022-09-16 : 更新索引位置                    by Chang Chuntao -> Version : 1.21
    """
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    PrintGDD('当前为Windows系统', "important")
    wget = os.path.join(dirname, 'bin', 'wget.exe')
    lftp = os.path.join(dirname, 'bin', 'lftp')
    wget += " -T 3 -t 10 -N -c "
    lftp += ' '
else:
    PrintGDD('当前为Linux系统', "important")
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    wget = os.path.join(dirname, 'bin', 'wget')
    lftp = os.path.join(dirname, 'bin', 'lftp')
    wget += " -T 3 -t 10 -N -c "
    lftp += ' '


def wgets(fn):  # 下载单个文件
    """
    2022-03-27 : 调取wget下载单个文件 by Chang Chuntao -> Version : 1.00
    """
    if isinpath(fn.split("/")[-1]):
        return 0
    else:
        cmd = wget + fn
        print(cmd)
        os.system(cmd)


def wgetm(url):  # 下载列表内文件
    """
    2022-03-27 : 通过下载列表调取wget下载单个文件 by Chang Chuntao -> Version : 1.00
    """
    for fn in url:
        file = fn.split("/")[-1]
        if isinpath(file):
            # PrintGDD("文件已经存在：" + file + "!", "warning")
            return 0
        else:
            PrintGDD("正在下载文件：" + file + "!", "normal")
            try:
                wgets(fn)
                # PrintGDD("文件下载结束：" + file + "!", "normal")
            except IOError:
                continue
            else:
                continue


def lftps(url):
    """
    2022-03-27 : 通过下载列表调取lftp下载文件 by Chang Chuntao -> Version : 1.00
    """

    cmd = lftp + url
    os.system(cmd)
    time.sleep(0.1)


def cddpooldownload(urllist, process):
    """
    2022-03-27 : 引导模式并发下载子程序 by Chang Chuntao -> Version : 1.00
    """
    PrintGDD("正在开始下载!", "important")
    print("")
    start_time = timeit.default_timer()
    pool = ThreadPool(process)
    pool.map(wgetm, urllist)
    pool.close()
    pool.join()
    end_time = timeit.default_timer() - start_time
    PrintGDD("全部下载结束!", "important")
    PrintGDD("程序运行时间 : %.02f seconds" % end_time, "important")


def argpooldownload(urllist, process, loc, compress):
    """
    2022-03-27 : 参数输入模式并发下载子程序 by Chang Chuntao -> Version : 1.00
    """
    nowdir = os.getcwd()
    if len(loc) == 0:
        os.chdir(nowdir)
    else:
        os.chdir(loc)
    PrintGDD("正在开始下载!", "important")
    print("")
    start_time = timeit.default_timer()
    for typeurl in urllist:
        pool = ThreadPool(process)
        pool.map(wgetm, typeurl)
        pool.close()
        pool.join()
    if compress == "Y" or compress == "y":
        # unzip_format(loc)
        uncompress_arg(loc, urllist)
    end_time = timeit.default_timer() - start_time
    PrintGDD("全部下载结束!", "important")
    PrintGDD("程序运行时间 : %.02f seconds" % end_time, "important")
    os.chdir(nowdir)
