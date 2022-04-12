# FAST （Fusion Abundant multi-Source data download Terminal）

#### 介绍
**FAST**
针对目前GNSS数据下载步骤繁琐、下载速度慢等问题，开发了一套较为完备的融合多源数据下载终端软件——FAST。  
软件目前包含GNSS科研学习过程中绝大部分所需的数据源，采用并行下载的方式极大的提升了下载的效率。

#### Git地址
- [https://github.com/ChangChuntao/FAST](https://github.com/ChangChuntao/FAST)
- [https://gitee.com/changchuntao/FAST](https://gitee.com/changchuntao/FAST)


#### 软件特点
- **多平台**：同时支持windows与linux系统；
- **资源丰富**：基本囊括了GNSS科研学习中所需的数据源，目前支持15个大类、62个小类，具体支持数据见**数据支持**；
- **快速**：软件采用并行下载方式，在命令行参数运行模式可自行指定下载线程数，经测试下载100天的brdc+igs+clk文件只需要48.93s！
- **易拓展**：如需支持更多数据源，可在FTP_Source.py、GNSS_TYPE.py中指定所需的数据与数据源；
- **简单易行**：程序有引导下载模式与命令行带参数运行模式两种方式下载，直接运行程序便可进入引导下载模式，命令行带参数运行`FAST -h`可查看带参数运行模式介绍；
- **灵活**：在带参数运行模式下，用户可灵活指定下载类型、下载位置、下载时间、是否解压、线程数等，可根据自我需求编写bat、shell、python等脚本运行；
- **轻便**：windows程序包仅有18.9 MB，Liunx程序包仅有6.63 MB.


#### 安装教程
- **Windows系统**下仅需解压程序包即可直接运行,CMD运行`FAST.exe -h`可查看带参数运行模式介绍；
- **Linux系统**下需安装先导软件wget\lftp\ncompress\python3，以Ubuntu系统为例，于终端中输入以下代码：  

```
apt-get install wget
apt-get install lftp
apt-get install ncompress
apt-get install python3
```
安装后如windows系统下相同可直接运行程序，或将程序配置至环境变量中。

#### 使用说明

**引导下载模式**Windows系统双击运行FAST.exe便可进入引导下载，若为Linux系统终端输入`FAST`运行即可：  
1.  以下载武汉大学多系统精密星历为例，在一级选择目录中选择SP3，即为输入2后回车；  
![一级目录](Windows/RUN_image/%E5%BC%95%E5%AF%BC%E4%B8%BB%E7%9B%AE%E5%BD%95.png)
  
2.  选择MGEX_WUH_sp3即为输入6并回车，其中MGEX代表多系统，WUH代表武汉大学IGS数据处理中心，SP3代表精密星历；
![二级目录](Windows/RUN_image/%E5%BC%95%E5%AF%BC%E4%BA%8C%E7%BA%A7%E7%9B%AE%E5%BD%95.png)  
  
3.  根据引导输入时间，回车完成输入；
![输入时间](Windows/RUN_image/%E8%BE%93%E5%85%A5%E6%97%B6%E9%97%B4.png)

4.  下载完成，根据提示直接回车完成解压或者输入任意字符回车不解压；
![下载完成](Windows/RUN_image/%E8%A7%A3%E5%8E%8B.png)
![解压完成](Windows/RUN_image/%E4%B8%8B%E8%BD%BD%E5%AE%8C%E6%88%90.png)  

5.  根据提示输入y再次进入引导或退出；  
![在此引导](Windows/RUN_image/%E5%86%8D%E6%AC%A1%E5%BC%95%E5%AF%BC.png)
  
**命令行带参数运行模式**Windows系统CMD或power shell运行`FAST.exe -h`可查看命令行运行帮助，若为Linux系统终端输入`FAST -h`查看帮助：  
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


#### 数据支持

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

#### 参与贡献

1.  **常春涛**@中国测绘科学研究院  
    程序思路、主程序编写、文档编写、程序测试

2.  **慕任海**博士@武汉大学  
    程序思路、程序编写、程序测试

3.  **李博**博士@辽宁工程技术大学&中国测绘科学研究院  
    程序测试、文档编写、节点汇总

4.  **李勇熹**@兰州交通大学&中国测绘科学研究院  
    程序测试、节点汇总

5.  **曹多明**@山东科技大学&中国测绘科学研究院  
    程序测试、节点汇总
