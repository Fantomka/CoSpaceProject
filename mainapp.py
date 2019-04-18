"""
Класс программы
В нем будет собран конфигуратор, для редактирования графа потоков движения робота
Данные на экспорт будут заносится в файл data.py
Приложение упаковывает в себе два фрейма, описанные в классах panel.py и graphics_editor.py
"""

from panel import Panel
from graphics_editor import Editor
from tkinter import *


class MainApp(Tk):
    """
    Класс программы (приложения)
    """
    def __init__(self, title="CoSpaceProject", ico_path="icon.ico"):
        """
        инициализация окна и фреймов, наследованных из классов tkinter, panel и graphics_editor
        :param title: имя программы
        :param ico_path: путь до иконки
        """
        Tk.__init__(self)
        self.title = title
        self.iconbitmap = ico_path

        self.resizable(False, False)
        self.geometry("855x540+300+200")

        self.editor = Editor(self)
        self.panel = Panel(self, bg="black")

        self.editor.place(width=360*2, height=270*2)
        self.panel.place(width=120, height=540, relx=0.85)
