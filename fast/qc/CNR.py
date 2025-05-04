import datetime

def writeCnr(cnrData, cnrFile):
    # cnrData[gnssSys][prn][band][epoch]
    cnrFileWrite = open(cnrFile, 'w+')
    cnrFileWrite.write('# PGM       : FAST\n')
    cnrFileWrite.write('# Author    : Chuntao Chang\n')
    cnrFileWrite.write('# Inf       : Carrier-to-Noise Ratio [dBHz]\n')
    cnrFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    cnrFileWrite.write('#             END OF HEADER\n')
    cnrFileWrite.write('\n')
    cnrSysData = {}
    cnrSatData = {}
    for gnssSys in cnrData:
        cnrSysData[gnssSys] = {}
        cnrSysData[gnssSys]['AVE'] = 0.0
        cnrSysData[gnssSys]['MIN'] = 999.0
        cnrSysData[gnssSys]['MAX'] = 0.0
        bandSysSum = 0.0
        bandSysNum = 0.0

        for prn in cnrData[gnssSys]:
            cnrSatData[prn] = {}
            for band in cnrData[gnssSys][prn]:
                cnrSatData[prn][band] = {}
                cnrSatData[prn][band]['AVE'] = 0.0
                cnrSatData[prn][band]['MIN'] = 999.0
                cnrSatData[prn][band]['MAX'] = 0.0
                bandSum = 0.0
                bandNum = 0.0
                for epoch in cnrData[gnssSys][prn][band]:
                    nowcnr = cnrData[gnssSys][prn][band][epoch]
                    if nowcnr > cnrSatData[prn][band]['MAX']:
                        cnrSatData[prn][band]['MAX'] = nowcnr
                    if nowcnr < cnrSatData[prn][band]['MIN']:
                        cnrSatData[prn][band]['MIN'] = nowcnr
                    if nowcnr > cnrSysData[gnssSys]['MAX']:
                        cnrSysData[gnssSys]['MAX'] = nowcnr
                    if nowcnr < cnrSysData[gnssSys]['MIN']:
                        cnrSysData[gnssSys]['MIN'] = nowcnr
                    bandSum += nowcnr
                    bandNum += 1
                    bandSysSum += nowcnr
                    bandSysNum += 1
                if bandNum == 0:
                    continue
                cnrSatData[prn][band]['AVE'] = bandSum / bandNum
        if bandSysNum != 0:
            cnrSysData[gnssSys]['AVE'] = bandSysSum / bandSysNum
    
    cnrFileWrite.write('+SYS\n')
    cnrFileWrite.write('    gSys   AVE   MIN   MAX\n')
    cnrFileWrite.write('--------------------------\n')
    for gnssSys in cnrSysData:
        line = str(gnssSys).rjust(8) + '%6.1f' % cnrSysData[gnssSys]['AVE'] + '%6.1f' % cnrSysData[gnssSys]['MIN'] + '%6.1f' % cnrSysData[gnssSys]['MAX'] + '\n'
        cnrFileWrite.write(line)
    cnrFileWrite.write('--------------------------\n')
    cnrFileWrite.write('+SYS\n')
    cnrFileWrite.write('\n')
    
    cnrFileWrite.write('+SAT\n')
    # cnrSatData[prn][band]
    cnrFileWrite.write(' prnFreq   AVE   MIN   MAX\n')
    cnrFileWrite.write('--------------------------\n')
    for prn in cnrSatData:
        for band in cnrSatData[prn]:
            prn_band = prn + '_' + band
            line = prn_band.rjust(8) + '%6.1f' % cnrSatData[prn][band]['AVE'] + '%6.1f' % cnrSatData[prn][band]['MIN'] + '%6.1f' % cnrSatData[prn][band]['MAX'] + '\n'
            cnrFileWrite.write(line)

    cnrFileWrite.write('--------------------------\n')
    cnrFileWrite.write('-SAT\n')
                



