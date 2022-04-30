#!/usr/bin/python3
# FAST_Print      : Program output style
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.12
# Creation Date  : 2022.03.27 - Version 1.0

# 2022-03-27 : * 屏幕打印样式 by Chang Chuntao -> Version : 1.00
# 2022-04-30 : * 新增nothing
def PrintGDD(string, printtype):
    if printtype == "input":
        print("  -  " + string)
    elif printtype == "normal":
        print("  *  " + string)
    elif printtype == "fail":
        print("  x  " + string)
    elif printtype == "warning":
        print("  #  " + string)
    elif printtype == "important":
        print(" *** " + string)
    elif printtype == "nothing":
        print("     " + string)
