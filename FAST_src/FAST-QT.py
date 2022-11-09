import os
import subprocess
import sys
import time
from os.path import expanduser
import psutil
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QComboBox, QFileDialog, QTextEdit, QMessageBox
import GNSS_Timestran
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QDateTime, QSize, pyqtSlot, QProcess, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QFrame, QWidget, QSplitter, QLabel, \
    QPushButton, QLineEdit, QVBoxLayout, QDateTimeEdit
from QT_Frame import FramelessWindow
from GNSS_TYPE import gnss_type, yd_type, ym_type, no_type, yds_type, s_type
import qdarkstyle


class Worker(QThread):
    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

    def run(self):
        if run_not:
            st = subprocess.STARTUPINFO()
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE

            self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      startupinfo=st)
            PID = self.p.pid
            while self.p.poll() is None:
                line = self.p.stdout.readline()
                line = line.strip()
                if line:
                    line = line.decode('gbk')
                    if 'Windows' not in line and 'wget' not in line and 'done' not in line and 'listing' not in line and 'required' not in line \
                            and '正在下载文件' not in line and '正在开始下载' not in line and len(
                        line.replace(' ', '')) != 0:
                        self.sig.emit(line)
                if PID == 0:
                    self.sig.emit('下载结束')
                    break
        else:
            mypid = os.getpid()
            for proc in psutil.process_iter():
                if mypid != proc.pid:
                    if 'FAST.exe' in proc.name() or 'wget.exe' in proc.name() or 'lftp.exe' in proc.name() or \
                            'crx2rnx.exe' in proc.name() or 'gzip.exe' in proc.name():
                        self.sig.emit('下载终止！')
                        proc.kill()


def IsFloatNum(str):
    s = str.split('.')
    if 0 > len(s) > 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True


class mainWindow(QMainWindow):
    move_Flag = False
    Window_Width = 1150
    Window_Length = 1000
    Window_Title = 'FAST-大地测量数据下载软件V2.0'

    def __init__(self):
        super().__init__()  # 继承类
        self.initUI()
        self.show()

    def initUI(self):

        # self.setWindowFlag(Qt.FramelessWindowHint)
        #
        self.setWindowTitle(self.Window_Title)
        global font
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setFamily('Microsoft YaHei')

        lable_size = 100
        lable_h = 40
        choose_size = 290
        choose_h = 18

        # ------------------标题栏-------------------
        self.resize(self.Window_Width, self.Window_Length)
        self.setWindowOpacity(0.75)

        self.setWindowIcon(QtGui.QIcon("./win_bin/WHU.png"))
        self.status = self.statusBar()
        self.status.showMessage("武汉大学-GNSS中心")
        self.showName = QLabel("作者：常春涛")
        self.showName.setFont(font)
        # self.showEmail = QLabel("邮箱:1252443496@qq.com")
        self.showWechat = QLabel("微信:amst-jazz")
        self.showWechat.setFont(font)

        self.status.addPermanentWidget(self.showName, stretch=0)  # 比例
        self.status.addPermanentWidget(self.showWechat, stretch=0)
        # ------------------标题栏-------------------

        # ----------------左侧控件布局----------------

        datetime_Label_box = QHBoxLayout()
        datetime_Label = QLabel("UTC Datetime")
        datetime_Label.setFont(font)
        datetime_Label.setAlignment(Qt.AlignCenter)
        datetime_Label_box.addWidget(datetime_Label)
        datetime_Label_wg = QWidget()
        datetime_Label_wg.setLayout(datetime_Label_box)

        dateTimeEdit_box = QHBoxLayout()
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.dateTimeEdit.setFont(font)
        dateTimeEdit_box.addWidget(self.dateTimeEdit)
        dateTimeEdit_wg = QWidget()
        dateTimeEdit_wg.setLayout(dateTimeEdit_box)

        year_Label_box = QHBoxLayout()
        year_Label = QLabel("Year")
        year_Label.setAlignment(Qt.AlignCenter)
        year_Label.setFont(font)
        month_Label = QLabel("Month")
        month_Label.setFont(font)
        month_Label.setAlignment(Qt.AlignCenter)
        day_Label = QLabel("Day")
        day_Label.setFont(font)
        day_Label.setAlignment(Qt.AlignCenter)
        year_Label_box.addWidget(year_Label)
        year_Label_box.addWidget(month_Label)
        year_Label_box.addWidget(day_Label)
        year_Label_wg = QWidget()
        year_Label_wg.setLayout(year_Label_box)

        ymd_box = QHBoxLayout()
        self.year_text = QLineEdit(self)
        self.year_text.setFont(font)
        self.year_text.setAlignment(Qt.AlignCenter)
        self.month_text = QLineEdit(self)
        self.month_text.setFont(font)
        self.month_text.setAlignment(Qt.AlignCenter)
        self.day_text = QLineEdit(self)
        self.day_text.setAlignment(Qt.AlignCenter)
        self.day_text.setFont(font)
        ymd_box.addWidget(self.year_text)
        ymd_box.addWidget(self.month_text)
        ymd_box.addWidget(self.day_text)
        ymd_wg = QWidget()
        ymd_wg.setLayout(ymd_box)

        ydoy_Label_box = QHBoxLayout()
        ydoy_Label = QLabel("Year")
        ydoy_Label.setFont(font)
        ydoy_Label.setAlignment(Qt.AlignCenter)
        doy_Label = QLabel("Doy")
        doy_Label.setFont(font)
        doy_Label.setAlignment(Qt.AlignCenter)
        ydoy_Label_box.addWidget(ydoy_Label)
        ydoy_Label_box.addWidget(doy_Label)
        ydoy_Label_wg = QWidget()
        ydoy_Label_wg.setLayout(ydoy_Label_box)

        ydoy_box = QHBoxLayout()
        self.yearofdoy_text = QLineEdit(self)
        self.yearofdoy_text.setFont(font)
        self.yearofdoy_text.setAlignment(Qt.AlignCenter)
        self.doy_text = QLineEdit(self)
        self.doy_text.setFont(font)
        self.doy_text.setAlignment(Qt.AlignCenter)
        ydoy_box.addWidget(self.yearofdoy_text)
        ydoy_box.addWidget(self.doy_text)
        ydoy_wg = QWidget()
        ydoy_wg.setLayout(ydoy_box)

        gpsweekd_Label_box = QHBoxLayout()
        gpsweek_Label = QLabel("GPS Week")
        gpsweek_Label.setFont(font)
        gpsweek_Label.setAlignment(Qt.AlignCenter)
        gps_dow_Label = QLabel("Day of Week")
        gps_dow_Label.setFont(font)
        gps_dow_Label.setAlignment(Qt.AlignCenter)
        gpsweekd_Label_box.addWidget(gpsweek_Label)
        gpsweekd_Label_box.addWidget(gps_dow_Label)
        gpsweekd_Label_wg = QWidget()
        gpsweekd_Label_wg.setLayout(gpsweekd_Label_box)

        gpsweekd_box = QHBoxLayout()
        self.gpsweek_text = QLineEdit(self)
        self.gpsweek_text.setFont(font)
        self.gpsweek_text.setAlignment(Qt.AlignCenter)
        self.gpsdow_text = QLineEdit(self)
        self.gpsdow_text.setFont(font)
        self.gpsdow_text.setAlignment(Qt.AlignCenter)
        gpsweekd_box.addWidget(self.gpsweek_text)
        gpsweekd_box.addWidget(self.gpsdow_text)
        gpsweekd_wg = QWidget()
        gpsweekd_wg.setLayout(gpsweekd_box)

        bdsweekd_Label_box = QHBoxLayout()
        bdsweek_Label = QLabel("BDS week")
        bdsweek_Label.setFont(font)
        bdsweek_Label.setAlignment(Qt.AlignCenter)
        bds_dow_Label = QLabel("Day of Week")
        bds_dow_Label.setFont(font)
        bds_dow_Label.setAlignment(Qt.AlignCenter)
        bdsweekd_Label_box.addWidget(bdsweek_Label)
        bdsweekd_Label_box.addWidget(bds_dow_Label)
        bdsweekd_Label_wg = QWidget()
        bdsweekd_Label_wg.setLayout(bdsweekd_Label_box)

        bdsweekd_box = QHBoxLayout()
        self.bdsweek_text = QLineEdit(self)
        self.bdsweek_text.setFont(font)
        self.bdsweek_text.setAlignment(Qt.AlignCenter)
        self.bdsdow_text = QLineEdit(self)
        self.bdsdow_text.setFont(font)
        self.bdsdow_text.setAlignment(Qt.AlignCenter)
        bdsweekd_box.addWidget(self.bdsweek_text)
        bdsweekd_box.addWidget(self.bdsdow_text)
        bdsweekd_wg = QWidget()
        bdsweekd_wg.setLayout(bdsweekd_box)

        mjdsod_Label_box = QHBoxLayout()
        mjd_Label = QLabel("MJD")
        mjd_Label.setFont(font)
        mjd_Label.setAlignment(Qt.AlignCenter)
        sod_Label = QLabel("SOD")
        sod_Label.setFont(font)
        sod_Label.setAlignment(Qt.AlignCenter)
        mjdsod_Label_box.addWidget(mjd_Label)
        mjdsod_Label_box.addWidget(sod_Label)
        mjdsod_Label_wg = QWidget()
        mjdsod_Label_wg.setLayout(mjdsod_Label_box)

        none_Label_box = QHBoxLayout()
        none_Label = QLabel("")
        none_Label_box.addWidget(none_Label)
        none_Label_wg = QWidget()
        none_Label_wg.setLayout(none_Label_box)

        mjdsod_box = QHBoxLayout()
        self.mjd_text = QLineEdit(self)
        self.mjd_text.setAlignment(Qt.AlignCenter)
        self.mjd_text.setFont(font)
        self.sod_text = QLineEdit(self)
        self.sod_text.setAlignment(Qt.AlignCenter)
        self.sod_text.setFont(font)
        mjdsod_box.addWidget(self.mjd_text)
        mjdsod_box.addWidget(self.sod_text)
        mjdsod_wg = QWidget()
        mjdsod_wg.setLayout(mjdsod_box)

        time_tran_box = QHBoxLayout()
        time_tran_btn = QPushButton('转换', self)
        time_tran_btn.setFont(font)
        time_tran_btn.setMinimumSize(QSize(120, 30))
        time_tran_btn.clicked.connect(self.time_tran)

        time_tran_none_btn = QPushButton('清空', self)
        time_tran_none_btn.setFont(font)
        time_tran_none_btn.setMinimumSize(QSize(120, 30))
        time_tran_none_btn.clicked.connect(self.time_tran_none)

        time_tran_box.addWidget(time_tran_btn)
        time_tran_box.addWidget(time_tran_none_btn)
        time_tran_wg = QWidget()
        time_tran_wg.setLayout(time_tran_box)

        gnss_time_box = QVBoxLayout()
        gnss_time_box.setSpacing(0)
        gnss_time_box.addStretch(0)
        gnss_time_box.addWidget(datetime_Label_wg)
        gnss_time_box.addWidget(dateTimeEdit_wg)
        gnss_time_box.addWidget(year_Label_wg)
        gnss_time_box.addWidget(ymd_wg)
        gnss_time_box.addWidget(ydoy_Label_wg)
        gnss_time_box.addWidget(ydoy_wg)
        gnss_time_box.addWidget(gpsweekd_Label_wg)
        gnss_time_box.addWidget(gpsweekd_wg)
        gnss_time_box.addWidget(bdsweekd_Label_wg)
        gnss_time_box.addWidget(bdsweekd_wg)
        gnss_time_box.addWidget(mjdsod_Label_wg)
        gnss_time_box.addWidget(mjdsod_wg)

        gnss_time_box.addStretch(10)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(time_tran_wg)

        splitterLeft_in = QFrame()
        splitterLeft_in.setFrameShape(QFrame.StyledPanel)
        splitterLeft_in.setLayout(gnss_time_box)

        # 添加到左侧控件布局
        splitterLeft = QSplitter(Qt.Vertical)
        splitterLeft.addWidget(splitterLeft_in)

        # ----------------左侧控件布局----------------

        # ----------------右侧控件布局----------------
        # |--数据下载 -> 右侧上方
        type_choose_lay = QGridLayout()
        type_choose_lay.setSpacing(20)

        data_type_lable = QLabel('数据类型')
        data_type_lable.setFont(font)
        data_type_lable.setAlignment(Qt.AlignRight)
        data_type_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(data_type_lable, 1, 0)

        data_type_combo = QComboBox(self)
        for gt in gnss_type:
            data_type_combo.addItem(gt[0])
        data_type_combo.setFont(font)
        data_type_combo.textActivated[str].connect(self.onActivated)
        data_type_combo.setMinimumSize(QSize(choose_size, choose_h + 20))
        type_choose_lay.addWidget(data_type_combo, 1, 1, 1, 2)

        name_type_lable = QLabel('数据名称')
        name_type_lable.setFont(font)
        name_type_lable.setAlignment(Qt.AlignRight)
        name_type_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(name_type_lable, 1, 3)

        self.name_type_combo = QComboBox(self)
        self.name_type_combo.clear()
        for gt2 in gnss_type[0][1]:
            self.name_type_combo.addItem(gt2)
        self.name_type_combo.setFont(font)
        self.name_type_combo.setMinimumSize(QSize(choose_size, choose_h + 20))
        type_choose_lay.addWidget(self.name_type_combo, 1, 4, 1, 2)

        year_lable = QLabel('下载年份')
        year_lable.setFont(font)
        year_lable.setAlignment(Qt.AlignRight)
        year_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(year_lable, 2, 0)

        self.year_line = QLineEdit(self)
        self.year_line.setFont(font)
        self.year_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.year_line, 2, 1, 1, 2)

        month_lable = QLabel('下载月份')
        month_lable.setFont(font)
        month_lable.setAlignment(Qt.AlignRight)
        month_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(month_lable, 2, 3)

        self.month_line = QLineEdit(self)
        self.month_line.setFont(font)
        self.month_line.setPlaceholderText("IVS_week_snx/P1C1/P1P2/P2C2可用")
        self.month_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.month_line, 2, 4, 1, 2)

        begin_doy_lable = QLabel('起始日')
        begin_doy_lable.setFont(font)
        begin_doy_lable.setAlignment(Qt.AlignRight)
        begin_doy_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(begin_doy_lable, 3, 0)

        self.begin_doy_line = QLineEdit(self)
        self.begin_doy_line.setFont(font)
        self.begin_doy_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.begin_doy_line, 3, 1, 1, 2)

        end_doy_lable = QLabel('截止日')
        end_doy_lable.setFont(font)
        end_doy_lable.setAlignment(Qt.AlignRight)
        end_doy_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(end_doy_lable, 3, 3)

        self.end_doy_line = QLineEdit(self)
        self.end_doy_line.setFont(font)
        self.end_doy_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.end_doy_line, 3, 4, 1, 2)

        unzip_lable = QLabel('是否解压')
        unzip_lable.setFont(font)
        unzip_lable.setAlignment(Qt.AlignRight)
        unzip_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(unzip_lable, 4, 0)

        self.unzip_combo = QComboBox(self)
        self.unzip_combo.addItem('是')
        self.unzip_combo.addItem('否')
        self.unzip_combo.setFont(font)
        self.unzip_combo.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.unzip_combo, 4, 1, 1, 2)

        pool_lable = QLabel('并行数量')
        pool_lable.setFont(font)
        pool_lable.setAlignment(Qt.AlignRight)
        pool_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(pool_lable, 4, 3)

        self.pool_combo = QComboBox(self)
        for pool_num_counter in range(1, 13):
            self.pool_combo.addItem(str(pool_num_counter))
        self.pool_combo.setFont(font)
        self.pool_combo.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.pool_combo, 4, 4, 1, 2)

        site_dir_lable = QLabel('站点文件')
        site_dir_lable.setFont(font)
        site_dir_lable.setAlignment(Qt.AlignRight)
        site_dir_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(site_dir_lable, 5, 0)

        self.site_file_line = QLineEdit(self)
        self.site_file_line.setFont(font)
        self.site_file_line.setPlaceholderText("站点名按空格或行分割都可")
        self.site_file_line.setMinimumSize(QSize(600, choose_h))
        type_choose_lay.addWidget(self.site_file_line, 5, 1, 1, 4)

        open_site_file_btn = QPushButton('  ...  ', self)
        open_site_file_btn.setFont(font)
        open_site_file_btn.setMinimumSize(QSize(80, choose_h + 15))
        type_choose_lay.addWidget(open_site_file_btn, 5, 5, alignment=Qt.AlignRight)
        open_site_file_btn.clicked.connect(self.choose_site_file)

        dd_dir_lable = QLabel('下载位置')
        dd_dir_lable.setFont(font)
        dd_dir_lable.setAlignment(Qt.AlignRight)
        dd_dir_lable.setMaximumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(dd_dir_lable, 6, 0)

        self.out_dir_line = QLineEdit(self)
        self.out_dir_line.setFont(font)
        self.out_dir_line.setMinimumSize(QSize(600, choose_h))
        self.out_dir_line.setPlaceholderText("若为空则下载至当前文件夹")
        type_choose_lay.addWidget(self.out_dir_line, 6, 1, 1, 4)

        open_out_dir_btn = QPushButton('  ...  ', self)
        open_out_dir_btn.setFont(font)
        open_out_dir_btn.setMinimumSize(QSize(80, choose_h + 15))
        type_choose_lay.addWidget(open_out_dir_btn, 6, 5, alignment=Qt.AlignRight)
        open_out_dir_btn.clicked.connect(self.choose_out_dir)

        none_lable = QLabel('')
        type_choose_lay.addWidget(none_lable, 7, 0)

        font_big = QtGui.QFont()
        font_big.setPointSize(10)
        font_big.setFamily('Microsoft YaHei')

        dd_btn = QPushButton('下 载', self)
        dd_btn.setFont(font_big)
        dd_btn.setMinimumSize(QSize(120, choose_h + 30))
        dd_btn.clicked.connect(self.dd)
        type_choose_lay.addWidget(dd_btn, 8, 1, 1, 2, alignment=Qt.AlignCenter)

        kill_btn = QPushButton('终 止', self)
        kill_btn.setFont(font_big)
        kill_btn.setMinimumSize(QSize(120, choose_h + 30))
        kill_btn.clicked.connect(self.kill_p)
        type_choose_lay.addWidget(kill_btn, 8, 3, 1, 2, alignment=Qt.AlignCenter)

        RightTop = QFrame()
        RightTop.setFrameShape(QFrame.StyledPanel)
        RightTop.setLayout(type_choose_lay)

        # |--log打印控件 -> 右侧下方
        self.logPrint = QTextEdit()
        self.logPrint.setLineWrapMode(QTextEdit.NoWrap)
        self.logPrint.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.logPrint.setReadOnly(True)
        self.logPrint.setFont(font)

        # 右侧控件布局设置
        splitterRight = QSplitter(Qt.Vertical)
        splitterRight.addWidget(RightTop)
        splitterRight.addWidget(self.logPrint)
        splitterRight.setSizes([400, 200])
        # ----------------右侧控件布局----------------

        # ----------------总体控件布局----------------
        splitterAll = QSplitter(Qt.Horizontal)
        splitterAll.addWidget(splitterLeft)
        splitterAll.addWidget(splitterRight)
        splitterAll.setSizes([200, 400])
        # 声明布局
        layout = QHBoxLayout(self)
        layout.addWidget(splitterAll)
        # 声明QWidget
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)
        # 展示
        self.show()
        # ----------------总体控件布局----------------

    def showDialog(self):
        print('')

    def onActivated(self, text):
        self.name_type_combo.clear()
        for gt in gnss_type:
            if text == gt[0]:
                for gt2 in gt[1]:
                    self.name_type_combo.addItem(gt2)
        self.name_type_combo.setFont(font)

    # 打印log
    def printLog(self, logStr):
        import datetime
        time.sleep(0.001)
        nowtimeStrft = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logStr = '[' + nowtimeStrft + ']: ' + logStr
        self.logPrint.setFontWeight(QFont.Normal)
        self.logPrint.append(logStr)

    def choose_out_dir(self):
        sel_out_dir_win = QFileDialog.getExistingDirectory(self, '选择下载路径', expanduser("~"),
                                                           QFileDialog.ShowDirsOnly)
        self.out_dir_line.setText(sel_out_dir_win)
        if len(sel_out_dir_win) == 0:
            self.printLog('未选择！')
        else:
            self.printLog('选择下载路径为 -> ' + sel_out_dir_win)

    def choose_site_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "选取站点文件", expanduser("~"),
                                                         "")
        self.site_file_line.setText(filename)
        if len(filename) == 0:
            self.printLog('未选择！')
        else:
            self.printLog('选择站点文件为 -> ' + filename)

    def dd(self):

        if getattr(sys, 'frozen', False):
            dirname = os.path.dirname(sys.executable)
        else:
            dirname = os.path.dirname(os.path.abspath(__file__))
        global cmd
        win_bin_fast = os.path.join(dirname, 'win_bin', 'FAST.exe')
        cmd = win_bin_fast
        type_name = self.name_type_combo.currentText()
        pool_num = self.pool_combo.currentText()
        unzip_str = self.unzip_combo.currentText()

        self.printLog('选择数据为 -> ' + type_name)
        self.printLog('下载并发数 -> ' + pool_num)
        if type_name in yd_type:
            year = self.year_line.text()
            doy1 = self.begin_doy_line.text()
            doy2 = self.end_doy_line.text()
            loc = self.out_dir_line.text()
            if year == '':
                self.printLog('请输入年份！')
                return
            if not year.isdigit():
                self.printLog('请输入正确年份！')
                return
            if doy1 == '':
                self.printLog('请输入年积日！')
                return
            if not doy1.isdigit():
                self.printLog('请输入正确年积日！')
                return
            if doy2 == '':
                doy2 = doy1
            if not doy2.isdigit():
                self.printLog('请输入正确年积日！')
                return
            if loc != '' and not os.path.isdir(loc):
                self.printLog('请输入正确下载位置！')
                return

            self.printLog('下载数据类型 -> ' + type_name)
            cmd += ' -t ' + type_name
            self.printLog('下载年份 -> ' + year)
            cmd += ' -y ' + year
            self.printLog('起始年积日 -> ' + doy1)
            cmd += ' -o ' + doy1
            self.printLog('中止年积日 -> ' + doy2)
            cmd += ' -e ' + doy2
            if loc != '':
                self.printLog('下载路径 -> ' + loc)
                cmd += ' -l ' + loc
        if type_name in yds_type:
            year = self.year_line.text()
            doy1 = self.begin_doy_line.text()
            doy2 = self.end_doy_line.text()
            loc = self.out_dir_line.text()
            site_file = self.site_file_line.text()
            if year == '':
                self.printLog('请输入年份！')
                return
            if not year.isdigit():
                self.printLog('请输入正确年份！')
                return
            if doy1 == '':
                self.printLog('请输入年积日！')
                return
            if not doy1.isdigit():
                self.printLog('请输入正确年积日！')
                return
            if doy2 == '':
                doy2 = doy1
            if not doy2.isdigit():
                self.printLog('请输入正确年积日！')
                return
            if loc != '' and not os.path.isdir(loc):
                self.printLog('请输入正确下载位置！')
                return
            if site_file == '':
                self.printLog('请输入站点位置文件！')
                return
            if site_file != '' and not os.path.isfile(site_file):
                self.printLog('请输入正确站点文件！')
                return
            self.printLog('下载数据类型 -> ' + type_name)
            cmd += ' -t ' + type_name
            self.printLog('下载年份 -> ' + year)
            cmd += ' -y ' + year
            self.printLog('起始年积日 -> ' + doy1)
            cmd += ' -o ' + doy1
            self.printLog('中止年积日 -> ' + doy2)
            cmd += ' -e ' + doy2
            self.printLog('站点文件 -> ' + site_file)
            cmd += ' -f ' + site_file
            if loc != '':
                self.printLog('下载路径 -> ' + loc)
                cmd += ' -l ' + loc
        if type_name in no_type:
            loc = self.out_dir_line.text()
            if loc != '' and not os.path.isdir(loc):
                self.printLog('请输入正确下载位置！')
                return
            cmd += ' -t ' + type_name
            if loc != '':
                cmd += ' -l ' + loc
        if type_name in ym_type:
            year = self.year_line.text()
            month = self.month_line.text()
            loc = self.out_dir_line.text()
            if year == '':
                self.printLog('请输入年份！')
                return
            if not year.isdigit():
                self.printLog('请输入正确年份！')
                return
            if month == '':
                self.printLog('请输入月份！')
                return
            if not month.isdigit():
                self.printLog('请输入正确月份！')
                return
            if int(month) > 12 or int(month) < 1:
                self.printLog('请输入正确月份！')
                return
            self.printLog('下载数据类型 -> ' + type_name)
            cmd += ' -t ' + type_name
            self.printLog('下载年份 -> ' + year)
            cmd += ' -y ' + year
            self.printLog('下载月份 -> ' + month)
            cmd += ' -m ' + month
            if loc != '':
                self.printLog('下载路径 -> ' + loc)
                cmd += ' -l ' + loc
        if type_name in s_type:
            loc = self.out_dir_line.text()
            site_file = self.site_file_line.text()
            if loc != '' and not os.path.isdir(loc):
                self.printLog('请输入正确下载位置！')
                return
            if site_file == '':
                self.printLog('请输入站点位置文件！')
                return
            if site_file != '' and not os.path.isfile(site_file):
                self.printLog('请输入正确站点文件！')
                return
            self.printLog('下载数据类型 -> ' + type_name)
            cmd += ' -t ' + type_name
            self.printLog('站点文件 -> ' + site_file)
            cmd += ' -f ' + site_file
            if loc != '':
                self.printLog('下载路径 -> ' + loc)
                cmd += ' -l ' + loc
        self.printLog('下载并发 -> ' + pool_num)
        cmd += ' -p ' + pool_num
        if unzip_str == '否':
            cmd += ' -u N'
        print(cmd)
        self.printLog('########################FAST########################')
        self.printLog('开始下载！')
        global run_not
        run_not = True
        self.thread = Worker()
        self.thread.sig.connect(self.printLog)
        self.thread.start()

    def kill_p(self):
        global run_not
        run_not = False
        self.thread = Worker()
        self.thread.sig.connect(self.printLog)
        self.thread.start()

    def time_tran(self):
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
            nowdatetime = GNSS_Timestran.ymd2datetime(year, month, day)
        elif yearofdoy.isdigit() and doy.isdigit():
            yearofdoy = int(yearofdoy)
            if yearofdoy < 1980:
                QMessageBox.information(self, "警告", "请输入大于1980的年份", QMessageBox.Yes)
                return
            doy = int(doy)
            if doy > 366 or doy < 0:
                QMessageBox.information(self, "警告", "请输入正确年积日", QMessageBox.Yes)
                return
            nowdatetime = GNSS_Timestran.doy2datetime(yearofdoy, doy)
        elif gpsweek.isdigit() and gpsdayofweek.isdigit():
            gpsweek = int(gpsweek)
            if gpsweek < 0:
                QMessageBox.information(self, "警告", "请输入正确GPS周", QMessageBox.Yes)
                return
            gpsdayofweek = int(gpsdayofweek)
            if gpsdayofweek < 0 or gpsdayofweek > 6:
                QMessageBox.information(self, "警告", "请输入正确周内天", QMessageBox.Yes)
                return
            nowdatetime = GNSS_Timestran.gpswd2datetime(gpsweek, gpsdayofweek)
        elif bdsweek.isdigit() and bdsdayofweek.isdigit():
            bdsweek = int(bdsweek)
            if bdsdayofweek < 0:
                QMessageBox.information(self, "警告", "请输入正确BDS周", QMessageBox.Yes)
                return
            bdsdayofweek = int(bdsdayofweek)
            if bdsdayofweek < 0 or bdsdayofweek > 6:
                QMessageBox.information(self, "警告", "请输入正确周内天", QMessageBox.Yes)
                return
            nowdatetime = GNSS_Timestran.gpswd2datetime(bdsweek + 1356, bdsdayofweek)
        elif mjd.isdigit() and IsFloatNum(sod):
            mjd = int(mjd)
            if mjd < 0:
                QMessageBox.information(self, "警告", "请输入正确MJD", QMessageBox.Yes)
                return
            sod = float(sod)
            if sod < 0. or sod > 86400.:
                QMessageBox.information(self, "警告", "请输入正确天内秒", QMessageBox.Yes)
                return
            nowdatetime = GNSS_Timestran.mjd2datetime(mjd, sod)
        else:
            nowdatetime = self.dateTimeEdit.dateTime().toPyDateTime()

        gnss_time = GNSS_Timestran.datetime2allgnssTime(nowdatetime)
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


def ytAppMain():
    ytApp = QApplication(sys.argv)
    ytApp.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ytApp.setStyleSheet(qdarkstyle.load_stylesheet())

    framelessWnd = FramelessWindow()
    framelessWnd.setWindowIcon(QtGui.QIcon("./win_bin/WHU.png"))
    framelessWnd.setWindowTitle('FAST-大地测量数据下载软件 V2.01')

    win = mainWindow()
    framelessWnd.setContent(win)
    framelessWnd.show()
    win.printLog('欢迎使用FAST-大地测量数据下载软件!')
    sys.exit(ytApp.exec())


# 软件加密思路
# 获取机器码，转为加密字符，生成文件，一机一码
# 发给用户，程序自动解码，否则退出
if __name__ == '__main__':
    ytAppMain()
