import pygame
import json


class variables:
    max_velocity = 100
    movement_velocity = 7
    frame_rate = 60
    screen_size = (1300, 900)
    current_offset = [0, 0]
    current_scale = 1

def get_current_scale():
    width, height = pygame.display.get_surface().get_size()
    if width / 13 > height / 9:
        variables.current_scale = height / variables.screen_size[1]
        variables.current_offset[0] = abs((variables.screen_size[0] * variables.current_scale - width) / 2)
        variables.current_offset[1] = 0
    else:
        variables.current_scale = width / variables.screen_size[0]
        variables.current_offset[1] = abs((variables.screen_size[1] * variables.current_scale - height) / 2)
        variables.current_offset[0] = 0

gameObjects = []
gameEntities = []
class GameObjects:
    def __init__(self, isEntity: bool = False):
        gameObjects.append(self)
        if isEntity:
            gameEntities.append(self)

    @staticmethod
    def get(name: str):
        for gameObject in gameObjects:
            if gameObject.__class__.__name__ == name:
                return gameObject
        return None


    @staticmethod
    def update(collidables):
        for entity in gameEntities:
            entity.update(collidables)
    @staticmethod
    def blit(screen):
        for object in gameObjects:
            object.blit(screen)


class settings:
    settings_dictionary = {"key_down": "r", "key_up": "w", "key_left": "a", "key_right": "s", "shoot": "space"}
    pygame_settings_dictionary = {"1": pygame.K_1, "2": pygame.K_2, "3": pygame.K_3, "4": pygame.K_4, "5": pygame.K_5,
                                  "6": pygame.K_6, "7": pygame.K_7, "8": pygame.K_8, "9": pygame.K_9, "0": pygame.K_0,
                                  "q": pygame.K_q, "w": pygame.K_w, "f": pygame.K_f, "p": pygame.K_p, "g": pygame.K_g,
                                  "j": pygame.K_j, "l": pygame.K_l, "u": pygame.K_u, "y": pygame.K_y, "a": pygame.K_a,
                                  "r": pygame.K_r, "s": pygame.K_s, "t": pygame.K_t, "d": pygame.K_d, "h": pygame.K_h,
                                  "n": pygame.K_n, "e": pygame.K_e, "i": pygame.K_i, "o": pygame.K_o, "z": pygame.K_z,
                                  "x": pygame.K_x, "c": pygame.K_c, "v": pygame.K_v, "b": pygame.K_b, "k": pygame.K_k,
                                  "m": pygame.K_m, "space": pygame.K_SPACE}
    key_down = None
    key_up = None
    key_left = None
    key_right = None
    shoot = None

    @staticmethod
    def read_settings():
        try:
            with open("assets/settings.json") as settings_file:
                data = json.load(settings_file)
                for i in data:
                    settings.settings_dictionary[i] = data[i]
        except FileNotFoundError:
            print("Failed to read settings.")
        settings.key_down = settings.pygame_settings_dictionary[settings.settings_dictionary["key_down"]]
        settings.key_up = settings.pygame_settings_dictionary[settings.settings_dictionary["key_up"]]
        settings.key_left = settings.pygame_settings_dictionary[settings.settings_dictionary["key_left"]]
        settings.key_right = settings.pygame_settings_dictionary[settings.settings_dictionary["key_right"]]
        settings.shoot = settings.pygame_settings_dictionary[settings.settings_dictionary["shoot"]]

    @staticmethod
    def save_settings():
        try:
            with open("assets/settings.json", "w") as settings_file:
                settings_file.write(json.dumps(settings.settings_dictionary))
        except FileNotFoundError:
            print("Failed to save settings.")
