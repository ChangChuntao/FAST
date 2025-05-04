#!/usr/bin/python3
# gnssbox        : The most complete GNSS Python toolkit ever
# readsiteinfo   : Read a simple site information file
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.03
# Latest Version : 2022.06.03


def readSiteInf(sitefile):
    # 简易站点信息文件，文件格式：
    # | L1 B1 SITE_NAME1 |
    # | L2 B2 SITE_NAME2 |
    # | ................ |
    # | LN BN SITE_NAMEN |
    try:
        sitefile_line = open(sitefile, 'r+').readlines()
        siteinfo = {}
        for line in sitefile_line:
            if len(line) > 1:
                siteinfo[line.split()[2]] = {'L': float(line.split()[0]), 'B': float(line.split()[1])}
        return siteinfo
    except:
        return {}
    

def readIgsSiteList(sitefile, megxSiteList):
    import os
    try:
        chooseSiteList = {}
        if os.path.isfile(sitefile):
            fileLine = open(sitefile, "r").readlines()
            for line in fileLine:
                lineSplit = line.split()
                for siteInLine in lineSplit:
                    siteLower = siteInLine[:4].lower()
                    if siteLower in megxSiteList:
                        chooseSiteList[siteLower] = megxSiteList[siteLower]
        return chooseSiteList
    except:
        return {}
    



