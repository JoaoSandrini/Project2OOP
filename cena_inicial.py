import sys
import pygame

from config_jogo import ConfigJogo
from utils import ler_imagem
from cronometro import Cronometro

class CenaInicial:
    def __init__(self, tela: pygame.display):
        self.tela = tela
        self.encerrada = False

        # cria os textos que serao mostrados na tela
        fonte_subtitulo = pygame.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.subtitulos = [fonte_subtitulo.render(f'Modo 1 Jogador: Pressione F1', True, ConfigJogo.COR_SUBTITULO), fonte_subtitulo.render(f'Modo 2 Jogadores: Pressione F2', True, ConfigJogo.COR_SUBTITULO)]

        # variaveis usadas para fazer o subtitulo piscar
        self.cronometro = Cronometro()
        self.mostrar_subtitulo = True

    def rodar(self):
        while not self.encerrada:
            self.tratamento_eventos()
            self.atualiza_estado()
            self.desenha()

    def tratamento_eventos(self):
        pygame.event.get()

        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)

        # evento de prosseguimento
        if pygame.key.get_pressed()[pygame.K_F1]:
            self.num_jogadores = 1
            self.encerrada = True

        if pygame.key.get_pressed()[pygame.K_F2]:
            self.num_jogadores = 2
            self.encerrada = True
 
    def atualiza_estado(self):
        if self.cronometro.tempo_passado() > 0.35:
            self.mostrar_subtitulo = not self.mostrar_subtitulo
            self.cronometro.reset()

    def desenha(self):
        self.tela.fill(ConfigJogo.COR_INICIO)
        self.desenha_titulo(self.tela)
        self.desenha_subtitulos(self.tela)
        pygame.display.flip()

    def desenha_titulo(self, tela):
        # desenha o titulo no meio da tela
        self.img_titulo = ler_imagem('telas/logo.png', (ConfigJogo.LARGURA_LOGO, ConfigJogo.ALTURA_LOGO))
        px = (ConfigJogo.LARGURA_TELA - ConfigJogo.LARGURA_LOGO)//2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.img_titulo, (px, py))

    def desenha_subtitulos(self, tela):
        if self.mostrar_subtitulo:
            # desenha os subtitulos
            espacamento_y = ConfigJogo.ESPACO_SUBTITULO
            for subtitulo in self.subtitulos:
                px1 = (ConfigJogo.LARGURA_TELA - subtitulo.get_size()[0]) // 2
                py1 = (espacamento_y * ConfigJogo.ALTURA_TELA // 2)
                tela.blit(subtitulo, (px1, py1))
                espacamento_y += 0.2
