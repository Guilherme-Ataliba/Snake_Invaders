import pygame
from random import randint

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, extra_lives=0):
        super().__init__()
        file_path = "Space-invaders-main/graphics/" + color + ".png"
        self.image =pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.color = color

        if color == 'red': self.value = 100; self.health = 1+extra_lives
        elif color == 'green': self.value = 200; self.health = 2+extra_lives
        elif color == 'yellow': self.value = 300; self.health = 3+extra_lives

    def alien_original_movement(self, x_velocity):
        """Essa função faz apenas ele se mover para um lado, dado a velocidade. Na main, no método original_aliens_position_cheker,
         detectamos a colisão com as bordas da tela e alteramos o valor da velocidade em x, para faze-los andar par ao outro lado.
         Essa tipo verificação tem que ser feita na main, pois devemos alterar o valor da velocidade de todos os aliens na tela
         ao mesmo tempo"""
        self.rect.x += x_velocity

    def alien_get_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return 1    #se matar retorna 1
        else:
            return 0

    def update(self, x_velocity):
        self.alien_original_movement(x_velocity)

class ExtraAlien(pygame.sprite.Sprite): #Alien extra
    def __init__(self, x_pos, screen_width, velocity=3):
        super().__init__()
        self.screen_width = screen_width
        self.image = pygame.image.load("Space-invaders-main/graphics/extra.png").convert_alpha()
        self.speed = randint(velocity-2, velocity+2)
        self.y_pos = randint(10, 100)

        if x_pos > screen_width/2: #Para ele se mover para a esquerda, caso depois da metade da tela
            self.speed = -self.speed

        self.rect = self.image.get_rect(topleft = (x_pos, self.y_pos))

    def destroy(self):
        """Destroy os aliens caso estejam fora da tela, assim aliviamos o processamento do jogo"""
        if self.rect.right <= -1000 or self.rect.left >= self.screen_width+1000:
            self.kill()

    def update(self):
        self.rect.x += self.speed   #movimento dos aliens
        self.destroy()

class HorizontalAlien(ExtraAlien):
    """Como é subclasse de ExtraAlien não precisamos redifinir as funções"""
    def __init__(self, x_pos, screen_width, velocity, y_pos=650):
        super().__init__(x_pos, screen_width, velocity)
        self.image = pygame.image.load("Space-invaders-main/graphics/horizontal_alien.png").convert_alpha()
        self.y_pos = y_pos
        self.rect = self.image.get_rect(topleft = (x_pos, self.y_pos))
        self.speed = velocity

        if x_pos > screen_width/2:
            self.image = pygame.transform.rotate(self.image, 90)    #girando a imagem de acordo com a direção que ele viaja
            self.speed = -self.speed
        else:
            self.image = pygame.transform.rotate(self.image, -90)
