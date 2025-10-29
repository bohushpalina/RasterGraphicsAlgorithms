# Растровые алгоритмы — визуализатор (Tkinter)

**Кратко:** приложение на Python/Tkinter для иллюстрации базовых растровых алгоритмов:
- пошаговый алгоритм,
- ЦДА (DDA),
- алгоритм Брезенхема для отрезка,
- алгоритм Брезенхема для окружности.

Приложение рисует пиксели на клетчатом поле (каждая клетка — "пиксель").  
Интерфейс: большое поле слева, параметры и кнопки — справа. Поля ввода: `x1,y1,x2,y2`, `x0,y0,radius`.

---

## Содержимое репозитория
- `main.py` — основной код приложения (Tkinter).
- `README.md` — это руководство.
- `Отчет.docx` — отчёт (с примерами и измерениями).
- `dist/` — папка с `exe` после сборки PyInstaller.

---

## Требования
- Python 3.8+ (рекомендуется 3.9–3.11).
- Модули: стандартная библиотека (tkinter, ttk, time, math и т.д.) — ничего дополнительного не нужно.

---

## Запуск (локально)
```bash
python main.py

# Запуск через Docker

```bash
git clone https://github.com/<твой_ник>/DDA-Bresenham-Visualizer.git
cd DDA-Bresenham-Visualizer
sudo docker build -t raster-app .
xhost +local:docker
sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix raster-app
