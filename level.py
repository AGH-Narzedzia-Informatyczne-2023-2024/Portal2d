import pygame
from typing import List, Type, Tuple

import simulation


class building_block:
    def __init__(self, position: Tuple):
        self.table_position = position
        self.position = (100 * self.table_position[0], 100 * self.table_position[1])
        self.rect = pygame.Rect(self.position[0], self.position[1], 100, 100)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, (0, 255, 0), self.rect)

    def blit(self, screen):
        width, height = pygame.display.get_surface().get_size()
        offset_x = 0
        offset_y = 0
        if width / 13 > height / 9:
            scale = height / simulation.variables.screen_size[1]
            offset_x = abs((simulation.variables.screen_size[0] * scale - width) / 2)
        else:
            scale = width / simulation.variables.screen_size[0]
            offset_y = abs((simulation.variables.screen_size[1] * scale - height) / 2)
        square_side = int(100 * scale)
        pygame.draw.rect(screen, (0, 200, 0), (offset_x + self.table_position[0] * square_side, offset_y + self.table_position[1] * square_side, square_side, square_side))


class basic_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, (0, 255, 0), self.rect)

class spike_block(building_block):

    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, (200, 0, 0), self.rect)

class door_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, (0, 0, 200), self.rect)


class level:
    '''level layout is 9x13, every block is a class itself'''

    layout_rects = []

    layout = []

    @staticmethod
    def load_level():
        try:
            with open("assets/levels", "r") as level_file:
                line = level_file.read()
                print(line)
        except FileNotFoundError:
            print("Failed to load a level.")

    @staticmethod
    def create_level():
        for i in range(13):
            temp = []
            for j in range(9):
                if i == 0 or i == 12 or j == 0 or j == 8:
                    block = basic_block((i, j))
                    temp.append(block)
                    level.layout_rects.append(block)
                else:
                    temp.append(None)
            level.layout.append(temp)
