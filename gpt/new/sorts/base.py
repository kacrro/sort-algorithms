from abc import ABC, abstractmethod


class SortAlgorithm(ABC):
    """Interfejs dla algorytmów sortowania."""
    name: str

    @abstractmethod
    def sort(self, data: list[int], visualizer) -> None:
        """
        Sortuje dane, korzystając z metod visualizera do aktualizacji widoku.
        """
        pass