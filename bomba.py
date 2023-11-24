import pygame
from config_jogo import ConfigJogo
from utils import ler_imagem
from cronometro import Cronometro
import time
class Bomba:
    def __init__(self, x: int, y: int, ) -> None:
        self.img_bomba = ler_imagem('items/bomba.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.duracao = ConfigJogo.DURACAO_BOMBA
        self.alcance = ConfigJogo.ALCANCE_BOMBA
        self._x = x
        self._y = y
        self.time_lancamento = time.time()  
        self.explodida = False

    def atualizar(self):
        tempo_atual = time.time()

        if tempo_atual - self.time_lancamento > self.duracao:
            self.explodida = True

    def desenha(self, tela: pygame.Surface):
        self.atualizar()
        if not self.explodida:
            tela.blit(self.img_bomba, (self._x, self._y))


