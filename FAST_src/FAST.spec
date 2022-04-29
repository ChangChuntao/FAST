# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['FAST.py', 'ARG_Mode.py', 'ARG_Sub.py', 'CDD_Mode.py', 'CDD_Sub.py', 'Dowload.py', 'FTP_Source.py', 'FAST_Print.py', 'GET_Ftp.py', 'GNSS_TYPE.py', 'Help.py', 'MGEX_name.py', 'Format.py', 'GNSS_Timestran.py'],
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
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='FAST',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='FAST.ico')
