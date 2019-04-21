from tkinter import *
import tkinter.ttk
from PIL import Image, ImageTk
import os

CHECKPOINT_NEW = 1
CHECKPOINT_DELETE = 2
CONSTRAINT_NEW = 3
CONSTRAINT_DELETE = 4
List_env = ['Environment ' + str(i) for i in range(4)]
CONF_PATH = "configuration.txt"
MAP_PATH = '1.png'


class CustomMenu(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        root.title('CoSpaceProject')
        root.iconbitmap("icon.ico")
        root.geometry("855x540+300+200")
        root.resizable(False, False)
        root.config(background="#373A68")

        self.first_frame = Frame(root, bg="#A3A3D7")
        self.first_frame.place(width=360*2, height=270*2)
        self.x = self.y = 0
        self.canvas = Canvas(self.first_frame, width=360*2, height=270*2, cursor="cross")
        self.canvas.place(width=360*2, height=270*2)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_move)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.checkpoints = []
        self.constraints = []

        self._draw_image()
        self.second_frame = Frame(root, bg="#FFFFFF")
        self.second_frame.place(width=131, height=540, relx=0.845)

        self.env = StringVar(value='Environment 0')
        self.__opEnvironments = OptionMenu(self.second_frame, self.env, *List_env)

        self.vector = Label(self.second_frame, text=f'x - 0, y - 0')

        self.__rBtnPressed = IntVar()
        self.__rButton1 = Radiobutton(self.second_frame, text=f"CheckPoint -> new   ", variable=self.__rBtnPressed, value=CHECKPOINT_NEW)
        self.__rButton2 = Radiobutton(self.second_frame, text=f"Constraint -> new   ", variable=self.__rBtnPressed, value=CONSTRAINT_NEW)
        self.__rButton3 = Radiobutton(self.second_frame, text=f"Last Rect -> redraw", variable=self.__rBtnPressed, value=CONSTRAINT_DELETE)

        self.__ExportBtn = Button(self.second_frame, text="Export", width=4, height=2)
        self.__ExportBtn.bind("<Button-1>", self.export_data)

        # Упаковка кнопок
        self.__opEnvironments.pack(side="top", fill="both")

        self.vector.pack(side="top", fill="both")

        self.__rButton1.pack(side="top", fill="both")
        self.__rButton2.pack(side="top", fill="both")
        self.__rButton3.pack(side="top", fill="both")
        self.__ExportBtn.pack(side="bottom", fill="both")

    def on_button_release(self, event):
        print(f'x1 - {self.start_x//2+1} y1 - {270-self.start_y//2}\n x2 - {event.x//2+1}, y2 - {270-event.y//2}')
        if self.__rBtnPressed.get() == CHECKPOINT_NEW:
            self.checkpoints.append([self.start_x//2+1, 270-self.start_y//2, event.x//2+1, 270-event.y//2])
        elif self.__rBtnPressed.get() == CHECKPOINT_DELETE and len(self.checkpoints) != 0:
            self.checkpoints.pop()
        elif self.__rBtnPressed.get() == CONSTRAINT_NEW:
            self.constraints.append([self.start_x//2+1, 270-self.start_y//2, event.x//2+1, 270-event.y//2])
        elif self.__rBtnPressed.get() == CONSTRAINT_DELETE and len(self.constraints) !=  0:
            self.constraints.pop()
        print(self.checkpoints, self.constraints)

    def export_data(self, event):
        if os.path.exists(CONF_PATH):
            with open(CONF_PATH, "a") as f:
                f.write("\ntest")
        else:
            f = open(CONF_PATH, 'w')

    def _draw_image(self):
        self.im = Image.open(MAP_PATH)
        self.im = self.im.resize((360*2, 270*2))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        """Сохраняет координаты нажатия ЛКМ"""
        self.start_x = event.x
        self.start_y = event.y
        if self.__rBtnPressed.get() == CHECKPOINT_NEW:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='green')
        elif self.__rBtnPressed.get() == CONSTRAINT_NEW:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        """изменение размеров прямоугольника в соответствии с движением курсора"""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_move(self, event):
        self.vector.configure(text=f'x - {int(event.x//2)+1}, y - {int(270-event.y//2)}')

    def select_env(self):
        pass


if __name__ == '__main__':
    root = tkinter.Tk()
    run = CustomMenu(root)
    root.mainloop()
