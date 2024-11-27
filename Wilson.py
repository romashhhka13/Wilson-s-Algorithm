import time
import tkinter as tk

from random import *
from tkinter import messagebox
from PIL import ImageGrab

from Maze import *


color1 = "#DDA0DD"
color2 = "#EEAEEE"
color3 = "#CD96CD"
color4 = "red"


class Generator():
    def __init__(self):

        self.maze = Maze(width=5, height=5)
        self.cells = [[]]
        self.wall_ver = [[]]
        self.wall_hor = [[]]
        self.flag_save = False

        """Настройка размеров окна, ячейки лабиринта"""
        self.root = tk.Tk()
        self.root.configure(bg=color2)
        self.root.title("Алгоритм Уилсона для генерациия лабиринта")

        self.width_root = 1000
        self.height_root = 650
        self.k = self.width_root / (self.height_root - 50)
        width_screen = self.root.winfo_screenwidth()
        height_screen = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width_root}x{self.height_root}"
                           f"+{int((width_screen - self.width_root) / 2)}"
                           f"+{int((height_screen - self.height_root) / 3)}")
        self.root.resizable(width=False, height=False)


        self.width_wall = 2
        self.width_cell = 0

        if self.maze.GetWidth()/self.maze.GetHeight() > self.k:
            self.width_cell = self.width_root / self.maze.GetWidth()
        else:
            self.width_cell = (self.height_root - 50) / self.maze.GetHeight()


        """Разбиение на фреймы"""
        self.frameMenu = tk.Frame(self.root, height=50, bg=color1)
        self.frameMenu.place(relx=0, relwidth=1, rely=0)

        self.canvasMaze = tk.Canvas(self.root, highlightthickness=0,
                                    highlightbackground="black", bg=color2,
                                  width=self.width_cell * self.maze.GetWidth() - 2,
                                    height=self.width_cell * self.maze.GetHeight() - 2)
        self.canvasMaze.place(anchor='center', relx=0.5, y=350)


        """Создание кнопок и полей для взаимодействия с пользователем"""
        self.entry_width = tk.Entry(self.frameMenu, bg=color1, font=("Times New Roman", 14))
        self.entry_width.place(relx=0.12, rely=0.5, anchor="center", relheight=0.7, relwidth=0.2)
        self.entry_width.insert(0, " Ширина:")
        self.entry_width.bind("<FocusIn>", self.focus_in_width)
        self.entry_width.bind("<FocusOut>", self.focus_out_width)

        self.entry_height = tk.Entry(self.frameMenu, bg=color1, font=("Times New Roman", 14))
        self.entry_height.place(relx=0.33, rely=0.5, anchor="center", relheight=0.7, relwidth=0.2)
        self.entry_height.insert(0, " Высота:")
        self.entry_height.bind("<FocusIn>", self.focus_in_height)
        self.entry_height.bind("<FocusOut>", self.focus_out_height)

        self.btn_start = tk.Button(self.frameMenu, text="Генерировать", command=self.start,
                                   font=("Times New Roman", 14), bg=color1, cursor="hand2")
        self.btn_start.place(relx=0.9, rely=0.5, anchor="center", relheight=0.7, relwidth=0.15)

        self.btn_load = tk.Button(self.frameMenu, text="Загрузить", command=self.load,
                                   font=("Times New Roman", 14), bg=color1, cursor="hand2")
        self.btn_load.place(relx=0.54, rely=0.5, anchor="center", relheight=0.7, relwidth=0.15)

        self.btn_save = tk.Button(self.frameMenu, text="Сохранить", command=self.save,
                                   font=("Times New Roman", 14), bg=color1, cursor="hand2")
        self.btn_save.place(relx=0.72, rely=0.5, anchor="center", relheight=0.7, relwidth=0.15)

        self.root.mainloop()


    def save(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Название файла")
        entry_window.configure(bg=color2)
        width_screen = entry_window.winfo_screenwidth()
        height_screen = entry_window.winfo_screenheight()
        entry_window.geometry(f"{300}x{200}"
                              f"+{int((width_screen - 300) / 2)}"
                              f"+{int((height_screen - 200) / 3)}")

        label = tk.Label(entry_window, font=("Times New Roman", 14), bg=color2)
        label.configure(text="Название файла и картинки")
        label.place(anchor="center", relx=0.5, rely=0.2)

        entry_widget = tk.Entry(entry_window, font=("Times New Roman", 14), bg=color2)
        entry_widget.place(anchor="center", relx=0.5, rely=0.4, relwidth=0.8)

        # Функция, которая будет вызываться при нажатии кнопки ввода
        def on_submit():

            if self.flag_save:

                file_path = "./data/" + entry_widget.get()
                image_path = "./image/" + entry_widget.get() + ".png"
                entry_window.destroy()

                s = ""

                with open(file_path, "w") as file:
                    file.write(str(self.maze.GetHeight()) + "\n")
                    file.write(str(self.maze.GetWidth()) + "\n")
                    for i in range(self.maze.GetHeight()):
                        for j in range(self.maze.GetWidth()):
                            s += "1" if self.maze.cells[i][j].Bottom else "0"
                            s += "1" if self.maze.cells[i][j].Right else "0"
                        file.write(s + "\n")
                        s = ""
                time.sleep(0.3)
                x = self.canvasMaze.winfo_x() + self.root.winfo_rootx() - 1
                y = self.canvasMaze.winfo_y() + self.root.winfo_rooty() - 1
                width = self.canvasMaze.winfo_reqwidth() + 2
                height = self.canvasMaze.winfo_reqheight() + 2
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.save(image_path)

            else:
                entry_window.destroy()
                messagebox.showerror("Ошибка", "Лабиринт не сгенерирован")

        # Создаем кнопку для отправки текста
        submit_button = tk.Button(entry_window, text="Сохранить", command=on_submit,
                                  font=("Times New Roman", 12), bg=color2,
                                  cursor="hand2")
        submit_button.place(anchor="center", relx=0.5, rely=0.75)


    def load(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Название файла")
        entry_window.configure(bg=color2)
        width_screen = entry_window.winfo_screenwidth()
        height_screen = entry_window.winfo_screenheight()
        entry_window.geometry(f"{300}x{200}"
                              f"+{int((width_screen - 300) / 2)}"
                              f"+{int((height_screen - 200) / 3)}")

        label = tk.Label(entry_window, font=("Times New Roman", 14), bg=color2)
        label.configure(text="Название файла")
        label.place(anchor="center", relx=0.5, rely=0.2)


        entry_widget = tk.Entry(entry_window, font=("Times New Roman", 14), bg=color2)
        entry_widget.place(anchor="center", relx=0.5, rely=0.4, relwidth=0.8)

        # Функция, которая будет вызываться при нажатии кнопки ввода
        def on_submit():
            file_path = "./data/" + entry_widget.get()
            self.canvasMaze.delete("all")
            self.flag_save = False

            try:
                with open(file_path, "r") as file:
                    height = int(file.readline())
                    width = int(file.readline())

                    self.maze = Maze(width=width, height=height)
                    self.DetermineSize()

                    self.cells = [[0] * self.maze.GetWidth() for i in range(self.maze.GetHeight())]
                    self.wall_ver = [[0] * (self.maze.GetWidth() - 1) for i in range(self.maze.GetHeight())]
                    self.wall_hor = [[0] * self.maze.GetWidth() for i in range(self.maze.GetHeight() - 1)]

                    for row in range(self.maze.GetHeight()):
                        for column in range(self.maze.GetWidth()):
                            rect = self.canvasMaze.create_rectangle(column * self.width_cell, row * self.width_cell,
                                                                    (column + 1) * self.width_cell,
                                                                    (row + 1) * self.width_cell,
                                                                    fill=color2, outline="")
                            self.cells[row][column] = rect

                            if column != self.maze.GetWidth() - 1:
                                line_ver = self.canvasMaze.create_line((column + 1) * self.width_cell,
                                                                       row * self.width_cell,
                                                                       (column + 1) * self.width_cell,
                                                                       (row + 1) * self.width_cell,
                                                                       width=self.width_wall)
                                self.wall_ver[row][column] = line_ver

                            if row != self.maze.GetHeight() - 1:
                                line_hor = self.canvasMaze.create_line(column * self.width_cell,
                                                                       (row + 1) * self.width_cell,
                                                                       (column + 1) * self.width_cell,
                                                                       (row + 1) * self.width_cell,
                                                                       width=self.width_wall)
                                self.wall_hor[row][column] = line_hor

                    for i in range(height):
                        s = file.readline()
                        for index, sym in enumerate(s):
                            if index % 2 == 0 and sym == "1" and i != (height - 1):
                                self.canvasMaze.delete(self.wall_hor[i][index//2])

                            if index % 2 == 1 and sym == "1" and (index // 2) != width - 1:
                                self.canvasMaze.delete(self.wall_ver[i][index//2])

                    entry_window.destroy()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", f"Файл '{entry_widget.get()}' не найден.")
                entry_window.destroy()

        # Создаем кнопку для отправки текста
        submit_button = tk.Button(entry_window, text="Загрузить", command=on_submit,
                                  font=("Times New Roman", 12), bg=color2,
                                  cursor="hand2")
        submit_button.place(anchor="center", relx=0.5, rely=0.75)


    def start(self):
        flag: bool = False
        width = 0
        height = 0

        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            flag = True
        except:
            messagebox.showerror("Ошибка", "Введите корректные параметры!")

        if flag and (width <= 100 and height <= 100):

            self.maze = Maze(width=width, height=height)
            self.DetermineSize()

            self.cells = [[0] * self.maze.GetWidth() for i in range(self.maze.GetHeight())]
            self.wall_ver = [[0] * (self.maze.GetWidth() - 1) for i in range(self.maze.GetHeight())]
            self.wall_hor = [[0] * self.maze.GetWidth() for i in range(self.maze.GetHeight() - 1)]


            for row in range(self.maze.GetHeight()):
                for column in range(self.maze.GetWidth()):
                    rect = self.canvasMaze.create_rectangle(column * self.width_cell, row * self.width_cell,
                                                            (column + 1) * self.width_cell,
                                                            (row + 1) * self.width_cell,
                                                            fill=color2, outline="")
                    self.cells[row][column] = rect

                    if column != self.maze.GetWidth() - 1:
                        line_ver = self.canvasMaze.create_line((column + 1) * self.width_cell,
                                                               row * self.width_cell,
                                                               (column + 1) * self.width_cell,
                                                               (row + 1) * self.width_cell,
                                                               width=self.width_wall)
                        self.wall_ver[row][column] = line_ver

                    if row != self.maze.GetHeight() - 1:
                        line_hor = self.canvasMaze.create_line(column * self.width_cell,
                                                               (row + 1) * self.width_cell,
                                                               (column + 1) * self.width_cell,
                                                               (row + 1) * self.width_cell,
                                                               width=self.width_wall)
                        self.wall_hor[row][column] = line_hor

            self.Wilson()
            self.flag_save = True

        elif flag:
            messagebox.showerror("Большие значения",  "Ширина и высота должны быть меньше 100!")


    def DetermineSize(self):
        if self.maze.GetWidth()/self.maze.GetHeight() > self.k:
            self.width_cell = self.width_root / self.maze.GetWidth()
        else:
            self.width_cell = (self.height_root - 50) / self.maze.GetHeight()

        self.canvasMaze.configure(width=self.width_cell * self.maze.GetWidth() - 2,
                                  height=self.width_cell * self.maze.GetHeight() - 2,
                                  highlightthickness=1)

    def focus_out_width(self, event):
        if self.entry_width.get() == "":
            self.entry_width.insert(0, " Ширина:")

    def focus_in_width(self, event):
        if self.entry_width.get() == " Ширина:":
            self.entry_width.delete(0, 'end')

    def focus_out_height(self, event):
        if self.entry_height.get() == "":
            self.entry_height.insert(0, " Высота:")

    def focus_in_height(self, event):
        if self.entry_height.get() == " Высота:":
            self.entry_height.delete(0, 'end')

    def RandomCell(self):

        curr_x = randint(0, self.maze.GetWidth() - 1)
        curr_y = randint(0, self.maze.GetHeight() - 1)

        while self.maze.cells[curr_y][curr_x].visited:
            curr_x = randint(0, self.maze.GetWidth() - 1)
            curr_y = randint(0, self.maze.GetHeight() - 1)

        return Pair(curr_x, curr_y)

    def FindAdjacentCells(self, curr_x: int, curr_y: int):

        free_cell: list = []

        if curr_x > 0:
            free_cell.append(Pair(curr_x - 1, curr_y))

        if curr_x < (self.maze.GetWidth() - 1):
            free_cell.append(Pair(curr_x + 1, curr_y))

        if curr_y > 0:
            free_cell.append(Pair(curr_x, curr_y - 1))

        if curr_y < (self.maze.GetHeight() - 1):
            free_cell.append(Pair(curr_x, curr_y + 1))

        return free_cell


    def hasCycle(self, path: list, x: int, y: int):

        for i in range(len(path)):
            if path[i].x == x and path[i].y == y:
                for j in range(i + 1, len(path)):
                    self.canvasMaze.itemconfig(self.cells[path[-1].y][path[-1].x], fill=color2)
                    self.canvasMaze.update()
                    path.pop(-1)
                return True

        return False


    def OpenWall(self, first: Pair, second: Pair):

        x1: int = first.x
        x2: int = second.x
        y1: int = first.y
        y2: int = second.y

        if x1 == x2:

            if y1 < y2:
                self.maze.cells[y1][x1].Bottom = True
                self.maze.cells[y2][x2].Top = True
                self.canvasMaze.delete(self.wall_hor[y1][x1])

            else:
                self.maze.cells[y1][x1].Top = True
                self.maze.cells[y2][x2].Bottom = True
                self.canvasMaze.delete(self.wall_hor[y2][x2])

        if y1 == y2:
            if x1 < x2:
                self.maze.cells[y1][x1].Right = True
                self.maze.cells[y2][x2].Left = True
                self.canvasMaze.delete(self.wall_ver[y1][x1])

            else:
                self.maze.cells[y1][x1].Left = True
                self.maze.cells[y2][x2].Right = True
                self.canvasMaze.delete(self.wall_ver[y2][x2])


    def Wilson(self):

        unvisitedCells: int = self.maze.GetWidth() * self.maze.GetHeight();

        start_x: int = randint(0, self.maze.GetWidth() - 1)
        start_y: int = randint(0, self.maze.GetHeight() - 1)
        self.canvasMaze.itemconfig(self.cells[start_y][start_x], fill=color3)

        self.maze.cells[start_y][start_x].visited = True
        unvisitedCells -= 1

        while unvisitedCells > 0:

            path: list = []
            pair = self.RandomCell()
            path.append(pair)
            curr_x: int = pair.x
            curr_y: int = pair.y
            self.canvasMaze.itemconfig(self.cells[curr_y][curr_x], fill=color4)

            while not self.maze.cells[curr_y][curr_x].visited:

                adjacent_cells: list = self.FindAdjacentCells(curr_x=curr_x, curr_y=curr_y)
                rand_cell: int = randint(0, len(adjacent_cells) - 1)
                curr_x = adjacent_cells[rand_cell].x
                curr_y = adjacent_cells[rand_cell].y

                if not self.hasCycle(path, curr_x, curr_y):
                    path.append(Pair(curr_x, curr_y))
                    self.canvasMaze.itemconfig(self.cells[curr_y][curr_x], fill=color4)
                    self.canvasMaze.update()
                    time.sleep(0.05)


            for i in range(len(path)):
                unvisitedCells -= 1
                self.maze.cells[path[i].y][path[i].x].visited = True
                self.canvasMaze.itemconfig(self.cells[path[i].y][path[i].x], fill=color3)
                if i != len(path) - 1:
                    self.OpenWall(path[i], path[i + 1])

            unvisitedCells += 1

            self.canvasMaze.update()
            time.sleep(0.05)

        messagebox.showinfo("Конец!", "Лабиринт сгенерирован!")

if __name__ == "__main__":
    g = Generator()
