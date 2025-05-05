# -*- coding: utf-8 -*-
# menu              : Menu for FAST Downlad module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.03
# Creation Date     : 2022.03.27 - Version 1.00
# Date              : 2025.05.05 - Version 3.00.03

from fast.download.inf import fastHelp
from fast.com.pub import printFast, objnum, gnss_type
import sys


def level1menu():
    """
    2022-03-27 :    一级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-22 :    + 新增TRO一级类
                    by Chang Chuntao  -> Version : 1.11
    2022-04-30 :    * 新增GNSS日常使用工具: GNSS_Timestran
                    调整输入模式, 0 -> a -> HELP / b -> GNSS_Timestran,增加分栏
                    by Chang Chuntao  -> Version : 1.12
    2022-05-24 :    + 新增ION一级类
                    by Chang Chuntao  -> Version : 1.13
    2022-07-13 :    + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-09-20 :    > 修正TRO -> TROP
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    by Chang Chuntao  -> Version : 1.23
    2022-10-10 :    + 新增Tables一级类
                    by Chang Chuntao  -> Version : 1.24
    2023-03-17 :    > COSMIC -> LEO
                    by Chang Chuntao  -> Version : 2.08
    2023-09-27 :    + TOOL
                    by Chang Chuntao  -> Version : 3.00
    
    """
    print("")
    print("    +-----------------------------------FAST-----------------------------------+")
    print("    |                                                                          |")
    print("    |    1 : BRDC                2 : SP3                  3 : CLK              |")
    print("    |    4 : OBS                 5 : ERP                  6 : BIA_DCB_OBX      |")
    print("    |    7 : ION_TRO             8 : SINEX                9 : CNES_AR          |")
    print("    |   10 : Time_Series        11 : Velocity_Fields     12 : SLR              |")
    print("    |   13 : LEO                14 : PANDA               15 : GAMIT            |")
    print("    |                                                                          |")
    # print("    +-----------------------------------TOOL-----------------------------------+")
    # print("    |                                                                          |")
    # print("    |    a : obs_analysis        b : time_conver          c : site_selection   |")
    # print("    |    d : merge_data          e : spp                  f : gnss_file_edit   |")
    # print("    |                                                                          |")
    print("    +-----------------------------------HELP-----------------------------------+")
    print("    |                                                                          |")
    print("    |    h : help                                                              |")
    print("    |                                                                          |")
    print("    +--------------------------------------------------------------------------+")

    printFast("Note: 请输入数据编号 (eg. 2 or a)", "input")
    printFast("Note: Please enter the corresponding number or letter (eg. 2 or a)", "input")
    obj = input("  - ")
    while True:
        # if obj in ['a', 'b', 'c', 'd', 'e', 'f', 'h']:
        if obj in ['a', 'b', 'c', 'd', 'e', 'f', 'h']:
            return obj
        elif obj.isdigit():  # 判断输入是否为数字
            if int(obj) > len(gnss_type) or int(obj) < 0:  # 判断输入是否超出列表范围
                print("")
                printFast("Warning: 输入错误,请输入正确编号 / please enter the correct number (eg. 2 or a)", "input")
                obj = input("    ")
            else:
                obj = int(obj)
                return obj
        else:
            printFast("Warning: 输入错误,请输入正确编号 / please enter the correct number (eg. 2 or a)", "input")
            obj = input("    ")


def level2menu(obj):
    """
    2022-03-27 :    二级菜单 by Chang Chuntao -> Version : 1.00
    2022-04-12 :    新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    * 新增返回上级菜单操作,输入y回到上级菜单
                    by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-04-30 :    * 新增GNSS日常使用工具：GNSS_Timestran
                    gnssTimesTran调用
                    by Chang Chuntao  -> Version : 1.12
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
    2022-09-16 :    + 新增RINEX内MGEX_HK_cors
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    > 修正TRO -> TROP
                    + 新增TROP内资源Meteorological
                    by Chang Chuntao  -> Version : 1.22
    2022-09-28 :    + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
                    by Chang Chuntao  -> Version : 1.23
    2022-10-10 :    + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    ****重新配置分组 !
                    ****新增QT界面！
                    > BIA DCB OBX -> BIA_DCB_OBX
                    > ION TRO -> ION_TRO
                    > ATX SW_EOP Tables<PANDA> -> PANDA
                    > Tables<GAMIT> -> GAMIT
                    + IGS_hfile -> GAMIT
    2022-11-10 :    + 新增MGEX_WUHR_sp3、MGEX_WUHR_clk
                    by Chang Chuntao  -> Version : 2.02
    2022-11-15 :    + 新增GRE_IGS_01S
                    by Chang Chuntao  -> Version : 2.03
    2022-12-04 :    > MGEX_WUH_sp3 -> MGEX_WHU_F_sp3 / MGEX_WUHR_sp3 -> MGEX_WHU_R_sp3 / MGEX_WUHU_sp3 -> MGEX_WHU_U_sp3
                    > MGEX_WUH_Hour_sp3 -> MGEX_WHU_Hour_sp3 / MGEX_SHA_sp3 -> MGEX_SHA_F_sp3 / MGEX_COD_sp3 -> MGEX_COD_F_sp3
                    > MGEX_GRG_sp3 -> MGEX_GRG_F_sp3 / MGEX_GFZ_R_sp3 -> MGEX_GFZR_sp3 / GRE_CODR_sp3 -> GRE_COD_R_sp3
                    > GLO_IGL_sp3 -> GLO_IGL_F_sp3
                    + MGEX_GFZ_F_sp3
                    > MGEX_WUH_clk -> MGEX_WHU_F_clk / MGEX_WUHR_clk -> MGEX_WHU_R_clk / MGEX_WUHU_clk -> MGEX_WHU_U_clk
                    > MGEX_WUH_Hour_clk -> MGEX_WHU_Hour_clk / MGEX_COD_clk -> MGEX_COD_F_clk / MGEX_GRG_clk -> MGEX_GRG_F_clk
                    > MGEX_GFZR_clk -> MGEX_GFZ_R_clk
                    + MGEX_SHA_F_clk / MGEX_GFZ_F_clk / GRE_COD_R_clk / GLO_IGL_F_clk
                    > WUH_erp -> WHU_F_erp / WUHU_erp -> WHU_U_erp / GFZ_erp -> GFZ_F_erp / COD_erp -> COD_R_erp
                    > WUH_Hour_erp -> WHU_Hour_erp
                    > MGEX_COD_bia -> MGEX_COD_R_bia / MGEX_GFZ_bia -> MGEX_GFZ_R_bia / MGEX_WHU_ABS_bia -> MGEX_WHU_R_ABS_bia
                    > MGEX_WHU_OSB_bia -> MGEX_WHU_R_OSB_bia
                    x MGEX_WHU_OSB(与MGEX_WHU_R_OSB_bia重复)
                    > MGEX_CAS_dcb -> MGEX_CAS_R_dcb
                    > MGEX_WUH_obx -> MGEX_WHU_F_obx / MGEX_COD_obx -> MGEX_COD_F_obx / MGEX_GFZ_obx -> MGEX_GFZ_F_obx
                    > MGEX_WUHU_obx -> MGEX_WHU_U_obx
                    > WUHG_ion -> WHUG_ion
                    + MGEX_COD_F_bia
                    by Chang Chuntao  -> Version : 2.05
    2023-01-13 :    > MGEX_IGS_atx -> MGEX_IGS14_atx
                    + MGEX_IGS20_atx
                    x 删除GPS_GFZ_sp3 / GPS_GFZ_clk
                    > MGEX_GFZ_F_sp3 -> GRE_GFZ_F_sp3 / MGEX_GFZ_F_clk -> GRE_GFZ_F_clk
                    by Chang Chuntao  -> Version : 2.06
    2023-02-02 :    > P1C1 重复
                    > 修正clk数字
                    + COD_F_erp
                    + IGS_crd_snx / COD_sol_snx / ESA_sol_snx / GFZ_sol_snx / GRG_sol_snx / NGS_sol_snx / SIO_sol_snx
                    by Chang Chuntao  -> Version : 2.07
    2023-03-17 :    + COD_F_ion # 2023-02-27
                    > COSMIC -> LEO
                    + GRACE_dat / GRACE_rnxapp / GRACE_fo_dat / GRACE_fo1_sp3 / GRACE_fo1_sp3 / CHAMP_rnx / CHAMP_sp3
                    + SWARM_rnx / SWARM_sp3
                    by Chang Chuntao  -> Version : 2.08
    2023-06-30 :    > GPS_COD_bia -> GPS_COD_F_osb / MGEX_COD_F_bia -> MGEX_COD_F_osb / MGEX_COD_R_bia -> GRE_COD_R_osb
                    > MGEX_WHU_R_OSB_bia -> MGEX_WHU_R_osb / MGEX_WHU_R_ABS_bia -> MGEX_WHU_R_abs
                    > MGEX_GFZ_R_bia -> MGEX_GFZ_R_osb
                    x COD_F_ion, 与CODG_ion重复
                    by Chang Chuntao  -> Version : 2.09
    2023-08-11 :    + MGEX_WHU_RTS_sp3 / MGEX_WHU_RTS_clk
                    + MGEX_IAC_F_sp3 / MGEX_IAC_F_clk / MGEX_CAS_R_osb
                    by Chang Chuntao  -> Version : 2.10
    2023-09-20 :    + GRE_JAX_U_sp3 / GRE_JAX_U_clk_30s
                    by Chang Chuntao  -> Version : 2.11
    2025-05-05 :    + update inf see fast\download\ftpSrc.py
                    by Chang Chuntao  -> Version : 3.00.03
    """
    print("")
    if obj == 1:
        print("    +------------------------------------BRDC----------------------------------+")
        print("    |                                                                          |")
        print("    +-------------------------------------GPS----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GPS_brdc                                                           |")
        print("    |                                                                          |")
        print("    +-----------------------------------GCRE-----------------------------------+")
        print("    |                                                                          |")
        print("    |   2 : GCRE_brdc            3 : GCRE_CNAV_brdm       4 : GCRE_CNAV_brd4   |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 2:
        print("    +------------------------------------SP3-----------------------------------+")
        print("    |                                                                          |")
        print("    +------------------------------------GPS-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GPS_IGS_sp3          2 : GPS_IGR_sp3          3 : GPS_IGU_sp3      |")
        print("    |   4 : GPS_GRG_sp3                                                        |")
        print("    |                                                                          |")
        print("    +-----------------------------------GCRE-----------------------------------+")
        print("    |                                                                          |")
        print("    |   5 : GCRE_WHU_F_sp3       6 : GCRE_WHU_R_sp3       7 : GCRE_WHU_U_sp3   |")
        print("    |   8 : GCRE_WHU_H_sp3       9 : GCRE_WHU_RTS_sp3    10 : GCRE_SHA_F_sp3   |")
        print("    |  11 : GCRE_COD_F_sp3      12 : GCRE_GRG_F_sp3      13 : GCRE_GFZ_R_sp3   |")
        print("    |  14 : GCRE_IAC_F_sp3                                                     |")
        print("    |  15 : GRE_GFZ_F_sp3       16 : GRE_COD_R_sp3       17 : GLO_IGL_F_sp3    |")
        print("    |  18 : GRE_JAX_U_sp3       19 : CEG_GRG_U_sp3                             |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 3:
        print("    +------------------------------------CLK-----------------------------------+")
        print("    |                                                                          |")
        print("    +------------------------------------GPS-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GPS_IGS_clk         2 : GPS_IGR_clk           3 : GPS_GRG_clk      |")
        print("    |   4 : GPS_IGS_clk_30s                                                    |")
        print("    |                                                                          |")
        print("    +-----------------------------------GCRE-----------------------------------+")
        print("    |                                                                          |")
        print("    |   5 : GCRE_WHU_F_clk      6 : GCRE_WHU_R_clk        7 : GCRE_WHU_U_clk   |")
        print("    |   8 : GCRE_WHU_U_clk_30s  9 : GCRE_WHU_RTS_clk     10 : GCRE_SHA_F_clk   |")
        print("    |  11 : GCRE_COD_F_clk     12 : GCRE_GRG_F_clk       13 : GCRE_GFZ_R_clk   |")
        print("    |  14 : GCRE_IAC_F_clk                                                     |")
        print("    |  15 : GRE_GFZ_F_clk      16 : GRE_COD_R_clk        17 : GLO_IGL_F_clk    |")
        print("    |  18 : GRE_COD_F_clk_30s  19 : GRE_JAX_U_clk_30s    20 : CEG_GRG_U_clk    |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 4:
        print("    +------------------------------------OBS-----------------------------------+")
        print("    |                                                                          |")
        print("    +------------------------------------GPS-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GPS_IGS_obs         2 : GPS_USA_cors          3 : GPS_HK_cors      |")
        print("    |   4 : GPS_SIRGAS                                                         |")
        print("    |                                                                          |")
        print("    +-----------------------------------GCRE-----------------------------------+")
        print("    |                                                                          |")
        print("    |   5 : GCRE_MGEX_obs       6 : GCRE_MGEX_obs_01s                          |")
        print("    |   7 : GCRE_HK_cors        8 : GCRE_EU_cors          9 : GCRE_AU_cors     |")
        print("    |  10 : GRE_MGEX_obs_01s   11 : GCRE_SIRGAS                                |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 5:
        print("    +-----------------------------------ERP------------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : IGS_F_erp           2 : IGS_R_erp             3 : WHU_F_erp        |")
        print("    |   4 : COD_F_erp           5 : WHU_U_erp             6 : GFZ_R_erp        |")
        print("    |   7 : COD_R_erp           8 : WHU_H_erp                                  |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 6:
        print("    +-------------------------------BIA_DCB_OBX--------------------------------+")
        print("    |                                    |                                     |")
        print("    +-----------------------------------BIA------------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GPS_COD_F_osb       2 : GE_GRG_F_osb          3 : GRE_COD_R_osb    |")
        print("    |   4 : GCRE_WHU_F_osb      5 : GCRE_WHU_R_osb        6 : GCRE_WHU_R_abs   |")
        print("    |   7 : GCRE_COD_F_osb      8 : GCRE_GFZ_R_osb        9 : GCRE_CAS_R_osb   |")
        print("    |  10 : GCRE_WHU_U_osb     11 : GCRE_WHU_RTS_osb                           |")
        print("    |                                                                          |")
        print("    +-----------------------------------DCB------------------------------------+")
        print("    |                                                                          |")
        print("    |  12 : GPS_COD_dcb        13 : GCRE_CAS_R_dcb                             |")
        print("    |  14 : P1C1               15 : P1P2                 16 : P2C2             |")
        print("    |                                                                          |")
        print("    +-----------------------------------OBX------------------------------------+")
        print("    |                                                                          |")
        print("    |  17 : GPS_COD_F_obx      18 : GPS_GRG_F_obx                              |")
        print("    |  19 : GCRE_WHU_F_obx     20 : GCRE_WHU_R_obx       21 : GCRE_WHU_U_obx   |")
        print("    |  22 : GCRE_COD_F_obx     23 : GCRE_GFZ_R_obx                             |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 7:
        print("    +---------------------------------ION_TRO----------------------------------+")
        print("    |                                    |                                     |")
        print("    +-----------------------------------ION------------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : IGSG_ion            2 : IGRG_ion              3 : WHUG_ion         |")
        print("    |   4 : WURG_ion            5 : CODG_ion              6 : CORG_ion         |")
        print("    |   7 : UQRG_ion            8 : UPRG_ion              9 : JPLG_ion         |")
        print("    |  10 : JPRG_ion           11 : CASG_ion             12 : CARG_ion         |")
        print("    |  13 : ESAG_ion           14 : ESRG_ion                                   |")
        print("    |                                                                          |")
        print("    +-----------------------------------TRO------------------------------------+")
        print("    |                                                                          |")
        print("    |  15 : IGS_trop           16 : COD_trop             17 : JPL_trop         |")
        print("    |  18 : GRID_1x1_VMF3      19 : GRID_2.5x2_VMF1      20 : GRID_5x5_VMF3    |")
        print("    |  21 : vmf1grd            22 : Meteorological                             |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 8:
        print("    +----------------------------------SINEX-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : IGS_day_snx         2 : IGS_week_snx          3 : IVS_week_snx     |")
        print("    |   4 : ILS_week_snx        5 : IDS_week_snx                               |")
        print("    |   6 : IGS_crd_snx         7 : COD_sol_snx           8 : ESA_sol_snx      |")
        print("    |   9 : GFZ_sol_snx        10 : GRG_sol_snx          11 : NGS_sol_snx      |")
        print("    |  12 : SIO_sol_snx                                                        |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 9:
        print("    +---------------------------------CNES_AR----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : CNES_post           2 : CNES_realtime         3 : CNES_bia         |")
        print("    |   4 : CNES_backup                                                        |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 10:
        print("    +-------------------------------Time_Series--------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : IGS14_TS_ENU        2 : IGS14_TS_XYZ          3 : Series_TS_Plot   |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 11:
        print("    +-----------------------------Velocity_Fields------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : IGS14_Venu          2 : IGS08_Venu            3 : PLATE_Venu       |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 12:
        print("    +-----------------------------------SLR------------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : HY_SLR              2 : GRACE_SLR             3 : BEIDOU_SLR       |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 13:
        print("    +-----------------------------------LEO------------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : GRACE_dat           2 : GRACE_rnxapp                               |")
        print("    |   3 : GRACE_fo_dat        4 : GRACE_fo1_sp3         5 : GRACE_fo2_sp3    |")
        print("    |   6 : CHAMP_rnx           7 : CHAMP_sp3                                  |")
        print("    |   8 : SWARM_A_rnx         9 : SWARM_B_rnx          10 : SWARM_C_rnx      |")
        print("    |  11 : SWARM_A_sp3        12 : SWARM_B_sp3          13 : SWARM_C_sp3      |")
        print("    |  14 : COSMIC_1_att       15 : COSMIC_1_crx         16 : COSMIC_1_orb     |")
        print("    |  17 : COSMIC_2_att       18 : COSMIC_2_crx         19 : COSMIC_2_orb     |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")

    elif obj == 14:
        print("    +----------------------------------PANDA-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : Panda_jpleph_de405  2 : Panda_poleut1         3 : Panda_EGM        |")
        print("    |   4 : Panda_oceanload     5 : Panda_oceantide       6 : Panda_utcdif     |")
        print("    |   7 : Panda_antnam        8 : Panda_svnav           9 : Panda_nutabl     |")
        print("    |  10 : Panda_ut1tid       11 : Panda_leap_sec       12 : MGEX_IGS14_atx   |")
        print("    |  13 : MGEX_IGS20_atx     14 : SW_EOP               15 : Panda_gpsrapid   |")
        print("    |  16 : EOP_C04                                                            |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == 15:
        print("    +----------------------------------GAMIT-----------------------------------+")
        print("    |                                                                          |")
        print("    |   1 : Gamit_pmu_bull      2 : Gamit_ut1usno         3 : Gamit_poleusno   |")
        print("    |   4 : Gamit_dcb_dat       5 : Gamit_soltab          6 : Gamit_luntab     |")
        print("    |   7 : Gamit_leap_sec      8 : Gamit_nutabl          9 : Gamit_antmod     |")
        print("    |  10 : Gamit_svnav        11 : Gamit_rcvant         12 : Gamit_nbody      |")
        print("    |                                                                          |")
        print("    +---------------------------------SOLUTION---------------------------------+")
        print("    |                                                                          |")
        print("    |  13 : IGS_hfile                                                          |")
        print("    |                                                                          |")
        print("    +--------------------------------------------------------------------------+")
    elif obj == "h":
        fastHelp()
        return 0
    elif obj == "b":
        # gnssTimesTran()
        return 0

    printFast("Note: 请输入数据编号 / Please enter the data number (eg. 2)", "input")  # 二级索引
    printFast("Note: 返回上级目录,输入'y' / To go back to the parent directory, enter 'y'", "input")  # 二级索引
    subnum = input("    ")
    while True:
        if subnum == "y" or subnum == "Y":
            return "y"
        else:
            if subnum.isdigit():  # 判断是否为数字
                if int(subnum) > objnum[obj - 1] or int(subnum) < 1:  # 判断输入是否超出列表范围
                    print("")
                    printFast("Warning: 输入错误,请输入正确编号 / please enter the correct number (eg. 2)", "input")
                    printFast("Note: 返回上级目录,输入'y' / To go back to the parent directory, enter 'y'", "input")  # 二级索引
                    subnum = input("    ")  # 二级索引
                else:
                    subnum = int(subnum)
                    return subnum
            else:
                printFast("Warning: 输入错误,请输入正确编号 / please enter the correct number (eg. 2)", "input")
                printFast("Note: 返回上级目录,输入'y' / To go back to the parent directory, enter 'y'", "input")  # 二级索引
                subnum = input("    ")
