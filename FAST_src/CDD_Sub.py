#!/usr/bin/python3
# CDD_Sub        : Get user input
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.27
import os

from FAST_Print import PrintGDD
from GNSS_TYPE import objnum, gnss_type
from Get_Ftp import getsite
from Format import unzip_format
from help import cddhelp


def top_cdd():
    print("")
    # print("     -----------------------------------GDD--------------------------------------")
    # print("    |                                                                            |")
    # print("    |    0 : HELP                                                                |")
    # print("    |    1 : BRDC                   2 : SP3                   3 : RINEX          |")
    # print("    |    4 : CLK                    5 : ERP                   6 : BIA            |")
    # print("    |    7 : ION                    8 : SINEX                 9 : CNES           |")
    # print("    |   10 : UPD                   11 : ATX                  12 : DCB            |")
    # print("    |   13 : Time_Series           14 : Velocity_Fields                          |")
    # print("    |                                                                            |")
    # print("     ----------------------------------------------------------------------------")
    print("     ----------------------------------FAST--------------------------------------")
    print("    |                                                                            |")
    print("    |    0 : HELP                                                                |")
    print("    |    1 : BRDC                   2 : SP3                   3 : RINEX          |")
    print("    |    4 : CLK                    5 : ERP                   6 : BIA            |")
    print("    |    7 : ION                    8 : SINEX                 9 : CNES_AR        |")
    print("    |   10 : ATX                   11 : DCB                  12 : Time_Series    |")
    print("    |   13 : Velocity_Fields       14 : SLR                  15 : OBX            |")
    print("    |                                                                            |")
    print("     ----------------------------------------------------------------------------")
    PrintGDD("Note: 请输入数据编号 (例如 2)", "input")
    obj = input("     ")
    while True:
        if obj.isdigit():  # 判断输入是否为数字
            if int(obj) > len(gnss_type) or int(obj) < 0:  # 判断输入是否超出列表范围
                print("")
                PrintGDD("Warning: 输入错误，请输入正确编号 (例如 2)", "input")
                obj = input("     ")
            else:
                obj = int(obj)
                return obj
        else:
            PrintGDD("Warning: 输入错误，请输入正确编号 (例如 2)", "input")
            obj = input("     ")


def sub_cdd(obj):
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
        print("    |    1 : GPS_IGS_sp3            2 : GPS_IGR_sp3             3 : GPS_IGU_sp3  |")
        print("    |    4 : GPS_GFZ_sp3            5 : GPS_GRG_sp3                              |")
        print("    |    6 : MGEX_WUH_sp3           7 : MGEX_WUHU_sp3           8 : MGEX_GFZ_sp3 |")
        print("    |    9 : MGEX_COD_sp3           10: MGEX_SHA_sp3            11: MGEX_GRG_sp3 |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 3:
        print("     ----------------------------------RINEX-------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_rnx            2 : MGEX_IGS_rnx           3 : GPS_USA_cors  |")
        print("    |    4 : GPS_HK_cors            5 : GPS_EU_cors            6 : GPS_AU_cors   |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 4:
        print("     -----------------------------------CLK--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_IGS_clk            2 : GPS_IGR_clk            3 : GPS_GFZ_clk   |")
        print("    |    4 : GPS_GRG_clk                                                         |")
        print("    |    5 : MGEX_WUH_clk           6 : MGEX_COD_clk           7 : MGEX_GFZ_clk  |")
        print("    |    8 : MGEX_GRG_clk           9 : WUH_PRIDE_clk                            |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 5:
        print("     -----------------------------------ERP--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS_erp                2 : WUH_erp                3 : COD_erp       |")
        print("    |    4 : GFZ_erp                                                             |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 6:
        print("     -----------------------------------BIA--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : MGEX_WHU_bia           2 : GPS_COD_bia          3 : MGEX_COD_bia    |")
        print("    |    4 : MGEX_GFZ_bia                                                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 7:
        print("     -----------------------------------ION--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : IGS_ion                2 : WUH_ion                3 : COD_ion       |")
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
    # elif obj == 10:
    #     print("     -----------------------------------UPD--------------------------------------")
    #     print("    |                                                                            |")
    #     print("    |    1 : MGEX_WUH_IGMAS_upd                                                  |")
    #     print("    |                                                                            |")
    #     print("     ----------------------------------------------------------------------------")
    elif obj == 10:
        print("     -----------------------------------ATX--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : MGEX_IGS_atx                                                        |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 11:
        print("     -----------------------------------DCB--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_COD_dcb            2 : MGEX_CAS_dcb                             |")
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
        print("    |    1 : HY_SLR                                                              |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 15:
        print("     -----------------------------------OBX--------------------------------------")
        print("    |                                                                            |")
        print("    |    1 : GPS_COD_obx            2 : GPS_GRG_obx                              |")
        print("    |    3 : MGEX_WUH_obx           4 : MGEX_COD_obx           5 : MGEX_GFZ_obx  |")
        print("    |                                                                            |")
        print("     ----------------------------------------------------------------------------")
    elif obj == 0:
        cddhelp()
        return 0
    PrintGDD("Note: 请输入数据编号 (例如 2)", "input")  # 二级索引
    subnum = input("     ")
    while True:
        if subnum.isdigit():  # 判断是否为数字
            if int(subnum) > objnum[obj - 1] or int(subnum) < 1:  # 判断输入是否超出列表范围
                print("")
                PrintGDD("Warning: 输入错误，请输入正确编号 (例如 2)", "input")
                subnum = input("     ")  # 二级索引
            else:
                subnum = int(subnum)
                return subnum
        else:
            PrintGDD("Warning: 输入错误，请输入正确编号 (例如 2)", "input")
            subnum = input("     ")


def yd_cdd():
    print()
    PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> ", "input")
    PrintGDD("若需下载单天数据，请输入 <年 年积日>", "input")
    YD = input("     ").split()
    while True:
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
            PrintGDD("若需下载多天数据，请输入 <年 起始年积日 截止年积日> ", "input")
            PrintGDD("若需下载单天数据，请输入 <年 年积日>", "input")
            YD = input("     ").split()


def ym_cdd():
    print()
    PrintGDD("请输入 <年 月> ", "input")
    YM = input("     ").split()
    while True:
        if len(YM) == 2:
            year = int(YM[0])
            month = int(YM[1])
            return year, month
        else:
            PrintGDD("Warning: 请输入正确的时间!", "warning")
            PrintGDD("请输入 <年 月> ", "input")
            YM = input("     ").split()


def getfile(datatype):
    print()
    PrintGDD("请输入站点文件所在位置", "input")
    PrintGDD("文件内站点名以空格分割，类如<bjfs irkj urum>", "input")
    sitefile = input("     ")
    return getsite(sitefile, datatype)


def getuncompress():
    print()
    PrintGDD("是否解压文件？如需解压直接回车，若无需解压输入任意字符回车！", "input")
    isuncpmress = input("     ")
    if isuncpmress == "":
        unzip_format(os.getcwd())