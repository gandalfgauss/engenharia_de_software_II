import pygame.sprite


class Ground(pygame.sprite.Sprite):
    """Essa classe representa o chao do jogo"""

    def __init__(self, config, path_image="../sprites/grounds/ground2.png", x_pos=0, height=48, width=320):
        """ Contrutor do chao
            Parametros:
                path_image -> caminho para imagem do chao
                x_pos -> posicao x do chao
                height -> altura do chao
                width -> largura do chao
                config -> configurações do jogo"""

        pygame.sprite.Sprite.__init__(self)  # instanciar sprite

        self.x_pos = x_pos
        self.path_image = path_image
        self.config = config
        self.height = height
        self.width = width
        self.image = pygame.image.load(self.path_image).convert_alpha()  # atribuir imagem ao chao

        self.rect = self.image.get_rect()
        self.rect[0] = self.x_pos  # alterar x do chao
        self.rect[1] = self.config.height_window - self.height  # alterar y do chao

    def update(self, *args):
        """ Metodo que atualiza o chao"""
        self.rect[0] -= self.config.game_speed
