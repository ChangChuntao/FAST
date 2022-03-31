#!/usr/bin/python3
# ARG_Mode       : Program running with arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.27

from ARG_Sub import GET_ARG, ARG_ifwrong, geturl
from Dowload import argpooldownload, lftps
from FTP_Source import FTP_S
from Get_Ftp import ReplaceMMM
from Format import unzip_format


def ARG_Mode(argument):
    # PrintGDD("GDD 下载程序启动!", "important")
    cddarg = {"datatype": "", "year": 0, "loc": "", "day1": 0, "day2": 0, "month": 0, "file": "", "process": 12,
              "site": "", "uncompress": "y"}
    cddarg = GET_ARG(argument, cddarg)  # 获取参数内容
    ARG_ifwrong(cddarg)  # 判断输入参数正确性
    if cddarg['datatype'] == "IVS_week_snx":
        ftpsite = FTP_S[cddarg['datatype']][0]
        ftpsite = ftpsite.replace('<YY>', str(cddarg['year'])[2:4])
        ftpsite = ReplaceMMM(ftpsite, cddarg['month'])
        lftps(ftpsite)
        if "uncompress" == "y" or "uncompress" == "Y":
            unzip_format(cddarg["loc"])
    else:
        urllist = geturl(cddarg)  # 判断下载列表
        argpooldownload(urllist, cddarg["process"], cddarg["loc"], cddarg["uncompress"])  # 并行下载

