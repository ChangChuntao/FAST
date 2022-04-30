#!/usr/bin/python3
# ARG_Mode       : Program running with arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.04.12 - Version 1.10


import os
from ARG_Sub import GET_ARG, ARG_ifwrong, geturl
from Dowload import argpooldownload, lftps, wgets
from FTP_Source import FTP_S
from Format import unzip_vlbi, unzipfile
from Get_Ftp import ReplaceMMM


# 2022-03-27 : 输入参数模式主函数 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#              by Chang Chuntao  -> Version : 1.10
def ARG_Mode(argument):
    # PrintGDD("GDD 下载程序启动!", "important")
    cddarg = {"datatype": "", "year": 0, "loc": "", "day1": 0, "day2": 0, "month": 0, "file": "", "process": 12,
              "site": "", "uncompress": "y"}
    cddarg = GET_ARG(argument, cddarg)  # 获取参数内容
    ARG_ifwrong(cddarg)  # 判断输入参数正确性

    if cddarg['datatype'] == "IVS_week_snx":
        nowdir = os.getcwd()
        if len(cddarg["loc"]) == 0:
            os.chdir(nowdir)
        else:
            os.chdir(cddarg["loc"])
        ftpsite = FTP_S[cddarg['datatype']][0]
        ftpsite = ftpsite.replace('<YY>', str(cddarg['year'])[2:4])
        ftpsite = ReplaceMMM(ftpsite, cddarg['month'])
        lftps(ftpsite)
        if cddarg["uncompress"] == "y" or cddarg["uncompress"] == "Y":
            unzip_vlbi(cddarg["loc"], ftpsite)

    elif cddarg['datatype'] == "P1C1" or cddarg['datatype'] == "P1P2" or cddarg['datatype'] == "P2C2":
        nowdir = os.getcwd()
        if len(cddarg["loc"]) == 0:
            os.chdir(nowdir)
        else:
            os.chdir(cddarg["loc"])
        ftpsite = FTP_S[cddarg['datatype']]
        for ftp in ftpsite:
            ftp = ftp.replace('<YY>', str(cddarg['year'])[2:4])
            ftp = ftp.replace('<YYYY>', str(cddarg['year']))
            ftp = ReplaceMMM(ftp, cddarg['month'])
            wgets(ftp)
        if cddarg["uncompress"] == "Y" or cddarg["uncompress"] == "y":
            unzipfile(cddarg["loc"], ftpsite)

    else:
        urllist = geturl(cddarg)  # 判断下载列表
        argpooldownload(urllist, cddarg["process"], cddarg["loc"], cddarg["uncompress"])  # 并行下载
