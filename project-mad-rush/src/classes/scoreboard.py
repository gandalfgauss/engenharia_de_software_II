import pygame


class Scoreboard:
    """ Essa classe representa o placar do jogo"""

    def __init__(self, scoreboard_position, points_position):
        """ Esse é o contrutor da classe de pontuação
            Parâmetros:
                font -> fonte da Pontuação do jogo[
                pos  -> posição do contador na tela"""

        self.font = pygame.font.SysFont('Arial', 30)

        self.scoreboard_text = self.font.render('Placar', True, [255, 255, 255])
        self.scoreboard_position = scoreboard_position

        self.points = 0
        self.points_position = points_position
        self.points_text = self.font.render(f'{self.points}', True, [255, 255, 255])

    def add_point(self, x):
        """ Esse método adiciona uma quatidade x de pontos no placar"""
        self.points += x
        self.points_text = self.font.render(f'{self.points}', True, [255, 255, 255])

    def set_point(self, x):
        """ Esse método adiciona uma seta uma quantidade x de pontos no placar"""
        self.points = x
        self.points_text = self.font.render(f'{self.points}', True, [255, 255, 255])