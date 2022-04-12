#!/usr/bin/python3
# GNSS_TYPE      : ALL TYPE OF GNSS DATA
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.0
# Date           : 2022.04.12 - Version 1.1

# 2022-03-27 : 所有支持的数据类型 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#              by Chang Chuntao  -> Version : 1.10
gnss_type = [["BRDC", ["GPS_brdc", "MGEX_brdm"]],

             ["SP3", ["GPS_IGS_sp3", "GPS_IGR_sp3", "GPS_IGU_sp3", "GPS_GFZ_sp3", "GPS_GRG_sp3",
                      "MGEX_WUH_sp3", "MGEX_WUHU_sp3", "MGEX_GFZ_sp3", "MGEX_COD_sp3", "MGEX_SHA_sp3", "MGEX_GRG_sp3",
                      "GLO_IGL_sp3"]],

             ["RINEX", ["GPS_IGS_rnx", "MGEX_IGS_rnx", "GPS_USA_cors", "GPS_HK_cors", "GPS_EU_cors", "GPS_AU_cors"]],

             ["CLK", ["GPS_IGS_clk", "GPS_IGR_clk", "GPS_GFZ_clk", "GPS_GRG_clk", "GPS_IGS_clk_30s",
                      "MGEX_WUH_clk", "MGEX_COD_clk", "MGEX_GFZ_clk", "MGEX_GRG_clk", "WUH_PRIDE_clk"]],

             ["ERP", ["IGS_erp", "WUH_erp", "COD_erp", "GFZ_erp", "IGR_erp"]],

             ["BIA", ["MGEX_WHU_bia", "GPS_COD_bia", "MGEX_COD_bia", "MGEX_GFZ_bia"]],

             ["ION", ["IGS_ion", "WUH_ion", "COD_ion"]],

             ["SINEX", ["IGS_day_snx", "IGS_week_snx", "IVS_week_snx", "ILS_week_snx", "IDS_week_snx"]],

             ["CNES_AR", ["CNES_post", "CNES_realtime"]],

             ["ATX", ["MGEX_IGS_atx"]],

             ["DCB", ["GPS_COD_dcb", "MGEX_CAS_dcb", "MGEX_WHU_OSB", "P1C1", "P1P2", "P2C2"]],

             ["Time_Series", ["IGS14_TS_ENU", "IGS14_TS_XYZ", "Series_TS_Plot"]],

             ["Velocity_Fields", ["IGS14_Venu", "IGS08_Venu", "PLATE_Venu"]],

             ["SLR", ["HY_SLR", "GRACE_SLR", "BEIDOU_SLR"]],

             ["OBX", ["GPS_COD_obx", "GPS_GRG_obx", "MGEX_WUH_obx", "MGEX_COD_obx", "MGEX_GFZ_obx"]]]


# 2022-03-27 : 每个二级目录的个数 by Chang Chuntao -> Version : 1.00
objnum = []
for sub_type in gnss_type:
    objnum.append(len(sub_type[1]))

# 2022-03-27 : 输入为年， 起始年积日， 终止年积日 的数据类型 by Chang Chuntao -> Version : 1.00
objneedydqd2 = [1, 2, 4, 5, 6, 7, 8, 9, 11, 14, 15]

# 2022-03-27 : 输入为年， 起始年积日， 终止年积日, 站点文件 的数据类型 by Chang Chuntao -> Version : 1.00
objneedyd1d2loc = [3, 12]

# 2022-03-27 : 无需输入 的数据类型 by Chang Chuntao -> Version : 1.00
objneedn = [10, 13]


# 2022-03-27 : 判断数据类型是否支持 by Chang Chuntao -> Version : 1.00
def isinGNSStype(datatype):
    for gt in gnss_type:
        if datatype in gt[1]:
            return True
        else:
            continue
    return False


# 2022-03-27 : 获取数据类型在gnss_type中的索引位置 by Chang Chuntao -> Version : 1.00
def getobj(datatype):
    d1 = 0
    for gt in gnss_type:
        d2 = 0
        for dt in gt[1]:
            d2 += 0
            if datatype == dt:
                return d1, d2
        d1 += 1