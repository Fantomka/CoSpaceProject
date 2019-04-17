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
    def __init__(self, master=None, width=200, bg="white"):
        Frame.__init__(self, master=master, width=width, bg=bg)

        # Инициализация кнопок панеля редактора
        # TODO: доделать листбокс
        # self.__lbEnvironments = Listbox(master, width=10, height=2)
        # self.__lbEnvironments =
        # self.__lbEnvironments.bind("<<ListBoxSelect>>", self.select_env)

        # TODO: строка с координатами
        self.__vector = Label(self, text='x и y')

        self.__rBtnPressed = IntVar()
        self.__rButton1 = Radiobutton(self, text="Area -> new", variable=self.__rBtnPressed, value=AREA_NEW)
        self.__rButton2 = Radiobutton(self, text="Area -> delete", variable=self.__rBtnPressed, value=AREA_DELETE)
        self.__rButton3 = Radiobutton(self, text="Wall -> add", variable=self.__rBtnPressed, value=WALL_ADD)
        self.__rButton4 = Radiobutton(self, text="Wall -> remove", variable=self.__rBtnPressed, value=WALL_REMOVE)
        self.__rButton5 = Radiobutton(self, text="FlowPoint -> new", variable=self.__rBtnPressed, value=FLOW_POINT_NEW)
        self.__rButton6 = Radiobutton(self, text="FlowPoint -> delete", variable=self.__rBtnPressed, value=FLOW_POINT_DELETE)

        self.__ExportBtn = Button(self, text="Export", width=10, height=2)
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

    def export_data(self, event):
        if not os.path.exists(CONF_PATH):
            with open(CONF_PATH, "w+") as f:
                pass
        else:
            with open(CONF_PATH, "w+") as f:
                pass

    def select_env(self):
        pass
