# sorting_algorithms.py
"""
Sorting algorithm implementations using generators for step-by-step visualization.
Each algorithm yields control back to allow for animation between steps.
"""

import math


class SortingAlgorithms:
    """
    Collection of sorting algorithms implemented as generators for visualization.
    """

    @staticmethod
    def bubble_sort_generator(values, active_indices_callback):
        """
        Bubble sort algorithm generator.

        Args:
            values (list): List of values to sort
            active_indices_callback (callable): Callback to set active indices for visualization

        Yields:
            None: Control back to caller for animation frame
        """
        n = len(values)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight currently compared elements
                active_indices_callback([j, j + 1])
                yield  # Pause for visualization

                # Compare and swap if necessary
                if values[j] > values[j + 1]:
                    values[j], values[j + 1] = values[j + 1], values[j]
                    yield  # Pause after swap

    @staticmethod
    def merge_sort_generator(values, active_indices_callback):
        """
        Merge sort algorithm generator.

        Args:
            values (list): List of values to sort
            active_indices_callback (callable): Callback to set active indices for visualization

        Yields:
            None: Control back to caller for animation frame
        """
        yield from SortingAlgorithms._merge_sort_recursive(
            values, 0, len(values) - 1, active_indices_callback
        )

    @staticmethod
    def _merge_sort_recursive(values, start, end, active_indices_callback):
        """
        Recursive merge sort implementation.

        Args:
            values (list): List of values to sort
            start (int): Start index of the subarray
            end (int): End index of the subarray
            active_indices_callback (callable): Callback to set active indices

        Yields:
            None: Control back to caller for animation frame
        """
        if start < end:
            mid = (start + end) // 2

            # Recursively sort left and right halves
            yield from SortingAlgorithms._merge_sort_recursive(
                values, start, mid, active_indices_callback
            )
            yield from SortingAlgorithms._merge_sort_recursive(
                values, mid + 1, end, active_indices_callback
            )

            # Merge the sorted halves
            yield from SortingAlgorithms._merge(
                values, start, mid, end, active_indices_callback
            )

    @staticmethod
    def _merge(values, start, mid, end, active_indices_callback):
        """
        Merge two sorted subarrays.

        Args:
            values (list): List of values to sort
            start (int): Start index of the first subarray
            mid (int): End index of the first subarray
            end (int): End index of the second subarray
            active_indices_callback (callable): Callback to set active indices

        Yields:
            None: Control back to caller for animation frame
        """
        # Create copies of the left and right subarrays
        left = values[start:mid + 1]
        right = values[mid + 1:end + 1]

        # Merge the subarrays back into values[start:end+1]
        i, j, k = 0, 0, start

        while i < len(left) and j < len(right):
            # Highlight currently compared elements
            left_idx = start + i
            right_idx = mid + 1 + j
            if left_idx < len(values) and right_idx < len(values):
                active_indices_callback([left_idx, right_idx])
            yield

            if left[i] <= right[j]:
                values[k] = left[i]
                i += 1
            else:
                values[k] = right[j]
                j += 1
            k += 1
            yield

        # Copy remaining elements
        while i < len(left):
            values[k] = left[i]
            i += 1
            k += 1
            yield

        while j < len(right):
            values[k] = right[j]
            j += 1
            k += 1
            yield

    @staticmethod
    def quick_sort_generator(values, active_indices_callback):
        """
        Quick sort algorithm generator.

        Args:
            values (list): List of values to sort
            active_indices_callback (callable): Callback to set active indices for visualization

        Yields:
            None: Control back to caller for animation frame
        """
        yield from SortingAlgorithms._quick_sort_recursive(
            values, 0, len(values) - 1, active_indices_callback
        )

    @staticmethod
    def _quick_sort_recursive(values, low, high, active_indices_callback):
        """
        Recursive quick sort implementation.

        Args:
            values (list): List of values to sort
            low (int): Starting index
            high (int): Ending index
            active_indices_callback (callable): Callback to set active indices

        Yields:
            None: Control back to caller for animation frame
        """
        if low < high:
            # Partition the array and get the pivot index
            pivot_index = yield from SortingAlgorithms._partition(
                values, low, high, active_indices_callback
            )

            # Recursively sort elements before and after partition
            yield from SortingAlgorithms._quick_sort_recursive(
                values, low, pivot_index - 1, active_indices_callback
            )
            yield from SortingAlgorithms._quick_sort_recursive(
                values, pivot_index + 1, high, active_indices_callback
            )

    @staticmethod
    def _partition(values, low, high, active_indices_callback):
        """
        Partition function for quick sort.

        Args:
            values (list): List of values to sort
            low (int): Starting index
            high (int): Ending index (pivot element)
            active_indices_callback (callable): Callback to set active indices

        Yields:
            None: Control back to caller for animation frame

        Returns:
            int: Final position of the pivot element
        """
        pivot = values[high]  # Choose pivot as last element
        i = low - 1  # Index of smaller element

        for j in range(low, high):
            # Highlight currently compared elements
            active_indices_callback([j, high])
            yield

            # If current element is smaller than or equal to pivot
            if values[j] <= pivot:
                i += 1
                values[i], values[j] = values[j], values[i]

                # Show the swap
                active_indices_callback([i, j])
                yield

        # Place pivot in correct position
        values[i + 1], values[high] = values[high], values[i + 1]

        # Show the final pivot placement
        active_indices_callback([i + 1, high])
        yield

        return i + 1

    @staticmethod
    def bucket_sort_generator(values, active_indices_callback):
        """
        Bucket sort algorithm generator.

        Args:
            values (list): List of values to sort
            active_indices_callback (callable): Callback to set active indices for visualization

        Yields:
            None: Control back to caller for animation frame
        """
        n = len(values)
        max_val = max(values)

        # Create buckets
        num_buckets = min(n, 5)  # Adjustable number of buckets
        buckets = [[] for _ in range(num_buckets)]

        # Distribute elements into buckets
        for i in range(n):
            # Highlight current element
            active_indices_callback([i])
            yield

            # Calculate bucket index
            bucket_idx = min(
                math.floor((values[i] / max_val) * (num_buckets - 1)),
                num_buckets - 1
            )
            buckets[bucket_idx].append(values[i])
            yield

        # Sort buckets and merge them back
        k = 0
        for i in range(num_buckets):
            # Sort each bucket
            buckets[i].sort()

            # Move sorted elements back to original array
            for j in range(len(buckets[i])):
                values[k] = buckets[i][j]

                # Highlight current element
                active_indices_callback([k])
                yield

                k += 1
