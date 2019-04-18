"""
Main - конфигуратор, в котором строится визуализация пути для робота

loadfile - загрузить карту

export - выгрузка настроек
"""

from mainapp import MainApp

if __name__ == '__main__':
    App = MainApp(title='CoSpaceProject')
    App.mainloop()
