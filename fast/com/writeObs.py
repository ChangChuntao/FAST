def writeObs(obsHead, obsData, obsFile):
    obsWrite = open(obsFile, 'w+')
    obsWrite.write('     3.05           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE\n')
    obsWrite.write('GNSSBOX             CHUNTAO CHANG                           PGM / RUN BY / DATE\n')
    obsWrite.write('GNSS RESEARCH CENTER, WUHAN UNIVERSITY (WHU), P. R. CHINA   COMMENT\n')
    for gnssSys in obsHead['OBS TYPES']:
        bandList = obsHead['OBS TYPES'][gnssSys]
        bandNum = len(bandList)
        firstLineBegin = gnssSys + '%5d' % bandNum
        otherLineBegin = 6 * ' '
        line = firstLineBegin
        for i, band in enumerate(bandList):
            i += 1
            line += ' ' + band
            if bandNum > 13 and i != 0 and i % 13 == 0:
                line += (60 - (len(line))) * ' '
                line += 'SYS / # / OBS TYPES\n'
                obsWrite.write(line)
                line = otherLineBegin
            elif bandNum > 13 and i == bandNum:
                line += (60 - (len(line))) * ' '
                line += 'SYS / # / OBS TYPES\n'
                obsWrite.write(line)

            elif bandNum <= 13 and i == bandNum:
                line += (60 - (len(line))) * ' '
                line += 'SYS / # / OBS TYPES\n'
                obsWrite.write(line)

    if obsHead['Receiver'] is not None and obsHead['Receiver Type'] is not None:
        obsWrite.write(obsHead['Receiver'].ljust(20) + obsHead['Receiver Type'].ljust(20) + '                    REC # / TYPE / VERS\n')
    if obsHead['Antenna'] is not None and obsHead['Antenna Type'] is not None:
        obsWrite.write(obsHead['Antenna'].ljust(20) + obsHead['Antenna Type'].ljust(20) + '                    ANT # / TYPE\n')

    firstObsTime = list(obsData)[0]
    lastObsTime = list(obsData)[-1]
    obsWrite.write(firstObsTime.strftime("  %Y    %m    %d    %H    %M    %S.%f     GPS         TIME OF FIRST OBS\n"))
    obsWrite.write(lastObsTime.strftime("  %Y    %m    %d    %H    %M    %S.%f     GPS         TIME OF LAST OBS\n"))
    obsWrite.write('                                                            END OF HEADER\n')
    
    for epoch in obsData:
        obsWrite.write(epoch.strftime("> %Y %m %d %H %M %S.%f0  0 {:02d}\n".format(len(obsData[epoch]))))
        for prn in obsData[epoch]:
            prnLine = prn
            for band in obsData[epoch][prn]:
                bandV = obsData[epoch][prn][band]
                if bandV is None:
                    bandV = 0.0
                prnLine += '%14.3f' % bandV + '  '
            prnLine += '\n'
            obsWrite.write(prnLine)

def reWriteObs(obsHead, obsData, checkBand, newObsFile, startDatetime = None, endDatetime = None):
    renewObsData = {}
    for epoch in obsData:
        if startDatetime is not None:
            if epoch < startDatetime:
                continue
        if endDatetime is not None:
            if epoch > endDatetime:
                break
        prnData = {}
        for prn in obsData[epoch]:
            if prn[0] not in list(checkBand):
                continue
            bandAllExist = True
            for band in checkBand[prn[0]]:
                if obsData[epoch][prn][band] is None:
                    bandAllExist = False
            if bandAllExist:
                prnData[prn] = obsData[epoch][prn]
        if prnData != {}:
            renewObsData[epoch] = prnData
    writeObs(obsHead, renewObsData, newObsFile)
    return obsHead, renewObsData


# checkBand = {'G': ['C1C', 'C2W', 'L1C', 'L2W'], 'C': ['C1P', 'C5P', 'L1P', 'L5P'], 'E': ['C1C', 'C5Q', 'L1C', 'L5Q']}

# obsFile = r'E:\Project\NOW\Pos\napos\resource\05071410.23o'
# outFile = obsFile.replace('.23o', '_re.23o')

# from gnssbox.com.ioGnss.readObs import readObs3, readObs3Head
# obsHead = readObs3Head(obsFile)
# obsData = readObs3(obsFile)
# reWriteObs(obsHead, obsData, checkBand=checkBand, newObsFile=outFile)