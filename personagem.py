import time
import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
from bomba import Bomba

class Personagem:
    def __init__(self, mapa: Mapa, x: int, y: int,  tela: pygame.Surface) -> None:
        self._bomberman_b = ler_imagem('chars/bomberman-white.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_l = ler_imagem('chars/bomberman-orange.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_p = ler_imagem('chars/bomberman-black.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_a = ler_imagem('chars/bomberman-blue.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._sprites = [self._bomberman_a, self._bomberman_b, self._bomberman_l, self._bomberman_p]

        self.pIdx = random.randint(0, 3)
        self.personagem = self._sprites[self.pIdx]
        self._mapa = mapa
        self._x = x
        self._y = y
        self.pontos = 0
        self.colisao = self.personagem.get_rect(topleft=(self._x, self._y))
        self.inalvejavel = True
        
        self.vida = 3

        self._time_last_move = 0
        self.time_inalvejavel = time.time()
        self.tela = tela
        
        self.bombas: Bomba = []

    def desenha(self):
        self.tela.blit(self.personagem, (self._x, self._y))

    def soltar_bomba(self):
        if len(self.bombas) < ConfigJogo.MAX_BOMBA:
            bomba = Bomba(self, self._x+ConfigJogo.TAM_TILE/2, self._y+ConfigJogo.TAM_TILE/2)
            if bomba.verificar():
                self.bombas.append(bomba)

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y