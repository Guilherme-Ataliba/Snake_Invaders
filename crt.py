import pygame
from screenBase import ScreenBase
from random import randint

class CRT(ScreenBase):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        self.tv = pygame.image.load("Space-invaders-main/graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (self.screen_width, self.screen_height))

    def draw_lines(self):
        "Faz as linhas do efeito"
        line_height = 3
        line_amount = self.screen_height//line_height
        for line in range(line_amount):
            line_ypos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, line_ypos), (self.screen_width, line_ypos), 1)

    def draw(self):
        #Variamos o valor da transparência a cada tick para dar um efeito de tela piscando
        self.tv.set_alpha(randint(75, 100)) #termina o valor da transparencia 0 <= transparencia <= 255 (RGB)
        self.draw_lines()
        self.screen.blit(self.tv, (0,0))