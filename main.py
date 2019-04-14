"""
Main - конфигуратор, в котором строится визуализация пути для робота

btn upload - загрузить карту

"""

from tkinter import *
import tkinter.filedialog as tkFileDialog
from PIL import Image, ImageTk

def Quit(ev):
    global root
    root.destroy()


def LoadFile(ev):
    fn = tkFileDialog.Open(root, filetypes=[('*.png files', '.png')]).show()
    if fn == '':
        return
    return fn


def ExportData(ev):
    pass


root = Tk()
root.iconbitmap("icon.ico")
root.title("CoSpaceProject")

img = Image.open(LoadFile(root))
render = ImageTk.PhotoImage(img)

panelFrame = Frame(root, height=60, bg='gray')
ImgFrame = Label(root, image=render)
ImgFrame.image = render

panelFrame.pack(side='top', fill='x')
ImgFrame.pack(side='bottom', fill='both', expand=1)

ExportBtn = Button(panelFrame, text='Export')
quitBtn = Button(panelFrame, text='Quit')

ExportBtn.bind("<Button-1>", ExportData)
quitBtn.bind("<Button-1>", Quit)

ExportBtn.place(x=10, y=10, width=40, height=40)
quitBtn.place(x=60, y=10, width=40, height=40)

root.mainloop()
