import sys
from time import time 
from typing import Tuple
from mapa import Mapa, TileType
import pygame

from configJogo import ConfigJogo

class CenaPrincipal():
    def __init__(self, tela: pygame.display):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False

    def rodar(self):
        while not self.encerrada:
            self.mapa.desenha(self.tela)
            self.tratamento_eventos()

    def tratamento_eventos(self):
        pygame.event.get()

        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)