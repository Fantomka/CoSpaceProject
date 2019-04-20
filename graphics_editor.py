"""
TODO: Фрейм с картой на фоне, для прорисовки ограничений пути робота
"""

from tkinter import *
from PIL import Image, ImageTk

MAP_PATH = '1.png'


class Editor(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = Canvas(self, width=360*2, height=270*2, cursor="cross")
        self.canvas.place(width=360*2, height=270*2)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self._draw_image()

    def _draw_image(self):
        self.im = Image.open(MAP_PATH)
        self.im = self.im.resize((360*2, 270*2))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        """Сохраняет координаты нажатия ЛКМ"""
        self.start_x = event.x
        self.start_y = event.y

        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        # изменение размеров прямоугольника в соответствии с движением курсора
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        return curX, curY

    def on_button_release(self, event):
        pass
