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

    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))

    character = player.player((300, 300))

    level.level.create_level()

    left = False
    right = False
    up = False
    down = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_s:
                    right = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_r:
                    down = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_s:
                    right = True
                if event.key == pygame.K_w:
                    up = True
                if event.key == pygame.K_r:
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

        character.update(level.level.list_of_walls)
        screen.fill((255, 255, 255))

        for wall in level.level.list_of_walls:
            pygame.draw.rect(screen, (200, 0, 200), wall.rect)
        screen.blit(character.image, character.rect)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__": main()