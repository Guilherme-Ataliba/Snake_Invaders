import pygame
from laser import Laser
from music_mixer import Mixer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, speed=10):
        super().__init__()
        self.image = pygame.image.load("Space-invaders-main/graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.mixer = Mixer()

        #Player Movement
        self.player_speed = speed
        self.screen_width = screen[0]
        self.screen_height = screen[1]

        #Shooting and power-ups
        self.shoot_ready = True
        self.last_shot_time = 0
        self.shoot_cooldown = 400
        self.shoot_amount = 1
        self.shoot_piercing = 1
        self.laser_size = 4
        self.laser_shilded = False

        self.lasers = pygame.sprite.Group()
        self.player_laser_speed =  -8

        #Player iframes
        self.collision_on = True
        self.godmode = False
        self.iframes_time = 50
        self.collision_timer = 50

        #Cheats
        self.last_shoot_cooldown = 0

    #Player Basics
    """Clássico bug dos jogos, se você apertar para ir na diagonal ele soma a velocidade e anda com 2x"""
    def get_input(self):
        keys = pygame.key.get_pressed()
        movement_keys = [keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]

        #Resolvendo o bug clássico. Caso duas teclas (de movimento) ou mais forem apertadas, a velocidade é reduzida (diagonal)
        if movement_keys.count(True) > 1:    mov_speed = self.player_speed/1.6
        else:   mov_speed = self.player_speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= mov_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += mov_speed
        if keys[pygame.K_UP]:
            self.rect.y -= mov_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += mov_speed
        if keys[pygame.K_SPACE] and self.shoot_ready:
            self.shoot_laser()
            self.last_shot_time = pygame.time.get_ticks()   #Esse armazena o tempo quando atira
            self.shoot_ready = False

    def constrain_player(self):
        if self.rect.right < 0:
            self.rect.left = self.screen_width
        if self.rect.left > self.screen_width:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def shoot_recharge(self):
        if pygame.time.get_ticks() - self.last_shot_time >= self.shoot_cooldown:    #Esse verifica o tempo todo tick
            self.shoot_ready = True

    def shoot_laser(self):
        for _ in range(self.shoot_piercing):
            if self.shoot_amount == 1:
                self.lasers.add(Laser(self.rect.center, self.player_laser_speed, (self.screen_width, self.screen_height), self.laser_size))
            elif self.shoot_amount == 2:
                offset = 10 + self.laser_size
                self.lasers.add(Laser((self.rect.centerx - offset, self.rect.centery), self.player_laser_speed, (self.screen_width, self.screen_height), self.laser_size))
                self.lasers.add(Laser((self.rect.centerx + offset, self.rect.centery), self.player_laser_speed, (self.screen_width, self.screen_height), self.laser_size))
            elif self.shoot_amount == 3:
                offset = 20 + self.laser_size
                self.lasers.add(Laser((self.rect.centerx - offset, self.rect.centery), self.player_laser_speed,
                                      (self.screen_width, self.screen_height), self.laser_size))
                self.lasers.add(Laser((self.rect.centerx, self.rect.centery-offset), self.player_laser_speed,
                                      (self.screen_width, self.screen_height), self.laser_size))
                self.lasers.add(Laser((self.rect.centerx + offset, self.rect.centery), self.player_laser_speed,
                                      (self.screen_width, self.screen_height), self.laser_size))

        self.mixer.play_sfx("laser", 2)

    #Upgrades
    def get_shoot_amount(self):
        return self.shoot_amount

    def set_shoot_amount(self, new_shoot_amount):
        if new_shoot_amount not in [1, 2, 3]:
            return ValueNotAccepted
        else:
            self.shoot_amount = new_shoot_amount

    def get_shoot_piercing(self):
        return self.shoot_piercing

    def set_shoot_piercing(self, new_piercing_value):
        self.shoot_piercing = new_piercing_value

    def get_laser_size(self):
        return self.laser_size

    def set_laser_size(self, new_laser_size):
        self.laser_size = new_laser_size

    def change_shoot_cooldown(self, new_cooldow):   #setter
        self.shoot_cooldown = new_cooldow

    def get_player_shoot_cooldown(self):
        return self.shoot_cooldown

    def update_player_size(self, times):
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/times, self.image.get_height()/times))
        self.rect = self.image.get_rect(center = self.rect.center)

    def get_laser_shilded(self):
        return self.laser_shilded

    def set_laser_shilded(self, value):
        self.laser_shilded = value

    #Iframes
    def get_hit(self):
        if self.collision_on:
            self.collision_on = False

    def iframes(self):
        if not self.collision_on and self.godmode == False:
            self.collision_timer -= 1
            if self.collision_timer <= 0:
                self.collision_on = True
                self.collision_timer = self.iframes_time

    #Cheats
    def get_collision_on(self):
        return self.collision_on

    def switch_collision_on(self):
        if self.collision_on:
            self.collision_on = False
            self.godmode = True
        else:
            self.collision_on = True
            self.godmode = False


    def no_cooldown(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.last_shoot_cooldown
        else:
            self.last_shoot_cooldown = self.shoot_cooldown
            self.shoot_cooldown = 0
        self.mixer.mute_channel(2)

    #Sobrecarga do método já definido na classe pygame.sprite.Srite
    def update(self):
        self.get_input()
        self.constrain_player()
        self.shoot_recharge()
        self.lasers.update()
        self.iframes()