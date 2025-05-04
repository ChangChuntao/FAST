

import datetime

def writeSatNum(satNumData, satNumFile):
    #SatNum[prn][satNum]
    satNumFileWrite = open(satNumFile, 'w+')
    satNumFileWrite.write('# PGM       : FAST\n')
    satNumFileWrite.write('# Author    : Chuntao Chang\n')
    satNumFileWrite.write('# Inf       : satNum Count Statistics\n')
    satNumFileWrite.write('# Time      : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    satNumFileWrite.write('#             END OF HEADER\n')
    satNumFileWrite.write('\n')

    satLines = ['+SAT\n']

    firstLine = 'epoch'.rjust(20)
    firstLine += ' '
    for gSys in satNumData['stat']:
        firstLine += str(gSys).rjust(4)

    satLines.append(firstLine + '\n')
    
    for epoch in satNumData['data']:
        line = ' ' + epoch.strftime('%Y-%m-%d %H:%M:%S') + ' '
        for gSys in satNumData['stat']:
            line += '%4d' % satNumData['data'][epoch][gSys]
        line += '\n'
        satLines.append(line)
    satLines.append('-SAT\n')
    
    satNumFileWrite.write('+SYS\n')
    satNumFileWrite.write(' gSys  AVE  MIN  MAX\n')
    satNumFileWrite.write('--------------------\n')
    for gSys in satNumData['stat']:
        line = str(gSys).rjust(5) + '%5.1f' % satNumData['stat'][gSys]['AVE'] + '%5d' % satNumData['stat'][gSys]['MIN'] + '%5d' % satNumData['stat'][gSys]['MAX'] + '\n'
        satNumFileWrite.write(line)
    

    satNumFileWrite.write('--------------------\n')
    satNumFileWrite.write('-SYS\n')
    
    satNumFileWrite.write('\n')
    satNumFileWrite.writelines(satLines)
    