# gnssbox        : The most complete GNSS Python toolkit ever
# readObs        : Read Obs
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : AIR, Chinese Academy of Sciences
# Creation Date  : 2022.07.14
# Latest Version : 3.01.01
# Date           : 2026.08.03 - Version 3.01.01


def readRinex3LineTime(line):
    '''
    读取rinex3.x文件时间转为datetime   
        by ChangChuntao -> 2022.07.14
    适应非整秒
        by ChangChuntao -> 2023.09.04
    '''
    import datetime
    format_string = "> %Y %m %d %H %M %S.%f"
    lineDatetime = datetime.datetime.strptime(line[:28], format_string)
    return lineDatetime

def readRinex2LineTime(line):
    '''
    读取rinex2.x文件历元行时间转为datetime    by ChangChuntao -> 2022.07.14
    修复: 保留小数秒(高采样率文件), 兼容闰秒(60秒), 无效行返回None
        by ChangChuntao -> 2026.08.03
    '''
    import datetime
    line = str(line).split()
    try:
        year = int(line[0])
        month = int(line[1])
        day = int(line[2])
        hour = int(line[3])
        minute = int(line[4])
        second = float(line[5])
    except (ValueError, IndexError):
        return None
    if year < 80:
        year += 2000
    else:
        year += 1900
    lineDatetime = datetime.datetime(year, month, day, hour, minute)
    lineDatetime += datetime.timedelta(seconds=second)
    return lineDatetime

def _prnChunks(line, start):
    '''
    从指定列开始按3字符解析PRN列表(12(A1,I2)), 返回PRN列表; 含非法字段返回None
        by ChangChuntao -> 2026.08.03
    '''
    prnList = []
    for i in range(start, start + 36, 3):
        chunk = line[i:i + 3].strip()
        if not chunk:
            break
        if len(chunk) == 2 and chunk.isdigit():
            prnList.append('G' + chunk)
        elif len(chunk) == 3 and chunk[0].isalpha() and chunk[1:].isdigit():
            prnList.append(chunk)
        else:
            return None
    return prnList

def readRinex2EpochLine(line):
    '''
    解析rinex2.x历元行(EPOCH/SAT记录), 依据官方RINEX 2.11/2.10规范:
        列  1    : 空白                        (1X)
        列  2-3  : 年                          (I2.2)
        列  5-6  : 月, 8-9 日, 11-12 时, 14-15 分   (4(1X,I2))
        列 16-26 : 秒                          (F11.7)
        列 27-29 : 历元标志                     (2X,I1)
        列 30-32 : 卫星数                       (I3)
        列 33-68 : PRN列表                      (12(A1,I2))
    兼容个别转换器无前导空白(整体左移一列)的输出
    返回 (datetime, flag, satNum, prnList); 非历元行返回None
        by ChangChuntao -> 2026.08.03
    '''
    obsDatetime = readRinex2LineTime(line)
    if obsDatetime is None or len(line) < 30:
        return None
    # 卫星数在30-32列(标准), 个别文件左移一列(28-30列)
    try:
        satNum = int(line[29:32])
        prnStart = 32
        flagIdx = 28
    except ValueError:
        try:
            satNum = int(line[28:31])
            prnStart = 31
            flagIdx = 27
        except ValueError:
            return None
    if not 0 <= satNum <= 999:
        return None
    try:
        flag = int(line[flagIdx]) if line[flagIdx].strip() else 0
    except ValueError:
        flag = 0
    prnList = _prnChunks(line, prnStart)
    if prnList is None:
        return None
    return obsDatetime, flag, satNum, prnList

def readRinex2PrnContinuation(line):
    '''
    解析rinex2.x历元行的卫星续行(32X,12(A1,I2)), 返回PRN列表; 非续行返回None
        by ChangChuntao -> 2026.08.03
    '''
    prnList = _prnChunks(line, 32)
    if prnList is None:
        prnList = _prnChunks(line, 31)   # 兼容左移一列的布局
    return prnList



def readObs2Head(obsFile, needSatList = True, bar = None):
    '''
    读取rinex2.x文件的文件头    by ChangChuntao -> 2022.09.25
    修复: 历元扫描与类型行解析按官方规范, 继承系统类型用副本(避免双次转换)
        by ChangChuntao -> 2026.08.03
    '''

    # bar for QT
    if bar is not None:
        from PyQt5.QtWidgets import QApplication
        bar.status.showMessage("Reading Head...")
        QApplication.processEvents()

    with open(obsFile, 'r') as obsFileOpen:
        obsFileLines = obsFileOpen.readlines()
    gnssSysList = ['C', 'R', 'G', 'E', 'I', 'J', 'S', 'W', '0']
    obsHead = {'version': None,
                'PGM': 'gnssbox',
                'RUN': 'WHU',
                'MARKER NAME': None,
                'MARKER NUMBER': None,
                'Receiver': None,
                'Receiver Type': None,
                'Antenna': None,
                'Antenna Type': None,
                'Agency': None,
                'Approx Position': [None, None, None],
                'Antenna Delta': [None, None, None],
                'interval': None,
                'Leap Seconds': None,
                'epoch': [],
                'prn': [],
                'OBS TYPES': None}
    satList = []
    endHeadLineNum = 0
    for line in obsFileLines:
        if 'END OF HEADER' in line:
            endHeadLineNum += 1
            break
        endHeadLineNum += 1
    if needSatList:
        nowLineIndex = endHeadLineNum
        while nowLineIndex < len(obsFileLines):
            epochInfo = readRinex2EpochLine(obsFileLines[nowLineIndex])
            nowLineIndex += 1
            if epochInfo is None:
                continue
            _, epochFlag, satNum, prnList = epochInfo
            if epochFlag > 1:
                nowLineIndex += satNum   # 跳过事件标志(2-5)或周跳记录(6)
                continue
            while len(prnList) < satNum and nowLineIndex < len(obsFileLines):
                contPrnList = readRinex2PrnContinuation(obsFileLines[nowLineIndex])
                if not contPrnList:
                    break
                prnList += contPrnList
                nowLineIndex += 1
            for prn in prnList[:satNum]:
                if prn not in satList:
                    satList.append(prn)
    obsHead['prn'] = satList
    obs = {}
    for line in obsFileLines:
        if 'RINEX VERSION / TYPE' in line:
            obsHead['version'] = float(line.split()[0])
        elif 'PGM / RUN BY / DATE' in line:
            obsHead['PGM'] = line[:20].strip()
            obsHead['RUN'] = line[20:40].strip()
        elif 'MARKER NAME' in line:
            obsHead['MARKER NAME'] = line[:20].strip()
        elif 'MARKER NUMBER' in line:
            obsHead['MARKER NUMBER'] = line[:20].strip()
        elif 'OBSERVER / AGENCY' in line:
            obsHead['Agency'] = line[20:40].strip()
        elif 'REC # / TYPE / VERS' in line:
            obsHead['Receiver'] = line[:20].strip()
            obsHead['Receiver Type'] = line[20:40].strip()
        elif 'ANT # / TYPE' in line:
            obsHead['Antenna'] = line[:20].strip()
            obsHead['Antenna Type'] = line[20:40].strip()
        elif 'APPROX POSITION XYZ' in line:
            x = float(line.split()[0])
            y = float(line.split()[1])
            z = float(line.split()[2])
            obsHead['Approx Position'] =[x, y, z]
        elif 'ANTENNA: DELTA H/E/N' in line:
            h = float(line.split()[0])
            e = float(line.split()[1])
            n = float(line.split()[2])
            obsHead['Antenna Delta'] = [h, e, n]
        elif 'INTERVAL' in line:
            try:
                obsHead['interval'] = int(float(line.split()[0]))
            except ValueError:
                pass
        elif 'LEAP SECONDS' in line:
            try:
                obsHead['Leap Seconds'] = int(line.split()[0])
            except ValueError:
                pass
        elif '# / TYPES OF OBSERV' in line:
            # 官方格式: I6,9(4X,A2) 或混合系统 (A1,I2,9(4X,A2)), 续行 6X,9(4X,A2)
            tokens = line.split()
            if '#' in tokens:
                tokens = tokens[:tokens.index('#')]
            if not tokens:
                continue
            gnssSys = 'G'
            first = tokens[0]
            if len(first) == 1 and first in gnssSysList:
                gnssSys = first
                tokens = tokens[1:]
                if tokens and tokens[0].isdigit():
                    typeCount = int(tokens[0])
                    typeList = tokens[1:typeCount + 1]
                else:
                    typeList = tokens
            elif first.isdigit():
                typeCount = int(first)
                typeList = tokens[1:typeCount + 1]
            else:
                typeList = tokens   # 续行(无类型计数)
            if gnssSys in obs:
                obs[gnssSys] += typeList
            else:
                obs[gnssSys] = typeList

    # 先转换各系统自己的类型
    for gSys in obs:
        newBandList = []
        for bandIndex in range(len(obs[gSys])):
            newBandList.append(obsType2to3(gSys, obs[gSys][bandIndex]))
        obs[gSys] = newBandList

    # 无系统独立类型(共享类型文件)时, 继承转换后的G类型; 用副本避免互相影响
    for prn in satList:
        if prn[0] not in obs:
            if 'G' in obs:
                obs[prn[0]] = list(obs['G'])
            elif obs:
                obs[prn[0]] = list(next(iter(obs.values())))
            else:
                obs[prn[0]] = []

    obsHead['OBS TYPES'] = obs
    return obsHead

def readObs3Head(obsFile, needSatList = False, bar = None):
    '''
    读取rinex3.x文件的文件头    by ChangChuntao -> 2022.09.24
    '''
    
    if bar is not None:
        from PyQt5.QtWidgets import QApplication
        bar.status.showMessage("Reading Head...")
        QApplication.processEvents()

    obsHead = {'version': None,
                'PGM': 'gnssbox',
                'RUN': 'WHU',
                'MARKER NAME': None,
                'MARKER NUMBER': None,
                'Receiver': None,
                'Receiver Type': None,
                'Antenna': None,
                'Antenna Type': None,
                'Agency': None,
                'Approx Position': [None, None, None],
                'Antenna Delta': [None, None, None],
                'interval': None,
                'Leap Seconds': None,
                'epoch': [],
                'prn': [],
                'OBS TYPES': None}
    gnssSysList = ['C', 'R', 'G', 'E', 'I', 'J', 'S', 'W', '0', 'X']
    obs = {}
    obsFileOpen = open(obsFile, 'r')
    line = obsFileOpen.readline()
    readBegin = False
    satList = []
    while line != '':
        if needSatList and readBegin:
            if '>' not in line:
                sat = line[:3]
                gnssSys = line[0]
                if gnssSys in ['W', '0', 'X', 'L', '5', '1']:
                    gnssSys = 'W'
                    sat = gnssSys + sat[1:]
                if sat not in satList:
                    satList.append(sat)
        if 'RINEX VERSION / TYPE' in line:
            obsHead['version'] = float(line.split()[0])
        elif 'PGM / RUN BY / DATE' in line:
            obsHead['PGM'] = line[:20].strip()
            obsHead['RUN'] = line[20:40].strip()
        elif 'MARKER NAME' in line:
            obsHead['MARKER NAME'] = line[:20].strip()
        elif 'MARKER NUMBER' in line:
            obsHead['MARKER NUMBER'] = line[:20].strip()
        elif 'OBSERVER / AGENCY' in line:
            obsHead['Agency'] = line[20:40].strip()
        elif 'REC # / TYPE / VERS' in line:
            obsHead['Receiver'] = line[:20].strip()
            obsHead['Receiver Type'] = line[20:40].strip()
        elif 'ANT # / TYPE' in line:
            obsHead['Antenna'] = line[:20].strip()
            obsHead['Antenna Type'] = line[20:40].strip()
        elif 'APPROX POSITION XYZ' in line:
            x = float(line.split()[0])
            y = float(line.split()[1])
            z = float(line.split()[2])
            obsHead['Approx Position'] =[x, y, z]
        elif 'ANTENNA: DELTA H/E/N' in line:
            h = float(line.split()[0])
            e = float(line.split()[1])
            n = float(line.split()[2])
            obsHead['Antenna Delta'] = [h, e, n]
        elif 'INTERVAL' in line:
            obsHead['interval'] = int(float(line.split()[0]))
        elif 'LEAP SECONDS' in line:
            obsHead['Leap Seconds'] = int(line.split()[0])
        elif 'SYS / # / OBS TYPES' in line:
            if line[0] in gnssSysList:
                gnssSys = line[0]
                if gnssSys in ['W', '0', 'X', 'L', '5', '1']:
                    gnssSys = 'W'
                if gnssSys in obs:
                    obs[gnssSys] = obs[gnssSys] + line[7:60].split()
                else:
                    obs[gnssSys] = line[7:60].split()
            else:
                obs[gnssSys] += line[7:60].split()
        elif 'END OF HEADER' in line:
            if needSatList:
                readBegin = True
            else:
                break
        line = obsFileOpen.readline()
    obsHead['prn'] = satList
    obsFileOpen.close()
    
    for gSys in obs:
        newBandList = []
        for bandIndex in range(len(obs[gSys])):
            band = obs[gSys][bandIndex]
            if len(band) == 2:
                newBandList.append(obsType2to3(gSys, band))
            else:
                newBandList.append(band)
        obs[gSys] = newBandList

    obsHead['OBS TYPES'] = obs
    return obsHead


def readObs2(obsFile, obsHead=None, bar = None):
    '''
    读取rinex2.x文件的文件体        by ChangChuntao -> 2022.09.24
    存储方式 -> obsData[epoch][prn][band] -> band value
    修复: 历元行按官方规范列位置解析, 支持小数秒/事件标志/续行, 读取LLI
        by ChangChuntao -> 2026.08.03
    '''
    import time
    start_time = time.time()

    # bar for QT
    if bar is not None:
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()

    if obsHead is None:
        obsHead = readObs2Head(obsFile, needSatList=True)
    with open(obsFile, 'r') as obsFileOpen:
        obsFileLines = obsFileOpen.readlines()

    obsData = {}
    endHeadLineNum = 0
    for line in obsFileLines:
        if 'END OF HEADER' in line:
            endHeadLineNum += 1
            break
        endHeadLineNum += 1

    obsDatetime = None
    satEpoch = []          # 当前历元的卫星列表
    nowSatNum = 0          # 当前读取到第几颗卫星
    bandIndex = 0          # 当前卫星读到第几个观测值
    skipLineNum = 0        # 需跳过的特殊记录行数(历元标志 2-6)
    lineIndex = endHeadLineNum
    while lineIndex < len(obsFileLines):
        line = obsFileLines[lineIndex]
        lineIndex += 1

        if bar is not None:
            if lineIndex / len(obsFileLines) * 100 - int(lineIndex / len(obsFileLines) * 100) < 1.e-4:
                completed = int(20 * lineIndex / len(obsFileLines))
                remaining = 20 - completed
                barPercent = '=' * completed + '-' * remaining
                percentage = f'{(lineIndex / len(obsFileLines)) * 100:.2f}%'
                bar.status.showMessage("Reading obs   [" + barPercent + '] ' + percentage)
                QApplication.processEvents()

        if skipLineNum > 0:
            skipLineNum -= 1
            continue

        epochInfo = readRinex2EpochLine(line)
        if epochInfo is not None:
            obsDatetime, epochFlag, satNum, prnList = epochInfo
            if epochFlag > 1:
                # 事件标志 2-5: 后面跟satNum个特殊记录; 标志6: 周跳记录
                skipLineNum = satNum
                obsDatetime = None
                continue
            obsData[obsDatetime] = {}
            satEpoch = prnList[:satNum] if satNum > 0 else prnList
            nowSatNum = 0
            bandIndex = 0
            # 超过12颗卫星: 读取续行(32X,12(A1,I2))
            while len(satEpoch) < satNum and lineIndex < len(obsFileLines):
                contPrnList = readRinex2PrnContinuation(obsFileLines[lineIndex])
                if not contPrnList:
                    break
                lineIndex += 1
                satEpoch += contPrnList
            satEpoch = satEpoch[:satNum]
            for prn in satEpoch:
                obsData[obsDatetime][prn] = {}
                nowSys = prn[0]
                if nowSys in obsHead['OBS TYPES']:
                    for band in obsHead['OBS TYPES'][nowSys]:
                        obsData[obsDatetime][prn][band] = None
            continue

        # 观测值记录: 每16列一项(观测值F14.3 + LLI + 信号强度)
        if obsDatetime is None or nowSatNum >= len(satEpoch):
            continue
        nowPrn = satEpoch[nowSatNum]
        nowSys = nowPrn[0]
        if nowSys in obsHead['OBS TYPES']:
            bandList = obsHead['OBS TYPES'][nowSys]
        else:
            bandList = next(iter(obsHead['OBS TYPES'].values()), [])
        line = "{:<80}".format(line[:-1])
        for fieldStr in [line[i:i + 16] for i in range(0, len(line), 16)]:
            if bandIndex >= len(bandList):
                break
            band = bandList[bandIndex]
            valueStr = fieldStr[:14].strip()
            try:
                bandValue = float(valueStr)
                if bandValue == 0.0:
                    bandValue = None   # 规范: 缺失观测写为0.0或空白
            except ValueError:
                bandValue = None
            obsData[obsDatetime][nowPrn][band] = bandValue
            if band[0] == 'L':
                lliStr = fieldStr[14].strip() if len(fieldStr) >= 16 else ''
                obsData[obsDatetime][nowPrn][band + 'LLI'] = int(lliStr) if lliStr else 0
            bandIndex += 1
        if bandIndex >= len(bandList):
            nowSatNum += 1
            bandIndex = 0
            if nowSatNum >= len(satEpoch):
                obsDatetime = None   # 本历元读完, 等待下一个历元行

    end_time = time.time()
    execution_time = end_time - start_time
    print("Read OBS Time : ", execution_time, "s")
    if bar is not None:
        bar.status.showMessage("Read finished [" + 20*'=' + '] ' + "100% Elapsed time " + '%.2f' % (execution_time) + ' s')
        QApplication.processEvents()
    return obsData


def readObs3(obsFile, obsHead = None, bar = None):
    '''
    读取rinex3.x文件的文件体, 存储方式 -> obsDat[epoch][prn][band] -> band value        
        by ChangChuntao -> 2022.09.24
    '''
    import time
    start_time = time.time()

    # bar for QT
    if bar is not None:
        from PyQt5.QtWidgets import QApplication

    if obsHead is None:
        obsHead = readObs3Head(obsFile)
    obsFileOpen = open(obsFile, 'r')
    obsFileLines = obsFileOpen.readlines()
    obsFileOpen.close()

    obsData = dict()
    endHeadLineNum = 0
    for line in obsFileLines:
        endHeadLineNum += 1
        if 'END OF HEADER' in line:
            endHeadLineNum += 1
            break
    obsDatetime = None
    lineIndex = endHeadLineNum - 1
    for line in obsFileLines[endHeadLineNum-1:]:
        lineIndex += 1
        if bar is not None:
            if lineIndex / len(obsFileLines) * 100 - int(lineIndex / len(obsFileLines) * 100) < 1.e-4:
                completed = int(20 * lineIndex / len(obsFileLines)) - 1
                remaining = 20 - completed
                barPercent = '=' * completed + '>' + '+' * remaining
                percentage = f'{(lineIndex / len(obsFileLines)) * 100:.2f}%'
                bar.status.showMessage("Reading obs   [" + barPercent + '] ' + percentage)
                QApplication.processEvents()
        if line[0] == '>':
            if obsDatetime is not None:
                obsData[obsDatetime].update(prnData)
            obsDatetime = readRinex3LineTime(line)
            if obsDatetime not in obsData.keys():
                obsData[obsDatetime] = dict()
                prnData = dict()
        else:
            prn = line[:3]
            gnssSys = line[0]
            if gnssSys in ['W', '0', 'X', 'L', '5', '1']:
                gnssSys = 'W'
                prn = gnssSys + prn[1:]
            nowLineIndex = 3
            if gnssSys not in obsHead['OBS TYPES']:
                continue
            if prn[1] == ' ':
                prn = prn[0] + '0' + prn[2]
            prnData[prn] = dict()
            for band in obsHead['OBS TYPES'][gnssSys]:
                bandStr = line[nowLineIndex:nowLineIndex+14].strip()
                nowLineIndex += 16
                bandValue = None
                if bandStr:
                    try:
                        bandValue = float(bandStr)
                        if bandValue < -999999999.0 or bandValue == 0.0:
                            bandValue = None
                    except:
                        pass
                    
                    if band[0] == 'L':
                        if line[nowLineIndex-2].strip():
                            prnData[prn][band+'LLI'] = int(line[nowLineIndex-2])
                        else:
                            prnData[prn][band+'LLI'] = 0
                else:
                    if band[0] == 'L': prnData[prn][band+'LLI'] = 0
                prnData[prn][band] = bandValue
    obsData[obsDatetime].update(prnData)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("Read OBS Time : ", execution_time, "s")
    if bar is not None:
        bar.status.showMessage("Read finished [" + 20*'=' + '] ' + "100% Elapsed time " + '%.2f' % (execution_time) + ' s')
        QApplication.processEvents()
    return obsData


def readObs(obsFile, obsHead = None, bar=None):
    '''
    读取gnss观测数据文件            by ChangChuntao -> 2022.09.24
    '''
    obsFileOpen = open(obsFile, 'r')
    obsFileLine = obsFileOpen.readline()
    obsFileOpen.close()
    obsVersion = 0.0
    if 'RINEX VERSION / TYPE' in obsFileLine:
        obsVersion = float(obsFileLine.split()[0])
    else:
        return None

    if 2.0 <= obsVersion < 3.0:
        obsData = readObs2(obsFile,obsHead, bar)
    elif 4.0 > obsVersion >= 3.0:
        obsData = readObs3(obsFile,obsHead, bar)
    else:
        print('Higher versions of Rinex are not currently supported!')
        return None
    return obsData

def readObsHead(obsFile, needSatList = False, bar=None):
    '''
    读取gnss观测数据文件头          by ChangChuntao -> 2022.09.24
    '''
    
    obsFileOpen = open(obsFile, 'r')
    obsFileLine = obsFileOpen.readline()
    obsFileOpen.close()
    obsVersion = 0.0
    # for line in obsFileLines:
    if 'RINEX VERSION / TYPE' in obsFileLine:
        obsVersion = float(obsFileLine.split()[0])

    if 2.0 <= obsVersion < 3.0:
        obsHead = readObs2Head(obsFile, needSatList, bar)
    elif 4.0 > obsVersion >= 3.0:
        obsHead = readObs3Head(obsFile, needSatList, bar)
    else:
        print('Higher versions of Rinex are not currently supported!')
        return None
    return obsHead

def is_obs(obs_file):
    '''
    Check whether the file is obs - by chang chuntao 2022.12.03
    '''
    try:
        obs_file_open = open(obs_file , 'r')
        obs_file_line = obs_file_open.readline()
    except:
        return False
    obs_file_open.close()
    if 'RINEX VERSION / TYPE' in obs_file_line and 'NAV' not in obs_file_line and obs_file_line[20] != 'C':
        return True
    else:
        return False

def get_obs_in_path(rinex_path):
    '''
    获取给定路径内所有的obs文件 - by chang chuntao 2022.12.03
    '''
    import os
    output_filelist = []
    for root, dirs, files in os.walk(rinex_path):
        for filename in files:
            abs_filename = os.path.join(root, filename)
            if is_obs(abs_filename):
                output_filelist.append(abs_filename)
    return output_filelist

def getSatInObs3(obsFile):
    '''
    获取obs文件内所有的观测卫星 - by chang chuntao 2022.12.03
    '''
    obsOpen = open(obsFile, 'r')
    obsLines = obsOpen.readlines()
    obsOpen.close()
    readBegin = False
    satList = []
    for line in obsLines:
        if readBegin:
            if '>' not in line:
                line = line.split()
                sat = line[0]
                if sat not in satList:
                    satList.append(sat)
        if 'END OF HEADER' in line:
            readBegin = True
    return satList


def getRinex3SatTime(rinexFile):
    '''
    读取观测文件中卫星对应的时间    by ChangChuntao -> 2022.07.14
    rinexFile         : 观测数据文件
    rinexSatTime      : 存储形式
    {prn1 : [datetime1, datetim2, ..., datetimen],
     prn2 : [datetime1, datetim2, ..., datetimen],
     ...,
     prnn : [datetime1, datetim2, ..., datetimen]}
    '''
    rinexFileLineOpen = open(rinexFile, 'r')
    rinexFileLine = rinexFileLineOpen.readlines()
    rinexFileLineOpen.close()
    satList = []
    rinexSatTime = {}
    endHeadLineNum = 0
    for line in rinexFileLine:
        endHeadLineNum += 1
        if 'END OF HEADER' in line:
            endHeadLineNum += 1
            break
    for line in rinexFileLine[endHeadLineNum:]:
        satPrn = line[:3]
        if satPrn not in satList and line[0] != '>':
            satList.append(satPrn)
            rinexSatTime[satPrn] = []
    timeLine = []
    lineNum = 0
    for line in rinexFileLine:
        if line[0] == '>':
            timeLine.append(lineNum)
        lineNum += 1
    for lineNumIndex in range(0, len(timeLine) - 1):
        nowDateTime = readRinex3LineTime(rinexFileLine[timeLine[lineNumIndex]])
        for line in rinexFileLine[timeLine[lineNumIndex] + 1:timeLine[lineNumIndex + 1]]:
            satPrn = line[:3]
            rinexSatTime[satPrn].append(nowDateTime)
    return rinexSatTime

def getRinex3TimeSeries(rinexFile):
    rinexFileLineOpen = open(rinexFile, 'r')
    rinexFileLine = rinexFileLineOpen.readlines()
    rinexFileLineOpen.close()
    readBegin = False
    timeList = []
    for line in rinexFileLine:
        if readBegin:
            if '>' in line:
                nowTime = readRinex3LineTime(line)
                timeList.append(nowTime)
        if 'END OF HEADER' in line:
            readBegin = True
    def get_list(date):
        return date.timestamp()
    timeList = sorted(timeList, key=lambda date:get_list(date))
    return timeList


def get_obsfile_ST_ET_quick(rinexFile):
    '''
    get clkfile start_datetime & end_datetime quick - by chang chuntao 2023.06.22
    '''
    obs_file_open = open(rinexFile , 'r')
    obs_file_line = obs_file_open.readlines()
    obs_file_open.close()
    for line in obs_file_line:
        if '>' in line[0]:
            start_datetime = readRinex3LineTime(line)
            break
    for line in obs_file_line[-200:]:
        if '>' in line[0]:
            end_line = line
    end_datetime = readRinex3LineTime(end_line)
    return start_datetime, end_datetime

def getIntervalInRinex3(rinexFile):
    rinexFileLineOpen = open(rinexFile, 'r')
    rinexFileLine = rinexFileLineOpen.readlines()
    rinexFileLineOpen.close()
    readBegin = False
    timeList = []
    for line in rinexFileLine:
        if readBegin:
            if '>' in line:
                nowTime = readRinex3LineTime(line)
                timeList.append(nowTime)
        if 'END OF HEADER' in line:
            readBegin = True
    def get_list(date):
        return date.timestamp()
    timeList = sorted(timeList, key=lambda date:get_list(date))
    interval = 999999999999
    for nowTimeIndex in range(len(timeList[1:])):
        intervalTemp = (timeList[nowTimeIndex+1] - timeList[nowTimeIndex]).total_seconds()
        if intervalTemp < interval:
            interval = intervalTemp
    return interval

def obsType2to3(gSys, band):
    if band[0] == 'C' or band[0] == 'L' or band[0] == 'S' or band[0] == 'D':
        if band[1] == '1' or band[1] == '2':
            if gSys == 'G':
                if band == 'L2':
                    band = band[:2] + 'P'
                else:
                    band = band[:2] + 'C'
            else:
                band = band[:2] + 'P'
        else:
            if gSys == 'G':
                band = band[:2] + 'I'
            else:
                band = band[:2] + 'P'
    elif band[0] == 'P':
        band = 'C' + band[1] + 'P'
    else:
        return band
    return band