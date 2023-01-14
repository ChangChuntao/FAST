#!/usr/bin/python3
# -*- coding: utf-8 -*-
# CDD_Sub        : Format conversion subroutine
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.06
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-01-14 - Version 2.06

import os
import platform
import shutil
import subprocess
import sys
import time
from FAST_Print import PrintGDD
from GNSS_Timestran import gnssTime2datetime, datetime2GnssTime
from pubFuncs import mkdir, copyFile, moveFile, EmptyFolder


def isinpath(file):  # 判断相关文件是否存在
    """
    2022-03-27 :    判断文件在本地是否存在
                    by Chang Chuntao    -> Version : 1.00
    2022-09-09 :    > 修正广播星历文件判定
                    by Chang Chuntao    -> Version : 1.20
    2022-11-15 :    > 增加高采样率判定
                    by Chang Chuntao    -> Version : 2.03
    2023-01-14 :    > 修正SP3 CLK判定
                    by Chang Chuntao    -> Version : 2.03
    """
    orifile = str(file).split(".")[0]
    if len(orifile) > 9:
        if '.SP3' not in file and '.CLK' not in file:
            filelowo = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
            filelowd = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
            filelowp = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
            fileprolow = file.lower()[0:4] + file.lower()[16:20] + ".bia"
            sp3filelow = filelowo
            filelown = filelowo
        elif '.SP3' in file or '.sp3' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            sp3filelow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".sp3"
            filelowo = sp3filelow
            filelowd = sp3filelow
            filelowp = sp3filelow
            filelown = sp3filelow
            fileprolow = filelown
        elif '.CLK' in file or '.clk' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            sp3filelow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".clk"
            filelowo = sp3filelow
            filelowd = sp3filelow
            filelowp = sp3filelow
            filelown = sp3filelow
            fileprolow = filelown
    else:
        filelowo = file.lower()[0:11] + "o"
        filelowd = file.lower()[0:11] + "d"
        filelowp = file.lower()[0:11] + "p"
        filelown = file.lower()[0:11] + "n"
        fileprolow = file.lower()[0:12]
        sp3filelow = filelown
    gzdfile = filelowd + ".gz"
    zdfile = filelowd + ".Z"
    gzofile = filelowo + ".gz"
    zofile = filelowo + ".Z"
    filebialowZ = fileprolow + ".Z"
    filebialowgz = fileprolow + ".gz"
    highrate_file = file.split('.tar')[0][:-1] + 'o'
    highrate_file_mgex = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"

    if os.path.exists(file[0:-2]) or os.path.exists(file[0:-3]) \
            or os.path.exists(filelowo) or os.path.exists(filelowd) \
            or os.path.exists(gzdfile) or os.path.exists(zdfile) \
            or os.path.exists(gzofile) or os.path.exists(zofile) \
            or os.path.exists(filelowp) or os.path.exists(filelown) \
            or os.path.exists(filebialowgz) or os.path.exists(filebialowZ) \
            or os.path.exists(sp3filelow) or os.path.exists(highrate_file) or os.path.exists(highrate_file_mgex) \
            or os.path.exists(file):
        return True
    # if 'EPH_M' in file:
    #     if os.path.exists(file.split('.')[0] + '.sp3'):
    #         return True
    # if 'CLK_M' in file:
    #     if os.path.exists(file.split('.')[0] + '.clk'):
    #         return True
    # if 'BIA_M' in file:
    #     if os.path.exists(file.split('.')[0] + '.bia'):
    #         return True
    else:
        return False



"""
    2022-03-27 :    判断操作平台，获取bin下格式转换程序    
                    by Chang Chuntao    -> Version : 1.00
    2022-09-16 :    更新索引                           
                    by Chang Chuntao    -> Version : 1.21
    2022-11-15 :    增加teqc                          
                    by Chang Chuntao    -> Version : 2.03
    2022-12-04 :    增加tgz解压
                    by Chang Chuntao    -> Version : 2.05
"""
tar = 'tar -xf '
if platform.system() == 'Windows':
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    unzip = os.path.join(dirname, 'bin', 'gzip.exe')
    unzip += " -d "
    unzip_tgz = 'tar -xvzf'
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx.exe')
    crx2rnx += " "
    teqc = os.path.join(dirname, 'bin', 'teqc.exe')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'bin', 'gfzrnx_win.exe')
    gfzrnx = gfzrnx_exe + ' '
else:
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx')
    crx2rnx += ' '
    unzip_tgz = 'tar -xvzf'
    uncompress = os.path.join(dirname, 'bin', 'uncompress')
    unzip = uncompress + ' '
    teqc = os.path.join(dirname, 'bin', 'teqc')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'bin', 'gfzrnx_linux')
    gfzrnx = gfzrnx_exe + ' '


def uncompresss(file):
    """
    2022-03-27 :    解压单个文件
                    by Chang Chuntao    -> Version : 1.00
    2022-11-15 :    支持CentOS
                    by Chang Chuntao    -> Version : 2.03
    2022-12-04 :    支持tgz解压/COD产品更名
                    by Chang Chuntao    -> Version : 2.05
    """
    if not os.path.isfile(file):
        return
    if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz" or file.split(".")[-1] == "tgz":
        if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz":
            try:
                cmd_list = [unzip[:-1], file]
                p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except:
                cmd = unzip + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            try:
                cmd_list = [unzip_tgz[:-1], file]
                p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except:
                cmd = unzip_tgz + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        PID = p.pid
        completely = True
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                line = line.decode('gbk')
                if 'x ' in line:
                    PrintGDD("更名：" + line[2:], "normal")
                if 'unexpected end of file' in line:
                    completely = False
            if PID == 0:
                break
        if completely:
            PrintGDD('压缩文件完好 -> ' + file + ', 已成功解压！', 'warning')
            if os.path.exists(file):
                os.remove(file)
            if file.split(".")[-1] == "tgz":
                if os.path.isfile(file):
                    os.remove(file)
            # if 'EPH_M' in file:
            #     if not os.path.isfile(file[:-7] + 'sp3'):
            #         os.rename(file[:-2], file[:-7] + 'sp3')
            #         PrintGDD("更名：" + file[:-7] + 'sp3', "normal")
            # if 'CLK_M' in file:
            #     if not os.path.isfile(file[:-7] + 'clk'):
            #         os.rename(file[:-2], file[:-7] + 'clk')
            #         PrintGDD("更名：" + file[:-7] + 'clk', "normal")
            # if 'BIA_M' in file:
            #     if not os.path.isfile(file[:-7] + 'bia'):
            #         os.rename(file[:-2], file[:-7] + 'bia')
            #         PrintGDD("更名：" + file[:-7] + 'bia', "normal")
        else:
            PrintGDD('压缩文件破损 -> ' + file + ', 未成功解压！', 'warning')


def crx2rnxs(file):
    """
    2022-03-27 : crx2rnx by Chang Chuntao -> Version : 1.00
    """
    if file[-3:-1].isdigit() and file[-1] == "d":
        cmd = crx2rnx + file
        os.system(cmd)


def crx2d(file):
    """
    2022-03-27 :    crx更名为d by Chang Chuntao -> Version : 1.00
    """
    if file.split(".")[-1] == "crx":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        if not os.path.isfile(filelow):
            os.rename(file, filelow)
            PrintGDD("更名：" + filelow, "normal")


def renamebrdm(file):
    """
    2022-03-27 :    BRDM长名更名为brdm短名 by Chang Chuntao -> Version : 1.00
    """
    filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
    if not os.path.isfile(filelow):
        os.rename(file, filelow)
        PrintGDD("更名：" + filelow, "normal")


def unzip_vlbi(path, ftpsite):
    """
    2022-03-27 :    解压vlbi文件 by Chang Chuntao -> Version : 1.00
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    dirs = os.listdir(path)
    for filename in dirs:
        if ftpsite[83:88] == filename[0:5] and filename.split(".")[-1] == "gz":
            uncompresss(filename)


def unzipfile(path, ftpsite):
    """
    2022.04.12 :    通过下载列表解压相应文件
                    by Chang Chuntao -> Version : 1.10
    2022.12.04 :    BRDC/BRDM/BRD4更名
                    by Chang Chuntao -> Version : 2.05
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    all_zip_file = []
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if os.path.exists(zipfilename) and zipfilename not in all_zip_file:
            uncompresss(zipfilename)
            all_zip_file.append(zipfilename)
    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-3:-1].isdigit() or filename.split(".")[-1] == "crx":
            if filename.split(".")[-1] == "crx" or filename[-1] == "d":
                PrintGDD("目录内含有crx文件，正在进行格式转换！", "normal")
                break
    for filename in dirs:
        if filename.split(".")[-1] == "crx":
            crx2d(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename[-1] == "d" and filename[-3:-1].isdigit():
            crx2rnxs(filename)
            time.sleep(0.1)
            os.remove(filename)

    dirs = os.listdir(path)
    for filename in dirs:
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDM":
            renamebrdm(filename)
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDC":
            renamebrdm(filename)
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRD4":
            renamebrdm(filename)
    os.chdir(nowdir)


def unzipfile_highrate_rinex2(path, ftpsite):
    """
    2022.11.15 : 通过下载列表解压高采样率文件并转换合并 by Chang Chuntao -> Version : 2.03
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    all_zip_file = []
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if not os.path.exists(zipfilename):
            continue
        if zipfilename in all_zip_file:
            continue
        all_zip_file.append(zipfilename)
        site_dir = os.path.join(nowdir, zipfilename.split('.')[0])
        merge_file = os.path.join(nowdir, zipfilename.split('.tar')[0][:-1]) + 'o'
        mkdir(site_dir, isdel=True)
        shutil.copy2(zipfilename, site_dir)
        os.chdir(site_dir)
        tar_cmd = tar + zipfilename
        os.system(tar_cmd)
        now_gfz_cmd = gfzrnx + '-finp '
        for root, dirs, files in os.walk(site_dir):
            for filename in files:
                if '.gz' not in filename:
                    continue
                now_gz_file = os.path.join(root, filename)
                now_crx_file = os.path.join(root, filename.split('.gz')[0])
                now_rnx_file = filename.split('.gz')[0][:-1] + 'o'

                now_zip_cmd = unzip + now_gz_file
                os.system(now_zip_cmd)

                now_crx2rnx_cmd = crx2rnx + now_crx_file
                os.system(now_crx2rnx_cmd)

                now_gfz_cmd += now_rnx_file + ' '
        now_gfz_cmd += '-fout ' + merge_file
        os.system(now_gfz_cmd)
    os.chdir(nowdir)


def unzipfile_highrate_rinex3(path, ftpsite):
    """
    2022.11.15 :    通过下载列表解压高采样率文件并转换合并
                    by Chang Chuntao -> Version : 2.03
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    PrintGDD("开始解压文件!", "normal")
    all_zip_file = []
    for ftp in ftpsite:
        zipfilename = str(ftp).split("/")[-1]
        if not os.path.exists(zipfilename):
            continue
        if zipfilename in all_zip_file:
            continue
        all_zip_file.append(zipfilename)
        site_dir = os.path.join(nowdir, zipfilename.split('.')[0])

        merge_file = os.path.join(nowdir,
                                  zipfilename.lower()[0:4] + zipfilename.lower()[16:20] + "." + zipfilename.lower()[
                                                                                                14:16] + "o")
        if os.path.exists(merge_file):
            continue
        mkdir(site_dir, isdel=True)
        shutil.copy2(zipfilename, site_dir)
        os.chdir(site_dir)
        tar_cmd = tar + zipfilename
        os.system(tar_cmd)
        now_gfz_cmd = gfzrnx + '-finp '

        for root, dirs, files in os.walk(site_dir):
            for filename in files:
                if '.gz' not in filename:
                    continue
                now_gz_file = os.path.join(root, filename)

                now_zip_cmd = unzip + now_gz_file
                os.system(now_zip_cmd)

                long_crx_file = os.path.join(root, filename.split('.gz')[0])
                now_crx_file = os.path.join(root,
                                            filename.lower()[0:4] + filename.lower()[16:20] + filename[19:23] + "." +
                                            filename.lower()[14:16] + "d")
                if not os.path.exists(long_crx_file):
                    continue
                if not os.path.isfile(now_crx_file):
                    os.rename(long_crx_file, now_crx_file)
                PrintGDD("更名：" + now_crx_file, "normal")
                now_rnx_file = os.path.join(root,
                                            filename.lower()[0:4] + filename.lower()[16:20] + filename[19:23] + "." +
                                            filename.lower()[14:16] + "o")

                move_rnx_file = filename.lower()[0:4] + filename.lower()[16:20] + filename[
                                                                                  19:23] + "." + filename.lower()[
                                                                                                 14:16] + "o"

                now_crx2rnx_cmd = crx2rnx + now_crx_file
                os.system(now_crx2rnx_cmd)
                shutil.copy2(now_rnx_file, site_dir)

                now_gfz_cmd += move_rnx_file + ' '
        now_gfz_cmd += ' -satsys GCE -fout ' + merge_file

        # print(now_gfz_cmd)
        os.system(now_gfz_cmd)
        EmptyFolder(site_dir)
        # os.rmdir(site_dir)
        os.chdir(nowdir)
