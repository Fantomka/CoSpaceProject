"""
TODO: Фрейм с картой на фоне, для прорисовки ограничений пути робота
"""

from tkinter import *
from PIL import Image, ImageTk


class Editor(Frame):
    def __init__(self, master=None, img_path='map.png'):
        Frame.__init__(self, master=master)
        self.img_path = img_path
        self.x = self.y = IntVar()
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = Canvas(self, width=360, height=270, cursor="cross")
        self.canvas.pack(side="left")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self._draw_image()

    def _draw_image(self):
        self.image = Image.open(self.img_path)
        self.image = self.image.resize((360, 270))
        self.tk_im = ImageTk.PhotoImage(self.image)
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

    def on_button_release(self, event):
        pass
