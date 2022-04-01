#!/usr/bin/python3
# FTP_source     : FTP source of each gnss center
# Author         : Chang Chuntao, CAO Duoming, Li Yongxi
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.01.14

plate = ["AF", "AN", "AR", "AU", "BU", "CA", "CO", "EU", "IN", "MA", "NA", "NB", "NZ", "OK", "ON", "PA", "PM", "PS",
         "SA", "SB", "SC", "SL", "SO", "SU", "WL"]
plate_env = []

for p in plate:
    plate_env.append("http://geodesy.unr.edu/velocities/midas." + p + ".txt")

FTP_S = {"GPS_brdc": ["ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://igs.gnsswhu.cn//pub/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.Z",
                      "ftp://nfs.kasi.re.kr/gps/data/daily/<YEAR>/<DOY>/<YY>n/brdc<DOY>0.<YY>n.gz"],

         "MGEX_brdm": ["ftp://igs.gnsswhu.cn/pub/gps/data/daily/<YEAR>/<DOY>/<YY>p/"
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
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.Z",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/wum<GPSWD>.sp3.Z"],

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

         "MGEX_GFZ_sp3": ["ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/"
                          "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                          "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/"
                          "GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"
                          ],

         "MGEX_COD_sp3": [
             "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz",
             "--ftp-user anonymous --ftp-password cctcasm@163.com "
             "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_05M_ORB.SP3.gz"
         ],

         "MGEX_SHA_sp3": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/sha<GPSWD>.sp3.Z",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/SHA0MGXRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/sha<GPSWD>.sp3.Z"],

         "MGEX_GRG_sp3": [
             "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3.gz"],

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
                          "<SITE>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/data/daily/<YYYY>/<DOY>/<YY>d/"
                          "<SITE>_R_<YYYY><DOY>0000_01D_30S_MO.crx.gz"],

         "GPS_USA_cors": ["--http-user=anonymous --http-passwd=1252443496@qq.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.Z",
                          "--http-user=anonymous --http-passwd=1252443496@qq.com "
                          "http://garner.ucsd.edu/pub/rinex/<YYYY>/<DOY>/<SITE><DOY>0.<YY>d.gz"],

         "GPS_HK_cors": ["ftp://ftp.geodetic.gov.hk/rinex2/<YYYY>/<DOY>/<SITE>/30s/<SITE><DOY>0.<YY>o.gz"],

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

         "MGEX_WUH_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/wum<GPSWD>.clk.Z"],

         "MGEX_COD_clk": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.CLK_M.Z"],

         "MGEX_GFZ_clk": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz"],

         "MGEX_GRG_clk": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/grg<GPSWD>.clk.Z",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/"
                          "GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz",
                          "ftp://igs.ign.fr/pub/igs/products/mgex/<GPSW>/grg<GPSWD>.clk.Z"],

         "WUH_PRIDE_clk": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/clock/"
                           "WUM0MGXRAP_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz"],

         "IGS_erp": ["--http-user=anonymous --http-passwd=1252443496@qq.com -nd "
                     "http://garner.ucsd.edu/pub/products/<GPSW>/igs<GPSWD>.erp.Z"],

         "WUH_erp": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
                     "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/WUM0MGXFIN_<YYYY><DOY>0000_01D_01D_ERP.ERP.Z",
                     "ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/wum<GPSWD>.erp.Z"],

         "COD_erp": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.ERP_M.Z"],

         "GFZ_erp": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgex/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz",
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_ERP.ERP.gz"],

         "MGEX_WUHN_IGMAS_bia": ["--ftp-user casm_cct --ftp-password wangji531! "
                                 "http://igmas.users.sgg.whu.edu.cn/products/download/directory/products/osb/"
                                 "<GPSW>/SGG<GPSWD>.BIA.tar.gz"],

         "MGEX_WHU_bia": ["ftp://igs.gnsswhu.cn/pub/whu/phasebias/<YYYY>/bias/"
                          "WUM0MGXRAP_<YYYY><DOY>0000_01D_01D_ABS.BIA.Z"],

         "GPS_COD_bia": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>/COD<GPSWD>.BIA.Z",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.bia.Z"],

         "MGEX_COD_bia": ["ftp://ftp.aiub.unibe.ch/CODE/<YYYY>_M/COD<GPSWD>.BIA_M.Z"],

         "MGEX_GFZ_bia": [
             "ftp://ftp.gfz-potsdam.de//pub/GNSS/products/mgnss/<GPSW>/GBM0MGXRAP_<YYYY><DOY>0000_01D_01D_OSB.BIA.gz"],

         "IGS_ion": ["ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>>/igsg<DOY>0.<YY>i.Z"],

         "WUH_ion": ["ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/whug<DOY>0.<YY>i.Z"],

         "COD_ion": ["ftp://igs.gnsswhu.cn/pub/gps/products/ionex/<YYYY>/<DOY>/codg<DOY>0.<YY>i.Z"],

         "IGS_day_snx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z",
                         "--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/igs<YY>P<GPSWD>.snx.Z"],

         "IGS_week_snx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftp://igs.gnsswhu.cn/pub/gps/products/<GPSW>/igs<YY>P<GPSW>.snx.Z",
                          "--ftp-user anonymous --ftp-password cctcasm@163.com"
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

         "MGEX_CAS_dcb": ["ftp://igs.ign.fr/pub/igs/products/mgex/dcb/<YYYY>/"
                          "CAS0MGXRAP_<YYYY><DOY>0000_01D_01D_DCB.BSX.gz"],

         "IGS14_TS_ENU": ["http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/<SITE>.tenv3"],

         "IGS14_TS_XYZ": ["http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/<SITE>.txyz2"],

         "Series_TS_Plot": ["http://geodesy.unr.edu/tsplots/IGS14/IGS14/TimeSeries/<SITE>.png"],

         "IGS14_Venu": ["http://geodesy.unr.edu/velocities/midas.IGS14.txt"],

         "IGS08_Venu": ["http://geodesy.unr.edu/velocities/midas.IGS08.txt"],

         "PLATE_Venu": plate_env,

         "HY_SLR": ["ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2a/<YYYY>/hy2a_<YYYY><MM>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2b/<YYYY>/hy2b_<YYYY><MM>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2c/<YYYY>/hy2c_<YYYY><MM>.npt",
                    "ftp://edc.dgfi.tum.de/slr/data/npt_crd/hy2d/<YYYY>/hy2d_<YYYY><MM>.npt"],

         "GPS_COD_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/<GPSW>/cod<GPSWD>.obx.Z"],

         "GPS_GRG_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                         "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GRG0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "MGEX_WUH_obx": ["ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/<GPSW>/"
                          "WUM0MGXFIN_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"],

         "MGEX_COD_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/COD0MGXFIN_<YYYY><DOY>0000_01D_15M_ATT.OBX.gz"],

         "MGEX_GFZ_obx": ["--ftp-user anonymous --ftp-password cctcasm@163.com "
                          "ftps://gdc.cddis.eosdis.nasa.gov/gps/products/mgex/<GPSW>/GFZ0MGXRAP_<YYYY><DOY>0000_01D_30S_ATT.OBX.gz"]
         }
