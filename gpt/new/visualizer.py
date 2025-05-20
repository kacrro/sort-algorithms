import tkinter as tk
import random
from .constants import Config
from .sorts.bubble import BubbleSort
from .sorts.merge import MergeSort
from .sorts.quick import QuickSort
from .sorts.bucket import BucketSort


BAR_COUNT = Config.BAR_COUNT.value
MAX_HEIGHT = Config.MAX_HEIGHT.value
SPACING = Config.SPACING.value

class SortVisualizer:
    """Główna klasa obsługująca GUI i wizualizację."""
    def __init__(self, master):
        self.master = master
        master.title("Sort Visualizer")
        self.width, self.height = 800, 400

        self.default_color = "#03a609"
        self.highlight_color = "white"

        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Inicjalizacja danych
        self.data = [random.randint(1, MAX_HEIGHT) for _ in range(BAR_COUNT)]
        total_unit = self.width / BAR_COUNT
        self.bar_width = total_unit - SPACING

        self.bars, self.texts = [], []
        for idx, height in enumerate(self.data):
            x0 = idx * total_unit + SPACING / 2
            x1 = x0 + self.bar_width
            y1 = self.height
            y0 = y1 - (height / MAX_HEIGHT) * self.height

            bar = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=self.default_color, outline=self.default_color
            )
            text = self.canvas.create_text(
                (x0 + x1) / 2, y0 - 10,
                text=str(height), fill="white", font=("Arial", 8)
            )
            self.bars.append(bar)
            self.texts.append(text)

        frame = tk.Frame(master, bg="black")
        frame.pack(pady=10)

        self.algorithms = [BubbleSort(), MergeSort(), QuickSort(), BucketSort()]
        for algorithm in self.algorithms:
            btn = tk.Button(
                frame, text=algorithm.name,
                bg=self.default_color, fg="black",
                command=lambda a=algorithm: self.start_sort(a), width=10
            )
            btn.pack(side=tk.LEFT, padx=5)

    def disable_buttons(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    btn.config(state=tk.NORMAL)

    def highlight(self, idx: int, color: str):
        self.canvas.itemconfig(self.bars[idx], fill=color, outline=color)
        self.canvas.itemconfig(self.texts[idx], fill=color)
        self.canvas.update()

    def swap_bars(self, i: int, j: int):
        # Zamiana danych i aktualizacja widoku
        self.data[i], self.data[j] = self.data[j], self.data[i]
        for idx in (i, j):
            self.update_bar(idx)

    def update_bar(self, idx: int):
        # Aktualizacja pozycji i tekstu konkretnego słupka
        height = self.data[idx]
        total_unit = self.width / BAR_COUNT
        x0 = idx * total_unit + SPACING / 2
        x1 = x0 + self.bar_width
        y1 = self.height
        y0 = y1 - (height / MAX_HEIGHT) * self.height

        self.canvas.coords(self.bars[idx], x0, y0, x1, y1)
        self.canvas.coords(self.texts[idx], (x0 + x1) / 2, y0 - 10)
        self.canvas.itemconfig(self.texts[idx], text=str(height))
        self.canvas.update()

    def start_sort(self, algorithm):
        """Uruchamia wybrany algorytm sortowania."""
        self.disable_buttons()
        algorithm.sort(self.data, self)
        self.enable_buttons()