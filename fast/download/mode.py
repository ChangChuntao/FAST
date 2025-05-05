# -*- coding: utf-8 -*-
# mode           : Mode for FAST Downlad module
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2022.03.27 - Version 1.00
# Latest Version : 2023-09-20 - Version 2.11

from fast.com.pub import printFast, gnss_type
from fast.download.arg import getArg, checkInputArg
from fast.download.ftpSrc import FTP_S
from fast.download.fileOperation import unzip_vlbi
from fast.com.gnssTime import ReplaceMMM
from fast.com.mgexInf import mgex
from fast.download.inf import fastSoftwareInformation
from fast.download.menu import level1menu, level2menu
from fast.download.download import getUrlByRun, lftps, geturlByArg, argpooldownload
import os

def runApplication():
    """
    2022-03-27 : runApplication
    """
    fastSoftwareInformation()
    obj = level1menu()
    subnum = level2menu(obj)
    while True:
        if subnum == "y":
            obj = level1menu() 
            subnum = level2menu(obj)  
        else:
            if subnum != 0:
                fastArg = {'datatype': gnss_type[obj - 1][1][subnum - 1]} 
                printFast("The data type is " + fastArg['datatype'], "normal")
                break
            else:
                return 0
    
    back_sub = getUrlByRun(fastArg)
    while True:
        if back_sub == "y":
            subnum = level2menu(obj)  
            while True:
                if subnum == "y":
                    obj = level1menu()  
                    subnum = level2menu(obj) 
                else:
                    fastArg = {'datatype': gnss_type[obj - 1][1][subnum - 1]} 
                    printFast("The data type is " + fastArg['datatype'], "normal")
                    break
            back_sub = getUrlByRun(fastArg)
        else:
            break
    ...


def runApplicationWithArgs():
    """
    2022-03-27 :    输入参数模式主函数 by Chang Chuntao -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  -> Version : 1.10
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2023-06-30 :    + 增加小时参数
                    by Chang Chuntao  -> Version : 2.09
    """
    fastArg = {"datatype": "", "year": 2022, "loc": "", "day1": 1, "day2": 1, "month": 1, "file": "", "process": 4,
              "site": "", "uncompress": "y", 'rename': '', 'hour': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                                    15, 16, 17, 18, 19, 20, 21, 22, 23],}
    fastArg = getArg(fastArg)  # 获取参数内容
    if fastArg is None:
        return
    checkInputArg(fastArg)  # 判断输入参数正确性

    # 数据类型为IVS_week_snx, lftp下载
    if fastArg['datatype'] == "IVS_week_snx":
        nowdir = os.getcwd()
        if len(fastArg["loc"]) == 0:
            os.chdir(nowdir)
        else:
            os.chdir(fastArg["loc"])
        ftpsite = FTP_S[fastArg['datatype']][0]
        ftpsite = ftpsite.replace('<YY>', str(fastArg['year'])[2:4])
        ftpsite = ReplaceMMM(ftpsite, fastArg['month'])
        lftps(ftpsite)
        if fastArg["uncompress"] == "y" or fastArg["uncompress"] == "Y":
            unzip_vlbi(fastArg["loc"], ftpsite)
    else:
        urllist = geturlByArg(fastArg)  # 判断下载列表
        argpooldownload(urllist, fastArg["process"], fastArg["loc"], fastArg["uncompress"], fastArg['datatype'], fastArg['rename'])  # 并行下载



def runByYearDoy():
    """
    2022-03-27 :    输入年日时间
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    *新增返回上级菜单操作,输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    """
    print()
    printFast("若需下载多天数据,请输入 <年 起始年积日 截止年积日> / Enter <year start_doy end_doy>", "input")
    printFast("若需下载单天数据,请输入 <年 年积日> / or enter <year doy>", "input")
    printFast("Note: 如需返回上级目录,请输入y / In need of returning parent menu, plear enter <y> ", "input")
    yd = input("    ")
    while True:
        if yd == "y" or yd == "Y":
            return "y"

        else:
            YD = yd.split()
            if len(YD) == 2:
                year = int(YD[0])
                day1 = int(YD[1])
                day2 = int(YD[1])
                return year, day1, day2
            elif len(YD) == 3:
                year = int(YD[0])
                day1 = int(YD[1])
                day2 = int(YD[2])
                return year, day1, day2
            else:
                printFast("Warning: 请输入正确的时间 / Please enter the time in the correct format!", "warning")
                printFast("若需下载多天数据,请输入 <年 起始年积日 截止年积日> / Enter <year start_doy end_doy>", "input")
                printFast("若需下载单天数据,请输入 <年 年积日> / or enter <year doy>", "input")
                printFast("Note: 如需返回上级目录,请输入y / Enter <y> to return parent menu...", "input")
                yd = input("    ")

def runByYearMonth():
    '''
    2022-03-27 :    输入年月时间
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    *新增返回上级菜单操作,输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    '''
    print()
    printFast("Note: 请输入 <年 月> / Enter <year month>", "input")
    printFast("Note: 如需返回上级目录,请输入<y> / Enter <y> to return parent menu...", "input")
    ym = input("    ")
    while True:
        if ym == "y" or ym == "Y":
            return "y"
        else:
            YM = ym.split()
            if len(YM) == 2:
                year = int(YM[0])
                month = int(YM[1])
                return year, month
            else:
                printFast("Warning: 请输入正确的时间 / Please enter the time in the correct format!", "warning")
                printFast("请输入 <年 月> / Enter <year month>", "input")
                printFast("Note: 如需返回上级目录,请输入y / Enter <y> to return parent menu...", "input")
                ym = input("    ")


def getHour():
    """
    2023-05-11 :    输入小时
                    by Chang Chuntao -> Version : 1.00
    """
    print()
    printFast("Note: 请输入 <小时> / Enter <0-23>", "input")
    hourStr = input("    ")
    while True:
        try:
            hour = int(hourStr)
            if 23 >= hour >= 0:
                return hour
            else:
                printFast("Error: 输入错误, 请输入 <小时> / Enter <0-23>", "input")
                hourStr = input("    ")
                continue
        except:
            printFast("Error: 输入错误, 请输入 <小时> / Enter <0-23>", "input")
            hourStr = input("    ")
            continue


def getFile(datatype):
    """
    2022-03-27 :    * 输入站点文件
                    by Chang Chuntao  -> Version : 1.00
    2023-01-14 :    + 支持直接输入站点名
                    by Chang Chuntao  -> Version : 2.06
    """
    print()
    printFast(r"请输入站点名称或站点文件所在位置(绝对位置/相对位置) / Please enter the site name or the location of the site file\n         eg. BJFS00CHN irkj urum / site.txt or D:\site.txt", "input")
    printFast(r"文件内写入站名, 长名短名都可, 按行按空格分割都可！/ Write station names in the file, \n     both long and short names are accepted, separated by lines or spaces.\n         eg. - BJFS00CHN irkj urum", "input")
    sitefile = input("    ")
    return getSite(sitefile, datatype)


def getSite(file, datatype):
    """
    2022-03-27 : * 读取file中站点名,返回site
                 by Chang Chuntao -> Version : 1.00
    2022-08-04 : 修正时序文件下载需求
                 by Chang Chuntao -> Version : 1.19
    2022-09-11 : 站点文件可支持行列两种格式,或混合模式
                 by Chang Chuntao -> Version : 1.20
    2023-01-14 : 支持支持输入站点
                 by Chang Chuntao -> Version : 2.06
    """
    site = []
    if file == '':
        site = []
    else:
        if os.path.isfile(file):
            fileLine = open(file, "r").readlines()
            for line in fileLine:
                lineSplit = line.split()
                for siteInLine in lineSplit:
                    site.append(siteInLine)
        else:
            site = str(file).split()
    if datatype == "GCRE_MGEX_obs" or datatype == "GCRE_HK_cors":
        for s in range(0, len(site)):
            if len(site[s]) == 9:
                continue
            else:
                site[s] = site[s].lower()
                for m in mgex:
                    if site[s] == m[0]:
                        site[s] = m[1]
    elif datatype == "IGS14_TS_ENU" or datatype == "IGS14_TS_XYZ" or datatype == "Series_TS_Plot":
        for s in range(0, len(site)):
            site[s] = site[s].upper()[0:4]
    else:
        for s in range(0, len(site)):
            site[s] = site[s].lower()[0:4]
    return site


def getUncompress(successDownFileList):
    '''
    2022-04-12 : 通过下载列表解压文件(年日) by Chang Chuntao  -> Version : 1.10
    2023-11-10 : 通过成功下载的文件解压 by Chang Chuntao  -> Version : 3.00
    '''
    from fast.download.fileOperation import unzipfile
    # ftpsite = []
    # for i in range(len(urllist)):
    #     for j in range(len(urllist[i])):
    #         ftpsite.append(urllist[i][j])
    # print()
    extractedFileList = []
    isuncpmress = "N"
    for f in successDownFileList:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z" or str(f).split(".")[-1] == "tgz" \
                or str(f).split(".")[-1] == "zip" or str(f).split(".")[-1] == "ZIP":
            printFast("是否解压文件？如需解压直接回车,若无需解压输入任意字符回车！ / Unzip: Enter. Skip unzip: Any+Enter!", "input")
            isuncpmress = input("    ")
            break
    if isuncpmress == "":
        extractedFileList = unzipfile(os.getcwd(), successDownFileList)
    return extractedFileList

def getvlbicompress(ftpsite):
    '''
    2022-04-12 : 文件检索解压 by Chang Chuntao  -> Version : 1.10
    '''
    from fast.download.fileOperation import unzip_vlbi
    print()
    printFast("是否解压文件？如需解压直接回车,若无需解压输入任意字符回车！ / Unzip: Enter. Skip unzip: Any+Enter!", "input")
    isuncpmress = input("    ")
    if isuncpmress == "":
        unzip_vlbi(os.getcwd(), ftpsite)


def getRename(successDownFileList):
    from fast.download.fileOperation import renamePro
    rename3char = None
    for f in successDownFileList:
        fileType = str(f).split(".")[-1]
        if 'ULT' in f or 'ULA' in f:
            continue
        if fileType in ['SP3', 'CLK', 'BIA', 'DCB', 'ERP', 'SNX']:
            printFast("如无需更名直接回车,若需更名请输入三位字符！/ Rename: <3char> + Enter. Skip: Enter!", "input")
            rename3char = input("    ")
            break
    
    if rename3char is not None and len(rename3char) > 0:
        while len(rename3char) != 3:
            printFast("请输入正确字符！ / Rename: <3char> + Enter!", "input")
            rename3char = input("    ")
        renamePro(successDownFileList, rename3char)



        