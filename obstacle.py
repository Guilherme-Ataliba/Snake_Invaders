"""A lógica dos obstáculos é:
Teremos uma "matriz" (lista com strings) que desenha a forma do obstáculo. Andaremos por toda a matriz e, se detectarmos
colisão,  mudamos o que está escrito naquela posição, X (desenha) vazio (não desenha).
Depois, basta andar pela "matriz", onde tem X nós colocamos um "bloco" (sprite). O obstáculo será feito de vários sprites"""

import pygame

"""Aqui apenas defimos a forma e criamos a classe base para os blocos que fomaram os obstáculos. A construção dos obstáculos
é implementada na classe game, nos métodos create_obstacle e create_multiple_obstacles"""

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'    xxxxxxxx',
'  xxxxxxxxxxxx',
' xxxxxxxxxxxxxx',
'xxxxxxxxxxxxxxxx',
'xxxxxxxxxxxxxxxx',
'xxxxxxxxxxxxxxxx',
'xxxx        xxxx',
'xxx          xxx']

