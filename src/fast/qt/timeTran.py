

from PyQt5.QtCore import QDateTime

def IsFloatNum(str):
    s = str.split('.')
    if 0 > len(s) > 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True
    
def time_tran(self):
    from PyQt5.QtWidgets import QMessageBox
    import fast.com.gnssTime as gnssTime
    year = self.year_text.text()
    month = self.month_text.text()
    day = self.day_text.text()

    yearofdoy = self.yearofdoy_text.text()
    doy = self.doy_text.text()

    gpsweek = self.gpsweek_text.text()
    gpsdayofweek = self.gpsdow_text.text()

    bdsweek = self.gpsweek_text.text()
    bdsdayofweek = self.bdsdow_text.text()

    mjd = self.mjd_text.text()
    sod = self.sod_text.text()

    if year.isdigit() and month.isdigit() and day.isdigit():
        year = int(year)
        if year < 1980:
            QMessageBox.information(self, "警告", "请输入大于1980的年份", QMessageBox.Yes)
            return
        month = int(month)
        if month < 1 or month > 12:
            QMessageBox.information(self, "警告", "请输入正确月份", QMessageBox.Yes)
            return
        day = int(day)
        if day < 1 or day > 32:
            QMessageBox.information(self, "警告", "请输入正确日期", QMessageBox.Yes)
            return
        nowdatetime = gnssTime.ymd2datetime(year, month, day)
    elif yearofdoy.isdigit() and doy.isdigit():
        yearofdoy = int(yearofdoy)
        if yearofdoy < 1980:
            QMessageBox.information(self, "警告", "请输入大于1980的年份", QMessageBox.Yes)
            return
        doy = int(doy)
        if doy > 366 or doy < 0:
            QMessageBox.information(self, "警告", "请输入正确年积日", QMessageBox.Yes)
            return
        nowdatetime = gnssTime.doy2datetime(yearofdoy, doy)
    elif gpsweek.isdigit() and gpsdayofweek.isdigit():
        gpsweek = int(gpsweek)
        if gpsweek < 0:
            QMessageBox.information(self, "警告", "请输入正确GPS周", QMessageBox.Yes)
            return
        gpsdayofweek = int(gpsdayofweek)
        if gpsdayofweek < 0 or gpsdayofweek > 6:
            QMessageBox.information(self, "警告", "请输入正确周内天", QMessageBox.Yes)
            return
        nowdatetime = gnssTime.gpswd2datetime(gpsweek, gpsdayofweek)
    elif bdsweek.isdigit() and bdsdayofweek.isdigit():
        bdsweek = int(bdsweek)
        if bdsdayofweek < 0:
            QMessageBox.information(self, "警告", "请输入正确BDS周", QMessageBox.Yes)
            return
        bdsdayofweek = int(bdsdayofweek)
        if bdsdayofweek < 0 or bdsdayofweek > 6:
            QMessageBox.information(self, "警告", "请输入正确周内天", QMessageBox.Yes)
            return
        nowdatetime = gnssTime.gpswd2datetime(bdsweek + 1356, bdsdayofweek)
    elif mjd.isdigit() and IsFloatNum(sod):
        mjd = int(mjd)
        if mjd < 0:
            QMessageBox.information(self, "警告", "请输入正确MJD", QMessageBox.Yes)
            return
        sod = float(sod)
        if sod < 0. or sod > 86400.:
            QMessageBox.information(self, "警告", "请输入正确天内秒", QMessageBox.Yes)
            return
        nowdatetime = gnssTime.mjd2datetime(mjd, sod)
    else:
        nowdatetime = self.dateTimeEdit.dateTime().toPyDateTime()
    
    gnss_time = gnssTime.datetime2allgnssTime(nowdatetime)
    self.dateTimeEdit.setDateTime(QDateTime(nowdatetime.year, nowdatetime.month, nowdatetime.day, nowdatetime.hour,
                                            nowdatetime.minute, nowdatetime.second))

    self.year_text.setText(str(gnss_time.year))
    self.month_text.setText(str(gnss_time.month))
    self.day_text.setText(str(gnss_time.day))

    self.yearofdoy_text.setText(str(gnss_time.year))
    self.doy_text.setText(str(gnss_time.doy))

    self.gpsweek_text.setText(str(gnss_time.gpsweek))
    self.gpsdow_text.setText(str(gnss_time.dow))

    self.bdsweek_text.setText(str(gnss_time.gpsweek - 1356))
    self.bdsdow_text.setText(str(gnss_time.dow))

    self.mjd_text.setText(str(gnss_time.mjd))
    self.sod_text.setText(str(gnss_time.sod))



def time_tran_none(self):
    self.year_text.clear()
    self.month_text.clear()
    self.day_text.clear()

    self.yearofdoy_text.clear()
    self.doy_text.clear()

    self.gpsweek_text.clear()
    self.gpsdow_text.clear()

    self.bdsweek_text.clear()
    self.bdsdow_text.clear()

    self.mjd_text.clear()
    self.sod_text.clear()

    self.dateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
