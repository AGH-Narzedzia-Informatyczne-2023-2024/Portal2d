import pygame

class level:
    class wall:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)
            level.list_of_walls.append(self)

    list_of_walls = []

    @staticmethod
    def create_level():
        level.wall(1200, 0, 80, 720)
        level.wall(0, 0, 80, 720)
        level.wall(0, 0, 1280, 80)
        level.wall(0, 640, 1280, 80)
        level.wall(500, 300, 80, 80)