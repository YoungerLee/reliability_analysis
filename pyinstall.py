from PyInstaller.__main__ import run
import sys

if __name__ == '__main__':
    sys.setrecursionlimit(10000000)
    # opts = ['reliability_app.py', '-w', '-F', '--icon=app.ico']
    # run(opts)
    opts = ['-c',
            '--add-data', 'app.ico;.',
            '--icon', 'app.ico',
            '--add-binary', 'D:/Anaconda3/lib/site-packages/scipy/extra-dll/*;.',
            '--hidden-import', 'PyQt5.QtSerialPort',
            '--hidden-import', 'PyQt5.QtChart',
            '--hidden-import', 'PyQt5.sip',
            '--hidden-import', 'ctypes.wintypes',
            '--hidden-import', 'win32con',
            '--hidden-import', 'sqlalchemy',
            '--hidden-import', 'sqlalchemy.orm',
            '--hidden-import', 'logging.handlers',
            '--hidden-import', 'scipy._lib.messagestream',
            '-y', '--noupx', '--clean',
            'reliability_app.py']

    run(opts)
