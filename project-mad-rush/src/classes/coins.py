
from src.classes.collectibles import Collectibles


class Coins(Collectibles):
    """ Classe que representa a moeda"""

    def __init__(self, xpos, ypos, config, path_image="../sprites/ collectibles/coin.png"):
        """ Construtor da classe Coins
                    Parametros:
                                xpos -> posicao em x da moeda
                                ypos -> posicao em y da moeda
                                ysize -> posicao em y do coletavel
                                path_image -> path para a imagem
                                config -> configurações do jogo """
        super().__init__(xpos, ypos, path_image, config, 20, 20, 10, 10)

