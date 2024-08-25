import pygame
from sys import exit

import pygame.freetype

from scripts.grid import Grid

from scripts.utils import draw_text


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pygame of life")

        self.WIDTH, self.HEIGTH = 1000, 800
        self.BLOCK_SIZE = 20
        self.FRAME_RATE = 30
        self.speed = 10

        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGTH))
        self.screen = pygame.Surface((self.WIDTH, self.HEIGTH))
        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()

        self.main_font = pygame.font.SysFont(
            "Courier New", int(self.BLOCK_SIZE * 1.2), bold=True)
        self.bg_music = pygame.mixer.Sound(r"assets/sounds/bgmusic2.mp3")

        self.generate = False
        self.generation = -1

        self.main_color = "white"
        self.secondary_color = "black"

        self.is_mb1_down = False

    def generate_grid(self):
        self.grid = Grid(self.WIDTH, self.HEIGTH, self.BLOCK_SIZE)
        self.grid.generate_grid()

    def update_grid(self):
        self.grid.update_grid()
        self.generation += 1

    def draw_grid(self):
        self.grid.draw_grid(self.screen, self.main_color, self.secondary_color)

    def on_hold_cancel(self):
        self.grid.cancel_holding()

    def on_hold(self, mouse_pos):
        self.grid.holding(mouse_pos)

    def on_click(self, mouse_pos):
        self.grid.click(mouse_pos)

    def draw_lines_grid(self):
        x = self.WIDTH // self.BLOCK_SIZE
        y = self.HEIGTH // self.BLOCK_SIZE

        # 031c29
        for i in range(x):
            pygame.draw.line(self.screen, "grey24", (i * self.BLOCK_SIZE,
                             0), (i * self.BLOCK_SIZE, self.HEIGTH), 2)
        for i in range(y):
            pygame.draw.line(self.screen, "grey24", (0, i *
                             self.BLOCK_SIZE), (self.WIDTH, i * self.BLOCK_SIZE), 2)

    def draw_text(self):
        text1 = "JOGO RODANDO" if self.generate else "JOGO PAUSADO"

        draw_text(self.screen, text1, self.WIDTH//2,
                  self.BLOCK_SIZE * 4, self.main_color, self.main_font)
        draw_text(self.screen, f"GERAÇÃO: {
                  self.generation}", self.BLOCK_SIZE * 7, self.BLOCK_SIZE * 4, self.main_color, self.main_font)
        draw_text(self.screen, f"POPULAÇÃO: {
                  self.grid.alive_cells}", self.BLOCK_SIZE * 8, self.BLOCK_SIZE * 8, self.main_color, self.main_font)
        draw_text(self.screen, f"VELOCIDADE: {
                  self.speed}", self.WIDTH - self.BLOCK_SIZE * 8, self.BLOCK_SIZE * 4, self.main_color, self.main_font)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.handle_mouse_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.generate = not self.generate
                if event.key == pygame.K_DOWN:
                    self.speed -= 1
                if event.key == pygame.K_UP:
                    self.speed += 1
                if event.key == pygame.K_ESCAPE:
                    self.restart_game()

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.generate:
            self.is_mb1_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_hold_cancel()
            self.is_mb1_down = False

        if self.is_mb1_down and hasattr(event, 'pos'):
            self.on_hold(event.pos)

    def restart_game(self):
        self.generate_grid()
        self.generation = 0
        self.generate = False

    def run(self):

        self.generate_grid()
        self.update_grid()

        self.draw_grid()

        self.bg_music.play(-1)

        while True:
            # self.screen.fill("#FFFFFF")
            self.handle_events()

            if self.generate:
                self.update_grid()
                self.FRAME_RATE = self.speed
            else:
                self.FRAME_RATE = 30

            self.draw_grid()
            self.draw_lines_grid()
            self.draw_text()

            self.display.blit(self.screen, self.screen_rect)
            pygame.display.update()
            self.clock.tick(self.FRAME_RATE)


Game().run()
