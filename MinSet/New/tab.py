import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter import filedialog
import json
from itertools import islice
import timeit
import csv


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Время выполнения {func.__name__}={execution_time} секунд")
        return result

    return wrapper


class Tab(tk.Frame):
    def __init__(self, parent, notebooks, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.notebooks = notebooks
        self.style = ttk.Style()
        self.general_frame = tk.Frame(self.parent, borderwidth=1, relief="solid")
        self.general_frame.pack(side="top", fill="both", expand=True)
        self.buttons_frame = tk.Frame(self.parent, borderwidth=1, relief="solid")
        self.buttons_frame.pack(side="bottom", fill="x", expand=False)
        self.apply_btn = tk.Button(
            self.buttons_frame,
            text="Применить",
            command=self.apply,
            background="grey",
            height=2,
        )
        self.apply_btn.pack(side="bottom", fill="x", expand=False)

        self.tree = ttk.Treeview(
            self.general_frame, show="headings", selectmode="extended"
        )

        self.scroll_y = ttk.Scrollbar(
            self.general_frame, command=self.tree.yview, orient="vertical"
        )
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x = ttk.Scrollbar(
            self.general_frame, command=self.tree.xview, orient="horizontal"
        )
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.tree.configure(
            yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set
        )
        self.tree.bind("<Double-1>", self.edit)
        self.style.configure("Treeview", font=("Courier", 11))
        self.style.configure("Treeview.Heading", font=("Courier", 11))
        self.general_frame.drop_target_register(DND_ALL)
        self.general_frame.dnd_bind("<<Drop>>", self.open_file)

    def apply(self):
        pass

    @measure_time
    def fill_tree(self, filePath):
        """Fill the treeview with data"""
        self.tree.delete(*self.tree.get_children())
        data = []
        with open(filePath, "r") as f:
            reader = csv.reader(f)
            heads = next(reader)[0]
            heads = [head.strip() for head in heads.split(";")]
            data_tmp = list(reader)
            # data_tmp = f.read().splitlines()
            # heads = [element.strip() for element in data_tmp[0].strip().split(";")]
            # heads.pop()
            self.tree.configure(columns=heads)
            for index, arg in enumerate(heads, start=1):
                self.tree.heading(f"#{index}", text=arg)
                self.tree.column(f"#{index}", anchor="center")
            for line in data_tmp:
                values = line[0].strip().split(";")
                # values.pop()
                values = [element.strip() for element in values]
                dict_ = {}
                for index, key in enumerate(heads):
                    if key == heads[-1]:
                        connected = [
                            int(x) for x in values[index].split(" ") if x != ""
                        ]
                        # connected = ' '.join(map(str,key))
                        dict_[key] = connected
                        break
                    dict_[key] = str(values[index].strip())
                self.tree.insert("", "end", values=tuple(dict_[head] for head in heads))
                data.append(dict_)
        return data

    def open_file(self, event=None):
        if event is None:
            self.tree.path_to_data = filedialog.askopenfilename()
        else:
            self.tree.path_to_data = str(event.data).lstrip("{").rstrip("}")
        if self.tree.path_to_data == "":
            return
        self.data = self.fill_tree(self.tree.path_to_data)
        Tab.path_to_data = self.tree.path_to_data

    def edit(self, event):
        """
        Edit the value of a cell in the treeview

        This function is called when the user double clicks on a cell in the
        treeview. It opens an entry widget on top of the cell and allows the
        user to edit the value of the cell.
        """
        if self.tree.identify_region(event.x, event.y) == "cell":

            def ok(event):
                """Change item value."""
                self.tree.set(item, column, self.entry.get())
                self.entry.destroy()

            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            x, y, width, height = self.tree.bbox(item, column)
            value = self.tree.set(item, column)

        elif self.tree.identify_region(event.x, event.y) == "heading":

            def ok(event):
                """Change heading text."""
                self.tree.heading(column, text=self.entry.get())
                self.entry.destroy()

            column = self.tree.identify_column(event.x)

            x, y, width, _ = self.tree.bbox(self.tree.get_children("")[0], column)

            y2 = y

            while self.tree.identify_region(event.x, y2) != "heading":
                y2 -= 1

            y1 = y2
            while self.tree.identify_region(event.x, y1) == "heading":
                y1 -= 1
            height = y2 - y1
            y = y1
            value = self.tree.heading(column, "text")
        else:
            return

        self.entry = ttk.Entry(self.tree, font=("Courier", 11))
        self.entry.place(x=x, y=y, width=width, height=height, anchor="nw")
        self.entry.insert(0, value)
        self.entry.bind("<FocusOut>", lambda e: self.entry.destroy())
        self.entry.bind("<Return>", ok)
        self.entry.focus_set()

    @measure_time
    def get_data_from_tree(self, data: list):
        """ "Метод получения данных из таблицы tree"""
        keys = tuple(data[0].keys())
        data_new = []
        for row in self.tree.get_children(""):
            values = self.tree.item(row)["values"]
            item = values[-1]
            data_new.append(dict(zip(keys, self.typing(values))))
            data_new[-1][keys[-1]] = self.typing(item.split(" "))
        return data_new

    def mesure_time(self, func, number: int = 1, *args, **kwargs):
        extcution_time = timeit.timeit(lambda: func(*args, **kwargs), number=number)
        return extcution_time

    def typing(self, string_array: list):
        """
        Преобразует массив строк в массив элементов соответствующих типов.

        Args:
            string_array: Массив строк.

        Returns:
            Массив элементов соответствующих типов.
            Возвращает исходный массив, если произошла ошибка при преобразовании.
        """
        result_array = []
        for item in string_array:
            try:
                # Попытка преобразования в целое число
                int_value = int(item)
                result_array.append(int_value)
                continue
            except ValueError:
                pass
            try:
                # Попытка преобразования в число с плавающей точкой
                float_value = float(item)
                result_array.append(float_value)
                continue
            except ValueError:
                pass
            try:
                # Попытка преобразования в список (JSON)
                list_value = json.loads(item)
                if isinstance(list_value, list):  # Проверяем, что это именно список
                    result_array.append(list_value)
                    continue
            except (json.JSONDecodeError, TypeError):
                pass
            # Если ни одно из преобразований не удалось, оставляем строку как есть
            result_array.append(item)
        return result_array


if __name__ == "__main__":
    # root = TkinterDnD.Tk()
    # root.title('General tab')
    # root.notebooks = notebooks = ttk.Notebook(root)
    # app = Tab(root, notebooks, number = '№',
    #                             cell_form = 'Форма ячейки',
    #                             type_cell = 'Тип ячейки',
    #                             area_cell = 'Площадь ячейки',
    #                             hydraulic_diameter = 'Гидравлический диаметр',
    #                             wet_perimeter = 'Смоченный периметр',
    #                             heated_perimeter = 'Обогреваемый периметр',
    #                             temp = 'Температура',
    #                             connected = 'Связан с ячейками:'
    #                             )
    # app.pack()
    # root.mainloop()

    root1 = TkinterDnD.Tk()
    root1.title("General tab")
    root1.notebooks = notebooks = ttk.Notebook(root1)
    app1 = Tab(root1, notebooks)
    #   number= '№',
    #   type = 'Тип',
    #   x = 'X',
    #   y = 'Y',
    #   diameter = 'Диаметр',
    #   connected= 'Связан с элементами:')
    app1.pack()

    root1.mainloop()
