# python version : 3.8.5
# pip install -r requirements.txt
# pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
# pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
# https://journeytosth.tistory.com/4
# pyinstaller --clean -w -F --icon=resources/sound-waves.ico main2.py
# datas=[('./resources/*.ui','resources'), ('./resources/sound-waves.ico','resources'), ('./ffmpeg.exe','.')]
# pyinstaller main2.spec



"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main2.py'],
             pathex=['C:\\projects\\soundAnalysis-master\\soundAnalysis-master\\venv\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\projects\\soundAnalysis-master\\soundAnalysis-master'],
             binaries=[],
             datas=[('./resources/*.ui','resources'), ('./resources/sound-waves.ico','resources'), ('./ffmpeg.exe','.'), ('./venv/Lib/site-packages/librosa/util/example_data', './librosa/util/example_data')],
             hiddenimports=['sklearn.utils._weight_vector'],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='main2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main2')

"""