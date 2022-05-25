#!/usr/bin/python3
# FAST_Batch     :
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.13
# Creation Date  : 2022.05.24 - Version 1.13
# Date           : 2022.05.24 - Version 1.13
import os
import timeit

# 指定可执行程序位置 *** 必选
FAST_Path = r"D:\Code\FAST\Windows\FAST.exe"
# FAST_Path = "/mnt/d/Code/FAST/Linux/FAST"  # 注意LINUX WINDOWS破折号方向

# 指定下载数据类型 *** 必选
# 支持类型查看help.py内Supported_Data函数，或FAST -h查看
DATA_TYPE = ["GPS_IGS_sp3", "GPS_IGS_rnx"]

# 指定下载时间 *** 除特定类型外必选
year = 2022  # 指定年份，无需时间输入的随意指定，但必须存在
doy = [1, 3]  # 连续天，单天则指定doy = [4]

# 指定下载站点 **下载站点文件或时序文件等必选
site_file = r"D:\Code\FAST\Windows\igs.txt"  # 制定sitelist文件绝对路径
#  site_file = r"/mnt/d/Code/FAST/Linux/igs.txt"

# 指定下载位置 *可选
# 如需全部下载至同一路径，指定DD_PATH
# 如需指定各类型下载至不同路径，指定DD_PATH_LIST，其与DATA_TYPE一一对应
DD_PATH = ""
DD_PATH_LIST = [r"D:\Code\FAST\Windows\sp3", r"D:\Code\FAST\Windows\rinex"]
#  DD_PATH_LIST = ["/mnt/d/Code/FAST/Linux/sp3", "/mnt/d/Code/FAST/Linux/rinex"]
# 指定下载月份 *特定类型可选
month = 1

# 指定是否解压，默认为Y *可选
uncomprss = "Y"  # Y：解压；N：不解压

# 指定下载并发数 *可选
process = 8


def FAST_ARG(FAST_Path, DATA_TYPE, year, doy, site_file, DD_PATH, DD_PATH_LIST, month, uncomprss,
             process):
    if os.path.exists(FAST_Path):
        print("FAST批量运行程序启动")
        start_time = timeit.default_timer()
    else:
        print("程序不存在！检查程序路径！")
        return 0

    if len(DATA_TYPE) != len(DD_PATH_LIST) and DD_PATH == "" and len(DATA_TYPE) != 0 and len(DD_PATH_LIST) != 0:
        print("程序不存在！检查程序路径！")
        return 0

    for data_index in range(0, len(DATA_TYPE)):
        arg = FAST_Path + " "
        arg += "-t " + DATA_TYPE[data_index] + " "
        arg += "-y " + str(year) + " "
        if len(doy) == 1:
            arg += "-d " + str(doy[0]) + " "
        elif len(doy) > 1:
            arg += "-o " + str(doy[0]) + " -e " + str(doy[1]) + " "
        if site_file != "":
            arg += "-f " + site_file + " "
        if DD_PATH != "":
            arg += "-l " + DD_PATH + " "
        elif DD_PATH == "" and len(DD_PATH_LIST) != 0:
            arg += "-l " + DD_PATH_LIST[data_index] + " "
        arg += "-m " + str(month) + " "
        if uncomprss == "":
            arg += "-u Y "
        else:
            arg += "-u " + uncomprss + " "
        arg += "-p " + str(process) + " "
        print(arg)
        os.system(arg)

    end_time = timeit.default_timer() - start_time
    print("批量数据下载结束!")
    print("全部运行时间 : %.02f seconds" % end_time)
    input("任意键退出")


FAST_ARG(FAST_Path, DATA_TYPE, year, doy, site_file, DD_PATH, DD_PATH_LIST, month, uncomprss,
         process)
