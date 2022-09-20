#!/usr/bin/python3
# Help           : Help for all mode
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.22
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.09.20 - Version 1.22

from FAST_Print import PrintGDD


def Supported_Data():
    """
    2022-03-27 : 输出支持的数据类型 by Chang Chuntao -> Version : 1.00
    2022-04-12 : 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                 by Chang Chuntao  -> Version : 1.10
    2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                 by Chang Chuntao  -> Version : 1.11
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
    2022-09-16 : + 新增RINEX内MGEX_HK_cors资源
                 by Chang Chuntao  -> Version : 1.21
    2022-09-20 : + 新增TROP内资源Meteorological，为需要站点的气象文件
                 by Chang Chuntao  -> Version : 1.22
    """
    print("     Supported Data:  BRDC : GPS_brdc / MGEX_brdm ")
    print("")
    print("                       SP3 : GPS_IGS_sp3 / GPS_IGR_sp3 / GPS_IGU_sp3 / GPS_GFZ_sp3 / GPS_GRG_sp3 / ")
    print("                             MGEX_WUH_sp3 / MGEX_WUHU_sp3 / MGEX_GFZR_sp3 / MGEX_COD_sp3 / ")
    print("                             MGEX_SHA_sp3 / MGEX_GRG_sp3 ")
    print("                             GLO_IGL_sp3 / MGEX_WUH_Hour_sp3")
    print("")
    print("                     RINEX : GPS_IGS_rnx / MGEX_IGS_rnx / GPS_USA_cors / GPS_HK_cors / GPS_EU_cors / ")
    print("                             GPS_AU_cors / MGEX_HK_cors")
    print("")
    print("                       CLK : GPS_IGS_clk / GPS_IGR_clk / GPS_IGU_clk / MGEX_GFZR_clk / GPS_GRG_clk /  ")
    print("                             GPS_IGS_clk_30s  ")
    print("                             MGEX_WUH_clk / MGEX_COD_clk / MGEX_GFZ_clk / MGEX_GRG_clk / WUH_PRIDE_clk ")
    print("                             MGEX_WUHU_clk / MGEX_WUH_Hour_clk")
    print("")
    print("                       ERP : IGS_erp / WUH_erp / COD_erp / GFZ_erp/ IGR_erp/ WUHU_erp / WUH_Hour_erp")
    print("")
    print(
        "                       BIA : MGEX_WHU_ABS_bia / MGEX_WHU_OSB_bia / GPS_COD_bia / MGEX_COD_bia / MGEX_GFZ_bia")
    print("")
    print("                       ION : IGSG_ion / IGRG_ion / WUHG_ion / WURG_ion / CODG_ion / CORG_ion / UQRG_ion")
    print("                             UPRG_ion / JPLG_ion / JPRG_ion / CASG_ion / CARG_ion / ESAG_ion / ESRG_ion")
    print("")
    print("                     SINEX : IGS_day_snx / IGS_week_snx / IVS_week_snx / ILS_week_snx / IDS_week_snx ")
    print("")
    print("                    CNES_AR : CNES_post / CNES_realtime ")
    print("")
    print("                       ATX : MGEX_IGS_atx")
    print("")
    print("                       DCB : GPS_COD_dcb / MGEX_CAS_dcb / MGEX_WHU_OSB / P1C1 / P1P2 / P2C2")
    print("")
    print("               Time_Series : IGS14_TS_ENU / IGS14_TS_XYZ / Series_TS_Plot")
    print("")
    print("           Velocity_Fields : IGS14_Venu / IGS08_Venu / PLATE_Venu")
    print("")
    print("                       SLR : HY_SLR / GRACE_SLR / BEIDOU_SLR")
    print("")
    print("                       OBX : GPS_COD_obx / GPS_GRG_obx / MGEX_WUH_obx / MGEX_COD_obx / MGEX_GFZ_obx")
    print("                             MGEX_WUHU_obx")
    print("")
    print("                      TROP : IGS_zpd / COD_tro / JPL_tro / GRID_1x1_VMF3 / GRID_2.5x2_VMF1 / GRID_5x5_VMF3")
    print("                             Meteorological")
    print("")
    print("                 SpaceData : SW_EOP")


def cddhelp():
    """
    2022-03-27 : 引导模式输出帮助  by Chang Chuntao -> Version : 1.00
    2022-04-12 : Version update by Chang Chuntao -> Version : 1.10
    2022-04-22 : Version update by Chang Chuntao -> Version : 1.11
    2022-04-30 : Version update by Chang Chuntao -> Version : 1.12
    2022-05-24 : Version update by Chang Chuntao -> Version : 1.13
    2022-05-31 : Version update by Chang Chuntao -> Version : 1.14
    2022-07-03 : Version update by Chang Chuntao -> Version : 1.15
    2022-07-13 : Version update by Chang Chuntao -> Version : 1.16
    2022-07-22 : Version update by Chang Chuntao -> Version : 1.17
    2022-07-28 : Version update by Chang Chuntao -> Version : 1.18
    2022-08-04 : Version update by Chang Chuntao -> Version : 1.19
    2022-09-11 : Version update by Chang Chuntao -> Version : 1.20
    2022-09-16 : Version update by Chang Chuntao -> Version : 1.21
    2022-09-20 : Version update by Chang Chuntao -> Version : 1.22
    """
    print("==================================================================================")
    print("")
    print("     Python program: FAST(Fusion Abundant multi-Source data download Terminal)")
    print("     ©Copyright 2022.01 @ Chang Chuntao")
    print("     PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    Supported_Data()
    print("")
    print("     Chang Chuntao | January 2020: FAST program is compiled in Python and used for GNSS data download.\n"
          "                                   It supports two modes with parameter input and terminal input, and\n"
          "                                   supports multi-threaded download mode. The user can specify the nu-\n"
          "                                   mber of download threads. The program supports multiple data downl-\n"
          "                                   oads (see above). If you have any questions, you can contact me th-\n"
          "                                   rough amst-jazz #wechat and 1252443496 #QQ")
    print("     Auther: Chang Chuntao")
    print("     Organization: The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping")
    print("     Current version date: 2022.03.27 - Version 1.00")
    print("     Initial version date: 2022.09.20 - Version 1.22")
    print("")


def arg_help():
    """
    2022-03-27 : 参数输入模式输出帮助 by Chang Chuntao -> Version : 1.00
    """
    print("==================================================================================")
    print("")
    print("  FAST : Fusion Abundant multi-Source data download Terminal")
    print("  ©Copyright 2022.01 @ Chang Chuntao")
    print("  PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !")
    print("")
    arg_options()


def arg_options():
    """
    2022-03-27 : 参数输入模式输出帮助，参数类型帮助 by Chang Chuntao -> Version : 1.00
    """
    print("  Usage: FAST <options>")
    print("")
    print("  Where the following are some of the options avaiable:")
    print("")
    print("  -v,  --version                   display the version of GDD and exit")
    print("  -h,  --help                      print this help")
    print('  -t,  --type                      GNSS type, if you need to download multiple data,')
    print('                                   Please separate characters with " , "')
    print("                                   Example : GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk")
    print("  -l,  --loc                       which folder is the download in")
    print("  -y,  --year                      where year are the data to be download")
    print("  -d,  --day                       where day are the data to be download")
    print("  -o,  --day1                      where first day are the data to be download")
    print("  -e,  --day2                      where last day are the data to be download")
    print("  -m,  --month                     where month are the data to be download")
    print("  -u,  --uncomprss Y/N             Y - unzip file (default)")
    print("                                   N - do not unzip files")
    print("  -f,  --file                      site file directory,The site names in the file are separated by spaces.")
    print("                                   Example : bjfs irkj urum ")
    print("  -p   --process                   number of threads (default 12)")
    print("")
    print(r"  Example: FAST -t MGEX_IGS_atx")
    print(r"           FAST -t GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk -y 2022 -o 22 -e 30 -p 30")
    print(r"           FAST -t MGEX_WUH_sp3 -y 2022 -d 22 -u N -l D:\code\CDD\Example")
    print(r"           FAST -t MGEX_IGS_rnx -y 2022 -d 22 -f D:\code\cdd\mgex.txt")
    print(r"           FAST -t IVS_week_snx -y 2022 -m 1")
    print("")
    PrintGDD("是否查看支持的数据类型？(y)", "input")
    cont = input("     ")
    if cont == "y" or cont == "Y":
        Supported_Data()


def fastSoftwareInformation():
    """
    2022-04-30 : Software information by Chang Chuntao -> Version : 1.12
    2022-05-24 : Version update       by Chang Chuntao -> Version : 1.13
    2022-05-31 : Version update       by Chang Chuntao -> Version : 1.14
    2022-07-03 : Version update       by Chang Chuntao -> Version : 1.15
    2022-07-13 : Version update       by Chang Chuntao -> Version : 1.16
    2022-07-22 : Version update       by Chang Chuntao -> Version : 1.17
    2022-07-28 : Version update       by Chang Chuntao -> Version : 1.18
    2022-08-04 : Version update       by Chang Chuntao -> Version : 1.19
    2022-09-11 : Version update       by Chang Chuntao -> Version : 1.20
    2022-09-16 : Version update       by Chang Chuntao -> Version : 1.21
    2022-09-20 : Version update       by Chang Chuntao -> Version : 1.22
    """
    print("==================================================================================")
    print("     FAST           : Fusion Abundant multi-Source data download Terminal")
    print("     Author         : Chang Chuntao")
    print("     Copyright(C)   : The GNSS Center, Wuhan University & ")
    print("                      Chinese Academy of Surveying and mapping")
    print("     Contact        : QQ@1252443496 & WECHAT@amst-jazz GITHUB@ChangChuntao")
    print("     Git            : https://github.com/ChangChuntao/FAST.git")
    print("     Version        : 1.22 # 2022-09-20")
