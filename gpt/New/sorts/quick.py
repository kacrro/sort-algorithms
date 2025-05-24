from .base import SortAlgorithm


class QuickSort(SortAlgorithm):
    """Sortowanie szybkie."""
    name = "QuickSort"

    def sort(self, data: list[int], visualizer) -> None:
        self._quick_sort(data, 0, len(data) - 1, visualizer)

    def _quick_sort(self, data, low: int, high: int, visualizer) -> None:
        if low < high:
            pivot_index = self._partition(data, low, high, visualizer)
            self._quick_sort(data, low, pivot_index - 1, visualizer)
            self._quick_sort(data, pivot_index + 1, high, visualizer)

    def _partition(self, data, low: int, high: int, visualizer) -> int:
        pivot = data[high]
        visualizer.highlight(high, visualizer.highlight_color)
        i = low
        for j in range(low, high):
            visualizer.highlight(j, visualizer.highlight_color)
            if data[j] < pivot:
                visualizer.swap_bars(i, j)
                i += 1
            visualizer.highlight(j, visualizer.default_color)
        visualizer.swap_bars(i, high)
        visualizer.highlight(high, visualizer.default_color)
        return i