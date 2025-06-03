# -*- coding: utf-8 -*-
# inf               : Inf for FAST Downlad module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.03
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2025.05.05 - Version 3.00.03
from fast.com.pub import lastVersion, lastVersionTime



def supportData():
    """
    2022-03-27 :    输出支持的数据类型
                    by Chang Chuntao  -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-05-24 :    + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                    CARG_ion、ESAG_ion、ESRG_ion
                    by Chang Chuntao  -> Version : 1.13
    2022-05-31 :    + 新增BIA内资源MGEX_WHU_OSB_bia
                    > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                    by Chang Chuntao  -> Version : 1.14
    2022-07-03 :    + 新增CLK内资源MGEX_WUHU_clk
                    + 新增ERP内资源WUHU_erp
                    + 新增OBX内资源MGEX_WUHU_obx
                    by Chang Chuntao  -> Version : 1.15
    2022-07-13 :    + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-07-22 :    + 新增SP3内资源MGEX_WUH_Hour_sp3
                    + 新增CLK内资源MGEX_WUH_Hour_clk
                    + 新增ERP内资源WUH_Hour_erp
                    by Chang Chuntao  -> Version : 1.17
    2022-07-27 :    > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                    > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                    > 修正MGEX_COD_clk资源
                    by Chang Chuntao  -> Version : 1.18
    2022-09-16 :    + 新增RINEX内MGEX_HK_cors资源
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological,为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
    2022-10-10 :    + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    ***自动输出支持的数据类型
                    by Chang Chuntao  -> Version : 2.01
    """
    from fast.com.pub import gnss_type

    print("     Supported Data:  BRDC : GPS_brdc / GCRE_brdc / GCRE_CNAV_brdm / GCRE_CNAV_brd4 \n")
    max_long = 75
    for gs_list in gnss_type[1:]:
        str_len = 27
        str_print = gs_list[0].rjust(26) + ' : '
        for gs_type in gs_list[1]:
            str_print += gs_type
            str_len += len(gs_type)
            if gs_type == gs_list[1][-1]:
                if '\n' in str_print[-29:]:
                    print(str_print)
                else:
                    print(str_print)
                    print()
            if str_len > max_long:
                str_print += '\n                             '
                str_len = 29
            else:
                str_print += ' / '
                str_len += 3


def fastHelp():
    """
    2022-03-27 :    引导模式输出帮助
                    by Chang Chuntao -> Version : 1.00
    2022-04-12 :    Version update
                    by Chang Chuntao -> Version : 1.10
    """
    print("==================================================================================")
    print("")
    print("     Python program: FAST(File Download and Signal Processing Toolkit for GNSS)")
    print("     ©Copyright 2022.01 @ Chang Chuntao")
    print("     PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    supportData()
    print("     Chang Chuntao | January 2024: FAST program is compiled in Python and used for GNSS data download.\n"
          "                                   It supports two modes with parameter input and terminal input, and\n"
          "                                   supports multi-threaded download mode. The user can specify the nu-\n"
          "                                   mber of download threads. The program supports multiple data downl-\n"
          "                                   oads (see above). If you have any questions, you can contact me th-\n"
          "                                   rough amst-jazz #wechat and 1252443496 #QQ")
    print("     Auther: Chang Chuntao")
    print("     Organization: The GNSS Center, Wuhan University ")
    print("     Version date: " + lastVersionTime + " - Version " + lastVersion)
    print("")


def arg_help():
    """
    2022-03-27 : 参数输入模式输出帮助 by Chang Chuntao -> Version : 1.00
    """
    print("==================================================================================")
    print("")
    print("  FAST : File Download and Signal Processing Toolkit for GNSS.")
    print("  ©Copyright " + lastVersionTime + " - Version " + lastVersion + " @ Chang Chuntao")
    print("  PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    arg_options()


def arg_options():
    """
    2022-03-27 :    Displays help information for command-line options and parameter types.
                    by Chang Chuntao -> Version : 1.00
    2023-06-29 :    Added options for specifying sites and hours.
                    by Chang Chuntao -> Version : 2.09
    """
    from fast.com.pub import printFast
    print("  Usage: FAST <options>")
    print("")
    print("  Available options include:")
    print("")
    print("  -v,  -version                   Display the version of FAST and exit.")
    print("  -h,  -help                      Print this help message.")
    print('  -t,  -type                      Specify GNSS data type(s). Use commas to separate multiple types.')
    print('                                  Example: GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk')
    print("  -l,  -loc                       Specify the download folder [Default: current working directory].")
    print("  -y,  -year                      Specify the year for data download.")
    print("  -d,  -day                       Specify the doy for data download.")
    print("  -s,  -day1                      Specify the start doy for data download.")
    print("  -e,  -day2                      Specify the end doy for data download.")
    print("       -hour                      Specify the hour(s) for data download [Default: 0 - 23].")
    print("  -m,  -month                     Specify the month for data download.")
    print("  -r,  -rename                    Rename downloaded products (limit to 3 characters) [Default: no rename].")
    print("  -u,  -uncompress                Unzip downloaded files [Default: Y].")
    print("                                  Options: Y (unzip) / N (do not unzip).")
    print("  -f,  -file                      Specify a file containing site names (separated by spaces).")
    print("                                  Example: bjfs irkj urum")
    print("  -i,  -site                      Specify site names for data download (separated by commas).")
    print("                                  Example: bjfs,irkj,urum")
    print("  -p,  -process                   Specify the number of threads for parallel processing [Default: 12].")
    print("")
    print("  Examples:")
    print(r"    FAST -t Panda_svnav")
    print(r"    FAST -t GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk -y 2022 -s 22 -e 30 -p 30")
    print(r"    FAST -t GCRE_MGEX_obs -y 2022 -d 22 -i bjfs,abpo -l D:\Code\FAST\test")
    print(r"    FAST -t GCRE_MGEX_obs -y 2022 -d 22 -f D:\Code\FAST\mgex.txt")
    print(r"    FAST -t GCRE_WHU_F_sp3 -y 2022 -d 22 -r whu")
    print(r"    FAST -t IVS_week_snx -y 2022 -m 1")
    print("")
    printFast("Would you like to see the supported data types? (y/n)", "input")
    cont = input("    ")
    if cont.lower() == "y":
        supportData()



def fastSoftwareInformation():
    """
    2023-09.26 :    Software information
    """
    print("==================================================================================")
    print("     FAST           : File Download and Signal Processing Toolkit for GNSS")
    print("     Author         : Chang Chuntao")
    print("     Organization   : The GNSS Center, Wuhan University")
    print("     Contact        : chuntaochang@whu.edu.cn")
    print("     Git            : https://github.com/ChangChuntao/FAST")
    print("     Version        : " + lastVersionTime + " # " + lastVersion)