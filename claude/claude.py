import pygame
import sys
import time
import math
import copy

# Inicjalizacja Pygame
pygame.init()

# Kolory
CZARNY = (0, 0, 0)
ZIELONY = (0, 255, 0)
BIALY = (255, 255, 255)
CIEMNY_ZIELONY = (0, 150, 0)
NIEBIESKI = (0, 100, 255)
CZERWONY = (255, 50, 50)
FIOLETOWY = (200, 50, 200)

# Wymiary okna
SZEROKOSC = 800
WYSOKOSC = 600

# Marginesy
MARGINES_GORNY = 50
MARGINES_DOLNY = 100  # Zwiększony margines dolny dla przycisków
MARGINES_BOCZNY = 50


class Przycisk:
    def __init__(self, x, y, szerokosc, wysokosc, tekst, kolor):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.kolor = kolor
        self.kolor_hover = (
        max(0, kolor[0] - 50), max(0, kolor[1] - 50), max(0, kolor[2] - 50))  # Ciemniejsza wersja koloru
        self.tekst = tekst
        self.font = pygame.font.SysFont('Arial', 18)  # Mniejsza czcionka dla mniejszych przycisków
        self.aktywny = True

    def rysuj(self, powierzchnia):
        if not self.aktywny:
            # Rysuj przycisk jako nieaktywny (szary)
            kolor = (100, 100, 100)
            pygame.draw.rect(powierzchnia, kolor, self.rect)
            pygame.draw.rect(powierzchnia, CZARNY, self.rect, 2)  # Obramowanie przycisku

            tekst_surface = self.font.render(self.tekst, True, CZARNY)
            tekst_rect = tekst_surface.get_rect(center=self.rect.center)
            powierzchnia.blit(tekst_surface, tekst_rect)
            return

        kolor = self.kolor
        mysz_x, mysz_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mysz_x, mysz_y):
            kolor = self.kolor_hover

        pygame.draw.rect(powierzchnia, kolor, self.rect)
        pygame.draw.rect(powierzchnia, CZARNY, self.rect, 2)  # Obramowanie przycisku

        tekst_surface = self.font.render(self.tekst, True, CZARNY)
        tekst_rect = tekst_surface.get_rect(center=self.rect.center)
        powierzchnia.blit(tekst_surface, tekst_rect)

    def sprawdz_klikniecie(self, mysz_pos):
        if not self.aktywny:
            return False
        return self.rect.collidepoint(mysz_pos)


class WizualizacjaSlupkow:
    def __init__(self, wartosci):
        self.wartosci_oryginalne = copy.deepcopy(wartosci)  # Zapisujemy oryginalne wartości
        self.wartosci = copy.deepcopy(wartosci)
        self.max_wartosc = max(wartosci)
        self.ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("Wizualizacja algorytmów sortowania")
        self.clock = pygame.time.Clock()

        # Dodajemy bufor do podwójnego buforowania
        self.bufor = pygame.Surface((SZEROKOSC, WYSOKOSC))

        # Utworzenie przycisków sortowania
        self.przyciski = []
        szerokosc_przycisku = 150
        odstep_przycisku = 10
        poczatek_x = (SZEROKOSC - (4 * szerokosc_przycisku + 3 * odstep_przycisku)) // 2
        przycisk_y = WYSOKOSC - MARGINES_DOLNY // 2

        # Przyciski dla różnych algorytmów sortowania
        self.przycisk_bubblesort = Przycisk(poczatek_x, przycisk_y, szerokosc_przycisku, 40, "BubbleSort", ZIELONY)
        self.przyciski.append(self.przycisk_bubblesort)

        self.przycisk_mergesort = Przycisk(poczatek_x + szerokosc_przycisku + odstep_przycisku, przycisk_y,
                                           szerokosc_przycisku, 40, "MergeSort", NIEBIESKI)
        self.przyciski.append(self.przycisk_mergesort)

        self.przycisk_quicksort = Przycisk(poczatek_x + 2 * (szerokosc_przycisku + odstep_przycisku), przycisk_y,
                                           szerokosc_przycisku, 40, "QuickSort", CZERWONY)
        self.przyciski.append(self.przycisk_quicksort)

        self.przycisk_bucketsort = Przycisk(poczatek_x + 3 * (szerokosc_przycisku + odstep_przycisku), przycisk_y,
                                            szerokosc_przycisku, 40, "BucketSort", FIOLETOWY)
        self.przyciski.append(self.przycisk_bucketsort)

        # Przycisk resetowania
        self.przycisk_reset = Przycisk(SZEROKOSC - 100, 10, 80, 30, "Reset", (220, 220, 220))

        # Lista indeksów aktualnie przetwarzanych słupków
        self.aktywne_slupki = []

        # Flaga sortowania
        self.sortowanie_aktywne = False

    def resetuj_wartosci(self):
        self.wartosci = copy.deepcopy(self.wartosci_oryginalne)
        self.aktywne_slupki = []
        self.rysuj()

    def rysuj(self):
        # Czyszczenie bufora (zamiast bezpośrednio ekranu)
        self.bufor.fill(CZARNY)

        # Obliczanie szerokości słupka
        szerokosc_slupka = (SZEROKOSC - 2 * MARGINES_BOCZNY) // len(self.wartosci)
        # Zostawiamy trochę odstępu między słupkami
        szerokosc_rysowania = int(szerokosc_slupka * 0.8)

        # Rysowanie słupków na buforze
        for i, wartosc in enumerate(self.wartosci):
            # Obliczanie wysokości słupka proporcjonalnie do maksymalnej wartości
            wysokosc_slupka = int((wartosc / self.max_wartosc) * (WYSOKOSC - MARGINES_GORNY - MARGINES_DOLNY))

            # Obliczanie pozycji słupka
            x = MARGINES_BOCZNY + i * szerokosc_slupka
            y = WYSOKOSC - MARGINES_DOLNY - wysokosc_slupka

            # Wybór koloru słupka - biały jeśli aktywny, zielony w przeciwnym przypadku
            kolor = BIALY if i in self.aktywne_slupki else ZIELONY

            # Rysowanie słupka na buforze
            pygame.draw.rect(self.bufor, kolor, (x, y, szerokosc_rysowania, wysokosc_slupka))

            # Rysowanie wartości nad słupkiem
            font = pygame.font.SysFont('Arial', 16)
            tekst = font.render(str(wartosc), True, ZIELONY)
            self.bufor.blit(tekst, (x + szerokosc_rysowania // 2 - tekst.get_width() // 2, y - 25))

        # Rysowanie przycisków na buforze
        for przycisk in self.przyciski:
            przycisk.rysuj(self.bufor)

        # Rysowanie przycisku reset
        self.przycisk_reset.rysuj(self.bufor)

        # Przeniesienie całego bufora na ekran (jednorazowa operacja)
        self.ekran.blit(self.bufor, (0, 0))

        # Aktualizacja ekranu
        pygame.display.flip()

    def ustaw_nieaktywne_przyciski(self, aktywny=False):
        for przycisk in self.przyciski:
            przycisk.aktywny = aktywny

    def sortuj_babelkowo(self):
        if self.sortowanie_aktywne:
            return

        self.sortowanie_aktywne = True
        self.ustaw_nieaktywne_przyciski(False)

        n = len(self.wartosci)

        for i in range(n):
            for j in range(0, n - i - 1):
                # Sprawdzenie, czy aplikacja nie została zamknięta
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Zaznaczenie aktualnie porównywanych słupków
                self.aktywne_slupki = [j, j + 1]
                self.rysuj()
                #time.sleep(0.02)

                # Porównanie elementów
                if self.wartosci[j] > self.wartosci[j + 1]:
                    # Zamiana elementów miejscami
                    self.wartosci[j], self.wartosci[j + 1] = self.wartosci[j + 1], self.wartosci[j]

                    # Wyświetlenie aktualnego stanu
                    self.rysuj()
                    #time.sleep(0.01)

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()

        self.ustaw_nieaktywne_przyciski(True)
        self.sortowanie_aktywne = False

    def merge_sort(self, arr, start, end):
        if self.sortowanie_aktywne and start < end:
            mid = (start + end) // 2

            # Rekurencyjne sortowanie lewej i prawej połówki
            self.merge_sort(arr, start, mid)
            self.merge_sort(arr, mid + 1, end)

            # Scalanie posortowanych połówek
            self.merge(arr, start, mid, end)

    def merge(self, arr, start, mid, end):
        # Tworzenie kopii lewej i prawej połówki
        L = arr[start:mid + 1]
        R = arr[mid + 1:end + 1]

        # Indeksy dla przechodzenia po lewej i prawej połówce
        i, j, k = 0, 0, start

        while i < len(L) and j < len(R):
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Zaznaczenie aktualnie porównywanych elementów
            self.aktywne_slupki = [start + i, mid + 1 + j]
            self.rysuj()
            #time.sleep(0.2)

            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

            # Wyświetlenie aktualnego stanu
            self.rysuj()
            #time.sleep(0.1)

        # Kopiowanie pozostałych elementów z L lub R
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            self.rysuj()
            #time.sleep(0.1)

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            self.rysuj()
            #time.sleep(0.1)

    def sortuj_mergesort(self):
        if self.sortowanie_aktywne:
            return

        self.sortowanie_aktywne = True
        self.ustaw_nieaktywne_przyciski(False)

        # Wywołanie merge sort
        self.merge_sort(self.wartosci, 0, len(self.wartosci) - 1)

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()

        self.ustaw_nieaktywne_przyciski(True)
        self.sortowanie_aktywne = False

    def partition(self, arr, low, high):
        pivot = arr[high]  # Wybieramy pivot jako ostatni element
        i = low - 1  # Indeks mniejszego elementu

        for j in range(low, high):
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Zaznaczenie aktualnie porównywanych elementów
            self.aktywne_slupki = [j, high]  # j i pivot
            self.rysuj()
            #time.sleep(0.2)

            # Jeśli bieżący element jest mniejszy lub równy pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

                # Wyświetlenie aktualnego stanu po zamianie
                self.aktywne_slupki = [i, j]
                self.rysuj()
                #time.sleep(0.1)

        # Zamiana pivota z elementem na pozycji i+1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        # Wyświetlenie aktualnego stanu po zamianie pivota
        self.aktywne_slupki = [i + 1, high]
        self.rysuj()
        #time.sleep(0.1)

        return i + 1

    def quick_sort(self, arr, low, high):
        if self.sortowanie_aktywne and low < high:
            # Znajdź indeks podziału
            pi = self.partition(arr, low, high)

            # Rekurencyjne sortowanie elementów przed i po podziale
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)

    def sortuj_quicksort(self):
        if self.sortowanie_aktywne:
            return

        self.sortowanie_aktywne = True
        self.ustaw_nieaktywne_przyciski(False)

        # Wywołanie quick sort
        self.quick_sort(self.wartosci, 0, len(self.wartosci) - 1)

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()

        self.ustaw_nieaktywne_przyciski(True)
        self.sortowanie_aktywne = False

    def sortuj_bucketsort(self):
        if self.sortowanie_aktywne:
            return

        self.sortowanie_aktywne = True
        self.ustaw_nieaktywne_przyciski(False)

        # Implementacja bucket sort
        # Bucket sort wymaga znormalizowanych wartości do poprawnego działania
        n = len(self.wartosci)
        max_val = max(self.wartosci)

        # Tworzymy kubełki (liczba kubełków może być różna)
        num_buckets = min(n, 5)  # Można dostosować liczbę kubełków
        buckets = [[] for _ in range(num_buckets)]

        # Umieszczamy elementy w kubełkach
        for i in range(n):
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Zaznaczenie aktualnego elementu
            self.aktywne_slupki = [i]
            self.rysuj()
            #time.sleep(0.2)

            # Oblicz indeks kubełka
            idx = math.floor((self.wartosci[i] / max_val) * (num_buckets - 1))
            buckets[idx].append(self.wartosci[i])

            # Wyświetlenie aktualnego stanu
            self.rysuj()
            #time.sleep(0.1)

        # Sortujemy kubełki i łączymy je
        k = 0
        for i in range(num_buckets):
            # Sortujemy każdy kubełek
            buckets[i].sort()

            # Przenosimy posortowane elementy z kubełka z powrotem do oryginalnej tablicy
            for j in range(len(buckets[i])):
                self.wartosci[k] = buckets[i][j]

                # Zaznaczenie aktualnego elementu
                self.aktywne_slupki = [k]
                self.rysuj()
                #time.sleep(0.1)

                k += 1

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()

        self.ustaw_nieaktywne_przyciski(True)
        self.sortowanie_aktywne = False

    def uruchom(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Sprawdzenie kliknięć przycisków
                    if not self.sortowanie_aktywne:
                        if self.przycisk_bubblesort.sprawdz_klikniecie(event.pos):
                            import threading
                            watek_sortowania = threading.Thread(target=self.sortuj_babelkowo)
                            watek_sortowania.daemon = True
                            watek_sortowania.start()
                        elif self.przycisk_mergesort.sprawdz_klikniecie(event.pos):
                            import threading
                            watek_sortowania = threading.Thread(target=self.sortuj_mergesort)
                            watek_sortowania.daemon = True
                            watek_sortowania.start()
                        elif self.przycisk_quicksort.sprawdz_klikniecie(event.pos):
                            import threading
                            watek_sortowania = threading.Thread(target=self.sortuj_quicksort)
                            watek_sortowania.daemon = True
                            watek_sortowania.start()
                        elif self.przycisk_bucketsort.sprawdz_klikniecie(event.pos):
                            import threading
                            watek_sortowania = threading.Thread(target=self.sortuj_bucketsort)
                            watek_sortowania.daemon = True
                            watek_sortowania.start()

                    # Przycisk resetowania - działa nawet podczas sortowania
                    if self.przycisk_reset.sprawdz_klikniecie(event.pos):
                        self.resetuj_wartosci()
                        self.sortowanie_aktywne = False
                        self.ustaw_nieaktywne_przyciski(True)

            # Rysowanie tylko gdy potrzebne
            if not self.sortowanie_aktywne:
                self.rysuj()

            self.clock.tick(30)  # Zmniejszenie FPS dla lepszej wydajności

        pygame.quit()
        sys.exit()


# Przykładowe wartości
wartosci = [10, 8, 15, 12, 4, 1, 22, 18, 5, 7, 3, 6, 14, 11, 9, 2, 13, 20, 19, 17, 16]

# Utworzenie i uruchomienie wizualizacji
wizualizacja = WizualizacjaSlupkow(wartosci)
wizualizacja.uruchom()