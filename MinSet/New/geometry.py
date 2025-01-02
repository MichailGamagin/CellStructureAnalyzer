import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter import filedialog
from tab import Tab, measure_time


class Geometry(Tab):
    PATH_TO_DATA = ""
    DATA = None

    def __init__(
        self,
        root,
        notebooks,
    ):
        super().__init__(
            root,
            notebooks,
            number="№",
            type="Тип",
            x="X",
            y="Y",
            diameter="Диаметр",
            connected="Связан с элементами:",
        )

    @measure_time
    def apply(self):
        Geometry.PATH_TO_DATA = self.path_to_data
        self.data = self.get_data_from_tree(self.data)

        Geometry.DATA = self.data

        print("****Время выполнения методов во вкладке Геометрия****")
        # running_time = self.mesure_time(self.fill_tree, filePath=self.tree.path_to_data)
        # print(f"Время выполнения fill_tree ={running_time} секунд")
        # running_time = self.mesure_time(self.get_data_from_tree, data=self.data)
        # print(f"Время выполнения get_data_from_tree={running_time} секунд")
        # running_time = self.mesure_time(self.get_data_from_tree, data = self.data)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Geometry")
    root.notebooks = notebooks = ttk.Notebook(root)
    app = Geometry(root, notebooks)
    app.pack()

    root.mainloop()
