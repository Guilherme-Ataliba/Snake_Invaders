import sys
import pygame as py
import os
from player import Player
import obstacle
from alien import *
from random import choice, randint, sample
from laser import *
from menu import Menu
from score import Score
from screenBase import *
from music_mixer import Mixer
from end_screen import EndScreen
from get_input import Input
from crt import CRT
from background import *
from music_screen import *
from math import floor
import pygame

class Game():
    def __init__(self):
        #Player setup
        self.player_velocity = 7
        self.start_player()

        #Console
        self.start_console()

        #Lives
        self.lives_surface = self.player.sprite.image
        self.live_xstart_pos = screen_width - (self.lives_surface.get_size()[0] * 2 + 120)
        self.start_lives()

        #Score
        self.font = pygame.font.Font("Space-invaders-main/font/Pixeled.ttf", 15)
        self.start_score()
        self.start_score()

        #Obstacle setup
        self.obstacle_shape = obstacle.shape
        self.block_size = 8
        self.obstacle_amount = 5
        self.start_obstacle()

        # Wave setup
        self.wave = 1
        self.start_wave_menssanger()

        #Aliens setup
        self.aliens_xvelocity = 1
        self.aliens_yvelocity = 5
        self.alien_laser_velocity = 6
        self.alien_shoot_timer = 350
        self.alien_extra_lives = 0
        self.start_aliens()

        #Extra alien setup
        self.bonus_reduced_time = 0 #reduz o tempo de spawn conforme avançam as waves
        self.extra_alien_velocity = 3
        self.start_extra_alien()
        self.horizontal_alien_velocity = 8
        self.start_horizontal_alien()
        self.horizontal_alien_warning = Mensager(screen, screen_width, screen_height, 'Danger!', 'orange')

        #Game state
        self.game_state = 'menu'

        #Sfx and music
        self.mixer = Mixer()

        #Controladores
        self.menu = Menu(screen, screen_width, screen_height, 'white')
        self.score_manager = Score(screen, screen_width, screen_height)
        self.end_screen = EndScreen(screen, screen_width, screen_height)
        self.music_screen = MusicScreen(screen, screen_width, screen_height)

    #Player
    def hit_player(self):
        self.player_sprite.get_hit()
        self.lives -= 1
        self.mixer.play_sfx("explosion")

    #Obstacle Methods
    def create_obstacle(self, x_pos, y_pos, offset):
        """Essa classe cria os blocos necessários para forma *um obstáculo*, com base na shape informada. Calculando
        a posição (coordenada x e y) de cada bloco com base nos blocos à cima e à esquerda.
        O offset define o espaçamento entre os blocos"""
        for row_index, row in enumerate(self.obstacle_shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = col_index * self.block_size + x_pos + offset
                    y = row_index * self.block_size + y_pos
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.obstacles.add(block) #Tá aqui por causa dessa linha

    def create_multiple_obstacles(self, x_pos, y_pos, offset):
        """Essa função apenas chama a anterior, para criar um obstáculo, a quantidade de vezes definida pelo parâmetro
        obstacle_amount"""
        current_offset = 0
        for i in range(self.obstacle_amount):
            self.create_obstacle(x_pos, y_pos, current_offset)
            current_offset += offset

    #Alien and Wave Methods
    def original_aliens_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_start = 70, y_start = 100):
        """Serve como um construtor para os aliens. Cria a formação na qual eles aparecerão na tela"""

        """row must be greater than 6"""
        if rows < 6:
            raise Exception("TooFewRows")

        #Distribuindo a quantidade de rows
        yellow_number_rows = 1
        green_number_rows = 2
        red_number_rows = 3
        i=0
        for c in range(6, rows):
            if i == 0:
                red_number_rows += 1
            elif i == 1:
                green_number_rows += 1
            else:
                yellow_number_rows += 1
            i = (i+1)%3


        for row in range(rows):
            for col in range(cols):
                x = col * x_distance + x_start
                y = row * y_distance + y_start

                #devemos somar o número de amarelas ao número de verde para contar o quanto o contador já andou
                if row <= yellow_number_rows-1: alien_sprite = Alien('yellow', x, y, self.alien_extra_lives)
                elif yellow_number_rows <= row <= green_number_rows+yellow_number_rows-1: alien_sprite = Alien('green', x, y, self.alien_extra_lives)
                else: alien_sprite = Alien('red', x, y, self.alien_extra_lives)

                self.aliens.add(alien_sprite)

    def original_aliens_position_cheker(self):
        """Make the aliens bounce back of the wall"""
        if self.aliens.sprites():  # Para não ocorrer erro caso o jogador mate todos os aliens
            all_aliens = self.aliens.sprites()
            for alien in all_aliens:
                if alien.rect.right >= screen_width or alien.rect.left <= 0:    #Aliens bateram em uma das bordas da tela
                    self.aliens_xvelocity = -self.aliens_xvelocity
                    self.alien_move_down(self.aliens_yvelocity)
                    break

    def alien_move_down(self, y_distance):
        if self.aliens.sprites(): #Para não ocorrer erro caso o jogador mate todos os aliens
            for alien in self.aliens.sprites():
                alien.rect.y += y_distance

    def alien_shoot(self):
        all_aliens = self.aliens.sprites()
        if all_aliens:  # Para não ocorrer erro caso o jogador mate todos os aliens
            random_alien = choice(all_aliens)
            if self.wave == 1:
                random_laser = Laser(random_alien.rect.center, self.alien_laser_velocity,
                                                         (screen_width, screen_height))
            else:
                random_laser = choice(self.available_lasers)(random_alien.rect.center, self.alien_laser_velocity,
                                                         (screen_width, screen_height))
            self.alien_lasers.add(random_laser)

    def alien_pick_wave_lasers(self):
        #Sempre começa com o laser normal, essa função escolherá quais outros tipos de lasers entrarão
        all_laser = [LightningLaser, BigLaser, DiagonalLaser]
        self.available_lasers = sample(all_laser, self.wave-1) if self.wave <= 4 else sample(all_laser, 3)
        self.available_lasers.append(Laser)

    def set_difficulty_wave(self):
        self.aliens_xvelocity = 1 + 0.5*(self.wave-1)    #5 waves: 1, 1.5, 2, 2.5, 3
        self.aliens_yvelocity = 5 + 5*(self.wave-1)      #5 waves: 5, 10, 15, 20, 25
        self.alien_shoot_timer = 350 - 50*(self.wave-1)    #5 waves: 350, 300, 250, 200, 150
        self.alien_extra_lives =  0 + floor((self.wave-1)/2)    #5 waves: 0, 0, 1, 1, 2
        self.bonus_reduced_time = 0 + 100*(self.wave-1)     #5 waves: (400, 600), (300, 500), (200, 400), (100, 300), (0, 200)

    #Extra Aliens Methods - Está aqui para entrar no sprite group
    def extra_alien_spawn(self):
        self.extra_alien_timer -= 1
        if self.extra_alien_timer <= 0:
            #Escolha entre spawnar no lado direito ou esquerdo da tela
            #Quando adicionamos um novo sprite a um GroupSingle, sobrescrevemos o anterior
            self.extra_alien.add(ExtraAlien(choice([-10, screen_width+10]), screen_width, self.extra_alien_velocity))
            self.extra_alien_timer = randint(400-self.bonus_reduced_time, 600-self.bonus_reduced_time)

    def horizontal_alien_spawn(self):
        self.horizontal_alien_timer -= 1
        if self.horizontal_alien_timer <= 0:
            # Escolha entre spawnar no lado direito ou esquerdo da tela
            # Quando adicionamos um novo sprite a um GroupSingle, sobrescrevemos o anterior
            spawn_side = choice([-500, screen_width + 500])     #spawn on left or right
            spawn_height = randint(650, screen_height-40-80-5)        #spawn height (-enemy height - player height - margin)
            self.horizontal_alien.add(HorizontalAlien(spawn_side, screen_width,
                                                      self.horizontal_alien_velocity, y_pos = spawn_height))
            self.horizontal_alien_warning.load((0, spawn_height) if spawn_side == -500 else (screen_width-150, spawn_height), 50)
            self.horizontal_alien_timer = randint(400-self.bonus_reduced_time, 600-self.bonus_reduced_time)

    #Menu Methods
    def menu_options(self):
        option = self.menu.arrow_select()
        if option == 'start':
            game.game_state = 'game'
            self.start_time()
        elif option == 'score':
            game.game_state = 'score'
        elif option == 'music':
            game.game_state = 'music'
        else:
            pygame.quit()
            sys.exit()

    def increase_volume(self):
        self.mixer.update_volume(self.music_screen.increase_volume(self.mixer.get_list_of_values()))

    def decrease_volume(self):
        self.mixer.update_volume(self.music_screen.decrease_volume(self.mixer.get_list_of_values()))

    def menu_row_back(self):
        if self.game_state == 'score' or self.game_state == 'music':
            self.game_state = 'menu'
        self.mixer.play_menu_sounds('select')
        return self.game_state

    def call_add_score(self, name):
        self.score_manager.add_score(name, self.score)
        self.game_state = 'menu'
        self.start_game()
        self.start_score()

    #Start-Up Setup
    def start_player(self):
        self.player_sprite = Player((screen_width // 2, screen_height), (screen_width, screen_height),
                                    self.player_velocity)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

    def start_console(self):
        #Precisamos atualizar a lista de comando toda vez que recarregamos o jogo (passamos de wave), pois um novo jogador é criado
        # e precisamos acessar os métodos desse jogador. Caso apenas colocássemos uma vez, quando passasse de wave ou perdesse
        #e iniciasse denovo o jogador no jogo não mais seria o jogador no dicionário, pois o do dicionário já foi substituído
        self.console_input_dict = {'godmode': self.player_sprite.switch_collision_on,
                                   'nocooldown': self.player_sprite.no_cooldown,
                                   'nextwave': self.next_wave}

    def start_lives(self):
        self.lives = 3

    def start_score(self):
        self.score = 0

    def start_obstacle(self):
        self.obstacles = pygame.sprite.Group()
        self.create_multiple_obstacles(45, 550, screen_width / self.obstacle_amount)

    def start_aliens(self):
        self.set_difficulty_wave()
        self.aliens = pygame.sprite.Group()
        self.original_aliens_setup(8, 18)
        self.alien_lasers = pygame.sprite.Group()
        self.alien_pick_wave_lasers()

    def start_extra_alien(self):
        self.extra_alien = pygame.sprite.Group()
        self.extra_alien_timer = randint(400-self.bonus_reduced_time, 600-self.bonus_reduced_time)
        self.spawn_extra = True

    def start_horizontal_alien(self):
        self.horizontal_alien = pygame.sprite.Group()
        self.horizontal_alien_timer = randint(400-self.bonus_reduced_time, 600-self.bonus_reduced_time)
        self.spawn_extra = True

    def start_time(self):
        self.inicial_time = pygame.time.get_ticks()

    def start_wave_menssanger(self):
        self.wave_messanger = Mensager(screen, screen_width, screen_height, f"Wave: {self.wave}", '#f5ce42')
        self.wave_messanger.load((screen_width / 2-80, 20), 100)

    def start_game(self):
        self.start_player()
        self.start_lives()
        self.start_obstacle()
        self.start_aliens()
        self.start_extra_alien()
        self.start_horizontal_alien()
        self.start_time()
        self.start_console()
        self.start_wave_menssanger()
        #Resolvendo problema do aúdio voltar ao padrão depois de uma wave
        self.mixer.update_volume(self.music_screen.get_volume_list())

    #Score
    def show_current_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, (200, 200, 200))
        score_rect = score_surface.get_rect(topleft=(15, -5))
        screen.blit(score_surface, score_rect)

    def decrement_score_time(self):
        self.score -= (pygame.time.get_ticks() - self.inicial_time)/100
        if self.score < 0:
            self.score = 0

    #Power Ups
    def pick_random_power_up(self):
        power_ups = [self.multiply_player_shoot_spped, self.increase_shoot_amount, self.increase_shoot_amount,
                     self.increase_shoot_amount, self.increase_shoot_amount, self.increase_shoot_piercing,
                     self.multiply_laser_size, self.player_size_down, self.shilded_tears_on]
        choice(power_ups)()

    def multiply_player_shoot_spped(self, times = 2):
        self.player_sprite.change_shoot_cooldown(self.player_sprite.get_player_shoot_cooldown()/times)

    def increase_shoot_amount(self):
        if self.player_sprite.get_shoot_amount() == 3:
            self.pick_random_power_up()
        else:
            self.player_sprite.set_shoot_amount(self.player_sprite.get_shoot_amount()+1)

    def increase_shoot_piercing(self):
        #Faz com que os tiros do jogador penetrem inimigos
        self.player_sprite.set_shoot_piercing(self.player_sprite.get_shoot_piercing()+1)

    def multiply_laser_size(self, times = 2):
        self.player_sprite.set_laser_size(self.player_sprite.get_laser_size()*2)

    def player_size_down(self, times = 1.5):
        self.player_sprite.update_player_size(times)

    def shilded_tears_on(self):
        #Faz com que os tiros do jogador destruam os tiros inimigos
        if self.player_sprite.get_laser_shilded():
            self.pick_random_power_up()
        else:
            self.player_sprite.set_laser_shilded(True)

    #General Methods
    def collisions(self):

        #Player lasers
        player_lasers = self.player.sprite.lasers
        if player_lasers:   #Verificando se tem laser na tela
            for laser in player_lasers:
                #Obstacle collisions
                #Bug de detectar dois quadrados do meio ao mesmo tempo. Para resolver, obrigamos a deletar apenas
                #um elemento da lista de colisões. O primeiro elemento colidido está na última posição da lista
                collided_with = pygame.sprite.spritecollide(laser, self.obstacles, False)
                if collided_with:
                    collided_with[len(collided_with)-1].kill()
                    laser.kill()

                #Alien collisions
                #O tiro do player pode colidir com mais de um alien ao mesmo tempo
                collided_with = pygame.sprite.spritecollide(laser, self.aliens, False)
                if collided_with:
                    if collided_with[len(collided_with)-1].alien_get_hit():
                        self.score += collided_with[len(collided_with)-1].value
                    laser.kill()

                #Extra Alien and Horizontal Alien collisions
                if pygame.sprite.spritecollide(laser, self.extra_alien, True) or pygame.sprite.spritecollide(laser, self.horizontal_alien, True):
                    self.score += 500 #Pontos recebidos pela Extra Alien
                    self.pick_random_power_up()
                    laser.kill()

                #Alien lasers
                if self.player_sprite.get_laser_shilded():
                    collided_with = pygame.sprite.spritecollide(laser, self.alien_lasers, False)
                    if collided_with:
                        self.score += 10
                        collided_with[len(collided_with)-1].kill()
                        laser.kill()

        #Alien lasers
        alien_lasers = self.alien_lasers
        if alien_lasers:
            for laser in alien_lasers:
                # Obstacle collisions
                collided_with = pygame.sprite.spritecollide(laser, self.obstacles, False)
                if collided_with:
                    if isinstance(laser, BigLaser): #lasers grandes destroem mais blocos
                        for obstacle in collided_with:
                            obstacle.kill()
                    else:
                        collided_with[len(collided_with) - 1].kill()
                    laser.kill()

                # Player collisions
                if self.player_sprite.get_collision_on():
                    if pygame.sprite.spritecollide(laser, self.player, False):
                        laser.kill()
                        self.hit_player()

        #Aliens
        if self.aliens:
            for alien in self.aliens:
                #Obstacle collisions
                pygame.sprite.spritecollide(alien, self.obstacles, True)

                #Player collisions
                if self.player_sprite.get_collision_on():
                    if pygame.sprite.spritecollide(alien, self.player, True):
                        self.lives = 0

                #Out of screen
                if alien.rect.bottom >= screen_height:
                    self.lives = 0

        #Horizontal Aliens
        if self.horizontal_alien:
            for alien in self.horizontal_alien:

                #player collisions
                if self.player_sprite.get_collision_on():
                    if pygame.sprite.spritecollide(alien, self.player, False):
                        self.hit_player()

    def show_lives(self):
        #Mostramos apenas 2, 1, 0 vidas na tela superior
        for live in range(self.lives):
            x = self.live_xstart_pos + live * (self.lives_surface.get_size()[0] + 10)
            screen.blit(self.lives_surface, (x, 8))

    def end_game(self):
        if self.lives <= 0:
            self.game_state = 'end'
            self.decrement_score_time()
            self.wave = 1
            self.mixer.play_sfx("game_over")

    def detect_victory(self):
        if self.wave > 5:
            self.spawn_extra = False
            self.game_state = 'victory'
            self.decrement_score_time()
            self.score *= self.lives
            self.mixer.play_sfx('victory')
            self.wave = 1
        elif not self.aliens.sprites():
            self.wave += 1
            self.score *= self.lives
            self.start_game()

    def next_wave(self):
        self.aliens.empty()

    def stop_game(self):
        py.quit()
        sys.exit()

    #Executará o jogo (atualizar e desenhar sprites)
    def run(self):
        #Player execution
        self.player.draw(screen)
        self.player.update()
        self.player.sprite.lasers.draw(screen)

        #Obstacle execution
        self.obstacles.draw(screen)

        #Alien execution
        self.aliens.draw(screen)
        self.original_aliens_position_cheker()
        self.aliens.update(self.aliens_xvelocity)

        self.alien_lasers.draw(screen)
        self.alien_lasers.update()

        #Extra Alien execution
        if self.spawn_extra:
            self.extra_alien_spawn()
            self.extra_alien.update()
            self.extra_alien.draw(screen)
            self.horizontal_alien_spawn()
            self.horizontal_alien.update()
            self.horizontal_alien.draw(screen)

        #Score executions
        self.show_current_score()

        #General executions
        self.collisions()
        self.show_lives()
        self.end_game()
        self.detect_victory()

#Para garantir que apenas a main será exectada, quando trabalhando com vários arquivos
if __name__ == '__main__':

    #Centraliza a janela do pygame na tela, ativando a função SDL_VIDEO_CENTERED no dicionário do os.eviron
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    #Definições Básicas e Inicialização
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    py.init()
    clock = py.time.Clock()
    # screen_width = 1500 #1500
    # screen_height = 850 #850

    #Pegando informações da atual tela
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    screen = py.display.set_mode((screen_width, screen_height), pygame.NOFRAME) #Adicionar parâmetro pygame.NOFRAME para borderless

    #Objetos
    game = Game()
    crt = CRT(screen, screen_width, screen_height)
    background_manager = Background(screen, screen_width, screen_height)
    score_input_manager = Input(screen = screen, screen_width = screen_width, screen_height = screen_height)


    #Console
    console_input_manager = Input(screen = screen, screen_width = screen_width, screen_height = screen_height)

    #BUG DO CONSOLE E PLAYER
    #console_input_dict = {'godmode': game.player_sprite.switch_collision_on, 'nocooldown': game.player_sprite.no_cooldown}

    console_background_rect = pygame.Rect(0, 0, 500, 120)
    console_font = pygame.font.Font("Space-invaders-main/font/pixelated.ttf", 40)
    console_background_text = console_font.render(">", False, 'green').convert_alpha()

    #Inputs
    menu_input_dict = {pygame.K_UP: game.menu.arrow_up, pygame.K_DOWN: game.menu.arrow_down,
                       pygame.K_SPACE: game.menu_options, pygame.K_ESCAPE: game.stop_game}
    menu_inputs = Input(menu_input_dict, 'menu')

    score_input_dict = {pygame.K_ESCAPE: game.menu_row_back}
    score_inputs = Input(score_input_dict, 'score')

    music_menu_dict = {pygame.K_UP: game.music_screen.arrow_up, pygame.K_DOWN: game.music_screen.arrow_down,
                       pygame.K_RIGHT: game.increase_volume, pygame.K_LEFT: game.decrease_volume,
                       pygame.K_ESCAPE: game.menu_row_back}
    music_menu_inputs = Input(music_menu_dict, 'music')

    #Timers
    ALIEN_LASER_TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER_TIMER, game.alien_shoot_timer)

    #Main Game Loop
    while True:

        #Event Loop
        for event in pygame.event.get():
            #Fechar a janela
            if event.type == py.QUIT:
                game.stop_game()

            #Timers
            if game.game_state == 'game':
                if event.type == ALIEN_LASER_TIMER:
                    game.alien_shoot()

            # Inputs
            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_QUOTE:
                    if game.game_state == 'game':
                        game.game_state = 'console'
                    elif game.game_state == 'console':
                        game.game_state = 'game'
                else:
                    #Colocamos esse else para garantir que a aspas usada para abrir o console não seja
                    # contada como um caractere digitado pelo usuário
                    if game.game_state == 'console':
                        if event.key == pygame.K_1:
                            game.player_sprite.no_cooldown()

                        console_input_manager.type_input(event, game.console_input_dict, 15)

                menu_inputs.check_execute_key(event, game.game_state)
                score_inputs.check_execute_key(event, game.game_state)
                music_menu_inputs.check_execute_key(event, game.game_state)

                #Da conflito ao digitar m na tela e usar m para mutar o jogo
                if event.key == pygame.K_m and game.game_state not in ['end', 'victory', 'console']:
                    game.mixer.mute()

                #game states em que se é permitido pegar entrada do usuário
                if game.game_state in ['end', 'victory']:
                    score_input_manager.type_input(event, game.call_add_score, 3)

        #Game screen
        if game.game_state == 'game':
            #screen.fill((30, 30, 30))
            background_manager.draw_gif_background('game', 0.05)
            game.horizontal_alien_warning.draw()
            game.run()
            game.wave_messanger.draw()

        # Console Screen
        elif game.game_state == 'console':
            pygame.draw.rect(screen, 'black', console_background_rect)
            screen.blit(console_background_text, (0,70))
            console_input_manager.show_and_get_typed((50, 50), text_color='green')

        #Menu screen
        elif game.game_state == 'menu':
            background_manager.draw_background('menu')
            game.menu.update()

        #Score screen
        elif game.game_state == 'score':
            background_manager.draw_gif_background('game', 0.1)
            game.score_manager.update()

        #Music screen
        elif game.game_state == 'music':
            background_manager.draw_gif_background('game', 0.1)
            game.music_screen.update()

        #End screen
        elif game.game_state == 'end':
            game.end_screen.death_screen_draw(game.score)
            score_input_manager.show_and_get_typed(game.end_screen.get_score_rect(), text_color='#f4d346')

        #Victory screen
        elif game.game_state == 'victory':
            game.end_screen.victory_screen_draw(game.score)
            score_input_manager.show_and_get_typed(game.end_screen.get_score_rect(), text_color='#f4d346')

        # General screens
        game.mixer.play_background(game.game_state)
        crt.draw()

        py.display.update()     #Atualiza a janela do jogo
        clock.tick(60)      #Limita o númeor de frames (velocidade) que o jogo roda

