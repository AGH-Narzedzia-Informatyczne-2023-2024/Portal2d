import pygame
from typing import List, Type, Tuple
from numpy import sign

import simulation
from simulation import variables



class entities(simulation.GameObjects):
    def __init__(self):
        super().__init__(True)
        self.collisions = []
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.new_position = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.image = pygame.Surface((0, 0))

    def update(self, collidables):
        '''updates it's position, state nad movement'''
        pass

    def collide(self, collidables: List[List[Type[pygame.Rect]]]):
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

    def blit(self, screen):
        try:
            self.image = pygame.transform.scale(self.image_og, (self.rect.width * simulation.variables.current_scale, self.rect.height * simulation.variables.current_scale))
            screen.blit(self.image, (simulation.variables.current_offset[0] + self.position.x * simulation.variables.current_scale, simulation.variables.current_offset[1] + self.position.y * simulation.variables.current_scale))
        except:
        #screen.blit(self.image, self.rect.scale_by(scale, scale).move(self.position.x * scale, self.position.y * scale))
            pygame.draw.rect(screen, (0, 0, 0), (simulation.variables.current_offset[0] + self.position[0] * simulation.variables.current_scale, simulation.variables.current_offset[1] + self.position[1] * simulation.variables.current_scale, self.rect.width * simulation.variables.current_scale, self.rect.height * simulation.variables.current_scale))

class enemy_bean(entities):
    def __init__(self, position: Tuple):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.image_og = pygame.image.load("assets/images/enemy_bean.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_og, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self, collidables):
        player = simulation.GameObjects.get("player")
        self.velocity.x = sign(player.position.x - self.position.x) * 3
        self.velocity.y = sign(player.position.y - self.position.y) * 3
        self.collide(collidables)

class enemy_virus(entities):
    def __init__(self, position: Tuple):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.image_og = pygame.image.load("assets/images/enemy_virus.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_og, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self, collidables):
        player = simulation.GameObjects.get("player")
        self.velocity.x = sign(player.position.x - self.position.x)
        self.velocity.y = sign(player.position.y - self.position.y)
        self.collide([])