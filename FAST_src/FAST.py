#!/usr/bin/python3
# FAST_Main      : MAIN
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.0
# Date           : 2022.04.12 - Version 1.1

# Version 1.1    : *新增返回上级菜单操作，输入y回到上级菜单
#                  *通过下载列表解压文件
#                  新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#                  by Chang Chuntao
#                  Github push test 2022 04 29 13 34

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
            PrintGDD("下载结束，是否需要下载其他数据？(y)", "input")
            cont = input("     ")
        else:
            break
else:
    # ARG MODE 带参数运行
    ARG_Mode(argument)  # ARG MODE 主函数
