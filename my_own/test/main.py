import tkinter as tk

from bar_chart import draw_bars
from data import generate_data

def main():
    window = tk.Tk()
    window.title("Visualizer")
    window.geometry("800x400")

    canvas = tk.Canvas(window, width=800, height=350, bg="black")
    canvas.pack()

    data = generate_data()
    draw_bars(canvas, data, 800, 350)

    window.mainloop()


if __name__ == "__main__":
    main()
