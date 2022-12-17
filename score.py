import pygame
import pickle
from random import randint
from screenBase import ScreenBase

class Score(ScreenBase):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        self.score = {}     #Guarda o nome e o score obtido por um jogador

        #Retorna erro se não tiver nada escrito no arquivo para carregar
        try:
            self.load_score()
        except:
            pass

    #Lógica do armazenamento e carregamento do score
    def add_score(self, name, new_score):
        self.score[name] = new_score

        #ordernar o dicionário por chave: vamos usar a função sorted com o parâmetro key (que recebe uma função que
        #deve retornar o que servirá para ordernar)
        #sorted precisa de uma lista para ordenar, por isso, usamos .items()
        #além disso, ele retorna uma lista, então, utilizamos a função disct para transformar em dicionário
        self.score = dict(sorted(self.score.items(), key=lambda player_score: player_score[1], reverse=True))

        with open("Scores/score.txt", 'wb') as data:
            pickle.dump(self.score, data)

    def load_score(self):
        with open('Scores/score.txt', 'rb') as data:
            self.score = pickle.load(data)

    def clear_score(self):
        with open("Scores/score.txt", 'wb') as data:
            pass

    #Lógica da tela
    def show_score(self):
        if self.score:  #tratamento de erro: se tiver score para ser mostrado
            start_position = pygame.Vector2(0,0)    #utilizamos vetor para ser mais claro ao acessarmos a posição x e y
            last_score = 10 if len(self.score) > 10 else len(self.score)    #carregamos apenas os 10 maiores scores (primeiros 10 no dicionário)

            for i in range(0, last_score):
                current_name = list(self.score.keys())[i]
                start_position.x = self.screen_width/6 if i < 5 else self.screen_width*3/5      #Fazendo duas colunas para o score
                start_position.y = self.v_unit*(i%5) + (self.title_rect.centery + 2*self.v_unit)

                current_score_surface = self.menu_font.render(f'{i+1}. {current_name}: {round(self.score[current_name], 4)}', False, 'white')

                self.screen.blit(current_score_surface, start_position)

    def make_title_score(self):
        self.title_rect.x = 0
        self.screen.blit(self.title_screen, self.title_rect)

        score_text_font = pygame.font.Font("Space-invaders-main/font/8-bit Arcade In.ttf", 160)
        score_text = score_text_font.render("HIGH SCORES", False, 'red')
        score_text_rect = score_text.get_rect(midleft = (self.title_rect.right + self.title_rect.centerx/2, self.title_rect.centery))

        self.screen.blit(score_text, score_text_rect)

    def update(self):
        self.show_score()
        self.make_title_score()
