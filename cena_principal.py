import sys
from time import time 
from typing import Tuple
from mapa import Mapa, TileType
from personagem import Personagem
import pygame
from utils import ler_imagem
from cronometro import Cronometro

from config_jogo import ConfigJogo

class CenaPrincipal():
    def __init__(self, tela: pygame.display, num_jogadores: int):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False

        self.cronometro = Cronometro()

        self.fonte_hud = pygame.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.img_relogio = ler_imagem('telas/relogio.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        if num_jogadores == 1:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela)
            self.p2 = False
        else:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela)

            self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela)
            while(self.p1.pIdx == self.p2.pIdx):
                self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela)

    def rodar(self):
        while not self.encerrada:
            self.desenha_menu()
            self.mapa.desenha(self.tela)
            self.p1.tratamento_eventos(1) 
            self.tratamento_eventos()
            self.p1.desenha()

            if self.p2:
                self.p2.tratamento_eventos(2)
                self.p2.desenha()     

            
            for bomba in self.p1.bombas:
                bomba.desenha(self.tela)

            if self.p2:
                for bomba in self.p2.bombas:
                    bomba.desenha(self.tela)
       
            pygame.display.flip()

    def tratamento_eventos(self):
        pygame.event.get()

        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)

    def desenha_menu(self):
        pygame.draw.rect(self.tela, 'blue', (0, 0, ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_MENU))
        pygame.draw.rect(self.tela, 'green', (0, 0, ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_MENU), 4)

        fonte_hud = pygame.font.SysFont(None, ConfigJogo.FONTE_HUD)
        tempo_restante = int(120 - self.cronometro.tempo_passado())
        minutos =  tempo_restante // 60
        segundos =  tempo_restante % 60

        if segundos >= 10:
            mostra_tempo = fonte_hud.render(f'{minutos:.0f}:{segundos:.0f}', True, ConfigJogo.COR_FONTE_HUD)
        else:
            mostra_tempo = fonte_hud.render(f'{minutos:.0f}:0{segundos:.0f}', True, ConfigJogo.COR_FONTE_HUD)
        self.tela.blit(mostra_tempo, (ConfigJogo.LARGURA_TELA * .12, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
        self.tela.blit(self.img_relogio, (ConfigJogo.LARGURA_TELA * .05, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))


        if not self.p2:
            self.tela.blit(self.p1.personagem, (ConfigJogo.LARGURA_TELA * .5, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            mostra_pont_p1 = fonte_hud.render(f'{self.p1.pontos}', True, ConfigJogo.COR_FONTE_HUD)
            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.img_relogio, (ConfigJogo.LARGURA_TELA * .05, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            
        
        else:
            mostra_pont_p1 = fonte_hud.render(f'{self.p1.pontos}', True, ConfigJogo.COR_FONTE_HUD)
            mostra_pont_p2 = fonte_hud.render(f'{self.p2.pontos}', True, ConfigJogo.COR_FONTE_HUD)

            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(mostra_pont_p2, (ConfigJogo.LARGURA_TELA * .82, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.p1.personagem, (ConfigJogo.LARGURA_TELA * .5, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(self.p2.personagem, (ConfigJogo.LARGURA_TELA * .75, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
