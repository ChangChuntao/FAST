# gnssbox        : The most complete GNSS Python toolkit ever
# mgexSite       : mgex site information
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : AIR, Chinese Academy of Sciences
# Creation Date  : 2022.06.05
# Latest Version : 3.01.01
# Date           : 2026.08.03 - Version 3.01.01
# url            : https://files.igs.org/pub/station/general/IGSNetworkWithFormer.json
#                   旧版: https://files.igs.org/pub/station/general/IGSNetwork.csv

def readMegxSiteInf(mgexInfoFile):
    """
    Reads the MGEX site information from a file and parses it into a dictionary format.
    支持新的IGS JSON格式(IGSNetworkWithFormer.json)与旧版CSV格式(IGSNetwork.csv), 按文件扩展名自动识别

    Parameters:
        mgexInfoFile : The path to the MGEX site information file.

    Returns:
        mgexSiteInfo: A dictionary containing the MGEX site information, with site short names as keys and detailed information as values.

    2026.08.03 : 支持IGS新JSON格式站点信息文件
                    by ChangChuntao
    """
    if str(mgexInfoFile).lower().endswith('.json'):
        return readMegxSiteInfJson(mgexInfoFile)
    # ---- 旧版CSV格式(IGSNetwork.csv) ----
    mgexInfoFileData = open(mgexInfoFile, 'r').readlines()
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

def readMegxSiteInfJson(mgexInfoFile):
    """
    读取IGS官方新JSON格式站点信息文件(IGSNetworkWithFormer.json):
        顶层为字典, 键为9位长站名, 值为站点信息
    返回结构与readMegxSiteInf一致:
        {短站名(4位小写): {'LongName','X','Y','Z','B','L','H','Rec','System','Ant'}}
        by ChangChuntao -> 2026.08.03
    """
    import json
    with open(mgexInfoFile, 'r', encoding='utf-8') as mgexInfoFileOpen:
        mgexSiteData = json.load(mgexInfoFileOpen)
    mgexSiteInfo = {}
    for siteNameLong, siteInf in mgexSiteData.items():
        siteNameShort = siteNameLong.lower()[:4]
        receiver = siteInf.get('Receiver', {}) or {}
        antenna = siteInf.get('Antenna', {}) or {}
        siteLat = siteInf.get('Latitude')
        siteLon = siteInf.get('Longitude')
        mgexSiteInfo[siteNameShort] = {
            'LongName': siteNameLong,
            'X': siteInf.get('X'), 'Y': siteInf.get('Y'), 'Z': siteInf.get('Z'),
            'B': float(siteLat) if siteLat is not None else None,
            'L': float(siteLon) if siteLon is not None else None,
            'H': siteInf.get('Height'),
            'Rec': receiver.get('Name'),
            'System': [x for x in str(receiver.get('SatelliteSystem') or '').split('+') if x],
            'Ant': antenna.get('Name'),
        }
    return mgexSiteInfo


