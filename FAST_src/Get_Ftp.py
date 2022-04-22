#!/usr/bin/python3
# GET_Ftp        : Reconstruct FTP address
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.00
# Date           : 2022.03.27

from datetime import datetime, timedelta

from FTP_Source import FTP_S
from MGEX_name import mgex


def getftp(t, y, d):
    yeard1 = '%04d' % y + '-01-01 00:00:00'
    yeard1 = datetime.strptime(yeard1, '%Y-%m-%d %H:%M:%S')
    spectime = yeard1 + timedelta(days=d - 1)
    ftpsite = FTP_S[t]
    ftpsiteout = []
    for fd in ftpsite:
        ftpsiteout.append(ReplaceTimeWildcard(fd, spectime))
    return ftpsiteout


# Replace time wild cards in string with specific date time
def ReplaceTimeWildcard(string, spectime):
    """Replace time wild cards in string with specific date time"""
    import datetime
    newstr = str(string)
    # replace four digit GPS week
    if newstr.find('<GPSW>') >= 0:
        deltime = spectime - datetime.datetime(year=1980, month=1, day=6)
        gpsweek = deltime.days // 7
        newstr = newstr.replace('<GPSW>', '%04d' % gpsweek)
    # replace four digit GPS week and one digit week day
    if newstr.find('<GPSWD>') >= 0:
        deltime = spectime - datetime.datetime(year=1980, month=1, day=6)
        gpsweek = deltime.days // 7
        gpswday = deltime.days - gpsweek * 7
        newstr = newstr.replace('<GPSWD>', '%04d%1d' % (gpsweek, gpswday))
    # replace four digit year
    if newstr.find('<YEAR>') >= 0:
        newstr = newstr.replace('<YEAR>', '%04d' % spectime.year)
    if newstr.find('<YYYY>') >= 0:
        newstr = newstr.replace('<YYYY>', '%04d' % spectime.year)
    if newstr.find('<YY>') >= 0:
        newstr = newstr.replace('<YY>', '%02d' % (spectime.year % 100))
    # replace three digit day number in year
    if newstr.find('<DOY>') >= 0:
        deltime = spectime - datetime.datetime(year=spectime.year, month=1, day=1)
        newstr = newstr.replace('<DOY>', '%03d' % (deltime.days + 1))
    if newstr.find('<DDD>') >= 0:
        newstr = newstr.replace('<DDD>', spectime.strftime('%j'))
    # replace two digit month in year
    if newstr.find('<MONTH>') >= 0:
        newstr = newstr.replace('<MONTH>', '%02d' % spectime.month)
    # replace two digit day in month
    if newstr.find('<DAY>') >= 0:
        newstr = newstr.replace('<DAY>', '%02d' % spectime.day)
    # replace two digit hour in day
    if newstr.find('<HOUR>') >= 0:
        newstr = newstr.replace('<HOUR>', '%02d' % spectime.hour)
    # replace two digit minute in hour
    if newstr.find('<MINUTE>') >= 0:
        newstr = newstr.replace('<MINUTE>', '%02d' % spectime.minute)
    # replace two digit second in minute
    if newstr.find('<SECOND>') >= 0:
        newstr = newstr.replace('<SECOND>', '%02d' % spectime.second)
    # return new string
    return newstr


def ReplaceMMM(url, month):
    newurl = str(url)
    if month == 1:
        month = "JAN"
    elif month == 2:
        month = "FEB"
    elif month == 3:
        month = "MAR"
    elif month == 4:
        month = "APR"
    elif month == 5:
        month = "MAY"
    elif month == 6:
        month = "JUN"
    elif month == 7:
        month = "JUL"
    elif month == 8:
        month = "AUG"
    elif month == 9:
        month = "SEP"
    elif month == 10:
        month = "OCT"
    elif month == 11:
        month = "NOV"
    elif month == 12:
        month = "DEC"
    newurl = newurl.replace('<MMM>', month)
    return newurl


def ReplaceMM(url, month):
    newurl = str(url)
    month = int(month)
    newurl = newurl.replace('<MM>', '%02d'%month)
    return newurl


def getsite(file, datatype):
    site = open(file, "r").readlines()[0].split(" ")
    if datatype == "MGEX_IGS_rnx" or datatype == "MGEX_HK_cors":
        for s in range(0, len(site)):
            if len(site[s]) == 9:
                continue
            else:
                for m in mgex:
                    if site[s] == m[0]:
                        site[s] = m[1]
    else:
        for s in range(0, len(site)):
            site[s] = site[s].lower()[0:4]
    return site
