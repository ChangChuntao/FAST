#!/usr/bin/python3
# CDD_Sub        : Get user input
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.22
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.09.20 - Version 1.22

import os
from GNSS_Timestran import gnssTimesTran
from Format import *
from help import *
from Dowload import *
from FAST_Print import *
from GNSS_TYPE import *
from Get_Ftp import *


def top_cdd():
    """
    2022-03-27 : 一级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                 by Chang Chuntao  -> Version : 1.11
    2022-04-30 : * 新增GNSS日常使用工具：GNSS_Timestran
                 调整输入模式, 0 -> a -> HELP / b -> GNSS_Timestran，增加分栏
                 by Chang Chuntao  -> Version : 1.12
    2022-05-24 : + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                 CARG_ion、ESAG_ion、ESRG_ion
                 by Chang Chuntao  -> Version : 1.13
    2022-07-13 : + 新增SpaceData一级类
                 + 新增SpaceData内资源SW_EOP
                 by Chang Chuntao  -> Version : 1.16
    2022-09-20 : > 修正TRO -> TROP
                 by Chang Chuntao  -> Version : 1.22
    """
    print("")
    print("     ----------------------------------FAST--------------------------------------")
    print("    |                                                                            |")
    print("    |    1 : BRDC                   2 : SP3                   3 : RINEX          |")
    print("    |    4 : CLK                    5 : ERP                   6 : BIA            |")
    print("    |    7 : ION                    8 : SINEX                 9 : CNES_AR        |")
    print("    |   10 : ATX                   11 : DCB                  12 : Time_Series    |")
    print("    |   13 : Velocity_Fields       14 : SLR                  15 : OBX            |")
    print("    |   16 : TROP                  17 : SpaceData                                |")
    print("    |                                                                            |")
    print("     ----------------------------------------------------------------------------")
    print("    |                                                                            |")
    print("    |    a : HELP                   b : GNSS_Timestran                           |")
    print("    |                                                                            |")
    print("     ----------------------------------------------------------------------------")

    PrintGDD("Note: 请输入数据编号 (eg. 2 or a)", "input")
    obj = input("     ")
    while True:
        if obj == "a" or obj == "b":
            return obj
        elif obj.isdigit():  # 判断输入是否为数字
            if int(obj) > len(gnss_type) or int(obj) < 0:  # 判断输入是否超出列表范围
                print("")
                PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2 or a)", "input")
                obj = input("     ")
            else:
                obj = int(obj)
                return obj
        else:
            PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2 or a)", "input")
            obj = input("     ")


def sub_cdd(obj):
    """
    2022-03-27 : 二级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-12 : 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                 * 新增返回上级菜单操作，输入y回到上级菜单
                 by Chang Chuntao  -> Version : 1.10
    2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                 by Chang Chuntao  -> Version : 1.11
    2022-04-30 : * 新增GNSS日常使用工具：GNSS_Timestran
                 gnssTimesTran调用
                 by Chang Chuntao  -> Version : 1.12
    2022-05-24 : + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                 CARG_ion、ESAG_ion、ESRG_ion
                 by Chang Chuntao  -> Version : 1.13
    2022-05-31 : + 新增BIA内资源MGEX_WHU_OSB_bia
                 > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                 by Chang Chuntao  -> Version : 1.14
    2022-07-03 : + 新增CLK内资源MGEX_WUHU_clk
                 + 新增ERP内资源WUHU_erp
                 + 新增OBX内资源MGEX_WUHU_obx
                 by Chang Chuntao  -> Version : 1.15
    2022-07-13 : + 新增SpaceData一级类
                 + 新增SpaceData内资源SW_EOP
                 by Chang Chuntao  -> Version : 1.16
    2022-07-22 : + 新增SP3内资源MGEX_WUH_Hour_sp3
                 + 新增CLK内资源MGEX_WUH_Hour_clk
                 + 新增ERP内资源WUH_Hour_erp
                 by Chang Chuntao  -> Version : 1.17
    2022-07-27 : > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                 > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                 > 修正MGEX_COD_clk资源
                 by Chang Chuntao  -> Version : 1.18
    2022-09-16 : + 新增RINEX内MGEX_HK_cors
                 by Chang Chuntao  -> Version : 1.21
    2022-09-20 : > 修正TRO -> TROP
                 + 新增TROP内资源Meteorological
                 by Chang Chuntao  -> Version : 1.22
    """
    print("")
    if obj == 1:
        print("     -----------------------------------BRDC-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_brdc               2 : MGEX_brdm                                |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 2:
        print("     -----------------------------------SP3 -------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_sp3            2 : GPS_IGR_sp3            3 : GPS_IGU_sp3   |")
        print("    |    4 : GPS_GFZ_sp3            5 : GPS_GRG_sp3                              |")
        print("    |    6 : MGEX_WUH_sp3           7 : MGEX_WUHU_sp3          8 : MGEX_GFZR_sp3 |")
        print("    |    9 : MGEX_COD_sp3          10 : MGEX_SHA_sp3          11 : MGEX_GRG_sp3  |")
        print("    |   12 : GLO_IGL_sp3           13 : MGEX_WUH_Hour_sp3                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 3:
        print("     ----------------------------------RINEX-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_rnx            2 : MGEX_IGS_rnx           3 : GPS_USA_cors  |")
        print("    |    4 : GPS_HK_cors            5 : GPS_EU_cors            6 : GPS_AU_cors   |")
        print("    |    7 : MGEX_HK_cors                                                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 4:
        print("     -----------------------------------CLK--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_clk            2 : GPS_IGR_clk            3 : GPS_GFZ_clk   |")
        print("    |    4 : GPS_GRG_clk            5 : GPS_IGS_clk_30s                          |")
        print("    |    6 : MGEX_WUH_clk           7 : MGEX_COD_clk           8 : MGEX_GFZR_clk |")
        print("    |    9 : MGEX_GRG_clk          10 : WUH_PRIDE_clk         11 : MGEX_WUHU_clk |")
        print("    |   12 : MGEX_WUH_Hour_clk                                                   |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 5:
        print("     -----------------------------------ERP--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS_erp                2 : WUH_erp                3 : COD_erp       |")
        print("    |    4 : GFZ_erp                5 : IGR_erp                6 : WUHU_erp      |")
        print("    |    7 : WUH_Hour_erp                                                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 6:
        print("     -----------------------------------BIA--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : MGEX_WHU_ABS_bia       2 : MGEX_WHU_OSB_bia       3 : GPS_COD_bia   |")
        print("    |    4 : MGEX_COD_bia           5 : MGEX_GFZ_bia                             |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 7:
        print("     -----------------------------------ION--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGSG_ion               2 : IGRG_ion               3 : WUHG_ion      |")
        print("    |    4 : WURG_ion               5 : CODG_ion               6 : CORG_ion      |")
        print("    |    7 : UQRG_ion               8 : UPRG_ion               9 : JPLG_ion      |")
        print("    |   10 : JPRG_ion              11 : CASG_ion              12 : CARG_ion      |")
        print("    |   13 : ESAG_ion              14 : ESRG_ion                                 |")

        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 8:
        print("     ----------------------------------SINEX-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS_day_snx            2 : IGS_week_snx           3 : IVS_week_snx  |")
        print("    |    4 : ILS_week_snx           5 : IDS_week_snx                             |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 9:
        print("     --------------------------------CNES_AR-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : CNES_post              2 : CNES_realtime                            |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 10:
        print("     -----------------------------------ATX--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : MGEX_IGS_atx                                                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 11:
        print("     -----------------------------------DCB--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_COD_dcb            2 : MGEX_CAS_dcb           3 : MGEX_WHU_OSB  |")
        print("    |    4 : P1C1                   5 : P1P2                   6 : P2C2          |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 12:
        print("     --------------------------------Time_Series---------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS14_TS_ENU           2 : IGS14_TS_XYZ           3 : Series_TS_Plot|")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 13:
        print("     ------------------------------Velocity_Fields-------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS14_Venu             2 : IGS08_Venu             3 : PLATE_Venu    |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 14:
        print("     -----------------------------------SLR--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : HY_SLR                 2 : GRACE_SLR              3 : BEIDOU_SLR    |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 15:
        print("     -----------------------------------OBX--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_COD_obx            2 : GPS_GRG_obx                              |")
        print("    |    3 : MGEX_WUH_obx           4 : MGEX_COD_obx           5 : MGEX_GFZ_obx  |")
        print("    |    6 : MGEX_WUHU_obx                                                       |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 16:
        print("     -----------------------------------TROP-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS_zpd                2 : COD_tro                3 : JPL_tro       |")
        print("    |    4 : GRID_1x1_VMF3          5 : GRID_2.5x2_VMF1        6 : GRID_5x5_VMF3 |")
        print("    |    7 : Meteorological                                                      |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 17:
        print("     --------------------------------SpaceData-----------------------------------")
        print("    |                                                                            |")
        print("    |    1 : SW_EOP                                                              |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == "a":
        cddhelp()
        return 0
    elif obj == "b":
        gnssTimesTran()
        return 0

    PrintGDD("Note: 请输入数据编号 (eg. 2)", "input")  # 二级索引
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
    subnum = input("     ")
    while True:
        if subnum == "y" or subnum == "Y":
            return "y"
        else:
            if subnum.isdigit():  # 判断是否为数字
                if int(subnum) > objnum[obj - 1] or int(subnum) < 1:  # 判断输入是否超出列表范围
                    print("")
                    PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2)", "input")
                    PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
                    subnum = input("     ")  # 二级索引
                else:
                    subnum = int(subnum)
                    return subnum
            else:
                PrintGDD("Warning: 输入错误，请输入正确编号 (eg. 2)", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")  # 二级索引
                subnum = input("     ")


# 2022-03-27 : 输入年日时间 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : *新增返回上级菜单操作，输入y回到上级菜单
#              by Chang Chuntao  -> Version : 1.10
def yd_cdd():
    print()
    PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> <year start_doy end_doy>", "input")
    PrintGDD("若需下载单天数据，请输入 <年 年积日> <year doy>", "input")
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")
    yd = input("     ")
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
                PrintGDD("Warning: 请输入正确的时间!", "warning")
                PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> <year start_doy end_doy>", "input")
                PrintGDD("若需下载单天数据，请输入 <年 年积日> <year doy>", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")
                yd = input("     ")


# 2022-03-27 : 输入年月时间 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : *新增返回上级菜单操作，输入y回到上级菜单
#              by Chang Chuntao  -> Version : 1.10
def ym_cdd():
    print()
    PrintGDD("Note: 请输入 <年 月> <year month>", "input")
    PrintGDD("Note: 如需返回上级目录，请输入y", "input")
    ym = input("     ")
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
                PrintGDD("Warning: 请输入正确的时间!", "warning")
                PrintGDD("请输入 <年 月> <year month>", "input")
                PrintGDD("Note: 如需返回上级目录，请输入y", "input")
                ym = input("     ")


# 2022-03-27 : 输入站点文件 by Chang Chuntao -> Version : 1.00
def getFile(datatype):
    print()
    PrintGDD("请输入文件所在位置 / Please enter the location of the site file", "input")
    PrintGDD("文件内站点名以空格分割,可含有多行，eg. <bjfs irkj urum>", "input")
    sitefile = input("     ")
    return getSite(sitefile, datatype)


# 2022-04-12 : vlbi文件解压 by Chang Chuntao  -> Version : 1.10
def getvlbicompress(ftpsite):
    print()
    PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
    isuncpmress = input("     ")
    if isuncpmress == "":
        unzip_vlbi(os.getcwd(), ftpsite)


# 2022-04-12 : 通过下载列表解压文件(年日) by Chang Chuntao  -> Version : 1.10
def uncompress(urllist):
    ftpsite = []
    for i in range(len(urllist)):
        for j in range(len(urllist[i])):
            ftpsite.append(urllist[i][j])
    print()
    isuncpmress = "y"
    for f in ftpsite:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z":
            PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
            isuncpmress = input("     ")
            break
    if isuncpmress == "":
        unzipfile(os.getcwd(), ftpsite)


# 2022-04-12 : 通过下载列表解压文件(年月) by Chang Chuntao  -> Version : 1.10
def uncompress_ym(url):
    isuncpmress = "y"
    ftpsite = []
    for u in url:
        ftpsite.append(u)
    for f in ftpsite:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z":
            PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！ / Press enter to unzip!", "input")
            isuncpmress = input("     ")
            break
    if isuncpmress == "":
        unzipfile(os.getcwd(), ftpsite)


def geturl_download_uncompress(cddarg, obj):
    """
    2022-04-12 : 通过输入引导的参数获取下载列表，下载文件、解压文件 by Chang Chuntao  -> Version : 1.10
    2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                 by Chang Chuntao  -> Version : 1.11
    2022-08-04 : 修正时序文件下载需求
                 by Chang Chuntao  -> Version : 1.19
    2022-09-16 : 新增站点字符串替换子程序
                 by Chang Chuntao  -> Version : 1.21
    2022-09-20 : + 新增TROP内资源Meteorological，为需要站点的气象文件
                 by Chang Chuntao  -> Version : 1.22
    """
    urllist = []  # 下载列表

    # 数据类型为IVS_week_snx
    if cddarg['datatype'] == "IVS_week_snx":
        ftpsite = FTP_S[cddarg['datatype']][0]
        ym = ym_cdd()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            ftpsite = ftpsite.replace('<YY>', str(year)[2:4])
            ftpsite = ReplaceMMM(ftpsite, month)
            lftps(ftpsite)
            getvlbicompress(ftpsite)
            return "n"

    # 数据类型为输入年月
    elif cddarg['datatype'] == "P1C1" or cddarg['datatype'] == "P1P2" or cddarg['datatype'] == "P2C2":
        ftpsite = FTP_S[cddarg['datatype']]
        ym = ym_cdd()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            ftpsite_new = []
            for ftp in ftpsite:
                ftp = ftp.replace('<YYYY>', str(year))
                ftp = ftp.replace('<YY>', str(year)[2:4])
                ftp = ReplaceMM(ftp, month)
                wgets(ftp)
                ftpsite_new.append(ftp)
            uncompress_ym(ftpsite_new)
            return "n"

    else:
        # 数据类型为输入年日
        # 输入为年， 起始年积日， 终止年积日 的数据类型
        if obj in objneedydqd2 and cddarg['datatype'] != "IGS_zpd" and cddarg['datatype'] != "Meteorological":
            yd = yd_cdd()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                cddarg['year'] = year
                cddarg['day1'] = day1
                cddarg['day2'] = day2
                PrintGDD(
                    "下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']),
                    "normal")
                print("")
                for day in range(cddarg['day1'], cddarg['day2'] + 1):
                    ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                    urllist.append(ftpsitelist)  # 按天下载
                cddpooldownload(urllist, 3)  # 多线程下载
                uncompress(urllist)
                return "n"

        # 数据类型为输入年日站点文件
        # 输入为年， 起始年积日， 终止年积日, 站点文件 的数据类型
        elif obj in objneedyd1d2loc or cddarg['datatype'] == "IGS_zpd" or cddarg['datatype'] == "Meteorological":
            yd = yd_cdd()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                cddarg['year'] = year
                cddarg['day1'] = day1
                cddarg['day2'] = day2
                PrintGDD(
                    "下载时间为" + str(cddarg['year']) + "年，年积日" + str(cddarg['day1']) + "至" + str(cddarg['day2']),
                    "normal")
                cddarg['site'] = getFile(cddarg['datatype'])
                for day in range(cddarg['day1'], cddarg['day2'] + 1):
                    ftpsitelist = getftp(cddarg['datatype'], cddarg['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                    for siteInList in cddarg['site']:
                        siteftp = []
                        for ftpInList in ftpsitelist:
                            ftpInList = replaceSiteStr(ftpInList, siteInList)
                            # f = f.replace('<SITE>', s)
                            siteftp.append(ftpInList)
                        urllist.append(siteftp)  # 按天下载
                cddpooldownload(urllist, 3)  # 多线程下载
                uncompress(urllist)
                return "n"

        elif obj in objneedloc:  # 输入为站点文件 的数据类型
            cddarg['site'] = getFile(cddarg['datatype'])
            ftpsite = FTP_S[cddarg['datatype']]
            for siteInList in cddarg['site']:
                siteftp = []
                for ftpInList in ftpsite:
                    ftpInList = replaceSiteStr(ftpInList, siteInList)
                    # ftpInList = ftpInList.replace('<SITE>', siteInList)
                    siteftp.append(ftpInList)
                urllist.append(siteftp)  # 按天下载
            cddpooldownload(urllist, 3)  # 多线程下载
            uncompress(urllist)
            return "n"

        # 无需输入时间的数据类型
        elif obj in objneedn:
            ftpsite = FTP_S[cddarg['datatype']]
            for ftp in ftpsite:
                wgets(ftp)
            cddpooldownload(urllist, 3)  # 多线程下载
            uncompress(urllist)
            return "n"
