#!/usr/bin/python3
# FAST_Main      : MAIN of Fusion Abundant multi-Source data download Terminal
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.15
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.07.13 - Version 1.16

# Version 1.00   : * Fusion Abundant multi-Source data download Terminal
#                  by Chang Chuntao  # 2022-03-27
#
# Version 1.10   : * 新增返回上级菜单操作，输入y回到上级菜单
#                  * 通过下载列表解压文件
#                  + 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#                  by Chang Chuntao  # 2022-04-12
#
# Version 1.11   : + 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF3、 GRID_5x5_VMF3资源
#                  > 修正GPS_HK_cors节点资源
#                  by Chang Chuntao  # 2022-04-22
#
# Version 1.12   : > 调整一级输入模式引导, 0 -> a -> Help / b -> GNSS_Timestran，增加分栏显示
#                  * 新增GNSS日常使用工具：GNSS_Timestran
#                  > 修正GPS_USA_cors节点
#                  by Chang Chuntao  # 2022-04-30
#
# Version 1.13   : + 新增ION内资源WURG_ion/CODG_ion/CORG_ion/UQRG_ion/UPRG_ion/JPLG_ion/JPRG_ion/CASG_ion/
#                  CARG_ion/ESAG_ion/ESRG_ion
#                  > 修正MGEX_GFZ_clk节点内 05M -> 30S
#                  > 修正MGEX_brdm节点内 BRDM00DLR_S_ -> BRDC00IGS_R_，但保留BRDM00DLR_S_
#                  by Chang Chuntao  # 2022-05-24
#
# Version 1.14   : + 新增BIA内资源MGEX_WHU_OSB_bia
#                  > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
#                  by Chang Chuntao  # 2022-05-31
#
# Version 1.15   : + 新增CLK内资源MGEX_WUHU_clk
#                  + 新增ERP内资源WUHU_erp
#                  + 新增OBX内资源MGEX_WUHU_obx
#                  by Chang Chuntao  # 2022-07-03
#
# Version 1.16   : + 新增SpaceData一级类
#                  + 新增SpaceData内资源SW_EOP
#                  by Chang Chuntao  # 2022-07-13
#
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
