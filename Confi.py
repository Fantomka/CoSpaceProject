"""
Графическое приложение для генерации инструкций
роботу по езде на карте в виде кода

Авторы: O0Starley0o, Fantomka

Взаимодействие:
Используя инструмент checkpoint -> new
создаете прямгоульник начиная рисовать от левого нижнего угла
до правого верхнего. Это зоны где робот будет находится определенное время.
Время задается площадью зоны помноженнный на коэффициент
Используя инструмент constraints -> new
создаете 'зоны отчуждения' попав на которые, робот повернет на угол,
заданный пользователем.Чтобы задать угод нажмите пкм в ту сторону
куда робот должен уезжать попав на зону. Делать это стоит после создания зоны

v2.0
25.04.2019
"""

import tkinter as tk
import math as m
from PIL import Image, ImageTk

# используются константы для удобочитаемости
NEW_CHECKPOINT = 1
REDRAW_CHECKPOINT = 2
CONSTRAINT_NEW = 3
REDRAW_CONSTRAINT = 4
TIME_SET_COEFFICIENT = 0.007

# пути для карты и output file
CONF_PATH = "configuration.txt"
MAP_PATH = '1.png'
FIRMWARE_PATH = './CsBot/our_ai.c'


class CustomMenu(tk.Tk):
    """Класс конфигуратора"""
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('CoSpaceProject')
        self.iconbitmap("icon.ico")
        self.geometry("855x540+300+200")
        self.resizable(False, False)

        self.editor = tk.Frame(self)                      # фрейм карты
        self.editor.place(width=360*2, height=270*2)

        self.canvas = tk.Canvas(self.editor, width=360*2, height=270*2, cursor="cross")
        self.canvas.place(width=360*2, height=270*2)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<Button-3>", self.set_angle)

        self.rect = None
        self.vector_constr = None
        self.vector_checkp = None
        self.start_x = None
        self.start_y = None
        self.checkpoints = []
        self.constraints = []

        self._draw_image()

        self.panel = tk.Frame(self, bg="#FFFFFF")                        # фрейм панели управления
        self.panel.place(width=131, height=540, relx=0.845)

        self.coords = tk.Label(self.panel, text=f'x - 0, y - 0')         # координаты курсора

        # радиопереключатель панели инструментов
        self.rb_press = tk.IntVar()
        self.rb1 = tk.Radiobutton(self.panel, text="New checkpoint   ", variable=self.rb_press, value=NEW_CHECKPOINT)
        self.rb2 = tk.Radiobutton(self.panel, text="Redraw checkpoint", variable=self.rb_press, value=REDRAW_CHECKPOINT)
        self.rb3 = tk.Radiobutton(self.panel, text="New constraint   ", variable=self.rb_press, value=CONSTRAINT_NEW)
        self.rb4 = tk.Radiobutton(self.panel, text="Redraw constraint", variable=self.rb_press, value=REDRAW_CONSTRAINT)

        # кнопка выгрузки конфигурационных данных
        self.export_btn = tk.Button(self.panel, text="Export", width=4, height=2)
        self.export_btn.bind("<Button-1>", self.export_data)

        # Упаковка кнопок
        self.coords.pack(side="top", fill="both")
        self.rb1.pack(side="top", fill="both")
        self.rb2.pack(side="top", fill="both")
        self.rb3.pack(side="top", fill="both")
        self.rb4.pack(side="top", fill="both")
        self.export_btn.pack(side="bottom", fill="both")

    def _draw_image(self):
        """
        Загружает карту и подгоняет ее размер
        """
        self.image = Image.open(MAP_PATH)
        self.image = self.image.resize((360*2, 270*2))
        self.tk_im = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        """Сохраняет координаты нажатия ЛКМ и рисует прямоугльники"""
        self.start_x = event.x
        self.start_y = event.y
        if self.rb_press.get() == NEW_CHECKPOINT:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='green', tag='cp')
        elif self.rb_press.get() == CONSTRAINT_NEW:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='red', tag='ct')

    def on_move_press(self, event):
        """изменение размеров прямоугольника в соответствии с движением курсора"""
        self.on_move(event)
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        """
        при отжатии клавиши лкм происходит просчет и
        выгрузка координат созданной зоны, а также дополнительных
        индвивидуальных данных в список self.checkpoints и self.constraints
        После этого рисуются вектора
        :param event: отжатие лкм
        """
        if self.start_x < event.x:
            x_left = self.start_x // 2 + 1          # Поиск координат
            x_right = event.x // 2 + 1              # Левой нижней
        else:                                       # И правой верхней точки
            x_left = event.x // 2 + 1
            x_right = self.start_x // 2 + 1         # Так же идет пересчет координат
        if self.start_y > event.y:                  # Необходимо из-за
            y_left = 270 - self.start_y // 2        # разных систем координат
            y_right = 270 - event.y // 2
        else:
            y_left = 270 - event.y // 2
            y_right = 270 - self.start_y // 2
        center_x = (x_right + x_left) // 2
        center_y = (y_left + y_right) // 2
        time_set = int((x_right - x_left) * (y_right - y_left) * TIME_SET_COEFFICIENT)

        if self.rb_press.get() == NEW_CHECKPOINT:    # соохраняем координаты и рисуем вектор между чекпоинтами
            self.checkpoints.append([x_left, y_left, x_right, y_right, center_x, center_y, time_set])
            if len(self.checkpoints) > 1:
                self.vector_checkp = self.canvas.create_line(self.checkpoints[-2][4] * 2 - 1,     \
                                                             (270 - self.checkpoints[-2][5]) * 2, \
                                                             center_x * 2 - 1,                    \
                                                             (270 - center_y) * 2,                \
                                                             arrow=tk.LAST,                       \
                                                             fill='green')

        elif self.rb_press.get() == REDRAW_CHECKPOINT:       # перезаписываем список
            self.checkpoints.pop()                           # и перерисовываем вектор
            self.checkpoints.append([x_left, y_left, x_right, y_right, center_x, center_y, time_set])
            if len(self.checkpoints) > 1:
                self.canvas.delete(self.vector_checkp)
                self.vector_checkp = self.canvas.create_line(self.checkpoints[-2][4] * 2 - 1,     \
                                                             (270 - self.checkpoints[-2][5]) * 2, \
                                                             center_x * 2 - 1,                    \
                                                             (270 - center_y) * 2,                \
                                                             arrow=tk.LAST,                       \
                                                             fill='green')

        elif self.rb_press.get() == CONSTRAINT_NEW:  # (прорисовка вектора происходит в set_angle)
            self.constraints.append([x_left, y_left, x_right, y_right, center_x, center_y])
        elif self.rb_press.get() == REDRAW_CONSTRAINT:
            self.constraints.pop()
            self.constraints.append([x_left, y_left, x_right, y_right, center_x, center_y])
            self.canvas.delete(self.vector_constr)
        print(self.checkpoints, self.constraints)

    def on_move(self, event):
        """
        Обновление координат в label coords
        :param event: движеие курсора
        """
        self.coords.configure(text=f'x - {int(event.x//2)+1}, y - {int(270-event.y//2)}')

    def set_angle(self, event):
        """
        Высчитавыет угол в соответсвии с тригонометрическим кругом, данный на площадке
        Высчитывание идет через центр зоны и точкой, заданной пользователем
        Далее идет построение вектора до этой точки (рекомедуется выбирать точку
        в пределах зоны)
        :param event: нажаттие ПКМ
        """
        if self.rb_press.get() != CONSTRAINT_NEW and self.rb_press.get() != REDRAW_CONSTRAINT:
            return

        center_x = self.constraints[-1][4]
        center_y = self.constraints[-1][5]
        dot_x = event.x // 2 + 1
        dot_y = 270 - event.y // 2

        # Высчитывается угол в соответствии с системой углов
        if center_x > dot_x:
            if center_y > dot_y:
                angle = m.asin(abs(center_y-dot_y)/m.sqrt((center_y-dot_y)**2+(center_x-dot_x)**2))*180/m.pi+90
            else:
                angle = m.acos(abs(center_y-dot_y)/m.sqrt((center_y-dot_y)**2+(center_x-dot_x)**2))*180/m.pi
        else:
            if center_y > dot_y:
                angle = m.acos(abs(center_y-dot_y)/m.sqrt((center_y-dot_y)**2+(center_x-dot_x)**2))*180/m.pi+180
            else:
                angle = m.asin(abs(center_y-dot_y)/m.sqrt((center_y-dot_y)** 2+(center_x-dot_x)**2))*180/m.pi+270
        angle = int(angle) # все числа в прошивке - целые
        if len(self.constraints[-1]) == 6:
            self.constraints[-1].append(angle)
        else:
            self.constraints[-1][-1] = angle

        x_begin = center_x * 2 + 1
        y_begin = (270 - center_y) * 2       # Выводим координаты
        x_end = dot_x * 2 + 1              # для вектора
        y_end = (270 - dot_y) * 2
        self.vector_constr = self.canvas.create_line(x_begin, y_begin, x_end, y_end, arrow=tk.LAST, fill='red')

    def export_data(self, event):
        """
        Экспорт списков self.checkpoints и self.constraints
        в формате, понимаемом нашей прошивкой робота напрямую в прошивку
        :param event: нажатие кнопки Exports
        """
        #  Собираем и форматируем данные на экспорт в прошивку
        export_buffer = []
        for stroke in self.checkpoints:
            temp = '_checkpoint('
            for i, elem in enumerate(stroke):
                if i != len(stroke) - 1:
                    temp += str(elem) + ', '
                else:
                    temp += str(elem) + ');\n'
            export_buffer.append(temp)
        export_buffer.append('\n')
        for stroke in self.constraints:
            temp = '_constraint('
            for i, elem in enumerate(stroke):
                if i != len(stroke) - 1:
                    if i not in (4, 5):
                        temp += str(elem) + ', '
                else:
                    temp += str(elem) + ');\n'
            export_buffer.append(temp)

        with open(FIRMWARE_PATH, 'r+') as file:
            contents = file.readlines()                 # сохраняем код в буфер
            for i, line in enumerate(contents):
                if 'void init_values(){' in line:       # Парсим строку после которой произойдет вставка
                    for j, func in enumerate(export_buffer, start=1):
                        contents.insert(i + j, func)    # Вставка в буффер данные на экспорт
                    break
            file.seek(0)                                # Обнуляем указатель файла
            file.writelines(contents)                   # Переписываем фал с вставленными данными


if __name__ == '__main__':
    ROOT = CustomMenu()
    ROOT.mainloop()
