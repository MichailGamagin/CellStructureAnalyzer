#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo, showwarning
from PIL import Image, ImageDraw, ImageTk
from paint import Paint
from geometry import Geometry
from cells import Cells
from tkinterdnd2 import *


class App:

    def __init__(self, width, height, title="Геометрия", resizable=(True, True)):
        self.root = TkinterDnD.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+200+100")
        self.root.resizable(resizable[0], resizable[1])
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.window_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.menu_bar.add_cascade(label="Window", menu=self.window_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)

        self.root.config(menu=self.menu_bar)

        self.notebooks = ttk.Notebook(self.root)

        self.tab_paint_frame = ttk.Frame(self.notebooks)
        self.geometry_frame = ttk.Frame(self.notebooks)
        self.cells_frame = ttk.Frame(self.notebooks)
        self.notebooks.pack(expand=True, fill="both")
        self.notebooks.add(self.tab_paint_frame, text="Рисунок")
        self.notebooks.add(self.geometry_frame, text="Геометрия стержней")
        self.notebooks.add(self.cells_frame, text="Ячейки")

        self.notebooks.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.create_tabs(self.notebooks)

    def run(self):
        """Запуск основного цикла"""
        self.root.mainloop()

    def create_tabs(self, notebooks):
        """
        Create and initialize tabs for the application.
        """
        self.first_tab = Paint(self.tab_paint_frame, notebooks)
        self.second_tab = Geometry(self.geometry_frame, notebooks)
        self.third_tab = Cells(self.cells_frame, notebooks)

    def redraw(self):
        self.first_tab.redraw()

    def on_tab_changed(self, event):
        """Handle notebook tab change event"""
        self.notebooks.active_tab = self.notebooks.index(event.widget.select())

    def open_file(self):
        if self.notebooks.active_tab == 0:
            self.first_tab.open_file()
        elif self.notebooks.active_tab == 1:
            self.second_tab.open_file()
        elif self.notebooks.active_tab == 2:
            self.third_tab.open_file()

    def save_file(self):
        pass


if __name__ == "__main__":
    app = App(1200, 600)

    app.run()
