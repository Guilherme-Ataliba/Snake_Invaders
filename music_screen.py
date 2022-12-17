import pygame
from screenBase import ScreenBase
from menu import Menu
from music_mixer import *

class MusicScreen(Menu):
    def __init__(self, screen, screen_width, screen_height, text_color = 'white'):
        super().__init__(screen, screen_width, screen_height, text_color)
        self.text_color = text_color
        self.v_unit = 2*self.v_unit     #redefinindo a unidade vertical para melhor caber nessa tela

        #Volumes para cada canal
        self.music_value = 0
        self.sfx_value = 0
        self.menu_value = 0

        #incremento no volume
        self.volume_constant = 0.05

        # Carregamento dos elementos visuais
        self.load_volume_control()

        #Redefinindo parâmetros da classe menu para esse contexto
        self.options = {'music': self.music_text_rect, 'sfx': self.sfx_text_rect, 'menu': self.menu_text_rect}
        self.arrow_rect = self.arrow_surf.get_rect(
            center=(self.music_text_rect.left - self.h_unit, self.music_text_rect.centery)) #Posição inicial da seta

    #Controle de volume
    def increase_volume(self, current_volume):
        option = list(self.options.keys())[self.arrow_selected]     #verificando qual opção está selecionada pela flecha

        if option == 'music' and round(current_volume[0], 1) < 0.5:     #fazemos round pois, após algumas iterações, os números flutuantes flutuam
            self.music_value += self.volume_constant
        elif option == 'sfx' and round(current_volume[1], 1) < 0.5:
            self.sfx_value += self.volume_constant
        elif option == 'menu' and round(current_volume[2], 1) < 0.5:
            self.menu_value += self.volume_constant

        return [self.music_value, self.sfx_value, self.menu_value]

    def decrease_volume(self, current_volume):
        option = list(self.options.keys())[self.arrow_selected]

        if option == 'music' and round(current_volume[0], 1) > -0.5:
            self.music_value -= self.volume_constant
        elif option == 'sfx' and round(current_volume[1], 1) > -0.5:
            self.sfx_value -= self.volume_constant
        elif option == 'menu' and round(current_volume[2], 1) > -0.5:
            self.menu_value -= self.volume_constant

        return [self.music_value, self.sfx_value, self.menu_value]

    def get_volume_list(self):
        return [self.music_value, self.sfx_value, self.menu_value]

    #Montando a tela
    def make_title_screen(self):
        self.title_rect.x = 0
        self.screen.blit(self.title_screen, self.title_rect)

        score_text_font = pygame.font.Font("Space-invaders-main/font/8-bit Arcade In.ttf", 120)
        score_text = score_text_font.render("Music and Sfx", False, '#a1e2e8')
        score_text_rect = score_text.get_rect(
            midleft=(self.title_rect.right + self.title_rect.centerx / 2, self.title_rect.centery))

        self.screen.blit(score_text, score_text_rect)

    """Essa função carrega todos os elementos visuais que serão necessários na tela de música"""
    def load_volume_control(self):
        position_x = self.screen_width / 2 - 50
        position_y = self.title_rect.centery + self.v_unit

        self.music_text = self.big_menu_font.render(f"Music: {int(self.music_value*100+50)}", False, self.text_color)
        self.music_text_rect = self.music_text.get_rect(center = (position_x, position_y))

        self.sfx_text = self.big_menu_font.render(f"SFX: {int(self.sfx_value*100+50)}", False, self.text_color)
        self.sfx_text_rect = self.sfx_text.get_rect(center = (position_x, position_y + self.v_unit))

        self.menu_text = self.big_menu_font.render(f"Menu: {int(self.menu_value*100+50)}", False, self.text_color)
        self.menu_text_rect = self.menu_text.get_rect(center = (position_x, position_y + 2*self.v_unit))

    def make_volume_control(self):
        self.screen.blit(self.music_text, self.music_text_rect)
        self.screen.blit(self.sfx_text, self.sfx_text_rect)
        self.screen.blit(self.menu_text, self.menu_text_rect)

    def make_arrow(self):
        self.screen.blit(self.arrow_surf, self.arrow_rect)

    def update(self):
        self.load_volume_control()
        self.make_title_screen()
        self.make_volume_control()
        self.make_arrow()
        self.arrow_animation()





