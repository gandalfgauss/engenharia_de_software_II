import pygame
import time
import threading

from src.utils.spritesheet import SpriteSheet
from src.classes.scoreboard import Scoreboard


class Player1(pygame.sprite.Sprite):
    """Classe responsavel pelas acoes do player"""

    def __init__(self, config, ground, n_images_run, width, height,
                 path_image_run, n_images_jump, path_image_jump, n_images_hurt, path_image_hurt):
        """Construtor da classe player
         Onde:
                path_image_run -> caminho para imagem que contem as sprites de correr
                n_images_run -> quantas imagens de correr o personagem possui
                width -> largura das sprites
                height -> altura das sprites
                config -> configurações do jogo
                n_images_jump -> quantas imagens de pulo o personagem possui
                path_image_jump -> caminho para a imagem do jump do personagem
                n_images_hurt -> numero de imagens do personagem tomando dano
                path_image_hurt -> caminho da imagem do personagem tomando dano"""

        pygame.sprite.Sprite.__init__(self)

        self.mutiply = 1
        self.shield = False
        self.stoptime = False

        self.width = width
        self.height = height

        self.config = config
        self.move_in_y = 0
        self.move_in_x = 0

        self.velocity = self.config.game_speed

        self.ground = ground

        self.rect = pygame.Rect(self.width + 2, self.config.height_window - 120, 50, 100)

        self.n_images_run = n_images_run

        self.run_image = pygame.image.load(path_image_run)  # carrega a imagem com os sprites de correr
        self.run_SH = SpriteSheet(self.run_image)  # cria um extrator de sprites
        self.image_run = [self.run_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                          range(self.n_images_run)]  # extrai os n sprites de correr

        self.n_images_jump = n_images_jump
        self.jump_image = pygame.image.load(path_image_jump)  # carrega a imagem com os sprites de pular
        self.jump_SH = SpriteSheet(self.jump_image)  # cria um extrator de sprites
        self.image_jump = [self.jump_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                           range(self.n_images_jump)]  # extrai os n sprites de correr

        self.current_image_run = 0
        self.image = self.image_run[self.current_image_run].convert_alpha()  # definir imagem atual para o ‘player’

        self.current_image_jump = 0

        self.n_images_hurt = n_images_hurt
        self.hurt_image = pygame.image.load(path_image_hurt)  # carrega a imagem com os sprites de tomar dano
        self.hurt_SH = SpriteSheet(self.hurt_image)  # cria um extrator de sprites
        self.image_hurt = [self.hurt_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                           range(self.n_images_hurt)]  # extrai os n sprites de correr
        self.current_image_hurt = 0

        self.scoreboard = Scoreboard(scoreboard_position=[25, 20], points_position=[50, 50])
        self.vencedor = 0

        self.musica_pulo1 = pygame.mixer.Sound("../sounds/jump1.ogg")
        self.musica_pulo2 = pygame.mixer.Sound("../sounds/jump1.ogg")

        self.musica_coin = pygame.mixer.Sound("../sounds/coin.ogg")

        self.musica_double_points = pygame.mixer.Sound("../sounds/doublepoints.ogg")

        self.musica_stone = pygame.mixer.Sound("../sounds/stone.ogg")

        self.musica_shield = pygame.mixer.Sound("../sounds/shield.wav")

        self.musica_stoptime = pygame.mixer.Sound("../sounds/stoptime.wav")

        self.musica_bomb = pygame.mixer.Sound("../sounds/bomb.flac")

    def animacao_hurt(self):
        """ Realiza a animacao do dano """
        self.current_image_hurt = 0
        for i in range(self.n_images_hurt):
            self.image = self.image_hurt[i]
            time.sleep(0.01)

    def animacao_jump(self):
        """ Realiza a animacao do pulo"""

        self.image = self.image_jump[self.current_image_jump]
        self.current_image_jump = (self.current_image_jump + 1) % self.n_images_jump

    def animacao_idle(self):
        """ Animacao do player parado"""
        self.current_image_run = (self.current_image_run + 1) % self.n_images_run
        self.image = self.image_run[self.current_image_run]

    def limites(self):
        """ Essa metodo verifica se o player ultrapassou os limites da tela"""
        # verificar se player atingiu limites da tela
        if self.rect[0] > self.config.width_window - self.width:
            self.rect[0] = self.config.width_window - self.width - 5
        if self.rect[0] < self.width:
            self.rect[0] = 48
        if self.rect[1] < self.height + 1:
            self.rect[1] = self.height + 1
        if self.rect[1] > self.config.height_window - 120:
            self.rect[1] = self.config.height_window - 120

    def move_player(self):
        """Esse metodo faz o player correr na horizontal"""

        key = pygame.key.get_pressed()  # declara uma tecla chave
        if key[pygame.K_d]:  # se a tecla 'd' for pressionada
            self.move_in_x += self.velocity  # varia o x do player para direita

        if key[pygame.K_a]:  # se a tecla 'a' for pressionada
            self.move_in_x -= 1.5 * self.velocity  # varia o x do player para esquerda

        self.rect[0] += self.move_in_x
        self.move_in_x = 0

    def fall(self):
        """ Metodo que faz animacao do player caindo"""
        if self.rect[1] + self.move_in_y > self.config.height_window - 120:
            self.move_in_y = 0  # remove gravidade
            self.rect[1] = self.config.height_window - 120
        else:
            self.move_in_y += 3.5
            self.rect[1] += self.move_in_y
            # animacao player caindo
            # self.animacao_idle()

    def jump2(self):
        """ Metodo para ajudar a realizar o pulo"""
        self.current_image_jump = 0
        self.current_image_run = 0
        self.musica_pulo1.play()
        for i in range(self.n_images_jump):
            self.move_in_y -= 1.2 * self.velocity
            self.rect[1] += self.move_in_y
            self.animacao_jump()
            time.sleep(0.09)

            self.move_in_y = 0

            # se pressionar 'w' da o pulo alterando em y
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and i > 1:
                self.musica_pulo2.play()
                for j in range(2 * self.n_images_jump - i - 1):
                    self.move_in_y -= 1.3 * self.velocity
                    self.rect[1] += self.move_in_y
                    self.animacao_jump()
                    time.sleep(0.05)

                    self.move_in_y = 0
                break

    def jump(self):
        """ Metodo que faz o player pular quando pressionado a tecla w"""
        key = pygame.key.get_pressed()

        # se pressionar 'w' da o pulo alterando em y
        if key[pygame.K_w] and self.player_no_chao():
            t = threading.Thread(target=self.jump2)
            t.start()

    def player_colidiu_com_moeda(self, objects_groups):
        """ Esse método trata a colisão do player com uma moeda"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["coins"], False, True)
        if colision != {}:
            self.scoreboard.add_point(1 * self.mutiply)  # aumentar os pontos
            self.musica_coin.set_volume(0.1)
            self.musica_coin.play()
            if not self.stoptime:
                self.velocity = min(self.config.game_speed, 18)

    def player_colidiu_com_2x(self, objects_groups):
        """ Esse método trata a colisão do player com um 2x"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["2x"], False, True)
        if colision != {}:
            self.musica_double_points.play()
            self.mutiply += 1  # aumentar multiplicador de pontos

    def player_colidiu_com_shield(self, objects_groups):
        """ Esse método trata a colisão do player com um shield"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["shields"], False, True)
        if colision != {}:
            self.musica_shield.set_volume(0.3)
            self.musica_shield.play()
            self.shield = True  # jogador fica defendido

    def stoptime_now(self, seconds):
        """ Esse método para o tempo por alguns segundos"""
        game_speed_before = self.config.game_speed
        self.config.game_speed = 4
        self.musica_stoptime.set_volume(0.3)
        self.musica_stoptime.play()
        time.sleep(seconds)
        self.config.game_speed = game_speed_before
        self.stoptime = False
        self.musica_stoptime.stop()

    def player_colidiu_com_stoptime(self, objects_groups):
        """ Esse método trata a colisão do player com um stoptime"""
        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["stoptime"], False, True)
        if colision != {}:
            self.stoptime = True
            # thread parar o tempo por 8 segundos
            t = threading.Thread(target=self.stoptime_now, args=(8,))
            t.start()

    def player_colidiu_com_stone(self, objects_groups):
        """ Esse método trata a colisão do player com um stone"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["stones"], False, True)
        if colision != {}:

            # animacao de dano
            t = threading.Thread(target=self.animacao_hurt)
            t.start()

            self.musica_stone.set_volume(0.3)
            self.musica_stone.play()

            if not self.shield:
                self.scoreboard.set_point(max(0, self.scoreboard.points - 50))  # perde pontos
            else:
                self.shield = False

    def player_colidiu_com_bomba(self, objects_groups):
        """ Esse metodo trata a colisao do player com a bomba"""
        # se o player colidir com a bomba
        colision = pygame.sprite.groupcollide(objects_groups["player1"], objects_groups["bombs"], False, True)
        if colision != {}:
            # animacao de dano
            t = threading.Thread(target=self.animacao_hurt)
            t.start()

            self.musica_bomb.set_volume(0.4)
            self.musica_bomb.play()

            if not self.shield:
                self.config.game_loop = False  # Sai do jogo
                self.vencedor = 2
            else:
                self.shield = False

    def colisions(self, objects_groups):
        """ Esse método trata as colisoes do player"""
        self.player_colidiu_com_bomba(objects_groups)
        self.player_colidiu_com_shield(objects_groups)
        self.player_colidiu_com_2x(objects_groups)
        self.player_colidiu_com_stone(objects_groups)
        self.player_colidiu_com_stoptime(objects_groups)
        self.player_colidiu_com_moeda(objects_groups)

    def player_no_chao(self):
        """ Esse metodo define se o player esta no chao ou nao"""
        return self.rect[1] >= self.config.height_window - 120

    def update(self, *args):
        """ Metodo que atualiza o player"""
        self.move_player()  # atualiza movimento horizontal do player
        self.jump()  # faz o pulo do personagem
        self.fall()  # faz a descida do personagem
        self.limites()  # verifica se player nao saiu dos limites da tela

        if self.player_no_chao():  # se o player estiver no chao chama animacao de corrida
            self.animacao_idle()  # atualiza a animacao parado do player


class Player2(pygame.sprite.Sprite):
    """Classe responsavel pelas acoes do player"""

    def __init__(self, config, ground, n_images_run, width, height,
                 path_image_run, n_images_jump, path_image_jump, n_images_hurt, path_image_hurt):
        """Construtor da classe player
         Onde:
                path_image_run -> caminho para imagem que contem as sprites de correr
                n_images_run -> quantas imagens de correr o personagem possui
                width -> largura das sprites
                height -> altura das sprites
                config -> configurações do jogo
                n_images_jump -> quantas imagens de pulo o personagem possui
                path_image_jump -> caminho para a imagem do jump do personagem
                n_images_hurt -> numero de imagens do personagem tomando dano
                path_image_hurt -> caminho da imagem do personagem tomando dano"""

        pygame.sprite.Sprite.__init__(self)

        self.mutiply = 1
        self.shield = False
        self.stoptime = False

        self.width = width
        self.height = height

        self.config = config
        self.move_in_y = 0
        self.move_in_x = 0

        self.velocity = self.config.game_speed

        self.ground = ground

        self.rect = pygame.Rect(self.width + 50, self.config.height_window - 120, 50, 100)

        self.n_images_run = n_images_run

        self.run_image = pygame.image.load(path_image_run)  # carrega a imagem com os sprites de correr
        self.run_SH = SpriteSheet(self.run_image)  # cria um extrator de sprites
        self.image_run = [self.run_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                          range(self.n_images_run)]  # extrai os n sprites de correr

        self.n_images_jump = n_images_jump
        self.jump_image = pygame.image.load(path_image_jump)  # carrega a imagem com os sprites de pular
        self.jump_SH = SpriteSheet(self.jump_image)  # cria um extrator de sprites
        self.image_jump = [self.jump_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                           range(self.n_images_jump)]  # extrai os n sprites de correr

        self.current_image_run = 0
        self.image = self.image_run[self.current_image_run].convert_alpha()  # definir imagem atual para o ‘player’

        self.current_image_jump = 0

        self.n_images_hurt = n_images_hurt
        self.hurt_image = pygame.image.load(path_image_hurt)  # carrega a imagem com os sprites de tomar dano
        self.hurt_SH = SpriteSheet(self.hurt_image)  # cria um extrator de sprites
        self.image_hurt = [self.hurt_SH.get_image(n, width, height, 2, (0, 0, 0)) for n in
                           range(self.n_images_hurt)]  # extrai os n sprites de correr
        self.current_image_hurt = 0

        self.scoreboard = Scoreboard(scoreboard_position=[1100, 20], points_position=[1125, 50])

        self.vencedor = 0

        self.musica_pulo1 = pygame.mixer.Sound("../sounds/jump1.ogg")
        self.musica_pulo2 = pygame.mixer.Sound("../sounds/jump1.ogg")

        self.musica_coin = pygame.mixer.Sound("../sounds/coin.ogg")

        self.musica_double_points = pygame.mixer.Sound("../sounds/doublepoints.ogg")

        self.musica_stone = pygame.mixer.Sound("../sounds/stone.ogg")

        self.musica_shield = pygame.mixer.Sound("../sounds/shield.wav")

        self.musica_stoptime = pygame.mixer.Sound("../sounds/stoptime.wav")

        self.musica_bomb = pygame.mixer.Sound("../sounds/bomb.flac")


    def animacao_hurt(self):
        """ Realiza a animacao do dano """
        self.current_image_hurt = 0
        for i in range(self.n_images_hurt):
            self.image = self.image_hurt[i]
            time.sleep(0.01)

    def animacao_jump(self):
        """ Realiza a animacao do pulo"""

        self.image = self.image_jump[self.current_image_jump]
        self.current_image_jump = (self.current_image_jump + 1) % self.n_images_jump

    def animacao_idle(self):
        """ Animacao do player parado"""
        self.current_image_run = (self.current_image_run + 1) % self.n_images_run
        self.image = self.image_run[self.current_image_run]

    def limites(self):
        """ Essa metodo verifica se o player ultrapassou os limites da tela"""
        # verificar se player atingiu limites da tela
        if self.rect[0] > self.config.width_window - self.width:
            self.rect[0] = self.config.width_window - self.width - 5
        if self.rect[0] < self.width:
            self.rect[0] = 48
        if self.rect[1] < self.height + 1:
            self.rect[1] = self.height + 1
        if self.rect[1] > self.config.height_window - 120:
            self.rect[1] = self.config.height_window - 120

    def move_player(self):
        """Esse metodo faz o player correr na horizontal"""

        key = pygame.key.get_pressed()  # declara uma tecla chave
        if key[pygame.K_RIGHT]:  # se a tecla 'd' for pressionada
            self.move_in_x += self.velocity  # varia o x do player para direita

        if key[pygame.K_LEFT]:  # se a tecla 'a' for pressionada
            self.move_in_x -= 1.5 * self.velocity  # varia o x do player para esquerda

        self.rect[0] += self.move_in_x
        self.move_in_x = 0

    def fall(self):
        """ Metodo que faz animacao do player caindo"""
        if self.rect[1] + self.move_in_y > self.config.height_window - 120:
            self.move_in_y = 0  # remove gravidade
            self.rect[1] = self.config.height_window - 120
        else:
            self.move_in_y += 3.5
            self.rect[1] += self.move_in_y
            # animacao player caindo
            # self.animacao_idle()

    def jump2(self):
        """ Metodo para ajudar a realizar o pulo"""
        self.current_image_jump = 0
        self.current_image_run = 0
        self.musica_pulo1.play()

        for i in range(self.n_images_jump):
            self.move_in_y -= 1.2 * self.velocity
            self.rect[1] += self.move_in_y
            self.animacao_jump()
            time.sleep(0.09)

            self.move_in_y = 0

            # se pressionar 'w' da o pulo alterando em y
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and i > 1:
                self.musica_pulo2.play()
                for j in range(2 * self.n_images_jump - i - 1):
                    self.move_in_y -= 1.3 * self.velocity
                    self.rect[1] += self.move_in_y
                    self.animacao_jump()
                    time.sleep(0.05)

                    self.move_in_y = 0
                break

    def jump(self):
        """ Metodo que faz o player pular quando pressionado a tecla w"""
        key = pygame.key.get_pressed()

        # se pressionar 'w' da o pulo alterando em y
        if key[pygame.K_UP] and self.player_no_chao():
            t = threading.Thread(target=self.jump2)
            t.start()

    def player_colidiu_com_moeda(self, objects_groups):
        """ Esse método trata a colisão do player com uma moeda"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["coins"], False, True)
        if colision != {}:
            self.scoreboard.add_point(1 * self.mutiply)  # aumentar os pontos
            self.musica_coin.set_volume(0.1)
            self.musica_coin.play()
            if not self.stoptime:
                self.velocity = min(self.config.game_speed, 18)

    def player_colidiu_com_2x(self, objects_groups):
        """ Esse método trata a colisão do player com um 2x"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["2x"], False, True)
        if colision != {}:
            self.musica_double_points.play()
            self.mutiply += 1  # aumentar multiplicador de pontos

    def player_colidiu_com_shield(self, objects_groups):
        """ Esse método trata a colisão do player com um shield"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["shields"], False, True)
        if colision != {}:

            self.musica_shield.set_volume(0.3)
            self.musica_shield.play()
            self.shield = True  # jogador fica defendido

    def stoptime_now(self, seconds):
        """ Esse método para o tempo por alguns segundos"""
        game_speed_before = self.config.game_speed
        self.config.game_speed = 4

        self.musica_stoptime.set_volume(0.3)
        self.musica_stoptime.play()
        time.sleep(seconds)
        self.config.game_speed = game_speed_before
        self.stoptime = False
        self.musica_stoptime.stop()

    def player_colidiu_com_stoptime(self, objects_groups):
        """ Esse método trata a colisão do player com um stoptime"""
        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["stoptime"], False, True)
        if colision != {}:
            self.stoptime = True
            # thread parar o tempo por 8 segundos
            t = threading.Thread(target=self.stoptime_now, args=(8,))
            t.start()

    def player_colidiu_com_stone(self, objects_groups):
        """ Esse método trata a colisão do player com um stone"""

        # se o player colidir com o chao
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["stones"], False, True)
        if colision != {}:
            # animacao de dano
            t = threading.Thread(target=self.animacao_hurt)
            t.start()

            self.musica_stone.set_volume(0.3)
            self.musica_stone.play()

            if not self.shield:
                self.scoreboard.set_point(max(0, self.scoreboard.points - 50))  # perde pontos
            else:
                self.shield = False

    def player_colidiu_com_bomba(self, objects_groups):
        """ Esse metodo trata a colisao do player com a bomba"""
        # se o player colidir com a bomba
        colision = pygame.sprite.groupcollide(objects_groups["player2"], objects_groups["bombs"], False, True)
        if colision != {}:
            # animacao de dano
            t = threading.Thread(target=self.animacao_hurt)
            t.start()

            self.musica_bomb.set_volume(0.4)
            self.musica_bomb.play()

            if not self.shield:
                self.config.game_loop = False  # Sai do jogo
                self.vencedor = 1
            else:
                self.shield = False

    def colisions(self, objects_groups):
        """ Esse método trata as colisoes do player"""
        self.player_colidiu_com_bomba(objects_groups)
        self.player_colidiu_com_shield(objects_groups)
        self.player_colidiu_com_2x(objects_groups)
        self.player_colidiu_com_stone(objects_groups)
        self.player_colidiu_com_stoptime(objects_groups)
        self.player_colidiu_com_moeda(objects_groups)

    def player_no_chao(self):
        """ Esse metodo define se o player esta no chao ou nao"""
        return self.rect[1] >= self.config.height_window - 120

    def update(self, *args):
        """ Metodo que atualiza o player"""
        self.move_player()  # atualiza movimento horizontal do player
        self.jump()  # faz o pulo do personagem
        self.fall()  # faz a descida do personagem
        self.limites()  # verifica se player nao saiu dos limites da tela

        if self.player_no_chao():  # se o player estiver no chao chama animacao de corrida
            self.animacao_idle()  # atualiza a animacao parado do player
