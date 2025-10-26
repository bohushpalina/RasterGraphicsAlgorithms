import tkinter as tk
from tkinter import ttk, messagebox

# Константы холста / сетки
CANVAS_W = 1000
CANVAS_H = 800
STEP = 10  # размер "пикселя" (ячейки сетки)
GRID_W = CANVAS_W // STEP
GRID_H = CANVAS_H // STEP


class RasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Растровые алгоритмы визуализации (ЦДА, Брезенхем и др.)")
        self.root.geometry("1300x900")
        self.root.configure(bg="#e0ddd3")

        self.step = STEP  # размер "пикселя" в сетке

        # ==== Основная сетка ====
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=4)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # ==== Поле рисования ====
        canvas_frame = ttk.LabelFrame(main_frame, text="Поле рисования")
        canvas_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="white", width=CANVAS_W, height=CANVAS_H)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.draw_grid()

        self.coord_label = ttk.Label(canvas_frame, text="Координаты: ( , )")
        self.coord_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.canvas.bind("<Motion>", self.update_coords)

        # ==== Правая панель ====
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=1, sticky="ns")
        control_frame.grid_propagate(False)

        # ====== Параметры ======
        params_frame = ttk.LabelFrame(control_frame, text="Параметры")
        params_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(params_frame, text="x₁:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.x1_entry = ttk.Entry(params_frame, width=8)
        self.x1_entry.grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(params_frame, text="y₁:").grid(row=0, column=2, padx=5, pady=3, sticky="e")
        self.y1_entry = ttk.Entry(params_frame, width=8)
        self.y1_entry.grid(row=0, column=3, padx=5, pady=3)

        ttk.Label(params_frame, text="x₂:").grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.x2_entry = ttk.Entry(params_frame, width=8)
        self.x2_entry.grid(row=1, column=1, padx=5, pady=3)

        ttk.Label(params_frame, text="y₂:").grid(row=1, column=2, padx=5, pady=3, sticky="e")
        self.y2_entry = ttk.Entry(params_frame, width=8)
        self.y2_entry.grid(row=1, column=3, padx=5, pady=3)

        ttk.Separator(params_frame, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky="ew", pady=8)

        ttk.Label(params_frame, text="Радиус:").grid(row=3, column=0, padx=5, pady=3, sticky="e")
        self.radius_entry = ttk.Entry(params_frame, width=8)
        self.radius_entry.grid(row=3, column=1, padx=5, pady=3)

        ttk.Label(params_frame, text="(x₀, y₀):").grid(row=4, column=0, padx=5, pady=3, sticky="e")
        self.center_x_entry = ttk.Entry(params_frame, width=8)
        self.center_x_entry.grid(row=4, column=1, padx=5, pady=3)
        self.center_y_entry = ttk.Entry(params_frame, width=8)
        self.center_y_entry.grid(row=4, column=2, padx=5, pady=3)

        # ====== Алгоритмы ======
        algo_frame = ttk.LabelFrame(control_frame, text="Алгоритмы")
        algo_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(algo_frame, text="Пошаговый алгоритм", width=25, command=self.draw_step).pack(pady=5)
        ttk.Button(algo_frame, text="ЦДА (отрезок)", width=25, command=self.draw_dda).pack(pady=5)
        ttk.Button(algo_frame, text="Брезенхем (отрезок)", width=25, command=self.draw_bresenham_line).pack(pady=5)
        ttk.Button(algo_frame, text="Брезенхем (окружность)", width=25, command=self.draw_bresenham_circle).pack(pady=5)

        ttk.Separator(control_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(control_frame, text="Очистить поле", width=25, command=self.clear_canvas).pack(pady=10)

    # ======= Рисование и утилиты =======
    def draw_pixel(self, x, y, color="black"):
        """Рисует пиксель (ячейку сетки). x,y — в координатах клетки."""
        if not (0 <= x < GRID_W and 0 <= y < GRID_H):
            return  # игнорируем точки вне области
        step = self.step
        x1, y1 = x * step, y * step
        self.canvas.create_rectangle(x1, y1, x1 + step, y1 + step, fill=color, outline=color)

    def draw_grid(self):
        """Рисует сетку (фон). Очищает canvas."""
        self.canvas.delete("all")
        # светлая рамка
        self.canvas.create_rectangle(0, 0, CANVAS_W, CANVAS_H, outline="#bbb", width=2)
        # линии
        for x in range(0, CANVAS_W, self.step):
            self.canvas.create_line(x, 0, x, CANVAS_H, fill="#eee")
        for y in range(0, CANVAS_H, self.step):
            self.canvas.create_line(0, y, CANVAS_W, y, fill="#eee")

    def update_coords(self, event):
        gx = event.x // self.step
        gy = event.y // self.step
        if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
            self.coord_label.config(text=f"Координаты: ({gx}, {gy})")
        else:
            self.coord_label.config(text="Координаты: ( , )")

    def get_line_coords(self):
        """Считывает координаты отрезка (ячейки). Возвращает кортеж или None."""
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для координат!")
            return None

        # Проверим диапазон (необязательно, но полезно)
        if not (0 <= x1 < GRID_W and 0 <= y1 < GRID_H and 0 <= x2 < GRID_W and 0 <= y2 < GRID_H):
            if messagebox.askyesno("Вне области", "Координаты выходят за пределы поля. Продолжить и обрезать?"):
                # можно обрезать точки в границы
                x1 = max(0, min(GRID_W - 1, x1))
                y1 = max(0, min(GRID_H - 1, y1))
                x2 = max(0, min(GRID_W - 1, x2))
                y2 = max(0, min(GRID_H - 1, y2))
            else:
                return None

        return x1, y1, x2, y2

    # ======= Алгоритмы =======
    def draw_step(self):
        """Пошаговый (простой) алгоритм (как в учебнике)."""
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            # единичная точка
            self.draw_pixel(x1, y1)
            return

        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            self.draw_pixel(round(x), round(y))
            x += x_inc
            y += y_inc

    def draw_dda(self):
        """Алгоритм ЦДА (DDA)."""
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self.draw_pixel(x1, y1, color="blue")
            return

        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            self.draw_pixel(round(x), round(y), color="blue")
            x += x_inc
            y += y_inc

    def draw_bresenham_line(self):
        """Алгоритм Брезенхема для отрезка."""
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords

        # стандартный целочисленный алгоритм
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x = x1
        y = y1
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        if dx >= dy:
            err = dx // 2
            while True:
                self.draw_pixel(x, y, color="green")
                if x == x2 and y == y2:
                    break
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy // 2
            while True:
                self.draw_pixel(x, y, color="green")
                if x == x2 and y == y2:
                    break
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def draw_bresenham_circle(self):
        """Алгоритм Брезенхема для окружности (центр и радиус в клетках)."""
        try:
            xc = int(self.center_x_entry.get())
            yc = int(self.center_y_entry.get())
            r = int(self.radius_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые центр (x0,y0) и радиус!")
            return

        if r < 0:
            messagebox.showerror("Ошибка", "Радиус должен быть >= 0")
            return

        x = 0
        y = r
        d = 3 - 2 * r

        def plot_circle_points(xc_, yc_, x_, y_):
            pts = [
                (xc_ + x_, yc_ + y_), (xc_ - x_, yc_ + y_),
                (xc_ + x_, yc_ - y_), (xc_ - x_, yc_ - y_),
                (xc_ + y_, yc_ + x_), (xc_ - y_, yc_ + x_),
                (xc_ + y_, yc_ - x_), (xc_ - y_, yc_ - x_),
            ]
            for px, py in pts:
                self.draw_pixel(px, py, color="red")

        # специальный случай r == 0
        if r == 0:
            self.draw_pixel(xc, yc, color="red")
            return

        while y >= x:
            plot_circle_points(xc, yc, x, y)
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

    # ======= Вспомогательные =======
    def clear_canvas(self):
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterApp(root)
    root.mainloop()
