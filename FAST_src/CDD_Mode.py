#!/usr/bin/python3
# CDD_Mode       : Direct run program mode
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.11
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.04.12 - Version 1.11

from CDD_Sub import *
from FAST_Print import PrintGDD
from GNSS_TYPE import gnss_type


# 2022-03-27 : 引导模式主函数 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : *新增返回上级菜单操作，输入y回到上级菜单
#              by Chang Chuntao  -> Version : 1.10
# 2022-04-22 : 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF3、 GRID_5x5_VMF3
#              by Chang Chuntao  -> Version : 1.11
def CDD_Mode():
    print("==================================================================================")
    print("      FAST           : Fusion Abundant multi-Source data download Terminal")
    print("      Author         : Chang Chuntao")
    print("      Copyright(C)   : The GNSS Center, Wuhan University & ")
    print("                       Chinese Academy of Surveying and mapping")
    print("      Contact        : QQ@1252443496 & WECHAT@amst-jazz GITHUB@ChangChuntao")
    print("      Git            : https://github.com/ChangChuntao/FAST.git")
    print("      Version        : 1.12 # 2022-04-30")
    obj = top_cdd()  # 一级目录 obj：一级索引
    subnum = sub_cdd(obj)  # 二级目录 subnum：二级索引 返回y为返回上级一级菜单，或返回二级菜单
    while True:
        if subnum == "y":
            obj = top_cdd()  # 一级目录 obj：一级索引
            subnum = sub_cdd(obj)  # 二级目录 subnum：二级索引
        else:
            if subnum != 0:
                cddarg = {'datatype': gnss_type[obj - 1][1][subnum - 1]}  # 索引数据类型
                PrintGDD("数据类型为" + cddarg['datatype'], "normal")
                break
            else:
                return 0

    back_sub = geturl_download_uncompress(cddarg, obj)  # 返回y为返回上级二级菜单，或返回n并进行下载
    while True:
        if back_sub == "y":
            subnum = sub_cdd(obj)  # 二级目录 subnum：二级索引
            while True:
                if subnum == "y":
                    obj = top_cdd()  # 一级目录 obj：一级索引
                    subnum = sub_cdd(obj)  # 二级目录 subnum：二级索引
                else:
                    cddarg = {'datatype': gnss_type[obj - 1][1][subnum - 1]}  # 索引数据类型
                    PrintGDD("数据类型为" + cddarg['datatype'], "normal")
                    break
            back_sub = geturl_download_uncompress(cddarg, obj)
        else:
            break
