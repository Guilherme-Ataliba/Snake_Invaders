import pygame
from screenBase import *
from get_input import Input
from background import Background

class EndScreen(ScreenBase):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        self.background_manager = Background(self.screen, self.screen_width, self.screen_height)

        #Death Screen
        self.you_died_text = self.big_menu_font.render("GAME OVER", False, 'white', 'black')
        self.you_died_rect = self.you_died_text.get_rect(center = (self.screen_width/2, 2*self.v_unit))
        self.type_your_name_lose_text = self.menu_font.render("Name: ", False, 'white', 'black')
        self.type_your_name_lose_rect = self.type_your_name_lose_text.get_rect(center = (self.screen_width/2-50,
                                                                               self.you_died_rect.centery + 4*self.v_unit))

        #Win Screen
        self.you_win_surf = pygame.image.load("Space-invaders-main/graphics/you_win.png").convert_alpha()
        self.you_win_surf = pygame.transform.scale(self.you_win_surf,
                                                   (self.you_win_surf.get_width()/2, self.you_win_surf.get_height()/2))
        self.you_win_rect = self.you_win_surf.get_rect(center = (self.screen_width/2, 2*self.v_unit))

        self.type_your_name_win_text = self.menu_font.render("Name: ", False, 'white')
        self.type_your_name_win_rect = self.type_your_name_win_text.get_rect(center=(self.screen_width / 2 - 50,
                                                                                       self.you_died_rect.centery + 5 * self.v_unit))

    def load_score(self, score, pos, type):
        """Carrega as variáveis que iram mostrar o score na tela"""
        if type == 'win':
            self.score_text = self.menu_font.render(f'Score: {score}', False, 'white')
        else:
            self.score_text = self.menu_font.render(f'Score: {score}', False, 'white', 'black')

        self.score_rect = self.score_text.get_rect(center = pos)

    def death_screen_draw(self, score):
        self.load_score(score, ((self.you_died_rect.centerx, self.you_died_rect.centery + 2*self.v_unit)), 'death')

        self.score_pos_rect = pygame.Rect(self.type_your_name_lose_rect.right, self.type_your_name_lose_rect.top,
                                      2 * self.h_unit, self.v_unit)

        pygame.draw.rect(self.screen, 'black', self.score_pos_rect)
        self.screen.blit(self.you_died_text, self.you_died_rect)
        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.type_your_name_lose_text, self.type_your_name_lose_rect)

    def get_score_rect(self):
        return self.score_pos_rect

    def victory_screen_draw(self, score):
        self.load_score(score, ((self.you_win_rect.centerx, self.you_win_rect.centery + 3*self.v_unit)), 'win')

        self.score_pos_rect = pygame.Rect(self.type_your_name_win_rect.right, self.type_your_name_win_rect.top,
                                      2 * self.h_unit, self.v_unit)

        self.background_manager.draw_gif_background("victory", 0.2, 0.8)
        self.screen.blit(self.you_win_surf, self.you_win_rect)
        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.type_your_name_win_text, self.type_your_name_win_rect)


