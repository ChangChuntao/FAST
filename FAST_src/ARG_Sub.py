#!/usr/bin/python3
# ARG_Sub        : Identify program arguments
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.0
# Date           : 2022.04.12 - Version 1.1

import sys
from FAST_Print import PrintGDD
from Format import unzipfile
from GNSS_TYPE import isinGNSStype, getobj, objneedydqd2, objneedyd1d2loc
import getopt
from Get_Ftp import getftp, getsite
from help import Supported_Data, arg_options, arg_help


# 2022-03-27 : 获取输入参数 by Chang Chuntao -> Version : 1.00
def GET_ARG(argument, cddarg):
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


#  2022-03-27 : 判断输入参数正确性 by Chang Chuntao -> Version : 1.00
def ARG_ifwrong(cddarg):  # 判断输入参数正确性
    datatype = str(cddarg['datatype']).split(",")
    for dt in datatype:
        if isinGNSStype(dt):  # 判断输入数据类型是否正确
            [obj, subnum] = getobj(dt)
            if dt == "IVS_week_snx":
                if cddarg['year'] == 0 or cddarg['month'] == 0:
                    PrintGDD("本数据类型需输入年与月，请指定[-y <year>] [-m <month>]！", "fail")
                    sys.exit(2)
            else:
                if obj + 1 in objneedydqd2:  # 输入为年， 起始年积日， 终止年积日的数据类型, 判断输入时间是否正确
                    if cddarg['year'] == 0:
                        PrintGDD("本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！", "fail")
                        sys.exit(2)
                    else:
                        if cddarg['day1'] == 0 and cddarg['day2'] == 0:
                            PrintGDD("本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                                     "fail")
                            sys.exit(2)
                if obj + 1 in objneedyd1d2loc:
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


#  2022.04.12 : 获取下载列表 by Chang Chuntao -> Version : 1.10
def geturl(cddarg):
    urllist = []
    for dt in str(cddarg['datatype']).split(","):
        typeurl = []
        [obj, subnum] = getobj(dt)
        PrintGDD("数据类型为:" + dt, "normal")
        if obj + 1 in objneedydqd2:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']) + "\n",
                     "normal")
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                url = []
                for ftpsite in ftpsitelist:
                    url.append(ftpsite)
                typeurl.append(url)

        elif obj + 1 in objneedyd1d2loc:
            PrintGDD("下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']) + "\n",
                     "normal")
            print("")
            cddarg['site'] = getsite(cddarg['file'], dt)
            for day in range(cddarg['day1'], cddarg['day2'] + 1):
                ftpsitelist = getftp(dt, cddarg['year'], day)
                for s in cddarg['site']:
                    siteftp = []
                    for f in ftpsitelist:
                        f = f.replace('<SITE>', s)
                        siteftp.append(f)
                    typeurl.append(siteftp)  # 按天下载
        urllist.append(typeurl)
    return urllist


#  2022.04.12 : 传入需解压的文件至unzipfile by Chang Chuntao -> Version : 1.10
def uncompress_arg(path, urllist):
    ftpsite = []
    for a1 in urllist:
        for a2 in a1:
            for a3 in a2:
                ftpsite.append(a3)
    unzipfile(path, ftpsite)
