import tkinter as tk
from tkinter import ttk, messagebox

STEP = 10

class RasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raster Visualizer")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=4)
        root.columnconfigure(1, weight=1)

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Motion>", self.update_coords)

        self.step = STEP
        self.grid_w = 0
        self.grid_h = 0
        self.draw_grid(800, 600)

        control_frame = ttk.Frame(root, padding=10)
        control_frame.grid(row=0, column=1, sticky="ns")

        coords_frame = ttk.LabelFrame(control_frame, text="Координаты")
        coords_frame.pack(fill="x", pady=5)
        ttk.Label(coords_frame, text="x1:").grid(row=0, column=0)
        ttk.Label(coords_frame, text="y1:").grid(row=0, column=2)
        ttk.Label(coords_frame, text="x2:").grid(row=1, column=0)
        ttk.Label(coords_frame, text="y2:").grid(row=1, column=2)
        self.x1_entry = ttk.Entry(coords_frame, width=5)
        self.y1_entry = ttk.Entry(coords_frame, width=5)
        self.x2_entry = ttk.Entry(coords_frame, width=5)
        self.y2_entry = ttk.Entry(coords_frame, width=5)
        self.x1_entry.grid(row=0, column=1)
        self.y1_entry.grid(row=0, column=3)
        self.x2_entry.grid(row=1, column=1)
        self.y2_entry.grid(row=1, column=3)

        circle_frame = ttk.LabelFrame(control_frame, text="Окружность")
        circle_frame.pack(fill="x", pady=5)
        ttk.Label(circle_frame, text="x₀:").grid(row=0, column=0)
        ttk.Label(circle_frame, text="y₀:").grid(row=0, column=2)
        ttk.Label(circle_frame, text="r:").grid(row=1, column=0)
        self.center_x_entry = ttk.Entry(circle_frame, width=5)
        self.center_y_entry = ttk.Entry(circle_frame, width=5)
        self.radius_entry = ttk.Entry(circle_frame, width=5)
        self.center_x_entry.grid(row=0, column=1)
        self.center_y_entry.grid(row=0, column=3)
        self.radius_entry.grid(row=1, column=1)

        algo_frame = ttk.LabelFrame(control_frame, text="Алгоритмы")
        algo_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(algo_frame, text="Пошаговый", width=25, command=self.draw_step).pack(pady=2)
        ttk.Button(algo_frame, text="ЦДА (DDA)", width=25, command=self.draw_dda).pack(pady=2)
        ttk.Button(algo_frame, text="Брезенхем (отрезок)", width=25, command=self.draw_bresenham_line).pack(pady=2)
        ttk.Button(algo_frame, text="Брезенхем (окружность)", width=25, command=self.draw_bresenham_circle).pack(pady=2)

        ttk.Separator(control_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(control_frame, text="Очистить", width=25, command=self.clear_canvas).pack(pady=5)

        self.coord_label = ttk.Label(control_frame, text="Координаты: ( , )")
        self.coord_label.pack(pady=5)

    def draw_grid(self, width, height):
        self.canvas.delete("all")
        self.grid_w = width // self.step
        self.grid_h = height // self.step
        self.canvas.create_rectangle(0, 0, width, height, outline="#bbb", width=2)
        for x in range(0, width, self.step):
            self.canvas.create_line(x, 0, x, height, fill="#eee")
        for y in range(0, height, self.step):
            self.canvas.create_line(0, y, width, y, fill="#eee")

    def draw_pixel(self, x, y, color="black"):
        if not (0 <= x < self.grid_w and 0 <= y < self.grid_h):
            return
        s = self.step
        self.canvas.create_rectangle(x * s, y * s, (x + 1) * s, (y + 1) * s, fill=color, outline=color)

    def on_resize(self, event):
        self.draw_grid(event.width, event.height)

    def update_coords(self, event):
        gx = event.x // self.step
        gy = event.y // self.step
        if 0 <= gx < self.grid_w and 0 <= gy < self.grid_h:
            self.coord_label.config(text=f"Координаты: ({gx}, {gy})")
        else:
            self.coord_label.config(text="Координаты: ( , )")

    def get_line_coords(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            return x1, y1, x2, y2
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа координат!")
            return None

    def draw_step(self):
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx, dy = x2 - x1, y2 - y1
        if dx == 0:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.draw_pixel(x1, y)
            return
        k = dy / dx
        if abs(dx) >= abs(dy):
            if x1 > x2:
                x1, x2, y1, y2 = x2, x1, y2, y1
                dx, dy = x2 - x1, y2 - y1
                k = dy / dx
            for x in range(x1, x2 + 1):
                y = round(y1 + k * (x - x1))
                self.draw_pixel(x, y)
        else:
            if y1 > y2:
                x1, x2, y1, y2 = x2, x1, y2, y1
                dx, dy = x2 - x1, y2 - y1
                k = dy / dx
            inv_k = dx / dy
            for y in range(y1, y2 + 1):
                x = round(x1 + inv_k * (y - y1))
                self.draw_pixel(x, y)

    def draw_dda(self):
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            self.draw_pixel(x1, y1, color="blue")
            return
        x_inc, y_inc = dx / steps, dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            self.draw_pixel(round(x), round(y), color="blue")
            x += x_inc
            y += y_inc

    def draw_bresenham_line(self):
        coords = self.get_line_coords()
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.draw_pixel(x1, y1, color="green")
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_bresenham_circle(self):
        try:
            xc = int(self.center_x_entry.get())
            yc = int(self.center_y_entry.get())
            r = int(self.radius_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите центр и радиус!")
            return
        x, y = 0, r
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
        while y >= x:
            plot_circle_points(xc, yc, x, y)
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

    def clear_canvas(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.draw_grid(w, h)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = RasterApp(root)
    root.mainloop()
