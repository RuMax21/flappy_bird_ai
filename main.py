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
        self.background = pygame.transform.scale(pygame.image.load('images/background.png').convert_alpha(), (600, 900))

        self.ground = Ground()
        self.birds = []
        self.tubes = []
        self.nets = []
        self.ge = []

        self.tube_generate_counter = -1
        self.score = 0

        self.score_monitoring = False

        self.clock = pygame.time.Clock()

    def drawing_objects(self, delta) -> None:
        self.screen.blit(self.background, (0, 0))
        for bird in self.birds:
            self.screen.blit(bird.image_frame, bird.rect)
        
        for tube in self.tubes:
            self.screen.blit(tube.tube_top, tube.rect_top)
            self.screen.blit(tube.tube_down, tube.rect_down)
        
        self.screen.blit(self.ground.ground_image, (self.ground.start_x, self.ground.y))
        self.screen.blit(self.ground.ground_image, (self.ground.end_x, self.ground.y))

        self.drawing_text()

    def drawing_text(self) -> None:
        bird_label = pygame.font.SysFont("comicsans", 50).render("Birds: " + str(len(self.birds)),1,(255,255,255))
        self.screen.blit(bird_label, (self.screen_width - bird_label.get_width() - 15, 10))

        score_label = pygame.font.SysFont("comicsans", 50).render("Score: " + str(self.score),1,(255,255,255))
        self.screen.blit(score_label, (self.screen_width - score_label.get_width() - 15, 40))

    def working_tubes(self, delta: float) -> None:
        if self.tube_generate_counter > 70:
            self.tubes.append(Tube())
            self.tube_generate_counter = 0
        self.tube_generate_counter += 1

        for tube in self.tubes:
            tube.update(delta)

        if len(self.tubes) != 0:
            if self.tubes[0].rect_top.right < 0:
                self.tubes.pop(0)

    def counter_score(self, bird) -> None:
        if len(self.tubes) > 0:
            if bird.rect.left > self.tubes[0].rect_down.left and bird.rect.right < self.tubes[0].rect_down.right and not self.score_monitoring:
                self.score_monitoring = True
            if bird.rect.left > self.tubes[0].rect_down.right and self.score_monitoring:
                self.score_monitoring = False
                self.score += 1
                for genome in self.ge:
                    genome.fitness += 1

    def collide_checking(self, bird) -> bool:
        if len(self.tubes):
            if (bird.rect.bottom > 730) or (bird.rect.top < 0) or bird.rect.colliderect(self.tubes[0].rect_top) or bird.rect.colliderect(self.tubes[0].rect_down):
                return True

    def restart_game(self) -> None:
        self.score = 0
        self.tubes.clear()

    def neat_run(self, config_path) -> None:
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
        population = neat.Population(config)

        population.add_reporter(neat.StdOutReporter(True))
        statistics = neat.StatisticsReporter()
        population.add_reporter(statistics)

        winner = population.run(self.game_loop, 50)

    def game_loop(self, genomes, config) -> None:
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.birds.append(Bird())
            self.ge.append(genome)

        run = True
        last_time = time.time()
        while run:
            new_time = time.time()
            delta = new_time - last_time
            last_time = new_time

            if len(self.birds) == 0:
                run = False
                self.restart_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            aiming_tube = 0
            if len(self.birds) > 0:
                if len(self.tubes) > 1 and self.birds[0].rect.x > self.tubes[0].rect_top.x + self.tubes[0].tube_top.get_width():
                    aiming_tube = 1

            for x, bird in enumerate(self.birds):
                self.ge[x].fitness += 0.1

                if len(self.tubes) > 0:
                    output = self.nets[self.birds.index(bird)].activate((bird.rect.y, bird.rect.y - self.tubes[aiming_tube].rect_top.y, bird.rect.y - self.tubes[aiming_tube].rect_down.y, bird.rect.x - self.tubes[aiming_tube].rect_down.x))
                    if output[0] > 0.5:
                        bird.moving_bird(delta)

            self.ground.move(delta)

            self.working_tubes(delta)

            for bird in self.birds:
                bird.update(delta)
                self.counter_score(bird)

                if self.collide_checking(bird):
                    self.ge[self.birds.index(bird)].fitness -= 5
                    self.nets.pop(self.birds.index(bird))
                    self.ge.pop(self.birds.index(bird))
                    self.birds.pop(self.birds.index(bird))
                else:
                    self.ge[self.birds.index(bird)].fitness += 5

            pygame.display.update()
            self.clock.tick(60)

            self.drawing_objects(delta)


class Ground:
    SPEED: int = 400
    SPAWN_Y: int = 730
    def __init__(self) -> None:
        self.ground_speed = self.SPEED
        self.ground_image = pygame.transform.scale2x(pygame.image.load('images/ground.png').convert_alpha())
        self.ground_width = self.ground_image.get_width()

        self.start_x = 0
        self.end_x = self.ground_width
        self.y = self.SPAWN_Y

    def move(self, delta: float) -> None:
        self.start_x -= self.ground_speed * delta
        self.end_x -= self.ground_speed * delta
        
        if self.start_x + self.ground_width < 0:
            self.start_x = self.end_x + self.ground_width
        
        if self.end_x + self.ground_width < 0:
            self.end_x = self.start_x + self.ground_width

class Bird:
    FLAP: int = 300
    GRAVITY: int = 9
    def __init__(self) -> None:
        self.images_of_birds = [pygame.transform.scale2x(pygame.image.load('images/bird1.png').convert_alpha()),
                                pygame.transform.scale2x(pygame.image.load('images/bird2.png').convert_alpha()),
                                pygame.transform.scale2x(pygame.image.load('images/bird3.png').convert_alpha())]
        self.index_frame = 0
        self.animation_count = 0
        self.image_frame = self.images_of_birds[self.index_frame]
        self.rect = self.image_frame.get_rect(center = (100, 100))

        self.gravity = self.GRAVITY
        self.flap = self.FLAP
        self.speed_y = 0

        self.is_flying = True
    
    def update(self, delta: float) -> None:
        if self.is_flying:
            self.speed_y += self.gravity * delta
            self.rect.y += self.speed_y
            self.animation()
        
    def moving_bird(self, delta: float) -> None:
        self.speed_y = -self.flap * delta

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
    MOVE_SPEED: int = 400
    DISTANCE: int = 220
    SPAWN_TUBE_X: int = 700

    def __init__(self) -> None:
        self.image = pygame.transform.scale2x(pygame.image.load('images/tube.png').convert_alpha())
        self.tube_down = pygame.transform.flip(self.image, False, True)
        self.tube_top = self.image

        self.move_speed = self.MOVE_SPEED
        self.distance = self.DISTANCE

        self.rect_top = self.tube_top.get_rect()
        self.rect_down = self.tube_down.get_rect()
       
        self.rect_top.y = randint(250, 520)
        self.rect_top.x = self.SPAWN_TUBE_X
        self.rect_down.y = self.rect_top.y - self.distance - self.rect_top.height
        self.rect_down.x = self.SPAWN_TUBE_X
        
    def update(self, delta: float) -> None:
        self.rect_top.x -= self.move_speed * delta
        self.rect_down.x -= self.move_speed * delta

if __name__ == "__main__":
    game = Game()
    config_path = 'config'
    game.neat_run(config_path)