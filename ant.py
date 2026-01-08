from PIL import Image
import random


class Ant:
    '''
    Klasa reprezentująca logikę mrówki.
    '''
    def __init__(self, pillow_image: Image, window_width, window_height):
        '''
        Konstrukor klasy.
        Pobiera od uzytkownika obraz, szerokość i wysokość okna.
        '''
        self.pillow_img = pillow_image
        self.window_width = window_width
        self.window_height = window_height
        self.pixels = pillow_image.load()
        self.current_x = window_width // 2
        self.current_y = window_height // 2
        self.directions = ['Up', 'Right', 'Down', 'Left']
        self.direction = 'Up'

    def inverse_pixel(self):
        '''
        Zmiana koloru piksela na przeciwny.
        '''
        current_color = self.pixels[self.current_x, self.current_y]
        if current_color == (0, 0, 0):
            self.pixels[self.current_x, self.current_y] = (255, 255, 255)
        else:
            self.pixels[self.current_x, self.current_y] = (0, 0, 0)

    def rotation(self):
        '''
        Obrót mrówki zależnie od koloru pola.
        '''
        dir_index = self.directions.index(self.direction)
        current_color = self.pixels[self.current_x, self.current_y]
        if current_color == (255, 255, 255):
            if self.direction == 'Up':
                self.direction = self.directions[3]
            else:
                self.direction = self.directions[dir_index - 1]
        else:
            if self.direction == 'Left':
                self.direction = self.directions[0]
            else:
                self.direction = self.directions[dir_index + 1]

    def verify_position(self, x, y):
        '''
        Sprawdza,czy x i y są na planszy.
        '''
        return 0 <= x < self.window_width and 0 <= y < self.window_height

    def random_movement(self):
        '''
        Popełnia randomowy ruch ze wszystkich możliwych
        '''
        valid_movements = []
        possible_direct = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for x, y in possible_direct:
            new_x = self.current_x + x
            new_y = self.current_y + y
            if self.verify_position(new_x, new_y):
                valid_movements.append((new_x, new_y))
        self.current_x, self.current_y = random.choice(valid_movements)

    def next_step(self):
        '''
        Popełnia następny krok
        '''
        current_dir = self.direction
        x, y = 0, 0
        if current_dir == "Up":
            y = 1
        elif current_dir == "Down":
            y = -1
        elif current_dir == "Left":
            x = -1
        elif current_dir == "Right":
            x = 1
        new_x = self.current_x + x
        new_y = self.current_y + y
        if self.verify_position(new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
        else:
            self.random_movement()
