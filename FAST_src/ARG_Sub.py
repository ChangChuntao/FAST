#!/usr/bin/python3
# ARG_Sub        : Identify program arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.24
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.10.10 - Version 1.24


import sys
from FAST_Print import PrintGDD
from Format import unzipfile
from GNSS_TYPE import isinGNSStype, yd_type, yds_type, ym_type, s_type, no_type
import getopt
from Get_Ftp import getftp, getSite, replaceSiteStr
from help import Supported_Data, arg_options, arg_help


def GET_ARG(argument, cddarg):
    """
    2022-03-27 : 获取输入参数 by Chang Chuntao -> Version : 1.00
    """
    try:
        opts, args = getopt.getopt(argument, "hvt:l::y::o::e::d::m::f::p::u::",
                                   ["type=", "loc=", "year=", "day1=", "day2=", "day=", "month=", "file=", "process=",
                                    "uncompress="])
    except getopt.GetoptError:
        PrintGDD("参数类型输入错误！", "fail")
        print()
        arg_options()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            arg_help()
            sys.exit()
        elif opt == '-v' or opt == '-version':
            print("3.0.0")
            sys.exit()
        elif opt in ("-t", "--type"):
            cddarg["datatype"] = arg
        elif opt in ("-y", "--year"):
            cddarg['year'] = int(arg)
        elif opt in ("-l", "--loc"):
            cddarg["loc"] = arg
        elif opt in ("-o", "--day1"):
            cddarg["day1"] = int(arg)
        elif opt in ("-e", "--day2"):
            cddarg["day2"] = int(arg)
        elif opt in ("-d", "--day"):
            cddarg["day1"] = int(arg)
            cddarg["day2"] = int(arg)
        elif opt in ("-m", "--month"):
            cddarg["month"] = int(arg)
        elif opt in ("-f", "--file"):
            cddarg["file"] = arg
        elif opt in ("-p", "--process"):
            cddarg["process"] = int(arg)
        elif opt in ("-u", "--uncompress"):
            cddarg["uncompress"] = arg
        # elif opt in ("-s", "--site"):
        #     cddarg["site"] = arg.split(",")
    # print(cddarg)
    return cddarg


def ARG_ifwrong(cddarg):  # 判断输入参数正确性
    """
    2022-03-27 : 判断输入参数正确性 by Chang Chuntao -> Version : 1.00
    """
    datatype = str(cddarg['datatype']).split(",")
    for dt in datatype:
        if isinGNSStype(dt):  # 判断输入数据类型是否正确
            if dt in ym_type:
                if cddarg['year'] == 0 or cddarg['month'] == 0:
                    PrintGDD("本数据类型需输入年与月，请指定[-y <year>] [-m <month>]！", "fail")
                    sys.exit(2)
            else:
                if dt in yd_type:  # 输入为年， 起始年积日， 终止年积日的数据类型, 判断输入时间是否正确
                    if cddarg['year'] == 0:
                        PrintGDD(
                            "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                            "fail")
                        sys.exit(2)
                    else:
                        if cddarg['day1'] == 0 and cddarg['day2'] == 0:
                            PrintGDD(
                                "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                                "fail")
                            sys.exit(2)
                if dt in yds_type or dt in s_type:
                    if cddarg['file'] == "" and cddarg['site'] == "":
                        PrintGDD("本类型需要输入文件位置参数或站点参数，请指定[-f <file>]或者[-s <site>]！", "fail")
                        sys.exit(2)
        else:
            PrintGDD(dt + "数据类型不存在！", "fail")
            PrintGDD("是否需要查看支持数据？(y)", "input")
            cont = input("     ")
            if cont == "y" or "Y":
                Supported_Data()
                sys.exit(2)
            else:
                sys.exit(2)


def geturl(cddarg):
    """
    2022.04.12 :    获取下载列表 by Chang Chuntao -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-09-16 :    新增站点字符串替换子程序
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological，为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-10-10 :    > 修复无需其他参数输入下载类下载
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    """
    urllist = []
    for dt in str(cddarg['datatype']).split(","):
        typeurl = []
        PrintGDD("数据类型为:" + dt, "normal")

        # 数据类型为无需输入
        if dt in no_type:
            ftpsitelist = getftp(dt, 2022, 1)
            typeurl.append(ftpsitelist)

        # 数据类型为输入年日
        if dt in yd_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                url = []
                if len(ftpsitelist) != 0:
                    for ftpsite in ftpsitelist:
                        url.append(ftpsite)
                    typeurl.append(url)

        # 数据类型为输入年日站点文件
        elif dt in yds_type:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(
                cddarg['day2']) + "\n",
                     "normal")
            print("")
            cddarg['site'] = getSite(cddarg['file'], dt)
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                for siteInList in cddarg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        # f = f.replace('<SITE>', siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载
        urllist.append(typeurl)
    return urllist


def uncompress_arg(path, urllist):
    """
    2022.04.12 : 传入需解压的文件至unzipfile by Chang Chuntao -> Version : 1.10
    """
    ftpsite = []
    for a1 in urllist:
        for a2 in a1:
            for a3 in a2:
                ftpsite.append(a3)
    unzipfile(path, ftpsite)
