from .base import SortAlgorithm


class BubbleSort(SortAlgorithm):
    """Sortowanie bąbelkowe."""
    name = "BubbleSort"

    def sort(self, data: list[int], visualizer) -> None:
        n = len(data)
        for i in range(n):
            for j in range(n - i - 1):
                visualizer.highlight(j, visualizer.highlight_color)
                if data[j] > data[j + 1]:
                    visualizer.swap_bars(j, j + 1)
                visualizer.highlight(j, visualizer.default_color)