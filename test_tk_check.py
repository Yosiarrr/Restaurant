import sys
print('executable:', sys.executable)
print('version:', sys.version.replace('\n',' '))
try:
    import tkinter
    print('tkinter imported:', tkinter)
    root = tkinter.Tk()
    root.withdraw()
    print('tkinter Tk ok')
    root.destroy()
except Exception as e:
    print('TK_ERROR', repr(e))
    raise
