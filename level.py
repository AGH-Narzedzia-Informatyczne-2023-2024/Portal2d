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
        self.has_hitbox = True

    def blit(self, screen):
        square_side = int(100 * simulation.variables.current_scale)
        self.position = (simulation.variables.current_offset[0] + self.table_position[0] * square_side, simulation.variables.current_offset[1] + self.table_position[1] * square_side)
        try:
            self.image_display = pygame.transform.scale(self.image, (square_side, square_side))
            screen.blit(self.image_display, self.position)
        except:
            # printf("failed to load")
            pygame.draw.rect(screen, (0, 200, 0), (self.position[0], self.position[1], square_side, square_side))

class basic_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image = pygame.image.load("assets/images/basic_block.png").convert()
        self.image_display = pygame.transform.scale(self.image, (100, 100))
        self.has_hitbox = True


class spike_block(building_block):

    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.image = pygame.image.load("assets/images/spike_block.png").convert()
        self.image_display = pygame.transform.scale(self.image, (100, 100))
        self.has_hitbox = False


class door_block(building_block):
    def __init__(self, position: Tuple) -> object:
        super().__init__(position)
        self.has_hitbox = False


class level:
    '''level layout is determinated by simulation.grid_size, every block is a class itself
    layout is in coordinates y, x'''

    layout_rects = []  # pure list [block, block, block, block]

    layout = [[None for i in range(simulation.variables.grid_size[1])]
              for j in range(simulation.variables.grid_size[0])]  # list of list [[block, block]
    #                                                                             [block, block]]

    @staticmethod
    def load_level(level_id: str):
        try:
            with open("assets/level" + level_id, "r") as level_file:
                level.layout_rects = []
                for i in range(simulation.variables.grid_size[0]):
                    for j in range(simulation.variables.grid_size[1]):
                        level.layout[i][j] = None
                for gameElement in simulation.gameObjects:
                    if any([gameElement.__class__.__name__ == name.__name__ for name in building_block.__subclasses__()]):
                        gameElement.delete()
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
    def save_level(level_id: str):
        try:
            with open("assets/level" + level_id, "w") as level_file:
                for block in level.layout_rects:
                    level_file.write(str(block.__class__.__name__) + "; " + str(block.table_position) + "\n")
        except FileNotFoundError:
            print("Failed to save a level.")

    @staticmethod
    def create_level():
        for i in range(simulation.variables.grid_size[0]):
            temp = []
            for j in range(simulation.variables.grid_size[1]):
                if i == 0 or i == simulation.variables.grid_size[0] - 1 or j == 0 or j == simulation.variables.grid_size[1] - 1:
                    block = basic_block((i, j))
                    temp.append(block)
                    level.layout_rects.append(block)
                else:
                    temp.append(None)
            level.layout.append(temp)
        block = spike_block((5, 4))
        level.layout.append(block)
        level.layout_rects.append(block)
