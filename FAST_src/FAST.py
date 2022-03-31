#!/usr/bin/python3
# FAST_Main      : MAIN
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.23

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
