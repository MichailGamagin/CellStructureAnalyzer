import unittest
from tkinterdnd2 import TkinterDnD
from tkinter import ttk
from geometry import Geometry


class TestTab(unittest.TestCase):
    def setUp(self):
        self.root = TkinterDnD.Tk()
        self.notebooks = ttk.Notebook(self.root)
        self.tab = Geometry(self.root, self.notebooks)
        self.test_csv_path = "tests\\tests_data\Геометрия 4ТВС.csv"

    def test_fill_tree(self):
        data = self.tab.fill_tree(self.test_csv_path)
        self.assertEqual(len(data), 1564)
        self.assertEqual(data[0]["№"], "1")
        self.assertEqual(data[0]["Тип"], "твэл")
        self.assertEqual(data[0]["X"], '236.000000')
        self.assertEqual(data[0]["Y"], "236.000000")
        self.assertEqual(data[0]["Диаметр"], "9.100000")
        self.assertEqual(data[0]["Связан с элементами:"], [2, 3, 4, 5, 6, 7])

    def test_get_data_from_tree(self):
        self.tab.data = self.tab.fill_tree(self.test_csv_path)
        data = self.tab.get_data_from_tree(self.tab.data)
        self.assertEqual(len(data), 1531)
        self.assertEqual(data[390]["№"], 391)
        self.assertEqual(data[390]["Тип"], "стенка объекта")
        self.assertEqual(data[390]["X"], 221.167295)
        self.assertEqual(data[390]["Y"], 363.690999)
        self.assertEqual(data[390]["Диаметр"], 0)
        self.assertEqual(data[390]["Связан с элементами:"], [332, 390, 331, 0, 0, 0])

    def test_typing(self):
        self.assertEqual(
            self.tab.typing(["154", "стенка объекта", "929.167295", "363.690999", '0', "[1505, 1563, 1504, 0, 0, 0]"]),
            [154, "стенка объекта", 929.167295, 363.690999, 0, [1505, 1563, 1504, 0, 0, 0]],
        )



if __name__ == "__main__":
    unittest.main()
