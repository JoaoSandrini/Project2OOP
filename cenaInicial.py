import sys
import pygame

from configJogo import ConfigJogo
from lerImagem import lerImagem
from cronometro import Cronometro

class CenaInicial:
    def __init__(self, tela):
        self.tela = tela
        self.encerrada = False

        # cria os textos que serao mostrados na tela
        fontSubtitulo = pygame.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.subtitulos = [fontSubtitulo.render(f'Modo 1 Jogador: Pressione F1', True, ConfigJogo.COR_SUBTITULO), fontSubtitulo.render(f'Modo 2 Jogadores: Pressione F2', True, ConfigJogo.COR_SUBTITULO)]

        # variaveis usadas para fazer o subtitulo piscar
        self.cronometro = Cronometro()
        self.mostrarSubtitulo = True

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
        if pygame.key.get_pressed()[pygame.K_1]:
            self.encerrada = True
        
        if pygame.key.get_pressed()[pygame.K_2]:
            self.encerrada = True

    def atualiza_estado(self):
        if self.cronometro.tempo_passado() > 0.35:
            self.mostrarSubtitulo = not self.mostrarSubtitulo
            self.cronometro.reset()

    def desenha(self):
        self.tela.fill(ConfigJogo.COR_INICIO)
        self.desenha_titulo(self.tela)
        self.desenha_subtitulos(self.tela)
        pygame.display.flip()

    def desenha_titulo(self, tela):
        # desenha o titulo no meio da tela
        self.imgTitulo = lerImagem('telas/logo.png', (ConfigJogo.LARGURA_LOGO, ConfigJogo.ALTURA_LOGO))
        px = (ConfigJogo.LARGURA_TELA - ConfigJogo.LARGURA_LOGO)//2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.imgTitulo, (px, py))

    def desenha_subtitulos(self, tela):
        if self.mostrarSubtitulo:
            # desenha os subtitulos
            espacamentoy = ConfigJogo.ESPACO_SUBTITULO
            for subtitulo in self.subtitulos:
                px1 = (ConfigJogo.LARGURA_TELA - subtitulo.get_size()[0]) // 2
                py1 = (espacamentoy * ConfigJogo.ALTURA_TELA // 2)
                tela.blit(subtitulo, (px1, py1))
                espacamentoy += 0.2
