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

    def rysuj(self, powierzchnia):
        if not self.aktywny:
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
        self.wartosci = wartosci
        self.max_wartosc = max(wartosci)
        self.ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("Wizualizacja słupków")
        self.clock = pygame.time.Clock()

        # Dodajemy bufor do podwójnego buforowania
        self.bufor = pygame.Surface((SZEROKOSC, WYSOKOSC))

        # Utworzenie przycisku sortowania
        przycisk_x = SZEROKOSC // 2 - 75
        przycisk_y = WYSOKOSC - MARGINES_DOLNY // 2
        self.przycisk_sortuj = Przycisk(przycisk_x, przycisk_y, 150, 40, "Sortuj", ZIELONY)

        # Lista indeksów aktualnie przetwarzanych słupków
        self.aktywne_slupki = []

        # Flaga sortowania
        self.sortowanie_aktywne = False

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

        # Rysowanie przycisku na buforze
        self.przycisk_sortuj.rysuj(self.bufor)

        # Przeniesienie całego bufora na ekran (jednorazowa operacja)
        self.ekran.blit(self.bufor, (0, 0))

        # Aktualizacja ekranu
        pygame.display.flip()

    def sortuj_babelkowo(self):
        if self.sortowanie_aktywne:
            return

        self.sortowanie_aktywne = True
        self.przycisk_sortuj.aktywny = False  # Wyłączenie przycisku podczas sortowania

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
                time.sleep(0.02)  # Dłuższa pauza dla lepszej widoczności

                # Porównanie elementów
                if self.wartosci[j] > self.wartosci[j + 1]:
                    # Zamiana elementów miejscami
                    self.wartosci[j], self.wartosci[j + 1] = self.wartosci[j + 1], self.wartosci[j]

                    # Wyświetlenie aktualnego stanu
                    self.rysuj()
                    time.sleep(0.01)  # Pauza dla lepszej wizualizacji

        # Wyczyszczenie aktywnych słupków po zakończeniu sortowania
        self.aktywne_slupki = []
        self.rysuj()

        self.przycisk_sortuj.aktywny = True  # Ponowne włączenie przycisku
        self.sortowanie_aktywne = False

    def uruchom(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.sortowanie_aktywne and self.przycisk_sortuj.sprawdz_klikniecie(event.pos):
                        # Uruchomienie sortowania w osobnym wątku
                        import threading
                        watek_sortowania = threading.Thread(target=self.sortuj_babelkowo)
                        watek_sortowania.daemon = True
                        watek_sortowania.start()

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