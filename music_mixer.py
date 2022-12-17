import pygame

class Mixer():
    def __init__(self):
        self.background_delay_time = {} #Define o delay (fade) para cada som de background
        self.current_background_playing = 0

        #Diferentes canais de aúdio, pois, caso mandemos tocar no mesmo canal de aúdio um som será parado para o outro tocar
        #Temos dois canais para sfx pois aúdios que tocam o tempo inteiro, como o do tiro da nave, podem impedir outros
        #sfx de tocarem, caso estejam no mesmo canal
        self.background_channel = pygame.mixer.Channel(0); self.background_channel.set_volume(0.5)
        self.sfx_channel_1 = pygame.mixer.Channel(1); self.sfx_channel_1.set_volume(0.5)
        self.sfx_channel_2 = pygame.mixer.Channel(2); self.sfx_channel_2.set_volume(0.5)    #canal dedicado para o som de tiro da nave
        self.menu_channel = pygame.mixer.Channel(3); self.menu_channel.set_volume(0.5)
        self.channel_list = [self.background_channel, self.sfx_channel_1, self.sfx_channel_2, self.menu_channel]

        #Armazenamento dos sons
        # Cada som é adicionado com um nome para nos referirmos ao momento do jogo em que ele será executado
        self.background_songs = {}
        self.sfx_songs = {}
        self.menu_songs = {}

        #volume de cada canal
        self.music_volume = 0
        self.sfx_volume = 0
        self.menu_volume = 0
        self.muted = False

        #Carregamento de todos os sons usados
        self.load_all_music()
        self.load_all_sfx()
        self.load_all_menu()

    #Carregando todos os sons. O volume de cada som é definido como 0.5 (ou seja, todos eles começam em 50%, como é no
    #menu de música) + o referente valor do volume. Como começa em 50, pode subtrair até 0 ou somar até 100.
    #Dependendo da sua função cada som tem seu tempo de fade-in
    def load_all_music(self):
        self.load_background_song("menu", "Space-invaders-main/audio/menu_music.wav", 0.5 + self.music_volume, 500)
        self.load_background_song("game", "Space-invaders-main/audio/game_music.wav", 0.5 + self.music_volume, 1000)
        self.load_background_song("console", "Space-invaders-main/audio/game_music.wav", 0, 1000)
        self.load_background_song("score", "Space-invaders-main/audio/menu_music.wav", 0.5 + self.music_volume)
        self.load_background_song("music", "Space-invaders-main/audio/menu_music.wav", 0.5 + self.music_volume)
        self.load_background_song("end", "Space-invaders-main/audio/end.wav", 0.5 + self.music_volume, 10000)
        self.load_background_song("victory", "Space-invaders-main/audio/victory-background.wav",
                                  0.8 + self.music_volume, 17000)

    def load_all_sfx(self):
        self.load_sfx("explosion", "Space-invaders-main/audio/explosion.wav", 0.5 + self.sfx_volume)
        self.load_sfx("laser", "Space-invaders-main/audio/laser.wav", 0.5 + self.sfx_volume)
        self.load_sfx("victory", "Space-invaders-main/audio/victory.wav", 0.5 + self.sfx_volume)
        self.load_sfx("game_over", "Space-invaders-main/audio/game-over.wav", 0.5 + self.sfx_volume)

    def load_all_menu(self):
        self.load_menu_sound("switch", "Space-invaders-main/audio/menu.wav", 0.5+self.menu_volume)
        self.load_menu_sound("select", "Space-invaders-main/audio/confirm.wav", 0.5+self.menu_volume)
        self.load_menu_sound("game_start", "Space-invaders-main/audio/game-start.wav", 0.5+self.menu_volume)


    #Load
    def load_background_song(self, name, path, volume = 1, delay_time = -1):
        """Apenas armazena nos respectivos dicionários o som passado e define seu volume"""
        self.background_delay_time[name] = delay_time

        self.background_songs[name] = pygame.mixer.Sound(path)
        self.background_songs[name].set_volume(volume)

    def load_sfx(self, name, path, volume=1):
        self.sfx_songs[name] = pygame.mixer.Sound(path)
        self.sfx_songs[name].set_volume(volume)

    def load_menu_sound(self, name, path, volume=1):
        self.menu_songs[name] = pygame.mixer.Sound(path)
        self.menu_songs[name].set_volume(volume)


    #Play
    def play_background(self, game_state):
        if game_state != self.current_background_playing:
            #parar de tocar o antigo background quando trocar
            if self.current_background_playing != 0:
                self.background_songs[self.current_background_playing].stop()

            self.background_channel.play(self.background_songs[game_state], loops=-1, fade_ms=self.background_delay_time[game_state])
            self.current_background_playing = game_state

    def play_sfx(self, sfx, channel=1):
        """Utilizar canal 2 para sfx que estão o tempo inteiro tocando, como o tiro do jogador, e o canal 1 para sfx
        esporádicos, que não entraram um em cima do otro. """
        if channel==1:
            self.sfx_channel_1.play(self.sfx_songs[sfx])
        else:
            self.sfx_channel_2.play(self.sfx_songs[sfx])

    def play_menu_sounds(self, song):
        self.menu_channel.play(self.menu_songs[song])


    #Volume Control
    #A atualização da lista de volumes vem de funções presentes na classe que controla a tela de música no menu
    def update_volume(self, list_of_volumes):
        self.music_volume, self.sfx_volume, self.menu_volume = list_of_volumes
        self.background_channel.set_volume(0.5 + self.music_volume)
        self.sfx_channel_1.set_volume(0.5 + self.sfx_volume)
        self.sfx_channel_2.set_volume(0.5 + self.sfx_volume)
        self.menu_channel.set_volume(0.5 + self.menu_volume)

    def get_list_of_values(self):
        return [self.music_volume, self.sfx_volume, self.menu_volume]

    def mute(self):
        if not self.muted:
            self.background_channel.set_volume(0)
            self.sfx_channel_1.set_volume(0)
            self.sfx_channel_2.set_volume(0)
            self.menu_channel.set_volume(0)
            self.muted = True
        else:
            self.update_volume([self.music_volume, self.sfx_volume, self.menu_volume])
            self.muted = False

    def mute_channel(self, channel):
        if self.channel_list[channel].get_volume() == 0:
            self.update_volume([self.music_volume, self.sfx_volume, self.menu_volume])
        else:
            self.channel_list[channel].set_volume(0)

