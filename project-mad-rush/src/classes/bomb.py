from src.classes.collectibles import Collectibles


class Bomb(Collectibles):
    """ Classe representa a bomba do jogo"""

    def __init__(self, xpos, ypos, config, path_image="../sprites/obstacles/bomb.png"):
        """ Construtor da classe bomb
            Parametros:
                        xpos -> posicao em x do obstaculo
                        ypos -> posicao em y do obstaculo
                        path_image -> path para a imagem
                        config -> configurações do jogo"""

        super().__init__(xpos, ypos, path_image, config, 50, 50, 10, 10)
