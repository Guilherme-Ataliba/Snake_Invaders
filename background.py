import pygame
from screenBase import *

class Background(ScreenBase):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        self.background_surfaces = {}
        self.gif_background_surfaces = {}

        self.load_background("menu", "Space-invaders-main/graphics/background.png")

        self.load_gif_background("game", 43,
         "Space-invaders-main/graphics/Possible_Backgrounds/Gifs/space_and_stars/pixel art _ Tumblr-", '.png')

        self.load_gif_background("victory", 19, "Space-invaders-main/graphics/Possible_Backgrounds/Gifs/clouds_sun_river_black/Pixel Gif -",
        '.png')

    def load_background(self, name, path):
        temp_background = pygame.image.load(path).convert_alpha()
        temp_background = pygame.transform.scale(temp_background, (self.screen_width, self.screen_height))
        self.background_surfaces[name] = temp_background

    def draw_background(self, name):
        self.screen.blit(self.background_surfaces[name], (0,0))

    def load_gif_background(self, name, number_images, path, extension):
        temp_background = Gifs(self.screen, self.screen_width, self.screen_height, number_images, path, extension)
        self.gif_background_surfaces[name] = temp_background

    def draw_gif_background(self, name, speed=1, fade=False):
        self.gif_background_surfaces[name].play_gifs(speed=speed, fade=fade)


class Mensager(ScreenBase):
    def __init__(self, screen, screen_width, screen_height, message, color='white'):
        super().__init__(screen, screen_width, screen_height)
        self.counter = 0
        self.time = 0

        self.text_surface = self.menu_font.render(message, False, color).convert_alpha()


    def load(self, pos, time):
        self.text_rect = self.text_surface.get_rect(topleft=pos)
        self.time = time
        self.counter = 0

    def draw(self):
        self.counter += 1
        if self.counter <= self.time:
            self.screen.blit(self.text_surface, self.text_rect)



