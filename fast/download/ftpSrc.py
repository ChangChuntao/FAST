#!/usr/bin/python3
# -*- coding: utf-8 -*-
# FTP_source     : FTP source of each gnss center
# Author         : Chang Chuntao, CAO Duoming, Li Yongxi
# Copyright(C)   : The GNSS Center, Wuhan University
# Latest Version : 2.11
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-09-20 - Version 2.11
import datetime

# nowTime = datetime.datetime.utcnow()
# year = str(nowTime.year)

# 2022-03-27 : 板块列表 by Chang Chuntao -> Version : 1.00
plate = ["AF", "AN", "AR", "AU", "BU", "CA", "CO", "EU", "IN", "MA", "NA", "NB", "NZ", "OK", "ON", "PA", "PM", "PS",
         "SA", "SB", "SC", "SL", "SO", "SU", "WL"]
plate_env = []
for p in plate:
    plate_env.append("http://geodesy.unr.edu/velocities/midas." + p + ".txt")

'''
    2022-03-27 :    * 资源列表 by Chang Chuntao -> Version : 1.00
    2022-04-12 :    + 新增P1C1、P1P2、P2C2、GRACE_SLR、BEIDOU_SLR、MGEX_WHU_OSB、GLO_IGL_sp3、GPS_IGS_clk_30s资源
                    by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    + 新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-04-30 :    > 修正GPS_USA_cors节点
                    by Chang Chuntao  -> Version : 1.12
    2022-05-24 :    + 新增ION内资源WURG_ion、CODG_ion、CORG_ion、UQRG_ion、UPRG_ion、JPLG_ion、JPRG_ion、CASG_ion、
                    CARG_ion、ESAG_ion、ESRG_ion
                    > 修正MGEX_GFZ_clk节点内 05M -> 30S
                    > 修正MGEX_brdm节点内 BRDM00DLR_S_ -> BRDC00IGS_R_，但保留BRDM00DLR_S_
                    by Chang Chuntao  -> Version : 1.13
    2022-05-31 :    + 新增BIA内资源MGEX_WHU_OSB_bia
                    > 修正BIA内资源MGEX_WHU_bia -> MGEX_WHU_ABS_bia
                    by Chang Chuntao  -> Version : 1.14
    2022-07-03 :    + 新增CLK内资源MGEX_WUHU_clk
                    + 新增ERP内资源WUHU_erp
                    + 新增OBX内资源MGEX_WUHU_obx
                    by Chang Chuntao  -> Version : 1.15
    2022-07-13 :    + 新增SpaceData内资源SW&EOP
                    by Chang Chuntao  -> Version : 1.16
    2022-07-22 :    + 新增SP3内资源MGEX_WUH_Hour_sp3
                    + 新增CLK内资源MGEX_WUH_Hour_clk
                    + 新增ERP内资源WUH_Hour_erp
                    by Chang Chuntao  -> Version : 1.17
    2022-07-27 :    > 修正MGEX_GFZ_sp3 -> MGEX_GFZR_sp3
                    > 修正MGEX_GFZ_clk -> MGEX_GFZR_clk
                    > 修正MGEX_COD_clk资源
                    by Chang Chuntao  -> Version : 1.18
    2022-09-16 :    > 修正<SITE> <SITE_LONG>
                    + 新增MGEX_HK_cors资源
                    by Chang Chuntao  -> Version : 1.21
    2022-09-28 :    + 新增COSMIC一级类
                    + 新增COSMIC内资源'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx','C1_L1b_atmPhs', 'C1_L1b_gpsBit',
                    'C1_L1b_ionPhs', 'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec', 'C1_L1b_scnLv1', 'C2_L1a_leoAtt',
                    'C2_L1a_opnGps', 'C2_L1a_podCrx', 'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2'
                    by Chang Chuntao  -> Version : 1.23
    2022-10-10 :    + 新增Tables一级类
                    + 新增Tables内资源'Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM','Panda_oceanload',
                    'Panda_oceantide', 'Panda_utcdif','Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                    'Panda_ut1tid', 'Panda_leap_sec',
                    'Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno','Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                    'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod','Gamit_svnav', 'Gamit_rcvant'
                    by Chang Chuntao  -> Version : 1.24
    2022-11-02 :    > IVS_week_snx : 更换网站: ivs.bkg.bund.de -> ivsopar.obspm.fr
                    > IDS_week_snx : 更换策略: wd12/14         -> wd16/19
    2022-11-09 :    + 新增IGS_hfile
                    by Chang Chuntao  -> Version : 2.01
    2022-11-10 :    + 新增MGEX_WUHR_sp3 / MGEX_WUHR_clk
                    by Chang Chuntao  -> Version : 2.02
    2022-11-15 :    + 新增GRE_IGS_01S / GCRE_MGEX_01S
                    by Chang Chuntao  -> Version : 2.03
    2022-12-02 :    > MGEX_brdm -> MGEX_brdc
                    + MGEX_CNAV_brdm / MGEX_CNAV_brdm
                    > GPS_IGS_sp3 / GPS_IGS_clk : igs -> IGS0OPSFIN
                    > GPS_IGR_sp3 / GPS_IGR_clk : igr -> IGS0OPSRAP
                    > GPS_IGU_sp3               : igu -> IGS0OPSULT
                    by Chang Chuntao  -> Version : 2.04
    2022-12-04 :    > MGEX_WUH_sp3 -> MGEX_WHU_F_sp3 / MGEX_WUHR_sp3 -> MGEX_WHU_R_sp3 / MGEX_WUHU_sp3 -> MGEX_WHU_U_sp3
                    > MGEX_WUH_Hour_sp3 -> MGEX_WHU_Hour_sp3 / MGEX_SHA_sp3 -> MGEX_SHA_F_sp3 / MGEX_COD_sp3 -> MGEX_COD_F_sp3
                    > MGEX_GRG_sp3 -> MGEX_GRG_F_sp3 / MGEX_GFZR_sp3 -> MGEX_GFZ_R_sp3 / GRE_CODR_sp3 -> GRE_COD_R_sp3
                    > GLO_IGL_sp3 -> GLO_IGL_F_sp3
                    + MGEX_GFZ_F_sp3
                    > MGEX_WUH_clk -> MGEX_WHU_F_clk / MGEX_WUHR_clk -> MGEX_WHU_R_clk / MGEX_WUHU_clk -> MGEX_WHU_U_clk
                    > MGEX_WUH_Hour_clk -> MGEX_WHU_Hour_clk / MGEX_COD_clk -> MGEX_COD_F_clk / MGEX_GRG_clk -> MGEX_GRG_F_clk
                    > MGEX_GFZR_clk -> MGEX_GFZ_R_clk 
                    + MGEX_SHA_F_clk / MGEX_GFZ_F_clk / GRE_COD_R_clk / GLO_IGL_F_clk
                    > WUH_erp -> WHU_F_erp / WUHU_erp -> WHU_U_erp / GFZ_erp -> GFZ_F_erp / COD_erp -> COD_R_erp
                    > WUH_Hour_erp -> WHU_Hour_erp
                    > MGEX_COD_bia -> MGEX_COD_R_bia / MGEX_GFZ_bia -> MGEX_GFZ_R_bia / MGEX_WHU_ABS_bia -> MGEX_WHU_R_ABS_bia
                    > MGEX_WHU_OSB_bia -> MGEX_WHU_R_OSB_bia
                    x MGEX_WHU_OSB(与MGEX_WHU_R_OSB_bia重复)
                    > MGEX_CAS_dcb -> MGEX_CAS_R_dcb
                    > MGEX_WUH_obx -> MGEX_WHU_F_obx / MGEX_COD_obx -> MGEX_COD_F_obx / MGEX_GFZ_obx -> MGEX_GFZ_F_obx
                    > MGEX_WUHU_obx -> MGEX_WHU_U_obx
                    > WUHG_ion -> WHUG_ion
                    by Chang Chuntao  -> Version : 2.05
    2023-01-13 :    > MGEX_IGS_atx -> MGEX_IGS14_atx
                    + MGEX_IGS20_atx
                    x 删除GPS_GFZ_sp3 / GPS_GFZ_clk
                    > MGEX_GFZ_F_sp3 -> GRE_GFZ_F_sp3 / MGEX_GFZ_F_clk -> GRE_GFZ_F_clk
                    > IGS rename -> GPS_IGS_sp3 / GPS_IGR_sp3 / GPS_IGU_sp3 / GRE_COD_R_sp3 / GPS_IGS_clk
                    >               GPS_IGR_clk / GPS_IGS_clk_30s / GRE_COD_R_clk / IGS_erp
                    by Chang Chuntao  -> Version : 2.06
    2023-02-10 :    > GPS_EU_CORS -> MGEX_EU_cors
                    > MGEX_EU_cors / CODG_ion  add source
                    > IGS rename -> IGS_day_snx / IGS_week_snx
                    + COD_F_erp
                    + IGS_crd_snx / COD_sol_snx / ESA_sol_snx / GFZ_sol_snx / GRG_sol_snx / NGS_sol_snx / SIO_sol_snx
                    > MGEX_GFZ_F_obx -> MGEX_GFZ_R_obx
                    by Chang Chuntao  -> Version : 2.07
    2023-03-12 :    > 修复仅需站点模式,增加<SITE_SHORT>标识 # 2023-02-27
                    + COD_F_ion # 2023-02-27
                    > 调整优先级 ***
                    > COSMIC -> LEO
                    + LEO -> GRACE_dat / GRACE_rnxapp / GRACE_fo_dat / GRACE_fo1_sp3 / GRACE_fo1_sp3 
                    + LEO -> CHAMP_rnx / CHAMP_sp3 / SWARM_rnx / SWARM_sp3
                    > GFZ多系统数据地址更新(IGS20) -> MGEX_GFZ_R_sp3 / MGEX_GFZ_F_clk / GFZ_R_erp / MGEX_GFZ_R_bia
                    by Chang Chuntao  -> Version : 2.08
    2023-06-29 :    + Ultra Product add <HOUR> flag
                    + MGEX_GFZ_R_obx add WHU source
                    + MGEX_WHU_F_osb
                    > GRE_IGS_01S GCRE_MGEX_01S change source
                    > MGEX_WHU_U_clk rename source : WUM0MGXULT_ -> WUM0MGXULA_
                    > GPS_COD_bia -> GPS_COD_F_osb / MGEX_COD_F_bia -> MGEX_COD_F_osb / MGEX_COD_R_bia -> GRE_COD_R_osb
                    > MGEX_WHU_R_OSB_bia -> MGEX_WHU_R_osb / MGEX_WHU_R_ABS_bia -> MGEX_WHU_R_abs
                    > MGEX_GFZ_R_bia -> MGEX_GFZ_R_osb / ...
                    x COD_F_ion, 与CODG_ion重复
                    by Chang Chuntao  -> Version : 2.09
    2023-08-11 :    + MGEX_WHU_RTS_sp3 / MGEX_WHU_RTS_clk
                    + MGEX_IAC_F_sp3 / MGEX_IAC_F_clk / MGEX_CAS_R_osb
                    by Chang Chuntao  -> Version : 2.10
    2023-09-20 :    + GRE_JAX_U_sp3 / GRE_JAX_U_clk_30s
                    by Chang Chuntao  -> Version : 2.11
    2023-10-25 :    > MGEX -> GCRE
                    by Chang Chuntao  -> Version : 3.00
    2024-07-11 :    > IGS_zpd -> IGS_trop
                    > tro -> trop
                    > GCRE_WHU_U_sp3 : ULT -> NRT
                    by Chang Chuntao  -> Version : 3.00.02
'''

FTP_S = {"GPS_brdc": ["ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz",
                      "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz"],

         "GCRE_brdc": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDC00IGS_R_<YEAR><DOY>0000_01D_MN.rnx.gz",
                       "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                       "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YEAR>/<DOY>/<YY>p/"
                       "BRDC00IGS_R_<YEAR><DOY>0000_01D_MN.rnx.gz"],

         "GCRE_CNAV_brdm": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
                            "BRDM00DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YEAR>/<DOY>/<YY>p/"
                            "BRDM00DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz"],

         "GCRE_CNAV_brd4": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
                            "BRD400DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YEAR>/<DOY>/<YY>p/"
                            "BRD400DLR_S_<YEAR><DOY>0000_01D_MN.rnx.gz"],

         "GPS_IGS_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.sp3.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igs<GPSWD>.sp3.Z"],

         "GPS_IGR_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igr<GPSWD>.sp3.Z"],

         "GPS_IGU_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSULT_<YYYY><DOY>0000_02D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSULT_<YYYY><DOY>0600_02D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSULT_<YYYY><DOY>1200_02D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSULT_<YYYY><DOY>1800_02D_15M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_00.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_06.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_12.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igu<GPSWD>_18.sp3.Z"],

         "GPS_GRG_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GRG0OPSFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GRG0OPSFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/grg<GPSWD>.sp3.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/grg<GPSWD>.sp3.Z"],

         "GCRE_WHU_F_sp3": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "WUM0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                            "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "WUM0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                            "WUM0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

         "GCRE_WHU_R_sp3": [
             "ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/orbit/WUM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/orbit/WUM0MGXRAP_<YYYY><DOY>0000_01D_01M_ORB.SP3.gz"],

         "GCRE_WHU_U_sp3": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW_B>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_02D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_02D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULT_<YYYY><DOY><HOUR>00_01D_05M_ORB.SP3.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY><HOUR>00_01D_05M_ORB.SP3.gz",
         ],

         "GCRE_WHU_RTS_sp3": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/orbit/"
                              "WUM0MGXRTS_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"],

         "GRE_GFZ_F_sp3": [
             'ftp://ftp.gfz-potsdam.de/pub/GNSS/products/final/w<GPSW>/GFZ0OPSFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz',
             'ftp://ftp.gfz-potsdam.de/pub/GNSS/products/final/w<GPSW>/gfz<GPSWD>.sp3.Z'],

         "GCRE_GFZ_R_sp3": ["ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>_IGS20/"
                            "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                            "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/"
                            "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                            "ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgnss/<GPSW>_IGS20/"
                            "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                            "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/"
                            "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"
                            ],

         "GCRE_IAC_F_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IAC0MGXFIN_"
                            "<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"],

         "GCRE_COD_F_sp3": ["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/COD0MGXFIN_<YYYY><DOY"
                            ">0000_01D_05M_ORB.SP3.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY"
                            ">0000_01D_05M_ORB.SP3.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"
                            ],

         "GCRE_SHA_F_sp3": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/SHA0MGXRAP_<YYYY><DOY"
                            ">0000_01D_15M_ORB.SP3.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY"
                            ">0000_01D_15M_ORB.SP3.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

         "GCRE_GRG_F_sp3": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

         "GLO_IGL_F_sp3": ["ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igl<GPSWD>.sp3.Z"],

         "GCRE_WHU_H_sp3": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_<HOUR>.sp3.Z"
         ],

         'GRE_COD_R_sp3': ['http://ftp.aiub.unibe.ch/CODE/COD0OPSRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3',
                           'http://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.EPH_M.Z'],

         'GRE_JAX_U_sp3':['ftp://mgmds01.tksc.jaxa.jp/products/<GPSW>/jxu<GPSWD>_<HOUR>.sp3.Z'],

         'CEG_GRG_U_sp3':["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/GRG0OPSULT_<YYYY><DOY><HOUR>00_02D_05M_ORB.SP3.gz"],

         "GPS_IGS_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSFIN_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.clk.Z"],

         "GPS_IGR_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSRAP_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz",
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igr<GPSWD>.clk.Z"],

         "GPS_GRG_clk": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                         "http://garner.ucsd.edu/pub/products/<GPSW>/grg<GPSWD>.clk.Z",
                         "ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/<GPSW>/grg<GPSWD>.clk.Z"],

         "GPS_IGS_clk_30s": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSWD>.clk_30s.Z",
             "ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igs<GPSWD>.clk_30s.Z"],

         "GCRE_WHU_F_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                            "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "GCRE_WHU_R_clk": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/clock/"
                            "WUM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],
        
         "GCRE_WHU_U_clk": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW_B>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_02D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_02D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULT_<YYYY><DOY><HOUR>00_01D_05M_CLK.CLK.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY><HOUR>00_01D_05M_CLK.CLK.gz",
         ],

         "GCRE_WHU_U_clk_30s": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_02D_30S_CLK.CLK.gz",
         ],

        #  "GCRE_WHU_H_clk": [
        #      "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_<HOUR>.clk.Z"
        #  ],

         "GCRE_WHU_RTS_clk": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/clock/"
                              "WUM0MGXRTS_<YYYY><DOY>0000_01D_05S_CLK.CLK.gz"],

         "GCRE_SHA_F_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "SHA0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "GCRE_COD_F_clk": ["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/"
                            "COD0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/"
                            "COD0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                            "COD0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "GCRE_GRG_F_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                            "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/grg<GPSWD>.clk.Z",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                            "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                            "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/grg<GPSWD>.clk.Z"],

         "GCRE_GFZ_R_clk": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>_IGS20/GBM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "GCRE_IAC_F_clk": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IAC0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],


         "GRE_GFZ_F_clk": [
             'ftp://ftp.gfz-potsdam.de/pub/GNSS/products/final/w<GPSW>/GFZ0OPSFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz',
             'ftp://ftp.gfz-potsdam.de/pub/GNSS/products/final/w<GPSW>/gfz<GPSWD>.clk.Z'],

         'GRE_COD_R_clk': ['http://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.CLK_M.Z',
                           'http://ftp.aiub.unibe.ch/CODE/COD0OPSRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK'],

         "GLO_IGL_F_clk": ["ftp://nfs.kasi.re.kr/gps/products/<GPSW>/igl<GPSWD>.clk.Z"],

         "GRE_COD_F_clk_30s": ['http://ftp.aiub.unibe.ch/CODE/<YYYY>/COD0OPSFIN_<YYYY><DOY>0000_01D_05S_CLK.CLK.gz'],

         "GRE_JAX_U_clk_30s": ['ftp://mgmds01.tksc.jaxa.jp/products/<GPSW>/jxu<GPSWD>_<HOUR>.clk_30s.Z'],

         'CEG_GRG_U_clk':["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/GRG0OPSULT_<YYYY><DOY><HOUR>00_02D_05M_CLK.CLK.gz"],

         "GPS_IGS_obs": ["ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>o/<SITE><DOY>0.<YY>o.gz",
                         "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>o/<SITE><DOY>0.<YY>o.Z",
                         "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/<SITE><DOY>0.<YY>d.gz",
                         "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/<SITE><DOY>0.<YY>d.Z",
                         "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>o/"
                         "<SITE><DOY>0.<YY>o.gz",
                         "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>o/"
                         "<SITE><DOY>0.<YY>o.Z",
                         "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                         "<SITE><DOY>0.<YY>d.gz",
                         "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                         "<SITE><DOY>0.<YY>d.Z"],

         "GPS_USA_cors": ["https://geodesy.noaa.gov/corsdata/rinex/<YYYY>/<DOY>/<SITE>/<SITE><DOY>0.<YY>d.gz",
                          "--http-user=anonymous --http-passwd=fast@whu.wdu.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.Z",
                          "--http-user=anonymous --http-passwd=fast@whu.wdu.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.gz"],

         "GPS_HK_cors": [
                        "https://rinex.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/30s/<SITE><DOY>0.<YY>d.gz",
                        # "https://rinex.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/<SITE><DOY>0.<YY>n.gz",
                        # "https://rinex.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/<SITE><DOY>0.<YY>g.gz",
                        "https://rinex.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/30s/<SITE><DOY>0.<YY>o.gz"
                        ],

         "GCRE_AU_cors": ["https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                         "https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_30S_MO.crx.gz"
                         ],

         "GCRE_MGEX_obs": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                          "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                          "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_S_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                          "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz"],

         "GRE_IGS_01S": [
             "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a00.<YY>d.gz",
             "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a15.<YY>d.gz",
             "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a30.<YY>d.gz",
             "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a45.<YY>d.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a00.<YY>d.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a15.<YY>d.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a30.<YY>d.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE><DOY>a45.<YY>d.gz",
         ],

        "GPS_SIRGAS": ["https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/<YYYY>/<DOY>/<SITE><DOY>1.zip -O <SITE><DOY>_<YY>.zip"],

         "GCRE_MGEX_obs_01s": [
             
                          
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_01S_MO.crx.tar",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_01S_MO.crx.tar",
         
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",
            #  "ftp://igs.gnsswhu.cn/pub/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",

             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_01S_MO.crx.tar",
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_01S_MO.crx.tar",
             
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>00_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>15_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>30_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_R_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",
            #  "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<YY>d/<HOUR>/<SITE_LONG>_S_<YYYY><DOY><HOUR>45_15M_01S_MO.crx.gz",
         ],

         "GRE_MGEX_obs_01s": [
             "--ftp-user anonymous --ftp-password cctcasm@163.com ftps://gdc.cddis.eosdis.nasa.gov/gnss/data/highrate/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.tar"
         ],

         "GCRE_HK_cors": [
                        "https://rinex.geodetic.gov.hk/rinex3/<YYYY>/<DOY>/<SITE>/30s/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                        # "https://rinex.geodetic.gov.hk/rinex3//<YYYY>/<DOY>/<SITE>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_GN.rnx.gz",
                        # "https://rinex.geodetic.gov.hk/rinex3//<YYYY>/<DOY>/<SITE>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_RN.rnx.gz"
                        ],

         "GCRE_EU_cors": [
             "https://igs.bkg.bund.de/root_ftp/EUREF/obs/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/EUREF/obs/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/MGEX/obs/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/MGEX/obs/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/IGS/obs/<YYYY>/<DOY>/<SITE_LONG>_S_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/IGS/obs/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
             "https://igs.bkg.bund.de/root_ftp/GREF/obs/<YYYY>/<DOY>/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz"],
        
        "GCRE_SIRGAS": ["https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/<YYYY>/<DOY>/<SITE_SHORT>00BRA_R_<YYYY><DOY>0000_01D_15S_MO.crx.gz"],

         "IGS_F_erp": [
             'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSFIN_<YEAR><WEEK0DOY>0000_07D_01D_ERP.ERP.gz',
             "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<GPSW>7.erp.Z"],

         "WHU_F_erp": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.Z",
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/wum<GPSWD>.erp.Z"],

         "COD_R_erp": ["http://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.ERP_M.Z"],

         "COD_F_erp": ["ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_03D_12H_ERP.ERP.gz"],

         "GFZ_R_erp": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>_IGS20/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.Z"],

         "IGS_R_erp": ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/products/<GPSW>/igr<GPSWD>.erp.Z",
                       "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz"],

         "WHU_U_erp": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY><HOUR>00_01D_01D_ERP.ERP.gz",
         ],

         "WHU_H_erp": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/<GPSW>/hour<GPSWD>_<HOUR>.erp.Z"
         ],


         "GPS_COD_F_osb": ['ftp://igs.gnsswhu.cn/pub/gps/products/<YYYY>/COD0OPSFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz',
                           "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/COD0OPSFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz",
                           "http://ftp.aiub.unibe.ch/CODE/<YYYY>/COD<GPSWD>.BIA.Z",
                           "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.bia.Z"],

         "GE_GRG_F_osb": ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GRG0OPSFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz'],

         "GRE_COD_R_osb": [
             'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/COD0OPSRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz'],

         "GCRE_WHU_F_osb": [
             'ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz'],

         "GCRE_WHU_R_osb": [
             "ftp://igs.gnsswhu.cn/pub/whu/MGEX/DCB/<YYYY>/WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "GCRE_WHU_R_abs": [
             "ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/bias/WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_ABS.BIA.gz"],

         "GCRE_COD_F_osb": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz",
             "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "GCRE_GFZ_R_osb": [
             "ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgnss/<GPSW>_IGS20/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz",
             "ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "GCRE_CAS_R_osb": [
            #  "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz",
             "ftp://ftp.gipp.org.cn/product/dcb/mgex/<YEAR>/CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],
        
         "GCRE_WHU_U_osb": [
             'ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW_B>/WUM0MGXNRT_<YYYY_B><DOY_B><HOUR>00_01D_01D_OSB.BIA.gz'],


        "GCRE_WHU_RTS_osb":['ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/bias/WUM0MGXRTS_<YYYY><DOY>0000_01D_05M_OSB.BIA.gz'],

         "GPS_COD_dcb": ["http://ftp.aiub.unibe.ch/CODE_MGEX/CODE/<YYYY>/COM<GPSWD>.DCB.Z"],

         "GCRE_CAS_R_dcb": ["ftp://igs.ign.fr/pub/igs/products/mgex/dcb/<YYYY>/"
                            "CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_DCB.BSX.gz",
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/dcb/<YYYY>/"
                            "CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_DCB.BSX.gz"],

         "P1C1": ["http://ftp.aiub.unibe.ch/CODE/<YYYY>/P1C1<YY><MM>.DCB.Z",
                  "http://ftp.aiub.unibe.ch/CODE/<YYYY>/P1C1<YY><MM>_RINEX.DCB.Z"],

         "P1P2": ["http://ftp.aiub.unibe.ch/CODE/<YYYY>/P1P2<YY><MM>.DCB.Z",
                  "http://ftp.aiub.unibe.ch/CODE/<YYYY>/P1P2<YY><MM>_ALL.DCB.Z"],

         "P2C2": ["http://ftp.aiub.unibe.ch/CODE/<YYYY>/P2C2<YY><MM>_RINEX.DCB.Z"],

         "GPS_COD_F_obx": ["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/COD0OPSFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz",
                           "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.obx.Z"],

         "GPS_GRG_F_obx": ["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz",
                           "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                           "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz",
                           'ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz'],

         'GCRE_WHU_F_obx': [
             'ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz'],

         "GCRE_WHU_R_obx": [
             'ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YEAR>/orbit/WUM0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz'],

         "GCRE_WHU_U_obx": [
             "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXULA_<YYYY><DOY><HOUR>00_01D_05M_ATT.OBX.gz",
         ],

         "GCRE_COD_F_obx": ["--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz",
                            'ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz',
                            "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                            "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_15M_ATT.OBX.gz "],

         "GCRE_GFZ_R_obx": [
             'ftp://igs.gnsswhu.cn/pub/gps/products/mgex/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz',
             'ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz',
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "IGSG_ion": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/IGS0OPSFIN_<YYYY><DOY>0000_01D_02H_GIM.INX.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/ionex/<YYYY>/<DOY>/IGS0OPSFIN_<YYYY><DOY>0000_01D_02H_GIM.INX.gz",
             "ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z",
             "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/igsg<DOY>0.<YY>i.Z"],

         "IGRG_ion": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/IGS0OPSRAP_<YYYY><DOY>0000_01D_02H_GIM.INX.gz",
             "ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/ionex/<YYYY>/<DOY>/IGS0OPSRAP_<YYYY><DOY>0000_01D_02H_GIM.INX.gz",
             "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z",
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/igrg<DOY>0.<YY>i.Z"],

         "WHUG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z"],

         "WURG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/whrg<DOY>0.<YY>i.Z"],

         "CODG_ion": ['http://ftp.aiub.unibe.ch/CODE/<YYYY>/COD0OPSFIN_<YYYY><DOY>0000_01D_01H_GIM.ION.gz',
                      "ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                    #   "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                    #   "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                    #   "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                    #   "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/COD0OPSFIN_<YYYY><DOY>0000_01D_01H_GIM.ION.gz"],

         "CORG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/corg<DOY>0.<YY>i.Z"],

         "UQRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/uqrg<DOY>0.<YY>i.Z"],

         "UPRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/uprg<DOY>0.<YY>i.Z"],

         "JPLG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/jplg<DOY>0.<YY>i.Z"],

         "JPRG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                      "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z",
                      "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/jprg<DOY>0.<YY>i.Z"],

         "CASG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/casg<DOY>0.<YY>i.Z"],

         "CARG_ion": ["ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/carg<DOY>0.<YY>i.Z"],

         "ESAG_ion": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/ESA0OPSFIN_<YYYY><DOY>0000_01D_02H_GIM.ION.gz",
             "ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
             "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
             "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z",
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/esag<DOY>0.<YY>i.Z"],

         "ESRG_ion": [
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/ESA0OPSRAP_<YYYY><DOY>0000_01D_01H_GIM.ION.gz",
             "ftp://ftp.gipp.org.cn/product/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
             "ftp://gssc.esa.int/gnss/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
             "ftp://igs.ign.fr/pub/igs/products/ionosphere/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z",
             "ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/esrg<DOY>0.<YY>i.Z"],

         "IGS_day_snx": ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSSNX_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z",
                         "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z"],

         "IGS_week_snx": ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSSNX_<YYYY><DOY>0000_07D_07D_SOL.SNX.gz',
                          "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSW>.snx.Z",
                          "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/igs<YY>P<GPSW>.snx.Z"],

         "IVS_week_snx": [
             '-d -e "set ftp:ssl-force true" -e "mget /pub/vlbi/ivsproducts/daily_sinex/ivs2020a/'
             '<YY><MMM>*;exit" ivsopar.obspm.fr'
         ],

         "ILS_week_snx": [
             "ftp://edc.dgfi.tum.de/pub/slr/products/pos+eop/<YYYY>/<YY><MONTH><DAY>/"
             "ilrsb.pos+eop.<YY><MONTH><DAY>.v170.snx.gz",
             "ftp://edc.dgfi.tum.de/pub/slr/products/pos+eop/<YYYY>/<YY><MONTH><DAY>/"
             "ilrsb.pos+eop.<YY><MONTH><DAY>.v135.snx.gz"
         ],

         "IDS_week_snx": [
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/doris/products/sinex_series/idswd/ids<YY><DOY>wd16.snx.Z",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/doris/products/sinex_series/idswd/ids<YY><DOY>wd19.snx.Z",
         ],

         'IGS_crd_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/IGS0OPSSNX_<YYYY><DOY>0000_01D_01D_CRD.SNX.gz',
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSW>.ssc.Z"],

         'COD_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/COD0OPSFIN_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/cod<GPSWD>.snx.Z'],

         'ESA_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/ESA0OPSFIN_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/esa<GPSWD>.snx.Z'],

         'GFZ_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GFZ0OPSFIN_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/gfz<GPSWD>.snx.Z'],

         'GRG_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/GRG0OPSFIN_<YYYY><DOY>0000_01D_000_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/grg<GPSWD>.snx.Z'],

         'NGS_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/NGS0OPSFIN_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/ngs<GPSWD>.snx.Z'],

         'SIO_sol_snx': ['ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/SIO0OPSFIN_<YYYY><DOY>0000_01D_01D_SOL.SNX.gz',
                         'ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/sio<GPSWD>.snx.Z'],

         "CNES_post": ["http://www.ppp-wizard.net/products/POST_PROCESSED/post_<YYYY><DOY>.tgz"],

         "CNES_realtime": ["http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.bia.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.clk.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.sp3.gz",
                           "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.obx.gz"],
        
         "CNES_bia":        ["http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>.bia.gz"],

         "CNES_backup": ["http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>_backup.bia.gz",
                        "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>_backup.clk.gz",
                        "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>_backup.sp3.gz",
                        "http://www.ppp-wizard.net/products/REAL_TIME/cnt<GPSWD>_backup.obx.gz"],

         "MGEX_IGS14_atx": ["http://files.igs.org/pub/station/general/igs14.atx"],

         "MGEX_IGS20_atx": ["http://files.igs.org/pub/station/general/igs20.atx"],

         "IGS14_TS_ENU": ["http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/<SITE_SHORT>.tenv3"],

         "IGS14_TS_XYZ": ["http://geodesy.unr.edu/gps_timeseries/txyz/IGS14/<SITE_SHORT>.txyz2"],

         "Series_TS_Plot": ["http://geodesy.unr.edu/tsplots/IGS14/IGS14/TimeSeries/<SITE_SHORT>.png"],

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

         "IGS_trop": [
             'ftp://igs.gnsswhu.cn/pub/gps/products/troposphere/new/<YYYY>/<DOY>/IGS0OPSFIN_<YYYY><DOY>0000_01D_05M_<SITE_LONG>_TRO.TRO.gz',
             "ftp://igs.gnsswhu.cn/pub/gps/products/troposphere/new/<YYYY>/<DOY>/<SITE><DOY>0.<YY>zpd.gz",
             "--ftp-user anonymous --ftp-password fast@whu.edu.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/troposphere/zpd/<YYYY>/<DOY>/<SITE><DOY>0.<YY"
             ">zpd.gz"],

         "COD_trop": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/COD0OPSFIN_<YYYY><DOY>0000_01D_01H_TRO.TRO.gz",
                     "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/cod<GPSWD>.tro.Z",
                     "--ftp-user anonymous --ftp-password fast@whu.edu.com "
                     "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/<GPSW>/cod<GPSWD>.tro.Z"],

         "JPL_trop": ["ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/jpl<GPSWD>.tro.Z",
                     "--ftp-user anonymous --ftp-password fast@whu.edu.com "
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

        "vmf1grd": ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                    "http://garner.ucsd.edu/pub/gamit/tables/vmf1grd.<YEAR>"],

         "Meteorological": [
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_10S_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30S_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_05M_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_15M_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_30M_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE_LONG>_R_<YYYY><DOY>0000_01D_MM.rnx.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE><DOY>0.<YY>m.gz",
             "ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YYYY>/<DOY>/<YY>m/<SITE><DOY>0.<YY>m.Z",
             ],

         "SW_EOP": ["http://celestrak.com//SpaceData/SW-All.txt",
                    "http://celestrak.com//SpaceData/EOP-All.txt"],

         'GRACE_dat': [
             'ftp://isdcftp.gfz-potsdam.de/grace/Level-1B/JPL/INSTRUMENT/RL02/<YYYY>/grace_1B_<YYYY>-<MONTH>-<DAY>_02.tar.gz'],

         'GRACE_rnxapp': [
             'ftp://isdcftp.gfz-potsdam.de/grace/SOFTWARE/GraceReadSW_L1_2010-03-31.tar.gz'],

         'GRACE_fo_dat': [
             ' ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/INSTRUMENT/RL04/<YYYY>/gracefo_1B_<YYYY>-<MONTH>-<DAY>_RL04.ascii.noLRI.tgz'],

         'GRACE_fo1_sp3': [
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L64/RSO/<YYYY>/<DOY>/GFZOP_RSO_L64_G_<YYYY_B><MONTH_B><DAY_B>_220000_<YYYY><MONTH><DAY>_120000_v02.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L64/RSO/<YYYY>/<DOY>/GFZOP_RSO_L64_G_<YYYY><MONTH><DAY>_100000_<YYYY_F><MONTH_F><DAY_F>_000000_v02.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L64/RSO/<YYYY>/<DOY>/GFZOP_RSO_L64_G_<YYYY_B><MONTH_B><DAY_B>_220000_<YYYY><MONTH><DAY>_120000_v03.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L64/RSO/<YYYY>/<DOY>/GFZOP_RSO_L64_G_<YYYY><MONTH><DAY>_100000_<YYYY_F><MONTH_F><DAY_F>_000000_v03.sp3.gz',
             ],

         'GRACE_fo2_sp3': [
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L65/RSO/<YYYY>/<DOY>/GFZOP_RSO_L65_G_<YYYY_B><MONTH_B><DAY_B>_220000_<YYYY><MONTH><DAY>_120000_v02.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L65/RSO/<YYYY>/<DOY>/GFZOP_RSO_L65_G_<YYYY><MONTH><DAY>_100000_<YYYY_F><MONTH_F><DAY_F>_000000_v02.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L65/RSO/<YYYY>/<DOY>/GFZOP_RSO_L65_G_<YYYY_B><MONTH_B><DAY_B>_220000_<YYYY><MONTH><DAY>_120000_v03.sp3.gz',
             'ftp://isdcftp.gfz-potsdam.de/grace-fo/ORBIT/L65/RSO/<YYYY>/<DOY>/GFZOP_RSO_L65_G_<YYYY><MONTH><DAY>_100000_<YYYY_F><MONTH_F><DAY_F>_000000_v03.sp3.gz',
             ],

         'CHAMP_rnx': [
             'ftp://isdcftp.gfz-potsdam.de/champ/OG/Level1/SST/<YYYY>/CH-OG-1-SST+<YYYY>_<DOY>_00_R.9.zip',
             'ftp://isdcftp.gfz-potsdam.de/champ/OG/Level1/SST/<YYYY>/CH-OG-1-SST+<YYYY>_<DOY>_00_M.9.zip',
             'ftp://isdcftp.gfz-potsdam.de/champ/OG/Level1/SST/<YYYY>/CH-OG-1-SST+<YYYY>_<DOY>_00.9.zip'],

         'CHAMP_sp3': [
             'ftp://isdcftp.gfz-potsdam.de/champ/OG/Level3/RSO/<YYYY>/CH-OG-3-RSO+CTS-GPS_<YYYY>_<DOY>_00.zip'],

         'SWARM_A_rnx': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_A%2F'
             'SW_OPER_GPSA_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O "swma<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_A%2F'
             'SW_OPER_GPSA_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O "swma<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_A%2F'
             'SW_OPER_GPSA_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O "swma<DOY>0.<YY>o.zip"',
             ],

         'SWARM_B_rnx': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_B%2F'
             'SW_OPER_GPSB_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O "swmb<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_B%2F'
             'SW_OPER_GPSB_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O "swmb<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_B%2F'
             'SW_OPER_GPSB_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O "swmb<DOY>0.<YY>o.zip"',
             ],
             
         'SWARM_C_rnx': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_C%2F'
             'SW_OPER_GPSC_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O "swmc<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_C%2F'
             'SW_OPER_GPSC_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O "swmc<DOY>0.<YY>o.zip"',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSx_RO%2FSat_C%2F'
             'SW_OPER_GPSC_RO_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O "swmc<DOY>0.<YY>o.zip"',
             ],
        
         'SWARM_A_sp3': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_A%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O '
             'swa<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_A%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O '
             'swa<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_A%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O '
             'swa<GPSWD>.sp3.zip',
         ],

         'SWARM_B_sp3': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_B%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O '
             'swb<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_B%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O '
             'swb<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_B%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O '
             'swb<GPSWD>.sp3.zip',
         ],

         'SWARM_C_sp3': [
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_C%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0505.ZIP" -O '
             'swc<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_C%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0504.ZIP" -O '
             'swc<GPSWD>.sp3.zip',
             '"https://swarm-diss.eo.esa.int/?do=download&file=swarm%2FLevel1b%2FEntire_mission_data%2FGPSxNAV%2F'
             'Sat_C%2FSW_OPER_GPSBNAV_1B_<YYYY><MONTH><DAY>T000000_<YYYY><MONTH><DAY>T235959_0502.ZIP" -O '
             'swc<GPSWD>.sp3.zip',
         ],

         'COSMIC_1_att': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1a/<YYYY>/<DOY>/leoAtt_repro2013_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_1_crx': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1a/<YYYY>/<DOY>/podCrx_repro2013_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_1_orb': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/leoOrb_repro2013_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_1_clk': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/leoClk_repro2013_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_2_att': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1a/<YYYY>/<DOY>/leoAtt_nrt_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_2_crx': [
             "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1a/<YYYY>/<DOY>/podCrx_nrt_<YYYY>_<DOY>.tar.gz"],

         'COSMIC_2_orb': [
             'https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1b/<YYYY>/<DOY>/leoOrb_nrt_<YYYY>_<DOY>.tar.gz'],


        #  'C1_L1a_leoAtt': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1a/<YYYY>/<DOY>/leoAtt_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1a_opnGps': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1a/<YYYY>/<DOY>/opnGps_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1a_podCrx': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1a/<YYYY>/<DOY>/podCrx_repro2013_<YYYY>_<DOY>.tar.gz"],
    
        #  'C1_L1b_atmPhs': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/atmPhs_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_gpsBit': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/gpsBit_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_ionPhs': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/ionPhs_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_leoClk': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/leoClk_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_leoOrb': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/leoOrb_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_podTec': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/podTec_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C1_L1b_scnLv1': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic1/repro2013/level1b/<YYYY>/<DOY>/scnLv1_repro2013_<YYYY>_<DOY>.tar.gz"],

        #  'C2_L1a_leoAtt': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1a/<YYYY>/<DOY>/leoAtt_nrt_<YYYY>_<DOY>.tar.gz"],

        #  'C2_L1a_opnGps': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1a/<YYYY>/<DOY>/opnGps_nrt_<YYYY>_<DOY>.tar.gz"],

        #  'C2_L1a_podCrx': [
        #      "https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1a/<YYYY>/<DOY>/podCrx_nrt_<YYYY>_<DOY>.tar.gz"],

        #  'C2_L1b_conPhs': [
        #      'https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1b/<YYYY>/<DOY>/conPhs_nrt_<YYYY>_<DOY>.tar.gz'],

        #  'C2_L1b_leoOrb': [
        #      'https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1b/<YYYY>/<DOY>/leoOrb_nrt_<YYYY>_<DOY>.tar.gz'],

        #  'C2_L1b_podTc2': [
        #      'https://data.cosmic.ucar.edu/gnss-ro/cosmic2/nrt/level1b/<YYYY>/<DOY>/podTc2_nrt_<YYYY>_<DOY>.tar.gz'],

         'Panda_jpleph_de405': ['ftp://ics.gnsslab.cn/panda_tables/jpleph_de405'],

         'Panda_poleut1': ['ftp://ics.gnsslab.cn/panda_tables/poleut1'],

         'Panda_EGM': ['ftp://igshk.gnsswhu.cn/panda_tables/EGM'],

         'Panda_oceanload': ['ftp://ics.gnsslab.cn/panda_tables/oceanload'],

         'Panda_oceantide': ['ftp://ics.gnsslab.cn/panda_tables/oceantide'],

         'Panda_utcdif': ['ftp://ics.gnsslab.cn/panda_tables/utcdif'],

         'Panda_antnam': ['ftp://ics.gnsslab.cn/panda_tables/antnam'],

         'Panda_svnav': ['ftp://ics.gnsslab.cn/panda_tables/svnav.dat'],

         'Panda_nutabl': ['ftp://ics.gnsslab.cn/panda_tables/nutabl'],

         'Panda_ut1tid': ['ftp://ics.gnsslab.cn/panda_tables/ut1tid'],

         'Panda_leap_sec': ['ftp://ics.gnsslab.cn/panda_tables/leap.sec'],

         'Panda_gpsrapid': ['https://datacenter.iers.org/data/latestVersion/gpsrapid.out.txt'],

         "EOP_C04": ["https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt"],

         'Gamit_pmu_bull': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/pmu.bull_a",
                            "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/pmu.bull_r.last",
                            "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/pmu.bull_a.last",
                            "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/pmu.bull_a"
                            ],

         'Gamit_ut1usno': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                           "http://garner.ucsd.edu/pub/gamit/tables/ut1.usno"],

         'Gamit_poleusno': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/pole.usno"],

         'Gamit_dcb_dat': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                           "http://garner.ucsd.edu/pub/gamit/tables/dcb.dat.allgnss"],

         'Gamit_soltab': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/soltab.2000.J2000"],

         'Gamit_luntab': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/luntab.2000.J2000"],

         'Gamit_leap_sec': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                            "http://garner.ucsd.edu/pub/gamit/tables/leap.sec"],

         'Gamit_nutabl': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/nutabl.2020",
                          "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/nutabl.J2000.2020"],

         'Gamit_antmod': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/antmod.dat"],

         'Gamit_svnav': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                         "http://garner.ucsd.edu/pub/gamit/tables/svnav.dat"],

         'Gamit_rcvant': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                          "http://garner.ucsd.edu/pub/gamit/tables/rcvant.dat"],

         'Gamit_nbody': ['--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd '
                         'http://garner.ucsd.edu/pub/gamit/tables/nbody'],

         'IGS_hfile': ["--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs1a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs2a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs3a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs4a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs5a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs6a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs7a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs8a.<YY><DOY>.Z",
                       "--http-user=anonymous --http-passwd=fast@whu.wdu.com -nd "
                       "http://garner.ucsd.edu/pub/solutions/global/<YYYY>/<DOY>/higs9a.<YY><DOY>.Z"]
         }
