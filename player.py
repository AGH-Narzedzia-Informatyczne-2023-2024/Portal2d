import pygame
from typing import List, Type, Tuple
from numpy import sign
from simulation import variables
import entities

class player(entities.entities):
    def __init__(self, init_position: Tuple[int, int]):
        self.rect = pygame.Rect(init_position[0], init_position[1], 100, 100)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, (0, 0, 0), self.rect)
        self.position = pygame.Vector2(init_position[0], init_position[1])
        self.velocity = pygame.Vector2(0, 0)
        self.new_position = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self, collidables: List[List[Type[pygame.Rect]]]):
        # limit maximum velocity
        if abs(self.velocity.x) > variables.max_velocity:
            self.velocity.x = sign(self.velocity.x) * variables.max_velocity
        if abs(self.velocity.y) > variables.max_velocity:
            self.velocity.y = sign(self.velocity.y) * variables.max_velocity
        # move and check collisions
        self.collide(collidables)

    def move(self, direction: str):
        if direction == "left":
            self.velocity.x = - variables.movement_velocity
        elif direction == "right":
            self.velocity.x = variables.movement_velocity
        elif direction == "stop horizontal":
            self.velocity.x = 0
        elif direction == "up":
            self.velocity.y = - variables.movement_velocity
        elif direction == "down":
            self.velocity.y = variables.movement_velocity
        elif direction == "stop vertical":
            self.velocity.y = 0