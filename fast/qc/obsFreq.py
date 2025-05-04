

import datetime

def writeFreqData(freqData, freqFile):
    #freqData[prn][freq]
    freqFileWrite = open(freqFile, 'w+')
    freqFileWrite.write('# PGM       : FAST\n')
    freqFileWrite.write('# Author    : Chuntao Chang\n')
    freqFileWrite.write('# Inf       : Frequency Count Statistics\n')
    freqFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    freqFileWrite.write('#             END OF HEADER\n')
    freqSysData = {}
    freqFileWrite.write('\n')
    satLines = []
    satLines.append('+SAT\n')
    for prn in freqData:
        gSys = prn[0]
        if gSys not in freqSysData:
            freqSysData[gSys] = {}
        line = ' ' + prn + ' -'
        for freq in freqData[prn]:
            if freq not in freqSysData[gSys]:
                freqSysData[gSys][freq] = 0
            freqSysData[gSys][freq] += freqData[prn][freq]
            line += ' ' + freq + ': ' + '%7d' % freqData[prn][freq]
        line += '\n'
        satLines.append(line)
    satLines.append('-SAT\n')
    
    freqFileWrite.write('+SYS\n')
    for gSys in freqSysData:
        line = ' ' + gSys + '   -'
        for freq in freqSysData[gSys]:
            line += ' ' + freq + ': ' + '%7d' % freqSysData[gSys][freq]
        line += '\n'
        freqFileWrite.write(line)
    freqFileWrite.write('-SYS\n')
    freqFileWrite.write('\n')
    freqFileWrite.writelines(satLines)


