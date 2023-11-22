import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
import time
class Personagem:
    def __init__(self, mapa: Mapa, x: int, y: int) -> None:
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
        
        self._time_last_move = 0

    def desenha(self, tela: pygame.Surface):
        tela.blit(self.personagem, (self._x, self._y))

    def tratamento_eventos(self):
        if time.time() - self._time_last_move > 0.01:
        
            new_y = self._y
            new_x = self._x

            if pygame.key.get_pressed()[pygame.K_a]:
                new_x = self._x - ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_d]:
                new_x = self._x + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_s]:
                new_y = self._y + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_w]:
                new_y = self._y - ConfigJogo.VELOCIDADE_PERSONAGEM
            
            if not self._mapa.is_wall(new_x, new_y):
                self._x = new_x
                self._y = new_y
                self._time_last_move = time.time()
        