# gnssbox        : The most complete GNSS Python toolkit ever
# mgexSite       : mgex site information
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.05
# Latest Version : 2022.06.05
# url            : https://files.igs.org/pub/station/general/IGSNetwork.csv

def readMegxSiteInf(mgexInfoFile):
    mgexInfoFileData = open(mgexInfoFile, 'r+').readlines()
    mgexSiteInfo = {}
    for line in mgexInfoFileData[1:]:
        siteNameLong = line.split(',')[0]
        siteNameShort = siteNameLong.lower()[:4]
        siteX = float(line.split(',')[1])
        siteY = float(line.split(',')[2])
        siteZ = float(line.split(',')[3])
        siteB = float(line.split(',')[4])
        siteL = float(line.split(',')[5])
        siteH = line.split(',')[6]
        Receiver = line.split(',')[7]
        satSystem = line.split(',')[8].split('+')
        antenna = line.split(',')[13]
        mgexSiteInfo[siteNameShort] = {'LongName': siteNameLong, 'X': siteX, 'Y': siteY, 'Z': siteZ, 'B': siteB, 'L': siteL,
                                    'H': siteH, 'Rec': Receiver, 'System': satSystem, 'Ant': antenna}
    return mgexSiteInfo


