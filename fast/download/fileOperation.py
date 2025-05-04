
import os
import sys
import time
import platform
import subprocess
import datetime
# import distro
from fast.com.pub import printFast, mkdir, moveFile, EmptyFolder, exeCmd

def isFileInPath(file):  # 判断相关文件是否存在
    """
    2022-03-27 :    判断文件在本地是否存在
                    by Chang Chuntao    -> Version : 1.00
    2022-09-09 :    > 修正广播星历文件判定
                    by Chang Chuntao    -> Version : 1.20
    2022-11-15 :    > 增加高采样率判定
                    by Chang Chuntao    -> Version : 2.03
    2023-01-14 :    > 修正SP3 CLK判定
                    by Chang Chuntao    -> Version : 2.06
    2023-03-17 :    > 重写本地文件判定
                    by Chang Chuntao    -> Version : 2.08
    2023-06-30 :    + 增加高采样率文件判断
                    + 增加igu文件的判断
                    by Chang Chuntao    -> Version : 2.09
    """
    from fast.com.gnssTime import gnssTime2datetime, datetime2GnssTime, ReplaceTimeWildcard
    orifile = str(file).split(".")[0]
    ionfile = file
    projectFileLow = file
    filelowo = file
    filelowd = file
    filelowp = file
    filelown = file
    fileprolow = file
    rtrFile = file
    rtsFile = file
    projectFileUpper = file
    if len(orifile) > 9:
        ionfile = file.lower()[0:4] + 'g' + file.lower()[16:20] + "." + file.lower()[14:16] + "i"
        if '.SP3' in file or '.CLK' in file or '.OBX' in file or '.ERP' in file or '.ION' in file \
                or '.BIA' in file or '.TRO' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            proType = str(file).split(".")[-2].lower()
            if 'IGS0OPS' in file:
                if 'FIN' in file:
                    sp3_flag = 's'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType
                elif 'RAP' in file:
                    sp3_flag = 'r'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType
                elif 'ULT' in file:
                    sp3_flag = 'u'
                    hh = file[18:20]
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + '_' + hh + "." + proType
                else:
                    sp3_flag = 's'
                    projectFileLow = file.lower()[0:2] + sp3_flag + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + "." + proType

            elif 'COD0OPSRAP_' in file:
                projectFileLow = 'COD<GPSWD>.EPH_M'
                projectFileLow = ReplaceTimeWildcard(projectFileLow, specTime)
            else:
                projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + "." + proType
        elif '.SNX' in file:
            year = file.lower()[11:15]
            doy = file.lower()[15:18]
            specTime = gnssTime2datetime(year + " " + doy, "YearDoy")
            [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
            if '_SOL' in file:
                if 'IGS0OPSSNX' in file and '01D_01D_SOL' in file:
                    projectFileLow = file.lower()[0:3] + str(YearMonthDay[0])[:2] + 'P' + str(GPSWeekDay[0]) + str(
                        GPSWeekDay[1]) + ".snx"
                elif 'IGS0OPSSNX' in file and '07D_07D_SOL' in file:
                    projectFileLow = file.lower()[0:3] + str(YearMonthDay[0])[:2] + 'P' + str(GPSWeekDay[0]) + ".snx"
                else:
                    projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".snx"
            else:
                projectFileLow = file.lower()[0:3] + str(GPSWeekDay[0]) + str(GPSWeekDay[1]) + ".ssc"
        elif 'CH-OG-1-SST' in file:
            projectFileLow = str(file).replace('.zip', '') + '.rnx'
            filelowo = orifile[:27] + '.rnx'
        elif 'igu' in file and 'sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            hour = file[9:11]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSULT_<YYYY><DOY><nowHour>00_02D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
            projectFileUpper = str(projectFileUpper).replace('<nowHour>', hour)
        else:
            filelowo = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
            filelowd = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
            filelowp = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
            fileprolow = file.lower()[0:4] + file.lower()[16:20] + ".bia"
            rtrFile = str(rtrFile).replace('_S_', '_R_')
            rtrFile = str(rtrFile).replace('_R_', '_R_')
            rtsFile = str(rtsFile).replace('_R_', '_S_')
            rtsFile = str(rtsFile).replace('_S_', '_S_')
    else:
        if 'igs' in file and '.sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.sp3' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSRAP_<YYYY><DOY>0000_01D_15M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igs' in file and '.clk' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.clk' in file and '30s' not in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSRAP_<YYYY><DOY>0000_01D_05M_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'igr' in file and '.clk' in file and '30s' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'IGS0OPSFIN_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'COD' in file and '.EPH_M.Z' in file:
            gpsw = file[3:7]
            gpsd = file[7]
            specTime = gnssTime2datetime(gpsw + " " + gpsd, "GPSWeekDay")
            projectFileUpper = 'COD0OPSRAP_<YYYY><DOY>0000_01D_05M_ORB.SP3'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        elif 'codg' in file and 'i.Z' in file:
            doy = file[4:7]
            yyyy = str(2000 + int(file[9:11]))
            specTime = gnssTime2datetime(yyyy + " " + doy, "YearDoy")
            projectFileUpper = 'COD0OPSFIN_<YYYY><DOY>0000_01D_01H_GIM.INX'
            projectFileUpper = ReplaceTimeWildcard(projectFileUpper, specTime)
        filelowo = file.lower()[0:11] + "o"
        filelowd = file.lower()[0:11] + "d"
        filelowp = file.lower()[0:11] + "p"
        filelown = file.lower()[0:11] + "n"
        fileprolow = file.lower()[0:12]
    projectFileLowGz = projectFileLow + '.gz'
    projectFileLowZ = projectFileLow + '.Z'
    projectFileUpperGz = projectFileUpper + '.gz'
    projectFileUpperZ = projectFileUpper + '.Z'
    highrate_file = file.split('.tar')[0][:-1] + 'o'
    fileUnzip = str(file).replace('.' + file.split('.')[-1], '')
    highrate_file_mgex = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "o"
    filelowoZ = filelowo + '.Z'
    filelowogz = filelowo + '.gz'
    filelowdZ = filelowd + '.Z'
    filelowdgz = filelowd + '.gz'
    filelowdtar = filelowd + '.tar'
    filelowpZ = filelowp + '.Z'
    filelowpgz = filelowp + '.gz'
    filelownZ = filelown + '.Z'
    filelowngz = filelown + '.gz'
    if os.path.exists(file[0:-2]) or os.path.exists(file[0:-3]) \
            or os.path.exists(file) or os.path.exists(file.replace('05M', '15M')) or os.path.exists(projectFileLowZ) or os.path.exists(projectFileLowGz) \
            or os.path.exists(file.replace('15M', '05M')) or os.path.exists(highrate_file) or os.path.exists(highrate_file_mgex) or os.path.exists(filelowo) \
            or os.path.exists(filelowd) or os.path.exists(filelowp) or os.path.exists(filelown) \
            or os.path.exists(fileprolow) or os.path.exists(ionfile) or os.path.exists(projectFileLow) \
            or os.path.exists(fileUnzip) or os.path.exists(projectFileUpperGz) or os.path.exists(projectFileUpperZ) \
            or os.path.exists(projectFileUpper) or os.path.exists(filelowoZ) or os.path.exists(filelowogz)\
            or os.path.exists(filelowdZ) or os.path.exists(filelowdgz) or os.path.exists(filelowdtar) or os.path.exists(filelowpZ) \
            or os.path.exists(rtrFile) or os.path.exists(rtsFile) \
            or os.path.exists(filelowpgz) or os.path.exists(filelownZ) or os.path.exists(filelowngz):
        return True
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
    2023-03-18 :    增加zip解压
                    by Chang Chuntao    -> Version : 2.08
    2023-10-16 :    增加tar解压
                    by Chang Chuntao    -> Version : 3.00
"""
tar = 'tar -xf '

if platform.system() == 'Windows':
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.join(dirname, '..')
    unzip = os.path.join(dirname, 'bin', 'gzip.exe')
    unzip += " -d "
    unzip_tgz = 'tar -xvzf'
    unzip_zip = os.path.join(dirname, 'bin', 'unzip.exe') + ' '
    crx2rnx = os.path.join(dirname, 'bin', 'crx2rnx.exe')
    crx2rnx += " "
    teqc = os.path.join(dirname, 'bin', 'teqc.exe')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'bin', 'gfzrnx_win.exe')
    gfzrnx = gfzrnx_exe + ' '
    unzip_tar = 'tar -zxvf'
elif platform.system() == 'Darwin':
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        dirname = os.path.join(dirname, '..')
    crx2rnx = os.path.join(dirname, 'mac_bin', 'crx2rnx')
    crx2rnx += ' '
    unzip_tgz = 'tar -xvzf '
    uncompress = os.path.join(dirname, 'mac_bin', 'gunzip')
    unzip_zip = os.path.join(dirname, 'mac_bin', 'gunzip') + ' '
    unzip = uncompress + ' '
    teqc = os.path.join(dirname, 'mac_bin', 'teqc')
    teqc += ' '
    gfzrnx_exe = os.path.join(dirname, 'mac_bin', 'gfzrnx')
    gfzrnx = gfzrnx_exe + ' '
    unzip_tar = 'tar -xvf'
else:
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
    crx2rnx = os.path.join(binDir, 'crx2rnx')
    crx2rnx += ' '
    unzip_tgz = 'tar -xvzf '
    uncompress = os.path.join(binDir, 'uncompress')
    unzip_zip = os.path.join(binDir, 'unzip') + ' '
    unzip = uncompress + ' '
    teqc = os.path.join(binDir, 'teqc')
    teqc += ' '
    gfzrnx_exe = os.path.join(binDir, 'gfzrnx_linux')
    gfzrnx = gfzrnx_exe + ' '
    unzip_tar = 'tar -xvf'


def uncompressFile(file):
    """
    2022-03-27 :    解压单个文件
                    by Chang Chuntao    -> Version : 1.00
    2022-11-15 :    支持CentOS
                    by Chang Chuntao    -> Version : 2.03
    2022-12-04 :    支持tgz解压/COD产品更名
                    by Chang Chuntao    -> Version : 2.05
    """
    if not os.path.isfile(file):
        return None
    if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz" or file.split(".")[-1] == "tgz" or\
            file.split(".")[-1] == "ZIP" or file.split(".")[-1] == "zip":
        if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz":
            try:
                cmd_list = [unzip[:-1], file]
                p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except:
                cmd = unzip + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif file.split(".")[-1] == "ZIP" or file.split(".")[-1] == "zip":
            if platform.system() == 'Windows':
                cmd = unzip_zip + file
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                try:
                    cmd_list = [unzip_zip[:-1], file]
                    p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except:
                    cmd = unzip_zip + file
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
                    printFast("rename:" + line[2:], "normal")
                if 'unexpected end of file' in line:
                    completely = False
            if PID == 0:
                break
        if completely:
            # printFast('压缩文件完好 -> ' + file + ', 已成功解压！', 'warning')
            if os.path.exists(file):
                os.remove(file)
            if file.split(".")[-1] == "tgz":
                if os.path.isfile(file):
                    os.remove(file)
            return file
        else:
            printFast('This compressed file is corrupted -> ' + file, 'warning')
            os.remove(file)
            return None


def crx2rnxs(file):
    """
    2022-03-27 : crx2rnx by Chang Chuntao -> Version : 1.00
    """
    if file[-3:-1].isdigit() and file[-1] == "d":
        ofile = file[:-1] + 'o'
        if not os.path.isfile(ofile):
            cmd = crx2rnx + file
            exeCmd(cmd)


def crx2d(file):
    """
    2022-03-27 :    crx更名为d by Chang Chuntao -> Version : 1.00
    """
    if file.split(".")[-1] == "crx":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        if not os.path.isfile(filelow):
            os.rename(file, filelow)
            printFast("Rename - " + filelow, "normal")
    return filelow


def renamebrdm(file):
    """
    2022-03-27 :    BRDM长名更名为brdm短名 by Chang Chuntao -> Version : 1.00
    """
    filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
    if not os.path.isfile(filelow):
        os.rename(file, filelow)
        printFast("Rename - " + filelow, "normal")


def renameMeteorological(file):
    """解压完成
    2023-12-18 :    长名更名为brdm短名 by Chang Chuntao -> Version : 1.00
    """
    filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "m"
    if not os.path.isfile(filelow):
        os.rename(file, filelow)
        printFast("Rename - " + filelow, "normal")


def unzip_vlbi(path, ftpsite):
    """
    2022-03-27 :    解压vlbi文件 by Chang Chuntao -> Version : 1.00
    """
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    printFast("开始解压文件 / Start extracting the file.", "normal")
    dirs = os.listdir(path)
    for filename in dirs:
        if ftpsite[83:88] == filename[0:5] and filename.split(".")[-1] == "gz":
            uncompressFile(filename)


def uncompress_ym(successDownFileList):
    '''
    2022-04-12 : 通过下载列表解压文件(年月) by Chang Chuntao  -> Version : 1.10
    '''
    isuncpmress = "y"
    ftpsite = []
    # for u in url:
    #     ftpsite.append(u)
    for f in successDownFileList:
        if str(f).split(".")[-1] == "gz" or str(f).split(".")[-1] == "Z":
            printFast("如需解压直接回车，若无需解压输入任意字符回车！ / Enter to proceed, otherwise cancel!", "input")
            isuncpmress = input("     ")
            break
    if isuncpmress == "":
        unzipfile(os.getcwd(), ftpsite)


def uncompress_highrate_rinex(successDownFileList):
    '''
    2022-11-15 : 通过下载列表解压GRE_IGS_01S文件 by Chang Chuntao  -> Version : 2.03
    '''
    # ftpsite = []
    # for i in range(len(urllist)):
    #     for j in range(len(urllist[i])):
    #         ftpsite.append(urllist[i][j])
    
    printFast("如需解压直接回车，若无需解压输入任意字符回车！ / Enter to proceed, otherwise cancel!", "input")
    isuncpmress = input("     ")
    if isuncpmress == "":
        try:
            if len(successDownFileList) == 0:
                return
            if '.crx.gz' in successDownFileList[0]:
                unzipfile_highrate_rinex_hourly(os.getcwd(), successDownFileList)
            else:
                unzipfile_highrate_rinex(os.getcwd(), successDownFileList)
        except:
            pass


def unzipfile(path, successDownFileList):
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
    printFast("开始解压文件 / Start extracting the file!", "normal")
    extractedFileList = []
    for file in successDownFileList:
        successUnzip = uncompressFile(file)
        if successUnzip is not None:
            for zipFormat in ['.Z', '.gz', '.ZIP', '.gz', '.tgz', '.zip']:
                successUnzip = successUnzip.replace(zipFormat, '')
            extractedFileList.append(successUnzip)
    if len(extractedFileList) > 0:
        printFast("解压完成 / Extraction completed!", "normal")
    for filename in extractedFileList:
        if filename[-3:-1].isdigit() or filename.split(".")[-1] == "crx":
            if filename.split(".")[-1] == "crx" or filename[-1] == "d":
                printFast("crx -> rnx", "normal")
                break
    dFileList = []
    for filename in extractedFileList:
        if filename.split(".")[-1] == "crx":
            dFile = crx2d(filename)
            dFileList.append(dFile)
        if filename[-1] == "d" and filename[-3:-1].isdigit():
            dFileList.append(filename)

    dirs = os.listdir(path)
    for filename in dFileList:
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
        if '_MM.rnx' in filename:
            renameMeteorological(filename)

    os.chdir(nowdir)
    return extractedFileList

def char_to_num(char):
    return ord(char) - 97

def convertNum2ab(number):
    """
    将数字转换为对应的字母
    :param number: 输入的数字
    :return: 对应的字母
    """
    try:
        number = int(number)
    except:
        return None
    if not isinstance(number, int) or number < 0:
        return None
    return chr(ord('a') + number)

def unzipfile_highrate_rinex(path, successDownFileList):
    """
    2022.11.15 :    通过下载列表解压高采样率文件并转换合并
                    by Chang Chuntao -> Version : 2.03
    2023.10.16 :    条件更新
                    by Chang Chuntao -> Version : 3.00
    """
    from fast.com.pub import  mkdir, moveFile, getFileInWalkPath, exeCmd
    from fast.com.pub import printFast
    nowdir = os.getcwd()
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    printFast("开始解压高采样文件 / Start extracting the highrate file!", "normal")
    siteList = []

    for ftp in successDownFileList:
        zipfilename = os.path.basename(ftp)
        if os.path.isfile(zipfilename):
            siteList.append(zipfilename)
    for siteTar in siteList:
        try:
            printFast("解压小时文件并转为rnx格式 / Extract and convert file to RINEX format.", "normal")
            if len(siteTar) > 20:
                stn = siteTar[-42:-38].lower()
                yy = siteTar[-28:-26]
                doy = siteTar[-26:-23]
                oFile = stn + doy + '0.' + yy + 'o'
            else:
                oFile = siteTar.split('.')[0] + '.' + siteTar.split('.')[1][:-1] + 'o'
            oFile = os.path.join(path, oFile)
            siteTarAbs = os.path.join(path, siteTar)
            siteName = siteTar.split('.')[0]
            sitePath = os.path.join(path, siteName)
            mkdir(sitePath, isdel=True)
            os.chdir(sitePath)
            exeCmd(unzip_tar + ' ' + siteTarAbs, printLog=False)
            allGzFile = getFileInWalkPath(sitePath, needStr='.gz', baseName=False)
            now_gfz_cmd = gfzrnx + '-finp '
            oFileList = {}
            for gzFie in allGzFile:
                exeCmd(unzip + ' ' + gzFie, printLog=False, printCmd=False)
                crxFile = gzFie.replace('.gz', '')
                if '.crx' == crxFile[-4:]:
                    stn = crxFile[-38:-34].lower()
                    yy = crxFile[-24:-22]
                    doy = crxFile[-22:-19]
                    hh = crxFile[-19:-17]
                    hhab = convertNum2ab(hh)
                    mm = crxFile[-17:-15]
                    nowtimeFlag = datetime.datetime(2023,1,1,int(hh), int(mm))
                    dFile = stn + doy + hhab + mm + '.' + yy + 'd'
                    if not os.path.isfile(crxFile):
                        continue
                    moveFile(crxFile, dFile)
                elif 'd' == crxFile[-1]:
                    hh = char_to_num(crxFile[-7])
                    mm = crxFile[-6:-4]
                    nowtimeFlag = datetime.datetime(2023,1,1,int(hh), int(mm))
                    dFile = crxFile
                else:
                    continue
                crx2rnxs(dFile)
                hourOfile = dFile[:-1] + 'o'
                now_gfz_cmd += hourOfile + ' '
                os.remove(dFile)
                oFileList[os.path.join(sitePath, hourOfile)] = nowtimeFlag
                # oFileList.append(os.path.join(sitePath, hourOfile))
            # os.chdir(path)
            oFileList = dict(sorted(oFileList.items(), key=lambda x: x[1]))
            printFast('Merging files -> ' + oFile, 'normal')
            now_gfz_cmd += ' -fout ' + oFile
            # print(now_gfz_cmd)
            # exeCmd(now_gfz_cmd, printLog=True, printCmd=True)
            mergeOfile(list(oFileList), oFile)
        except:
            pass
    os.chdir(path)

def unzipfile_highrate_rinex_hourly(path, successDownFileList):
    """
    2022.11.15 :    通过下载列表解压高采样率文件并转换合并
                    by Chang Chuntao -> Version : 2.03
    2023.10.16 :    条件更新
                    by Chang Chuntao -> Version : 3.00
    """
    from fast.com.pub import  mkdir, moveFile, getFileInWalkPath, exeCmd, copyFile
    if len(path) == 0:
        path = os.getcwd()
    os.chdir(path)
    printFast("开始解压高采样文件 / Start extracting the highrate file!", "normal")
    siteList = []

    for ftp in successDownFileList:
        zipfilename = os.path.basename(ftp)
        if os.path.isfile(zipfilename):
            siteList.append(zipfilename)
    oFileList = {}
    for siteTar in siteList:
        try:
            printFast("解压小时文件并转为rnx格式 / Extract and convert file to RINEX format.", "normal")
            if len(siteTar) > 20:
                stn = siteTar[-41:-37].lower()
                yy = siteTar[-27:-25]
                doy = siteTar[-25:-22]
                oFile = stn + doy + '0.' + yy + 'o'
            else:
                oFile = siteTar.split('.')[0] + '.' + siteTar.split('.')[1][:-1] + 'o'
            oFile = os.path.join(path, oFile)
            siteTarAbs = os.path.join(path, siteTar)
            siteName = siteTar.split('.')[0][:19]
            sitePath = os.path.join(path, siteName)
            if not os.path.isdir(sitePath):
                mkdir(sitePath, isdel=False)
            os.chdir(sitePath)
            copyFile(siteTarAbs, sitePath)
            os.system(unzip + siteTar)
            crxFile = siteTar.replace('.gz', '')
            stn = crxFile[-38:-34].lower()
            yy = crxFile[-24:-22]
            doy = crxFile[-22:-19]
            hh = crxFile[-19:-17]
            mm = crxFile[-17:-15]
            hhab = convertNum2ab(hh)
            nowtimeFlag = datetime.datetime(2000+int(yy),1,1,int(hh), int(mm)) + datetime.timedelta(days=int(doy)-1)
            dFile = stn + doy + hhab + mm + '.' + yy + 'd'
            moveFile(crxFile, dFile)
            crx2rnxs(dFile)
            hourOfile = dFile[:-1] + 'o'
            if oFile not in oFileList:
                oFileList[oFile] = {}
            os.remove(dFile)
            oFileList[oFile][os.path.join(sitePath, hourOfile)] = nowtimeFlag
        except:
            pass
    
    for siteTar in siteList:
        siteTarAbs = os.path.join(path, siteTar)
        os.remove(siteTarAbs)
    for oFile in oFileList:
        printFast('Merging files -> ' + oFile, 'normal')
        oFileList1Sat = dict(sorted(oFileList[oFile].items(), key=lambda x: x[1]))
        mergeOfile(list(oFileList1Sat), oFile)
    os.chdir(path)


def mergeOfile(oFileList, outFile):
    firstFile = True
    outFileOpen = open(outFile, 'w+')
    for oFile in oFileList:
        printFast(oFile + ' >> ' + outFile, 'normal')
        oFileOpen = open(oFile, 'r+')
        oFileLines = oFileOpen.readlines()
        if firstFile:
            firstFile = False
            outFileOpen.writelines(oFileLines)
        else:
            for lineIndex in range(len(oFileLines)):
                line = oFileLines[lineIndex]
                if 'END OF HEADER' in line:
                    break
            outFileOpen.writelines(oFileLines[lineIndex+1:])


def uncompressFileArg(path, successDownFileList):
    """
    2022.04.12 :    传入需解压的文件至unzipfile
                    by Chang Chuntao -> Version : 1.10
    2022.11.15 :    新增GRE_IGS_01S判断
                    by Chang Chuntao -> Version : 2.03
    """
    extractedFileList = []
    highrate_rinex_hourlyList = []
    highrate_rinex_hourly = []
    unzipfileList = []
    for ff in successDownFileList:
        if '_15M_01S_MO.crx.gz' in ff:
            highrate_rinex_hourlyList.append(ff)
        elif '0000_01D_01S_MO.crx.tar' in ff:
            highrate_rinex_hourly.append(ff)
        else:
            unzipfileList.append(ff)
    if len(highrate_rinex_hourlyList) > 0:
        unzipfile_highrate_rinex_hourly(path, highrate_rinex_hourlyList)
    if len(highrate_rinex_hourly) > 0:
        unzipfile_highrate_rinex(path, highrate_rinex_hourly)
    extractedFileList = unzipfile(path, unzipfileList)
    return extractedFileList

def renamePro(successDownFileList, rename3char):
    from fast.com.gnssTime import doy2gpswd
    from fast.com.pub import moveFile
    
    for f in successDownFileList:
        if 'ULT' in f or 'ULA' in f:
            continue
        if len(f) != 38:
            continue
        inPro = False
        for proType in ['SP3', 'CLK', 'BIA', 'DCB', 'ERP', 'SNX']:
            if proType in f:
                year = int(f.lower()[11:15])
                doy = int(f.lower()[15:18])
                gpsw, gpswd = doy2gpswd(year, doy)
                shortName = rename3char.lower() + str(gpsw) + str(gpswd) + '.' + proType.lower()
                moveFile(f, shortName)
                inPro = True
            if inPro:
                continue


