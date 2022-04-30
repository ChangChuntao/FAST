#!/usr/bin/python3
# FAST_Time      : MAIN of FAST_Time
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.12
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.04.30 - Version 1.12

from FAST_Print import PrintGDD
from help import fastSoftwareInformation
from GNSS_Timestran import gnssTimesTran

# 2022-04-30 : 引导 by Chang Chuntao -> Version : 1.00
fastSoftwareInformation()
cont = "y"
while True:  # 循环运行
    if cont == "y" or cont == "Y":
        print()
        gnssTimesTran()
        PrintGDD("运行结束，是否重新引导？(y)", "input")
        cont = input("     ")
    else:
        break
