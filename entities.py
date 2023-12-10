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
        self.image_display = None

    def update(self, collidables):
        '''updates it's position, state nad movement'''
        pass

    def collide(self, collidables: List[List[Type[pygame.Rect]]]):
        '''moves to by a designated velocity and for checks collisions, drives hitboxes out of each other if necessary'''
        self.new_position = pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y,
                                        self.rect.width, self.rect.height)
        self.collisions = [collidables[i] for i in self.new_position.collidelistall(collidables)]
        #check if it has hitbox
        for collidable in self.collisions:
            # define interaction
            if self.__class__.__name__ == "player":
                self.interact(collidable.__class__.__name__)
            if not collidable.has_hitbox:
                self.collisions.remove(collidable)

        if self.collisions:
            self.new_position = self.rect
            steps = round(self.velocity.length())
            if steps == 0:
                return
            velocity = self.velocity.normalize()
            for step in range(steps):

                self.position.x += velocity.x
                self.new_position.x = self.position.x
                if self.new_position.collidelistall(self.collisions):
                    self.position.x -= velocity.x
                    self.new_position.x = self.position.x
                    self.velocity.x = 0
                    velocity.x = 0

                self.position.y += velocity.y
                self.new_position.y = self.position.y
                if self.new_position.collidelistall(self.collisions):
                    self.position.y -= velocity.y
                    self.new_position.y = self.position.y
                    self.velocity.y = 0
                    velocity.y = 0
        else:
            # keep float point position
            self.position = pygame.Vector2(self.position.x + self.velocity.x, self.position.y + self.velocity.y)
        # move the actual rect
        self.rect = self.new_position

    def blit(self, screen):
        try:
            self.image_display = pygame.transform.scale(self.image, (self.rect.width * simulation.variables.current_scale, self.rect.height * simulation.variables.current_scale))
            screen.blit(self.image_display, (simulation.variables.current_offset[0] + self.position.x * simulation.variables.current_scale, simulation.variables.current_offset[1] + self.position.y * simulation.variables.current_scale))
        except:
            pygame.draw.rect(screen, (0, 0, 0), (simulation.variables.current_offset[0] + self.position[0] * simulation.variables.current_scale, simulation.variables.current_offset[1] + self.position[1] * simulation.variables.current_scale, self.rect.width * simulation.variables.current_scale, self.rect.height * simulation.variables.current_scale))


class enemy_bean(entities):
    def __init__(self, position: Tuple):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.image = pygame.image.load("assets/images/enemy_bean.png").convert_alpha()
        self.image_display = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image_display.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self, collidables):
        player = simulation.GameObjects.get("player")
        self.velocity.x = player.rect.centerx - self.rect.centerx
        self.velocity.y = player.rect.centery - self.rect.centery
        if self.velocity.length() != 0:
            self.velocity.clamp_magnitude_ip(3)
        self.collide(collidables)

class enemy_virus(entities):
    def __init__(self, position: Tuple):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.image = pygame.image.load("assets/images/enemy_virus.png").convert_alpha()
        self.image_display = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image_display.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self, collidables):
        player = simulation.GameObjects.get("player")
        self.velocity.x = player.rect.centerx - self.rect.centerx
        self.velocity.y = player.rect.centery - self.rect.centery
        if self.velocity.length() != 0:
            self.velocity.clamp_magnitude_ip(1)
        self.collide([])

ownedItems = []
class playerItems():
    def __init__(self):
        self.owned = False
        self.equipped = False

    def obtain(self):
        self.owned = True
        ownedItems.append(self)

    def equip(self):
        pass                            #TBA kiedy bedzie inventory

class Guns(playerItems):
    def __init__(self, bullet_velocity: int):
        super().__init__()
        self.bullet_velocity = bullet_velocity

class PortalGuns(Guns):
    pass

class LaserGuns(Guns):
    pass

class Shoes(playerItems):
    def __init__(self, bonus_speed: int):
        super().__init__()
        self.bonus_speed = bonus_speed

class Potions(playerItems):
    def __init__(self):
        super().__init__()
        self.used = False

class HP_Potions(Potions):
    def __init__(self, points: int):
        super().__init__()
        self.points = points

    def obtain(self):
        self.owned = True
        self.used = False
        ownedItems.append(self)

    def drink(self):
        self.used = True
        #Dodac HP
        ownedItems.remove(self)

class MysteryBox(playerItems):
    def __init__(self):
        super().__init__()






