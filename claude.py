import pygame
import sys
import time

# Inicjalizacja Pygame
pygame.init()

# Kolory
CZARNY = (0, 0, 0)
ZIELONY = (0, 255, 0)
BIALY = (255, 255, 255)
CIEMNY_ZIELONY = (0, 150, 0)

# Wymiary okna
SZEROKOSC = 800
WYSOKOSC = 600

# Marginesy
MARGINES_GORNY = 50
MARGINES_DOLNY = 100  # Zwiększony margines dolny dla przycisku
MARGINES_BOCZNY = 50


class Przycisk:
    def __init__(self, x, y, szerokosc, wysokosc, tekst, kolor):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.kolor = kolor
        self.kolor_hover = CIEMNY_ZIELONY
        self.tekst = tekst
        self.font = pygame.font.SysFont('Arial', 24)
        self.aktywny = True

    def rysuj(self, ekran):
        if not self.aktywny:
            return

        kolor = self.kolor
        mysz_x, mysz_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mysz_x, mysz_y):
            kolor = self.kolor_hover

        pygame.draw.rect(ekran, kolor, self.rect)
        pygame.draw.rect(ekran, CZARNY, self.rect, 2)  # Obramowanie przycisku

        tekst_surface = self.font.render(self.tekst, True, CZARNY)
        tekst_rect = tekst_surface.get_rect(center=self.rect.center)
        ekran.blit(tekst_surface, tekst_rect)

    def sprawdz_klikniecie(self, mysz_pos):
        if not self.aktywny:
            return False
        return self.rect.collidepoint(mysz_pos)


class WizualizacjaSlupkow:
    def __init__(self, wartosci):
        self.wartosci = wartosci
        self.max_wartosc = max(wartosci)
        self.ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("Wizualizacja słupków")
        self.clock = pygame.time.Clock()

        # Utworzenie przycisku sortowania
        przycisk_x = SZEROKOSC // 2 - 75
        przycisk_y = WYSOKOSC - MARGINES_DOLNY // 2
        self.przycisk_sortuj = Przycisk(przycisk_x, przycisk_y, 150, 40, "Sortuj", ZIELONY)

        # Lista indeksów aktualnie przetwarzanych słupków
        self.aktywne_slupki = []

    def rysuj(self):
        # Czyszczenie ekranu
        self.ekran.fill(CZARNY)

        # Obliczanie szerokości słupka
        szerokosc_slupka = (SZEROKOSC - 2 * MARGINES_BOCZNY) // len(self.wartosci)
        # Zostawiamy trochę odstępu między słupkami
        szerokosc_rysowania = int(szerokosc_slupka * 0.8)

        # Rysowanie słupków
        for i, wartosc in enumerate(self.wartosci):
            # Obliczanie wysokości słupka proporcjonalnie do maksymalnej wartości
            wysokosc_slupka = int((wartosc / self.max_wartosc) * (WYSOKOSC - MARGINES_GORNY - MARGINES_DOLNY))

            # Obliczanie pozycji słupka
            x = MARGINES_BOCZNY + i * szerokosc_slupka
            y = WYSOKOSC - MARGINES_DOLNY - wysokosc_slupka

            # Wybór koloru słupka - biały jeśli aktywny, zielony w przeciwnym przypadku
            kolor = BIALY if i in self.aktywne_slupki else ZIELONY

            # Rysowanie słupka
            pygame.draw.rect(self.ekran, kolor, (x, y, szerokosc_rysowania, wysokosc_slupka))

            # Rysowanie wartości nad słupkiem
            font = pygame.font.SysFont('Arial', 16)
            tekst = font.render(str(wartosc), True, ZIELONY)
            self.ekran.blit(tekst, (x + szerokosc_rysowania // 2 - tekst.get_width() // 2, y - 25))

        # Rysowanie przycisku
        self.przycisk_sortuj.rysuj(self.ekran)

        # Aktualizacja ekranu
        pygame.display.flip()

    def sortuj_babelkowo(self):
        n = len(self.wartosci)
        self.przycisk_sortuj.aktywny = False  # Wyłączenie przycisku podczas sortowania

        for i in range(n):
            for j in range(0, n - i - 1):
                # Zaznaczenie aktualnie porównywanych słupków
                self.aktywne_slupki = [j, j + 1]
                self.rysuj()
                time.sleep(0.01)  # Dłuższa pauza dla lepszej widoczności

                # Porównanie elementów
                if self.wartosci[j] > self.wartosci[j + 1]:
                    # Zamiana elementów miejscami
                    self.wartosci[j], self.wartosci[j + 1] = self.wartosci[j + 1], self.wartosci[j]

                    # Wyświetlenie aktualnego stanu
                    self.rysuj()
                    # time.sleep(0.01)  # Pauza dla lepszej wizualizacji

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()
        self.przycisk_sortuj.aktywny = True  # Ponowne włączenie przycisku

    def uruchom(self):
        running = True
        sortowanie_uruchomione = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not sortowanie_uruchomione and self.przycisk_sortuj.sprawdz_klikniecie(event.pos):
                        sortowanie_uruchomione = True
                        # Uruchomienie sortowania w osobnym wątku
                        import threading
                        watek_sortowania = threading.Thread(target=self.sortuj_babelkowo)
                        watek_sortowania.daemon = True
                        watek_sortowania.start()
                        sortowanie_uruchomione = False

            self.rysuj()
            self.clock.tick(140)

        pygame.quit()
        sys.exit()


# Przykładowe wartości
wartosci = [10, 8, 15, 12, 4, 1, 22, 11, 5, 7, 3, 6, 2, 9, 14, 13, 20, 18, 17, 19]

# Utworzenie i uruchomienie wizualizacji
wizualizacja = WizualizacjaSlupkow(wartosci)
wizualizacja.uruchom()