import pygame
import random


class Collectibles(pygame.sprite.Sprite):
    """ Classe que representa a objetos colecionaveis """

    def __init__(self, xpos, ypos, path_image, config, width, heigth, width_colision=10, heigth_colison=10):
        """ Construtor da classe Coins
                    Parametros:
                                xpos -> posicao em x da moeda
                                ypos -> posicao em y da moeda
                                ysize -> posicao em y do coletavel
                                path_image -> path para a imagem
                                width -> largura do objeto
                                height -> altura do objeto
                                width_colision -> largura do objeto de colisao
                                height_colision -> altura do objeto de colisao
                                inf -> limite
                                config -> configurações do jogo """
        pygame.sprite.Sprite.__init__(self)

        self.path_image = path_image
        self.width = width
        self.heigth = heigth
        self.width_colision = width_colision
        self.heigth_colision = heigth_colison
        self.config = config
        self.image = pygame.image.load(path_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, [self.width, self.heigth])
        self.rect = pygame.Rect(xpos, ypos, self.width_colision, self.heigth_colision)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        """ Método que desloca o item na tela"""
        self.rect[0] -= self.config.game_speed
        # print('coin')

    def get_random(self, inf, sup, group, rarity):
        """ Esse método retorna um item em uma posição aleatória do cenário
            Parâmetros:
            sup -> limite superior que o item pode aparecer na tela
            inf -> limite inferior que o item pode aparecer na tela
            group -> grupo do item
            quantify -> quantidade de itens que serao gerados
            rarity ->raridade do item"""

        # E crio uma quantidade de 2x aletatorias
        if random.random() < rarity:
            xpos = self.config.width_window * random.uniform(1, 1.3)
            ypos = random.randint(inf, sup)
            new_item = Collectibles(xpos, ypos, self.path_image, self.config, self.width, self.heigth,
                                    self.width_colision, self.heigth_colision)
            group.add(new_item)

