import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.messagebox import showerror, showinfo, showwarning
from PIL import Image, ImageDraw, ImageTk
from colour import Color
from geometry import Geometry
from cells import Cells
from tkinterdnd2 import *
from tab import measure_time


class Paint(tk.Frame):
    def __init__(self, parent, notebooks):
        """
        Initializes the Paint class, setting up the main frames and widgets for the UI.

        Args:
            parent: The parent tkinter widget.
            notebooks: A ttk.Notebook widget for managing tabs.

        Sets up the following components:
        - A general frame that contains top and bottom frames.
        - A top frame with check buttons for showing rod numbers and temperature fields.
        - A button for finding cells, with an associated entry and combobox for selection.
        - A bottom frame with path labels for geometry and cell files.
        - Zoom controls including plus and minus buttons, a scale slider, and labels showing the zoom percentage.
        - Initializes data lists for geometry and cells, and sets default states and configurations for widgets.
        """
        super().__init__(parent)
        self.parent = parent
        self.general_frame = ttk.Frame(self.parent)
        self.general_frame.pack(fill="both", expand=True)
        self.top_frame = ttk.Frame(self.general_frame)
        self.top_frame.pack(side="top", fill="x")
        self.chekBtn_enabled = tk.IntVar()
        self.chekBtn_lbl = ttk.Label(self.top_frame, text="Показать номера стержней:")
        self.chekBtn_lbl.pack(side="left")
        self.show_text_rod_checkBtn = tk.Checkbutton(
            self.top_frame,
            variable=self.chekBtn_enabled,
            offvalue=0,
            onvalue=1,
        )
        self.show_text_rod_checkBtn.pack(side="left")
        self.chekcBtn_recolor_lbl = ttk.Label(self.top_frame, text="Поле температур")
        self.chekcBtn_recolor_lbl.pack(side="left")
        self.recolor_chekBtn_enabled = tk.IntVar()
        self.recolor_checkBtn = tk.Checkbutton(
            self.top_frame,
            variable=self.recolor_chekBtn_enabled,
            offvalue=0,
            onvalue=1,
        )
        self.recolor_checkBtn.pack(side="left")

        self.find_cell_btn_image = self._resize(r"code\images\find.gif", (13, 13))
        self.find_cell_button = ttk.Button(
            self.top_frame, image=self.find_cell_btn_image, command=self.find
        )
        self.find_cell_button.pack(side="right")

        # self.vcmd = (self.top_frame.register(self._validate_input), '%S')
        self.find_cell_entry = ttk.Entry(
            self.top_frame,
            # validate='key',
            # validatecommand= self.vcmd,
        )
        self.find_cell_entry.pack(side="right")
        self.find_methods = ["Поиск ячейки", "Поиск стержня"]
        self.cell_cmbx_var = tk.StringVar(value=self.find_methods[0])
        self.find_cell_cmbx = ttk.Combobox(
            self.top_frame,
            textvariable=self.cell_cmbx_var,
            values=self.find_methods,
            state="readonly",
            width=15,
        )
        self.find_cell_cmbx.pack(side="right")
        self.bootom_frame = ttk.Frame(self.general_frame)
        self.bootom_frame.pack(side="bottom", fill="x")
        self.bootom_path_frame = ttk.Frame(self.bootom_frame)
        self.bootom_path_frame.pack(side="left")
        self.file_path_geometry_label = tk.Label(
            self.bootom_path_frame, text="Путь к текущему файлу геометрии: "
        )
        self.file_path_geometry_label.grid(column=0, row=0, sticky="w")

        self.file_path_geometry_lbl = tk.Label(self.bootom_path_frame, text=r"")
        self.file_path_geometry_lbl.grid(column=1, row=0, sticky="w")

        self.file_path_cells_label = tk.Label(
            self.bootom_path_frame, text="Путь к текущему файлу ячеек: "
        )
        self.file_path_cells_label.grid(column=0, row=1, sticky="w")

        self.file_path_cells_lbl = tk.Label(self.bootom_path_frame, text=r"")
        self.file_path_cells_lbl.grid(column=1, row=1, sticky="w")

        self.btn_plus = ttk.Button(
            self.bootom_frame, text="+", width=2, command=self.zoom_plus
        )
        self.btn_plus.pack(side="right")
        self.btn_plus.config(state="disabled")

        self.scale_value = tk.IntVar(value=100)

        self.scale_slader = tk.Scale(
            self.bootom_frame,
            from_=0,
            to=300,
            variable=self.scale_value,
            resolution=10.0,
            showvalue=True,
            tickinterval=100.0,
            length=150,
            orient="horizontal",
            sliderlength=15,
            sliderrelief="flat",
            font=("Arial", 10, "normal"),
            command=self.zoom_scale,
        )

        self.scale_factor = 1.1
        self.max_scale = 300
        self.scale_slader.configure(to=self.max_scale, state="disabled")
        self.scale_slader.pack(side="right")
        self.previous_scale = self.scale_slader.get()
        self.btn_minus = ttk.Button(
            self.bootom_frame, text="-", width=2, command=self.zoom_minus
        )
        self.btn_minus.pack(side="right")
        self.btn_minus.config(state="disabled")
        self.zoom_label_quantity = ttk.Label(
            self.bootom_frame, text=f"{self.scale_slader.get()}%"
        )
        self.zoom_label_quantity.pack(side="right")
        self.zoom_label_name = ttk.Label(self.bootom_frame, text="Масштаб: ")
        self.zoom_label_name.pack(side="right")

        self.data_geometry = []
        self.data_cells = []
        self.show_text_rod_checkBtn.configure(command=self.checkBtn_changed)
        self.show_text_rod_checkBtn.config(state="disabled")
        self.recolor_checkBtn.config(
            state="disabled", command=self.recolor_typeСells_to_temperatureСells
        )

        self.setiing_defaults()

    def _resize(self, filePath: str, new_size: tuple):
        """Метод изменения размера импортируемых изображений"""
        original_image = Image.open(filePath)
        resize_image = original_image.resize(new_size)
        photo = ImageTk.PhotoImage(resize_image)
        return photo

    def _validate_input(self, char):
        """Метод валидации вводимых символов в find_cell_entry.
        Разрешены только цифры"""
        return char.isdigit()

    def on_enter(self, event):
        """Метод привязки нажатия клавиши Enter к методу find
        Вызывает метод find"""
        self.find()

    def find(self):
        """Метод поиска введеного в find_cell_entry значения в зависимости от self.find_cell_cmbx"""
        try:
            number = int(self.find_cell_entry.get())
        except ValueError:
            showerror(
                title="Ошибка", message="Не должно быть других символов кроме цифр"
            )
            return self.find_cell_entry.delete(0, "end")
        find_method = self.find_cell_cmbx.get()
        rects = self.canvas.find_withtag("rect")
        circles = self.canvas.find_withtag("circle")
        print((rects[0], rects[-1]), (circles[0], circles[-1]))
        if find_method == self.find_methods[0]:
            if number > len(rects):
                showwarning(
                    title="Предупреждение",
                    message=f"Введен номер ячейки больше, чем всего ячеек ({len(rects)} шт.)",
                )
                self.find_cell_entry.delete(0, "end")
            elif number == 0:
                showwarning(
                    title="Предупреждение", message=f"Номера ячеек начинаются с 1"
                )
                self.find_cell_entry.delete(0, "end")
            for rect in rects:
                if rect == number:
                    self.canvas.itemconfig(rect, outline="red", fill="black")
                    break
        elif find_method == self.find_methods[1]:
            if number > len(circles):
                showwarning(
                    title="Предупреждение",
                    message=f"Введен номер стержня больше, чем всего стержней ({len(circles)} шт.) (без учета стенок)",
                )
                self.find_cell_entry.delete(0, "end")
            elif number == 0:
                showwarning(
                    title="Предупреждение", message=f"Номера стержней начинаются с 1"
                )
                self.find_cell_entry.delete(0, "end")
            for circle in circles:
                if (circle == len(rects) + number) and (self.data_cells):
                    self.canvas.itemconfig(circle, outline="red", fill="green")
                    break
        else:
            self.find_cell_entry.delete(0, "end")
            self.find_cell_entry.insert(0, "Не найдено")

    def checkBtn_changed(self):
        """Метод отобразить/скрытия номера стержней"""
        data = self.data_geometry
        if self.chekBtn_enabled.get() == 1:
            self.create_text_rod(data)
        else:
            if hasattr(self, "canvas"):
                self.canvas.delete("text")
                self.canvas.delete("text4")
            else:
                pass

    def show_info(self, event):
        """Обработчик события входа курсора мыши в границы ячейки"""
        number_cells = self.canvas.find_withtag("current")[0]
        if hasattr(self, "data_frame"):
            self.data_frame.destroy()
        self.data_frame = ttk.Frame(
            self.canvas, padding=[2, 2], borderwidth=1, relief="solid"
        )
        self.data_frame.pack(side="top", anchor="ne")
        self.number_data_cells_lbl = tk.Label(
            self.data_frame, text=f"Номер ячейки: {number_cells}"
        )
        self.number_data_cells_lbl.pack(side="top", anchor="w")
        self.type_cells_lbl = tk.Label(
            self.data_frame,
            text=f'Тип ячейки: {Cells.DATA[number_cells-1]["Тип ячейки"]}',
        )
        self.type_cells_lbl.pack(side="top", anchor="w")

        self.temp_lbl = tk.Label(
            self.data_frame,
            text=f'Температура в ячейке: {Cells.DATA[number_cells-1] ["Температура"]} {chr(176)}C',
        )
        self.temp_lbl.pack(side="top", anchor="w")

    def hide_info(self, event):
        """Обработчик события выхода курсора мыши из границ ячеек"""
        if hasattr(self, "data_frame"):
            self.data_frame.destroy()

    def move_start(self, event):
        """Обработчик события нажатия левой клавиши мыши,
        запоминает координаты точки нажатия
        """
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        """Обработчик события движения мыши с зажатой левой кнопкой"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoomer(self, event):
        """Метод изменения масштаба путем прокрутки колеса мыши"""
        if event.delta > 0:
            self.scale_value.set(self.scale_value.get() + 10)
            self.zoom_plus(event.x, event.y)
        elif event.delta < 0:
            self.scale_value.set(self.scale_value.get() - 10)
            self.zoom_minus(event.x, event.y)

    def zoom_plus(self, relX: float = None, relY: float = None):
        """Метод увеличения масштаба путем нажатия кнопки "+" """
        if str(self.btn_plus.cget("state")) == "disabled":
            return
        if relX == None and relY == None:
            relX = self.canvas.winfo_width() / 2
            relY = self.canvas.winfo_height() / 2
        self.btn_minus.config(state="normal")
        self.zoom_label_quantity.config(text=f"{self.scale_value.get()}%")
        self.btn_plus.config(state="normal")
        self.canvas.scale("all", relX, relY, self.scale_factor, self.scale_factor)
        self.canvas.fontSize = self.canvas.fontSize * self.scale_factor
        self.canvas.fontSize4 = self.canvas.fontSize4 * self.scale_factor
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(
                child_widget, font=("Times", int(self.canvas.fontSize))
            )
        for child_widget in self.canvas.find_withtag("text4"):
            self.canvas.itemconfigure(
                child_widget, font=("Times", int(self.canvas.fontSize4))
            )
        for child_widget in self.canvas.find_withtag("text_cells"):
            self.canvas.itemconfigure(
                child_widget, font=("Times", int(self.canvas.fontSize4))
            )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if (
            int(
                self.zoom_label_quantity.cget("text")[
                    : len(self.zoom_label_quantity.cget("text")) - 1
                ]
            )
            > 40
        ):
            rects = self.canvas.find_withtag("rect")
            circles = self.canvas.find_withtag("circle")
            for rect in rects:
                self.canvas.itemconfigure(
                    rect, width=1, outline="black", activefill="blue"
                )
            for circle in circles:
                self.canvas.itemconfigure(
                    circle,
                    state="normal",
                )

        if self.scale_value.get() == self.max_scale:
            self.btn_plus.config(state="disabled")

    def zoom_minus(self, relX: float = None, relY: float = None):
        """Метод уменьшения масштаба путем нажатия кнопки "-" """
        if str(self.btn_minus.cget("state")) == "disabled":
            return
        if relX == None and relY == None:
            relX = self.canvas.winfo_width() / 2
            relY = self.canvas.winfo_height() / 2
        self.btn_plus.config(state="normal")
        self.canvas.scale(
            "all", relX, relY, 1 / self.scale_factor, 1 / self.scale_factor
        )
        self.canvas.fontSize = self.canvas.fontSize * 1 / self.scale_factor
        self.canvas.fontSize4 = self.canvas.fontSize4 * 1 / self.scale_factor
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(
                child_widget, font=("Times", int(self.canvas.fontSize))
            )
        for child_widget in self.canvas.find_withtag("text4"):
            self.canvas.itemconfigure(
                child_widget, font=("Times", int(self.canvas.fontSize4))
            )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.zoom_label_quantity.config(text=f"{self.scale_value.get()}%")

        if (
            int(
                self.zoom_label_quantity.cget("text")[
                    : len(self.zoom_label_quantity.cget("text")) - 1
                ]
            )
            <= 40
        ):
            rects = self.canvas.find_withtag("rect")
            circles = self.canvas.find_withtag("circle")
            for rect in rects:
                self.canvas.itemconfigure(
                    rect,
                    width=None,
                    outline="white",
                )
            for circle in circles:
                self.canvas.itemconfigure(
                    circle,
                    state="hidden",
                )
        if self.scale_value.get() == 0:
            self.btn_minus.config(state="disabled")

    def zoom_scale(self, value: float = None):
        """Метод изменения масштаба путем изменения значения Слайдера"""
        new_value = int(value)
        delta = new_value - self.previous_scale
        if delta > 0:
            self.zoom_plus()
        elif delta == 0:
            pass
        else:
            self.zoom_minus()
        self.previous_scale = new_value

    def setiing_defaults(self):
        """Метод сброса всех значений полей до значения по умолчанию"""
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        if hasattr(self, "xsb"):
            self.xsb.destroy()
        if hasattr(self, "ysb"):
            self.ysb.destroy()
        self.canvas = tk.Canvas(
            self.general_frame,
            background="white",
            width=800,
            height=450,
        )
        self.canvas.properties_circles = {
            "fill": "white",
            "activefill": "red",
            "tags": "circle",
        }
        self.canvas.properties_rects = {
            "activefill": "blue",
            "fill": "white",
            "activewidth": 3,
            "width": 1,
            "outline": "black",
            "tags": "rect",
        }
        self.xsb = tk.Scrollbar(
            self.general_frame, orient="horizontal", command=self.canvas.xview
        )
        self.ysb = tk.Scrollbar(
            self.general_frame, orient="vertical", command=self.canvas.yview
        )
        self.xsb.pack(side="bottom", fill="x")
        self.ysb.pack(side="right", fill="y")
        self.canvas.fontSize = 4
        self.canvas.fontSize4 = 3
        self.font = Font(self.canvas, f"Times {self.canvas.fontSize}")
        self.canvas.pack(side="top", fill="both", expand=True, anchor="w")
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 900, 600))
        self.canvas.tag_bind("rect", "<Enter>", self.show_info)
        self.canvas.tag_bind("rect", "<Leave>", self.hide_info)
        self.canvas.bind("<MouseWheel>", self.zoomer)
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.find_cell_entry.bind("<KeyPress - Return>", self.on_enter)
        self.canvas.fontSize = 4
        self.canvas.fontSize4 = 3
        self.scale_value.set(100)
        self.zoom_label_quantity.config(
            text=f"{round(float(self.scale_slader.get()))}%"
        )
        self.btn_plus.config(state="normal")
        self.btn_minus.config(state="normal")
        if hasattr(self, "canvas_color_frame"):
            self.canvas_color_frame.destroy()
        self.data_geometry = []
        self.data_cells = []
        self.file_path_data = None
        self.file_path_cells = None
        self.canvas_color_labels = []
        if hasattr(self.canvas, "number_data_cells_lbl"):
            self.canvas.number_data_cells_lbl.destroy()
        self.scale_slader.config(state="normal")
        self.btn_plus.config(state="normal")
        self.btn_minus.config(state="normal")
        self.recolor_checkBtn.config(state="normal")
        self.recolor_chekBtn_enabled.set(0)

    def open_file(self):
        """Метод открытия файлов путем нажатия на кнопку "Open" в меню "File" """
        self.setiing_defaults()
        self.canvas.update()
        self.file_path_data = Geometry.PATH_TO_DATA
        self.file_path_cells = Cells.PATH_TO_DATA
        self.file_path_geometry_lbl.config(text=self.file_path_data)
        self.data_geometry = Geometry.DATA
        self.file_path_cells_lbl.config(text=self.file_path_cells)
        self.data_cells = Cells.DATA
        try:
            self.new_data_geometry = self.convert_data(self.data_geometry)
            if self.data_geometry and self.data_cells:
                self.draw_cells(self.data_cells, self.new_data_geometry)
                self.draw_rod(self.new_data_geometry)
                self.create_text_rod(self.new_data_geometry)
            else:
                self.setiing_defaults()

        except Exception:
            showerror(
                title="Ошибка", message=f"Отсутствуют исходные данные. Смотри вкладки"
            )

    def save_file(self):
        """Метод сохранения изображения на холсте"""
        pass

    def convert_data(self, data: list) -> list:
        """Перевод координат в центр холста"""
        if not all(
            isinstance(item, dict) and "X" in item and "Y" in item for item in data
        ):
            raise ValueError(
                "Each item in data must be a dictionary with 'X' and 'Y' keys"
            )

        xArr = []
        yArr = []
        for item in data:
            xArr.append(item["X"])
            yArr.append(item["Y"])
        canvas_width = (
            self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
        )
        canvas_height = (
            self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 450
        )
        deltaY = (min(yArr) + max(yArr)) / 2 - canvas_height / 2
        deltaX = (min(xArr) + max(xArr)) / 2 - canvas_width / 2
        data_copy = [element.copy() for element in data]
        for element in data_copy:
            element["X"] = element["X"] - deltaX
            element["Y"] = element["Y"] - deltaY
        return data_copy

    def recolor_typeСells_to_temperatureСells(self):
        """Метод перекрашивания ячеек из поля type_cell в поле температур"""
        if self.recolor_chekBtn_enabled.get() == 1:
            if hasattr(self, "canvas_color_frame"):
                self.canvas_color_frame.destroy()
            self.canvas_color_frame = ttk.Frame(
                self.canvas, padding=[2, 2], borderwidth=1, relief="solid"
            )
            self.canvas_color_frame.pack(side="left")
            rects = self.canvas.find_withtag("rect")
            min_temp = float("inf")
            max_temp = float("-inf")
            for rect_number in rects:
                temp = float(Cells.TEMP_GRADIENT[rect_number - 1]["Температура"])
                if temp < min_temp:
                    min_temp = temp
                if temp > max_temp:
                    max_temp = temp
                self.canvas.itemconfig(
                    rect_number, fill=Cells.TEMP_GRADIENT[rect_number - 1]["Цвет"]
                )
            self.create_color_label(
                Color("red").hex, Color("green").hex, Color("blue").hex
            )
        else:
            self.recolor_temperatureСells_to_typeСells()

    def create_color_label(self, first_color: str, second_color: str, third_color: str):
        """Метод создания цветой шкалы из трех цветов"""
        img = Image.new("RGB", (20, 300), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        first_color = Color(first_color)
        colors_1 = list(Color(first_color).range_to(Color(second_color), 100))
        colors_2 = list(Color(second_color).range_to(Color(third_color), 100))
        colors = colors_1 + colors_2
        for i in range(len(colors)):
            height = i * 300 / len(colors)
            draw.line((0, height, 300, height), fill=str(colors[i].hex), width=2)
        self.color_image = ImageTk.PhotoImage(img)
        self.color_label = tk.Label(self.canvas_color_frame, image=self.color_image)
        self.color_label.pack(side="top", anchor="ne")

    def recolor_temperatureСells_to_typeСells(self):
        """Метод прекрашивания ячеек из поля температур в поле type_cell"""
        if hasattr(self, "canvas_color_frame"):
            self.canvas_color_frame.destroy()
        self.canvas_color_labels = []
        self.canvas_color_frame = ttk.Frame(
            self.canvas, padding=[2, 2], borderwidth=1, relief="solid"
        )
        self.canvas_color_frame.pack(side="left")
        type_cells = []
        rects = self.canvas.find_withtag("rect")
        type_cells = [cell_type["Тип ячейки"] for cell_type in Cells.DATA]
        type_cells = list(set(type_cells))
        cell_colors = ["#ab76d8", "#41b1e7", "#53e3dc", "#f6e94c"]
        dict_type_cells = dict(zip(type_cells, cell_colors))
        for rect_number in rects:
            if rect_number == Cells.DATA[rect_number - 1]["№"]:
                self.canvas.itemconfig(
                    rect_number,
                    fill=dict_type_cells[Cells.DATA[rect_number - 1]["Тип ячейки"]],
                )
        for i in range(0, len(cell_colors)):
            try:
                self.canvas_color_labels.append(
                    tk.Label(
                        self.canvas_color_frame,
                        text=type_cells[i],
                        background=cell_colors[i],
                        width=2,
                        height=7,
                    )
                )
            except IndexError:
                break
            self.canvas_color_labels[i].pack(side="top")

    @measure_time
    def draw_rod(self, data: list):
        """Метод отрисовки стержней на холсте"""
        for element in data:
            if element["Диаметр"] > 0:
                circle = self.canvas.create_oval(
                    element["X"] - element["Диаметр"] / 2,
                    element["Y"] - element["Диаметр"] / 2,
                    element["X"] + element["Диаметр"] / 2,
                    element["Y"] + element["Диаметр"] / 2,
                    **self.canvas.properties_circles,
                )

    @measure_time
    def create_text_rod(self, data: list):
        """Метод отрисовки номеров стержней на холсте"""
        keys = tuple(data[0].keys())  # Заголовки таблицы
        for element in data:
            if element["Диаметр"] > 0:
                if len(str(element[keys[0]])) >= 4:
                    text4 = self.canvas.create_text(
                        element["X"],
                        element["Y"],
                        text=str(element[keys[0]]),
                        tags="text4",
                        font=("Times", int(self.canvas.fontSize - 1)),
                    )
                else:
                    text = self.canvas.create_text(
                        element["X"],
                        element["Y"],
                        text=str(element[keys[0]]),
                        tags="text",
                        font=("Times", int(self.canvas.fontSize)),
                    )

    @measure_time
    def draw_cells(self, data_cells: list, data_geometry: list):
        """Метод отрисовки ячеек на холсте"""
        if not data_cells and not data_geometry:
            return None
        keys_data_cells = tuple(data_cells[0].keys())
        keys_data_geometry = tuple(data_geometry[0].keys())
        for element in data_cells:
            points = []
            for connected in element[keys_data_cells[-1]]:
                if connected > 0:
                    connected_element = next(
                        (
                            x
                            for x in data_geometry
                            if x[keys_data_geometry[0]] == connected
                        ),
                        None,
                    )
                    if connected_element:
                        points.append((connected_element["X"], connected_element["Y"]))
                # self.canvas.update()
            # self.canvas.geometry_coordinates = dict(
            rect = self.canvas.create_polygon(*points, **self.canvas.properties_rects)

    def redraw(
        self, data_cells: list = Cells.DATA, data_geometry: list = Geometry.DATA
    ):
        self.draw_cells(data_cells, data_geometry)
        self.draw_rod(data_geometry)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Geometry")
    root.geometry("900x600+600+200")
    root.notebooks = notebooks = ttk.Notebook(root)
    app = Paint(root, notebooks)
    app.pack()
    root.mainloop()
