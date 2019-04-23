from tkinter import *
import tkinter.ttk
from PIL import Image, ImageTk
import os
import math as m

CHECKPOINT_NEW = 1
LAST_CHECKPOINT_REDRAW = 2
CONSTRAINT_NEW = 3
LAST_CONSTRAINT_REDRAW = 4

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
        self.canvas.bind("<Button-3>", self.set_angle)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.checkpoints = []
        self.constraints = []

        self._draw_image()
        self.second_frame = Frame(root, bg="#FFFFFF")
        self.second_frame.place(width=131, height=540, relx=0.845)

        self.coords = Label(self.second_frame, text=f'x - 0, y - 0')

        self.__rBtnPressed = IntVar()
        self.__rButton1 = Radiobutton(self.second_frame, text=f"CheckPoint -> new     ", variable=self.__rBtnPressed, value=CHECKPOINT_NEW)
        self.__rButton2 = Radiobutton(self.second_frame, text=f"Last Checkpoint redraw", variable=self.__rBtnPressed, value=LAST_CHECKPOINT_REDRAW)
        self.__rButton3 = Radiobutton(self.second_frame, text=f"Constraint  -> new    ", variable=self.__rBtnPressed, value=CONSTRAINT_NEW)
        self.__rButton4 = Radiobutton(self.second_frame, text=f"Last Constraint redraw", variable=self.__rBtnPressed, value=LAST_CONSTRAINT_REDRAW)

        self.__ExportBtn = Button(self.second_frame, text="Export", width=4, height=2)
        self.__ExportBtn.bind("<Button-1>", self.export_data)

        # Упаковка кнопок
        self.coords.pack(side="top", fill="both")

        self.__rButton1.pack(side="top", fill="both")
        self.__rButton2.pack(side="top", fill="both")
        self.__rButton3.pack(side="top", fill="both")
        self.__rButton4.pack(side="top", fill="both")

        self.__ExportBtn.pack(side="bottom", fill="both")

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
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='green', tag='cp')
        elif self.__rBtnPressed.get() == CONSTRAINT_NEW:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', tag='ct')

    def on_move_press(self, event):
        """изменение размеров прямоугольника в соответствии с движением курсора"""
        self.on_move(event)
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x1 = self.start_x // 2 + 1
        y1 = 270 - self.start_y // 2
        x2 = event.x // 2 + 1
        y2 = 270 - event.y // 2
        center_x = (x2 + x1) // 2
        center_y = (y1 + y2) // 2
        if self.__rBtnPressed.get() == CHECKPOINT_NEW:
            self.checkpoints.append([x1, y1, x2, y2, center_x, center_y])
            if len(self.checkpoints) > 1:
                self.vector = self.canvas.create_line(self.checkpoints[-2][4] * 2 - 1, (270 - self.checkpoints[-2][5]) * 2, center_x * 2 - 1, (270 - center_y) * 2, arrow=LAST, fill='green')
        elif self.__rBtnPressed.get() == LAST_CHECKPOINT_REDRAW:
            self.checkpoints.pop()
            self.checkpoints.append([x1, y1, x2, y2, center_x, center_y])
            if len(self.checkpoints) > 1:
                self.canvas.delete(self.vector)
                self.vector = self.canvas.create_line(self.checkpoints[-2][4] * 2 - 1, (270 - self.checkpoints[-2][5]) * 2, center_x * 2 - 1, (270 - center_y) * 2, arrow=LAST, fill='green')
        elif self.__rBtnPressed.get() == CONSTRAINT_NEW:
            self.constraints.append([x1, y1, x2, y2, center_x, center_y])
        elif self.__rBtnPressed.get() == LAST_CONSTRAINT_REDRAW:
            self.constraints.pop()
            self.constraints.append([x1, y1, x2, y2, center_x, center_y])
        print(self.checkpoints, self.constraints)

    def on_move(self, event):
        self.coords.configure(text=f'x - {int(event.x//2)+1}, y - {int(270-event.y//2)}')

    def export_data(self, event):
        if os.path.exists(CONF_PATH):
            with open(CONF_PATH, "w") as f:
                for stroke in self.checkpoints:
                    f.write("\n_checkpoint(")
                    for i in range(len(stroke)):
                        if i != len(stroke) - 1:
                            f.write(str(stroke[i]) + ', ')
                        else:
                            f.write(str(stroke[i]) + ');')
                f.write("\n")
                for stroke in self.constraints:
                    f.write("\n_constraint(")
                    for i in range(len(stroke)):
                        if i != len(stroke) - 1:
                            if i != 4 and i != 5:
                                f.write(str(stroke[i]) + ', ')
                        else:
                            f.write(str(stroke[i]) + ');')
        else:
            f = open(CONF_PATH, 'w')

    def set_angle(self, event):
        print('test')
        if self.__rBtnPressed.get() == CONSTRAINT_NEW or self.__rBtnPressed.get():
            center_x = self.constraints[-1][4]
            center_y = self.constraints[-1][5]
            dot_x = event.x // 2 + 1
            dot_y = 270 - event.y // 2
            print(center_x, center_y, dot_x, dot_y)
            if center_x > dot_x:
                if center_y > dot_y:
                    angle = m.asin(abs(center_y - dot_y)/m.sqrt((center_y - dot_y) ** 2 + (center_x - dot_x) ** 2)) * 180/m.pi + 90
                else:
                    angle = m.acos(abs(center_y - dot_y)/m.sqrt((center_y - dot_y) ** 2 + (center_x - dot_x) ** 2)) * 180/m.pi
            else:
                if center_y > dot_y:
                    angle = m.acos(abs(center_y - dot_y)/m.sqrt((center_y - dot_y) ** 2 + (center_x - dot_x) ** 2)) * 180/m.pi + 180
                else:
                    angle = m.asin(abs(center_y - dot_y)/m.sqrt((center_y - dot_y) ** 2 + (center_x - dot_x) ** 2)) * 180/m.pi + 270

            if len(self.constraints[-1]) == 6:
                self.constraints[-1].append(int(angle))
            else:
                self.constraints[-1][-1] = int(angle)
            print(self.constraints)


if __name__ == '__main__':
    root = tkinter.Tk()
    run = CustomMenu(root)
    root.mainloop()
