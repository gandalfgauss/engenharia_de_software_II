from src.classes.collectibles import Collectibles

class Stone(Collectibles):
    """ Classe que representa o obstaculo Stone"""

    def __init__(self, xpos, ypos, config, path_image="../sprites/obstacles/stone.png"):
        """ Construtor da classe Coins
                    Parametros:
                                xpos -> posicao em x da moeda
                                ypos -> posicao em y da moeda
                                ysize -> posicao em y do coletavel
                                path_image -> path para a imagem
                                config -> configurações do jogo """
        super().__init__(xpos, ypos, path_image, config, 60, 60, 10, 10)
