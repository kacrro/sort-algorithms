from .base import SortAlgorithm


class MergeSort(SortAlgorithm):
    """Sortowanie przez scalanie."""
    name = "MergeSort"

    def sort(self, data: list[int], visualizer) -> None:
        self._merge_sort(data, 0, len(data), visualizer)

    def _merge_sort(self, data, left: int, right: int, visualizer) -> None:
        if right - left > 1:
            mid = (left + right) // 2
            self._merge_sort(data, left, mid, visualizer)
            self._merge_sort(data, mid, right, visualizer)

            left_part = data[left:mid]
            right_part = data[mid:right]
            i = j = 0

            for k in range(left, right):
                visualizer.highlight(k, visualizer.highlight_color)
                if j >= len(right_part) or (i < len(left_part) and left_part[i] <= right_part[j]):
                    data[k] = left_part[i]
                    i += 1
                else:
                    data[k] = right_part[j]
                    j += 1
                visualizer.update_bar(k)
                visualizer.highlight(k, visualizer.default_color)