from tkinter import *
import tkinter.ttk
from PIL import Image, ImageTk
import os

AREA_NEW = 1
AREA_DELETE = 2
WALL_ADD = 3
WALL_REMOVE = 4
FLOW_POINT_NEW = 5
FLOW_POINT_DELETE = 6
CONF_PATH = "./configuration.csv"

class CustomMenu(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        root_window.title('CoSpaceProject')
        root_window.iconbitmap("icon.ico")
        root_window.geometry("900x600+300+200")
        root_window.resizable(0, 0)
        root_window.config(background ="#373A68" )


        self.first_frame= Frame(root_window, bg = "#A3A3D7")
        self.first_frame.place(width = 360*2, height = 270*2)
        self.x = self.y = 0
        self.canvas = Canvas(self.first_frame, width=360*2, height=270*2, cursor="cross")
        self.canvas.place(width = 360*2, height = 270*2)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self._draw_image()

        self.second_frame = Frame(root_window, bg="#FFFFFF")
        self.second_frame.place(width = 135, height =250, relx = 0.85)
        self.__vector = Label(self.second_frame, text='x и y')

        self.__rBtnPressed = IntVar()
        self.__rButton1 = Radiobutton(self.second_frame, text="Area -> new", variable=self.__rBtnPressed, value=AREA_NEW)
        self.__rButton2 = Radiobutton(self.second_frame, text="Area -> delete", variable=self.__rBtnPressed, value=AREA_DELETE)
        self.__rButton3 = Radiobutton(self.second_frame, text="Wall -> add", variable=self.__rBtnPressed, value=WALL_ADD)
        self.__rButton4 = Radiobutton(self.second_frame, text="Wall -> remove", variable=self.__rBtnPressed, value=WALL_REMOVE)
        self.__rButton5 = Radiobutton(self.second_frame, text="FlowPoint -> new", variable=self.__rBtnPressed, value=FLOW_POINT_NEW)
        self.__rButton6 = Radiobutton(self.second_frame, text="FlowPoint -> delete", variable=self.__rBtnPressed,
                                      value=FLOW_POINT_DELETE)

        self.__ExportBtn = Button(self.second_frame, text="Export", width=10, height=2)
        self.__ExportBtn.bind("<Button-1>", self.export_data)

        # Упаковка кнопок
        # self.__lbEnvironments.pack(side="top", fill="both")

        self.__vector.pack(side="top", fill="both")

        self.__rButton1.pack(side="top", fill="x")
        self.__rButton2.pack(side="top", fill="both")
        self.__rButton3.pack(side="top", fill="both")
        self.__rButton4.pack(side="top", fill="both")
        self.__rButton5.pack(side="top", fill="both")
        self.__rButton6.pack(side="top", fill="both")

        self.__ExportBtn.pack(side="bottom", fill="x")

    def _draw_image(self):
        self.image = Image.open("map.png")
        self.image = self.image.resize((360*2, 270*2))
        self.tk_im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        #one rectangle
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, )

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        pass

    def export_data(self, event):
        if not os.path.exists(CONF_PATH):
            with open(CONF_PATH, "w+") as f:
                f.write("test")
                f.close()
        else:
            with open(CONF_PATH, "a+") as f:
                f.write("test\n")
                f.close()

    def select_env(self):
        pass





if __name__ == '__main__':

   root_window = tkinter.Tk()
   run = CustomMenu(root_window)
   root_window.mainloop()