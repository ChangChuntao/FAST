#!/usr/bin/python3
# CDD_Sub        : Format conversion subroutine
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.21
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.09.16 - Version 1.21

import os
import platform
import sys
import time
from FAST_Print import PrintGDD

from GNSS_Timestran import gnssTime2datetime, datetime2GnssTime


# 2022-03-27 : 判断文件在本地是否存在 by Chang Chuntao -> Version : 1.00
# 2022-09-09 : > 修正广播星历文件判定
#              by Chang Chuntao  -> Version : 1.20
def isinpath(file):  # 判断相关文件是否存在
    orifile = str(file).split(".")[0]
    if len(orifile) > 9:
        filelowo = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
        filelowd = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        filelowp = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
        fileprolow = file.lower()[0:4] + file.lower()[16:20] + ".bia"
        sp3filelow = file
        filelown = file
    elif orifile.split(".")[-1] == "SP3":
        year = file.lower()[11:15]
        doy = file.lower()[15:18]
        specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
        [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
        sp3filelow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".sp3"
        filelowo = file
        filelowd = file
        filelowp = file
        filelown = file
        fileprolow = file
    else:
        filelowo = file.lower()[0:11] + "o"
        filelowd = file.lower()[0:11] + "d"
        filelowp = file.lower()[0:11] + "p"
        filelown = file.lower()[0:11] + "n"
        fileprolow = file.lower()[0:12]
        sp3filelow = file
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
            or os.path.exists(filelowp) or os.path.exists(filelown) \
            or os.path.exists(filebialowgz) or os.path.exists(filebialowZ) \
            or os.path.exists(sp3filelow):
        return True
    else:
        return False


"""
2022-03-27 : 判断操作平台，获取bin下格式转换程序      by Chang Chuntao -> Version : 1.00
2022-09-16 : 更新索引                            by Chang Chuntao -> Version : 1.21
"""
if platform.system() == 'Windows':
    dirname = os.path.split(os.path.abspath(sys.argv[0]))[0]
    unzip = os.path.join(dirname, 'bin', 'gzip.exe')
    unzip += " -d "
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx.exe')
    crx2rnx += " "
else:
    dirname = os.path.split(os.path.abspath(sys.argv[0]))[0]
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx')
    crx2rnx += ' '
    unzip = 'uncompress '


# 2022-03-27 : 解压单个文件 by Chang Chuntao -> Version : 1.00
def uncompresss(file):
    if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz":
        cmd = unzip + file
        os.system(cmd)


# 2022-03-27 : crx2rnx by Chang Chuntao -> Version : 1.00
def crx2rnxs(file):
    if file[-3:-1].isdigit() and file[-1] == "d":
        cmd = crx2rnx + file
        os.system(cmd)


# 2022-03-27 : crx更名为d by Chang Chuntao -> Version : 1.00
def crx2d(file):
    if file.split(".")[-1] == "crx":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        os.rename(file, filelow)


# 2022-03-27 : BRDM长名更名为brdm短名 by Chang Chuntao -> Version : 1.00
def renamebrdm(file):
    if file.split(".")[-1] == "rnx" and file[0:4] == "BRDM":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
        os.rename(file, filelow)
    if file.split(".")[-1] == "rnx" and file[0:4] == "BRDC":
        filelow = "brdm" + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
        os.rename(file, filelow)


#
def renamesp3(file):
    if file.split(".")[-1] == "SP3":
        if file.split("_")[0] == "WUM0MGXULA":
            pass
        else:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            filelow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".sp3"
            os.rename(file, filelow)


# 2022-03-27 : 解压vlbi文件 by Chang Chuntao -> Version : 1.00
def unzip_vlbi(path, ftpsite):
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    dirs = os.listdir(path)
    for filename in dirs:
        if ftpsite[83:88] == filename[0:5] and filename.split(".")[-1] == "gz":
            uncompresss(filename)


#  2022.04.12 : 通过下载列表解压相应文件 by Chang Chuntao -> Version : 1.10
def unzipfile(path, ftpsite):
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if os.path.exists(zipfilename):
            uncompresss(zipfilename)
    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-3:-1].isdigit() or filename.split(".")[-1] == "crx":
            if filename.split(".")[-1] == "crx" or filename[-1] == "d":
                PrintGDD("目录内含有crx文件，正在进行格式转换！", "normal")
                break
    for filename in dirs:
        if filename.split(".")[-1] == "crx":
            crx2d(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-1] == "d" and filename[-3:-1].isdigit():
            crx2rnxs(filename)
            time.sleep(0.1)
            os.remove(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDM":
            renamebrdm(filename)
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDC":
            renamebrdm(filename)
    os.chdir(nowdir)
