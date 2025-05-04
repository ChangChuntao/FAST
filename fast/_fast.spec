# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['_fast.py', 'D:\\Code\\FAST\\fast\\com\\gnssTime.py', 'D:\\Code\\FAST\\fast\\com\\mgexInf.py', 'D:\\Code\\FAST\\fast\\com\\mgexSite.py', 'D:\\Code\\FAST\\fast\\com\\pub.py', 'D:\\Code\\FAST\\fast\\download\\arg.py', 'D:\\Code\\FAST\\fast\\download\\download.py', 'D:\\Code\\FAST\\fast\\download\\fileOperation.py', 'D:\\Code\\FAST\\fast\\download\\ftpSrc.py', 'D:\\Code\\FAST\\fast\\download\\inf.py', 'D:\\Code\\FAST\\fast\\download\\menu.py', 'D:\\Code\\FAST\\fast\\download\\mode.py'],
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
    a.binaries,
    a.datas,
    [],
    name='_fast',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Code\\FAST\\fast\\win_bin\\black_c.ico'],
)
