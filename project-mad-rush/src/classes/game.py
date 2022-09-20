import time

import pygame

from src.classes.ground import Ground
from src.classes.bomb import Bomb
from src.classes.coins import Coins
from src.classes.double_points import DoublePoints
from src.classes.stone import Stone
from src.classes.shield import Shield
from src.classes.stoptime import Stoptime


class Game:
    """ Essa é a classe que rodará o jogo"""

    def __init__(self, config):
        """ Construtor da classe Game
            Parâmetros:
                config -> configurações do jogo
                name_of_game -> nome do jogo"""

        self.config = config  # criar configurações do jogo
        self.game_window = pygame.display.set_mode(
            [self.config.width_window, self.config.height_window])  # inicializa janela do jogo

        self.clock = pygame.time.Clock()  # definindo o clock do jogo, para a animacao ter sentido / remover ticks  #
        # definindo o clock do jogo, para a animacao ter sentido / remover ticks

        self.objects_groups = {}  # grupo de objetos

        self.ground = None  # criando grupo do chao do jogo

        self.player1, self.player1_group = None, None  # criar grupo de player e adicionar no PlayerGroup do pygame
        self.player2, self.player2_group = None, None

        self.background = None  # Criar BackGroud (Tela de fundo) do jogo

        self.bg_images = []

        escala = self.config.height_window / pygame.image.load(
            f"../sprites/backgrounds/plx-{1}.png").convert_alpha().get_height()
        for i in range(1, 6):
            bg_image = pygame.image.load(f"../sprites/backgrounds/plx-{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (bg_image.get_width() * escala, bg_image.get_height() * escala))
            self.bg_images.append(bg_image)

        self.bg_width = self.bg_images[0].get_width()
        self.scroll = 0

        self.musica_menu = pygame.mixer.Sound("../sounds/musicaMenu2.mp3")
        self.musica_jogando = pygame.mixer.Sound("../sounds/musicaJogando.mp3")

    def cria_chao(self, ground):
        """ Esse método cria o chão do jogo"""
        self.ground = ground

        if not self.objects_groups.get("ground"):
            self.objects_groups["ground"] = pygame.sprite.Group()

        self.objects_groups["ground"].add(self.ground)

        for i in range(10):
            self.objects_groups["ground"].add(Ground(x_pos=self.ground.width - 60 + 200 * i,
                                                     config=self.config))

    def criar_players(self, player):
        """ Esse método cria os jogadores do jogo"""

        if not self.objects_groups.get("player1"):
            self.player1 = player
            self.objects_groups["player1"] = pygame.sprite.Group()
            self.objects_groups["player1"].add(self.player1)

        else:
            self.player2 = player
            self.objects_groups["player2"] = pygame.sprite.Group()
            self.objects_groups["player2"].add(self.player2)

    def cria_background(self, background):
        """ Método que cria o Background do jogo"""
        self.background = background

    def draw_bg(self):
        """ Metodo que faz o Paralax do background"""
        for x in range(0, 5 + int(abs(self.scroll) // 200)):
            speed = 1
            for n, i in enumerate(self.bg_images):
                self.game_window.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                # print((x * self.bg_width) - self.scroll * speed)
                speed += 1

        self.scroll += self.config.game_speed // 6

        """if self.scroll >= 840:
            self.scroll = 0"""

        # print("Scrool", self.scroll)

    def update(self, n_players=1):
        """Metódo que atualiza os frames dos objetos do jogo
        Parametros ->
            n_players -> numero de jogadores no game
        """
        if n_players == 2:
            for object_game in self.objects_groups.values():
                object_game.update()
        else:
            for key, object_game in self.objects_groups.items():
                if key != "player2":
                    object_game.update()

    def draw(self, n_players=1):
        """Método Desenha os objetos do jogo na tela
        Parametros ->
            n_players -> numero de jogadores no game
        """
        if n_players == 2:
            for object_game in self.objects_groups.values():
                object_game.draw(self.game_window)
        else:
            for key, object_game in self.objects_groups.items():
                if key != "player2":
                    object_game.draw(self.game_window)

    def tratar_chao_fora_da_tela(self):
        """ Esse método trata o chão fora da tela e controi outro"""
        if self.objects_groups["ground"].sprites():
            if self.is_off_screen(self.objects_groups["ground"].sprites()[0]):
                self.objects_groups["ground"].remove(self.objects_groups["ground"].sprites()[0])
                new_ground = Ground(x_pos=self.config.width_window + 100, config=self.config)
                self.objects_groups["ground"].add(new_ground)

    def tratar_item_fora_da_tela(self):
        """ Remove um item fora da tela"""
        # para cada grupo
        for group in self.objects_groups.values():
            # se esse grupo for nao vazio
            if group.sprites():
                # e se estiver fora da tela o removo
                if self.is_off_screen(group.sprites()[0]):
                    group.remove(group.sprites()[0])

    def dropar_itens(self):
        """ Esse método dropa os itens do jogo"""

        if not self.objects_groups.get("2x"):
            self.objects_groups["2x"] = pygame.sprite.Group()
        DoublePoints(0, 0, self.config).get_random(60, self.config.height_window - 74 - 48,
                                                   self.objects_groups["2x"], 0.0035)

        if not self.objects_groups.get("coins"):
            self.objects_groups["coins"] = pygame.sprite.Group()
        Coins(0, 0, self.config).get_random(60, self.config.height_window - 74 - 48,
                                            self.objects_groups["coins"], 0.03)

        if not self.objects_groups.get("bombs"):
            self.objects_groups["bombs"] = pygame.sprite.Group()
        Bomb(0, 0, self.config).get_random(60, self.config.height_window - 74 - 48,
                                           self.objects_groups["bombs"], 0.029)

        if not self.objects_groups.get("stones"):
            self.objects_groups["stones"] = pygame.sprite.Group()
        Stone(0, 0, self.config).get_random(self.config.height_window - 74,
                                            self.config.height_window - 74,
                                            self.objects_groups["stones"], 0.024)

        if not self.objects_groups.get("shields"):
            self.objects_groups["shields"] = pygame.sprite.Group()
        Shield(0, 0, self.config).get_random(60, self.config.height_window - 74 - 48,
                                             self.objects_groups["shields"], 0.0035)

        if not self.objects_groups.get("stoptime"):
            self.objects_groups["stoptime"] = pygame.sprite.Group()
        Stoptime(0, 0, self.config).get_random(60, self.config.height_window - 74 - 48,
                                               self.objects_groups["stoptime"], 0.0035)

    def atualiza_velocidade(self):
        """ Esse método atualiza a velocidade do jogo"""
        if not self.player1.stoptime and not self.player2.stoptime:
            nova_velocidade = self.config.game_speed + self.config.incremento
            self.config.game_speed = min(nova_velocidade, 70)

    def ler_scores(self):
        """ Ler pontuacoes do arquivo"""
        scores = []
        try:
            with open('scores.txt', ) as arquivo:
                scores = arquivo.readlines()
                scores = [str(int(score)) for score in scores]
        except FileNotFoundError:
            open("scores.txt", "w")

        return scores

    def escrever_pontuacao(self, n_players=1):
        """ Esse metodo escrece a pontuacao apos o termino do jogo
        Parametros:
            n_players -> numero de jogadores"""

        scores = self.ler_scores()
        scores = [int(score) for score in scores]

        if n_players == 1:

            scores.append(int(self.player1.scoreboard.points))
            scores.sort(reverse=True)

            with open('scores.txt', "w") as arquivo:
                for i in range(min(10, len(scores))):
                    arquivo.write(str(scores[i]) + "\n")

        elif n_players == 2:
            scores.append(int(self.player1.scoreboard.points))
            scores.append(int(self.player2.scoreboard.points))
            scores.sort(reverse=True)

            with open('scores.txt', "w") as arquivo:
                for i in range(min(10, len(scores))):
                    arquivo.write(str(scores[i]) + "\n")

    def mostrar_scores(self):
        """ Esse metodo mostra as pontuacoes do jogo"""
        """ Menu do jogo"""
        menu_online = True

        while menu_online:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                    menu_online = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clicou no botao de voltar
                    print("Clicou,", mouse[0], mouse[1])
                    if self.config.width_window / 2 - 250 <= mouse[0] <= self.config.width_window / 2 - 250 + 130 and \
                            self.config.height_window / 2 - 150 <= mouse[1] <= self.config.height_window / 2 - 150 + 40:
                        menu_online = False

            self.game_window.blit(self.background.image, (0, 0))  # tela de fundo do jogo

            # Criar texto inicial do jogo ----------------------------------------------------
            scores_text = "Scores"
            fonte = pygame.font.SysFont('comicsans', 70)

            scores_text = fonte.render(scores_text, True, [255, 255, 0])

            self.game_window.blit(scores_text, [self.config.width_window // 2 - 120, 48])
            # ---------------------------------------------------------------------------------

            # Desenhar pontuações:
            scores = self.ler_scores()
            fonte_botao = pygame.font.SysFont('comicsans', 30)

            position = 0
            for score in scores:
                text = fonte_botao.render(score, True, [255, 255, 0])

                pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 50,
                                                               self.config.height_window / 2 - 150 + position, 130, 40])

                self.game_window.blit(text, (
                    self.config.width_window / 2 - 40, self.config.height_window / 2 - 150 + position))

                position += 50

            # Desenhar botao de voltar
            pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 250,
                                                           self.config.height_window / 2 - 150, 130, 40])

            text = fonte_botao.render("Voltar", True, [255, 255, 0])
            self.game_window.blit(text,
                                  (self.config.width_window / 2 - 230, self.config.height_window / 2 - 150))
            pygame.display.update()  # atualizar tela pygame
        self.musica_menu.stop()

    def fim_de_jogo(self, vencedor):
        """ Esse metodo cria a tela de fim de jogo
            Parametros
                vencedor -> vencedor do jogo"""

        menu_online = True

        while menu_online:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                    menu_online = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clicou no botao de voltar
                    print("Clicou,", mouse[0], mouse[1])
                    if self.config.width_window / 2 - 50 <= mouse[0] <= self.config.width_window / 2 - 50 + 130 and \
                            self.config.height_window / 2 + 50 <= mouse[1] <= self.config.height_window / 2 + 50 + 40:
                        menu_online = False

            self.game_window.blit(self.background.image, (0, 0))  # tela de fundo do jogo

            # Falar quem venceu ----------------------------------------------------
            text = "Player " + str(vencedor) + " venceu !!!"
            fonte = pygame.font.SysFont('comicsans', 70)

            text = fonte.render(text, True, [255, 255, 0])

            self.game_window.blit(text, [self.config.width_window // 2 - 300, 48])
            # ---------------------------------------------------------------------------------

            fonte_botao = pygame.font.SysFont('comicsans', 30)

            # Desenhar botao de voltar
            pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 50,
                                                           self.config.height_window / 2 + 50, 130, 40])

            text = fonte_botao.render("Voltar", True, [255, 255, 0])
            self.game_window.blit(text,
                                  (self.config.width_window / 2 - 30, self.config.height_window / 2 + 50))

            pygame.display.update()  # atualizar tela pygame
        self.musica_jogando.stop()

    def menu(self):
        """ Menu do jogo"""
        self.musica_menu.set_volume(0.1)
        self.musica_menu.play(loops=-1)
        menu_online = True
        tela = ""
        while menu_online:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                    menu_online = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clicou no botao de 1 jogador
                    if self.config.width_window / 2 - 50 <= mouse[0] <= self.config.width_window / 2 - 50 + 130 and \
                            self.config.height_window / 2 - 40 <= mouse[1] <= self.config.height_window / 2 - 40 + 40:
                        menu_online = False
                        tela = "1player"

                    # Clicou no botao de 2 jogadores
                    if self.config.width_window / 2 - 50 <= mouse[0] <= self.config.width_window / 2 - 50 + 130 and \
                            self.config.height_window / 2 + 40 <= mouse[1] <= self.config.height_window / 2 + 40 + 40:
                        menu_online = False
                        tela = "2players"

                    # Clicou no botao de 2 jogadores
                    if self.config.width_window / 2 - 50 <= mouse[0] <= self.config.width_window / 2 - 50 + 130 and \
                            self.config.height_window / 2 + 120 <= mouse[1] <= self.config.height_window / 2 + 120 + 40:
                        menu_online = False
                        tela = "scores"

            self.game_window.blit(self.background.image, (0, 0))  # tela de fundo do jogo

            # Criar texto inicial do jogo ----------------------------------------------------
            nome_do_jogo = "Mad Rush"
            fonte = pygame.font.SysFont('comicsans', 70)

            nome_do_jogo_text = fonte.render(nome_do_jogo, True, [255, 255, 0])

            self.game_window.blit(nome_do_jogo_text, [self.config.width_window // 2 - 120, 48])
            # ---------------------------------------------------------------------------------

            # Desenhar botao 1 player
            fonte_botao = pygame.font.SysFont('comicsans', 30)
            botao1_text = fonte_botao.render("1 Player", True, [255, 255, 0])

            pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 50,
                                                           self.config.height_window / 2 - 40, 130, 40])

            self.game_window.blit(botao1_text, (self.config.width_window / 2 - 40, self.config.height_window / 2 - 40))

            # Desenhar botao 2 players
            fonte_botao = pygame.font.SysFont('comicsans', 30)
            botao1_text = fonte_botao.render("2 Players", True, [255, 255, 0])

            pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 50,
                                                           self.config.height_window / 2 + 40, 130, 40])

            self.game_window.blit(botao1_text, (self.config.width_window / 2 - 49, self.config.height_window / 2 + 40))

            # Desenhar botao Scores
            fonte_botao = pygame.font.SysFont('comicsans', 30)
            botao1_text = fonte_botao.render("Scores", True, [255, 255, 0])

            pygame.draw.rect(self.game_window, [0, 0, 0], [self.config.width_window / 2 - 50,
                                                           self.config.height_window / 2 + 120, 130, 40])

            self.game_window.blit(botao1_text, (self.config.width_window / 2 - 33, self.config.height_window / 2 + 117))

            pygame.display.update()  # atualizar tela pygame

        if tela == "1player":
            self.start_game()
        elif tela == "2players":
            self.start_game2()

        elif tela == "scores":
            self.mostrar_scores()

    def start_game2(self):
        """ ‘Loop’ que rodara o jogo """
        # loop do jogo
        self.musica_menu.stop()
        self.musica_jogando.play(loops=-1)
        self.musica_jogando.set_volume(0.1)

        while self.config.game_loop:  # atualiza a cada frame
            # self.game_window.blit(self.background.image, (0, 0))  # desenha a tela de fundo

            self.clock.tick(self.config.fps)  # rodar fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                    # pygame.quit()
                    self.config.game_loop = False

            self.dropar_itens()  # dropa os itens do jogo

            self.tratar_chao_fora_da_tela()  # se o meu chao estiver fora da tela eu removo-o e crio um novo chao

            self.tratar_item_fora_da_tela()  # remove um item que está fora da tela

            self.player1.colisions(self.objects_groups)  # tratar colisao do player com os objetos da tela

            self.player2.colisions(self.objects_groups)  # tratar colisao do player com os objetos da tela

            self.atualiza_velocidade()  # atualiza a velocidade do jogo

            self.draw_bg()

            # inserir contador de pontos na tela do player 1 --------------------
            # inserir "Pontos: " na tela
            self.game_window.blit(self.player1.scoreboard.scoreboard_text, self.player1.scoreboard.scoreboard_position)

            self.game_window.blit(self.player1.scoreboard.points_text, self.player1.scoreboard.points_position)
            # --------------------------------------------------------------------

            # inserir contador de pontos na tela do player 2 --------------------
            # inserir "Pontos: " na tela
            self.game_window.blit(self.player2.scoreboard.scoreboard_text, self.player2.scoreboard.scoreboard_position)

            self.game_window.blit(self.player2.scoreboard.points_text, self.player2.scoreboard.points_position)
            # --------------------------------------------------------------------
            # --------------------------------------------------------------------

            self.draw(2)  # redesenhar objetos

            self.update(2)  # atualizar objetos na tela

            pygame.display.update()  # atualizar tela pygame

        self.escrever_pontuacao(2)
        self.fim_de_jogo(max(self.player1.vencedor, self.player2.vencedor))

    def start_game(self):
        """ ‘Loop’ que rodara o jogo """
        # loop do jogo
        self.musica_menu.stop()
        self.musica_jogando.play(loops=-1)
        self.musica_jogando.set_volume(0.1)
        while self.config.game_loop:  # atualiza a cada frame
            # self.game_window.blit(self.background.image, (0, 0))  # desenha a tela de fundo

            self.clock.tick(self.config.fps)  # rodar fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # tratar o botao de fechar janela
                    # pygame.quit()
                    self.config.game_loop = False

            self.dropar_itens()  # dropa os itens do jogo

            self.tratar_chao_fora_da_tela()  # se o meu chao estiver fora da tela eu removo-o e crio um novo chao

            self.tratar_item_fora_da_tela()  # remove um item que está fora da tela

            self.player1.colisions(self.objects_groups)  # tratar colisao do player com os objetos da tela

            self.atualiza_velocidade()  # atualiza a velocidade do jogo

            self.draw_bg()

            # inserir "Pontos: " na tela

            self.game_window.blit(self.player1.scoreboard.scoreboard_text, self.player1.scoreboard.scoreboard_position)

            self.game_window.blit(self.player1.scoreboard.points_text, self.player1.scoreboard.points_position)

            self.draw()  # redesenhar objetos

            self.update()  # atualizar objetos na tela

            pygame.display.update()  # atualizar tela pygame

        self.escrever_pontuacao()
        self.fim_de_jogo(1)

    def is_off_screen(self, sprite):
        """ Esse método determina se um objeto esta ou nao fora da tela
            Parametros:
                sprite -> objeto"""
        return sprite.rect[0] < -(sprite.rect[2])
