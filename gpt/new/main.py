import tkinter as tk
from visualizer import SortVisualizer


def main():
    root = tk.Tk()
    app = SortVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()