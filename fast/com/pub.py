# -*- coding: utf-8 -*-
# pub            : pub for FAST
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2022.03.27 - Version 1.00
# Latest Version : 2023-09-26 - Version 3.00



_version = {    '1.00':     '2022-03-27', 
                '1.10':     '2022-04-12',
                '1.11':     '2022-04-22', 
                '1.12':     '2022-04-30', 
                '1.13':     '2022-05-24', 
                '1.14':     '2022-05-31', 
                '1.15':     '2022-07-03', 
                '1.16':     '2022-07-13', 
                '1.17':     '2022-07-22', 
                '1.18':     '2022-07-28', 
                '1.19':     '2022-08-04', 
                '1.20':     '2022-09-11', 
                '1.21':     '2022-09-16', 
                '1.22':     '2022-09-20', 
                '1.23':     '2022-09-28', 
                '1.24':     '2022-10-10', 
                '1.25':     '2022-11-02',
                '2.01':     '2022-11-09', 
                '2.02':     '2022-11-10', 
                '2.03':     '2022-11-15', 
                '2.04':     '2022-12-02', 
                '2.05':     '2022-12-04', 
                '2.06':     '2023-01-14', 
                '2.07':     '2023-02-10', 
                '2.08':     '2023-03-17', 
                '2.09':     '2023-06-30', 
                '2.10':     '2023-08-11', 
                '2.11':     '2023-09-20',
                '3.00.01':  '2024-01-09',
                '3.00.02':  '2024-05-22',
                '3.00.03':  '2025-05-05',
            }

lastVersion = list(_version)[-1]
lastVersionTime = _version[lastVersion]

gnss_type = [["BRDC", ["GPS_brdc", "GCRE_brdc", "GCRE_CNAV_brdm", "GCRE_CNAV_brd4"]],  # 1 BRDC

             ["SP3", ["GPS_IGS_sp3", "GPS_IGR_sp3", "GPS_IGU_sp3", "GPS_GRG_sp3",  # 2 SP3

                      "GCRE_WHU_F_sp3", "GCRE_WHU_R_sp3", "GCRE_WHU_U_sp3",
                      "GCRE_WHU_H_sp3",  "GCRE_WHU_RTS_sp3", "GCRE_SHA_F_sp3",
                      "GCRE_COD_F_sp3",  "GCRE_GRG_F_sp3", 'GCRE_GFZ_R_sp3',
                      "GCRE_IAC_F_sp3",
                      "GRE_GFZ_F_sp3",  'GRE_COD_R_sp3', 'GLO_IGL_F_sp3',
                      'GRE_JAX_U_sp3', 'CEG_GRG_U_sp3']],

             ["CLK", ["GPS_IGS_clk", "GPS_IGR_clk", "GPS_GRG_clk", "GPS_IGS_clk_30s",  # 3 CLK

                      "GCRE_WHU_F_clk", "GCRE_WHU_R_clk", "GCRE_WHU_U_clk",
                      "GCRE_WHU_U_clk_30s", "GCRE_WHU_RTS_clk", "GCRE_SHA_F_clk",
                      'GCRE_COD_F_clk', "GCRE_GRG_F_clk", 'GCRE_GFZ_R_clk',
                      "GCRE_IAC_F_clk",
                      'GRE_GFZ_F_clk', 'GRE_COD_R_clk', 'GLO_IGL_F_clk',
                      'GRE_COD_F_clk_30s', 'GRE_JAX_U_clk_30s', 'CEG_GRG_U_clk']],

             ["OBS", ["GPS_IGS_obs", "GPS_USA_cors", "GPS_HK_cors", 
                      "GPS_SIRGAS",
                      
                        "GCRE_MGEX_obs", "GCRE_MGEX_obs_01s",
                        "GCRE_HK_cors", "GCRE_EU_cors", "GCRE_AU_cors",
                        "GRE_MGEX_obs_01s", "GCRE_SIRGAS"]],

             ["ERP", ["IGS_F_erp", "IGS_R_erp", "WHU_F_erp",
                      "COD_F_erp", "WHU_U_erp", "GFZ_R_erp",
                      'COD_R_erp', "WHU_H_erp"]],  # 5 ERP

             ["BIA_DCB_OBX", ["GPS_COD_F_osb",  "GE_GRG_F_osb", "GRE_COD_R_osb",
                              'GCRE_WHU_F_osb', "GCRE_WHU_R_osb", "GCRE_WHU_R_abs",
                              "GCRE_COD_F_osb", "GCRE_GFZ_R_osb", "GCRE_CAS_R_osb",   
                              "GCRE_WHU_U_osb", "GCRE_WHU_RTS_osb",  # 6 BIA_DCB_OBX

                              "GPS_COD_dcb", "GCRE_CAS_R_dcb",
                              "P1C1", "P1P2", "P2C2",

                              "GPS_COD_F_obx", "GPS_GRG_F_obx",
                              "GCRE_WHU_F_obx", 'GCRE_WHU_R_obx', 'GCRE_WHU_U_obx',
                              "GCRE_COD_F_obx", "GCRE_GFZ_R_obx"]],

             ["ION_TRO", ["IGSG_ion", "IGRG_ion", "WHUG_ion",
                          "WURG_ion", "CODG_ion", "CORG_ion",
                          "UQRG_ion", "UPRG_ion", "JPLG_ion",
                          "JPRG_ion", "CASG_ion", "CARG_ion",
                          "ESAG_ion", "ESRG_ion",

                          "IGS_trop", "COD_trop", "JPL_trop",
                          "GRID_1x1_VMF3", "GRID_2.5x2_VMF1", "GRID_5x5_VMF3",
                          "vmf1grd", "Meteorological"]],

             ["SINEX", ["IGS_day_snx", "IGS_week_snx",
                        "IVS_week_snx", "ILS_week_snx", "IDS_week_snx",
                        'IGS_crd_snx', 'COD_sol_snx', 'ESA_sol_snx',
                        'GFZ_sol_snx', 'GRG_sol_snx', 'NGS_sol_snx',
                        'SIO_sol_snx']],  # 8 SINEX

             ["CNES_AR", ["CNES_post", "CNES_realtime", "CNES_bia", "CNES_backup"]],  # 9 CNES_AR

             ["Time_Series", ["IGS14_TS_ENU", "IGS14_TS_XYZ", "Series_TS_Plot"]],  # 10 Time_Series

             ["Velocity_Fields", ["IGS14_Venu", "IGS08_Venu", "PLATE_Venu"]],  # 11 Velocity_Fields

             ["SLR", ["HY_SLR", "GRACE_SLR", "BEIDOU_SLR"]],  # 12 SLR

            #  ["LEO", ['GRACE_dat', 'GRACE_rnxapp', 'GRACE_fo_dat',  # 13 LEO
            #           'GRACE_fo1_sp3', 'GRACE_fo2_sp3', 'CHAMP_rnx',
            #           'CHAMP_sp3', 'SWARM_rnx', 'SWARM_sp3',

            #           'C1_L1a_leoAtt', 'C1_L1a_opnGps', 'C1_L1a_podCrx',
            #           'C1_L1b_atmPhs', 'C1_L1b_gpsBit', 'C1_L1b_ionPhs',
            #           'C1_L1b_leoClk', 'C1_L1b_leoOrb', 'C1_L1b_podTec',
            #           'C1_L1b_scnLv1',
            #           'C2_L1a_leoAtt', 'C2_L1a_opnGps', 'C2_L1a_podCrx',
            #           'C2_L1b_conPhs', 'C2_L1b_leoOrb', 'C2_L1b_podTc2']],

             ["LEO", ['GRACE_dat', 'GRACE_rnxapp', 
                      'GRACE_fo_dat',  'GRACE_fo1_sp3', 'GRACE_fo2_sp3', 
                      'CHAMP_rnx', 'CHAMP_sp3', 
                      'SWARM_A_rnx', 'SWARM_B_rnx', 'SWARM_C_rnx',
                      'SWARM_A_sp3', 'SWARM_B_sp3', 'SWARM_C_sp3',
                      'COSMIC_1_att', 'COSMIC_1_crx', 'COSMIC_1_orb',
                      'COSMIC_2_att', 'COSMIC_2_crx', 'COSMIC_2_orb']],

             ['PANDA', ['Panda_jpleph_de405', 'Panda_poleut1', 'Panda_EGM',  # 14 PANDA
                        'Panda_oceanload', 'Panda_oceantide', 'Panda_utcdif',
                        'Panda_antnam', 'Panda_svnav', 'Panda_nutabl',
                        'Panda_ut1tid', 'Panda_leap_sec', 'MGEX_IGS14_atx',
                        "MGEX_IGS20_atx", "SW_EOP",'Panda_gpsrapid',
                        'EOP_C04']],

             ['GAMIT', ['Gamit_pmu_bull', 'Gamit_ut1usno', 'Gamit_poleusno',  # 15 GAMIT
                        'Gamit_dcb_dat', 'Gamit_soltab', 'Gamit_luntab',
                        'Gamit_leap_sec', 'Gamit_nutabl', 'Gamit_antmod',
                        'Gamit_svnav', 'Gamit_rcvant', 'Gamit_nbody',
                        'IGS_hfile']]
             ]

# 2022-03-27 :  索引方式改为type:
#               yd_type -> year doy / no_type -> none /  yds_type -> year doy site / ym_type -> year month / s_type -> site
#               by Chang Chuntao -> Version : 2.01

yd_type = []
no_type = []
yds_type = []
ym_type = []
s_type = []
ydsh_type = []
ydh_type = []

for gs_list in gnss_type:
    if gs_list[0] in ['BRDC', "SP3", "CLK", "ERP", "CNES_AR", "SLR", "LEO"]:
        for gs_type in gs_list[1]:
            if gs_type == 'GRACE_rnxapp':
                no_type.append(gs_type)
            elif gs_type in ["GCRE_WHU_U_sp3", "GCRE_WHU_U_clk", "WHU_U_erp",
                             "WHU_H_erp", "GRE_JAX_U_sp3", "GRE_JAX_U_clk_30s", 'CEG_GRG_U_clk', 
                             'CEG_GRG_U_sp3', 'GCRE_WHU_U_clk_30s']:
                ydh_type.append(gs_type)
            else:
                yd_type.append(gs_type)

    elif gs_list[0] == 'ION_TRO':
        for gs_type in gs_list[1]:
            if gs_type == 'IGS_zpd' or gs_type == 'Meteorological':
                yds_type.append(gs_type)
            else:
                yd_type.append(gs_type)

    elif gs_list[0] == 'BIA_DCB_OBX':
        for gs_type in gs_list[1]:
            if gs_type in ["P1C1", "P1P2", "P2C2"]:
                ym_type.append(gs_type)
            elif gs_type in ["GCRE_WHU_U_obx", "GCRE_WHU_U_osb"]:
                ydh_type.append(gs_type)
            else:
                yd_type.append(gs_type)

    elif gs_list[0] == 'OBS':
        for gs_type in gs_list[1]:
            if gs_type in ["GCRE_MGEX_obs_01s"]:
                ydsh_type.append(gs_type)
            else:
                yds_type.append(gs_type)

    elif gs_list[0] == 'SINEX':
        for gs_type in gs_list[1]:
            if gs_type == 'IVS_week_snx':
                ym_type.append(gs_type)
            else:
                yd_type.append(gs_type)

    elif gs_list[0] == 'Time_Series':
        for gs_type in gs_list[1]:
            s_type.append(gs_type)

    elif gs_list[0] in ["Velocity_Fields", 'PANDA']:
        for gs_type in gs_list[1]:
            no_type.append(gs_type)

    elif gs_list[0] in ["Velocity_Fields", 'GAMIT']:
        for gs_type in gs_list[1]:
            if gs_type == 'IGS_hfile':
                yd_type.append(gs_type)
            else:
                no_type.append(gs_type)

# 2022-03-27 : 每个二级目录的个数 by Chang Chuntao -> Version : 1.00
objnum = []
for sub_type in gnss_type:
    objnum.append(len(sub_type[1]))

def isSupportedDatatype(datatype):
    """
    2022-03-27 : 判断数据类型是否支持 by Chang Chuntao -> Version : 1.00
    """
    for gt in gnss_type:
        if datatype in gt[1]:
            return True
        else:
            continue
    return False


#
def getobj(datatype):
    """
    2022-03-27 : 获取数据类型在gnss_type中的索引位置 by Chang Chuntao -> Version : 1.00
    """
    d1 = 0
    for gt in gnss_type:
        d2 = 0
        for dt in gt[1]:
            d2 += 0
            if datatype == dt:
                return d1, d2
        d1 += 1


#############################Panda_print##############################
def printFast(string, printtype):
    """
    2022-03-27 : * 屏幕打印样式     by Chang Chuntao -> Version : 1.00
    2022-04-30 : * 新增nothing    by Chang Chuntao -> Version : 1.12
    """
    if printtype == "input":
        print("  - " + string)
    elif printtype == "normal":
        print("  * " + string)
    elif printtype == "fail":
        print("  x " + string)
    elif printtype == "warning":
        print("  # " + string)
    elif printtype == "important":
        print(" ***" + string)
    elif printtype == "nothing":
        print("    " + string)

def printPanda(istring, logFile=None, onlyLog = False):
    import datetime
    nowtimeStrft = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out_string = '[' + nowtimeStrft + ']: ' + str(istring)
    if not onlyLog:
        print(out_string)
    if logFile is not None:
        logfile_open = open(logFile, 'a+',encoding="utf-8")
        logfile_open.write(out_string + '\n')
        logfile_open.close()
#############################Panda_print##############################


#############################File_Folder##############################
def mkdir(path, isdel=False):
    # Creating a folder
    # If the folder exists and isdel is true, the folder is emptied
    import os
    path = path.strip()
    path = path.rstrip('\\')
    if path == '':
        path = '..'
    isExists = os.path.exists(path)
    if not isExists:
        printPanda(path + ' created successfully')
        os.makedirs(path)
        return True
    else:
        if isdel: EmptyFolder(path)
        printPanda(path + ' created successfully')
        return False

def EmptyFolder(folder):
    # Empty one folder but do not delete the folder
    import os
    import shutil
    # check whether the input folder exists
    if not os.path.isdir(folder):
        return
    for path in os.listdir(folder):
        path = os.path.join(folder, path)
        if os.path.isfile(path):  # regular file
            os.remove(path)
        elif os.path.isdir(path):  # existing directory
            shutil.rmtree(path)
    return None

def getFileInPath(path, needStr = None, baseName = False):
    import os
    all_file = []
    for f in os.listdir(path):
        f_name = os.path.join(path, f)
        if needStr is None:
            if baseName:
                all_file.append(f)
            else:
                all_file.append(f_name)
        else:
            inFile = True
            for nStr in needStr:
                if nStr not in f:
                    inFile = False
                    break
            if inFile:
                if baseName:
                    all_file.append(f)
                else:
                    all_file.append(f_name)
    return all_file

def getFileInWalkPath(path, needStr = None, baseName = False):
    import os
    all_file = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if needStr is None:
                if baseName:
                    all_file.append(filename)
                else:
                    all_file.append(os.path.join(root, filename))
            else:
                inFile = True
                for nStr in needStr:
                    if nStr not in filename:
                        inFile = False
                        break
                if inFile:
                    if baseName:
                        all_file.append(filename)
                    else:
                        all_file.append(os.path.join(root, filename))
    return all_file

def copyFolder(oldFolder, nowFolder):
    import os
    import shutil
    if os.path.isdir(nowFolder):
        shutil.rmtree(nowFolder)
    shutil.copytree(oldFolder, nowFolder)
    
def modifyFile(file, lineStr, lineNum = None, lineStrFlag = None):
    fileOpen = open(file, 'r+')
    fileLines = fileOpen.readlines()
    fileOpen.close()
    if lineNum is None and lineStrFlag is None:
        raise IOError('LineNum or lineStrFlag is not passed to the function!')
    elif lineNum is not None:
        fileLines[lineNum - 1] = lineStr + '\n'
    elif lineStrFlag is not None:
        for lineNumInFile in range(len(fileLines)):
            if lineStrFlag in fileLines[lineNumInFile]:
                fileLines[lineNumInFile] = lineStr + '\n'
    fileWrite = open(file, 'w+')
    fileWrite.writelines(fileLines)
    fileWrite.close()

# 获取文件大小（可直接嵌入工程使用）
# input:文件路径
# output：文件大小,单位
def getFileSize(filePath, unit = 'M'):
    # B K M G
    import os
    fsize = os.path.getsize(filePath)	# 返回的是字节大小
    '''
    为了更好地显示,应该时刻保持显示一定整数形式,即单位自适应
    '''
    if unit == 'B':
        return fsize
    elif unit == 'K':
        return fsize / 1024
    elif unit == 'M':
        return fsize / 1024 / 1024
    elif unit == 'G':
        return fsize / 1024 / 1024 / 1024
    elif unit == 'T':
        return fsize / 1024 / 1024 / 1024 / 1024

#############################File_Folder##############################


###############################Run_Exe################################
def SetPathEnv(exebin):
    # Get related software directories based on main executable file, and set PATH environment variable
    import os
    import platform
    import stat

    # Add directories contains executable files to PATH environment variable
    pathenv = exebin + os.pathsep + os.getenv('PATH')  # notice, path separator
    os.putenv('PATH', pathenv)
    if platform.system() not in ['Windows']:
        for binfile in os.listdir(exebin):
            binfile = os.path.join(exebin, binfile)
            if os.path.isfile(binfile):
                os.chmod(binfile, os.stat(binfile).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return

def mean(numbers):
    if len(numbers) == 0:
        return 0
    # 计算列表的总和
    total = sum(numbers)
    return total / len(numbers)

def rms(numbers):
    import math
    if len(numbers) == 0:
        return 0
    squared = [x ** 2 for x in numbers]
    mean_squared = mean(squared)
    return math.sqrt(mean_squared)

# Use the shell to perform command line, return standard output, standard error, return code
def exeCmd(args, logFile = None, printLog = True, printCmd = True, addTime = True):
    'Use the shell to perform command line, return standard output, standard error, return code'
    import subprocess
    import platform
    if printCmd:
        printPanda('=== Execute command: %s ===' % args, logFile)
    lineList = []
    if platform.system() == 'Windows':
        st = subprocess.STARTUPINFO()
        st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,startupinfo=st)
        PID = p.pid
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                line = line.decode('gbk')
                lineList.append(line)
                if printLog:
                    if addTime:
                        printPanda(line, logFile)
                    else:
                        print(line)
            if PID == 0:
                break
    else:
        process = subprocess.Popen(args, shell=True,stdout=subprocess.PIPE)
        PID = process.pid
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                try:
                    line = line.decode('gbk')
                except:
                    line = str(line)
                
                lineList.append(line)
                if printLog:
                    if addTime:
                        printPanda(line, logFile)
                    else:
                        print(line)
            if PID == 0:
                break
    return lineList

def killExe(exe):
    import os
    import psutil
    mypid = os.getpid()
    for proc in psutil.process_iter():
        if mypid != proc.pid:
            if exe in proc.name():
                printPanda(exe + ' has been killed.')
                proc.kill()
###############################Run_Exe################################


def batchcompress(path, compressType):
    import subprocess
    filelist = getFileInPath(path)
    if compressType == 'Z':
        for file in filelist:
            args = 'compress ' + file
            subprocess.Popen(args=args, shell=True)

    

def copyFile(ori_file, target):
    import os
    import shutil
    if not os.path.isfile(ori_file):
        raise IOError(ori_file + ' is not file!')
    if os.path.isdir(target):
        shutil.copy(ori_file, target)
    if os.path.isfile(target):
        os.remove(target)
        shutil.copy(ori_file, target)
    else:
        shutil.copy(ori_file, target)

def moveFile(ori_file, target):
    import os
    import shutil
    if not os.path.isfile(ori_file):
        raise IOError(ori_file + ' is not file!')
    
    if os.path.isdir(target):
        shutil.move(ori_file, target)
    if os.path.isfile(target):
        os.remove(target)
        shutil.move(ori_file, target)
    else:
        shutil.move(ori_file, target)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#############################File_Folder##############################


###############################Run_Exe################################
def delFolderByHourDif(folder, dayDif):
    import os
    import datetime
    import time
    import shutil
    # print(datetime.datetime.now() - datetime.timedelta(days=dayDif))
    checkTime = datetime.datetime.now() - datetime.timedelta(hours=dayDif)
    for f in os.listdir(folder):
        abs_path = os.path.join(folder, f)
        timestamp = os.path.getctime(abs_path)
        timeFile = datetime.datetime.fromtimestamp(timestamp)
        if timeFile < checkTime:
            print(abs_path)
            shutil.rmtree(abs_path)
        print(timeFile)


def batchRename(path, oldStr, newStr):
    import os
    fileList = getFileInPath(path)
    for file in fileList:
        newFile = str(file).replace(oldStr, newStr)
        os.rename(file, newFile)


