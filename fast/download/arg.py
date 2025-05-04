
import sys
from fast.download.inf import arg_help, supportData
from fast.com.pub import isSupportedDatatype, printFast, ym_type, yd_type, yds_type, s_type, lastVersionTime, lastVersion


def getArg(fastArg):
    """
    2022-03-27 :    * 获取输入参数
                    by Chang Chuntao -> Version : 1.00
    2023-06-30 :    * 更换参数读取方式， -start 对应为 -s
                    + "-i", "-site", 输入站点
                    + "-h", "-hour", 输入小时
                    by Chang Chuntao -> Version : 2.09
    """
    args = sys.argv
    if 'from multiprocessing.resource_tracker import main;main(6)' in args:
        return None
    for argIndex in range(len(args)):
        nowArg = args[argIndex]
        if '-h' == nowArg:
            arg_help()
            sys.exit()
        elif nowArg == '-v' or nowArg == '-version' or nowArg == '-V':
            print(lastVersionTime + ' - ' + lastVersion)
            sys.exit()
        elif nowArg in ["-t", "-type"]:
            fastArg["datatype"] = args[argIndex + 1]
        elif nowArg in ["-y", "-year"]:
            fastArg["year"] = int(args[argIndex + 1])
        elif nowArg in ["-l", "-loc"]:
            fastArg["loc"] = args[argIndex + 1]
        elif nowArg in ["-d", "-day"]:
            fastArg["day1"] = int(args[argIndex + 1])
            fastArg["day2"] = int(args[argIndex + 1])
        elif nowArg in ["-s", "-day1", "-start"]:
            if args[argIndex + 1] == '-c':
                continue
            fastArg["day1"] = int(args[argIndex + 1])
        elif nowArg in ["-e", "-day2", "-end"]:
            fastArg["day2"] = int(args[argIndex + 1])
        elif nowArg in ["-m", "-month"]:
            fastArg["month"] = int(args[argIndex + 1])
        elif nowArg in ["-hour"]:
            fastArg["hour"] = [int(args[argIndex + 1])]
        elif nowArg in ["-f", "-file"]:
            fastArg["file"] = args[argIndex + 1]
        elif nowArg in ["-p", "-process"]:
            fastArg["process"] = int(args[argIndex + 1])
        elif nowArg in ["-u", "-uncompress"]:
            fastArg["uncompress"] = args[argIndex + 1]
        elif nowArg in ["-r", "-rename"]:
            fastArg["rename"] = args[argIndex + 1]
        elif nowArg in ["-i", "-site"]:
            fastArg["file"] = args[argIndex + 1].replace(',', ' ')
    return fastArg

def checkInputArg(fastArg):  # 判断输入参数正确性
    """
    2022-03-27 : 判断输入参数正确性 by Chang Chuntao -> Version : 1.00
    """
    datatype = str(fastArg['datatype']).split(",")
    if len(fastArg["rename"]) > 0 and len(fastArg["rename"]) != 3:
        printFast("[-r] limit 3 char!", "fail")
        sys.exit()

    for dt in datatype:
        if isSupportedDatatype(dt):  # 判断输入数据类型是否正确
            if dt in ym_type:
                if fastArg['year'] == 0 or fastArg['month'] == 0:
                    printFast("本数据类型需输入年与月，请指定[-y <year>] [-m <month>]！", "fail")
                    printFast("This data type requires input of year and month.[-y <year>] [-m <month>]！", "fail")
                    sys.exit(2)
            else:
                if dt in yd_type:  # 输入为年， 起始年积日， 终止年积日的数据类型, 判断输入时间是否正确
                    if fastArg['year'] == 0:
                        printFast(
                            "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                            "fail")
                        printFast(
                            "This data type requires input of year and doy.[-y <year>] [-o <day1>] [-e <day2>] or [-y <year>] [-d <day>]！",
                            "fail")
                        sys.exit(2)
                    else:
                        if fastArg['day1'] == 0 and fastArg['day2'] == 0:
                            printFast(
                                "本数据类型需输入年与天，请指定[-y <year>] [-o <day1>] [-e <day2>]或[-y <year>] [-d <day>]！",
                                "fail")
                            printFast(
                                "This data type requires input of year and doy.[-y <year>] [-o <day1>] [-e <day2>] or [-y <year>] [-d <day>]！",
                                "fail")
                            sys.exit(2)
                if dt in yds_type or dt in s_type:
                    if fastArg['file'] == "" and fastArg['site'] == "":
                        printFast("本类型需要输入文件位置参数或站点参数，请指定[-f <file>]或者[-i <site>]！", "fail")
                        printFast("This type requires input of file location parameter or site parameter.[-f <file>] or [-i <site>]！", "fail")
                        sys.exit(2)
        elif dt =='':
            sys.exit()
        else:
            printFast(dt + " -> 数据类型不存在！ / Data type error!", "fail")
            printFast("是否需要查看支持数据？ / Would you like to see the supported data types? (y)", "input")
            cont = input("     ")
            if cont == "y" or "Y":
                supportData()
                sys.exit(2)
            else:
                sys.exit(2)