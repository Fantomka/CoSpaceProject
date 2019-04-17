"""
Класс программы
В нем будет собран конфигуратор, для редактирования графа потоков движения робота
Данные на экспорт будут заносится в файл data.py
Приложение упаковывает в себе два фрейма, описанные в классах panel.py и graphics_editor.py
TODO: Создать файл configuration.csv и осуществить выгрузку данных в него
"""

from panel import Panel
from graphics_editor import Editor
from tkinter import *


class MainApp(Tk):
    """
    Класс программы (приложения), который используется для созддания графа потоков
    """
    def __init__(self, title="CoSpaceProject", ico_path="icon.ico", map_path="map.png"):
        """
        инициализация окна и фреймов, наследованных из классов tkinter, panel и graphics_editor
        :param title: имя программы
        :param ico_path: путь до иконки
        :param map_path: путь до карты
        """
        Tk.__init__(self)
        self.title = title
        self.iconbitmap = ico_path

        self.resizable(True, True)
        self.geometry("900x600+300+200")

        self.__panel = Panel(self, bg="black", width=10)
        self.__editor = Editor(self, map_path, bg="black")

        self.__editor.pack(side="left", fill="both")
        self.__panel.pack(side="right", fill="y")


