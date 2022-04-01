#!/usr/bin/python3
# CDD_Mode       : Direct run program mode
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.27

from CDD_Sub import *
from Dowload import cddpooldownload, wgets, lftps
from FTP_Source import FTP_S
from FAST_Print import PrintGDD
from GNSS_TYPE import gnss_type, objneedyd1d2loc, objneedn, objneedydqd2
from Get_Ftp import ReplaceMMM, getftp, ReplaceMM


def CDD_Mode():
    print("==================================================================================")
    print("      FAST           : Fusion Abundant multi-Source data download Terminal")
    print("      Author         : Chang Chuntao")
    print("      Copyright(C)   : The GNSS Center, Wuhan University & ")
    print("                       Chinese Academy of Surveying and mapping")
    print("      Latest Version : 1.00")
    print("      Date           : 2022.01.14")
    obj = top_cdd()  # 一级目录 obj：一级索引
    subnum = sub_cdd(obj)  # 二级目录 subnum：二级索引
    cddarg = {'datatype': gnss_type[obj - 1][1][subnum - 1]}  # 索引数据类型
    PrintGDD("数据类型为" + cddarg['datatype'], "normal")
    urllist = []  # 下载列表

    if cddarg['datatype'] == "IVS_week_snx":
        ftpsite = FTP_S[cddarg['datatype']][0]
        [year, month] = ym_cdd()  # 获取下载时间
        ftpsite = ftpsite.replace('<YY>', str(year)[2:4])
        ftpsite = ReplaceMMM(ftpsite, month)
        lftps(ftpsite)
        getuncompress()

    elif cddarg['datatype'] == "HY_SLR":
        ftpsite = FTP_S[cddarg['datatype']]
        [year, month] = ym_cdd()  # 获取下载时间
        for ftp in ftpsite:
            ftp = ftp.replace('<YYYY>', str(year))
            ftp = ReplaceMM(ftp, month)
            wgets(ftp)

    else:
        if obj in objneedydqd2:  # 输入为年， 起始年积日， 终止年积日 的数据类型
            [year, day1, day2] = yd_cdd()  # 获取下载时间
            cddarg['year'] = year
            cddarg['day1'] = day1
            cddarg['day2'] = day2
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']), "normal")
            print("")
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                urllist.append(ftpsitelist)  # 按天下载
            cddpooldownload(urllist, 6)  # 多线程下载
            getuncompress()

        elif obj in objneedyd1d2loc:  # 输入为年， 起始年积日， 终止年积日, 站点文件 的数据类型
            [year, day1, day2] = yd_cdd()  # 获取下载时间
            cddarg['year'] = year
            cddarg['day1'] = day1
            cddarg['day2'] = day2
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']), "normal")
            print("")
            cddarg['site'] = getfile(cddarg['datatype'])
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                for s in cddarg['site']:
                    siteftp = []
                    for f in ftpsitelist:
                        f = f.replace('<SITE>', s)
                        siteftp.append(f)
                    urllist.append(siteftp)  # 按天下载
            cddpooldownload(urllist, 6)  # 多线程下载
            getuncompress()

        elif obj in objneedn:
            ftpsite = FTP_S[cddarg['datatype']]
            for ftp in ftpsite:
                wgets(ftp)
            cddpooldownload(urllist, 6)  # 多线程下载
            getuncompress()