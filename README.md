
# Описание

## Общее

Эта программа представляет собой графический интерфейс для работы с геометрическими данными и ячейками. Программа позволяет открывать файлы с данными, отображать их на холсте, изменять масштаб, искать ячейки и стержни, а также перекрашивать ячейки в зависимости от температуры.

Файлы геометрии должны быть в [формате](Geometry/Геометрия%20312%20твэл.csv).
Файлы ячеек должны быть в [формате](Geometry/cells(1%20ТВС%20напр.кан).csv).

## Основной функционал

- **Открытие файлов**: Возможность открыть файлы с геометрическими данными и данными ячеек.
- **Отображение данных**: Отрисовка ячеек и стержней на холсте.
- **Изменение масштаба**: Увеличение и уменьшение масштаба с помощью кнопок, колесика мыши и слайдера.
- **Поиск**: Поиск ячеек и стержней по их номерам (реализованно криво на данный момент).
- **Перекрашивание ячеек**: Перекрашивание ячеек в зависимости от температуры.
- **Перетаскивание файлов на вкладки "Геометрия" и "Ячейки"**: 

## Запуск программы

1. Убедитесь, что у вас установлены все необходимые зависимости
([список необходимых зависимостей](requirements.txt)) :
    - `tkinter`
    - `Pillow`
    - `colour`
    - `tkinterdnd2`

2. Скопируйте репозиторий на ваш локальный компьютер.

3. Перейдите в директорию с проектом.

4. Запустите файл `window.py`:
    ```sh
    python code/window.py
    ```
5. Программа откроется в новом окне. Вы можете использовать меню для открытия файлов, изменения масштаба и поиска ячеек и стержней.

## Пример использования

1. Откройте программу.
2. Выберите вкладку "Геометрия".
3. В меню выберите "File" -> "Open" для открытия файлов .csv с данными или просто перетащите нужный файл. Например [файл](Geometry/Геометрия%20312%20твэл.csv)
4. Перейдите на вкладку "Ячейки".
5. В меню выберите "File" -> "Open" для открытия файлов .csv с данными или просто перетащите нужный файл. Например [файл](Geometry/cells(1%20ТВС%20напр.кан).csv)
6. На вкладках "Геометрия" и "Ячейки" нажмите на кнопку "Применить".
7. Перейдите на вкладку "Рисунок" и в меню выберите "File" -> "Open", на вкладке отобразится рисунок.
8. Используйте кнопки "+" и "-" или колесико мыши для изменения масштаба.
9. Введите номер ячейки или стержня(пока не надо) в поле поиска и нажмите кнопку поиска для нахождения элемента.
10. Используйте чекбокс для перекрашивания ячеек.
