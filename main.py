import pygame
import neat
import os
import sys, time
import random

pygame.init()

class Game:
    WIDTH: int = 600
    HEIGHT: int = 800
    def __init__(self) -> None:
        self.screen_width = self.WIDTH
        self.screen_height = self.HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.caption = pygame.display.set_caption("Flappy bird with AI")

        self.clock = pygame.time.Clock()

        self.background = pygame.transform.scale(pygame.image.load('images/background.png').convert_alpha(), (600, 900))
        self.ground = Ground()
        self.bird = Bird()

        self.game_loop()

    def drawing_objects(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ground.ground_image, (self.ground.start_x, self.ground.y))
        self.screen.blit(self.ground.ground_image, (self.ground.end_x, self.ground.y))
        self.screen.blit(self.bird.image_frame, self.bird.rect)

    def game_loop(self) -> None:
        last_time = time.time()
        while True:
            new_time = time.time()
            delta = new_time - last_time
            last_time = new_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.drawing_objects()
            self.ground.move()
            self.bird.update(delta)

            pygame.display.update()
            self.clock.tick(60)

class Ground:
    SPEED: float = 2.5
    SPAWN_Y: int = 730
    def __init__(self) -> None:
        self.ground_speed = self.SPEED
        self.ground_image = pygame.transform.scale2x(pygame.image.load('images/ground.png').convert_alpha())
        self.ground_width = self.ground_image.get_width()

        self.start_x = 0
        self.end_x = self.ground_width
        self.y = self.SPAWN_Y

    def move(self) -> None:
        self.start_x -= self.ground_speed
        self.end_x -= self.ground_speed
        
        if self.start_x + self.ground_width < 0:
            self.start_x = self.end_x + self.ground_width
        
        if self.end_x + self.ground_width < 0:
            self.end_x = self.start_x + self.ground_width

class Bird:
    def __init__(self) -> None:
        self.images_of_birds = [pygame.transform.scale2x(pygame.image.load('images/bird1.png').convert_alpha()),
                                pygame.transform.scale2x(pygame.image.load('images/bird2.png').convert_alpha()),
                                pygame.transform.scale2x(pygame.image.load('images/bird3.png').convert_alpha())]
        self.index_frame = 0
        self.image_frame = self.images_of_birds[self.index_frame]
        self.rect = self.image_frame.get_rect(center = (100, 100))
        
        self.gravity = 10
        self.speed_y = 0
    
    def update(self, delta) -> None:
        self.speed_y += self.gravity * delta
        self.rect.y += self.speed_y

class Tube():
    def __init__(self) -> None:
        pass


game = Game()