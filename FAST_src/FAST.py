#!/usr/bin/python3
# -*- coding: utf-8 -*-
# FAST_Main      : MAIN of Fusion Abundant multi-Source data download Terminal
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.05
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022-12-04 - Version 2.05

def FAST():
    """
    Version 1.00  : * Fusion Abundant multi-Source data download Terminal
                    by Chang Chuntao  # 2022-03-27

    Version 1.10  : * 新增返回上级菜单操作，输入y回到上级菜单
                    * 通过下载列表解压文件
                    + 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  # 2022-04-12

    Version 1.11  : + 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF3、 GRID_5x5_VMF3资源
                    > 修正GPS_HK_cors节点资源
                    by Chang Chuntao  # 2022-04-22

    Version 1.12  : > 调整一级输入模式引导, 0 -> a -> Help / b -> GNSS_Timestran，增加分栏显示
                    * 新增GNSS日常使用工具：GNSS_Timestran
                    > 修正GPS_USA_cors节点
                    by Chang Chuntao  # 2022-04-30

    Version 1.13  : + 新增ION内资源WURG_ion/CODG_ion/CORG_ion/UQRG_ion/UPRG_ion/JPLG_ion/JPRG_ion/CASG_ion/
                    CARG_ion/ESAG_ion/ESRG_ion
                    > 修正MGEX_GFZ_clk节点内 05M -> 30S
                    > 修正MGEX_brdm节点内 BRDM00DLR_S_ -> BRDC00IGS_R_，但保留BRDM00DLR_S_
                    by Chang Chuntao  # 2022-05-24

    Version 1.14  : + 新增BIA内资源MGEX_WHU_OSB_bia
                    > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                    by Chang Chuntao  # 2022-05-31

    Version 1.15  : + 新增CLK内资源MGEX_WUHU_clk
                    + 新增ERP内资源WUHU_erp
                    + 新增OBX内资源MGEX_WUHU_obx
                    by Chang Chuntao  # 2022-07-03

    Version 1.16  : + 新增SpaceData一级类
                    + 新增SpaceData内资源SW_EOP
                    by Chang Chuntao  # 2022-07-13

    Version 1.17  : + 新增SP3内资源MGEX_WUH_Hour_sp3
                    + 新增CLK内资源MGEX_WUH_Hour_clk
                    + 新增ERP内资源WUH_Hour_erp
                    by Chang Chuntao  # 2022-07-22

    Version 1.18  : > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                    > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                    > 修正MGEX_COD_clk资源
                    by Chang Chuntao  # 2022-07-27

    Version 1.19  : > 修正时序文件下载需求
                    by Chang Chuntao  # 2022-08-04

    Version 1.20  : > 修正广播星历文件判定
                    + 站点文件可支持行列两种格式，或混合模式
                    by Chang Chuntao  # 2022-09-09

    Version 1.21  : + 新增RINEX内MGEX_HK_cors
                    新增替换站点字符串子函数Get_Ftp -> replaceSiteStr
                    by Chang Chuntao  # 2022-09-16

    Version 1.22  : > 修正TRO -> TROP
                    + 新增TROP内资源Meteorological
                    by Chang Chuntao  # 2022-09-20

    Version 1.23  : + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
                    by Chang Chuntao  # 2022-09-28

    Version 1.24  : + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    > 修复无需其他参数输入下载类下载
                    by Chang Chuntao  # 2022-10-10

    Version 1.25  : > 添加DORIS判断,每周第0天下载
                    > IVS_week_snx : 更换网站：ivs.bkg.bund.de -> ivsopar.obspm.fr
                    > IDS_week_snx : 更换策略：wd12/14         -> wd16/19
                    by Chang Chuntao  # 2022-11-02

    Version 2.00  : ***新增界面版
                    by Chang Chuntao  # 2022-11-08

    Version 2.01  : + 新增IGS_hfile
                    by Chang Chuntao  # 2022-11-09

    Version 2.02    + 新增MGEX_WUHR_sp3、MGEX_WUHR_clk
                    by Chang Chuntao  # 2022-11-10

    Version 2.03    + 新增GRE_IGS_01S / GCRE_MGEX_01S
                    by Chang Chuntao  # 2022-11-15

    Version 2.04    > MGEX_brdm -> MGEX_brdc
                    + MGEX_CNAV_brdm / MGEX_CNAV_brdm
                    > GPS_IGS_sp3 / GPS_IGS_clk : igs -> IGS0OPSFIN
                    > GPS_IGR_sp3 / GPS_IGR_clk : igr -> IGS0OPSRAP
                    > GPS_IGU_sp3               : igu -> IGS0OPSULT
                    + GRE_CODR_sp3 / GRE_CODR_clk
                    by Chang Chuntao  # 2022-12-02

    Version 2.05    > MGEX_WUH_sp3 -> MGEX_WHU_F_sp3 / MGEX_WUHR_sp3 -> MGEX_WHU_R_sp3 / MGEX_WUHU_sp3 -> MGEX_WHU_U_sp3
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
                    + 增加tgz解压,支持tgz解压/COD产品更名
                    by Chang Chuntao  # 2022-12-04

    Version 2.06    > MGEX_IGS_atx -> MGEX_IGS14_atx
                    + MGEX_IGS20_atx
                    x 删除GPS_GFZ_sp3 / GPS_GFZ_clk
                    > MGEX_GFZ_F_sp3 -> GRE_GFZ_F_sp3 / MGEX_GFZ_F_clk -> GRE_GFZ_F_clk
                    > IGS rename -> GPS_IGS_sp3 / GPS_IGR_sp3 / GPS_IGU_sp3 / GRE_COD_R_sp3 / GPS_IGS_clk
                    >               GPS_IGR_clk / GPS_IGS_clk_30s / GRE_COD_R_clk /
                    + 支持直接输入站点名
                    by Chang Chuntao  # 2023-01-14
    """
    import sys
    from ARG_Mode import ARG_Mode
    from CDD_Mode import CDD_Mode
    from FAST_Print import PrintGDD

    argument = sys.argv[1:]  # 程序是否带参数运行
    if len(argument) == 0:
        # CDD MODE 无参数命令行运行
        cont = "y"
        while True:  # 循环运行
            if cont == "y" or cont == "Y":
                CDD_Mode()  # CDD MODE 主函数
                PrintGDD("运行结束，是否重新引导？(y)", "input")
                cont = input("     ")
            else:
                break
    else:
        # ARG MODE 带参数运行
        ARG_Mode(argument)  # ARG MODE 主函数


if __name__ == '__main__':
    FAST()