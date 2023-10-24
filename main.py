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

        self.tubes = []
        self.tube_generate_counter = 71
        self.score = 0
        self.passed = False

        self.is_game_started = False
        self.game_loop()

    def drawing_objects(self, delta) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.bird.image_frame, self.bird.rect)
        
        for tube in self.tubes:
            self.screen.blit(tube.tube_top, tube.rect_top)
            self.screen.blit(tube.tube_bottom, tube.rect_down)
        
        self.screen.blit(self.ground.ground_image, (self.ground.start_x, self.ground.y))
        self.screen.blit(self.ground.ground_image, (self.ground.end_x, self.ground.y))

        score_label = pygame.font.SysFont("comicsans", 50).render("Score: " + str(self.score),1,(255,255,255))
        self.screen.blit(score_label, (self.screen_width - score_label.get_width() - 15, 10))

    def updating_objects(self, delta: float) -> None:
        if self.is_game_started:
            self.ground.move()
            self.bird.update(delta)

            if self.tube_generate_counter > 70:
                self.tubes.append(Tube())
                self.tube_generate_counter = 0
            self.tube_generate_counter += 1

            for tube in self.tubes:
                tube.update(delta)


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
    # IMAGE_TUBE = pygame.transform.scale2x(pygame.image.load('images/tube.png').convert_alpha())
    MOVE_SPEED = 250
    def __init__(self):
        self.image = pygame.transform.scale2x(pygame.image.load('images/tube.png').convert_alpha())
        self.tube_bottom = pygame.transform.flip(self.image, False, True)
        self.tube_top = self.image
        self.rect_top = self.tube_top.get_rect()
        self.rect_down = self.tube_bottom.get_rect()
        self.distance = 150
        self.rect_top.y = randint(250, 520)
        self.rect_top.x = 700
        self.rect_down.y = self.rect_top.y - self.distance - self.rect_top.height
        self.rect_down.x = 700
        self.move_speed = self.MOVE_SPEED

    def update(self, delta):
        self.rect_top.x -= self.move_speed * delta
        self.rect_down.x -= self.move_speed * delta


game = Game()