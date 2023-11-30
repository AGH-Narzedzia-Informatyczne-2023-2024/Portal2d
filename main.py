import pygame
import simulation
import entities
import sys
import player

import level
import menu


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(simulation.variables.screen_size, pygame.RESIZABLE)
    screen.fill((255, 255, 255))

    level.level.create_level()

    level.level.load_level()

    character = player.player((300, 300))

    entities.enemy_bean((500, 500))
    entities.enemy_virus((900, 700))

    left = False
    right = False
    up = False
    down = False

    simulation.settings.read_settings()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pass
            if event.type == pygame.VIDEOEXPOSE:
                pass
            if event.type == pygame.KEYUP:
                if event.key == simulation.settings.key_left:
                    left = False
                if event.key == simulation.settings.key_right:
                    right = False
                if event.key == simulation.settings.key_up:
                    up = False
                if event.key == simulation.settings.key_down:
                    down = False
            if event.type == pygame.KEYDOWN:
                if event.key == simulation.settings.key_left:
                    left = True
                if event.key == simulation.settings.key_right:
                    right = True
                if event.key == simulation.settings.key_up:
                    up = True
                if event.key == simulation.settings.key_down:
                    down = True

        if left and right:
            character.move("stop horizontal")
        elif right:
            character.move("right")
        elif left:
            character.move("left")
        else:
            character.move("stop horizontal")

        if up and down:
            character.move("stop vertical")
        elif up:
            character.move("up")
        elif down:
            character.move("down")
        else:
            character.move("stop vertical")

        simulation.GameObjects.update(level.level.layout_rects)

        screen.fill((255, 255, 255))

        simulation.GameObjects.blit(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__": main()
