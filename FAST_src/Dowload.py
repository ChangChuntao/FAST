#!/usr/bin/python3
# Download       : Sub functions required by the download module
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.27

import os
import sys
import time
import timeit
from multiprocessing.pool import ThreadPool
import platform
from FAST_Print import PrintGDD
from Format import unzip_format

dirname = os.path.split(os.path.abspath(sys.argv[0]))[0]
if platform.system() == 'Windows':
    PrintGDD('当前为Windows系统', "important")
    wget = dirname + "\\bin\\wget.exe" + " -T 5 -t 1 "
    lftp = dirname + "\\bin\\lftp.exe" + " "
else:
    PrintGDD('当前为Linux系统', "important")
    wget = "wget -T 3 -t 1 "
    lftp = "lftp "


def isinpath(file):  # 判断相关文件是否存在
    orifile = str(file).split(".")[0]
    if len(orifile) > 9:
        filelowo = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
        filelowd = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        filelowp = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
        filelown = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "n"
        fileprolow = file.lower()[0:4] + file.lower()[16:20] + ".bia"
    else:
        filelowo = file.lower()[0:11] + "o"
        filelowd = file.lower()[0:11] + "d"
        filelowp = file.lower()[0:11] + "p"
        filelown = file.lower()[0:11] + "n"
        fileprolow = file.lower()[0:12]
    gzdfile = filelowd + ".gz"
    zdfile = filelowd + ".Z"
    gzofile = filelowo + ".gz"
    zofile = filelowo + ".Z"
    filebialowZ = fileprolow + ".Z"
    filebialowgz = fileprolow + ".gz"
    if os.path.exists(file) or os.path.exists(file[0:-2]) or os.path.exists(file[0:-3]) \
            or os.path.exists(filelowo) or os.path.exists(filelowd) \
            or os.path.exists(gzdfile) or os.path.exists(zdfile) \
            or os.path.exists(gzofile) or os.path.exists(zofile) \
            or os.path.exists(filelowp) or os.path.exists(filelown)\
            or os.path.exists(filebialowgz) or os.path.exists(filebialowZ):
        return True
    else:
        return False


def wgets(fn):  # 下载单个文件
    if isinpath(fn.split("/")[-1]):
        return 0
    else:
        cmd = wget + fn
        os.system(cmd)


def wgetm(url):  # 下载列表内文件
    for fn in url:
        file = fn.split("/")[-1]
        if isinpath(file):
            # PrintGDD("文件已经存在：" + file + "!", "warning")
            return 0
        else:
            PrintGDD("正在下载文件：" + file + "!", "normal")
            try:
                wgets(fn)
                PrintGDD("文件下载结束：" + file + "!", "normal")
            except IOError:
                continue
            else:
                continue


def lftps(url):  # lftp批量下载
    PrintGDD("正在开始下载!", "important")
    print("")
    start_time = timeit.default_timer()
    cmd = lftp + url
    os.system(cmd)
    time.sleep(0.1)
    end_time = timeit.default_timer() - start_time
    PrintGDD("全部下载结束!", "important")
    PrintGDD("程序运行时间 : %.02f seconds" % end_time, "important")


def cddpooldownload(urllist, process):
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
        unzip_format(loc)
    end_time = timeit.default_timer() - start_time
    PrintGDD("全部下载结束!", "important")
    PrintGDD("程序运行时间 : %.02f seconds" % end_time, "important")
    os.chdir(nowdir)
