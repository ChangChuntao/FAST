

import datetime

def nav2timeLine2datetime(timeline):
    navDataTime = datetime.datetime.strptime(timeline[3:22], '%y %m %d %H %M %S.%f')
    return navDataTime

def nav3timeLine2datetime(timeline):
    navDataTime = datetime.datetime.strptime(timeline[4:23], '%Y %m %d %H %M %S')
    return navDataTime


def readNav2Head(navFile):
    navOpen = open(navFile, 'r+')
    navHead = {}
    navHead['ION ALPHA'] = []
    navHead['ION BETA'] = []
    navHead['LEAP SECONDS'] = 18
    while True:
        try:
            line = navOpen.readline()
        except:
            break
        if 'END OF HEADER' in line:
            break
        lines = line.split()
        if 'RINEX VERSION / TYPE' in line:
            if 'GLONASS' in line:
                navHead['system'] = 'R'
            else:
                navHead['system'] = 'G'
        
        elif 'ION ALPHA' in  line:
            lines = line.split()
            navHead['ION ALPHA'].append(float(lines[0].replace('D', 'E')))
            navHead['ION ALPHA'].append(float(lines[1].replace('D', 'E')))
            navHead['ION ALPHA'].append(float(lines[2].replace('D', 'E')))
            navHead['ION ALPHA'].append(float(lines[3].replace('D', 'E')))
        elif 'ION BETA' in  line:
            navHead['ION BETA'].append(float(lines[0].replace('D', 'E')))
            navHead['ION BETA'].append(float(lines[1].replace('D', 'E')))
            navHead['ION BETA'].append(float(lines[2].replace('D', 'E')))
            navHead['ION BETA'].append(float(lines[3].replace('D', 'E')))
        elif 'LEAP SECONDS' in  line:
            navHead['LEAP SECONDS'] = int(lines[0])
    
    navOpen.close()
    return navHead


def readNav3Head(navFile):
    navOpen = open(navFile, 'r+')
    navHead = {}
    navHead['LEAP SECONDS'] = 18
    navHead['ion'] = {}
    navHead['ion']['E'] = {}
    navHead['ion']['G'] = {}
    navHead['ion']['C'] = {}
    navHead['ion']['I'] = {}
    navHead['ion']['J'] = {}

    while True:
        try:
            line = navOpen.readline()
        except:
            ...
        if 'END OF HEADER' in line:
            break
        lines = line.split()
        if 'RINEX VERSION / TYPE' in line:
            rnxVersion = float(line.split()[0])
            navHead['rnxVersion'] = rnxVersion
        elif 'LEAP SECONDS' in  line:
            navHead['LEAP SECONDS'] = int(lines[0])
        elif 'IONOSPHERIC CORR' in line:
            if 'GAL' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['E']['ai0'] = float(lines[1])
                navHead['ion']['E']['ai1'] = float(lines[2])
                navHead['ion']['E']['ai2'] = float(lines[3])
            elif 'GPSA' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['G']['alpha0'] = float(lines[1])
                navHead['ion']['G']['alpha1'] = float(lines[2])
                navHead['ion']['G']['alpha2'] = float(lines[3])
                navHead['ion']['G']['alpha4'] = float(lines[4])
            elif 'GPSB' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['G']['beta0'] = float(lines[1])
                navHead['ion']['G']['beta1'] = float(lines[2])
                navHead['ion']['G']['beta2'] = float(lines[3])
                navHead['ion']['G']['beta4'] = float(lines[4])
            elif 'BDSA' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['C']['alpha0'] = float(lines[1])
                navHead['ion']['C']['alpha1'] = float(lines[2])
                navHead['ion']['C']['alpha2'] = float(lines[3])
                navHead['ion']['C']['alpha4'] = float(lines[4])

            elif 'BDSB' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['C']['beta0'] = float(lines[1])
                navHead['ion']['C']['beta1'] = float(lines[2])
                navHead['ion']['C']['beta2'] = float(lines[3])
                navHead['ion']['C']['beta4'] = float(lines[4])
            elif 'IRNA' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['I']['alpha0'] = float(lines[1])
                navHead['ion']['I']['alpha1'] = float(lines[2])
                navHead['ion']['I']['alpha2'] = float(lines[3])
                navHead['ion']['I']['alpha4'] = float(lines[4])
            elif 'IRNB' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['I']['beta0'] = float(lines[1])
                navHead['ion']['I']['beta1'] = float(lines[2])
                navHead['ion']['I']['beta2'] = float(lines[3])
                navHead['ion']['I']['beta4'] = float(lines[4])
            elif 'QZSA' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['J']['alpha0'] = float(lines[1])
                navHead['ion']['J']['alpha1'] = float(lines[2])
                navHead['ion']['J']['alpha2'] = float(lines[3])
                navHead['ion']['J']['alpha4'] = float(lines[4])
            elif 'QZSB' in line:
                line = line.replace('D', 'E')
                lines = line.split()
                navHead['ion']['J']['beta0'] = float(lines[1])
                navHead['ion']['J']['beta1'] = float(lines[2])
                navHead['ion']['J']['beta2'] = float(lines[3])
                navHead['ion']['J']['beta4'] = float(lines[4])
    
    return navHead


def readNav2(navFile, navHead = None):
    if navHead is None:
        navHead = readNav2Head(navFile)
    navOpen = open(navFile, 'r+')
    navLines = navOpen.readlines()
    navOpen.close()
    lineBeginIndex = 0
    for line in navLines:
        if 'END OF HEADER' not in line:
            lineBeginIndex += 1
        else:
            lineBeginIndex += 1
            break
    navData = {}

    lineNum = lineBeginIndex
    fileLen = len(navLines)
    if navHead['system'] == 'G':
        updateLine = 8
    else:
        updateLine = 4

    while lineNum < fileLen:
        if navHead['system'] == 'G':
            navLines0 = navLines[lineNum + 0].replace('D', 'E')
            navLines1 = navLines[lineNum + 1].replace('D', 'E')
            navLines2 = navLines[lineNum + 2].replace('D', 'E')
            navLines3 = navLines[lineNum + 3].replace('D', 'E')
            navLines4 = navLines[lineNum + 4].replace('D', 'E')
            navLines5 = navLines[lineNum + 5].replace('D', 'E')
            navLines6 = navLines[lineNum + 6].replace('D', 'E')
            navLines7 = navLines[lineNum + 7].replace('D', 'E')
            nowEpoch = nav2timeLine2datetime(navLines0)
            prn = navHead['system'] + '%02d' % int(navLines0[:2])
            if prn not in navData:
                navData[prn] = {}
            navData[prn][nowEpoch] = {}

            navData[prn][nowEpoch]['SVclockBias'] = float(navLines0[22:41])
            navData[prn][nowEpoch]['SVclockDrift'] = float(navLines0[41:60])
            navData[prn][nowEpoch]['SVclockDriftRate'] = float(navLines0[60:79])

            navData[prn][nowEpoch]['IODE'] = float(navLines1[3:22])
            navData[prn][nowEpoch]['crs'] = float(navLines1[22:41])
            navData[prn][nowEpoch]['DeltaN'] = float(navLines1[41:60])
            navData[prn][nowEpoch]['M0'] = float(navLines1[60:79])

            navData[prn][nowEpoch]['cuc'] = float(navLines2[3:22])
            navData[prn][nowEpoch]['e'] = float(navLines2[22:41])
            navData[prn][nowEpoch]['cus'] = float(navLines2[41:60])
            navData[prn][nowEpoch]['roota'] = float(navLines2[60:79])

            navData[prn][nowEpoch]['toe'] = float(navLines3[3:22])
            navData[prn][nowEpoch]['cic'] = float(navLines3[22:41])
            navData[prn][nowEpoch]['OMEGA0'] = float(navLines3[41:60])
            navData[prn][nowEpoch]['cis'] = float(navLines3[60:79])

            navData[prn][nowEpoch]['i0'] = float(navLines4[3:22])
            navData[prn][nowEpoch]['crc'] = float(navLines4[22:41])
            navData[prn][nowEpoch]['omega'] = float(navLines4[41:60])
            navData[prn][nowEpoch]['OMEGA_DOT'] = float(navLines4[60:79])

            navData[prn][nowEpoch]['IDOT'] = float(navLines5[3:22])
            navData[prn][nowEpoch]['L2Codes'] = float(navLines5[22:41])
            navData[prn][nowEpoch]['GPS_Week'] = float(navLines5[41:60])
            navData[prn][nowEpoch]['L2PdataFlag'] = float(navLines5[60:79])

            navData[prn][nowEpoch]['SVaccuracy'] = float(navLines6[3:22])
            navData[prn][nowEpoch]['SVhealth'] = float(navLines6[22:41])
            navData[prn][nowEpoch]['TGD'] = float(navLines6[41:60])
            navData[prn][nowEpoch]['IODC'] = float(navLines6[60:79])

            navData[prn][nowEpoch]['ttm'] = float(navLines7[3:22])
            navData[prn][nowEpoch]['fi'] = float(navLines7[22:41])
        else:
            navLines0 = navLines[lineNum + 0].replace('D', 'E')
            navLines1 = navLines[lineNum + 1].replace('D', 'E')
            navLines2 = navLines[lineNum + 2].replace('D', 'E')
            navLines3 = navLines[lineNum + 3].replace('D', 'E')
            nowEpoch = nav2timeLine2datetime(navLines0)
            prn = navHead['system'] + '%02d' % int(navLines0[:2])
            if prn not in navData:
                navData[prn] = {}
            navData[prn][nowEpoch] = {}

            navData[prn][nowEpoch]['SVclockBias'] = float(navLines0[23:42])
            navData[prn][nowEpoch]['SVrelativeFrequencyBias'] = float(navLines0[42:61])
            navData[prn][nowEpoch]['MessageFrameTime'] = float(navLines0[61:80])

            navData[prn][nowEpoch]['x'] = float(navLines1[4:23])
            navData[prn][nowEpoch]['vx'] = float(navLines1[23:42])
            navData[prn][nowEpoch]['ax'] = float(navLines1[42:61])
            navData[prn][nowEpoch]['SVhealth'] = float(navLines1[61:80])

            navData[prn][nowEpoch]['y'] = float(navLines2[4:23])
            navData[prn][nowEpoch]['vy'] = float(navLines2[23:42])
            navData[prn][nowEpoch]['ay'] = float(navLines2[42:61])
            navData[prn][nowEpoch]['frequency'] = float(navLines2[61:80])

            navData[prn][nowEpoch]['z'] = float(navLines3[4:23])
            navData[prn][nowEpoch]['vz'] = float(navLines3[23:42])
            navData[prn][nowEpoch]['az'] = float(navLines3[42:61])
            navData[prn][nowEpoch]['operAge'] = float(navLines3[61:80])

        lineNum += updateLine
    return navData

def readNav3(navFile, navHead = None):
    if navHead is None:
        navHead = readNav3Head(navFile)
    navOpen = open(navFile, 'r+')
    navLines = navOpen.readlines()
    navOpen.close()
    lineBeginIndex = 0
    for line in navLines:
        if 'END OF HEADER' not in line:
            lineBeginIndex += 1
        else:
            lineBeginIndex += 1
            break
    navData = {}
    lineNum = lineBeginIndex
    fileLen = len(navLines)

    addLine = {'C': 8, 'G':8, 'E': 8, 'R': 4, 'J': 8, 'S':4, 'I':8}

    while lineNum < fileLen:
        navLines0 = navLines[lineNum + 0].replace('D', 'E')
        gSys = navLines0[0]
        if gSys not in addLine:
            lineNum += 1
            continue
        navLines0splict = navLines0.split()
        prn = navLines0splict[0]
        if prn not in navData:
            navData[prn] = {}
        # 历元
        epoch = nav3timeLine2datetime(navLines0)
        # if gSys == 'C':
        #     epoch += datetime.timedelta(seconds=14)
        navData[prn][epoch] = {}

        if gSys == 'C':
            # 当为BDS时,读取8行,按照说明读取。
            # lineNum + 8
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVclockDrift'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['SVclockDriftRate'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['AODE'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['crs'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['DeltaN'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['M0'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['cuc'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['e'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['cus'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['roota'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['toe'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['cic'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['OMEGA0'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['cis'] = float(navLines[lineNum + 3][61:80])

            navData[prn][epoch]['i0'] = float(navLines[lineNum + 4][4:23])
            navData[prn][epoch]['crc'] = float(navLines[lineNum + 4][23:42])
            navData[prn][epoch]['omega'] = float(navLines[lineNum + 4][42:61])
            navData[prn][epoch]['OMEGA_DOT'] = float(navLines[lineNum + 4][61:80])

            navData[prn][epoch]['IDOT'] = float(navLines[lineNum + 5][4:23])
            navData[prn][epoch]['Spare1'] = 0.0
            navData[prn][epoch]['BDT_Week'] = float(navLines[lineNum + 5][42:61])
            navData[prn][epoch]['Spare2'] = 0.0

            navData[prn][epoch]['SVaccuracy'] = float(navLines[lineNum + 6][4:23])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 6][23:42])
            navData[prn][epoch]['TGD1'] = float(navLines[lineNum + 6][42:61])
            navData[prn][epoch]['TGD2'] = float(navLines[lineNum + 6][61:80])

            navData[prn][epoch]['Transmission'] = float(navLines[lineNum + 7][4:23])
            navData[prn][epoch]['AODC'] = float(navLines[lineNum + 7][23:42])

        elif gSys == 'G':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVclockDrift'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['SVclockDriftRate'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['IODE'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['crs'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['DeltaN'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['M0'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['cuc'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['e'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['cus'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['roota'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['toe'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['cic'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['OMEGA0'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['cis'] = float(navLines[lineNum + 3][61:80])

            navData[prn][epoch]['i0'] = float(navLines[lineNum + 4][4:23])
            navData[prn][epoch]['crc'] = float(navLines[lineNum + 4][23:42])
            navData[prn][epoch]['omega'] = float(navLines[lineNum + 4][42:61])
            navData[prn][epoch]['OMEGA_DOT'] = float(navLines[lineNum + 4][61:80])

            navData[prn][epoch]['IDOT'] = float(navLines[lineNum + 5][4:23])
            navData[prn][epoch]['L2Codes'] = float(navLines[lineNum + 5][23:42])
            navData[prn][epoch]['GPS_Week'] = float(navLines[lineNum + 5][42:61])
            navData[prn][epoch]['L2PdataFlag'] = float(navLines[lineNum + 5][61:80])

            navData[prn][epoch]['SVaccuracy'] = float(navLines[lineNum + 6][4:23])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 6][23:42])
            navData[prn][epoch]['TGD'] = float(navLines[lineNum + 6][42:61])
            navData[prn][epoch]['IODC'] = float(navLines[lineNum + 6][61:80])

            navData[prn][epoch]['Transmission'] = float(navLines[lineNum + 7][4:23])

        elif gSys == 'E':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVclockDrift'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['SVclockDriftRate'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['IODnav'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['crs'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['DeltaN'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['M0'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['cuc'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['e'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['cus'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['roota'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['toe'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['cic'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['OMEGA0'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['cis'] = float(navLines[lineNum + 3][61:80])

            navData[prn][epoch]['i0'] = float(navLines[lineNum + 4][4:23])
            navData[prn][epoch]['crc'] = float(navLines[lineNum + 4][23:42])
            navData[prn][epoch]['omega'] = float(navLines[lineNum + 4][42:61])
            navData[prn][epoch]['OMEGA_DOT'] = float(navLines[lineNum + 4][61:80])

            navData[prn][epoch]['IDOT'] = float(navLines[lineNum + 5][4:23])
            navData[prn][epoch]['DataSources'] = float(navLines[lineNum + 5][23:42])
            navData[prn][epoch]['GAL_Week'] = float(navLines[lineNum + 5][42:61])
            navData[prn][epoch]['Spare'] = 0.0

            navData[prn][epoch]['SISA'] = float(navLines[lineNum + 6][4:23])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 6][23:42])
            navData[prn][epoch]['BGD_E5a_E1'] = float(navLines[lineNum + 6][42:61])
            navData[prn][epoch]['BGD_E5b_E1'] = float(navLines[lineNum + 6][61:80])

            navData[prn][epoch]['Transmission'] = float(navLines[lineNum + 7][4:23])

        elif gSys == 'R':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVrelativeFrequencyBias'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['MessageFrameTime'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['posX'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['velX'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['accelerationX'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['posY'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['velY'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['accelerationY'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['frequency'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['posZ'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['velZ'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['accelerationZ'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['operAge'] = float(navLines[lineNum + 3][61:80])
        elif gSys == 'J':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVclockDrift'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['SVclockDriftRate'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['IODE'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['crs'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['DeltaN'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['M0'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['cuc'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['e'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['cus'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['roota'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['toe'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['cic'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['OMEGA0'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['cis'] = float(navLines[lineNum + 3][61:80])

            navData[prn][epoch]['i0'] = float(navLines[lineNum + 4][4:23])
            navData[prn][epoch]['crc'] = float(navLines[lineNum + 4][23:42])
            navData[prn][epoch]['omega'] = float(navLines[lineNum + 4][42:61])
            navData[prn][epoch]['OMEGA_DOT'] = float(navLines[lineNum + 4][61:80])

            navData[prn][epoch]['IDOT'] = float(navLines[lineNum + 5][4:23])
            navData[prn][epoch]['L2Codes'] = float(navLines[lineNum + 5][23:42])
            navData[prn][epoch]['GPS_Week'] = float(navLines[lineNum + 5][42:61])
            navData[prn][epoch]['L2PdataFlag'] = float(navLines[lineNum + 5][61:80])

            navData[prn][epoch]['SVaccuracy'] = float(navLines[lineNum + 6][4:23])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 6][23:42])
            navData[prn][epoch]['TGD'] = float(navLines[lineNum + 6][42:61])
            navData[prn][epoch]['IODC'] = float(navLines[lineNum + 6][61:80])

            navData[prn][epoch]['Transmission'] = float(navLines[lineNum + 7][4:23])
            navData[prn][epoch]['FitIntervalFlag'] = float(navLines[lineNum + 7][23:42])
        elif gSys == 'S':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVrelativeFrequencyBias'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['Transmission'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['posX'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['velX'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['accelerationX'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['posY'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['velY'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['accelerationY'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['AccuracyCode'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['posZ'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['velZ'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['accelerationZ'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['IODN'] = float(navLines[lineNum + 3][61:80])
        elif gSys == 'I':
            navData[prn][epoch]['SVclockBias'] = float(navLines[lineNum][23:42])
            navData[prn][epoch]['SVclockDrift'] = float(navLines[lineNum][42:61])
            navData[prn][epoch]['SVclockDriftRate'] = float(navLines[lineNum][61:80])

            navData[prn][epoch]['IODEC'] = float(navLines[lineNum + 1][4:23])
            navData[prn][epoch]['crs'] = float(navLines[lineNum + 1][23:42])
            navData[prn][epoch]['DeltaN'] = float(navLines[lineNum + 1][42:61])
            navData[prn][epoch]['M0'] = float(navLines[lineNum + 1][61:80])

            navData[prn][epoch]['cuc'] = float(navLines[lineNum + 2][4:23])
            navData[prn][epoch]['e'] = float(navLines[lineNum + 2][23:42])
            navData[prn][epoch]['cus'] = float(navLines[lineNum + 2][42:61])
            navData[prn][epoch]['roota'] = float(navLines[lineNum + 2][61:80])

            navData[prn][epoch]['toe'] = float(navLines[lineNum + 3][4:23])
            navData[prn][epoch]['cic'] = float(navLines[lineNum + 3][23:42])
            navData[prn][epoch]['OMEGA0'] = float(navLines[lineNum + 3][42:61])
            navData[prn][epoch]['cis'] = float(navLines[lineNum + 3][61:80])

            navData[prn][epoch]['i0'] = float(navLines[lineNum + 4][4:23])
            navData[prn][epoch]['crc'] = float(navLines[lineNum + 4][23:42])
            navData[prn][epoch]['omega'] = float(navLines[lineNum + 4][42:61])
            navData[prn][epoch]['OMEGA_DOT'] = float(navLines[lineNum + 4][61:80])

            navData[prn][epoch]['IDOT'] = float(navLines[lineNum + 5][4:23])

            navData[prn][epoch]['IRN_Week'] = float(navLines[lineNum + 5][42:61])
            navData[prn][epoch]['Spare1'] = 0.0

            navData[prn][epoch]['RangeAccuracy'] = float(navLines[lineNum + 6][4:23])
            navData[prn][epoch]['SVhealth'] = float(navLines[lineNum + 6][23:42])
            navData[prn][epoch]['TGD'] = float(navLines[lineNum + 6][42:61])
            navData[prn][epoch]['Spare2'] = 0.0

            navData[prn][epoch]['Transmission'] = float(navLines[lineNum + 7][4:23])
        lineNum += addLine[gSys]
    return navData

def readNav4(navFile):
    ...

def readNav(navFile):
    navOpen = open(navFile, 'r+')
    navFirstLine = navOpen.readline()
    navOpen.close()
    rnxVersion = 0.0
    if 'RINEX VERSION / TYPE' in navFirstLine:
        rnxVersion = float(navFirstLine.split()[0])
    else:
        return None
    
    if 2 <= rnxVersion < 3:
        navData = readNav2(navFile)
    elif 3 <= rnxVersion < 4:
        navData = readNav3(navFile)
    # elif 4 <= rnxVersion < 5:
    #     navData = readNav4(navFile)
    else:
        print('versions of Rinex are not currently supported!')
        return None

    return navData

    
def is_nav(nav_file):
    '''
    Check whether the file is nav - by chang chuntao 2022.12.03
    '''
    try:
        nav_file_open = open(nav_file , 'r+')
        nav_file_line = nav_file_open.readline()
    except:
        return False
    nav_file_open.close()
    if 'RINEX VERSION / TYPE' in nav_file_line and nav_file_line[20] == 'N':
        return True
    else:
        return False
    

def getEpochListInNavData(navData):
    epochList = []
    for prn in navData:
        for epoch in navData[prn]:
            if epoch not in epochList:
                epochList.append(epoch)
    
    epochList = sorted(epochList)
    return epochList