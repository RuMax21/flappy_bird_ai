import pygame
import neat
import sys, time
from random import randint

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

        self.is_game_started = False
        self.game_loop()

    def drawing_objects(self, delta) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.bird.image_frame, self.bird.rect)
        self.screen.blit(self.ground.ground_image, (self.ground.start_x, self.ground.y))
        self.screen.blit(self.ground.ground_image, (self.ground.end_x, self.ground.y))

    def updating_objects(self, delta: float) -> None:
        if self.is_game_started:
            self.ground.move()
            self.bird.update(delta)


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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.is_game_started = True
                    if event.key == pygame.K_SPACE:
                        self.bird.horizontal_offset(delta)
            
            self.drawing_objects(delta)

            self.updating_objects(delta)

            pygame.display.update()
            self.clock.tick(60)

class Ground:
    SPEED: int = 2
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
        self.animation_count = 0

        self.gravity = 10
        self.speed_y = 0
        self.speed_x = 300
    
    def update(self, delta: float) -> None:
        self.speed_y += self.gravity * delta
        self.rect.y += self.speed_y
        self.animation()
    
    def horizontal_offset(self, delta: float) -> None:
        self.speed_y = -self.speed_x * delta

    def animation(self) -> None:
        if self.animation_count < 5:
            self.image_frame = self.images_of_birds[0]
        elif self.animation_count < 10:
            self.image_frame = self.images_of_birds[1]
        elif self.animation_count < 15:
            self.image_frame = self.images_of_birds[2]
        else:
            self.animation_count = 0
            self.image_frame = self.images_of_birds[0]
        
        self.animation_count += 1

class Tube:
    pass

game = Game()