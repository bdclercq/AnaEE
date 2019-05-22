from tkinter import filedialog
from tkinter import *
import sys

def run():
    root = Tk()
    filename = filedialog.askopenfilename()
    print(filename)
    return filename

sys.exit(run())
