import pygame
from math import cos
from screenBase import ScreenBase
from music_mixer import Mixer

class Menu(ScreenBase):
    def __init__(self,screen, screen_width, screen_height, text_color='white'):
        super().__init__(screen, screen_width, screen_height)

        """Referente a criação visual do menu inicial"""
        #Start text
        self.start_text = self.menu_font.render("Start", False, text_color)
        self.start_text_rect = self.start_text.get_rect(center = (self.title_rect.centerx, self.title_rect.centery + self.v_unit*2))

        #Score text
        self.score_text = self.menu_font.render("Score", False, text_color)
        self.score_text_rect = self.start_text.get_rect(center=(self.start_text_rect.centerx, self.start_text_rect.centery + self.v_unit))

        #Music text
        self.music_text = self.menu_font.render("Music", False, text_color)
        self.music_text_rect = self.music_text.get_rect(
            center=(self.score_text_rect.centerx, self.score_text_rect.centery + self.v_unit))

        #Exit text
        self.exit_text = self.menu_font.render("Quit Game", False, text_color)
        self.exit_text_rect = self.exit_text.get_rect(center=(self.music_text_rect.centerx, self.music_text_rect.centery + self.v_unit))


        """Referente a lógica de como os menus irão funcionar"""
        #Arrow
        self.arrow_surf = pygame.image.load("Space-invaders-main/graphics/New Piskel.png").convert_alpha()
        self.arrow_surf = pygame.transform.scale(self.arrow_surf, (self.arrow_surf.get_width()*0.8, self.arrow_surf.get_height()*0.8))
        self.arrow_rect = self.arrow_surf.get_rect(center = (self.start_text_rect.left - self.h_unit, self.start_text_rect.centery))

        self.arrow_selected = 0     #Diz a opção selecionada no momento
        self.options = {'start' : self.start_text_rect, 'score' : self.score_text_rect, 'music' : self.music_text_rect,
                        'exit' : self.exit_text_rect}

        self.arrow_movement = 1     #Faz parte da animação da flecha, serve como um angulo que sempre aumenta

        #Sound
        self.mixer = Mixer()

    #Lógica da seleção/flecha
    def arrow_down(self):
        "Move a seta uma opção para baixo"
        number_of_options = len(self.options)

        #Contador utilizando resto da divisão
        self.arrow_selected = (self.arrow_selected + 1) % number_of_options

        #Utilizamos isso para tornar mais simples a implementação de subclasses
        options_values = list(self.options.values())

        #Se a seta estiver an última posição, ela vai pra primeira
        if self.arrow_rect.centery == options_values[len(options_values)-1].centery:
            self.arrow_rect.centery = options_values[0].centery

        #caso contrário, vai pra opção a baixo
        else:
            self.arrow_rect.centery = options_values[self.arrow_selected].centery

        #Reposiciona a seta horizontalmente, para combinar com o tamanho da palvra que representa a opção
        self.arrow_rect.centerx = options_values[self.arrow_selected].left - self.h_unit
        self.arrow_movement = 1 #Resolvendo bug de entrar na letra no meio de uma transição de uma opção para outra
        #ocorre pois continua somando de onde o angulo estava à partir da nova posição

        self.mixer.play_menu_sounds('switch')

    def arrow_up(self):
        #Move a seta um opção para cima
        number_of_options = len(self.options)
        self.arrow_selected = (self.arrow_selected - 1) % number_of_options

        # Utilizamos isso para tornar mais simples a implementação de subclasses
        options_values = list(self.options.values())

        if self.arrow_rect.centery == options_values[0].centery:
            self.arrow_rect.centery = options_values[len(options_values)-1].centery
        else:
            self.arrow_rect.centery = options_values[self.arrow_selected].centery

        self.arrow_rect.centerx = options_values[self.arrow_selected].left - self.h_unit
        self.arrow_movement = 1  #resolvendo bug

        self.mixer.play_menu_sounds('switch')

    def arrow_select(self):
        option = list(self.options.keys())[self.arrow_selected]
        if option == 'start':
            self.mixer.play_menu_sounds('game_start')
        else:
            self.mixer.play_menu_sounds('select')
        return option

    #Criação visual do menu
    def show(self):
        self.screen.blit(self.title_screen, self.title_rect)
        self.screen.blit(self.start_text, self.start_text_rect)
        self.screen.blit(self.arrow_surf, self.arrow_rect)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.music_text, self.music_text_rect)
        self.screen.blit(self.exit_text, self.exit_text_rect)

    def arrow_animation(self):
        #bug com soma de inteiros e floats em python. inteiro - float sempre reduz em 1, inteiro + float só adiciona um
        #se float maior que 0.5
        self.arrow_movement += 0.1
        if cos(self.arrow_movement) > 0 : self.arrow_rect.x += 1
        else: self.arrow_rect.x -= 1

    def update(self):
        self.show()
        self.arrow_animation()
