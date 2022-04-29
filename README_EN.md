# FAST （Fusion Abundant multi-Source data download Terminal）

####Introduce
**FAST**
Aiming at the problems of cumbersome steps and slow download speed of GNSS data, a relatively complete set of integrated multi-source data download terminal software fast is developed.   
The software contains most of the data sources required in the process of GNSS scientific research and learning. The way of parallel download greatly improves the efficiency of download.

#### Git
- [https://github.com/ChangChuntao/FAST](https://github.com/ChangChuntao/FAST)
- [https://gitee.com/changchuntao/FAST](https://gitee.com/changchuntao/FAST)


#### Software features

- **Multi platform**: Support both windows and Linux systems;
- **Abundant Resources**: It basically includes the data sources required in GNSS scientific research and learning. At present, it supports 15 categories and 62 subcategories. See the specific **Data support**;
- **Fast**: The software adopts parallel download mode, and the number of download threads can be specified in the command line parameter operation mode. After testing, it only takes 48.93s to download the 100 days BRDC+IGS+CLK file!
- **Easy to expand**: If you need to support more data sources, you can specify the required data and data sources in FTP_Source.py and GNSS_TYPE.py;
- **Easy to run**: The program can be downloaded in two ways: boot download mode and terminal input mode with parameters. Run the program directly to enter the boot download mode. Run `FAST -h` on the terminal with parameters to view the introduction of operation mode with parameters;
- **Flexible**: In the operation mode with parameters, users can flexibly specify the download type, download location, download time, whether to decompress, number of threads, etc., and can write scripts such as bat, shell and python to run according to their own needs;
- **Portable**: the windows package is only 18.9 MB, and the Linux package is only 6.63 MB


#### Installation tutorial

- **Windows**you only need to unzip the package to run directly, enter `FAST.exe -h` can view the introduction of operation mode with parameters;
- **Linux**The pilot software wget\LFTP\ncompress\python3 needs to be installed. Take Ubuntu system as an example, enter the following code in the terminal：  

```
apt-get install wget
apt-get install lftp
apt-get install ncompress
apt-get install python3
```

After installation, as under Windows system, you can directly run the program or configure the program to environment variables.

#### Instructions

**Boot Download Mode**: In Windows system, click run fast Exe can enter the boot download. If it is a Linux system, the terminal can enter `FAST` to run;  
1. Take downloading the multi system precise ephemeris of Wuhan University as an example, select SP3 in the primary selection directory, enter 2 and press enter；  
![一级目录](Windows/RUN_image/%E5%BC%95%E5%AF%BC%E4%B8%BB%E7%9B%AE%E5%BD%95.png)
  
2. Select MGEX_WUH_SP3 is input 6 and enter, where MGEX represents multi system GNSS, WHU represents Wuhan University, IGS data processing center and SP3 represents precision ephemeris;
![二级目录](Windows/RUN_image/%E5%BC%95%E5%AF%BC%E4%BA%8C%E7%BA%A7%E7%9B%AE%E5%BD%95.png)  
  
3. Enter the time according to the prompt and press enter to complete the input;
![输入时间](Windows/RUN_image/%E8%BE%93%E5%85%A5%E6%97%B6%E9%97%B4.png)

4. After the download is completed, press enter directly according to the prompt to complete the decompression, or press enter without decompression;
![下载完成](Windows/RUN_image/%E8%A7%A3%E5%8E%8B.png)
![解压完成](Windows/RUN_image/%E4%B8%8B%E8%BD%BD%E5%AE%8C%E6%88%90.png)  

5. Enter y or exit again according to the prompt;
![在此引导](Windows/RUN_image/%E5%86%8D%E6%AC%A1%E5%BC%95%E5%AF%BC.png)
  
**Terminal input mode**: In Windows system, run `FAST.exe -h` in CMD or power shell software to view the help. If it is a Linux system terminal, enter `FAST -h` to view the help;
```
  FAST : Fusion Abundant multi-Source data download Terminal
  ©Copyright 2022.01 @ Chang Chuntao
  PLEASE DO NOT SPREAD WITHOUT PERMISSION OF THE AUTHOR !

  Usage: FAST <options>

  Where the following are some of the options avaiable:

  -v,  --version                   display the version of GDD and exit
  -h,  --help                      print this help
  -t,  --type                      GNSS type, if you need to download multiple data,
                                   Please separate characters with " , "
                                   Example : GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk
  -l,  --loc                       which folder is the download in
  -y,  --year                      where year are the data to be download
  -o,  --day1                      where first day are the data to be download
  -e,  --day2                      where last day are the data to be download
  -m,  --month                     where month are the data to be download
  -u,  --uncomprss Y/N             Y - unzip file (default)
                                   N - do not unzip files
  -f,  --file                      site file directory,The site names in the file are separated by spaces.
                                   Example : bjfs irkj urum
  -p   --process                   number of threads (default 12)

  Example: FAST -t MGEX_IGS_atx
           FAST -t GPS_brdc,GPS_IGS_sp3,GPS_IGR_clk -y 2022 -d 22 -p 30
           FAST -t MGEX_WUH_sp3 -y 2022 -d 22 -u N -l D:\code\CDD\Example
           FAST -t MGEX_IGS_rnx -y 2022 -d 22 -f D:\code\cdd\mgex.txt
           FAST -t IVS_week_snx -y 2022 -m 1
```


#### Supported Data

1. BRDC : GPS_brdc / MGEX_brdm  
  
  
2. SP3 : GPS_IGS_sp3 / GPS_IGR_sp3 / GPS_IGU_sp3 / GPS_GFZ_sp3 / GPS_GRG_sp3   
   MGEX_WUH_sp3 / MGEX_WUHU_sp3 / MGEX_GFZ_sp3 / MGEX_COD_sp3  
   MGEX_SHA_sp3 / MGEX_GRG_sp3 / GLO_IGL_sp3

  
3. RINEX :GPS_IGS_rnx / MGEX_IGS_rnx / GPS_USA_cors / GPS_HK_cors / GPS_EU_cors  
   GPS_AU_cors

  
4. CLK : GPS_IGS_clk / GPS_IGR_clk / GPS_IGU_clk / GPS_GFZ_clk / GPS_GRG_clk
   GPS_IGS_clk_30s
   MGEX_WUH_clk / MGEX_COD_clk / MGEX_GFZ_clk / MGEX_GRG_clk / WUH_PRIDE_clk

  
5. ERP : IGS_erp / WUH_erp / COD_erp / GFZ_erp

  
6. BIA : MGEX_WHU_bia / GPS_COD_bia / MGEX_COD_bia / MGEX_GFZ_bia

  
7. ION : IGS_ion / WUH_ion / COD_ion

  
8. SINEX : IGS_day_snx / IGS_week_snx / IVS_week_snx / ILS_week_snx / IDS_week_snx

  
9. CNES_AR : CNES_post / CNES_realtime

  
10. ATX : MGEX_IGS_atx

  
11. DCB : GPS_COD_dcb / MGEX_CAS_dcb / MGEX_WHU_OSB / P1C1 / P1P2 / P2C2  

  
12. Time_Series : IGS14_TS_ENU / IGS14_TS_XYZ / Series_TS_Plot  

  
13. Velocity_Fields : IGS14_Venu / IGS08_Venu / PLATE_Venu  

  
14. SLR : HY_SLR / GRACE_SLR / BEIDOU_SLR  

  
15. OBX : GPS_COD_obx / GPS_GRG_obx / MGEX_WUH_obx / MGEX_COD_obx / MGEX_GFZ_obx  

  
16. TRO : IGS_zpd / COD_tro / JPL_tro / GRID_1x1_VMF3 / GRID_2.5x2_VMF1 / GRID_5x5_VMF3

#### Participation and contribution


1. **Chang Chuntao** @China Academy of Surveying and mapping  
    Program design/ Program writing/ Document writing/ Program testing/ Program maintenance     
    

2. Pd. **Jiang Kecai**@WuHan University   
    Program idea / parallel computing processing idea
  

3. Dr. **Mu Renhai**@WuHan University  
    Program design/ program testing/ Documentation


4.  Dr. **Li Bo** @Liaoning Technical University&China Academy of Surveying and mapping  
    Program testing/ Documentation/ Download node summary


5.  **Li Yongxi** @Lanzhou Jiaotong University&China Academy of Surveying and mapping  
    Program testing/ Download node summary


6.  **Cao Duoming** @Shandong University of Science and Technology&China Academy of Surveying and mapping  
    Program testing/ Download node summary