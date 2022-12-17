import pygame
from screenBase import ScreenBase
#Módulo criado para esse código com o intuíto de servir de base para a manipulação de elementos na tela

#Essa classe deve ser usada dentro de um event loop na main
"""Dicinários de inputs são uma ideia para relacionar uma entrada de usuário com uma função/método/ação do código
de forma mais simples. Eles se consistem em um dicionário em que as chaves são possíveis teclas / ações e os valores são as funções
a serem executadas caso essas teclas forem pressionadas. 

A lógica por traz da execução de tais dicionário foi aqui implementada. Functionality é um dicionário de inputs """

class Input(ScreenBase):
    def __init__(self, functionality=False, game_state=0, screen=False, screen_width=False, screen_height=False):

        self.accepted_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', '_', '0', '1',
                              '2', '3', '4', '5', '6', '7', '8', '9', '=', "'", ',', '[', ']', ';', '.']

        self.accepted_shift = {"'": '"', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '¨',
                               '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{',
                               ']': '}', ',': '<', '.': '>', ';': ':'}

        self.accepted_right_alt = {'q': '/'}

        self.typed_phrase = ''
        self.functionality = functionality
        self.game_state = game_state

        if self.functionality == False:
            super().__init__(screen, screen_width, screen_height)

    def type_input(self, event_key_down, function=False, limit=False):
        """Pega o que o player está digitando e transforma em uma frase, guardando-a dentro do atributo typed_phrase"""

        """Key_down precisa ser uma variável dentro de um event loop do tipo pygame.KEYDOWN"""
        character = pygame.key.name(event_key_down.key)
        left_shift, right_shit = pygame.key.get_pressed()[pygame.K_LSHIFT], pygame.key.get_pressed()[pygame.K_RSHIFT]
        right_alt = pygame.key.get_pressed()[pygame.K_RALT]

        #A ideia é que vamos adicionando ao final da string a letra digitada pela usuário. As funções abaixo se resumem
        #em captar essas entradas e verificar se alguma tecla de modificação foi ativada e se as letras equivalentes
        #estão dentro da lista de characteres permitidos. Caso tudo seja verdade, a letra é adicionado a typed_phrase

        # get special characters
        if left_shift or right_shit:
            if character in self.accepted_shift.keys():
                self.typed_phrase += self.accepted_shift[character]

            #Case Up Keys
            elif character in self.accepted_keys:   #Se não tiver nos caracters aceitos pelo shift, digita-se letra maiúscula (CAPS não funciona)
                self.typed_phrase += character.upper()

        elif right_alt:
            if character in self.accepted_right_alt.keys():
                self.typed_phrase += self.accepted_right_alt[character]

        else:
            if self.typed_phrase != '' and character == 'backspace':    #Função de deletar
                self.typed_phrase = self.typed_phrase[:-1]

            elif character == 'space':
                self.typed_phrase += ' '

            elif character in self.accepted_keys:
                self.typed_phrase += character

        # Estipula um limite para a quantidade de letras que podem ser inseridas na frase
        if limit != False:
            if len(self.typed_phrase) >= limit:
                self.typed_phrase = self.typed_phrase[:limit]

        """Caso o usuário aperte enter, o que foi digitado até então será passado como parâmetro de uma função opcional 
        que deve ser informada na chamada da função, assim, podemos implementar a chamada de funções como 
        (adicionar score, executar cheats). Pode-se passar uma única função, ou um dicionário de inputs"""

        if character == 'return':
            phrase = self.typed_phrase
            self.typed_phrase = ''

            #Se for passado uma função
            if type(function).__name__ in ['method', 'function']:
                if function != False:
                    function(phrase)

            #Se for passado um dicionário de funções
            elif type(function).__name__ == 'dict':
                if function != False:
                    try:
                        function[phrase]()
                    except KeyError: #Caso o valor digitado não esteja no dicionário
                        pass

    def show_and_get_typed(self, pos, text_color='white'):
        """Mostra na tela o que está sendo captado pelo método type_input"""

        """Um mesmo gerenciador de inputs não pode ser usado para mostrar informações na 
        tela e executar entrada do usuário por motivos de organização"""
        if self.functionality != False:
            raise Exception(FuncionalityAndGetTypeOnSameObject)
        else:
            current_text = self.menu_font.render(self.typed_phrase, False, text_color)
            self.screen.blit(current_text, pos)

    def check_execute_key(self, event_key_down, current_game_state = 0):
        """Gerencia a entrada de usuário para realizar funções dentro do jogo. Tal relação
        entre a tecla digitada e a função que será executada deve ser passada em um
        dicionário de inputs"""

        #Caso não tenha passado o dicionário de inputs esse código levantará um erro
        if self.functionality == False:
            raise Exception(NoFunctionalityAtributed)

        else:
            if current_game_state == 0 or current_game_state == self.game_state:

                if event_key_down.key in self.functionality.keys():
                    self.functionality[event_key_down.key]()


"""Type_input deve aser utilizado junto com show_and_get_typed para pegar o que o usuário
 digita e escrever na tela"""