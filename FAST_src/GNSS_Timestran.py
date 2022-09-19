#!/usr/bin/python3
# GNSS_Timestran : GNSS_Timestran
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 1.10
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2022.04.30 - Version 1.12

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