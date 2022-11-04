#!/usr/bin/python3
# GNSS_Timestran : GNSS_Timestran
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.25
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.11.02 - Version 1.25

from FAST_Print import PrintGDD
import datetime


# 2022-04-30 : datetime转GNSS TIME并输出
#              by Chang Chuntao  -> Version : 1.12
def datetime2GnssTime(specTime):
    """
    2022-04-30 : datetime转GNSS TIME并输出
                 by Chang Chuntao  -> Version : 1.12
    """
    YearMonthDay = [specTime.year, specTime.month, specTime.day]
    gpsWeekdDelTime = specTime - datetime.datetime(year=1980, month=1, day=6)
    gpsWeek = gpsWeekdDelTime.days // 7
    gpsWeekD = gpsWeekdDelTime.days - gpsWeek * 7
    GPSWeekDay = [gpsWeek, gpsWeekD]

    delTime = specTime - datetime.datetime(year=specTime.year, month=1, day=1)
    doy = delTime.days + 1
    YearDoy = [int(specTime.year), doy]

    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)  # 简化儒略日起始日
    mjd = (specTime - mjdT0).days
    sod = specTime.hour * 3600.0 + specTime.minute * 60.0 + specTime.second + specTime.microsecond / 1000000.0
    MjdSod = [int(mjd), sod]

    return YearMonthDay, GPSWeekDay, YearDoy, MjdSod


def gnssTime2datetime(gnssTime, gnssTimeType):
    """
    2022-04-30 : GNSS TIME转datetime
             by Chang Chuntao  -> Version : 1.12
    """
    gnssTime = gnssTime.split()
    if gnssTimeType == "YearMonthDay":
        dateTime = datetime.datetime(int(gnssTime[0]), int(gnssTime[1]), int(gnssTime[2]), 0, 0, 0, 0)
    elif gnssTimeType == "YearDoy":
        day1Time = datetime.datetime(int(gnssTime[0]), 1, 1, 0, 0, 0, 0)
        dateTime = day1Time + datetime.timedelta(days=int(gnssTime[1]) - 1)
    elif gnssTimeType == "GPSWeekDay":
        wd1Time = datetime.datetime(year=1980, month=1, day=6)
        dateTime = wd1Time + datetime.timedelta(weeks=int(gnssTime[0])) + datetime.timedelta(days=int(gnssTime[1]))
    elif gnssTimeType == "MjdSod":
        mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
        dateTime = mjdT0 + datetime.timedelta(days=int(gnssTime[0])) + datetime.timedelta(seconds=float(gnssTime[1]))
    else:
        PrintGDD("暂不支持此格式!", "fail")
        dateTime = datetime.datetime.utcnow()  # 获取当前utc时间
        PrintGDD("当前系统UTC时间为" + str(dateTime)[:-7], "normal")
        datetime2GnssTime(dateTime)

    return dateTime


def printTime(specTime, GPSWeekDay, YearDoy, MjdSod):
    """
    2022-05-25 : 输出时间
             by Chang Chuntao  -> Version : 1.13
    """
    PrintGDD("Year / Month / Day ".ljust(22) + ": " + str(specTime.year).ljust(5) + " " +
             str(specTime.month).zfill(2) + " " + str(specTime.day).zfill(2), "nothing")
    PrintGDD("Year / Doy ".ljust(22) + ": " + str(YearDoy[0]).ljust(5) + " " + str(YearDoy[1]).zfill(3), "nothing")
    PrintGDD("GPSWeek / DayofWeek ".ljust(22) + ": " + str(GPSWeekDay[0]).ljust(5) + " " + str(GPSWeekDay[1]),
             "nothing")
    PrintGDD("MJD / Sod ".ljust(22) + ": " + str(MjdSod[0]).ljust(5) + " " + str(MjdSod[1]), "nothing")


def gnssTimesTran():
    """
    2022-04-30 : GNSS_Timestran引导
             by Chang Chuntao  -> Version : 1.12
    """
    nowdatetime = datetime.datetime.utcnow()  # 获取当前utc时间
    PrintGDD("当前系统UTC时间为" + str(nowdatetime)[:-7], "normal")
    [YearMonthDaynow, GPSWeekDaynow, YearDoynow, MjdSodnow] = datetime2GnssTime(nowdatetime)
    printTime(nowdatetime, GPSWeekDaynow, YearDoynow, MjdSodnow)
    print("")
    PrintGDD("1. Year Month Day  2. Year Doy  3. GPSWeek DayofWeek  4. MJD SOD", "input")
    PrintGDD("请输入所需转换的时间格式编号 (eg. 2)", "input")
    inputTime = input("     ")
    while True:
        if inputTime.isdigit() and 0 < int(inputTime) < 5:
            inputTime = int(inputTime)
            if inputTime == 1:
                PrintGDD("请输入 Year Month Day (eg. 2022 04 29)", "input")
                YearMonthDay = input("     ")
                while True:
                    if len(YearMonthDay.split(" ")) == 3:
                        break
                    else:
                        PrintGDD("请输入正确的 Year Month Day (eg. 2022 04 30)", "input")
                        YearMonthDay = input("     ")
                specTime = gnssTime2datetime(YearMonthDay, "YearMonthDay")
                break
            elif inputTime == 2:
                PrintGDD("请输入 Year Doy (eg. 2022 119)", "input")
                YearDoy = input("     ")
                while True:
                    if len(YearDoy.split(" ")) == 2:
                        break
                    else:
                        PrintGDD("请输入正确的 Year Doy (eg. 2022 119)", "input")
                        YearDoy = input("     ")
                specTime = gnssTime2datetime(YearDoy, "YearDoy")
                break
            elif inputTime == 3:
                PrintGDD("请输入 GPSWeek DayofWeek (eg. 2207 5)", "input")
                GPSWeekDay = input("     ")
                while True:
                    if len(GPSWeekDay.split(" ")) == 2:
                        break
                    else:
                        PrintGDD("请输入正确的 GPSWeek DayofWeek (eg. 2207 5)", "input")
                        GPSWeekDay = input("     ")
                specTime = gnssTime2datetime(GPSWeekDay, "GPSWeekDay")
                break
            elif inputTime == 4:
                PrintGDD("请输入 MJD SOD (eg. 59698 69656.17121)", "input")
                MjdSod = input("     ")
                while True:
                    if len(MjdSod.split(" ")) == 2:
                        break
                    else:
                        PrintGDD("请输入正确的 MJD SOD (eg. 59698 69656.17121)", "input")
                        MjdSod = input("     ")
                specTime = gnssTime2datetime(MjdSod, "MjdSod")
                break
        else:
            PrintGDD("请输入正确的编号 (eg. 2)", "input")
            inputTime = input("     ")
    [YearMonthDay, GPSWeekDay, YearDoy, MjdSod] = datetime2GnssTime(specTime)
    printTime(specTime, GPSWeekDay, YearDoy, MjdSod)
    print("")
    return 0


###########################datetime->other############################
def datetime2ymd(specTime):
    """
    2022.09.30 : datetime -> mjd
             by ChangChuntao -> Version : 1.00
    """
    return specTime.year, specTime.month, specTime.day


def datetime2doy(specTime):
    """
    2022.09.30 : datetime -> ydoy
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    doy = (specTime - datetime.datetime(year=specTime.year, month=1, day=1)).days + 1
    return specTime.year, doy


def datetime2mjd(specTime):
    """
    2022.09.30 : datetime -> mjd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    mjd = (specTime - mjdT0).days
    sod = specTime.hour * 3600.0 + specTime.minute * 60.0 + specTime.second + specTime.microsecond / 1000000.0
    return mjd, sod


def datetime2gpswd(specTime):
    """
    2022.09.30 : datetime -> gpswd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    gpsWeekdDelTime = specTime - datetime.datetime(year=1980, month=1, day=6)
    gpsWeek = gpsWeekdDelTime.days // 7
    gpsWeekD = gpsWeekdDelTime.days - gpsWeek * 7
    return gpsWeek, gpsWeekD


###########################datetime->other############################


##############################ymd->other##############################
def ymd2datetime(year, month, day):
    """
    2022.09.30 : ymd -> datetime
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    specTime = datetime.datetime(year, month, day)
    return specTime


def ymd2doy(year, month, day):
    """
    2022.09.30 : ymd -> doy
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    specTime = datetime.datetime(year, month, day)
    doy = (specTime - datetime.datetime(year=specTime.year, month=1, day=1)).days + 1
    return specTime.year, doy


def ymd2mjd(year, month, day):
    """
    2022.09.30 : ymd -> mjd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    specTime = datetime.datetime(year, month, day)
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    mjd = (specTime - mjdT0).days
    sod = specTime.hour * 3600.0 + specTime.minute * 60.0 + specTime.second + specTime.microsecond / 1000000.0
    return mjd, sod


def ymd2gpswd(year, month, day):
    """
    2022.09.30 : ymd -> gpswd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    specTime = datetime.datetime(year, month, day)
    gpsWeekdDelTime = specTime - datetime.datetime(year=1980, month=1, day=6)
    gpsWeek = gpsWeekdDelTime.days // 7
    gpsWeekD = gpsWeekdDelTime.days - gpsWeek * 7
    return gpsWeek, gpsWeekD


##############################ymd->other##############################

##############################doy->other##############################
def doy2datetime(year, doy):
    """
    2022.09.30 : year doy -> datetime
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    day1Time = datetime.datetime(year, 1, 1)
    specTime = day1Time + datetime.timedelta(days=int(doy) - 1)
    return specTime


def doy2ymd(year, doy):
    """
    2022.09.30 : year doy -> ymd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    day1Time = datetime.datetime(year, 1, 1)
    specTime = day1Time + datetime.timedelta(days=int(doy) - 1)
    return specTime.year, specTime.month, specTime.day


def doy2gpswd(year, doy):
    """
    2022.09.30 : year doy -> gpswd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    day1Time = datetime.datetime(year, 1, 1)
    specTime = day1Time + datetime.timedelta(days=int(doy) - 1)
    gpsWeekdDelTime = specTime - datetime.datetime(year=1980, month=1, day=6)
    gpsWeek = gpsWeekdDelTime.days // 7
    gpsWeekD = gpsWeekdDelTime.days - gpsWeek * 7
    return gpsWeek, gpsWeekD


def doy2mjd(year, doy):
    """
    2022.09.30 : year doy -> mjd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    day1Time = datetime.datetime(year, 1, 1)
    specTime = day1Time + datetime.timedelta(days=int(doy) - 1)
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    mjd = (specTime - mjdT0).days
    sod = specTime.hour * 3600.0 + specTime.minute * 60.0 + specTime.second + specTime.microsecond / 1000000.0
    return mjd, sod


##############################doy->other##############################

##############################mjd->other##############################
def mjd2datetime(mjd, sod=0.0):
    """
    2022.09.30 : mjd -> datetime
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    specTime = mjdT0 + datetime.timedelta(days=int(mjd)) + datetime.timedelta(seconds=float(sod))
    return specTime


def mjd2ymd(mjd, sod=0.0):
    """
    2022.09.30 : mjd -> ymd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    specTime = mjdT0 + datetime.timedelta(days=int(mjd)) + datetime.timedelta(seconds=float(sod))
    return specTime.year, specTime.month, specTime.day


def mjd2doy(mjd, sod=0.0):
    """
    2022.09.30 : mjd -> doy
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    specTime = mjdT0 + datetime.timedelta(days=int(mjd)) + datetime.timedelta(seconds=float(sod))
    doy = (specTime - datetime.datetime(year=specTime.year, month=1, day=1)).days + 1
    return specTime.year, doy


def mjd2gpswd(mjd, sod=0.0):
    """
    2022.09.30 : mjd -> gpswd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    specTime = mjdT0 + datetime.timedelta(days=int(mjd)) + datetime.timedelta(seconds=float(sod))
    gpsWeekdDelTime = specTime - datetime.datetime(year=1980, month=1, day=6)
    gpsWeek = gpsWeekdDelTime.days // 7
    gpsWeekD = gpsWeekdDelTime.days - gpsWeek * 7
    return gpsWeek, gpsWeekD


def sod2hms(sod):
    """
    2022.09.30 : Convert integer second in one day to hour minute second
             by ChangChuntao -> Version : 1.00
    """
    sec = sod
    hour = sec // 3600
    sec -= hour * 3600
    if (sec < 0):
        hour -= 1
        sec += 3600
    minu = sec // 60
    sec -= minu * 60
    return hour, minu, sec


##############################mjd->other##############################


#############################gpswd->other#############################
def gpswd2datetime(gpsWeek, gpsWeekD):
    """
    2022.09.30 : gpswd -> datetime
             by ChangChuntao -> Version : 1.00
    """
    import datetime

    wd1Time = datetime.datetime(year=1980, month=1, day=6)
    specTime = wd1Time + datetime.timedelta(weeks=int(gpsWeek)) + datetime.timedelta(days=int(gpsWeekD))
    return specTime


def gpswd2ymd(gpsWeek, gpsWeekD):
    """
    2022.09.30 : gpswd -> ymd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    wd1Time = datetime.datetime(year=1980, month=1, day=6)
    specTime = wd1Time + datetime.timedelta(weeks=int(gpsWeek)) + datetime.timedelta(days=int(gpsWeekD))
    return specTime.year, specTime.month, specTime.day


def gpswd2doy(gpsWeek, gpsWeekD):
    """
    2022.09.30 : gpswd -> year doy
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    wd1Time = datetime.datetime(year=1980, month=1, day=6)
    specTime = wd1Time + datetime.timedelta(weeks=int(gpsWeek)) + datetime.timedelta(days=int(gpsWeekD))
    doy = (specTime - datetime.datetime(year=specTime.year, month=1, day=1)).days + 1
    return specTime.year, doy


def gpswd2mjd(gpsWeek, gpsWeekD):
    """
    2022.09.30 : gpswd -> mjd
             by ChangChuntao -> Version : 1.00
    """
    import datetime
    wd1Time = datetime.datetime(year=1980, month=1, day=6)
    specTime = wd1Time + datetime.timedelta(weeks=int(gpsWeek)) + datetime.timedelta(days=int(gpsWeekD))
    mjdT0 = datetime.datetime(1858, 11, 17, 0, 0, 0, 0)
    mjd = (specTime - mjdT0).days
    sod = specTime.hour * 3600.0 + specTime.minute * 60.0 + specTime.second + specTime.microsecond / 1000000.0
    return mjd, sod
#############################gpswd->other#############################
