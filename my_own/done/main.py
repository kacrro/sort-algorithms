import random
import tkinter as tk

from my_own.done.bar_chart import draw_bars

# Window parameters
WINDOW_TITLE = "fajne oknienko do sortowania liczb"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
WINDOW_BG_COLOR = "#000000"

# Canvas parameters
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400

# Data parameters
BAR_COUNT = 50
a = 1
b = 10
RANGE = (a, b)


def main():
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=WINDOW_BG_COLOR)
    canvas.pack()

    # Inicjalizacja danych
    data = [random.randint(*RANGE) for _ in range(BAR_COUNT)]
    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)
    window.mainloop()


if __name__ == "__main__":
    main()
