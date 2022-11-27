import random
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER = pygame.Rect(WIDTH // 2 - 5, HEIGHT, 10, HEIGHT)

SPEED_PER_ITERATION = 0.03
SPEED_PER_SCORE = 3
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SCORE_FONT = pygame.font.SysFont('comicsans', 20)

player_img = pygame.image.load("spaceship.png")
player_ship = pygame.transform.rotate(pygame.transform.scale(player_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
astroid_img = pygame.image.load("clipart4515928.png")


class Game:

    def __init__(self):
        self.ship_pos = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.bullets = []
        self.spawn_counter = 0
        self.spawn_rate = 90
        self.score = 0
        self.fps = 60.0
        self.collision = False
        self.asteroids = []

    def drawWindow(self):
        WIN.fill(BLACK)
        WIN.blit(player_ship, (self.ship_pos.x, self.ship_pos.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, WHITE, bullet)
        for astroid in self.asteroids:
            # pygame.draw.rect(WIN, WHITE, astroid) => draw as a regtengle
            astroid_draw = pygame.transform.rotate(pygame.transform.scale(astroid_img, (astroid.width, astroid.height)),
                                                   -40)
            WIN.blit(astroid_draw, (astroid.x, astroid.y))
        draw_text = SCORE_FONT.render(str(int(self.score)), 1, WHITE)
        WIN.blit(draw_text, (10, 5))
        pygame.display.update()

    def ship_mov(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a] and self.ship_pos.x > 0:
            self.ship_pos.x -= VEL
        if key_pressed[pygame.K_d] and self.ship_pos.x + VEL + self.ship_pos.width < BORDER.x:
            self.ship_pos.x += VEL
        if key_pressed[pygame.K_w] and self.ship_pos.y > 0:
            self.ship_pos.y -= VEL
        if key_pressed[pygame.K_s] and self.ship_pos.y + VEL + self.ship_pos.height < BORDER.y:
            self.ship_pos.y += VEL

    def handle_astroid_beam(self):
        asteroid_index, beam_index = 0, 0

        for bullet in self.bullets:
            bullet.x += BULLET_VEL

        while asteroid_index < len(self.asteroids):
            astroid = self.asteroids[asteroid_index]
            if astroid.x < 0:
                self.asteroids.remove(astroid)
                continue

            while beam_index < len(self.bullets):
                bullet = self.bullets[beam_index]
                if bullet.x > WIDTH:
                    self.bullets.pop(beam_index)
                    continue
                if astroid.colliderect(bullet):
                    self.bullets.pop(beam_index)
                    self.asteroids.pop(asteroid_index)
                    self.score += 50
                    self.fps += 5
                    continue
                beam_index += 1

            # Ship Col chedck

            if astroid.colliderect(self.ship_pos):
                print(self.score)
                self.collision = True
            asteroid_index += 1

    def handle_astroid(self):
        if self.spawn_counter == self.spawn_rate:
            self.spawn_counter = 0
            astrid_scale = random.randint(90, 150)
            astroid = pygame.Rect(WIDTH, random.randint(self.ship_pos.width, BORDER.height - astrid_scale),
                                  astrid_scale, astrid_scale)
            self.asteroids.append(astroid)

        for asteroid in self.asteroids:
            asteroid.x -= BULLET_VEL

    def handle_events(self):
        # Event tracker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Bullets
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(self.bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(self.ship_pos.x + self.ship_pos.width,
                                         self.ship_pos.y + self.ship_pos.height // 2, 20, 5)
                    self.bullets.append(bullet)

    def play_step(self):
        self.spawn_counter += 1
        self.fps += SPEED_PER_ITERATION
        self.score += 0.1

        self.handle_events()
        self.handle_astroid()
        self.handle_astroid_beam()
        self.ship_mov()
        self.drawWindow()

    def main(self):
        clock = pygame.time.Clock()

        while clock.tick(self.fps) and not self.collision:
            self.play_step()


if __name__ == "__main__":
    game = Game()
    game.main()
