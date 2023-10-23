import pygame
import neat
import os
import sys
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy bird with AI")

class Bird:
    def __init__(self) -> None:
        pass

class Tube():
    def __init__(self) -> None:
        pass

class Ground:
    def __init__(self) -> None:
        pass

def main():
    pygame.time.delay(10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()