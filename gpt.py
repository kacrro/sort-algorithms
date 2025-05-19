import tkinter as tk
import random
import time

BAR_COUNT = 50
MAX_HEIGHT = 100
DELAY = 0.001  # sekundy


class BubbleSortApp:
    def __init__(self, master):
        self.master = master
        master.title("Bubble Sort Visualizer")
        self.width = 800
        self.height = 400

        # Canvas
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # generate data
        self.data = [random.randint(1, MAX_HEIGHT) for _ in range(BAR_COUNT)]
        self.bar_width = self.width / BAR_COUNT

        # Draw initial bars
        self.bars = []
        for i, h in enumerate(self.data):
            x0 = i * self.bar_width
            y0 = self.height - (h / MAX_HEIGHT) * self.height
            x1 = (i + 1) * self.bar_width
            y1 = self.height
            bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="green")
            self.bars.append(bar)

        # Sort button
        btn = tk.Button(master, text="Sortuj", bg="green", fg="black",
                        command=self.start_sort)
        btn.pack(pady=10)

    def start_sort(self):
        # wyłącz przycisk, żeby nie klikać w trakcie
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)
        self.bubble_sort()

    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                # podświetl aktualny słupek
                self.canvas.itemconfig(self.bars[j], fill="white", outline="white")
                self.canvas.update()
                time.sleep(DELAY)

                if self.data[j] > self.data[j + 1]:
                    # zamień wartości w liście
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    # zamień słupki na ekranie
                    x0 = j * self.bar_width
                    x1 = (j + 1) * self.bar_width
                    # przesunięcie wysokości
                    h0 = self.data[j]
                    h1 = self.data[j + 1]
                    y0_0 = self.height - (h0 / MAX_HEIGHT) * self.height
                    y0_1 = self.height - (h1 / MAX_HEIGHT) * self.height
                    # update obu prostokątów
                    self.canvas.coords(self.bars[j], x0, y0_0, x0 + self.bar_width, self.height)
                    self.canvas.coords(self.bars[j + 1], x1, y0_1, x1 + self.bar_width, self.height)
                    self.canvas.update()
                    time.sleep(DELAY)

                # przywróć zielony kolor
                self.canvas.itemconfig(self.bars[j], fill="green", outline="green")

        # po zakończeniu włącz przycisk
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = BubbleSortApp(root)
    root.mainloop()
