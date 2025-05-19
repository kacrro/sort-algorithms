import tkinter as tk
import random
import time

BAR_COUNT = 50
MAX_HEIGHT = 100
DELAY = 0.02   # sekundy
SPACING = 2   # px odstępu między słupkami

class SortVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Sort Visualizer")
        self.width = 800
        self.height = 400

        # Canvas
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # generate data
        self.data = [random.randint(1, MAX_HEIGHT) for _ in range(BAR_COUNT)]
        total_unit = self.width / BAR_COUNT
        self.bar_width = total_unit - SPACING

        # Draw bars + texts
        self.bars, self.texts = [], []
        for i, h in enumerate(self.data):
            x0 = i * total_unit + SPACING/2
            x1 = x0 + self.bar_width
            y1 = self.height
            y0 = y1 - (h / MAX_HEIGHT) * self.height

            bar = self.canvas.create_rectangle(x0, y0, x1, y1,
                                               fill="green", outline="green")
            txt = self.canvas.create_text((x0+x1)/2, y0 - 10,
                                          text=str(h), fill="white", font=("Arial", 8))
            self.bars.append(bar)
            self.texts.append(txt)

        # Buttons
        frame = tk.Frame(master, bg="black")
        frame.pack(pady=10)
        for name, cmd in [("BubbleSort", self.start_bubble),
                          ("MergeSort",  self.start_merge),
                          ("QuickSort",  self.start_quick),
                          ("BucketSort", self.start_bucket)]:
            btn = tk.Button(frame, text=name, bg="green", fg="black",
                            command=cmd, width=10)
            btn.pack(side=tk.LEFT, padx=5)

    def disable_buttons(self):
        for w in self.master.winfo_children():
            if isinstance(w, tk.Frame):
                for btn in w.winfo_children():
                    btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        for w in self.master.winfo_children():
            if isinstance(w, tk.Frame):
                for btn in w.winfo_children():
                    btn.config(state=tk.NORMAL)

    def highlight(self, idx, color):
        self.canvas.itemconfig(self.bars[idx],  fill=color, outline=color)
        self.canvas.itemconfig(self.texts[idx], fill=color)
        self.canvas.update()
        time.sleep(DELAY)

    def swap_bars(self, i, j):
        # swap data
        self.data[i], self.data[j] = self.data[j], self.data[i]
        total = self.width / BAR_COUNT
        for idx in (i, j):
            h = self.data[idx]
            x0 = idx * total + SPACING/2
            x1 = x0 + self.bar_width
            y1 = self.height
            y0 = y1 - (h / MAX_HEIGHT) * self.height
            self.canvas.coords(self.bars[idx], x0, y0, x1, y1)
            self.canvas.coords(self.texts[idx], (x0+x1)/2, y0 - 10)
            self.canvas.itemconfig(self.texts[idx], text=str(h))
        self.canvas.update()
        time.sleep(DELAY)

    # --- BubbleSort ---
    def start_bubble(self):
        self.disable_buttons()
        self.bubble_sort()
        self.enable_buttons()

    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(n - i - 1):
                self.highlight(j, "white")
                if self.data[j] > self.data[j+1]:
                    self.swap_bars(j, j+1)
                self.highlight(j, "green")

    # --- MergeSort ---
    def start_merge(self):
        self.disable_buttons()
        self.merge_sort(0, len(self.data))
        self.enable_buttons()

    def merge_sort(self, l, r):
        if r - l > 1:
            m = (l + r) // 2
            self.merge_sort(l, m)
            self.merge_sort(m, r)
            # merge
            left = self.data[l:m]
            right = self.data[m:r]
            i = j = 0
            for k in range(l, r):
                # highlight position k
                self.highlight(k, "white")
                if j >= len(right) or (i < len(left) and left[i] <= right[j]):
                    self.data[k] = left[i]; i += 1
                else:
                    self.data[k] = right[j]; j += 1
                # update bar k
                h = self.data[k]
                total = self.width / BAR_COUNT
                x0 = k * total + SPACING/2
                x1 = x0 + self.bar_width
                y1 = self.height
                y0 = y1 - (h / MAX_HEIGHT) * self.height
                self.canvas.coords(self.bars[k], x0, y0, x1, y1)
                self.canvas.coords(self.texts[k], (x0+x1)/2, y0 - 10)
                self.canvas.itemconfig(self.texts[k], text=str(h))
                self.canvas.update()
                time.sleep(DELAY)
                self.highlight(k, "green")

    # --- QuickSort ---
    def start_quick(self):
        self.disable_buttons()
        self.quick_sort(0, len(self.data)-1)
        self.enable_buttons()

    def quick_sort(self, low, high):
        if low < high:
            p = self.partition(low, high)
            self.quick_sort(low, p-1)
            self.quick_sort(p+1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        self.highlight(high, "white")
        i = low
        for j in range(low, high):
            self.highlight(j, "white")
            if self.data[j] < pivot:
                self.swap_bars(i, j)
                i += 1
            self.highlight(j, "green")
        self.swap_bars(i, high)
        self.highlight(high, "green")
        return i

    # --- BucketSort ---
    def start_bucket(self):
        self.disable_buttons()
        self.bucket_sort()
        self.enable_buttons()

    def bucket_sort(self):
        # create buckets
        bucket_count = 10
        buckets = [[] for _ in range(bucket_count)]
        for idx, v in enumerate(self.data):
            self.highlight(idx, "white")
            b = min(v * bucket_count // (MAX_HEIGHT+1), bucket_count-1)
            buckets[b].append(v)
            self.highlight(idx, "green")
        # sort each bucket and rebuild
        k = 0
        for b in buckets:
            b.sort()
            for v in b:
                # highlight position k
                self.highlight(k, "white")
                self.data[k] = v
                # update bar k
                total = self.width / BAR_COUNT
                x0 = k * total + SPACING/2
                x1 = x0 + self.bar_width
                y1 = self.height
                y0 = y1 - (v / MAX_HEIGHT) * self.height
                self.canvas.coords(self.bars[k], x0, y0, x1, y1)
                self.canvas.coords(self.texts[k], (x0+x1)/2, y0 - 10)
                self.canvas.itemconfig(self.texts[k], text=str(v))
                self.canvas.update()
                time.sleep(DELAY)
                self.highlight(k, "green")
                k += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SortVisualizer(root)
    root.mainloop()
