import pygame

class ScreenBase():
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.v_unit = screen_height/10
        self.h_unit = screen_width/30

        self.small_menu_font = pygame.font.Font("Space-invaders-main/font/Pixeled.ttf", 15)
        self.menu_font = pygame.font.Font("Space-invaders-main/font/Pixeled.ttf", 25)
        self.big_menu_font = pygame.font.Font("Space-invaders-main/font/Pixeled.ttf", 40)

        # Title screen
        self.title_screen = pygame.image.load("Space-invaders-main/graphics/title_screen2-cut.png").convert_alpha()
        self.title_screen = pygame.transform.scale(self.title_screen, (self.screen_width / 3, self.screen_height / 4 * 1.1))
        self.title_rect = self.title_screen.get_rect(center=(self.screen_width / 2, self.screen_height / 5))


class Gifs(ScreenBase):
    def __init__(self, screen, screen_width, screen_height, number_images, path, extension, scale=True):
        super().__init__(screen, screen_width, screen_height)
        self.number_images = number_images
        self.path = path
        self.extension = extension

        if scale: scale = (self.screen_width, self.screen_height)   #Se não passar nada, escala para tela inteira
        self.scale = scale

        self.images = []
        self.current_image = 0
        self.buffer = 0
        self.load_gif()
        self.fade_timer = 0

    def load_gif(self):
        for i in range(self.number_images):
            image_path = self.path + str(i) + self.extension
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.images.append(pygame.transform.scale(loaded_image, self.scale))

    def play_gifs(self, pos=(0,0), speed = 1, fade=False):
        if fade != False:
            if self.fade_timer < 255:
                self.fade_timer += fade
            self.images[self.current_image].set_alpha(self.fade_timer)

        self.screen.blit(self.images[self.current_image], pos)

        #O buffer é necessário pois só podemos passar valores inteiros para a atual imagem. Assim, ele acumula o valor da
        #velocidade de execução do gif, até que esse atinja um número maior que um, nesse caso, passamos para a próxima
        #imagem e reduzimos o valor do buffer em 1 (assim ainda sobre um pouco do valores decimais que estavam guardados
        #no buffer. Além disso, usamos a ideia de um contador com o resto da divisão.
        self.buffer += speed
        if self.buffer >= 1:
            iteration = int(self.buffer)
            self.buffer -= 1
            self.current_image = (self.current_image + iteration)%self.number_images



