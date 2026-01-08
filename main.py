from ant import Ant
from PIL import Image
import os
import random

PINK_COLOR = (255, 20, 147)


class Configuration:
    def __init__(self):
        '''
        Konstruktor klasy Configuration
        Zawiera niezbędnę dla symulacji atrybuty
        '''
        self.window_height = 0
        self.window_width = 0
        self.chance_black = 0
        self.steps = 0
        self.image_sel = False
        self.users_image = None
        self.result_folder = "result"
        self.background = None
        self.ant = None
        self.pixels_access = None

    def random_black_change(self):
        '''
        Zamienia kolor pikseli na czarny na obrazie
        w zależności od podanego przez użytkownika
        prawdopodobieństwa wystąpienia czarnego
        '''
        if self.chance_black > 0:
            for x in range(self.window_width):
                for y in range(self.window_height):
                    if random.randint(0, 100) < self.chance_black:
                        self.pixels_access[x, y] = (0, 0, 0)

    def console_information(self):
        '''
        Metoda dla wypisywania komunikatów,pobrania ścieżki obrazu,
        liczby kroków,wymiarów planszy,prawdopodobieństwa czarnych pól
        '''
        print("---KONFIGURACJA MRÓWKI LANGTONA---")
        print("Wybierz tryb: ")
        print("1 - Białe tło")
        print("2 - Własny czarno-biały obraz")
        print("3 - Losowo wygenerowany czarno-biały obraz")
        mode = int(input("Twój wybór (1-3): "))
        if self.check_int(mode, 'mode'):
            if mode == 2:
                path = input("Podaj ścieżkę do obrazka: ")
                if os.path.exists(path):
                    self.image_sel = True
                    self.users_image, self.window_width, self.window_height \
                        = self.load_and_process_image(path)
            else:
                self.window_width = int(input("Podaj szerokość planszy: "))
                self.window_height = int(input("Podaj wysokość planszy: "))
                if self.check_int(self.window_width) \
                        and self.check_int(self.window_height):
                    if mode == 3:
                        chance = int(input("Podaj czarnych pól: "))
                        if self.check_int(chance, 'chance'):
                            self.chance_black = chance
                else:
                    raise ValueError('Podana wartość nie jest poprawna')
        else:
            raise ValueError('Podana wartość nie jest poprawna')
        steps = int(input("Podaj liczbę kroków symulacji: "))
        if self.check_int(steps):
            self.steps = steps
        else:
            raise ValueError('Podana wartość nie jest poprawna')

    def check_int(self, input, which_value='standard_int'):
        '''
        Sprawdza liczbę, podaną przez użytkownika,zgodnie z wymaganiami
        '''
        if which_value == 'mode':
            return input in [1, 2, 3]
        elif which_value == 'chance':
            return 0 <= input <= 100
        return input > 1

    def load_and_process_image(self, path):
        """
        Wczytuje obraz, przetwarza go na format czarno-biały
        i zwraca obiekt obrazu oraz jego wymiary.
        """
        try:
            img = Image.open(path).convert('RGB')
            img = img.convert('1').convert('RGB')
            width, height = img.size
            return img, width, height
        except FileNotFoundError:
            print("Nie znaleziono pliku")
        except Exception:
            print("Plik jest uszkodzony")

    def ant_cycle(self):
        self.ant.rotation()
        self.ant.inverse_pixel()
        self.ant.next_step()

    def start(self):
        '''
        Główna pętla symulacji
        '''
        if os.path.exists(self.result_folder):
            os.system(f'rm -rf "{self.result_folder}"')
        os.makedirs(self.result_folder)
        if self.image_sel and self.users_image:
            self.background = self.users_image
        else:
            size = (self.window_width, self.window_height)
            self.background = Image.new('RGB', size, 'white')
        self.pixels_access = self.background.load()
        self.ant = Ant(self.background, self.window_width, self.window_height)
        self.random_black_change()
        # zapisuje pocztkową pozycję mrówki na planszy jako krok_0.png
        save = self.background.copy()
        save.putpixel((self.ant.current_x, self.ant.current_y), PINK_COLOR)
        save.save(os.path.join(self.result_folder, 'krok_0.png'))
        print(f"Rozpoczynam symulację na {self.steps} kroków.")
        print(f"Obrazy będą w folderze: {os.path.abspath(self.result_folder)}")
        for step in range(self.steps):
            self.ant_cycle()
            ax, ay = self.ant.current_x, self.ant.current_y
            real_color_under_ant = self.pixels_access[ax, ay]
            self.pixels_access[ax, ay] = PINK_COLOR
            filename = f"krok_{step+1}.png"
            path = os.path.join(self.result_folder, filename)
            self.background.save(path)
            self.pixels_access[ax, ay] = real_color_under_ant
        print("Zakończono.")


if __name__ == '__main__':
    sim = Configuration()
    sim.console_information()
    sim.start()
