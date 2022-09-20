import pygame


class Background:
    """ Essa classe representa a tela de fundo do jogo"""

    def __init__(self, width, heigth, path_image="../sprites/backgrounds/forest_game_background.jpg"):
        """ Construtor do plano de fundo do jogo
            Parâmetros:
                path_image -> Caminho para a imagem de fundo
                width       -> Largura da imagem
                height      -> Altura da imagem """

        self.image = pygame.image.load(path_image)
        self.width = width
        self.height = heigth
        self.image = pygame.transform.scale(self.image, [self.width, self.height]).convert_alpha()
