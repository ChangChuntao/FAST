import os
import platform
import sys
import time
from FAST_Print import PrintGDD

dirname = os.path.split(os.path.abspath(sys.argv[0]))[0]
if platform.system() == 'Windows':
    unzip = dirname + "\\bin\\gzip.exe" + " -d "
    crx2rnx = dirname + "\\bin\\crx2rnx.exe" + " "
else:
    unzip = "uncompress "
    crx2rnx = dirname + "\\bin\\crx2rnx" + " "


def uncompresss(file):
    if file.split(".")[-1] == "Z" or file.split(".")[-1] == "gz":
        cmd = unzip + file
        os.system(cmd)


def crx2rnxs(file):
    if file[-3:-1].isdigit() and file[-1] == "d":
        cmd = crx2rnx + file
        os.system(cmd)


def crx2d(file):
    if file.split(".")[-1] == "crx":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "d"
        os.rename(file, filelow)


def renamebrdm(file):
    if file.split(".")[-1] == "rnx" and file[0:4] == "BRDM":
        filelow = file.lower()[0:4] + file.lower()[16:20] + "." + file.lower()[14:16] + "p"
        os.rename(file, filelow)


def unzip_format(loc):
    nowdir = os.getcwd()
    if len(loc) == 0:
        loc = os.getcwd()
    os.chdir(loc)
    PrintGDD("开始解压文件!", "normal")

    dirs = os.listdir(loc)
    for filename in dirs:
        if filename.split(".")[-1] == "Z" or filename.split(".")[-1] == "gz":
            uncompresss(filename)
    PrintGDD("解压结束!", "normal")

    dirs = os.listdir(loc)
    for filename in dirs:
        if filename[-3:-1].isdigit() or filename.split(".")[-1] == "crx":
            if filename.split(".")[-1] == "crx" or filename[-1] == "d":
                PrintGDD("目录内含有crx文件，正在进行格式转换！", "normal")
                break
    for filename in dirs:
        if filename.split(".")[-1] == "crx":
            crx2d(filename)

    dirs = os.listdir(loc)
    for filename in dirs:
        if filename[-1] == "d" and filename[-3:-1].isdigit():
            crx2rnxs(filename)
            time.sleep(0.1)
            os.remove(filename)

    dirs = os.listdir(loc)
    for filename in dirs:
        if filename.split(".")[-1] == "rnx" and filename[0:4] == "BRDM":
            renamebrdm(filename)
    os.chdir(nowdir)
