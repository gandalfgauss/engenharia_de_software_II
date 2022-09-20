import pygame


class SpriteSheet:
    """ Essa classe repassa separa as sprites de uma imagem"""

    def __init__(self, image):
        """ Construtor da classe"""
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        """ Esse método obtem um frame de tamanho (width, height)
            escala o frame em scale vezes e coloca o fundo de uma cor (color)"""
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
