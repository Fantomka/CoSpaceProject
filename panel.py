"""
TODO: Фрейм панели и его данные и функционал. + описание
      К Данным входит:
                    потоки,
                    ограничения,
                    среды
      К функционалу входит:
                    выгрузка,
                    ограничение потока,
                    повышение приоритета на данном потоке,
                    создание дополнительных сред для нескольких потоков

"""

from tkinter import *
import os

AREA_NEW = 1
AREA_DELETE = 2
WALL_ADD = 3
WALL_REMOVE = 4
FLOW_POINT_NEW = 5
FLOW_POINT_DELETE = 6

# FLOW_ROUTE_NEW = 7
# FLOW_ROUTE_

List_env = ['Environment ' + str(i) for i in range(4)]
CONF_PATH = "configuration.csv"


class Panel(Frame):
    """
    Панель инструментов (размещается по горизонтали, лучше сверху
    """
    def __init__(self, master=None, width=200, bg="white", vector=(0, 0)):
        Frame.__init__(self, master=master, width=width, bg=bg)

        # Инициализация кнопок панеля редактора
        self.env = StringVar(value='Environment 0')
        self.__opEnvironments = OptionMenu(self, self.env, *List_env)

        # TODO: строка с координатами
        self.__vector = Label(self, text=f" x- {vector[0]}, y - {vector[1]}")
        self.__vector.bind()

        self.__rBtnPressed = IntVar()
        self.__rButton1 = Radiobutton(self, text=f"Area -> new        ", variable=self.__rBtnPressed, value=AREA_NEW)
        self.__rButton2 = Radiobutton(self, text=f"Area -> delete     ", variable=self.__rBtnPressed, value=AREA_DELETE)
        self.__rButton3 = Radiobutton(self, text=f"Wall -> add        ", variable=self.__rBtnPressed, value=WALL_ADD)
        self.__rButton4 = Radiobutton(self, text=f"Wall -> remove     ", variable=self.__rBtnPressed, value=WALL_REMOVE)
        self.__rButton5 = Radiobutton(self, text=f"FlowPoint -> new   ", variable=self.__rBtnPressed, value=FLOW_POINT_NEW)
        self.__rButton6 = Radiobutton(self, text=f"FlowPoint -> delete", variable=self.__rBtnPressed, value=FLOW_POINT_DELETE)

        self.__ExportBtn = Button(self, text="Export", width=4, height=2)
        self.__ExportBtn.bind("<Button-1>", self.export_data)

        # Упаковка кнопок
        self.__opEnvironments.pack(side="top", fill="both")

        self.__vector.pack(side="top", fill="both")

        self.__rButton1.pack(side="top", fill="both")
        self.__rButton2.pack(side="top", fill="both")
        self.__rButton3.pack(side="top", fill="both")
        self.__rButton4.pack(side="top", fill="both")
        self.__rButton5.pack(side="top", fill="both")
        self.__rButton6.pack(side="top", fill="both")

        self.__ExportBtn.pack(side="bottom", fill="both")

    def export_data(self, event):
        if os.path.exists(CONF_PATH):
            with open(CONF_PATH, "a") as f:
                f.write("\ntest")
        else:
            f = open(CONF_PATH, 'w')
