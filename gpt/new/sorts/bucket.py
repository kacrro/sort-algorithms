from .base import SortAlgorithm
from constants import Config

MAX_HEIGHT = Config.MAX_HEIGHT.value


class BucketSort(SortAlgorithm):
    """Sortowanie kubełkowe."""
    name = "BucketSort"

    def sort(self, data: list[int], visualizer) -> None:
        bucket_count = 10
        buckets: list[list[int]] = [[] for _ in range(bucket_count)]

        # Rozdzielanie do kubełków
        for idx, value in enumerate(data):
            visualizer.highlight(idx, visualizer.highlight_color)
            bucket_index = min(value * bucket_count // (MAX_HEIGHT + 1), bucket_count - 1)
            buckets[bucket_index].append(value)
            visualizer.highlight(idx, visualizer.default_color)

        # Scalanie i wizualizacja
        index = 0
        for bucket in buckets:
            bucket.sort()
            for value in bucket:
                visualizer.highlight(index, visualizer.highlight_color)
                data[index] = value
                visualizer.update_bar(index)
                visualizer.highlight(index, visualizer.default_color)
                index += 1