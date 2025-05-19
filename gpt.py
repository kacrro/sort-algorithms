import tkinter as tk
import random
import time

BAR_COUNT = 50
MAX_HEIGHT = 100
DELAY = 0.01  # sekundy
SPACING = 2  # px odstępu między słupkami

class BubbleSortApp:
    def __init__(self, master):
        self.master = master
        master.title("Bubble Sort Visualizer")
        self.width = 800
        self.height = 600

        # Canvas
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # generate data
        self.data = [random.randint(1, MAX_HEIGHT) for _ in range(BAR_COUNT)]
        total_unit = self.width / BAR_COUNT
        self.bar_width = total_unit - SPACING

        # Draw initial bars + texts
        self.bars  = []
        self.texts = []
        for i, h in enumerate(self.data):
            x0 = i * total_unit + SPACING/2
            x1 = x0 + self.bar_width
            y1 = self.height
            y0 = y1 - (h / MAX_HEIGHT) * self.height
            # słupek
            bar = self.canvas.create_rectangle(x0, y0, x1, y1,
                                               fill="green", outline="green")
            # wartość nad słupkiem
            txt = self.canvas.create_text(
                (x0+x1)/2, y0 - 10,
                text=str(h), fill="white", font=("Arial", 8)
            )
            self.bars.append(bar)
            self.texts.append(txt)

        # Sort button
        btn = tk.Button(master, text="Sortuj", bg="green", fg="black",
                        command=self.start_sort)
        btn.pack(pady=10)

    def start_sort(self):
        # wyłącz przycisk, żeby nie klikać w trakcie
        for w in self.master.winfo_children():
            if isinstance(w, tk.Button):
                w.config(state=tk.DISABLED)
        self.bubble_sort()

    def bubble_sort(self):
        n = len(self.data)
        total_unit = self.width / BAR_COUNT

        for i in range(n):
            for j in range(0, n - i - 1):
                # podświetl aktualny słupek
                self.canvas.itemconfig(self.bars[j],  fill="white", outline="white")
                self.canvas.itemconfig(self.texts[j], fill="white")
                self.canvas.update()
                time.sleep(DELAY)

                if self.data[j] > self.data[j + 1]:
                    # zamiana w liście
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

                    # oblicz nowe współrzędne i wartości
                    for idx in (j, j+1):
                        h = self.data[idx]
                        x0 = idx * total_unit + SPACING/2
                        x1 = x0 + self.bar_width
                        y1 = self.height
                        y0 = y1 - (h / MAX_HEIGHT) * self.height

                        # aktualizuj słupek
                        self.canvas.coords(self.bars[idx], x0, y0, x1, y1)
                        # aktualizuj tekst
                        self.canvas.coords(self.texts[idx], (x0+x1)/2, y0 - 10)
                        self.canvas.itemconfig(self.texts[idx], text=str(h))

                    self.canvas.update()
                    time.sleep(DELAY)

                # przywróć zielony kolor
                self.canvas.itemconfig(self.bars[j],  fill="green", outline="green")
                self.canvas.itemconfig(self.texts[j], fill="white")

        # po zakończeniu włącz przycisk
        for w in self.master.winfo_children():
            if isinstance(w, tk.Button):
                w.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = BubbleSortApp(root)
    root.mainloop()
