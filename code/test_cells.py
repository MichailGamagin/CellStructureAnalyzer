import unittest
from tkinterdnd2 import TkinterDnD
from tkinter import ttk
from cells import Cells


class TestTab(unittest.TestCase):
    def setUp(self):
        self.root = TkinterDnD.Tk()
        self.notebooks = ttk.Notebook(self.root)
        self.tab = Cells(self.root, self.notebooks)
        self.test_csv_path = "tests\\tests_data\cells(4 ТВС).csv"

    def test_fill_tree(self):
        data = self.tab.fill_tree(self.test_csv_path)
        self.assertEqual(len(data), 2640)
        self.assertEqual(data[0]["№"], "1")
        self.assertEqual(data[0]["Форма ячейки"], "треугольник")
        self.assertEqual(data[0]["Тип ячейки"], "300")
        self.assertEqual(data[0]["Площадь ячейки"], "37.8722")
        # self.assertEqual(data[0]["Гидравлический диаметр"], "окт.79")
        self.assertEqual(data[0]["Смоченный периметр"], "14.2942")
        self.assertEqual(data[0]["Обогреваемый периметр"], "14.2942")
        self.assertEqual(data[0]["Температура"], "100")
        self.assertEqual(data[0]["Связан с ячейками:"], [1, 2, 3])

    def test_get_data_from_tree(self):
        self.tab.data = self.tab.fill_tree(self.test_csv_path)
        data = self.tab.get_data_from_tree(self.tab.data)
        self.assertEqual(data[671]["№"], 672)
        self.assertEqual(data[671]["Форма ячейки"], "четырехугольник")
        self.assertEqual(data[671]["Тип ячейки"], 130)
        self.assertEqual(data[671]["Площадь ячейки"], 75.3221)
        self.assertEqual(data[671]["Гидравлический диаметр"], 18.0665)
        self.assertEqual(data[671]["Смоченный периметр"], 16.6766)
        self.assertEqual(data[671]["Обогреваемый периметр"], 16.6766)
        self.assertEqual(data[671]["Температура"], 771)
        self.assertEqual(data[671]["Связан с ячейками:"], [352, 703, 702, 762])

    def test_typing(self):
        self.assertEqual(
            self.tab.typing(
                [
                    "2640",
                    "четырехугольник",
                    "130",
                    "64.1481",
                    "17.9507",
                    "14.2942",
                    "14.2942",
                    "2739",
                    "[1503, 1504, 1564, 1563]",
                ]
            ),
            [
                2640,
                "четырехугольник",
                130,
                64.1481,
                17.9507,
                14.2942,
                14.2942,
                2739,
                [1503, 1504, 1564, 1563],
            ],
        )


if __name__ == "__main__":
    unittest.main()
