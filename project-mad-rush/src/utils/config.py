

class Configuration:
    """ Essa classe vai conter as configurações do jogo"""

    def __init__(self, width_window=1200, height_window=600, fps=15, game_speed=15):
        """ Construtor da classe Configuration
            Parâmetros:
                width_window -> largura da janela
                height_window -> altura da janela
                fps -> clock do jogo
                game_speed -> velocidade do jogo
        """
        self.width_window = width_window  # largura da janela
        self.height_window = height_window  # altura da janela
        self.fps = fps  # fps do jogo
        self.game_speed = game_speed    # velocidade do jogo
        self.incremento = 0.02
        self.game_loop = True  # loop do jogo
