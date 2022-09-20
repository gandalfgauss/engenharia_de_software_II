
from src.classes.collectibles import Collectibles


class Shield(Collectibles):
    """ Classe que representa o escudo"""

    def __init__(self, xpos, ypos, config, path_image="../sprites/ collectibles/shield.png"):
        """ Construtor da classe Coins
                    Parametros:
                                xpos -> posicao em x da moeda
                                ypos -> posicao em y da moeda
                                ysize -> posicao em y do coletavel
                                path_image -> path para a imagem
                                config -> configurações do jogo """
        super().__init__(xpos, ypos, path_image, config, 40, 40, 10, 10)
