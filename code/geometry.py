from tkinter import ttk
from tkinterdnd2 import *
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
        )

    @measure_time
    def apply(self):
        Geometry.PATH_TO_DATA = self.path_to_data
        self.data = self.get_data_from_tree(self.data)

        Geometry.DATA = self.data


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Geometry")
    root.notebooks = notebooks = ttk.Notebook(root)
    app = Geometry(root, notebooks)
    app.pack()

    root.mainloop()
