# -*- coding: utf-8 -*-
# FAST           : MAIN of FAST
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2022.03.27 - Version 1.00.00
# Latest Version : 2025.05.05 - Version 3.00.03

def fast():
    import sys
    from fast.com.pub import printFast
    from fast.download.mode import runApplication, runApplicationWithArgs
    # get args
    argument = sys.argv[1:]  
    if len(argument) == 0:
        # arg off
        cont = "y"
        while True:
            if cont == "y" or cont == "Y":
                runApplication()
                printFast("运行结束,是否重新引导？(y)", "input")
                printFast("Execution completed. Would you like to restart? (y)", "input")
                cont = input("    ")
            else:
                break
    else:
        # arg on
        runApplicationWithArgs()  


if __name__ == '__main__':
    fast()