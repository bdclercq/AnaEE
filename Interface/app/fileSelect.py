try:
    from tkinter import filedialog
    from tkinter import *
except ImportError:
    try:
        import tkFileDialog as filedialog
        from Tkinter import *
    except ImportError:
        print("Problem with TKinter, try Google for solutions.")
import sys


def run():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    print(filename)  # Remove this print and importing/exporting will stop working
    root.destroy()
    return filename


sys.exit(run())
