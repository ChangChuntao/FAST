# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['_fastQt.py', 'D:\\Code\\FAST\\fast\\com\\gnssParameter.py', 'D:\\Code\\FAST\\fast\\com\\gnssTime.py', 'D:\\Code\\FAST\\fast\\com\\mgexInf.py', 'D:\\Code\\FAST\\fast\\com\\mgexSite.py', 'D:\\Code\\FAST\\fast\\com\\nav2posclk.py', 'D:\\Code\\FAST\\fast\\com\\pub.py', 'D:\\Code\\FAST\\fast\\com\\readNav.py', 'D:\\Code\\FAST\\fast\\com\\readObs.py', 'D:\\Code\\FAST\\fast\\com\\readSiteinfo.py', 'D:\\Code\\FAST\\fast\\com\\sat2siteAngle.py', 'D:\\Code\\FAST\\fast\\com\\writeClk.py', 'D:\\Code\\FAST\\fast\\com\\writeObs.py', 'D:\\Code\\FAST\\fast\\com\\writeSiteInf.py', 'D:\\Code\\FAST\\fast\\com\\xy2azi.py', 'D:\\Code\\FAST\\fast\\com\\xyz2blh.py', 'D:\\Code\\FAST\\fast\\com\\xyz2neu.py', 'D:\\Code\\FAST\\fast\\plot\\plotCMC.py', 'D:\\Code\\FAST\\fast\\plot\\plotCnr.py', 'D:\\Code\\FAST\\fast\\plot\\plotCycleSlip.py', 'D:\\Code\\FAST\\fast\\plot\\plotFreq.py', 'D:\\Code\\FAST\\fast\\plot\\plotHighOrderDiff.py', 'D:\\Code\\FAST\\fast\\plot\\plotIOD.py', 'D:\\Code\\FAST\\fast\\plot\\plotLnoise.py', 'D:\\Code\\FAST\\fast\\plot\\plotMultipath.py', 'D:\\Code\\FAST\\fast\\plot\\plotSatNum.py', 'D:\\Code\\FAST\\fast\\plot\\plotSite.py', 'D:\\Code\\FAST\\fast\\qt\\qtDownload.py', 'D:\\Code\\FAST\\fast\\qt\\qtFrame.py', 'D:\\Code\\FAST\\fast\\qt\\qtQc.py', 'D:\\Code\\FAST\\fast\\qt\\qtSite.py', 'D:\\Code\\FAST\\fast\\qt\\qtSpp.py', 'D:\\Code\\FAST\\fast\\qt\\timeTran.py', 'D:\\Code\\FAST\\fast\\site\\thinning.py', 'D:\\Code\\FAST\\fast\\spp\\corr.py', 'D:\\Code\\FAST\\fast\\spp\\eph.py', 'D:\\Code\\FAST\\fast\\spp\\initObs.py', 'D:\\Code\\FAST\\fast\\spp\\satPos.py', 'D:\\Code\\FAST\\fast\\spp\\sppbybrdc.py', 'D:\\Code\\FAST\\fast\\spp\\trop.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='_fastQt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Code\\FAST\\fast\\win_bin\\black_c.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='_fastQt',
)
