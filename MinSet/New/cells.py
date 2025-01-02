from tkinter import ttk
from tkinterdnd2 import *
from tkinter.messagebox import showerror, showinfo, showwarning
from colour import Color
from tab import measure_time
from tab import Tab


class Cells(Tab):
    PATH_TO_DATA = ""
    DATA = None
    TEMP_GRADIENT = None

    def __init__(self, root, notebooks):
        super().__init__(
            root,
            notebooks,
            number="№",
            cell_form="Форма ячейки",
            type_cell="Тип ячейки",
            area_cell="Площадь ячейки",
            hydraulic_diameter="Гидравлический диаметр",
            wet_perimeter="Смоченный периметр",
            heated_perimeter="Обогреваемый периметр",
            temp="Температура",
            connected="Связан с ячейками:",
        )

    def get_gradient(self, data: list, parameter: str):
        """Метод получения градиента по парметру
         Args:
            data: Массив словарей
            parameter: Строка (например температура).
        Returns:
            Возвращает массив словарей, ключами которого являются ("№", parameter, "Цвет") .
        """
        red = Color("red")
        green = Color("green")
        blue = Color("blue")
        gradient = []
        list_prms = []
        numbers = []
        dict_unique_prms = {}
        color_cells_1 = list(red.range_to(green, int(len(data) // 2)))
        color_cells_2 = list(color_cells_1[-1 - 1].range_to(blue, int(len(data) // 2)))
        color_cells = color_cells_1 + color_cells_2
        for index, element in enumerate(data):
            list_prms.append(data[index][parameter])
            numbers.append(data[index]["№"])
        unique_prms = list(set(list_prms))
        unique_prms.sort(reverse=True)
        dict_unique_prms = dict(zip(unique_prms, color_cells))
        for number, par, color in zip(numbers, list_prms, color_cells):
            color = dict_unique_prms[par]
            gradient.append({"№": number, parameter: par, "Цвет": color})
        return gradient

    def read_data(self, filePath) -> list:
        """Метод распаковки файла с ячейками"""
        if filePath == "":
            return None
        data_cells = []
        temp_cells = []
        self.type_cells = []
        with open(filePath, "r") as f:
            data_tmp = f.read().splitlines()
            if len(data_tmp) == 0:
                showerror(
                    title="Ошибка",
                    message=f'Файл с ячейками "{filePath.split('/')[-1]}" пустой',
                )
                return None
        temp_cells = [float(line.strip().split(";")[7]) for line in data_tmp]
        temp_cells.sort(reverse=True)

        color_cells_1 = list(
            Color("red").range_to(Color("green"), int(len(temp_cells) / 2))
        )
        color_cells_2 = list(
            Color("green").range_to(Color("blue"), int(len(temp_cells) / 2))
        )
        self.notebooks.color_cells = color_cells_1 + color_cells_2

        for line in data_tmp:
            values = line.strip().split(";")
            connected = [int(x) for x in values[8:] if x != ""]
            if len(values) < 6:
                raise
            if not self.type_cells.count(values[2]):
                self.type_cells.append(values[2])
            data_cells.append(
                {
                    "number": int(values[0]),
                    "cell_form": values[1].strip(),
                    "type_cell": values[2],
                    "area_cell": float(values[3]),
                    "hydraulic_diameter": float(values[4]),
                    "wet_perimeter": float(values[5]),
                    "heated_perimeter": float(values[6]),
                    "temp": float(values[7]),
                    "connected": connected,
                    "color": self.notebooks.color_cells[
                        temp_cells.index(float(values[7]))
                    ],
                }
            )

        return data_cells

    @measure_time
    def apply(self):
        Cells.PATH_TO_DATA = self.path_to_data
        self.data = self.get_data_from_tree(self.data)
        Cells.DATA = self.data
        Cells.TEMP_GRADIENT = self.get_gradient(self.data, "Температура")

        print("****Время выполнения методов во вкладке Ячеки****")
        # running_time = self.mesure_time(self.fill_tree, filePath=self.tree.path_to_data)
        # print(f"Время выполнения fill_tree={running_time} секунд")
        # running_time = self.mesure_time(self.get_data_from_tree, data=self.data)
        # print(f"Время выполнения get_data_from_tree={running_time} секунд")
        # running_time = self.mesure_time(
        #     self.get_gradient, data=self.data, parameter="Температура"
        # )
        # print(f"Время выполнения get_gradient={running_time} секунд")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Geometry")
    root.notebooks = notebooks = ttk.Notebook(root)
    app = Cells(root, notebooks)
    app.pack()

    root.mainloop()
