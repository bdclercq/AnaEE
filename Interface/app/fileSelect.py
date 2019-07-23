try:
    from tkinter import filedialog
    from tkinter import *
except ImportError:
    try:
        import tkFileDialog as filedialog
        from Tkinter import *
    except ImportError:
        print("Fuck this, no exporting for you apparently.")
import sys


def run():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    print(filename)  # Remove this print and importing/exporting will stop working
    root.destroy()
    return filename


sys.exit(run())
