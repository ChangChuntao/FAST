# -*- coding: utf-8 -*-
# Download          : func for FAST Download module
# Author            : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)      : The GNSS Center, Wuhan University
# Creation Date     : 2022.06.06
# Latest Version    : 2023.06.30


import datetime
import os
import sys
import time
import timeit
from multiprocessing.pool import ThreadPool
from fast.download.fileOperation import isFileInPath, uncompressFileArg, uncompress_ym, uncompress_highrate_rinex
from fast.com.pub import ym_type, yd_type, ydh_type, yds_type, ydsh_type, s_type, gs_type, no_type, sub_type, gnss_type
from fast.com.gnssTime import ReplaceTimeWildcard, ReplaceMMM, doy2gpswd
from fast.download.ftpSrc import FTP_S
from fast.com.pub import printFast, exeCmd
from fast.com.mgexInf import replaceSiteStr
import platform
# import distro


if platform.system() == 'Windows':
    """
    2022-03-27 : 判断操作平台,获取bin下下载程序    by Chang Chuntao -> Version : 1.00
    2022-09-16 : 更新索引位置                    by Chang Chuntao -> Version : 1.21
    """
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.join(dirname, '..')
    # printFast('Operating system -> Windows', "important")
    wget = os.path.join(dirname, 'bin', 'wget.exe')
    lftp = os.path.join(dirname, 'bin', 'lftp')
    wget += " -T 3 -t 3 -N -c "
    lftp += ' '
elif platform.system() == 'Darwin':
    # printFast('当前为Mac系统', "important")
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.join(dirname, '..')
    wget = os.path.join(dirname, 'mac_bin', 'wget')
    lftp = os.path.join(dirname, 'mac_bin', 'lftp')
    wget += " -T 3 -t 3 -N -c "
    lftp += ' '
else:
    # printFast('Operating system -> Linux', "important")
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.join(dirname, '..')
    # if 'CentOS' in distro.name():
    #     binDir = os.path.join(dirname, 'cbin')
    #     binDir = os.path.join(dirname, 'bin')
    # else:
    #     binDir = os.path.join(dirname, 'ubin')
    #     binDir = os.path.join(dirname, 'bin')

    binDir = os.path.join(dirname, 'bin')
    # wget = os.path.join(binDir, 'wget')
    wget = 'wget'
    lftp = os.path.join(binDir, 'lftp')
    wget += " -T 3 -t 3 -N -c "
    lftp += ' '


def wgets(fn):  # 下载单个文件
    """
    2022-03-27 :    调取wget下载单个文件 by Chang Chuntao -> Version : 1.00
    2024-04-12 :    os.system -> subprocess.run # for macos
                    by Chang Chuntao -> Version : 3.00
    """
    import subprocess
    if isFileInPath(fn.split("/")[-1]):
        return 0
    else:
        cmd = wget + fn
        os.system(cmd)
        # exeCmd(cmd, addTime=False)
        # print(cmd)
        # os.system(cmd)
#         subprocess.run(cmd.split(),
#     # shell=True,
#     check=True
# )


def wgetm(url):  # 下载列表内文件
    """
    2022-03-27 : 通过下载列表调取wget下载单个文件 by Chang Chuntao -> Version : 1.00
    """
    downloadFileList = []
    for fn in url:
        file = fn.split("/")[-1]
        if isFileInPath(file):
            # printFast("文件已经存在：" + file + "!", "warning")
            continue
        else:
            # printFast("Try downloading file -> " + file + "!", "normal")
            wgets(fn)
        if os.path.isfile(file):
            downloadFileList.append(file)
    return downloadFileList




def lftps(url):
    """
    2022-03-27 : 通过下载列表调取lftp下载文件 by Chang Chuntao -> Version : 1.00
    """

    cmd = lftp + url
    os.system(cmd)
    time.sleep(0.1)


def fastPoolDownload(urllist, process):
    """
    2022-03-27 :    引导模式并发下载子程序 by Chang Chuntao -> Version : 1.00
    2022-03-27 :    pool.apply_async -> concurrent.futures.ThreadPoolExecutor # for macos
                    by Chang Chuntao -> Version : 3.00
    """
    import concurrent.futures
    printFast("Start downloading!", "important")
    print("")
    start_time = timeit.default_timer()

    with concurrent.futures.ThreadPoolExecutor(max_workers=process) as executor:
        results = [executor.submit(wgetm, task) for task in urllist]
        successDownFileList = []
        for future in concurrent.futures.as_completed(results):
            successDownFileList += future.result()

    end_time = timeit.default_timer() - start_time
    if len(successDownFileList) > 0:
        printFast("已下载 / Successfully downloaded " + str(len(successDownFileList)) + " files!", "important")
        printFast("Running Time : %.02f seconds" % end_time, "important")
    # else:
    #     printFast("No files were downloaded!", "important")
    #     printFast("没有下载任何文件!", "important")
    return successDownFileList


def argpooldownload(urllist, process, loc, compress, data_type, proname):
    """
    2022-03-27 : 参数输入模式并发下载子程序 by Chang Chuntao -> Version : 1.00
    """
    
    from fast.download.fileOperation import renamePro
    nowdir = os.getcwd()
    if len(loc) == 0:
        os.chdir(nowdir)
    else:
        os.chdir(loc)
    printFast("Start downloading!", "important")
    print("")
    start_time = timeit.default_timer()
    results = []
    for typeurl in urllist:
        pool = ThreadPool(process)
        # pool.map(wgetm, typeurl)
        for task in typeurl:
            result = pool.apply_async(wgetm, (task,))
            results.append(result)
        pool.close()
        pool.join()
    successDownFileList = []
    for i in results:
        successDownFileList += i.get()
    extractedFileList = []
    if compress == "Y" or compress == "y":
        extractedFileList = uncompressFileArg(loc, successDownFileList)
    if len(extractedFileList) > 0 and proname!= '':
        renamePro(extractedFileList, proname)

    end_time = timeit.default_timer() - start_time
    if len(successDownFileList) > 0:
        printFast("Successfully downloaded " + str(len(successDownFileList)) + " files!", "important")
        printFast("Running time : %.02f seconds" % end_time, "important")
    else:
        printFast("No files were downloaded!", "important")
    os.chdir(nowdir)
    return successDownFileList


def getUrlByRun(fastArgByRun):
    """
    2022-04-12 :    通过输入引导的参数获取下载列表,下载文件、解压文件 by Chang Chuntao  -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-08-04 :    修正时序文件下载需求
                    by Chang Chuntao  -> Version : 1.19
    2022-09-16 :    新增站点字符串替换子程序
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological,为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-11-02 :    > 添加DORIS判断
                    by Chang Chuntao  -> Version : 1.25
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2022-11-15 :    > 添加GRE_IGS_01S判断,调用uncompressFile_highrate_rinex
                    by Chang Chuntao  -> Version : 2.03
    2023-06-30 :    + 增加输入小时模式
                    by Chang Chuntao  -> Version : 2.09
    """
    
    urllist = []  # 下载列表

    from fast.download.mode import getHour, getFile, getvlbicompress, getUncompress
    from fast.download.mode import runByYearDoy, runByYearMonth
    from fast.download.mode import getRename
    # 数据类型为IVS_week_snx, lftp下载
    if fastArgByRun['datatype'] == "IVS_week_snx":
        ftpsite = FTP_S[fastArgByRun['datatype']][0]
        ym = runByYearMonth()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            ftpsite = ftpsite.replace('<YY>', str(year)[2:4])
            ftpsite = ReplaceMMM(ftpsite, month)
            printFast("Start downloading!", "important")
            start_time = timeit.default_timer()
            lftps(ftpsite)
            end_time = timeit.default_timer() - start_time
            printFast("Download finished!", "important")
            printFast("Running time : %.02f seconds" % end_time, "important")
            getvlbicompress(ftpsite)
            return "n"

    # 数据类型为输入年月
    elif fastArgByRun['datatype'] in ym_type and fastArgByRun['datatype'] != "IVS_week_snx":
        ftpsite = FTP_S[fastArgByRun['datatype']]
        ym = runByYearMonth()  # 获取下载时间
        if ym == "y":
            return "y"
        else:
            [year, month] = ym  # 获取下载时间
            # ftpsite_new = []
            successDownFileList = []
            ym_datetime = datetime.datetime(year, month, 1)
            for ftp in ftpsite:
                file = ftp.split("/")[-1]
                ftp = ReplaceTimeWildcard(ftp, ym_datetime)
                wgets(ftp)
                if os.path.isfile(file):
                    successDownFileList.append(file)
            uncompress_ym(successDownFileList)
            return "n"
    else:
        # 数据类型为输入年日
        # 输入为年, 起始年积日, 终止年积日 的数据类型
        if fastArgByRun['datatype'] in yd_type:
            yd = runByYearDoy()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                fastArgByRun['year'] = year
                fastArgByRun['day1'] = day1
                fastArgByRun['day2'] = day2
                printFast(
                    "Year - " + str(fastArgByRun['year']) + " Doy - " + str(fastArgByRun['day1']) + " ~ " + str(fastArgByRun['day2']),
                    "normal")
                print("")
                for day in range(fastArgByRun['day1'], fastArgByRun['day2'] + 1):
                    gpsweek, dayofweek = doy2gpswd(year, day)
                    if fastArgByRun['datatype'] == 'IDS_week_snx':
                        if dayofweek == 0:
                            ftpsitelist = getftp(fastArgByRun['datatype'], fastArgByRun['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                            urllist.append(ftpsitelist)  # 按天下载
                    else:
                        ftpsitelist = getftp(fastArgByRun['datatype'], fastArgByRun['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                        urllist.append(ftpsitelist)  # 按天下载
                if len(urllist) == 0:
                    printFast('此天无数据！ / No data available for this day!', 'fail')
                    return "n"
                if fastArgByRun['datatype'] == 'IGS_week_snx' or fastArgByRun['datatype'] == 'IVS_week_snx' or fastArgByRun[
                    'datatype'] == 'IDS_week_snx' or fastArgByRun['datatype'] == 'ILS_week_snx':
                    successDownFileList = fastPoolDownload(urllist, 1)  # 多线程下载
                else:
                    successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
                extractedFileList = getUncompress(successDownFileList)
                if extractedFileList is not None:
                    if len(extractedFileList) > 0:
                        getRename(extractedFileList)
                return "n"

        # 数据类型为输入年日小时
        # 输入为年, 起始年积日, 终止年积日 小时 的数据类型
        if fastArgByRun['datatype'] in ydh_type:
            yd = runByYearDoy()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                fastArgByRun['year'] = year
                fastArgByRun['day1'] = day1
                fastArgByRun['day2'] = day2
                hour = getHour()
                printFast(
                    "Year - " + str(fastArgByRun['year']) + " Doy - " + str(fastArgByRun['day1']) + " ~ " + str(fastArgByRun['day2']),
                    "normal")
                print("")
                for day in range(fastArgByRun['day1'], fastArgByRun['day2'] + 1):
                    ftpsitelist = getftp(fastArgByRun['datatype'], fastArgByRun['year'], day, [hour])  # 通过数据类型与下载时间获取完整下载地址
                    urllist.append(ftpsitelist)  # 按天下载
                if len(urllist) == 0:
                    printFast('此天无数据！ / No data available for this day!', 'fail')
                    return "n"
                successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
                getUncompress(successDownFileList)
                return "n"

        # 数据类型为输入年日站点文件小时数据
        # 输入为年, 起始年积日, 终止年积日, 站点文件 的小时数据类型
        elif fastArgByRun['datatype'] in ydsh_type:
            findFtp = []
            yd = runByYearDoy()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                fastArgByRun['year'] = year
                fastArgByRun['day1'] = day1
                fastArgByRun['day2'] = day2
                printFast(
                    "Year - " + str(fastArgByRun['year']) + " Doy - " + str(fastArgByRun['day1']) + " ~ " + str(fastArgByRun['day2']),
                    "normal")
                fastArgByRun['site'] = getFile(fastArgByRun['datatype'])
                for day in range(fastArgByRun['day1'], fastArgByRun['day2'] + 1):
                    for hour in range(24):
                        ftpsitelist = getftp(fastArgByRun['datatype'], fastArgByRun['year'], day, [hour])  # 通过数据类型与下载时间获取完整下载地址
                        for siteInList in fastArgByRun['site']:
                            siteftp = []
                            for ftpInList in ftpsitelist:
                                ftpInList = replaceSiteStr(ftpInList, siteInList)
                                if ftpInList not in findFtp:
                                    findFtp.append(ftpInList)
                                    siteftp.append(ftpInList)
                urllist.append(siteftp)  # 按天下载
                successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
                uncompress_highrate_rinex(successDownFileList)
                return "n"

        # 数据类型为输入年日站点文件
        # 输入为年, 起始年积日, 终止年积日, 站点文件 的数据类型
        elif fastArgByRun['datatype'] in yds_type:
            yd = runByYearDoy()
            if yd == "y":
                return "y"
            else:
                [year, day1, day2] = yd  # 获取下载时间
                fastArgByRun['year'] = year
                fastArgByRun['day1'] = day1
                fastArgByRun['day2'] = day2
                printFast(
                    "Year - " + str(fastArgByRun['year']) + " Doy - " + str(fastArgByRun['day1']) + " ~ " + str(fastArgByRun['day2']),
                    "normal")
                fastArgByRun['site'] = getFile(fastArgByRun['datatype'])
                for day in range(fastArgByRun['day1'], fastArgByRun['day2'] + 1):
                    ftpsitelist = getftp(fastArgByRun['datatype'], fastArgByRun['year'], day)  # 通过数据类型与下载时间获取完整下载地址
                    for siteInList in fastArgByRun['site']:
                        siteftp = []
                        for ftpInList in ftpsitelist:
                            ftpInList = replaceSiteStr(ftpInList, siteInList)
                            siteftp.append(ftpInList)
                        urllist.append(siteftp)  # 按天下载
                successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
                extractedFileList = getUncompress(successDownFileList)
                return "n"

        elif fastArgByRun['datatype'] in s_type:  # 输入为站点文件 的数据类型
            fastArgByRun['site'] = getFile(fastArgByRun['datatype'])
            ftpsite = FTP_S[fastArgByRun['datatype']]
            for siteInList in fastArgByRun['site']:
                siteftp = []
                for ftpInList in ftpsite:
                    ftpInList = replaceSiteStr(ftpInList, siteInList)
                    siteftp.append(ftpInList)
                urllist.append(siteftp)  # 按天下载
            successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
            getUncompress(successDownFileList)
            return "n"

        # 无需输入时间的数据类型
        elif fastArgByRun['datatype'] in no_type:
            ftpsite = FTP_S[fastArgByRun['datatype']]
            urllist.append(ftpsite)
            successDownFileList = fastPoolDownload(urllist, 3)  # 多线程下载
            getUncompress(successDownFileList)
            return "n"

def geturlByArg(fastArgByArg):
    """
    2022.04.12 :    获取下载列表 by Chang Chuntao -> Version : 1.10
    2022-04-22 :    新增TRO内资源IGS_zpd、COD_tro、 JPL_tro、 GRID_1x1_VMF3、 GRID_2.5x2_VMF1、 GRID_5x5_VMF3
                    by Chang Chuntao  -> Version : 1.11
    2022-09-16 :    新增站点字符串替换子程序
                    by Chang Chuntao  -> Version : 1.21
    2022-09-20 :    + 新增TROP内资源Meteorological,为需要站点的气象文件
                    by Chang Chuntao  -> Version : 1.22
    2022-10-10 :    > 修复无需其他参数输入下载类下载
                    by Chang Chuntao  -> Version : 1.24
    2022-11-09 :    > 修改索引: yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month
                    >         s_type -> site
                    > 删除旧索引: objneedydqd2 / objneedyd1d2loc / objneedloc / objneedn
                    by Chang Chuntao  -> Version : 2.01
    2023-03-12 :    > 修复仅需站点模式
                    by Chang Chuntao  -> Version : 2.08
    2023-06-30 :    + 增加输入小时模式
                    by Chang Chuntao  -> Version : 2.09
    """
    from fast.download.mode import getSite
    urllist = []
    for dt in str(fastArgByArg['datatype']).split(","):
        typeurl = []
        printFast("数据类型 / Data type :" + dt, "normal")

        # 数据类型为无需输入
        if dt in no_type:
            ftpsitelist = getftp(dt, 2022, 1)
            typeurl.append(ftpsitelist)
            urllist.append(typeurl)

        # 数据类型为输入年日
        elif dt in yd_type:
            printFast("Year " + str(fastArgByArg['year']) + " Doy - " + str(fastArgByArg['day1']) + " ~ " + str(
                fastArgByArg['day2']) + "\n",
                     "normal")
            for day in range(fastArgByArg['day1'], fastArgByArg['day2'] + 1):
                ftpsitelist = getftp(dt, fastArgByArg['year'], day)
                url = []
                if len(ftpsitelist) != 0:
                    for ftpsite in ftpsitelist:
                        url.append(ftpsite)
                    typeurl.append(url)
            urllist.append(typeurl)

        # 数据类型为输入年日站点文件
        elif dt in yds_type:
            printFast("Year " + str(fastArgByArg['year']) + " Doy - " + str(fastArgByArg['day1']) + " ~ " + str(
                fastArgByArg['day2']) + "\n",
                     "normal")
            print("")
            fastArgByArg['site'] = getSite(fastArgByArg['file'], dt)

            for day in range(fastArgByArg['day1'], fastArgByArg['day2'] + 1):
                ftpsitelist = getftp(dt, fastArgByArg['year'], day)
                for siteInList in fastArgByArg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载
            urllist.append(typeurl)

        # 数据类型为输入年月文件
        elif dt in ym_type and dt != "IVS_week_snx":
            printFast("Year - " + str(fastArgByArg['year']) + " Month - " + str(fastArgByArg['month']) + "\n",
                     "normal")
            print("")
            for day in range(fastArgByArg['month'], fastArgByArg['month'] + 1):
                typeurl = []
                ftpsite = FTP_S[dt]
                ym_datetime = datetime.datetime(fastArgByArg['year'], fastArgByArg['month'], 1)
                for ftp in ftpsite:
                    ftp = ReplaceTimeWildcard(ftp, ym_datetime)
                    typeurl.append([ftp])
            urllist.append(typeurl)

        # 数据类型为输入站点文件
        elif dt in s_type:
            fastArgByArg['site'] = getSite(fastArgByArg['file'], dt)
            for day in range(fastArgByArg['day1'], fastArgByArg['day2'] + 1):
                ftpsitelist = getftp(dt, fastArgByArg['year'], day)
                for siteInList in fastArgByArg['site']:
                    siteftp = []
                    for ftpInList in ftpsitelist:
                        ftpInList = replaceSiteStr(ftpInList, siteInList)
                        siteftp.append(ftpInList)
                    typeurl.append(siteftp)  # 按天下载
            urllist.append(typeurl)

        # 数据类型为输入年日时
        elif dt in ydh_type:
            printFast("Year - " + str(fastArgByArg['year']) + " Doy - " + str(fastArgByArg['day1']) + " ~ " + str(
                fastArgByArg['day2']) + "\n",
                     "normal")
            for day in range(fastArgByArg['day1'], fastArgByArg['day2'] + 1):
                ftpsitelist = getftp(dt, fastArgByArg['year'], day, fastArgByArg['hour'])
                url = []
                if len(ftpsitelist) != 0:
                    for ftpsite in ftpsitelist:
                        url.append(ftpsite)
                    typeurl.append(url)
            urllist.append(typeurl)

        # 数据类型为输入年日小时站点文件
        elif dt in ydsh_type:
            printFast("Year - " + str(fastArgByArg['year']) + " Doy - " + str(fastArgByArg['day1']) + " ~ " + str(
                fastArgByArg['day2']) + "\n",
                     "normal")
            print("")
            findFtp = []
            fastArgByArg['site'] = getSite(fastArgByArg['file'], dt)
            for day in range(fastArgByArg['day1'], fastArgByArg['day2'] + 1):
                for hour in list(range(24)):
                    ftpsitelist = getftp(dt, fastArgByArg['year'], day, [hour])  # 通过数据类型与下载时间获取完整下载地址
                    for siteInList in fastArgByArg['site']:
                        siteftp = []
                        for ftpInList in ftpsitelist:
                            ftpInList = replaceSiteStr(ftpInList, siteInList)
                            if ftpInList not in findFtp:
                                findFtp.append(ftpInList)
                                siteftp.append(ftpInList)
                        typeurl.append(siteftp)  # 按天下载
            urllist.append(typeurl)
    return urllist

def getftp(t, y, d, hour=None):
    """
    2022-03-27 : * 通过数据类型、年、年积日,获取下载列表,并调用ReplaceTimeWildcard生成下载链接list
                 by Chang Chuntao -> Version : 1.00
    2022-11-02 : > 添加DORIS判断
                 by Chang Chuntao -> Version : 1.25
    """
    if hour is None:
        hour = [0]
    yeard1 = '%04d' % y + '-01-01 00:00:00'
    yeard1 = datetime.datetime.strptime(yeard1, '%Y-%m-%d %H:%M:%S')
    spectime = yeard1 + datetime.timedelta(days=d - 1)
    gpsweek, dayofweek = doy2gpswd(y, d)
    ftpsiteout = []
    if t == 'IDS_week_snx':
        if dayofweek == 0:
            ftpsite = FTP_S[t]
            for fd in ftpsite:
                for nowHour in hour:
                    nowSpectime = spectime + datetime.timedelta(hours=nowHour)
                    ftpsiteout.append(ReplaceTimeWildcard(fd, nowSpectime))
    else:
        ftpsite = FTP_S[t]
        for fd in ftpsite:
                for nowHour in hour:
                    nowSpectime = spectime + datetime.timedelta(hours=nowHour)
                    fileInFtp = ReplaceTimeWildcard(fd, nowSpectime)
                    if fileInFtp not in ftpsiteout:
                        ftpsiteout.append(fileInFtp)
    return ftpsiteout
