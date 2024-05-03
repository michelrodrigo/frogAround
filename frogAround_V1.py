""" Sprite Sample Program """

# --- Bibliotecas ---
import random
import arcade
import math


# --- Constantes ---

# escala das imagens
SCALE_SAPO = 0.3
SCALE_FOLHA = 0.25
SCALE_NUM_TEMPO = 0.5
SCALE_NUM_PLACAR = 0.2
SCALE_NUM_RECORD = 0.3
SCALE_LILIES = 0.5
SCALE_DOCK = 0.4
SCALE_GAMEOVER = 0.8
SCALE_MOSCA = 0.3
SCALE_PONTO = 0.2
SCALE_LILY_FLOWER = 0.5
SCALE_NOVO_RECORDE = 0.8


#outras definições
NUM_LILIES = 40
NUM_SAPOS = 40
VELOCIDADE_INICIAL = 1                  # velocidade inicial com que a folha irá girar
INCREMENTO_VELOCIDADE = 1.05            # incremento de velocidade que será aplicado a cada vez que um sapo alcançar a folha
VELOCIDADE_SAPO = 10                    # velocidade do sapo
PONTUACAO_EXTRA = 2                     # Número de pontos da pontuação extra
RAIO_COLISAO_FOLHA = 830 * SCALE_FOLHA  # raio de colisão da folha
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

TECLA1 = arcade.key.A
TECLA2 = arcade.key.S
TECLA3 = arcade.key.ESCAPE

OFFSET_FILA = -50

# os números representam o estado nos quais o jogo pode estar
ESPERA = 0
JOGO = 1
GAME_OVER = 3


class FrogAround(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Frog Around", fullscreen=True)

        #declaração de variáveis
        # Sprites
        self.folha = arcade.Sprite()                        # sprite da folha principal
        self.sapo_list = arcade.SpriteList()                # Lista de sprites dos sapos
        self.sapo_hit_folha = arcade.SpriteList()           # Lista dos sapos que atingiram a folha
        self.sapo_folha = arcade.SpriteList()               # Lista dos sapos que já estão na folha
        self.numero_tempo_list = arcade.SpriteList()        # Lista dos dígitos do tempo
        self.numero_placar_list = arcade.SpriteList()       # Lista dos dígitos do placar
        self.numero_record_list = arcade.SpriteList()       # Lista dos dígitos do recorde
        self.lilies_list = arcade.SpriteList()              # Lista dos folhas decorativas
        self.mosca = arcade.Sprite()                        # Sprite da mosca
        self.gameover = arcade.Sprite()                     # Sprite do game over
        self.ponto = arcade.Sprite()                        # Sprite da pontuação

        #variáveis de controle
        self.pode_pular = True                              # indica se o sapo pode saltar
        self.perdeu = False                                 # indica se o jogador perdeu o jogo atual
        self.estado_mosca = 0                               # armazena o estado atual da mosca
        self.contador_mosca = 0                             # contador do número de movimentos da mosca
        self.soma_tempo = 0                                 # armazena o tempo cumulativo
        self.estado_atual = ESPERA                          # armazena o estado do jogo
        #self.primeiro_fila = None                           # armazena o sapo que está na primeira posição da fila
        self.posicao_fila = None                            # armazena as posições dos sapos na fila
        self.flag_movimentando = False                      # indica se os sapos estão se movimentando
        self.mosca_voando = False                           # indica se a mosca está voando
        self.mosca_liberada = False                         # indica se uma nova mosca pode ser criada
        self.tempo_ponto = 0                                # armazena o tempo decorrido desde o ponto
        self.fez_ponto = False                              # indica se o jogador fez ponto
        self.fez_ponto_extra = False                        # indica se o jogador fez ponto extra
        self.primeira_execucao = True                       # indica se é a primeira execução do código
        self.desenha_novo_recorde = False                   # indica quando a mensagem de novo recorde deve aparecer



        #outras definições
        self.X_BASE = 0                                     # armazena a posição base da fila de sapos
        self.Y_BASE = 0                                     # armazena a posição base da fila de sapos
        self.tempo = 0                                      # armazena o tempo restante da partida
        self.record = 0                                     # armazena o maior placar alcançado
        self.screen_width = 0                               # armazena o tamanho da tela
        self.screen_height = 0                              # armazena o tamanho da tela
        self.incremento_angulo = 0                          # armazena o incremento do ângulo da folha

        #efeitos sonoros
        self.som_pulo = None                                # som executado quando o sapo faz um salto
        self.som_ponto = None                               # som executado quando o jogador faz um ponto
        self.som_gameover = None                            # som executado quando o jogador perde a partida
        self.som_ponto_extra = None                         # som executado quando o jagador faz ponto extra

        #imagens
        self.tela_inicial = None                            # imagem exibida como tela inicial
        self.background = None                              # imagem exibida como fundo durante o jogo
        self.dock = None                                    # imagem da plataforma sobre a qual os sapos fica
        self.lily = None                                    # imagem da folha com flor
        self.novo_recorde = None                            # imagem que aparece quando o jogador atinge um novo recorde

        # Esconde o cursor do mouse
        self.set_mouse_visible(False)

    def setup(self):
        """ Configura o jogo e inicializa as variáveis"""

        # encontra o tamanho da tela
        self.screen_width, self.screen_height = self.get_size()
        self.X_BASE = self.screen_width / 2
        self.Y_BASE = self.screen_height / 4

        # inicialização dos Sprites
        # Folha
        self.folha = arcade.Sprite("resources/images/folha1.png", SCALE_FOLHA)
        self.folha.center_y = (self.screen_height / 4) * 3
        self.folha.center_x = self.screen_width / 2
        self.folha.collision_radius = RAIO_COLISAO_FOLHA

        # Sapos
        self.primeiro_fila = 0
        self.posicao_fila = preenche_posicao_fila(NUM_SAPOS, OFFSET_FILA, self.X_BASE, self.Y_BASE)
        for i in range(NUM_SAPOS):
            sapo = arcade.Sprite() #("sapo.png", SCALE_SAPO)
            sapo.append_texture(arcade.load_texture("resources/images/sapo.png", scale=SCALE_SAPO))
            sapo.append_texture(arcade.load_texture("resources/images/sapo1.png", scale=SCALE_SAPO))
            sapo.append_texture(arcade.load_texture("resources/images/sapo2.png", scale=SCALE_SAPO))
            sapo.append_texture(arcade.load_texture("resources/images/sapo3.png", scale=SCALE_SAPO))
            sapo.append_texture(arcade.load_texture("resources/images/sapo_lingua.png", scale=SCALE_SAPO))
            sapo.set_texture(1)
            sapo.center_x = self.posicao_fila[i][0]
            sapo.center_y = self.posicao_fila[i][1]
            sapo.x0 = sapo.center_x
            sapo.y0 = sapo.center_y
            sapo.collision_radius = 15
            sapo.velocidade = 0
            sapo.contador = 1   #variável auxiliar que será usada para lógica de animação durante o pulo
            self.sapo_list.append(sapo)

        # Números
        self.numero_tempo_list = cria_sprite_numero(self.folha.center_x - 30,
                                                    self.folha.center_y + 30,
                                                    self.folha.center_x + 30,
                                                    self.folha.center_y + 30,
                                                    SCALE_NUM_TEMPO)

        self.numero_placar_list = cria_sprite_numero(self.folha.center_x - 12,
                                                     self.folha.center_y - 70,
                                                     self.folha.center_x + 12,
                                                     self.folha.center_y - 70,
                                                     SCALE_NUM_PLACAR)

        self.numero_record_list = cria_sprite_numero(self.screen_width / 8,
                                                     self.screen_height * 3 / 4,
                                                     self.screen_width / 8 + 40,
                                                     self.screen_height * 3 / 4,
                                                     SCALE_NUM_RECORD)

        # Lilies
        if self.primeira_execucao:
            for i in range(NUM_LILIES):
                lily = arcade.Sprite()
                lily.append_texture(arcade.load_texture("resources/images/lily" + str(random.randrange(1, 3)) + ".png",
                                                        scale=SCALE_LILIES))
                lily.set_texture(0)
                lily.angle = random.randrange(360)
                aux = random.randrange(2)
                lily.center_x = aux*random.randrange(self.screen_width//3)\
                                +(1-aux)*random.randrange(self.screen_width*2//3, self.screen_width)
                lily.center_y = random.randrange(self.screen_height//2)
                self.lilies_list.append(lily)
        self.primeira_execucao = False

        # Game Over
        self.gameover = arcade.Sprite("resources/images/game_over.png", SCALE_GAMEOVER)
        self.gameover.center_y = random.randrange(self.screen_height)
        self.gameover.center_x = -200

        # Pontuação
        self.ponto = arcade.Sprite()
        self.ponto.append_texture(arcade.load_texture("resources/images/Numeros/_1.png", scale=SCALE_PONTO))
        self.ponto.append_texture(arcade.load_texture("resources/images/Numeros/_2.png", scale=SCALE_PONTO))
        self.ponto.append_texture(arcade.load_texture("resources/images/Numeros/_3.png", scale=SCALE_PONTO))
        self.ponto.append_texture(arcade.load_texture("resources/images/Numeros/_4.png", scale=SCALE_PONTO))
        self.ponto.append_texture(arcade.load_texture("resources/images/Numeros/_5.png", scale=SCALE_PONTO))
        self.ponto.set_texture(0)
        self.ponto.center_x = self.folha.center_x + 100
        self.ponto.center_y = self.folha.center_y - 200
        self.ponto.alpha = 0

        self.incremento_angulo = VELOCIDADE_INICIAL
        self.tempo = 60
        self.placar = 0

        # Imagens
        self.background = arcade.load_texture("resources/images/water.png")
        self.dock = arcade.load_texture("resources/images/dock.png", scale=SCALE_DOCK)
        self.tela_inicial = arcade.load_texture("resources/images/tela_inicial2.png")
        self.lily = arcade.load_texture("resources/images/lily_flower.png")
        self.novo_recorde = arcade.load_texture("resources/images/recorde.png")

        # Efeitos sonoros
        self.som_pulo = arcade.load_sound("resources/sound/pulo.wav")
        self.som_ponto = arcade.load_sound("resources/sound/ponto.wav")
        self.som_gameover = arcade.load_sound("resources/sound/pulo.wav")#game_over.mp3")
        self.som_ponto_extra = arcade.load_sound("resources/sound/pulo.wav")#ponto_extra.mp3")

    def draw_initial_screen(self):
        """ Função que desenaha a tela inicial """
        page_texture = self.tela_inicial
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2,
                                      self.screen_width, self.screen_height, page_texture, 0)

    def draw_game(self):
        """ Função que desenha os elementos do jogo """

        #imagem de fundo e plataforma
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2,
                                      self.screen_width, self.screen_height, self.background)
        arcade.draw_texture_rectangle(self.screen_width//2,self.screen_height//7,
                                      200, 500, self.dock)
        if self.desenha_novo_recorde:
            arcade.draw_texture_rectangle(self.numero_record_list[0].center_x + 20,
                                          self.numero_record_list[0].center_y - 80,
                                          100, 100, self.novo_recorde)
        #arcade.draw_texture_rectangle(self.screen_width / 4, self.screen_height * 3 / 4, 200, 200, self.lily)

        #demais Sprites
        self.folha.draw()
        self.sapo_list.draw()
        self.sapo_folha.draw()
        self.numero_tempo_list.draw()
        self.numero_placar_list.draw()
        self.lilies_list.draw()
        self.numero_record_list.draw()
        self.gameover.draw()
        self.ponto.draw()
        if self.mosca_voando:
            self.mosca.draw()

        # Put the text on the screen.
        #output = f"Tempo: {self.tempo}"
        #arcade.draw_text(output, self.folha.center_x - 40, self.folha.center_y - 5, arcade.color.WHITE, 14)

        # Elementos textuais
        arcade.draw_text("TEMPO", self.folha.center_x - 25, self.folha.center_y + 80, arcade.color.YELLOW, 14)
        arcade.draw_text("PLACAR", self.folha.center_x - 30, self.folha.center_y - 50, arcade.color.YELLOW, 14)
        arcade.draw_text("RECORDE", self.numero_record_list[1].center_x - 70,
                         self.numero_record_list[1].center_y + 40, arcade.color.YELLOW, 20)


        #arcade.draw_text(self.texto_gameover, 50, 50, arcade.color.BRIGHT_TURQUOISE, 30)

    def on_draw(self):
        """ Função que chama a função de draw específica de cada estado do jogo """

        # inicia a renderização
        arcade.start_render()

        #verifica o estado do jogo e chama a função correspondente
        if self.estado_atual == ESPERA:
            self.draw_initial_screen()
        elif self.estado_atual == JOGO:
            self.draw_game()
        elif self.estado_atual == GAME_OVER:
            self.draw_game()
        else:
            self.draw_game()

    def update(self, delta_time):
        """ Movement and game logic """

        # verifica se o estado atual é o de GAME OVER
        if self.estado_atual == GAME_OVER:
            self.gameover.update()                                  #atualiza o sprite do gameover
            self.soma_tempo += delta_time                           #atualiza o tempo decorrido desde o gameover

            if self.gameover.center_x > self.folha.center_x + 10:   #verifica se o sprite chegou na posição final
                self.gameover.change_x = 0                          #caso seja verdade, o faz parar
                self.gameover.change_y = 0

            if self.soma_tempo >= 5:                                #verifica se o tempo decorrido é >= 5s
                self.soma_tempo = 0                                 #se for, zera o acumulador de tempo
                self.estado_atual = ESPERA                          #atualiza o estado do jogo
                self.reset_game()                                   #chama a função para resetar o jogo

        # verifica se o estado atual é o de JOGO
        if self.estado_atual == JOGO:

            self.sapo_list.update()                                 #atualiza os Sprites
            self.sapo_folha.update()
            self.mosca.update()

            self.soma_tempo += delta_time                           #atualiza o acumulador de tempo
            if self.soma_tempo >= 1:                                #verifica se o tempo decorrido é >= 1s
                self.soma_tempo = 0                                 #reseta o acumulador de tempo
                self.tempo -= 1                                     #decrementa a variável tempo
                dig1, dig2 = quebra_numero(self.tempo)              #atualiza os dígitos do tempo
                self.numero_tempo_list[0].set_texture(dig1)
                self.numero_tempo_list[1].set_texture(dig2)

            self.folha.angle += self.incremento_angulo              #atualiza o ângulo da folha

            #atualiza as posições de todos os sapos
            for index in range(len(self.sapo_list)):
                self.sapo_list[index].center_y += self.sapo_list[index].velocidade
            if self.sapo_list[0].velocidade > 0:                    # verifica se o primeiro sapo está em movimento
                self.sapo_list[0].contador += 1                     # incrementa o contador
            #lógica para a execução da animação do sapo durante o pulo
            if (self.sapo_list[0].contador % 10) == 0:
                if self.sapo_list[0].cur_texture_index == 0 or self.sapo_list[0].cur_texture_index == 2:
                    self.sapo_list[0].set_texture(3)
                else:
                    self.sapo_list[0].set_texture(2)

            #verifica quando o sapo chega na primeira posição da fila e seta velocidade = 0
            if self.flag_movimentando:
                if self.sapo_list[1].center_y >= self.Y_BASE:
                    for index in range(1, len(self.sapo_list)):
                        self.sapo_list[index].velocidade = 0
                        self.sapo_list[index].set_texture(1)
                    self.flag_movimentando = False

            #verifica se um sapo encostou em outro sapo
            sapo_hit_sapo = arcade.check_for_collision_with_list(self.sapo_list[0], self.sapo_folha)
            # se a lista de sapos que encostaram um no outro é diferente de vazia ou se o tempo acabou, o jogo acaba
            if sapo_hit_sapo or self.tempo == 0:
                self.estado_atual = GAME_OVER                       #atualiza o estado do jogo
                self.soma_tempo = 0                                 #zera o contador de tempo
                self.gameover.change_x, self.gameover.change_y = calcula_incremento(self.folha.center_x, self.folha.center_y,
                                                                self.gameover.center_x, self.gameover.center_y,
                                                                10) #calcula o incremento na posição do Sprite gameover
                arcade.play_sound(self.som_gameover)            #executa o som de gameover
                self.perdeu = True                              #seta a flag perdeu
                if self.mosca_voando:
                        self.estado_mosca = 4
                        self.mosca_liberada = False
                if self.placar > self.record:                   #verifica se o placar obtido é maior que o recorde
                    self.record = self.placar                   #atualiza o recorde
                    dig1, dig2 = quebra_numero(self.record)     #atualiza os dígitos do placar
                    self.numero_record_list[0].set_texture(dig1)
                    self.numero_record_list[1].set_texture(dig2)
                    self.desenha_novo_recorde = True

            # verifica se o sapo encostou na folha
            if not self.perdeu: # se o sapo não encostou em outro sapo, verifica se ele encostou na folha
                sapo_hit_folha = arcade.check_for_collision_with_list(self.folha, self.sapo_list)
                for sapo in sapo_hit_folha: #se o sapo encostou na folha
                    self.incremento_angulo *= -1 * INCREMENTO_VELOCIDADE #atualiza a velocidade do giro da folha
                    sapo.set_texture(0)                                 #atualiza a imagem do sapo
                    self.sapo_folha.append(sapo)                        #coloca o sapo na lista de sapos que estão na folha
                    self.sapo_list.remove(sapo)                         #remove o sapo da lista de sapos da fila
                    self.pode_pular = True                              #seta a flag pode_pular
                    sapo.velocidade = 0                                 #atualiza a velocidade do sapo
                    self.mosca_liberada = True                          #libera a criação de uma nova mosca
                    self.fez_ponto = True
                    if not self.fez_ponto_extra:
                        self.placar += 1  # atualiza o placar
                        arcade.play_sound(self.som_ponto)
                    dig1, dig2 = quebra_numero(self.placar)  # atualiza os dígitos do placar
                    self.numero_placar_list[0].set_texture(dig1)
                    self.numero_placar_list[1].set_texture(dig2)

            if self.fez_ponto:
                self.tempo_ponto += delta_time
                if self.ponto.alpha < 255 and self.tempo_ponto < 0.5:
                    self.ponto.alpha += 1
                elif self.ponto.alpha > 0 and self.tempo_ponto >= 0.5:
                     self.ponto.alpha -= 1
                elif self.tempo_ponto >= 1:
                    self.fez_ponto = False
                    self.fez_ponto_extra = False
                    self.tempo_ponto = 0
                    self.ponto.set_texture(0)

            # atualiza as posições dos sapos que já chegaram nas folhas
            for sapo in self.sapo_folha:
                angulo_rot, x, y = atualiza_posicao(self.incremento_angulo,
                                                    sapo.center_x,
                                                    sapo.center_y,
                                                    self.folha.center_x,
                                                    self.folha.center_y)#calcula o angulo e coordenadas do sapo
                sapo.angle = int(angulo_rot)                                 #atualiza o ângulo e posição
                sapo.center_x = x
                sapo.center_y = y


            if ((self.placar+1) % 4) == 0 and self.mosca_liberada:
                self.mosca_liberada = False
                if not self.mosca_voando:
                    self.cria_mosca()
            if self.mosca_voando:
                sapo_acertou_mosca = arcade.check_for_collision(self.sapo_list[0], self.mosca)
                if sapo_acertou_mosca:
                    self.placar += PONTUACAO_EXTRA  # atualiza o placar
                    dig1, dig2 = quebra_numero(self.placar)  # atualiza os dígitos do placar
                    self.numero_placar_list[0].set_texture(dig1)
                    self.numero_placar_list[1].set_texture(dig2)
                    arcade.play_sound(self.som_ponto_extra)
                    self.fez_ponto = True
                    self.fez_ponto_extra = True
                    self.estado_mosca = 4
                    self.ponto.set_texture(PONTUACAO_EXTRA - 1)
                if self.estado_mosca == 0:
                    self.mosca.change_x, self.mosca.change_y = calcula_incremento(self.screen_width * 3 / 4,
                                                                                  self.screen_height / 2,
                                                                                  self.mosca.center_x,
                                                                                  self.mosca.center_y,
                                                                                  10)
                    if self.mosca.center_x <= self.screen_width * 3 / 4:
                        self.estado_mosca = 1
                elif self.estado_mosca == 1:
                    self.mosca.change_x = -10
                    self.mosca.change_y = 0
                    self.mosca.set_texture(0)
                    if self.mosca.center_x <= self.screen_width / 4:
                        if self.contador_mosca < 2:
                            self.estado_mosca = 2
                            self.mosca.change_x *= -1
                            self.mosca.set_texture(1)
                            self.contador_mosca += 1
                            self.mosca.set_texture(1)
                        else:
                            self.estado_mosca = 3
                            self.mosca.set_texture(0)
                elif self.estado_mosca == 2:
                    if self.mosca.center_x >= self.screen_width * 3 / 4:
                        self.estado_mosca = 1
                elif self.estado_mosca == 3:
                    self.mosca.change_x, self.mosca.change_y = calcula_incremento(-30,
                                                                                  self.screen_height * 4 / 5,
                                                                                  self.mosca.center_x,
                                                                                  self.mosca.center_y,
                                                                                  10)
                    if self.mosca.center_x <= -20:
                        self.mosca.change_x = 0
                        self.mosca.change_y = 0
                        self.estado_mosca = 4
                elif self.estado_mosca == 4:
                    self.estado_mosca = 5
                    self.mosca_voando = False
                    self.mosca.kill()



    def cria_mosca(self):
        self.mosca.append_texture(arcade.load_texture("resources/images/mosca.png", scale=SCALE_MOSCA))
        self.mosca.append_texture(arcade.load_texture("resources/images/mosca2.png", scale=SCALE_MOSCA * 0.65))
        self.mosca.set_texture(0)
        self.mosca.center_x = self.screen_width + 100
        self.mosca.center_y = random.randrange(self.screen_height)
        self.contador_mosca = 0
        self.mosca_voando = True
        self.estado_mosca = 0


    # Função chamada quando alguma tecla do teclado é pressionada
    def on_key_press(self, key, modifiers):
        #se tecla1, inicia o jogo
        if key == TECLA1:
            if not self.perdeu:
                self.estado_atual = JOGO

        #se tecla2
        if key == TECLA2:
            if self.estado_atual == JOGO:
                if self.pode_pular:                                         #verifica se o sapo pode saltar
                    for index in range(len(self.sapo_list)):                #para cada um dos sapos na fila
                        self.sapo_list[index].velocidade = VELOCIDADE_SAPO  #atualiza velocidade dos sapos
                        self.sapo_list[index].set_texture(0)                #atualiza imagem dos sapos
                        self.flag_movimentando = True                       #seta a flag_movimentando
                    arcade.play_sound(self.som_pulo)                        #executa o som do pulo
                    self.pode_pular = False                                 #reseta a flag pode_pular

        #se tecla3
        if key == TECLA3:
            arcade.finish_render()
            arcade.close_window()

        # def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        # self.sapo_list[0].center_x = x
        # self.sapo_list[0].center_y = y

    def reset_game(self):

        self.flag_movimentando = False
        self.pode_pular = True
        self.perdeu = False
        self.sapo_list = arcade.SpriteList()

        self.sapo_folha = arcade.SpriteList()
        self.incremento_angulo = VELOCIDADE_INICIAL

        self.primeiro_fila = 0

        # placar
        self.placar = 0
        self.tempo = 60
        self.desenha_novo_recorde = False
        self.fez_ponto = False
        self.fez_ponto_extra = False
        #self.primeiro_fila = 0

        self.setup()

        dig1, dig2 = quebra_numero(self.record)                     #atualiza os dígitos do recorde
        self.numero_record_list[0].set_texture(dig1)
        self.numero_record_list[1].set_texture(dig2)


def main():
    """ Main method """
    window = FrogAround()
    window.setup()
    arcade.run()


def calcula_incremento(x0, y0, x1, y1, fator):
    angulo = math.atan2(y0 - y1, x0 - x1)
    x2 = fator * math.cos(angulo)
    y2 = fator * math.sin(angulo)
    return x2, y2

def cria_sprite_numero(x_dezena, y_dezena, x_unidade, y_unidade, escala):
    num_list = arcade.SpriteList()

    digito_dezena = arcade.Sprite()
    for j in range(10):
        digito_dezena.append_texture(arcade.load_texture("resources/images/Numeros/" + str(j) + ".png", scale=escala))
    digito_dezena.set_texture(0)
    digito_dezena.center_x = x_dezena
    digito_dezena.center_y = y_dezena
    num_list.append(digito_dezena)

    digito_unidade = arcade.Sprite()
    for j in range(10):
        digito_unidade.append_texture(arcade.load_texture("resources/images/Numeros/" + str(j) + ".png", scale=escala))
    digito_unidade.set_texture(0)
    digito_unidade.center_x = x_unidade
    digito_unidade.center_y = y_unidade
    num_list.append(digito_unidade)

    return num_list


def preenche_posicao_fila(num_sapos, offset, x_base, y_base):
    fila = [[0 for col in range(2)] for row in range(num_sapos)]


    for i in range(num_sapos):
        fila[i][0] = x_base
        fila[i][1] = y_base + i*offset

    return fila

def atualiza_posicao(angulo, x1, y1, x0, y0):
    """função que calcula a nova posição dos sapos que já estão na folha
        -Argumentos
        angulo: diferença de ângulo desde a última atualização
        x1, y1: posição atual do sapo
        x0, y0: ponto em relação ao qual será feita a translação
        -Saída
        angulo_rot: ângulo em que o sapo deve girar em torno do próprio eixo
        x2, y2: nova posição do sapo
    """
    angulo = angulo * math.pi / 180 #transforma o angulo em radianos
    x = x1 - x0
    y = y1 - y0
    x2 = (x * math.cos(angulo) - y * math.sin(angulo)) + x0
    y2 = (y * math.cos(angulo) + x * math.sin(angulo)) + y0
    sinal = (angulo / abs(angulo))
    angulo_rot = math.atan2((y2 - y1), (x2 - x1))

    if sinal == -1:
        angulo_rot = (angulo_rot * 180 // math.pi) + 180
    else:
        angulo_rot = (angulo_rot * 180 // math.pi)

    return angulo_rot, x2, y2

def quebra_numero(numero):
    dig1 = numero//10
    dig2 = numero - (dig1 * 10)
    return dig1, dig2

if __name__ == "__main__":
    main()
