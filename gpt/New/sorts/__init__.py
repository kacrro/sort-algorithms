"""Pakiet zawierający implementacje algorytmów sortowania."""

from .bubble import BubbleSort
from .bucket import BucketSort
from .merge import MergeSort
from .quick import QuickSort

__all__ = ['BubbleSort', 'MergeSort', 'QuickSort', 'BucketSort']