# -*- coding: utf-8 -*-
# writeClk       : Write the clk file
# Author         : Chang Chuntao chuntaochang@whu.edu.cn
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation Date  : 2022.06.27
# Latest Version : 2022.06.27


# 2022.06.27 : 写入钟差文件
#              by ChangChuntao -> Version : 1.00
def writeClk(clkData, clkFile, sortBy = 'epoch', vel = None):
    import sys
    # clkHead: 钟差文件头,见readClk.py
    # clkData: 钟差数据类型,见readClk.py
    # clkFile: 钟差文件位置
    clkHead = {}
    clkHead['RINEX VERSION'] = 3.0
    clkHead['PGM'] = 'GNSSBOX'
    clkHead['RUN BY'] = 'CHUNTAO CHANG'
    clkHead['TYPES OF DATA'] = ['AS']
    
    prnList = []
    epochList = []
    if sortBy == 'prn':
        prnList = list(clkData)
        for prn in clkData:
            for epoch in clkData[prn]:
                if epoch not in epochList:
                    epochList.append(epoch)
    else:
        for epoch in clkData:
            epochList.append(epoch)
            for prn in clkData[epoch]:
                if prn not in prnList:
                    prnList.append(prn)
    clkHead['INTERVAL'] = (epochList[1] - epochList[0]).total_seconds()
    clkHead['ANALYSIS CENTER'] = 'WHU  GNSS RESEARCH CENTER'
    clkHead['SOLN SATS'] = prnList

    # 文件写入
    clkFileWrite = open(clkFile, 'w+')

    # 写入头文件
    # 版本号,类型
    clkFileWrite.write('     ' + '%.2f' % clkHead[
        'RINEX VERSION'] + '           C                   M                   RINEX VERSION / TYPE\n')
    # 内容,组织
    clkFileWrite.write(
        str(clkHead['PGM']).ljust(20) + str(clkHead['RUN BY']).ljust(20) + '                    PGM / RUN BY / DATE \n')
    # 判断钟差写入类型
    if len(clkHead['TYPES OF DATA']) == 0:
        # 无卫星数据,则退出
        print('无数据!')
        sys.exit()
    elif len(clkHead['TYPES OF DATA']) == 1:
        clkFileWrite.write('     1    ' + clkHead['TYPES OF DATA'][
            0] + '                                                # / TYPES OF DATA   \n')
    elif len(clkHead['TYPES OF DATA']) == 2:
        clkFileWrite.write('     2    AR    AS                                          # / TYPES OF DATA   \n')
    # 时间格式
    clkFileWrite.write('   GPS                                                      TIME SYSTEM ID \n')
    # 'INTERVAL'
    if 'INTERVAL' in clkHead:
        if clkHead['INTERVAL'] is not None:
            clkFileWrite.write(str('%.2f' % clkHead['INTERVAL']).rjust(
                9) + '                                                   INTERVAL\n')
    # 组织单位
    clkFileWrite.write(str(clkHead['ANALYSIS CENTER']).ljust(60) + 'ANALYSIS CENTER\n')
    # 卫星数量
    clkFileWrite.write(str(len(clkHead['SOLN SATS'])).rjust(
        6) + '                                                      # OF SOLN SATS      \n')
    # PRN LIST
    prnListLen = int(len(clkHead['SOLN SATS']) / 15)
    LastPrnListLen = 15 - len(clkHead['SOLN SATS']) + int(len(clkHead['SOLN SATS']) / 15) * 15
    prnList = []
    for prn in clkHead['SOLN SATS']:
        prnList.append(str(prn))

    for prnListLenLine in range(0, prnListLen):
        line = ''
        for lineIndex in range(0, 15):
            line += prnList[prnListLenLine * 15 + lineIndex] + ' '
        clkFileWrite.write(line + 'PRN LIST\n')
    line = ''
    if LastPrnListLen > 0:
        for lineIndex in range(prnListLen * 15, len(clkHead['SOLN SATS'])):
            line += prnList[lineIndex] + ' '
        line += LastPrnListLen * '    '
        line += 'PRN LIST\n'
        clkFileWrite.write(line)
    # 文件头写入完成
    clkFileWrite.write('                                                            END OF HEADER     \n')

    if sortBy == 'prn':
        # 按时间写入
        # 所有历元列表 -> datetimeList
        datetimeList = []
        for prn in clkData:
            for epoch in clkData[prn]:
                if epoch not in datetimeList:
                    datetimeList.append(epoch)
        datetimeList.sort()
        # 主文件写入
        for epoch in datetimeList:
            for prn in clkData:
                for now_epoch in clkData[prn]:
                    if now_epoch == epoch:
                        if clkData[prn][now_epoch]['clkVel'] is None:
                            line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                                2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                                str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  1' + (
                                            '%.12E' % clkData[prn][now_epoch]['clk']).rjust(22)
                        else:
                            if vel is None:
                                line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                                    2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                                    str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  1' + (
                                                '%.12E' % clkData[prn][now_epoch]['clk']).rjust(22)
                            else:
                                line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                                    2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                                    str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  2' + (
                                                '%.12E' % clkData[prn][now_epoch]['clk']).rjust(22) + ('%.12E' % clkData[prn][now_epoch]['clkVel']).rjust(20)
                        clkFileWrite.write(line + '\n')
                        break
    else:
        for epoch in clkData:
            for prn in clkData[epoch]:
                if clkData[epoch][prn]['clkVel'] is None:
                    line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                        2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                        str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  1' + (
                                    '%.12E' % clkData[epoch][prn]['clk']).rjust(22)
                else:
                    if vel is None:
                        line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                            2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                            str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  1' + (
                                        '%.12E' % clkData[epoch][prn]['clk']).rjust(22)
                    else:
                        line = 'AS ' + str(prn).ljust(4) + ' ' + str(epoch.year) + ' ' + str(epoch.month).zfill(
                            2) + ' ' + str(epoch.day).zfill(2) + ' ' + str(epoch.hour).zfill(2) + ' ' + \
                            str(epoch.minute).zfill(2) + ('%.6f' % epoch.second).rjust(10) + '  2' + (
                                        '%.12E' % clkData[epoch][prn]['clk']).rjust(22) + ('%.12E' % clkData[epoch][prn]['clkVel']).rjust(20)
                clkFileWrite.write(line + '\n')


def cleanClk(clkFile, outFile):
    from fast.com.readClk import readClk
    clkData = readClk(clkFile)
    writeClk(clkData, clkFile=outFile)