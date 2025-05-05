# -*- coding: utf-8 -*-
# qtDownload        : pyqt5 for download module
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02


from PyQt5.QtCore import Qt, QDateTime, QSize, QThread, pyqtSignal
import subprocess
import os
import psutil
from os.path import expanduser
from PyQt5.QtGui import QFont, QPixmap
from fast.com.pub import gnss_type, yd_type, ym_type, yds_type, s_type, ydsh_type, ydh_type
from PyQt5.QtWidgets import QGridLayout, QComboBox, QFileDialog
from qbstyles import mpl_style
import time
import sys


class Worker(QThread):
    sig = pyqtSignal(object, str)

    def __init__(self, mainSelf, parent=None):
        super(Worker, self).__init__(parent)
        self.mainSelf = mainSelf

    def run(self):
        if run_not:
            if sys.platform == 'win32':
                st = subprocess.STARTUPINFO()
                st.dwFlags = subprocess.STARTF_USESHOWWINDOW
                st.wShowWindow = subprocess.SW_HIDE
            else:
                st = None
            self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      startupinfo=st)
            PID = self.p.pid
            while self.p.poll() is None:
                line = self.p.stdout.readline()
                line = line.strip()
                if line:
                    try:
                        line = line.decode('gbk')
                    except UnicodeDecodeError:
                        line = line.decode('utf-8', errors='ignore')
                    if 'Windows' not in line and 'wget' not in line and 'done' not in line and 'listing' not in line and 'required' not in line \
                            and '正在下载文件' not in line and '正在开始下载' not in line and len(
                        line.replace(' ',
                                     '')) != 0 and 'gzip' not in line and 'No such file or directory' not in line and \
                            '! Notice ! splicing RINEX files' not in line:
                        self.sig.emit(self.mainSelf,line)
                if PID == 0:
                    if self.mainSelf.chinese:
                        self.sig.emit(self.mainSelf,'下载结束')
                    else:
                        self.sig.emit(self.mainSelf,'Download completed')
                    break
        else:
            mypid = os.getpid()
            for proc in psutil.process_iter():
                if mypid != proc.pid:
                    if 'FAST.exe' in proc.name() or 'wget.exe' in proc.name() or 'lftp.exe' in proc.name() or \
                            'crx2rnx.exe' in proc.name() or 'gzip.exe' in proc.name():
                        if self.mainSelf.chinese:
                            self.sig.emit(self.mainSelf, '下载终止！')
                        else:
                            self.sig.emit(self.mainSelf, 'Download interrupted!')
                        proc.kill()

def dataTypeOnActivated(self):
    text = self.data_type_combo.currentText()
    # self.month_line.setEnabled(False)
    self.name_type_combo.clear()
    for gt in gnss_type:
        if text == gt[0]:
            for gt2 in gt[1]:
                self.name_type_combo.addItem(gt2)
    nameTypeOnActivated(self)
    # self.name_type_combo.setFont(font)

def nameTypeOnActivated(self):
    text = self.name_type_combo.currentText()
    if text not in ym_type:
        
        if self.chinese:
            self.month_line.setPlaceholderText("无需填写")
        else:
            self.month_line.setPlaceholderText("Input not required.")
        self.month_line.setEnabled(False)
    else:
        if self.chinese:
            self.month_line.setPlaceholderText("需填写")
        else:
            self.month_line.setPlaceholderText("Input required.")
        self.month_line.setEnabled(True)

    


# 打印log
def printLog(self, logStr):
    import datetime
    time.sleep(0.001)
    nowtimeStrft = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logStr = '[' + nowtimeStrft + ']: ' + logStr
    self.logPrint.setFontWeight(QFont.Normal)
    self.logPrint.append(logStr)

def choose_out_dir(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog   # 可选,禁用本地对话框
    if os.path.isdir(os.path.join(self.exeDirName, 'win_bin')):
        binDir = os.path.join(self.exeDirName, 'win_bin')
    else:
        binDir = os.path.join(self.exeDirName, 'mac_bin')
    open_path_file = os.path.join(binDir, 'open.path')
    if os.path.isfile(open_path_file):
        open_path_file_open = open(open_path_file, 'r+')
        open_path = open_path_file_open.readline()
        open_path_file_open.close()
    else:
        open_path = '~'
    if self.chinese:
        sel_out_dir_win = QFileDialog.getExistingDirectory(self, '选择下载路径', expanduser(open_path),
                                                        options=options)
    else:
        sel_out_dir_win = QFileDialog.getExistingDirectory(self, 'Select download path', expanduser(open_path),
                                                        options=options)

    self.out_dir_line.setText(sel_out_dir_win)

    if len(sel_out_dir_win) == 0:
        if self.chinese:
            printLog(self,'未选择！')
        else:
            printLog(self,'Download path not selected!')
    else:
        if self.chinese:
            printLog(self,'选择下载路径为 -> ' + sel_out_dir_win)
        else:
            printLog(self,'Selected download path -> ' + sel_out_dir_win)
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(sel_out_dir_win)
        open_path_file_open.close()

def choose_site_file(self):
    if os.path.isdir(os.path.join(self.exeDirName, 'win_bin')):
        binDir = os.path.join(self.exeDirName, 'win_bin')
    else:
        binDir = os.path.join(self.exeDirName, 'mac_bin')
    open_path_file = os.path.join(binDir, 'open.path')
    if os.path.isfile(open_path_file):
        open_path_file_open = open(open_path_file, 'r+')
        open_path = open_path_file_open.readline()
        open_path_file_open.close()
    else:
        open_path = '~'
    if self.chinese:
        filename, filetype = QFileDialog.getOpenFileName(self, "选取站点文件", expanduser(open_path),
                                                        "")
    else:
        filename, filetype = QFileDialog.getOpenFileName(self, "Select site inf. file", expanduser(open_path),
                                                        "")

    self.site_file_line.setText(filename)
    if len(filename) == 0:
        if self.chinese:
            printLog(self,'未选择！')
        else:
            printLog(self,'Site inf. file not selected!')
    else:
        printLog(self,'Selected site inf. file -> ' + filename)
        out_dir = str(filename).split(os.path.basename(filename))[0][:-1]
        open_path_file_open = open(open_path_file, 'w+')
        open_path_file_open.write(out_dir)
        open_path_file_open.close()

def dd(self):
    global cmd
    if os.path.isdir(os.path.join(self.exeDirName, 'win_bin')):
        binDir = os.path.join(self.exeDirName, 'win_bin')
    else:
        binDir = os.path.join(self.exeDirName, 'mac_bin')
    win_bin_fast = os.path.join(binDir, 'FAST')
    cmd = win_bin_fast
    type_name = self.name_type_combo.currentText()
    pool_num = self.pool_combo.currentText()
    unzip_str = self.unzip_combo.currentText()
    proname = self.pro_name_line.text()
    if self.chinese:
        printLog(self,'选择数据 -> ' + type_name)
        printLog(self,'下载并发 -> ' + pool_num)
        printLog(self,'是否解压 -> ' + unzip_str)
    else:
        printLog(self,'Data Name -> ' + type_name)
        printLog(self,'Thread    -> ' + pool_num)
        printLog(self,'Unzip     -> ' + unzip_str)

    cmd += ' -t ' + type_name
    if type_name in yd_type or type_name in yds_type or type_name in ym_type or type_name in ydsh_type or type_name in ydh_type:
        year = self.year_line.text()
        if year == '':
            if self.chinese:
                printLog(self,'请输入年份！')
            else:
                printLog(self,'Please enter the year!')
            return
        if not year.isdigit():
            if self.chinese:
                printLog(self,'请输入正确年份！')
            else:
                printLog(self,'Please enter a valid year!')
            return
        if self.chinese:
            printLog(self,'下载年份 -> ' + year)
        else:
            printLog(self,'Year -> ' + year)
        cmd += ' -y ' + year

    if type_name in yd_type or type_name in yds_type or type_name in ydsh_type or type_name in ydh_type:
        doy1 = self.begin_doy_line.text()
        doy2 = self.end_doy_line.text()
        if doy1 == '':
            if self.chinese:
                printLog(self,'请输入年积日！')
            else:
                printLog(self,'Please enter the doy!')
            return
        if not doy1.isdigit():
            if self.chinese:
                printLog(self,'请输入正确年积日！')
            else:
                printLog(self,'Please enter a valid doy!')
            return
        if doy2 == '':
            doy2 = doy1
        if not doy2.isdigit():
            if self.chinese:
                printLog(self,'请输入正确年积日！')
            else:
                printLog(self,'Please enter a valid doy!')
            return
        if self.chinese:
            printLog(self,'起始年积日 -> ' + doy1)
            printLog(self,'终止年积日 -> ' + doy2)
        else:
            printLog(self,'Start Doy -> ' + doy1)
            printLog(self,'Stop  Doy -> ' + doy2)
        cmd += ' -s ' + doy1
        cmd += ' -e ' + doy2

    if type_name in yds_type or type_name in s_type or type_name in ydsh_type:
        site_file = self.site_file_line.text()
        if site_file == '':
            if self.chinese:
                printLog(self,'请输入站点位置文件或站点名称！')
            else:
                printLog(self,'Please enter site inf. file or site name!')
            return
        if os.path.isfile(site_file):
            if self.chinese:
                printLog(self,'站点文件 -> ' + site_file)
            else:
                printLog(self,'Site inf. file -> ' + site_file)
            cmd += ' -f ' + site_file
        else:
            site_name = str(site_file).replace(' ', ',')
            cmd += ' -site ' + site_name

    if type_name in ym_type:
        month = self.month_line.text()
        if month == '':
            if self.chinese:
                printLog(self,'请输入月份！')
            else:
                printLog(self,'Please enter the month!')
            
            return
        if not month.isdigit():
            if self.chinese:
                printLog(self,'请输入正确月份！')
            else:
                printLog(self,'Please enter a valid month!')
            return
        if int(month) > 12 or int(month) < 1:
            if self.chinese:
                printLog(self,'请输入正确月份！')
            else:
                printLog(self,'Please enter a valid month!')
            return
        if self.chinese:
            printLog(self,'下载数据类型 -> ' + type_name)
            printLog(self,'下载月份 -> ' + month)
        else:
            printLog(self,'Data Type -> ' + type_name)
            printLog(self,'Month -> ' + month)

        cmd += ' -m ' + month
    if type_name in ydsh_type or type_name in ydh_type:
        hour = self.hour_combo.currentText()
        if hour != '0-23':
            if self.chinese:
                printLog(self,'下载小时 -> ' + hour)
            else:
                printLog(self,'Hour -> ' + hour)
            cmd += ' -hour ' + hour

    loc = self.out_dir_line.text()
    if loc != '' and not os.path.isdir(loc):
        if self.chinese:
            printLog(self,'请输入正确下载位置！')
        else:
            printLog(self,'Please enter a valid download path!')
        return
    if loc != '':
        if self.chinese:
            printLog(self,'下载路径 -> ' + loc)
        else:
            printLog(self,'Download path -> ' + loc)
        cmd += ' -l ' + loc
    cmd += ' -p ' + pool_num

    if unzip_str == '否':
        cmd += ' -u N'

    if len(proname) > 0:
        cmd += ' -r ' + proname

    print(cmd)
    
    if sys.platform != 'win32':
        cmd = cmd.split()
    printLog(self,'########################FAST########################')
    if self.chinese:
        printLog(self,'开始下载！')
    else:
        printLog(self,'Start downloading!')

    global run_not
    run_not = True
    self.thread = Worker(self)
    self.thread.sig.connect(printLog)
    self.thread.start()

def kill_p(self):
    global run_not
    mpl_style(dark=False)
    run_not = False
    self.thread = Worker(self)
    self.thread.sig.connect(printLog)
    self.thread.start()
