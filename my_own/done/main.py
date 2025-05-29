import random
import tkinter as tk

from my_own.done.bar_chart import draw_bars

from my_own.done.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_BG_COLOR, CANVAS_WIDTH, CANVAS_HEIGHT, BAR_COUNT, RANGE
from my_own.done.data import generate_data


def main():

    # Window
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

    # Canvas
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=WINDOW_BG_COLOR)
    canvas.pack()

    # Data
    data = generate_data()

    # EXPORT THIS FUNCTION TO data.py

    def reset_data():
        nonlocal data
        data = generate_data()
        canvas.delete("all")
        draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Reset button
    reset_button = tk.Button(window, text="Reset", command=reset_data)
    reset_button.pack()

    # Bars
    draw_bars(canvas, data, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Loop
    window.mainloop()


if __name__ == "__main__":
    main()
