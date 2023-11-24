import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
import time
from enum import Enum

class Direcao(Enum):
    ESQUERDA = 0
    DIREITA = 1
    BAIXO = 2
    CIMA = 3
class Aienigena:
    def __init__(self, mapa: Mapa, tela: pygame.Surface) -> None:
        self.img_alien= ler_imagem('enemies/enemy-alien.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        self._mapa = mapa
        self._x = 288
        self._y = ConfigJogo.ALTURA_MENU + 224
        self._idx_movimento = random.randint(Direcao.ESQUERDA.value, Direcao.CIMA.value)
        
        self.tela = tela

        self._time_last_move = 0
        
    def desenha(self):
        self.tela.blit(self.img_alien, (self._x, self._y))

    def tratamento_eventos(self):

        if time.time() - self._time_last_move > ConfigJogo.CD_ALIEN:

            new_x = self._x
            new_y = self._y

            if self._idx_movimento == Direcao.ESQUERDA.value:
                new_x -= ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.DIREITA.value:
                new_x += ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.BAIXO.value:
                new_y += ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.CIMA.value:
                new_y -= ConfigJogo.VELOCIDADE_ALIEN

            if not self._mapa.is_any_wall(new_x, new_y):
                self._x = new_x
                self._y = new_y
                self._time_last_move = time.time()
            else:
                self._idx_movimento = random.randint(0, 3)