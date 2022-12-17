import pygame
from random import randint, choice

#Laser Base
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, screen, laser_size = 4):
        super().__init__()
        self.image = pygame.Surface((laser_size-2, laser_size+15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.laser_speed = velocity

        #Screen - Laser Movement
        self.screen_width = screen[0]
        self.screen_height = screen[1]

    def laser_move(self):
        self.rect.y += self.laser_speed

    def destroy(self):
        "Destroy o objeto quando fora da tela, para otimizar o jogo"
        if self.rect.bottom < 0 or self.rect.top > self.screen_height:
            self.kill()

    def update(self):
        self.laser_move()
        self.destroy()

#Diferentes tipos de Lasers que herdam da classe mãe.
class LightningLaser(Laser):
    def __init__(self, pos, velocity, screen, laser_size = 4):
        super().__init__(pos, velocity, screen, laser_size)
        self.image = pygame.image.load("Space-invaders-main/graphics/lightning_laser.png").convert_alpha()
        self.laser_speed = 1.5*velocity

class BigLaser(Laser):
    def __init__(self, pos, velocity, screen, laser_size = 4):
        super().__init__(pos, velocity, screen, laser_size)
        self.image = pygame.Surface((randint(3, 5)*laser_size, 10*laser_size))
        self.image.fill('white')
        self.laser_speed = 0.5*velocity

class DiagonalLaser(Laser):
    def __init__(self, pos, velocity, screen, laser_size = 4):
        super().__init__(pos, velocity, screen, laser_size)
        #A divisão por screen[y] = screen_height - pos[1] = posição vertical do spawn do laser serve para regular a
        #velocidade horizontal de laser mais alto e mais baixo na tela. *200 é fator de escala
        self.laser_direction = choice([-1,1])/(screen[1]-pos[1])*200

    #Aqui fazemos uma sobrecarga do método laser_move, pois esse laser se move de forma diferente
    def laser_move(self):
        self.rect.y += self.laser_speed*0.6
        self.rect.x += self.laser_direction*self.laser_speed*0.6