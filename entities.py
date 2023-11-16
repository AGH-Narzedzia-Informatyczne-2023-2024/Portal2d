import pygame
from typing import List, Type, Tuple
from numpy import sign
from simulation import variables



class entities():
    def __init__(self):
        self.collisions = []
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.new_position = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self, *args, **kwargs):
        '''updates it's position, state nad movement'''
        pass

    def collide(self, collidables: List[Type[pygame.Rect]]):
        '''moves to by a designated velocity and for checks collisions, drives hitboxes out of each other if necessary'''
        self.new_position = pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y,
                                        self.rect.width, self.rect.height)
        self.collisions = [collidables[i] for i in self.new_position.collidelistall(collidables)]
        if self.collisions:
            self.new_position = self.rect
            steps = round(max(abs(self.velocity.x), abs(self.velocity.y)))
            if abs(self.velocity.x) > abs(self.velocity.y):
                for step in range(steps):
                    self.move_x(steps)
                    self.move_y(steps)
            else:
                for step in range(steps):
                    self.move_y(steps)
                    self.move_x(steps)

        else:
            # keep float point position
            self.position = pygame.Vector2(self.position.x + self.velocity.x, self.position.y + self.velocity.y)
        # move the actual rect
        self.rect = self.new_position

    def move_x(self, steps):
        self.position.x += self.velocity.x / steps
        self.new_position.x = self.position.x
        if self.new_position.collidelistall(self.collisions):
            self.position.x -= self.velocity.x / steps
            self.new_position.x = self.position.x
            self.velocity.x = 0

    def move_y(self, steps):
        self.position.y += self.velocity.y / steps
        self.new_position.y = self.position.y
        if self.new_position.collidelistall(self.collisions):
            self.position.y -= self.velocity.y / steps
            self.new_position.y = self.position.y
            self.velocity.y = 0