import pygame
from classes.game import Game
from utils.config import Configuration

from src.classes.player import Player1
from src.classes.player import Player2
from src.classes.ground import Ground
from src.classes.background import Background

if __name__ == "__main__":
    loop = True
    while loop:

        pygame.init()  # inicializa pygame
        pygame.display.set_caption("Mad Rush")  # inserir titulo da janela do jogo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                pygame.quit()
                loop = False
        # Criar as configurações do jogo

        configuracoes = Configuration()

        # criar jogo infinite runner, a sua janela e o seu nome
        mad_rush = Game(config=configuracoes)

        mad_rush.cria_chao(Ground(config=mad_rush.config))  # criando grupo do chao do jogo

        mad_rush.cria_background(Background(width=mad_rush.config.width_window,
                                            heigth=mad_rush.config.height_window))

        mad_rush.criar_players(Player1(path_image_run="../sprites/players_sprites/player1_sprites/Biker_run.png",
                                       n_images_run=6, width=48, height=48, config=mad_rush.config,
                                       ground=mad_rush.ground, n_images_jump=6,
                                       path_image_jump="../sprites/players_sprites/player1_sprites/Biker_doublejump.png",
                                       n_images_hurt=2,
                                       path_image_hurt="../sprites/players_sprites/player1_sprites/Biker_hurt.png"))  # criar grupo de player e adicionar no PlayerGroup do pygame

        mad_rush.criar_players(Player2(path_image_run="../sprites/players_sprites/player2_sprites/Punk_run.png",
                                       n_images_run=6, width=48, height=48, config=mad_rush.config,
                                       ground=mad_rush.ground, n_images_jump=6,
                                       path_image_jump="../sprites/players_sprites/player2_sprites/Punk_doublejump.png",
                                       n_images_hurt=2,
                                       path_image_hurt="../sprites/players_sprites/player2_sprites/Punk_hurt.png"))  # criar grupo de player e adicionar no PlayerGroup do pygame
        mad_rush.menu()
