set PATH=%PATH%;c:\mingw\bin
setup.py build_ext --compiler=mingw32
pause 1
setup.py make_mo
pause 2
setup.py py2exe
pause Done