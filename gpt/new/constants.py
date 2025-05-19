# Stałe konfiguracyjne aplikacji
from enum import Enum

class Config(Enum):
    BAR_COUNT = 50       # liczba słupków
    MAX_HEIGHT = 100     # maksymalna wysokość słupka
    DELAY = 0.02         # opóźnienie w sekundach
    SPACING = 2          # odstęp między słupkami w pikselach