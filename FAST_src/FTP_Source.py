#!/usr/bin/python3
# FTP_source     : FTP source of each gnss center
# Author         : Chang Chuntao, CAO Duoming, Li Yongxi
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.21
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.09.16 - Version 1.21


# 2022-03-27 : 板块列表 by Chang Chuntao -> Version : 1.00
plate = ["AF", "AN", "AR", "AU", "BU", "CA", "CO", "EU", "IN", "MA", "NA", "NB", "NZ", "OK", "ON", "PA", "PM", "PS",
         "SA", "SB", "SC", "SL", "SO", "SU", "WL"]
plate_env = []
for p in plate:
    plate_env.append("http://geodesy.unr.edu/velocities/midas." + p + ".txt")

# 2022-03-27 : * 资源列表 by Chang Chuntao -> Version : 1.00
# 2022-04-12 : + 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
#              by Chang Chuntao  -> Version : 1.10
# 2022-04-22 : + 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
#              by Chang Chuntao  -> Version : 1.11
# 2022-04-30 : > 修正GPS_USA_cors节点
#              by Chang Chuntao  -> Version : 1.12
# 2022-05-24 : + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
#              CARG_ion、ESAG_ion、ESRG_ion
#              > 修正MGEX_GFZ_clk节点内 05M -> 30S
#              > 修正MGEX_brdm节点内 BRDM00DLR_S_ -> BRDC00IGS_R_，但保留BRDM00DLR_S_
#              by Chang Chuntao  -> Version : 1.13
# 2022-05-31 : + 新增BIA内资源MGEX_WHU_OSB_bia
#              > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
#              by Chang Chuntao  -> Version : 1.14
# 2022-07-03 : + 新增CLK内资源MGEX_WUHU_clk
#              + 新增ERP内资源WUHU_erp
#              + 新增OBX内资源MGEX_WUHU_obx
#              by Chang Chuntao  -> Version : 1.15
# 2022-07-13 : + 新增SpaceData内资源SW&EOP
#              by Chang Chuntao  -> Version : 1.16
# 2022-07-22 : + 新增SP3内资源MGEX_WUH_Hour_sp3
#              + 新增CLK内资源MGEX_WUH_Hour_clk
#              + 新增ERP内资源WUH_Hour_erp
#              by Chang Chuntao  -> Version : 1.17
# 2022-07-27 : > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
#              > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
#              > 修正MGEX_COD_clk资源
#              by Chang Chuntao  -> Version : 1.18
# 2022-09-16 : > 修正<SITE> <SITE_LONG>
#              + 新增MGEX_HK_cors资源
#              by Chang Chuntao  -> Version : 1.21


FTP_S = {"GPS_brdc": ["ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz"],

         "MGEX_brdm": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDC00IGS_R_<YEAR><DOY>0000_01D_MN.rnx.gz",
                       "--ftp-user anonymous --ftp-password cctcasm@163.com "
                       "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDC00IGS_R_<YEAR><DOY>0000_01D_MN.rnx.gz",
                       "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDM00DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz",
                       "--ftp-user anonymous --ftp-password cctcasm@163.com "
                       "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDM00DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz"],

         "GPS_IGS_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.sp3.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igs<GPSWD>.sp3.Z"],

         "GPS_IGR_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igr<GPSWD>.sp3.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igr<GPSWD>.sp3.Z",
                         "--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/igr<GPSWD>.sp3.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/igr<GPSWD>.sp3.Z"],

         "GPS_IGU_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_00.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_06.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_12.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_18.sp3.Z"],

         "GPS_GFZ_sp3": ["ftp://ftp.gfz-potsdam.de//pub/GNSS/products/final/w<GPSW>/gfz<GPSWD>.sp3.Z",
                         "ftp://igs.ign.fr/pub/igs/products/<GPSW>/gfz<GPSWD>.sp3.Z",
                         "--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/gfz<GPSWD>.sp3.Z"],

         "GPS_GRG_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "ftp://igs.ign.fr/pub/igs/products/<GPSW>/gfz<GPSWD>.sp3.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/grg<GPSWD>.sp3.Z"],

         "MGEX_WUH_sp3": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

         "MGEX_WUHU_sp3": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0100_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0200_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0300_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0400_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0500_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0600_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0700_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0800_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0900_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1000_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1100_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1200_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1300_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1400_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1500_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1600_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1800_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1900_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2000_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2100_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2200_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2300_01D_05M_ORB.SP3.gz"
         ],

         "MGEX_GFZR_sp3": ["ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/"
                           "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                           "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/"
                           "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"
                           ],

         "MGEX_COD_sp3": ["ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY"
                          ">0000_01D_05M_ORB.SP3.gz"],

         "MGEX_SHA_sp3": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/sha<GPSWD>.sp3.Z",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY"
                          ">0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/sha<GPSWD>.sp3.Z"],

         "MGEX_GRG_sp3": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY"
                          ">0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

         "GLO_IGL_sp3": ["ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igl<GPSWD>.sp3.Z"],

         "MGEX_WUH_Hour_sp3": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_00.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_01.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_02.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_03.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_04.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_05.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_06.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_07.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_08.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_09.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_10.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_11.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_12.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_13.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_14.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_15.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_16.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_17.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_18.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_19.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_20.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_21.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_22.sp3.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_23.sp3.Z"
         ],

         "GPS_IGS_rnx": ["ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/<SITE><DOY>0.<YY>d.Z",
                         "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/<SITE><DOY>0.<YY>d.gz",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                         "<SITE><DOY>0.<YY>d.gz",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                         "<SITE><DOY>0.<YY>d.Z",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>o/"
                         "<SITE><DOY>0.<YY>o.gz",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>o/"
                         "<SITE><DOY>0.<YY>o.Z"],

         "MGEX_IGS_rnx": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz"],

         "GPS_USA_cors": ["https://geodesy.noaa.gov/corsdata/rinex/<YYYY>/<DOY>/<SITE>/<SITE><DOY>0.<YY>d.gz",
                          "--http-user=anonymous --http-passwd=1252443496@qq.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.Z",
                          "--http-user=anonymous --http-passwd=1252443496@qq.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.gz"],

         "GPS_HK_cors": ["ftp://ftp.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/30s/<SITE><DOY>0.<YY>d.gz",
                         "ftp://ftp.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/30s/<SITE><DOY>0.<YY>o.gz"],

         "MGEX_HK_cors": [
             "ftp://ftp.geodetic.gov.hk/rinex3/<YYYY>/<DOY>/<SITE>/30s/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz"],

         "GPS_EU_cors": ["ftp://igs.bkg.bund.de/EUREF/obs/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.Z"],

         "GPS_AU_cors": ["ftp://ftp.ga.gov.au/geodesy-outgoing/gnss/data/daily/<YYYY>/<YY><DOY>/<SITE><DOY>0.<YY>d.Z"],

         "GPS_IGS_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.clk.Z"],

         "GPS_IGR_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igr<GPSWD>.clk.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igr<GPSWD>.clk.Z",
                         "--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/igr<GPSWD>.clk.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/igr<GPSWD>.clk.Z"],

         "GPS_GFZ_clk": ["ftp://ftp.gfz-potsdam.de//pub/GNSS/products/final/w<GPSW>/gfz<GPSWD>.clk.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/gbm<GPSWD>.clk.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/gfz<GPSWD>.clk.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/gbm<GPSWD>.clk.Z"],

         "GPS_GRG_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/grg<GPSWD>.clk.Z"],

         "GPS_IGS_clk_30s": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.clk_30s.Z"],

         "MGEX_WUH_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "MGEX_COD_clk": ["ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                          "COD0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/"
                          "COD0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "MGEX_GFZR_clk": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "MGEX_GRG_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/grg<GPSWD>.clk.Z",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                          "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/grg<GPSWD>.clk.Z"],

         "WUH_PRIDE_clk": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/clock/"
                           "WUM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "MGEX_WUHU_clk": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0100_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0200_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0300_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0400_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0500_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0600_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0700_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0800_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0900_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1000_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1100_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1200_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1300_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1400_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1500_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1600_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1800_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1900_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2000_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2100_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2200_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2300_01D_05M_CLK.CLK.gz"
         ],

         "MGEX_WUH_Hour_clk": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_00.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_01.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_02.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_03.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_04.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_05.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_06.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_07.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_08.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_09.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_10.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_11.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_12.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_13.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_14.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_15.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_16.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_17.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_18.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_19.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_20.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_21.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_22.clk.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_23.clk.Z"
         ],

         "IGS_erp": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSW>7.erp.Z"],

         "WUH_erp": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
                     "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.Z",
                     "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/wum<GPSWD>.erp.Z"],

         "COD_erp": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.ERP_M.Z"],

         "GFZ_erp": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz"],

         "IGR_erp": ["--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                     "http://garner.ucsd.edu/pub/products/<GPSW>/igr<GPSWD>.erp.Z"],

         "WUHU_erp": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0100_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0200_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0300_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0400_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0500_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0600_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0700_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0800_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0900_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1000_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1100_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1200_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1300_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1400_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1500_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1600_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1800_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1900_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2000_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2100_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2200_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2300_01D_01D_ERP.ERP.gz"
         ],

         "WUH_Hour_erp": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_00.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_01.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_02.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_03.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_04.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_05.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_06.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_07.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_08.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_09.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_10.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_11.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_12.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_13.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_14.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_15.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_16.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_17.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_18.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_19.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_20.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_21.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_22.erp.Z",
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_23.erp.Z"
         ],

         "MGEX_WUHN_IGMAS_bia": ["--ftp-user casm_cct --ftp-password wangji531! "
                                 "http://igmas.users.sgg.whu.edu.cn/products/download/directory/products/osb/"
                                 "<GPSW>/SGG<GPSWD>.BIA.tar.gz"],

         "MGEX_WHU_ABS_bia": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/bias/"
                              "WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_ABS.BIA.gz"],

         "MGEX_WHU_OSB_bia": ["ftp://igs.gnsswhu.cn/pub/whu/MGEX/DCB/<YYYY>"
                              "/WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "GPS_COD_bia": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/COD<GPSWD>.BIA.Z",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.bia.Z"],

         "MGEX_COD_bia": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.BIA_M.Z"],

         "MGEX_GFZ_bia": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "IGSG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z"],

         "IGRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z"],

         "WUHG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z"],

         "WURG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z"],

         "CODG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z"],

         "CORG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z"],

         "UQRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z"],

         "UPRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z"],

         "JPLG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z"],

         "JPRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z"],

         "CASG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/casg<DOY>0.<YY>i.Z"],

         "CARG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/carg<DOY>0.<YY>i.Z"],

         "ESAG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z"],

         "ESRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password cctcasm@163.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z"],

         "IGS_day_snx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z"],

         "IGS_week_snx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSW>.snx.Z",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/igs<YY>P<GPSW>.snx.Z"],

         "IVS_week_snx": ['-d -e "set ftp:ssl-force true" -e "mget /pub/vlbi/ivsproducts/daily_sinex/ivs2020a/'
                          '<YY><MMM>*;exit" ivs.bkg.bund.de'],

         "ILS_week_snx": ["ftp://edc.dgfi.tum.de/pub/slr/products/pos+eop/<YYYY>/<YY><MONTH><DAY>/"
                          "ilrsb.pos+eop.<YY><MONTH><DAY>.v170.snx.gz",
                          "ftp://edc.dgfi.tum.de/pub/slr/products/pos+eop/<YYYY>/<YY><MONTH><DAY>/"
                          "ilrsb.pos+eop.<YY><MONTH><DAY>.v135.snx.gz"],

         "IDS_week_snx": [
             # "ftp://doris.ensg.eu/pub/doris/products/sinex_series/idswd/ids<YY><DOY>wd12.snx.Z",
             # "ftp://doris.ensg.eu/pub/doris/products/sinex_series/idswd/ids<YY><DOY>wd14.snx.Z",
             "--ftp-user anonymous --ftp-password cctcasm@163.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/doris/products/sinex_series/idswd/ids<YY><DOY>wd12.snx.Z",
             "--ftp-user anonymous --ftp-password cctcasm@163.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/doris/products/sinex_series/idswd/ids<YY><DOY>wd14.snx.Z"],

         "CNES_post": ["http://www.ppp-wizard.net/products/POST_PROCESSED/post_<YYYY><DOY>.tgz"],

         "CNES_realtime": ["http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.bia.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.clk.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.sp3.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.obx.gz"],

         "MGEX_WUH_IGMAS_upd": [
             "http://igmas.users.sgg.whu.edu.cn/products/download/directory/products/upd/<YYYY>/<DOY>"
             "/upd_ewl_<YYYY><DOY>_GEC",
             "http://igmas.users.sgg.whu.edu.cn/products/download/directory/products/upd/<YYYY>/<DOY>"
             "/upd_nl_<YYYY><DOY>_GEC",
             "http://igmas.users.sgg.whu.edu.cn/products/download/directory/products/upd/<YYYY>/<DOY>"
             "/upd_wl_<YYYY><DOY>_GEC"],

         "MGEX_IGS_atx": ["http://files.igs.org/pub/station/general/igs14.atx"],

         "GPS_COD_dcb": ["ftp://ftp.aiub.unibe.ch/CODE_MGEX/CODE/<YYYY>/COM<GPSWD>.DCB.Z"],

         "MGEX_CAS_dcb": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/gps/products/mgex/dcb/<YYYY>/"
                          "CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_DCB.BSX.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/dcb/<YYYY>/"
                          "CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_DCB.BSX.gz"],

         "MGEX_WHU_OSB": ["ftp://igs.gnsswhu.cn/pub/whu/MGEX/DCB/<YYYY>/WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "P1C1": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/P1C1<YY><MM>.DCB.Z",
                  "ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/P1C1<YY><MM>_RINEX.DCB.Z"],

         "P1P2": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/P1P2<YY><MM>.DCB.Z",
                  "ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/P1P2<YY><MM>_ALL.DCB.Z"],

         "P2C2": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/P2C2<YY><MM>_RINEX.DCB.Z"],

         "IGS14_TS_ENU": ["http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/<SITE>.tenv3"],

         "IGS14_TS_XYZ": ["http://geodesy.unr.edu/gps_timeseries/txyz/IGS14/<SITE>.txyz2"],

         "Series_TS_Plot": ["http://geodesy.unr.edu/tsplots/IGS14/IGS14/TimeSeries/<SITE>.png"],

         "IGS14_Venu": ["http://geodesy.unr.edu/velocities/midas.IGS14.txt"],

         "IGS08_Venu": ["http://geodesy.unr.edu/velocities/midas.IGS08.txt"],

         "PLATE_Venu": plate_env,

         "HY_SLR": ["ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2a/<YYYY>/hy2a_<YYYY><MONTH>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2b/<YYYY>/hy2b_<YYYY><MONTH>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2c/<YYYY>/hy2c_<YYYY><MONTH>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2d/<YYYY>/hy2d_<YYYY><MONTH>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2a/<YYYY>/hy2a_<YYYY><MONTH><DAY>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2b/<YYYY>/hy2b_<YYYY><MONTH><DAY>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2c/<YYYY>/hy2c_<YYYY><MONTH><DAY>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2d/<YYYY>/hy2d_<YYYY><MONTH><DAY>.npt"],

         "GRACE_SLR": ["ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracea/<YYYY>/gracea_<YYYY><MONTH>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracea/<YYYY>/gracea_<YYYY><MONTH><DAY>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/graceb/<YYYY>/graceb_<YYYY><MONTH>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/graceb/<YYYY>/graceb_<YYYY><MONTH><DAY>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracefo1/<YYYY>/gracefo1_<YYYY><MONTH>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracefo1/<YYYY>/gracefo1_<YYYY><MONTH><DAY>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracefo2/<YYYY>/gracefo2_<YYYY><MONTH>.npt",
                       "ftp://edc.dgfi.tum.de/slr/data/npt_crd/gracefo2/<YYYY>/gracefo2_<YYYY><MONTH><DAY>.npt"],

         "BEIDOU_SLR": ["ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m1/<YYYY>/beidou3m1_<YYYY><MONTH>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m1/<YYYY>/beidou3m1_<YYYY><MONTH><DAY>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m10/<YYYY>/beidou3m10_<YYYY><MONTH>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m10/<YYYY>/beidou3m10_<YYYY><MONTH><DAY>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m2/<YYYY>/beidou3m2_<YYYY><MONTH>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m2/<YYYY>/beidou3m2_<YYYY><MONTH><DAY>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m3/<YYYY>/beidou3m3_<YYYY><MONTH>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m3/<YYYY>/beidou3m3_<YYYY><MONTH><DAY>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m9/<YYYY>/beidou3m9_<YYYY><MONTH>.npt",
                        "ftp://edc.dgfi.tum.de/slr/data/npt_crd/beidou3m9/<YYYY>/beidou3m9_<YYYY><MONTH><DAY>.npt"],

         "GPS_COD_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.obx.Z"],

         "GPS_GRG_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "MGEX_WUH_obx": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "MGEX_COD_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_15M_ATT.OBX.gz"],

         "MGEX_GFZ_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "MGEX_WUHU_obx": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0000_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0100_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0200_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0300_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0400_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0500_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0600_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0700_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0800_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>0900_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1000_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1100_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1200_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1300_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1400_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1500_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1600_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1800_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>1900_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2000_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2100_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2200_01D_05M_ATT.OBX.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY>2300_01D_05M_ATT.OBX.gz"
         ],

         "IGS_zpd": ["ftp://igs.gnsswhu.cn/pub/gps/products/troposphere/new/<YYYY>/<DOY>/<SITE><DOY>0.<YY>zpd.gz",
                     "--ftp-user anonymous --ftp-password cctcasm@163.com "
                     "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/troposphere/zpd/<YYYY>/<DOY>/<SITE><DOY>0.<YY>zpd.gz"],

         "COD_tro": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/cod<GPSWD>.tro.Z",
                     "--ftp-user anonymous --ftp-password cctcasm@163.com "
                     "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/cod<GPSWD>.tro.Z"],

         "JPL_tro": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/jpl<GPSWD>.tro.Z",
                     "--ftp-user anonymous --ftp-password cctcasm@163.com "
                     "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/jpl<GPSWD>.tro.Z"],

         "GRID_1x1_VMF3": [
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H00",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H06",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H12",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/1x1/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H18"],

         "GRID_2.5x2_VMF1": [
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/<YYYY>/VMFG_<YYYY><MONTH><DAY>.H00",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/<YYYY>/VMFG_<YYYY><MONTH><DAY>.H06",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/<YYYY>/VMFG_<YYYY><MONTH><DAY>.H12",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/<YYYY>/VMFG_<YYYY><MONTH><DAY>.H18"],

         "GRID_5x5_VMF3": [
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/5x5/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H00",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/5x5/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H06",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/5x5/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H12",
             "https://vmf.geo.tuwien.ac.at/trop_products/GRID/5x5/VMF3/VMF3_OP/<YYYY>/VMF3_<YYYY><MONTH><DAY>.H18"],

         "SW_EOP": ["http://celestrak.com//SpaceData/SW-All.txt",
                    "http://celestrak.com//SpaceData/EOP-All.txt"]
         }
