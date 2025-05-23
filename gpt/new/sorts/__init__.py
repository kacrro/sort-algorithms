"""Pakiet zawierający implementacje algorytmów sortowania."""

from .bubble import BubbleSort
from .merge import MergeSort
from .quick import QuickSort
from .bucket import BucketSort

__all__ = ['BubbleSort', 'MergeSort', 'QuickSort', 'BucketSort']