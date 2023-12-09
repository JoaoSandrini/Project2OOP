from utils import ler_imagem
from config_jogo import ConfigJogo
import time
import pygame
from enum import Enum
from mapa import Mapa
import random
class Direcao(Enum):
    ESQUERDA = 0
    DIREITA = 1
    BAIXO = 2
    CIMA = 3
class Projetil:
    def __init__(self, x: int, y: int, mapa: Mapa):
        self._mapa = mapa
        self._x = x
        self._y = y
        self.colisao = pygame.Rect(self._x, self._y, ConfigJogo.LARGURA_PROJETIL, ConfigJogo.ALTURA_PROJETIL)
        self._time_last_move = 0 
        self.colidido = False
        self._idx_movimento = random.randint(Direcao.ESQUERDA.value, Direcao.CIMA.value)

    def tratamento_eventos(self):
        if time.time() - self._time_last_move >= ConfigJogo.CD_SHOT_MOVE:
            new_x = self._x
            new_y = self._y

            if self._idx_movimento == Direcao.ESQUERDA.value:
                new_x -= ConfigJogo.VELOCIDADE_PROJETIL

            elif self._idx_movimento == Direcao.DIREITA.value:
                new_x += ConfigJogo.VELOCIDADE_PROJETIL

            elif self._idx_movimento == Direcao.BAIXO.value:
                new_y += ConfigJogo.VELOCIDADE_PROJETIL

            elif self._idx_movimento == Direcao.CIMA.value:
                new_y -= ConfigJogo.VELOCIDADE_PROJETIL

            if not self._mapa.is_fixed_wall(new_x, new_y):
                self._x = new_x
                self._y = new_y
                self._time_last_move = time.time()
                
            else:
                self.colidido = True

    def desenha(self, tela: pygame.Surface):
        rect = None
        if self._idx_movimento == Direcao.ESQUERDA.value or self._idx_movimento == Direcao.DIREITA.value:
            rect = (self._x, (self._y + ConfigJogo.TAM_TILE//2) - ConfigJogo.ALTURA_PROJETIL//2, ConfigJogo.LARGURA_PROJETIL, ConfigJogo.ALTURA_PROJETIL)
        elif self._idx_movimento == Direcao.BAIXO.value or self._idx_movimento == Direcao.CIMA.value:
            rect = ((self._x + ConfigJogo.TAM_TILE//2) - ConfigJogo.ALTURA_PROJETIL//2, self._y, ConfigJogo.ALTURA_PROJETIL, ConfigJogo.LARGURA_PROJETIL)
        pygame.draw.rect(tela, 'red', rect)
        self.colisao = pygame.Rect(self._x, self._y, ConfigJogo.LARGURA_PROJETIL, ConfigJogo.ALTURA_PROJETIL)
