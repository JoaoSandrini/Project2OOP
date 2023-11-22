import sys
from time import time 
from typing import Tuple
from mapa import Mapa, TileType
from personagem import Personagem
import pygame

from config_jogo import ConfigJogo

class CenaPrincipal():
    def __init__(self, tela: pygame.display, num_jogadores: int):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False

        if num_jogadores == 1:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
            self.p2 = False
        else:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)

            self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE))
            while(self.p1.pIdx == self.p2.pIdx):
                self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE))

    def rodar(self):
        while not self.encerrada:
            self.mapa.desenha(self.tela)
            self.p1.tratamento_eventos() 
            self.tratamento_eventos()
            self.p1.desenha(self.tela)
            if self.p2:
                self.p2.desenha(self.tela)               

            pygame.display.flip()

    def tratamento_eventos(self):
        pygame.event.get()

        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)