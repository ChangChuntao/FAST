# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['FAST-QT.py', 'GNSS_Timestran.py', 'GNSS_TYPE.py', 'QT_Frame.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FAST-QT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['.mac_binWHU.ico'],
)
app = BUNDLE(
    exe,
    name='FAST-QT.app',
    icon='.mac_binWHU.ico',
    bundle_identifier=None,
)
