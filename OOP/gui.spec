# PyInstaller spec for Student & Teacher Info
# Build from the oop folder: pyinstaller gui.spec
# Output: dist/Student Teacher Info.exe (Windows)

a = Analysis(
    ['gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['auth', 'student', 'teacher', 'human', 'InfoManager'],
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
    name='Student Teacher Info',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # No terminal window on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
