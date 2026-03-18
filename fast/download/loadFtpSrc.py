# -*- coding: utf-8 -*-
# loadFtpSrc        : FTP source of each gnss center
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.04
# Creation Date     : 2025.09.03 - Version 3.00.04
# Date              : 2025.09.03 - Version 3.00.04

import json, os, sys, platform

if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))
    dirname = os.path.join(dirname, '..')

ftpsJson = os.path.join(dirname, 'bin', 'fast_download_src.json')
if not os.path.isfile(ftpsJson):
    ftpsJson = os.path.join(os.path.join(dirname, '..'), 'bin', 'fast_download_src.json')


with open(ftpsJson, "r", encoding="utf-8") as f:
    FTP_S = json.load(f)