import json

import pygame
from typing import List, Type, Tuple

import player
import simulation


class building_block(simulation.GameObjects):
    def __init__(self, position: Tuple, isEntity: bool = False) -> object:
        super().__init__(isEntity)
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
        self.position = (
        offset_x + self.table_position[0] * square_side, offset_y + self.table_position[1] * square_side)
        try:
            self.image = pygame.transform.scale(self.image_og, (square_side, square_side))
            screen.blit(self.image, self.position)
        except:
            # printf("failed to load")
            pygame.draw.rect(screen, (0, 200, 0), (self.position[0], self.position[1], square_side, square_side))


class block_entity(building_block):
    def __init__(self, position: Tuple):
        super().__init__(position, True)

    def update(self):
        pass


class basic_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image_og = pygame.image.load("assets/images/basic_block.png").convert()
        self.image = pygame.transform.scale(self.image_og, (100, 100))


class spike_block(building_block):

    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image_og = pygame.image.load("assets/images/spike_block.png").convert()
        self.image = pygame.transform.scale(self.image_og, (100, 100))


class door_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)


class level:
    '''level layout is 9x13, every block is a class itself'''

    layout_rects = []  # pure list [block, block, block, block]

    layout = []  # list of list [[block, block]

    #              [block, block]]

    @staticmethod
    def load_level():
        try:
            with open("assets/levels", "r") as level_file:
                level.layout_rects = []
                for i in range(13):
                    for j in range(9):
                        level.layout[i][j] = None
                for gameElement in simulation.gameObjects:
                    if gameElement.__class__.__name__ != player.player.__name__:
                        simulation.gameObjects.remove(gameElement)
                for line in level_file.readlines():
                    line = line.split("; ")
                    line[1] = line[1].replace("(", "")
                    line[1] = line[1].replace(")", "")
                    position = line[1].split(", ")
                    position = (int(position[0]), int(position[1]))
                    for block_class in building_block.__subclasses__():
                        if block_class.__name__ == line[0]:
                            block = block_class(position)
                            level.layout_rects.append(block)
                            level.layout[position[0]][position[1]] = block
        except FileNotFoundError:
            print("Failed to load a level.")

    @staticmethod
    def save_level():
        try:
            with open("assets/levels", "w") as level_file:
                for block in level.layout_rects:
                    level_file.write(str(block.__class__.__name__) + "; " + str(block.table_position) + "\n")
        except FileNotFoundError:
            print("Failed to save a level.")

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
        block = spike_block((5, 4))
        level.layout.append(block)
        level.layout_rects.append(block)
